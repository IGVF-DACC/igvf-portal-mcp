# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "igvf-client==117.0.0",
#   "mcp[cli]==1.26.0",
# ]
# ///
"""
MCP server for the IGVF Data Portal.

Authentication (optional, for unreleased data):
  export IGVF_ACCESS_KEY=your_key
  export IGVF_SECRET_ACCESS_KEY=your_secret

Portal host (optional, defaults to production):
  export IGVF_HOST=https://api.sandbox.igvf.org  # sandbox
"""

import inspect
import json
import os
import typing

from mcp.server.fastmcp import FastMCP

import igvf_client
from igvf_client import ApiClient, Configuration, IgvfApi
from igvf_client.models.item_type import ItemType


mcp = FastMCP(
    "igvfd",
    instructions=(
        "Tools for querying the IGVF Data Portal. "
        "Use `igvf_portal_search` to find items, `igvf_portal_get_by_id` to retrieve a specific item "
        "by @id, accession, or UUID, and `igvf_portal_get_schema` to understand a type's fields. "
        "Use `igvf_portal_get_endpoint_params` to discover filter fields for igvf_portal_get_collection "
        "(underscore Python param names). For igvf_portal_search and igvf_portal_report, use real dotted "
        "field names as they appear on items, e.g. 'file_set.@id'."
    ),
)

ITEM_TYPES = sorted(v.value for v in ItemType)

_STANDARD_PARAMS = {"query", "limit", "sort"}


def _api() -> IgvfApi:
    """Build an IgvfApi instance, authenticated if env vars are set."""
    access_key = os.environ.get("IGVF_ACCESS_KEY")
    secret_key = os.environ.get("IGVF_SECRET_ACCESS_KEY")
    host = os.environ.get("IGVF_HOST")
    kwargs = {}
    if access_key and secret_key:
        kwargs["access_key"] = access_key
        kwargs["secret_access_key"] = secret_key
    if host:
        kwargs["host"] = host
    config = Configuration(**kwargs)
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
    if proxy:
        config.proxy = proxy
    ssl_ca_cert = os.environ.get("REQUESTS_CA_BUNDLE") or os.environ.get("SSL_CERT_FILE")
    if ssl_ca_cert:
        config.ssl_ca_cert = ssl_ca_cert
    return IgvfApi(ApiClient(config))


def _to_json(obj) -> str:
    """Serialize an API response object to a JSON string."""
    if hasattr(obj, "to_dict"):
        data = obj.to_dict()
    elif hasattr(obj, "actual_instance"):
        instance = obj.actual_instance
        data = instance.to_dict() if hasattr(instance, "to_dict") else instance
    elif isinstance(obj, list):
        data = [
            item.to_dict() if hasattr(item, "to_dict") else item for item in obj
        ]
    else:
        data = obj
    return json.dumps(data, indent=2, default=str)


def _list_collections(api: IgvfApi) -> list[str]:
    """Return sorted list of public, callable collection names on IgvfApi."""
    return sorted(
        m for m in dir(api)
        if not m.startswith("_")
        and not m.endswith(("_with_http_info", "_without_preload_content"))
        and callable(getattr(api, m))
    )


def _param_type_label(annotation) -> str:
    """Convert a (possibly nested Pydantic/typing) annotation to a simple label."""
    origin = typing.get_origin(annotation)
    args = typing.get_args(annotation)

    # Unwrap Annotated[X, ...] → recurse on X
    if origin is typing.Annotated:
        return _param_type_label(args[0]) if args else "any"

    # Unwrap Optional[X] / Union[X, None] → recurse on first non-None arg
    if origin is typing.Union:
        non_none = [a for a in args if a is not type(None)]
        if non_none:
            return _param_type_label(non_none[0])
        return "any"

    # Unwrap List[X] → list[inner]
    if origin is list:
        inner = _param_type_label(args[0]) if args else "any"
        return f"list[{inner}]"

    # Leaf types
    name = getattr(annotation, "__name__", "") or str(annotation)
    if "Bool" in name or annotation is bool:
        return "bool"
    if "Float" in name or "Int" in name or annotation in (float, int):
        return "number"
    return "str"


def _param_description(annotation) -> str:
    """Extract the Field description string from an Annotated annotation, if present."""
    try:
        import pydantic.fields as pf
        args = typing.get_args(annotation)
        for meta in args[1:]:
            if isinstance(meta, pf.FieldInfo) and meta.description:
                return meta.description
    except Exception:
        pass
    return ""


@mcp.tool()
def igvf_portal_search(
    query: str = "",
    type: list[str] | None = None,
    limit: int | str = 25,
    sort: list[str] | None = None,
    field_filters: dict | None = None,
) -> str:
    """Search the IGVF Data Portal.

    Args:
        query: Free-text search string.
        type: One or more item types to filter by, e.g. ["SequenceFile", "MeasurementSet"].
        limit: Max results to return (default 25). Pass "all" for every result.
        sort: Fields to sort by, e.g. ["-creation_timestamp"]. Prefix with '-' for descending.
        field_filters: Dict of field→value filters. Values can be a single string
                       or a list of strings (translated to repeated query params,
                       e.g. {"file_format": ["bam", "bed"]} → file_format=bam&file_format=bed).
                       Use '!' suffix for negation and 'gte:'/'lte:'/'gt:'/'lt:' for ranges.
                       IMPORTANT: Use real dotted field names as they appear on the items,
                       e.g. {"file_set.@id": "/analysis-sets/IGVFDS3909HJKS/"}, NOT the
                       underscore-based Python parameter names used by igvf_portal_get_collection
                       (e.g. "file_set_id"). Those underscore names only work with
                       igvf_portal_get_collection, not here.
    """
    api = _api()
    results = api.search(
        query=query or None,
        type=type,
        limit=limit,
        sort=sort,
        field_filters=field_filters,
    )
    data = results.to_dict()
    # Summarise each hit so results aren't overwhelming
    hits = data.get("@graph", [])
    summary = {
        "total": data.get("total", 0),
        "returned": len(hits),
        "results": hits,
    }
    return json.dumps(summary, indent=2, default=str)


@mcp.tool()
def igvf_portal_get_by_id(resource_id: str) -> str:
    """Retrieve a single IGVF item by its @id, accession, or UUID.

    Args:
        resource_id: Examples: "/sequence-files/IGVFFI1165AJSO/",
                     "IGVFFI1165AJSO", or a UUID string.
    """
    api = _api()
    result = api.get_by_id(resource_id)
    return _to_json(result)


@mcp.tool()
def igvf_portal_get_schema(item_type: str) -> str:
    """Return the JSON schema for an IGVF item type.

    Args:
        item_type: CamelCase type name, e.g. "SequenceFile", "MeasurementSet".
                   Call igvf_portal_list_item_types to see all valid values.
    """
    api = _api()
    schema = api.schema_for_item_type(ItemType(item_type))
    return json.dumps(schema, indent=2, default=str)


@mcp.tool()
def igvf_portal_list_item_types() -> str:
    """Return a sorted list of all valid IGVF item type names."""
    return json.dumps(ITEM_TYPES, indent=2)


@mcp.tool()
def igvf_portal_get_collection(
    collection: str,
    query: str = "",
    limit: int = 25,
    sort: list[str] | None = None,
    field_filters: dict | None = None,
) -> str:
    """List items from a specific IGVF collection endpoint.

    Call igvf_portal_get_endpoint_params first to discover which fields are available
    as filters for the given collection.

    Args:
        collection: Snake-case collection name, e.g. "sequence_files",
                    "measurement_sets", "genes", "tissues".
        query: Optional free-text filter.
        limit: Max results (default 25).
        sort: Sort fields, e.g. ["-creation_timestamp"].
        field_filters: Dict of underscore Python parameter names→value filters.
                       Use igvf_portal_get_endpoint_params to see valid filter fields.
                       NOTE: These underscore names (e.g. "file_set_id") are specific to
                       igvf_portal_get_collection and do NOT work with igvf_portal_search or igvf_portal_report.
    """
    api = _api()
    method = getattr(api, collection, None)
    if method is None:
        return json.dumps({
            "error": f"Unknown collection '{collection}'.",
            "available_collections": _list_collections(api),
        }, indent=2)

    sig = inspect.signature(method)
    kwargs: dict = {}
    if "query" in sig.parameters:
        kwargs["query"] = query or None
    if "limit" in sig.parameters:
        kwargs["limit"] = limit
    if "sort" in sig.parameters and sort is not None:
        kwargs["sort"] = sort
    if field_filters:
        for k, v in field_filters.items():
            if k in sig.parameters:
                kwargs[k] = v

    result = method(**kwargs)
    return _to_json(result)


@mcp.tool()
def igvf_portal_get_endpoint_params(endpoint: str) -> str:
    """Return the available filter parameters for a collection or endpoint.

    Returns filter parameters for a collection, showing both the underscore
    Python param name (collection_param, for igvf_portal_get_collection) and the
    real dotted field name (search_field, for igvf_portal_search and igvf_portal_report).
    E.g. collection_param="file_set_id" corresponds to search_field="file_set.@id".

    Args:
        endpoint: Snake-case collection or method name on IgvfApi, e.g.
                  "sequence_files", "measurement_sets", "genes", "tissues".
                  Pass "?" to list all available endpoints.
    """
    api = _api()

    if endpoint == "?":
        return json.dumps({
            "available_endpoints": _list_collections(api),
        }, indent=2)

    method = getattr(api, endpoint, None)
    if method is None:
        return json.dumps({
            "error": f"Unknown endpoint '{endpoint}'.",
            "available_endpoints": _list_collections(api),
        }, indent=2)

    sig = inspect.signature(method)
    filter_params = []
    for name, param in sig.parameters.items():
        if name.startswith("_") or name in _STANDARD_PARAMS:
            continue
        ann = param.annotation
        desc = _param_description(ann)
        search_field = desc.removeprefix("Filter by ") if desc.startswith("Filter by ") else name
        filter_params.append({
            "collection_param": name,
            "search_field": search_field,
            "type": _param_type_label(ann),
        })

    return json.dumps({
        "endpoint": endpoint,
        "standard_params": sorted(_STANDARD_PARAMS),
        "filter_params": filter_params,
        "notes": {
            "collection_param": "Use with igvf_portal_get_collection field_filters (underscore Python param name)",
            "search_field": "Use with igvf_portal_search and igvf_portal_report field_filters (dotted field name)",
        },
    }, indent=2)


@mcp.tool()
def igvf_portal_download(file_id: str, save_path: str) -> str:
    """Download an IGVF file directly to a local path.

    Args:
        file_id: The file identifier, e.g. "@id" (/tabular-files/IGVFFI8092FZKL/),
                 accession (IGVFFI8092FZKL), or UUID.
        save_path: Local filesystem path where the file will be written,
                   e.g. "/tmp/IGVFFI8092FZKL.tsv".
    """
    api = _api()
    data = api.download(file_id)
    with open(save_path, "wb") as f:
        f.write(data)
    return json.dumps({"saved_to": save_path, "bytes": len(data)}, indent=2)


METADATA_ALLOWED_TYPES = [
    "FileSet",
    "MeasurementSet",
    "AnalysisSet",
    "AuxiliarySet",
    "ConstructLibrarySet",
    "CuratedSet",
    "ModelSet",
    "PredictionSet",
]


@mcp.tool()
def igvf_portal_batch_download(
    type: list[str],
    save_path: str,
    query: str = "",
    field_filters: dict | None = None,
) -> str:
    """Get download URLs for files belonging to matching FileSet items and save them to a file.

    Only FileSet types are supported: MeasurementSet, AnalysisSet, AuxiliarySet,
    ConstructLibrarySet, CuratedSet, ModelSet, PredictionSet (and FileSet itself).

    Returns a file containing one download URL per line for all files in the
    matching FileSets.

    Args:
        type: One or more FileSet item types, e.g. ["MeasurementSet"].
        save_path: Local filesystem path where the URLs will be written,
                   e.g. "/tmp/urls.tsv".
        query: Optional free-text filter.
        field_filters: Dict of field→value filters using real dotted field names,
                       e.g. {"file_set.@id": "/analysis-sets/IGVFDS3909HJKS/"}.
    """
    invalid = [t for t in type if t not in METADATA_ALLOWED_TYPES]
    if invalid:
        return json.dumps({
            "error": f"Type(s) not allowed for batch download: {invalid}",
            "allowed_types": METADATA_ALLOWED_TYPES,
        }, indent=2)

    api = _api()
    result = api.batch_download(
        type=type,
        query=query or None,
        field_filters=field_filters,
    )
    content = result if isinstance(result, bytes) else str(result).encode("utf-8")
    with open(save_path, "wb") as f:
        f.write(content)
    return json.dumps({"saved_to": save_path, "bytes": len(content)}, indent=2)


@mcp.tool()
def igvf_portal_facets(
    type: list[str],
    query: str = "",
    field_filters: dict | None = None,
) -> str:
    """Get aggregated facet counts for an IGVF item type.

    Performs a search with limit=0 to return facet summaries without
    fetching actual records. Useful for understanding the distribution
    of values across a collection.

    Args:
        type: One or more item types, e.g. ["SequenceFile", "MeasurementSet"].
        query: Optional free-text filter to scope the facets.
        field_filters: Optional dict of field→value filters using real dotted
                       field names (same as igvf_portal_search).
    """
    api = _api()
    results = api.search(
        type=type,
        query=query or None,
        limit=0,
        field_filters=field_filters,
    )
    data = results.to_dict()
    return json.dumps({
        "total": data.get("total", 0),
        "facets": data.get("facets", []),
    }, indent=2, default=str)


@mcp.tool()
def igvf_portal_report(
    type: list[str],
    save_path: str,
    query: str = "",
    field_filters: dict | None = None,
) -> str:
    """Generate a TSV-formatted report for an item type and save it to a file.

    Args:
        type: One or more item types, e.g. ["SequenceFile"].
        save_path: Local filesystem path where the TSV will be written,
                   e.g. "/tmp/report.tsv".
        query: Optional free-text filter.
        field_filters: Dict of field→value filters. Values can be a single string
                       or a list of strings (translated to repeated query params,
                       e.g. {"file_format": ["bam", "bed"]} → file_format=bam&file_format=bed).
                       IMPORTANT: Use real dotted field names as they appear on the items,
                       e.g. {"file_set.@id": "/analysis-sets/IGVFDS3909HJKS/"}, NOT the
                       underscore-based Python parameter names used by igvf_portal_get_collection
                       (e.g. "file_set_id"). Those underscore names only work with
                       igvf_portal_get_collection, not here.
    """
    api = _api()
    result = api.report(
        type=type,
        query=query or None,
        field_filters=field_filters,
    )
    content = result if isinstance(result, bytes) else str(result).encode("utf-8")
    with open(save_path, "wb") as f:
        f.write(content)
    return json.dumps({"saved_to": save_path, "bytes": len(content)}, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
