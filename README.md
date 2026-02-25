# IGVF Portal MCP Server

An MCP server that exposes the [IGVF Data Portal](https://data.igvf.org) API as tools for AI coding agents. Use it to search, filter, download files, and generate reports from the portal directly within an agent session.

The server is built on top of the [IGVF Python client](https://github.com/IGVF-DACC/igvf-python-client), which documents the full underlying API.

## Examples (using Claude Code)

### Search for genes by name

```
❯ Search IGVF portal for ep300 genes

● igvf-portal-mcp - igvf_portal_search (MCP)(query: "ep300", type: ["Gene"])
  ⎿  {"result":"{\n  \"total\": 11,\n  \"returned\": 11, ...

● Found 11 genes related to EP300:

  ┌───────────┬───────────────────────────────────────────────────┬──────────────┬────────────────────┬─────────────────────────────┐
  │  Symbol   │                       Name                        │     Taxa     │      Gene ID       │          Location           │
  ├───────────┼───────────────────────────────────────────────────┼──────────────┼────────────────────┼─────────────────────────────┤
  │ EP300     │ E1A binding protein p300                          │ Homo sapiens │ ENSG00000100393    │ chr22:41,092,591–41,180,077 │
  ├───────────┼───────────────────────────────────────────────────┼──────────────┼────────────────────┼─────────────────────────────┤
  │ EP300-AS1 │ EP300 antisense RNA 1                             │ Homo sapiens │ ENSG00000231993    │ chr22:41,174,590–41,197,508 │
  ├───────────┼───────────────────────────────────────────────────┼──────────────┼────────────────────┼─────────────────────────────┤
  │ Ep300     │ E1A binding protein p300                          │ Mus musculus │ ENSMUSG00000055024 │ chr15:81,469,551–81,536,278 │
  ├───────────┼───────────────────────────────────────────────────┼──────────────┼────────────────────┼─────────────────────────────┤
  │ EID1      │ EP300 interacting inhibitor of differentiation 1  │ Homo sapiens │ ENSG00000255302    │ chr15                       │
  ├───────────┼───────────────────────────────────────────────────┼──────────────┼────────────────────┼─────────────────────────────┤
  │ EID2      │ EP300 interacting inhibitor of differentiation 2  │ Homo sapiens │ ENSG00000176396    │ chr19                       │
  ├───────────┼───────────────────────────────────────────────────┼──────────────┼────────────────────┼─────────────────────────────┤
  │ EID2B     │ EP300 interacting inhibitor of differentiation 2B │ Homo sapiens │ ENSG00000176401    │ chr19                       │
  ├───────────┼───────────────────────────────────────────────────┼──────────────┼────────────────────┼─────────────────────────────┤
  │ EID3      │ EP300 interacting inhibitor of differentiation 3  │ Homo sapiens │ ENSG00000255150    │ chr12                       │
  ├───────────┼───────────────────────────────────────────────────┼──────────────┼────────────────────┼─────────────────────────────┤
  │ Eid1      │ EP300 interacting inhibitor of differentiation 1  │ Mus musculus │ ENSMUSG00000091337 │ chr2                        │
  ├───────────┼───────────────────────────────────────────────────┼──────────────┼────────────────────┼─────────────────────────────┤
  │ Eid2      │ EP300 interacting inhibitor of differentiation 2  │ Mus musculus │ ENSMUSG00000046058 │ chr7                        │
  ├───────────┼───────────────────────────────────────────────────┼──────────────┼────────────────────┼─────────────────────────────┤
  │ Eid2b     │ EP300 interacting inhibitor of differentiation 2B │ Mus musculus │ ENSMUSG00000070705 │ chr7                        │
  ├───────────┼───────────────────────────────────────────────────┼──────────────┼────────────────────┼─────────────────────────────┤
  │ Eid3      │ EP300 interacting inhibitor of differentiation 3  │ Mus musculus │ ENSMUSG00000109864 │ chr10                       │
  └───────────┴───────────────────────────────────────────────────┴──────────────┴────────────────────┴─────────────────────────────┘

  The core EP300 gene itself appears in both human (ENSG00000100393) and mouse
  (ENSMUSG00000055024) versions, along with its antisense RNA and several
  EP300-interacting inhibitor of differentiation (EID) family members.
```

### Look up files in an analysis set

```
❯ What files are in /analysis-sets/IGVFDS9564JXGL/?

● igvf-portal-mcp - igvf_portal_get_by_id (MCP)(resource_id: "/analysis-sets/IGVFDS9564JXGL/")
  ⎿  {
       "result": "{\n  \"doi\": \"10.65695/IGVFDS9564JXGL\",\n  \"input_file_sets\": [\n    \"/measurement-sets/IGVFDS2443ZQHK/\", ...
     … +9 lines (ctrl+o to expand)

● IGVFDS9564JXGL is an intermediate analysis set from the Ryan Corces lab (10x multiome —
  snATAC-seq + snRNA-seq, genetically multiplexed). It contains 6 files:

  ┌────────────────┬────────────────┐
  │   Accession    │      Type      │
  ├────────────────┼────────────────┤
  │ IGVFFI3882BXBL │ Alignment file │
  ├────────────────┼────────────────┤
  │ IGVFFI6307SAFZ │ Index file     │
  ├────────────────┼────────────────┤
  │ IGVFFI9552YLAE │ Index file     │
  ├────────────────┼────────────────┤
  │ IGVFFI6617CCIB │ Matrix file    │
  ├────────────────┼────────────────┤
  │ IGVFFI8348ZDXP │ Matrix file    │
  ├────────────────┼────────────────┤
  │ IGVFFI0795NBVQ │ Tabular file   │
  └────────────────┴────────────────┘

  The analysis covers a multiplexed sample from 8 human donors across three brain
  regions: posterior cingulate gyrus, putamen, and substantia nigra.
```

### Drill into individual files

```
❯ Give me details on the BED and BAM files.

● igvf-portal-mcp - igvf_portal_get_by_id (MCP)(resource_id: "IGVFFI3882BXBL")
  ⎿  {
       "result": "{\n  \"controlled_access\": false,\n  \"release_timestamp\": \"2025-11-12T18:17:11.471572+00:00\", ...
     … +11 lines (ctrl+o to expand)

● igvf-portal-mcp - igvf_portal_get_by_id (MCP)(resource_id: "IGVFFI0795NBVQ")
  ⎿  {
       "result": "{\n  \"controlled_access\": false,\n  \"assembly\": \"GRCh38\",\n  \"file_format_type\": \"bed3+\", ...
     … +11 lines (ctrl+o to expand)

● BAM — IGVFFI3882BXBL
  - Format: BAM (unfiltered alignments), assembly GRCh38
  - Content: Raw aligned reads from Chromap (snATAC-seq)
  - Size: 19.4 GB
  - Reads: 454,907,788
  - Derived from: 9 sequence files + 3 configuration files
  - S3: s3://igvf-public/2025/10/21/ec04ba8e.../IGVFFI3882BXBL.bam

  BED — IGVFFI0795NBVQ
  - Format: BED (bed3+, gzipped), assembly GRCh38
  - Content: Raw ATAC-seq fragment file from Chromap (unfiltered)
  - Size: 2.18 GB
  - Derived from: same 9 sequence files + 3 configuration files as the BAM
  - S3: s3://igvf-public/2025/10/21/b7d07a7c.../IGVFFI0795NBVQ.bed.gz

  Both were produced by the IGVF DACC processing pipeline using the same workflow
  (IGVFWF6403DVII) and are unfiltered outputs. The BED is used as input to produce
  the index file IGVFFI6307SAFZ, and the BAM feeds into index file IGVFFI9552YLAE.
```

### Explore the samples

```
❯ What samples were used?

● igvf-portal-mcp - igvf_portal_get_by_id (MCP)(resource_id: "/multiplexed-samples/IGVFSM6670KYMT/")
  ⎿  {
       "result": "{\n  \"preview_timestamp\": \"2025-03-25T22:41:47.611954+00:00\",\n  \"release_timestamp\": \"2025-09-17T18:47:59.370110+00:00\", ...
     … +9 lines (ctrl+o to expand)

● The multiplexed sample consists of 8 tissue samples from 8 European donors, all postmortem
  brain tissue sourced from Banner Health:

  ┌────────────────┬───────────────────────────┬───────────┬─────┬──────────────────────────────────────────────────┐
  │   Accession    │          Tissue           │ Donor sex │ Age │                     Disease                      │
  ├────────────────┼───────────────────────────┼───────────┼─────┼──────────────────────────────────────────────────┤
  │ IGVFSM8850QXUW │ Putamen                   │ Male      │ 85  │ Parkinson's disease                              │
  ├────────────────┼───────────────────────────┼───────────┼─────┼──────────────────────────────────────────────────┤
  │ IGVFSM9308VHFW │ Putamen                   │ Female    │ 82  │ Parkinson's disease                              │
  ├────────────────┼───────────────────────────┼───────────┼─────┼──────────────────────────────────────────────────┤
  │ IGVFSM9550JLTC │ Putamen                   │ Male      │ 78  │ Parkinson's disease                              │
  ├────────────────┼───────────────────────────┼───────────┼─────┼──────────────────────────────────────────────────┤
  │ IGVFSM9314PSQK │ Substantia nigra          │ Male      │ 74  │ Parkinson's disease, cerebral amyloid angiopathy │
  ├────────────────┼───────────────────────────┼───────────┼─────┼──────────────────────────────────────────────────┤
  │ IGVFSM3597NWGE │ Substantia nigra          │ Female    │ 70  │ Parkinson's disease                              │
  ├────────────────┼───────────────────────────┼───────────┼─────┼──────────────────────────────────────────────────┤
  │ IGVFSM0019LQKQ │ Substantia nigra          │ Male      │ 70  │ Parkinson's disease                              │
  ├────────────────┼───────────────────────────┼───────────┼─────┼──────────────────────────────────────────────────┤
  │ IGVFSM7450JGGC │ Substantia nigra          │ Male      │ 79  │ None listed                                      │
  ├────────────────┼───────────────────────────┼───────────┼─────┼──────────────────────────────────────────────────┤
  │ IGVFSM4995KUZR │ Posterior cingulate gyrus │ Male      │ 83  │ Parkinson's disease, cerebral amyloid angiopathy │
  └────────────────┴───────────────────────────┴───────────┴─────┴──────────────────────────────────────────────────┘

  7 of 8 donors have Parkinson's disease; 2 also have cerebral amyloid angiopathy. Ages
  range from 70–85. The one donor without a listed disease (IGVFSM7450JGGC) likely
  serves as a control.
```

---

## Setup

### Requirements

- Python ≥ 3.11
- [`uv`](https://github.com/astral-sh/uv)

Dependencies are listed in `requirements.txt` and managed automatically by `uv`.

### Run

```bash
uv run server.py
```

### Connect to an AI coding agent

Add the server to your agent's MCP configuration. For example, in Claude Code (`.mcp.json`):

```json
{
  "mcpServers": {
    "igvf-portal": {
      "command": "uv",
      "args": ["run", "server.py"]
    }
  }
}
```

A `.mcp.json` with this configuration is included in this repo.

### Environment variables

| Variable | Required | Description |
|---|---|---|
| `IGVF_ACCESS_KEY` | No | API key for authenticated access (unreleased data) |
| `IGVF_SECRET_ACCESS_KEY` | No | API secret paired with `IGVF_ACCESS_KEY` |
| `IGVF_HOST` | No | Portal host override, e.g. `https://api.sandbox.igvf.org` |
| `HTTPS_PROXY` / `HTTP_PROXY` | No | Proxy server URL |
| `REQUESTS_CA_BUNDLE` / `SSL_CERT_FILE` | No | Custom CA certificate path |

Without credentials, the server connects anonymously to the production portal.

---

## Tool Reference

All tools are prefixed `igvf_portal_`.

### Primary Tools

| Tool | Description |
|---|---|
| [`igvf_portal_get_by_id`](#igvf_portal_get_by_id) | Retrieve a single item by `@id`, accession, or UUID |
| [`igvf_portal_search`](#igvf_portal_search) | Search the portal with free text and/or field filters |
| [`igvf_portal_get_collection`](#igvf_portal_get_collection) | List items from a collection endpoint |
| [`igvf_portal_download`](#igvf_portal_download) | Download a single file to a local path |
| [`igvf_portal_report`](#igvf_portal_report) | Generate a TSV report for an item type |
| [`igvf_portal_batch_download`](#igvf_portal_batch_download) | Get download URLs for files matching a query |

### Supporting Tools

| Tool | Description |
|---|---|
| [`igvf_portal_get_schema`](#igvf_portal_get_schema) | Return the JSON schema for an item type |
| [`igvf_portal_get_endpoint_params`](#igvf_portal_get_endpoint_params) | Discover available filter parameters for a collection |
| [`igvf_portal_list_item_types`](#igvf_portal_list_item_types) | List all valid item type names |
| [`igvf_portal_facets`](#igvf_portal_facets) | Get aggregated facet counts for an item type |

---

### `igvf_portal_search`

Search the portal using free text and/or field filters.

```python
igvf_portal_search(
    query: str = "",
    type: list[str] | None = None,
    limit: int | str = 25,
    sort: list[str] | None = None,
    field_filters: dict | None = None,
) -> str  # JSON
```

| Parameter | Type | Description |
|---|---|---|
| `query` | str | Free-text search string |
| `type` | list[str] | Item types to filter by, e.g. `["SequenceFile"]` |
| `limit` | int or "all" | Max results (default 25) |
| `sort` | list[str] | Sort fields; prefix `-` for descending |
| `field_filters` | dict | Dotted field name → value filters |

Use real dotted field names (e.g. `"file_set.@id"`), not underscore param names. See `igvf_portal_get_endpoint_params` for the distinction.

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

```python
igvf_portal_get_by_id(resource_id: str) -> str  # JSON
```

```python
igvf_portal_get_by_id("IGVFFI1165AJSO")
igvf_portal_get_by_id("/sequence-files/IGVFFI1165AJSO/")
```

---

### `igvf_portal_get_schema`

Return the JSON schema for an item type, describing all its fields.

```python
igvf_portal_get_schema(item_type: str) -> str  # JSON schema
```

```python
igvf_portal_get_schema("SequenceFile")
```

Use `igvf_portal_list_item_types` to get valid type names.

---

### `igvf_portal_list_item_types`

Return a sorted list of all valid IGVF item type names (CamelCase).

```python
igvf_portal_list_item_types() -> str  # JSON array
```

```python
igvf_portal_list_item_types()
# → ["AccessKey", "AlignmentFile", "AnalysisSet", ...]
```

---

### `igvf_portal_get_collection`

List items from a specific collection endpoint using underscore-style parameter names.

```python
igvf_portal_get_collection(
    collection: str,
    query: str = "",
    limit: int = 25,
    sort: list[str] | None = None,
    field_filters: dict | None = None,
) -> str  # JSON
```

`field_filters` here uses underscore Python param names (e.g. `"file_set_id"`), not dotted field names. Use `igvf_portal_get_endpoint_params` to discover valid filter names.

```python
igvf_portal_get_collection(
    "sequence_files",
    field_filters={"file_format": "fastq"},
    limit=10
)
```

---

### `igvf_portal_get_endpoint_params`

Discover available filter parameters for a collection. Returns both underscore param names (for `igvf_portal_get_collection`) and dotted field names (for `igvf_portal_search` / `igvf_portal_report`).

```python
igvf_portal_get_endpoint_params(endpoint: str) -> str  # JSON
```

```python
igvf_portal_get_endpoint_params("sequence_files")
# → {
#     "endpoint": "sequence_files",
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

```python
igvf_portal_download(file_id: str, save_path: str) -> str  # JSON
```

```python
igvf_portal_download("IGVFFI8092FZKL", "/tmp/IGVFFI8092FZKL.tsv")
# → {"saved_to": "/tmp/IGVFFI8092FZKL.tsv", "bytes": 204800}
```

---

### `igvf_portal_batch_download`

Get a newline-separated list of download URLs for files matching a query.

```python
igvf_portal_batch_download(
    type: list[str],
    query: str = "",
    field_filters: dict | None = None,
) -> str  # newline-separated URLs
```

```python
igvf_portal_batch_download(
    type=["SequenceFile"],
    field_filters={"file_set.@id": "/measurement-sets/IGVFDS1234ABCD/"}
)
```

---

### `igvf_portal_facets`

Get aggregated facet counts for an item type without fetching records. Useful for understanding data distribution before filtering.

```python
igvf_portal_facets(
    type: list[str],
    query: str = "",
    field_filters: dict | None = None,
) -> str  # JSON
```

```python
igvf_portal_facets(type=["SequenceFile"])
# → {"total": 45123, "facets": [{"field": "file_format", "title": "File Format", "terms": [...]}]}
```

---

### `igvf_portal_report`

Generate a TSV-formatted report for an item type and save it locally.

```python
igvf_portal_report(
    type: list[str],
    save_path: str,
    query: str = "",
    field_filters: dict | None = None,
) -> str  # JSON
```

```python
igvf_portal_report(
    type=["SequenceFile"],
    save_path="/tmp/sequence_files.tsv",
    field_filters={"file_format": "fastq"}
)
# → {"saved_to": "/tmp/sequence_files.tsv", "bytes": 512000}
```

---

## Agent Skill: `igvf-facet-filter`

This repo includes an agent skill for guided faceted exploration. It is currently implemented as a Claude Code skill (`.claude/skills/igvf-facet-filter/SKILL.md`) but the workflow it describes can be adapted for any coding agent.

### Purpose

Guides the user through progressive filtering of an IGVF item type — starting from a high-level summary and narrowing down to a target set of records before fetching them.

### Usage (Claude Code)

```
/igvf-facet-filter SequenceFile
```

Or without an argument to be prompted for the item type.

### Workflow

1. Calls `igvf_portal_facets` and shows the total item count plus a menu of available facet names — no values yet.
2. User picks facets to expand. The skill shows term values and counts only for those.
3. User picks a filter value. The skill re-queries with `field_filters` applied and shows the updated count and facet menu.
4. Steps 2–3 repeat until the user is ready to fetch records.
5. Fetches results with `igvf_portal_search` or `igvf_portal_get_collection`.
