"""Tests for the IGVF Portal MCP server."""

import json
import typing
from typing import Annotated, Optional, Union
from unittest.mock import MagicMock, patch
import pytest
import pydantic.fields as pf

from igvf_client import IgvfApi
from igvf_client.models.item_type import ItemType

from server import (
    _api,
    _to_json,
    _list_collections,
    _param_type_label,
    _param_description,
    igvf_portal_list_item_types,
    igvf_portal_get_schema,
    igvf_portal_get_by_id,
    igvf_portal_search,
    igvf_portal_get_collection,
    igvf_portal_get_endpoint_params,
    igvf_portal_download,
    igvf_portal_batch_download,
    igvf_portal_facets,
    igvf_portal_report,
    METADATA_ALLOWED_TYPES,
    ITEM_TYPES,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_obj(data: dict):
    """Return a mock whose .to_dict() returns data and has no actual_instance."""
    obj = MagicMock()
    obj.to_dict.return_value = data
    del obj.actual_instance
    return obj


def make_search_result(hits: list, total: int | None = None):
    result = MagicMock()
    result.to_dict.return_value = {
        "@graph": hits,
        "total": total if total is not None else len(hits),
    }
    return result


def clear_env(monkeypatch):
    for var in [
        "IGVF_ACCESS_KEY", "IGVF_SECRET_ACCESS_KEY", "IGVF_HOST",
        "HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy",
        "REQUESTS_CA_BUNDLE", "SSL_CERT_FILE",
    ]:
        monkeypatch.delenv(var, raising=False)


# ── _to_json ──────────────────────────────────────────────────────────────────

def test_to_json_plain_dict():
    assert json.loads(_to_json({"key": "value"})) == {"key": "value"}


def test_to_json_plain_list():
    assert json.loads(_to_json([1, 2, 3])) == [1, 2, 3]


def test_to_json_plain_string():
    assert json.loads(_to_json("hello")) == "hello"


def test_to_json_object_with_to_dict():
    obj = make_obj({"foo": "bar"})
    assert json.loads(_to_json(obj)) == {"foo": "bar"}


def test_to_json_object_with_actual_instance_having_to_dict():
    inner = MagicMock()
    inner.to_dict.return_value = {"inner": "data"}
    obj = MagicMock(spec=["actual_instance"])
    obj.actual_instance = inner
    assert json.loads(_to_json(obj)) == {"inner": "data"}


def test_to_json_object_with_actual_instance_as_plain_dict():
    obj = MagicMock(spec=["actual_instance"])
    obj.actual_instance = {"already": "a dict"}
    assert json.loads(_to_json(obj)) == {"already": "a dict"}


def test_to_json_list_items_with_to_dict():
    item = MagicMock()
    item.to_dict.return_value = {"x": 1}
    assert json.loads(_to_json([item])) == [{"x": 1}]


def test_to_json_list_with_mixed_items():
    item = MagicMock()
    item.to_dict.return_value = {"x": 1}
    assert json.loads(_to_json([item, "plain"])) == [{"x": 1}, "plain"]


# ── _param_type_label ─────────────────────────────────────────────────────────

def test_param_type_label_str():
    assert _param_type_label(str) == "str"


def test_param_type_label_int():
    assert _param_type_label(int) == "number"


def test_param_type_label_float():
    assert _param_type_label(float) == "number"


def test_param_type_label_bool():
    assert _param_type_label(bool) == "bool"


def test_param_type_label_optional_str():
    assert _param_type_label(Optional[str]) == "str"


def test_param_type_label_optional_int():
    assert _param_type_label(Optional[int]) == "number"


def test_param_type_label_list_str():
    assert _param_type_label(list[str]) == "list[str]"


def test_param_type_label_union_str_none():
    assert _param_type_label(Union[str, None]) == "str"


def test_param_type_label_annotated_str():
    assert _param_type_label(Annotated[str, "meta"]) == "str"


def test_param_type_label_annotated_optional_int():
    assert _param_type_label(Annotated[Optional[int], "meta"]) == "number"


def test_param_type_label_annotated_list():
    assert _param_type_label(Annotated[list[str], "meta"]) == "list[str]"


# ── _param_description ────────────────────────────────────────────────────────

def test_param_description_annotated_with_field_description():
    ann = Annotated[str, pf.Field(description="Filter by file_set.@id")]
    assert _param_description(ann) == "Filter by file_set.@id"


def test_param_description_annotated_without_field():
    ann = Annotated[str, "just a string meta"]
    assert _param_description(ann) == ""


def test_param_description_plain_type_returns_empty():
    assert _param_description(str) == ""


def test_param_description_annotated_field_without_description():
    ann = Annotated[str, pf.Field()]
    assert _param_description(ann) == ""


# ── _list_collections ─────────────────────────────────────────────────────────

def test_list_collections_excludes_private_methods():
    api = MagicMock()
    assert all(not c.startswith("_") for c in _list_collections(api))


def test_list_collections_excludes_with_http_info_suffix():
    api = MagicMock()
    assert all("_with_http_info" not in c for c in _list_collections(api))


def test_list_collections_excludes_without_preload_content_suffix():
    api = MagicMock()
    assert all("_without_preload_content" not in c for c in _list_collections(api))


def test_list_collections_returns_sorted():
    api = MagicMock()
    result = _list_collections(api)
    assert result == sorted(result)


def test_list_collections_only_includes_callables():
    api = MagicMock()
    api.not_callable = "a plain string attribute"
    result = _list_collections(api)
    assert all(callable(getattr(api, c)) for c in result)


# ── _api ──────────────────────────────────────────────────────────────────────

def test_api_no_env_vars_calls_configuration_with_no_kwargs(monkeypatch):
    clear_env(monkeypatch)
    with patch("server.Configuration") as MockConfig, \
         patch("server.ApiClient"), patch("server.IgvfApi"):
        _api()
        MockConfig.assert_called_once_with()


def test_api_credentials_passed_to_configuration(monkeypatch):
    clear_env(monkeypatch)
    monkeypatch.setenv("IGVF_ACCESS_KEY", "mykey")
    monkeypatch.setenv("IGVF_SECRET_ACCESS_KEY", "mysecret")
    with patch("server.Configuration") as MockConfig, \
         patch("server.ApiClient"), patch("server.IgvfApi"):
        _api()
        MockConfig.assert_called_once_with(access_key="mykey", secret_access_key="mysecret")


def test_api_partial_credentials_not_used(monkeypatch):
    """Only access key set — no secret — should not authenticate."""
    clear_env(monkeypatch)
    monkeypatch.setenv("IGVF_ACCESS_KEY", "mykey")
    with patch("server.Configuration") as MockConfig, \
         patch("server.ApiClient"), patch("server.IgvfApi"):
        _api()
        MockConfig.assert_called_once_with()


def test_api_host_override(monkeypatch):
    clear_env(monkeypatch)
    monkeypatch.setenv("IGVF_HOST", "https://api.sandbox.igvf.org")
    with patch("server.Configuration") as MockConfig, \
         patch("server.ApiClient"), patch("server.IgvfApi"):
        _api()
        MockConfig.assert_called_once_with(host="https://api.sandbox.igvf.org")


def test_api_https_proxy_applied_to_config(monkeypatch):
    clear_env(monkeypatch)
    monkeypatch.setenv("HTTPS_PROXY", "http://proxy:8080")
    with patch("server.Configuration") as MockConfig, \
         patch("server.ApiClient"), patch("server.IgvfApi"):
        _api()
        assert MockConfig.return_value.proxy == "http://proxy:8080"


def test_api_http_proxy_fallback(monkeypatch):
    clear_env(monkeypatch)
    monkeypatch.setenv("HTTP_PROXY", "http://fallback:3128")
    with patch("server.Configuration") as MockConfig, \
         patch("server.ApiClient"), patch("server.IgvfApi"):
        _api()
        assert MockConfig.return_value.proxy == "http://fallback:3128"


def test_api_ssl_ca_cert_from_requests_ca_bundle(monkeypatch):
    clear_env(monkeypatch)
    monkeypatch.setenv("REQUESTS_CA_BUNDLE", "/etc/ssl/certs/ca.pem")
    with patch("server.Configuration") as MockConfig, \
         patch("server.ApiClient"), patch("server.IgvfApi"):
        _api()
        assert MockConfig.return_value.ssl_ca_cert == "/etc/ssl/certs/ca.pem"


def test_api_ssl_ca_cert_from_ssl_cert_file_fallback(monkeypatch):
    clear_env(monkeypatch)
    monkeypatch.setenv("SSL_CERT_FILE", "/usr/local/certs/bundle.pem")
    with patch("server.Configuration") as MockConfig, \
         patch("server.ApiClient"), patch("server.IgvfApi"):
        _api()
        assert MockConfig.return_value.ssl_ca_cert == "/usr/local/certs/bundle.pem"


def test_api_client_wraps_config(monkeypatch):
    clear_env(monkeypatch)
    with patch("server.Configuration") as MockConfig, \
         patch("server.ApiClient") as MockClient, \
         patch("server.IgvfApi"):
        _api()
        MockClient.assert_called_once_with(MockConfig.return_value)


def test_api_igvf_api_wraps_client(monkeypatch):
    clear_env(monkeypatch)
    with patch("server.Configuration"), \
         patch("server.ApiClient") as MockClient, \
         patch("server.IgvfApi") as MockApi:
        _api()
        MockApi.assert_called_once_with(MockClient.return_value)


# ── igvf_portal_list_item_types ───────────────────────────────────────────────

def test_list_item_types_returns_list():
    assert isinstance(json.loads(igvf_portal_list_item_types()), list)


def test_list_item_types_is_sorted():
    data = json.loads(igvf_portal_list_item_types())
    assert data == sorted(data)


def test_list_item_types_contains_known_types():
    data = json.loads(igvf_portal_list_item_types())
    for t in ("SequenceFile", "MeasurementSet", "Gene", "HumanDonor"):
        assert t in data


def test_list_item_types_matches_constant():
    assert json.loads(igvf_portal_list_item_types()) == ITEM_TYPES


# ── igvf_portal_get_schema ────────────────────────────────────────────────────

def test_get_schema_returns_schema():
    mock_api = MagicMock()
    mock_api.schema_for_item_type.return_value = {"title": "Gene", "properties": {}}
    with patch("server._api", return_value=mock_api):
        data = json.loads(igvf_portal_get_schema("Gene"))
    assert data["title"] == "Gene"


def test_get_schema_passes_item_type_enum_value():
    mock_api = MagicMock()
    mock_api.schema_for_item_type.return_value = {}
    with patch("server._api", return_value=mock_api):
        igvf_portal_get_schema("SequenceFile")
    mock_api.schema_for_item_type.assert_called_once_with(ItemType("SequenceFile"))


# ── igvf_portal_get_by_id ─────────────────────────────────────────────────────

def test_get_by_id_returns_item_json():
    mock_api = MagicMock()
    mock_api.get_by_id.return_value = make_obj({"accession": "IGVFFI1234ABCD"})
    with patch("server._api", return_value=mock_api):
        data = json.loads(igvf_portal_get_by_id("IGVFFI1234ABCD"))
    assert data["accession"] == "IGVFFI1234ABCD"


def test_get_by_id_passes_accession_directly():
    mock_api = MagicMock()
    mock_api.get_by_id.return_value = make_obj({})
    with patch("server._api", return_value=mock_api):
        igvf_portal_get_by_id("IGVFFI1234ABCD")
    mock_api.get_by_id.assert_called_once_with("IGVFFI1234ABCD")


def test_get_by_id_passes_at_id_path():
    mock_api = MagicMock()
    mock_api.get_by_id.return_value = make_obj({})
    with patch("server._api", return_value=mock_api):
        igvf_portal_get_by_id("/sequence-files/IGVFFI1234ABCD/")
    mock_api.get_by_id.assert_called_once_with("/sequence-files/IGVFFI1234ABCD/")


# ── igvf_portal_search ────────────────────────────────────────────────────────

def test_search_returns_summary_with_expected_keys():
    mock_api = MagicMock()
    mock_api.search.return_value = make_search_result([{"@id": "/genes/ENSG001/"}], total=100)
    with patch("server._api", return_value=mock_api):
        data = json.loads(igvf_portal_search())
    assert {"total", "returned", "results"} <= data.keys()


def test_search_total_comes_from_api_not_graph_length():
    mock_api = MagicMock()
    mock_api.search.return_value = make_search_result([{"@id": "/genes/ENSG001/"}], total=9999)
    with patch("server._api", return_value=mock_api):
        data = json.loads(igvf_portal_search())
    assert data["total"] == 9999
    assert data["returned"] == 1


def test_search_empty_query_passed_as_none():
    mock_api = MagicMock()
    mock_api.search.return_value = make_search_result([])
    with patch("server._api", return_value=mock_api):
        igvf_portal_search(query="")
    assert mock_api.search.call_args.kwargs["query"] is None


def test_search_non_empty_query_passed_through():
    mock_api = MagicMock()
    mock_api.search.return_value = make_search_result([])
    with patch("server._api", return_value=mock_api):
        igvf_portal_search(query="BRCA1")
    assert mock_api.search.call_args.kwargs["query"] == "BRCA1"


def test_search_type_filter_forwarded():
    mock_api = MagicMock()
    mock_api.search.return_value = make_search_result([])
    with patch("server._api", return_value=mock_api):
        igvf_portal_search(type=["SequenceFile"])
    assert mock_api.search.call_args.kwargs["type"] == ["SequenceFile"]


def test_search_field_filters_forwarded():
    mock_api = MagicMock()
    mock_api.search.return_value = make_search_result([])
    with patch("server._api", return_value=mock_api):
        igvf_portal_search(field_filters={"file_format": "bam"})
    assert mock_api.search.call_args.kwargs["field_filters"] == {"file_format": "bam"}


def test_search_sort_forwarded():
    mock_api = MagicMock()
    mock_api.search.return_value = make_search_result([])
    with patch("server._api", return_value=mock_api):
        igvf_portal_search(sort=["-creation_timestamp"])
    assert mock_api.search.call_args.kwargs["sort"] == ["-creation_timestamp"]


def test_search_limit_all():
    mock_api = MagicMock()
    mock_api.search.return_value = make_search_result([])
    with patch("server._api", return_value=mock_api):
        igvf_portal_search(limit="all")
    assert mock_api.search.call_args.kwargs["limit"] == "all"


def test_search_default_limit_is_25():
    mock_api = MagicMock()
    mock_api.search.return_value = make_search_result([])
    with patch("server._api", return_value=mock_api):
        igvf_portal_search()
    assert mock_api.search.call_args.kwargs["limit"] == 25


# ── igvf_portal_get_collection ────────────────────────────────────────────────

def test_get_collection_unknown_returns_error():
    mock_api = MagicMock(spec=IgvfApi)
    with patch("server._api", return_value=mock_api):
        data = json.loads(igvf_portal_get_collection("nonexistent_xyz"))
    assert "error" in data
    assert "available_collections" in data
    assert "nonexistent_xyz" in data["error"]


def test_get_collection_valid_is_called():
    mock_api = MagicMock()
    mock_api.genes.return_value = make_obj({"@graph": [], "total": 0})
    with patch("server._api", return_value=mock_api):
        igvf_portal_get_collection("genes")
    mock_api.genes.assert_called_once()


def test_get_collection_returns_serialized_result():
    mock_api = MagicMock()
    mock_api.genes.return_value = make_obj({"@graph": [{"symbol": "BRCA1"}]})
    with patch("server._api", return_value=mock_api):
        data = json.loads(igvf_portal_get_collection("genes"))
    assert data["@graph"][0]["symbol"] == "BRCA1"


def test_get_collection_empty_query_passed_as_none():
    passed = {}

    def fake_genes(query=None, limit=25):
        passed["query"] = query
        return make_obj({})

    mock_api = MagicMock()
    mock_api.genes = fake_genes
    with patch("server._api", return_value=mock_api):
        igvf_portal_get_collection("genes", query="")
    assert passed["query"] is None


def test_get_collection_field_filters_applied_when_param_in_signature():
    passed = {}

    def fake_genes(query=None, limit=25, taxa=None):
        passed["taxa"] = taxa
        return make_obj({})

    mock_api = MagicMock()
    mock_api.genes = fake_genes
    with patch("server._api", return_value=mock_api):
        igvf_portal_get_collection("genes", field_filters={"taxa": "Homo sapiens"})
    assert passed["taxa"] == "Homo sapiens"


def test_get_collection_field_filters_ignored_when_param_not_in_signature():
    called = {}

    def fake_genes(query=None, limit=25):
        called["yes"] = True
        return make_obj({})

    mock_api = MagicMock()
    mock_api.genes = fake_genes
    with patch("server._api", return_value=mock_api):
        igvf_portal_get_collection("genes", field_filters={"unknown_field": "value"})
    assert called.get("yes")


# ── igvf_portal_get_endpoint_params ──────────────────────────────────────────

def test_get_endpoint_params_question_mark_lists_endpoints():
    mock_api = MagicMock()
    with patch("server._api", return_value=mock_api), \
         patch("server._list_collections", return_value=["genes", "tissues"]):
        data = json.loads(igvf_portal_get_endpoint_params("?"))
    assert data["available_endpoints"] == ["genes", "tissues"]


def test_get_endpoint_params_unknown_returns_error():
    mock_api = MagicMock(spec=IgvfApi)
    with patch("server._api", return_value=mock_api):
        data = json.loads(igvf_portal_get_endpoint_params("nonexistent_xyz"))
    assert "error" in data
    assert "available_endpoints" in data
    assert "nonexistent_xyz" in data["error"]


def test_get_endpoint_params_valid_endpoint_returns_params():
    def fake_genes(query=None, limit=25, taxa: Optional[str] = None):
        pass

    mock_api = MagicMock()
    mock_api.genes = fake_genes
    with patch("server._api", return_value=mock_api):
        data = json.loads(igvf_portal_get_endpoint_params("genes"))
    assert data["endpoint"] == "genes"
    assert "filter_params" in data
    assert "standard_params" in data
    assert "notes" in data


def test_get_endpoint_params_standard_params_excluded():
    def fake_genes(query=None, limit=25, sort=None, taxa: Optional[str] = None):
        pass

    mock_api = MagicMock()
    mock_api.genes = fake_genes
    with patch("server._api", return_value=mock_api):
        data = json.loads(igvf_portal_get_endpoint_params("genes"))
    param_names = [p["collection_param"] for p in data["filter_params"]]
    assert "query" not in param_names
    assert "limit" not in param_names
    assert "sort" not in param_names


def test_get_endpoint_params_search_field_extracted_from_annotated_description():
    def fake_genes(
        query=None,
        limit=25,
        file_set_id: Annotated[Optional[str], pf.Field(description="Filter by file_set.@id")] = None,
    ):
        pass

    mock_api = MagicMock()
    mock_api.genes = fake_genes
    with patch("server._api", return_value=mock_api):
        data = json.loads(igvf_portal_get_endpoint_params("genes"))
    param = next(p for p in data["filter_params"] if p["collection_param"] == "file_set_id")
    assert param["search_field"] == "file_set.@id"


def test_get_endpoint_params_filter_param_has_required_keys():
    def fake_genes(query=None, limit=25, taxa: Optional[str] = None):
        pass

    mock_api = MagicMock()
    mock_api.genes = fake_genes
    with patch("server._api", return_value=mock_api):
        data = json.loads(igvf_portal_get_endpoint_params("genes"))
    for param in data["filter_params"]:
        assert "collection_param" in param
        assert "search_field" in param
        assert "type" in param


# ── igvf_portal_download ──────────────────────────────────────────────────────

def test_download_writes_bytes_to_path(tmp_path):
    save_path = str(tmp_path / "file.tsv")
    mock_api = MagicMock()
    mock_api.download.return_value = b"col1\tcol2\nval1\tval2\n"
    with patch("server._api", return_value=mock_api):
        igvf_portal_download("IGVFFI1234ABCD", save_path)
    with open(save_path, "rb") as f:
        assert f.read() == b"col1\tcol2\nval1\tval2\n"


def test_download_returns_path_and_byte_count(tmp_path):
    save_path = str(tmp_path / "file.tsv")
    content = b"col1\tcol2\n"
    mock_api = MagicMock()
    mock_api.download.return_value = content
    with patch("server._api", return_value=mock_api):
        data = json.loads(igvf_portal_download("IGVFFI1234ABCD", save_path))
    assert data["saved_to"] == save_path
    assert data["bytes"] == len(content)


def test_download_calls_api_with_file_id(tmp_path):
    save_path = str(tmp_path / "file.tsv")
    mock_api = MagicMock()
    mock_api.download.return_value = b""
    with patch("server._api", return_value=mock_api):
        igvf_portal_download("IGVFFI1234ABCD", save_path)
    mock_api.download.assert_called_once_with("IGVFFI1234ABCD")


# ── igvf_portal_batch_download ────────────────────────────────────────────────

def test_batch_download_invalid_type_returns_error(tmp_path):
    save_path = str(tmp_path / "urls.txt")
    data = json.loads(igvf_portal_batch_download(["SequenceFile"], save_path))
    assert "error" in data
    assert "allowed_types" in data
    assert "SequenceFile" in data["error"]


def test_batch_download_multiple_invalid_types_listed_in_error(tmp_path):
    save_path = str(tmp_path / "urls.txt")
    data = json.loads(igvf_portal_batch_download(["SequenceFile", "Gene"], save_path))
    assert "error" in data


def test_batch_download_valid_type_writes_urls_to_file(tmp_path):
    save_path = str(tmp_path / "urls.txt")
    url_content = b"https://example.com/file1.tsv\nhttps://example.com/file2.tsv\n"
    mock_api = MagicMock()
    mock_api.batch_download.return_value = url_content
    with patch("server._api", return_value=mock_api):
        igvf_portal_batch_download(["MeasurementSet"], save_path)
    with open(save_path, "rb") as f:
        assert f.read() == url_content


def test_batch_download_returns_path_and_bytes(tmp_path):
    save_path = str(tmp_path / "urls.txt")
    url_content = b"https://example.com/file1.tsv\n"
    mock_api = MagicMock()
    mock_api.batch_download.return_value = url_content
    with patch("server._api", return_value=mock_api):
        data = json.loads(igvf_portal_batch_download(["MeasurementSet"], save_path))
    assert data["saved_to"] == save_path
    assert data["bytes"] == len(url_content)


def test_batch_download_str_result_encoded_to_bytes(tmp_path):
    save_path = str(tmp_path / "urls.txt")
    mock_api = MagicMock()
    mock_api.batch_download.return_value = "https://example.com/file.tsv\n"
    with patch("server._api", return_value=mock_api):
        igvf_portal_batch_download(["MeasurementSet"], save_path)
    with open(save_path, "rb") as f:
        assert f.read() == b"https://example.com/file.tsv\n"


def test_batch_download_field_filters_forwarded(tmp_path):
    save_path = str(tmp_path / "urls.txt")
    mock_api = MagicMock()
    mock_api.batch_download.return_value = b""
    with patch("server._api", return_value=mock_api):
        igvf_portal_batch_download(
            ["MeasurementSet"], save_path,
            field_filters={"assay_title": "RNA-seq"},
        )
    assert mock_api.batch_download.call_args.kwargs["field_filters"] == {"assay_title": "RNA-seq"}


def test_batch_download_empty_query_passed_as_none(tmp_path):
    save_path = str(tmp_path / "urls.txt")
    mock_api = MagicMock()
    mock_api.batch_download.return_value = b""
    with patch("server._api", return_value=mock_api):
        igvf_portal_batch_download(["MeasurementSet"], save_path, query="")
    assert mock_api.batch_download.call_args.kwargs["query"] is None


@pytest.mark.parametrize("allowed_type", METADATA_ALLOWED_TYPES)
def test_batch_download_all_allowed_types_accepted(allowed_type, tmp_path):
    save_path = str(tmp_path / "urls.txt")
    mock_api = MagicMock()
    mock_api.batch_download.return_value = b""
    with patch("server._api", return_value=mock_api):
        data = json.loads(igvf_portal_batch_download([allowed_type], save_path))
    assert "error" not in data


# ── igvf_portal_facets ────────────────────────────────────────────────────────

def test_facets_calls_search_with_limit_zero():
    mock_api = MagicMock()
    mock_api.search.return_value.to_dict.return_value = {"total": 0, "facets": [], "@graph": []}
    with patch("server._api", return_value=mock_api):
        igvf_portal_facets(type=["MeasurementSet"])
    assert mock_api.search.call_args.kwargs["limit"] == 0


def test_facets_returns_total_and_facets():
    mock_api = MagicMock()
    mock_api.search.return_value.to_dict.return_value = {
        "total": 42,
        "facets": [{"field": "file_format", "terms": [{"key": "bam", "doc_count": 10}]}],
        "@graph": [],
    }
    with patch("server._api", return_value=mock_api):
        data = json.loads(igvf_portal_facets(type=["SequenceFile"]))
    assert data["total"] == 42
    assert data["facets"][0]["field"] == "file_format"


def test_facets_type_forwarded():
    mock_api = MagicMock()
    mock_api.search.return_value.to_dict.return_value = {"total": 0, "facets": [], "@graph": []}
    with patch("server._api", return_value=mock_api):
        igvf_portal_facets(type=["SequenceFile", "MeasurementSet"])
    assert mock_api.search.call_args.kwargs["type"] == ["SequenceFile", "MeasurementSet"]


def test_facets_field_filters_forwarded():
    mock_api = MagicMock()
    mock_api.search.return_value.to_dict.return_value = {"total": 0, "facets": [], "@graph": []}
    with patch("server._api", return_value=mock_api):
        igvf_portal_facets(type=["SequenceFile"], field_filters={"file_format": "bam"})
    assert mock_api.search.call_args.kwargs["field_filters"] == {"file_format": "bam"}


def test_facets_empty_query_passed_as_none():
    mock_api = MagicMock()
    mock_api.search.return_value.to_dict.return_value = {"total": 0, "facets": [], "@graph": []}
    with patch("server._api", return_value=mock_api):
        igvf_portal_facets(type=["SequenceFile"], query="")
    assert mock_api.search.call_args.kwargs["query"] is None


# ── igvf_portal_report ────────────────────────────────────────────────────────

def test_report_writes_bytes_to_path(tmp_path):
    save_path = str(tmp_path / "report.tsv")
    tsv = b"accession\tstatus\nIGVFDS001\treleased\n"
    mock_api = MagicMock()
    mock_api.report.return_value = tsv
    with patch("server._api", return_value=mock_api):
        igvf_portal_report(type=["MeasurementSet"], save_path=save_path)
    with open(save_path, "rb") as f:
        assert f.read() == tsv


def test_report_str_result_encoded_to_bytes(tmp_path):
    save_path = str(tmp_path / "report.tsv")
    mock_api = MagicMock()
    mock_api.report.return_value = "accession\tstatus\n"
    with patch("server._api", return_value=mock_api):
        igvf_portal_report(type=["MeasurementSet"], save_path=save_path)
    with open(save_path, "rb") as f:
        assert f.read() == b"accession\tstatus\n"


def test_report_returns_path_and_byte_count(tmp_path):
    save_path = str(tmp_path / "report.tsv")
    content = b"accession\n"
    mock_api = MagicMock()
    mock_api.report.return_value = content
    with patch("server._api", return_value=mock_api):
        data = json.loads(igvf_portal_report(type=["MeasurementSet"], save_path=save_path))
    assert data["saved_to"] == save_path
    assert data["bytes"] == len(content)


def test_report_type_forwarded(tmp_path):
    save_path = str(tmp_path / "report.tsv")
    mock_api = MagicMock()
    mock_api.report.return_value = b""
    with patch("server._api", return_value=mock_api):
        igvf_portal_report(type=["SequenceFile"], save_path=save_path)
    assert mock_api.report.call_args.kwargs["type"] == ["SequenceFile"]


def test_report_field_filters_forwarded(tmp_path):
    save_path = str(tmp_path / "report.tsv")
    mock_api = MagicMock()
    mock_api.report.return_value = b""
    with patch("server._api", return_value=mock_api):
        igvf_portal_report(type=["SequenceFile"], save_path=save_path, field_filters={"file_format": "bam"})
    assert mock_api.report.call_args.kwargs["field_filters"] == {"file_format": "bam"}


def test_report_empty_query_passed_as_none(tmp_path):
    save_path = str(tmp_path / "report.tsv")
    mock_api = MagicMock()
    mock_api.report.return_value = b""
    with patch("server._api", return_value=mock_api):
        igvf_portal_report(type=["SequenceFile"], save_path=save_path, query="")
    assert mock_api.report.call_args.kwargs["query"] is None
