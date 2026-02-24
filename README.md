# IGVF Portal MCP Server & Skill Reference

## Overview

This directory contains an [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server that exposes the [IGVF Data Portal](https://data.igvf.org) API as tools for AI assistants. It also includes a Claude skill for guided faceted search.

```
igvf-portal-mcp/
├── .mcp.json                          ← MCP server registration for Claude Code
├── .claude/skills/igvf-facet-filter/
│   └── SKILL.md                       ← /igvf-facet-filter skill definition
├── server.py                          ← MCP server (10 tools, igvf_portal_ prefix)
├── README.md                          ← this file
└── PLAN.md                            ← original design notes
```

The server wraps the [`igvf-client`](https://pypi.org/project/igvf-client/) Python SDK and exposes it over the stdio MCP transport so Claude (and other MCP-compatible clients) can query, browse, download, and report on IGVF data.

---

## Setup

### Prerequisites

- Python ≥ 3.11
- [`uv`](https://github.com/astral-sh/uv) (recommended) or `pip`

### Install dependencies

```bash
# With uv (reads inline script metadata automatically)
uv run server.py

# Or install manually
pip install "igvf-client==110.0.0" "mcp[cli]==1.26.0"
```

### Run the server

```bash
# stdio transport (used by MCP clients like Claude Code)
python3 server.py

# Or with uv
uv run server.py
```

---

## Configuration

### `.mcp.json` (Claude Code)

The `.mcp.json` in this repo registers the server with Claude Code:

```json
{
  "mcpServers": {
    "igvfd": {
      "command": "python3",
      "args": ["server.py"]
    }
  }
}
```

### Environment variables

| Variable | Required | Description |
|---|---|---|
| `IGVF_ACCESS_KEY` | No | API key for authenticated access (unreleased data) |
| `IGVF_SECRET_ACCESS_KEY` | No | API secret paired with `IGVF_ACCESS_KEY` |
| `IGVF_HOST` | No | Portal host override, e.g. `https://api.sandbox.igvf.org` |
| `HTTPS_PROXY` / `HTTP_PROXY` | No | Proxy server URL |
| `REQUESTS_CA_BUNDLE` / `SSL_CERT_FILE` | No | Custom CA certificate path |

Without `IGVF_ACCESS_KEY` + `IGVF_SECRET_ACCESS_KEY`, the server connects anonymously to the production portal (`https://api.igvf.org`).

---

## Tool Reference

All tools are prefixed `igvf_portal_`. Tools marked with dotted field names accept filters like `{"file_set.@id": "/analysis-sets/IGVFDS3909HJKS/"}`.

---

### `igvf_portal_search`

Search the IGVF Data Portal using free text and/or field filters.

**Signature**
```python
igvf_portal_search(
    query: str = "",
    type: list[str] | None = None,
    limit: int | str = 25,
    sort: list[str] | None = None,
    field_filters: dict | None = None,
) -> str  # JSON
```

**Parameters**

| Parameter | Type | Description |
|---|---|---|
| `query` | str | Free-text search string |
| `type` | list[str] | Item types to filter by, e.g. `["SequenceFile"]` |
| `limit` | int or "all" | Max results (default 25) |
| `sort` | list[str] | Sort fields; prefix `-` for descending |
| `field_filters` | dict | Dotted field name → value filters |

**Example**
```python
igvf_portal_search(
    type=["SequenceFile"],
    field_filters={"file_format": "fastq"},
    limit=5
)
# → {"total": 12340, "returned": 5, "results": [...]}
```

---

### `igvf_portal_get_by_id`

Retrieve a single item by its `@id`, accession, or UUID.

**Signature**
```python
igvf_portal_get_by_id(resource_id: str) -> str  # JSON
```

**Example**
```python
igvf_portal_get_by_id("IGVFFI1165AJSO")
igvf_portal_get_by_id("/sequence-files/IGVFFI1165AJSO/")
```

---

### `igvf_portal_get_schema`

Return the JSON schema for an item type, describing all its fields.

**Signature**
```python
igvf_portal_get_schema(item_type: str) -> str  # JSON schema
```

**Example**
```python
igvf_portal_get_schema("SequenceFile")
```

Use `igvf_portal_list_item_types` to get valid `item_type` values.

---

### `igvf_portal_list_item_types`

Return a sorted list of all valid IGVF item type names (CamelCase).

**Signature**
```python
igvf_portal_list_item_types() -> str  # JSON array
```

**Example**
```python
igvf_portal_list_item_types()
# → ["AccessKey", "AlignmentFile", "AnalysisSet", ...]
```

---

### `igvf_portal_get_collection`

List items from a specific collection endpoint using Python-style underscore parameter names.

**Signature**
```python
igvf_portal_get_collection(
    collection: str,
    query: str = "",
    limit: int = 25,
    sort: list[str] | None = None,
    field_filters: dict | None = None,
) -> str  # JSON
```

> **Note:** `field_filters` here uses underscore Python param names (e.g. `"file_set_id"`), not dotted field names. Use `igvf_portal_get_endpoint_params` to discover valid filter names.

**Example**
```python
igvf_portal_get_collection(
    "sequence_files",
    field_filters={"file_format": "fastq"},
    limit=10
)
```

---

### `igvf_portal_get_endpoint_params`

Discover available filter parameters for a collection, with both underscore param names (for `igvf_portal_get_collection`) and dotted field names (for `igvf_portal_search`/`igvf_portal_report`).

**Signature**
```python
igvf_portal_get_endpoint_params(endpoint: str) -> str  # JSON
```

**Example**
```python
igvf_portal_get_endpoint_params("sequence_files")
# → {
#     "endpoint": "sequence_files",
#     "standard_params": ["limit", "query", "sort"],
#     "filter_params": [
#       {"collection_param": "file_set_id", "search_field": "file_set.@id", "type": "str"},
#       ...
#     ]
#   }

igvf_portal_get_endpoint_params("?")  # list all available endpoints
```

---

### `igvf_portal_download`

Download a single IGVF file to a local path.

**Signature**
```python
igvf_portal_download(file_id: str, save_path: str) -> str  # JSON
```

**Example**
```python
igvf_portal_download("IGVFFI8092FZKL", "/tmp/IGVFFI8092FZKL.tsv")
# → {"saved_to": "/tmp/IGVFFI8092FZKL.tsv", "bytes": 204800}
```

---

### `igvf_portal_batch_download`

Get a newline-separated list of download URLs for files matching a query.

**Signature**
```python
igvf_portal_batch_download(
    type: list[str],
    query: str = "",
    field_filters: dict | None = None,
) -> str  # newline-separated URLs
```

**Example**
```python
igvf_portal_batch_download(
    type=["SequenceFile"],
    field_filters={"file_set.@id": "/measurement-sets/IGVFDS1234ABCD/"}
)
```

---

### `igvf_portal_facets`

Get aggregated facet counts for an item type without fetching records. Useful for understanding data distribution before filtering.

**Signature**
```python
igvf_portal_facets(
    type: list[str],
    query: str = "",
    field_filters: dict | None = None,
) -> str  # JSON with total + facets array
```

**Example**
```python
igvf_portal_facets(type=["SequenceFile"])
# → {"total": 45123, "facets": [{"field": "file_format", "title": "File Format", "terms": [...]}]}
```

---

### `igvf_portal_report`

Generate a TSV-formatted report for an item type and save it locally.

**Signature**
```python
igvf_portal_report(
    type: list[str],
    save_path: str,
    query: str = "",
    field_filters: dict | None = None,
) -> str  # JSON with save path and byte count
```

**Example**
```python
igvf_portal_report(
    type=["SequenceFile"],
    save_path="/tmp/sequence_files.tsv",
    field_filters={"file_format": "fastq"}
)
# → {"saved_to": "/tmp/sequence_files.tsv", "bytes": 512000}
```

---

## Skill Reference: `igvf-facet-filter`

### Purpose

The `igvf-facet-filter` skill guides users through progressive faceted exploration of an IGVF item type — narrowing down a large collection step-by-step before fetching records.

### How to invoke

In Claude Code, type:

```
/igvf-facet-filter SequenceFile
```

Or without an argument to be prompted for the item type:

```
/igvf-facet-filter
```

### Workflow walkthrough

1. **Initial summary** — Calls `igvf_portal_facets(type=["<ItemType>"])` and shows the total item count plus a menu of available facet names (skipping facets with 0 or 1 term).

2. **Expand on demand** — User picks one or more facets to inspect. The skill shows term values and counts only for those facets.

3. **Apply filters** — User picks a filter value. The skill calls `igvf_portal_facets` again with `field_filters` applied and shows the updated count and facet menu.

4. **Repeat** — Steps 2–3 repeat until the user is satisfied with the filter set.

5. **Fetch results** — The skill calls `igvf_portal_search` or `igvf_portal_get_collection` with the accumulated filters to retrieve actual records.

The skill also offers to call `igvf_portal_get_endpoint_params` if the user wants to see filterable fields beyond what facets cover.

---

## Common Workflows

### Faceted exploration

```python
# 1. See what's available
igvf_portal_facets(type=["MeasurementSet"])

# 2. Narrow by assay term
igvf_portal_facets(
    type=["MeasurementSet"],
    field_filters={"assay_term.term_name": "ATAC-seq"}
)

# 3. Fetch results
igvf_portal_search(
    type=["MeasurementSet"],
    field_filters={"assay_term.term_name": "ATAC-seq"}
)
```

### Download files from a measurement set

```python
# List files
igvf_portal_batch_download(
    type=["SequenceFile"],
    field_filters={"file_set.@id": "/measurement-sets/IGVFDS1234ABCD/"}
)

# Download a specific file
igvf_portal_download("IGVFFI1165AJSO", "/tmp/reads.fastq.gz")
```

### Generate a filtered TSV report

```python
# Discover filter params first
igvf_portal_get_endpoint_params("sequence_files")

# Generate report
igvf_portal_report(
    type=["SequenceFile"],
    save_path="/tmp/fastq_files.tsv",
    field_filters={"file_format": "fastq"}
)
```

### Look up a specific item

```python
# By accession
igvf_portal_get_by_id("IGVFFI1165AJSO")

# By @id path
igvf_portal_get_by_id("/measurement-sets/IGVFDS1234ABCD/")

# Check its schema
igvf_portal_get_schema("MeasurementSet")
```
