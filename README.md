# IGVF Portal MCP Server

An MCP server that exposes the [IGVF Data Portal](https://data.igvf.org) API as tools for AI coding agents. Use it to search, filter, download files, and generate reports from the portal directly within an agent session.

The server is built on top of the [IGVF Python client](https://github.com/IGVF-DACC/igvf-python-client), which documents the full underlying API.

## Examples (using Claude Code)

### List all item types

```
❯ What types exist on the IGVF portal?

● igvf-portal-mcp - igvf_portal_list_item_types (MCP)
  ⎿  {
       "result": "[\n  \"AccessKey\",\n  \"AlignmentFile\",\n  \"AnalysisSet\",\n  \"AnalysisStep\",\n  \"AnalysisStepVersion\",\n  \"AssayTerm\",\n  \"AuxiliarySet\",\n  \"Award\",\n  \"Biomarker\",\n  \"ConfigurationFile\",
     \n  \"ConstructLibrarySet\",\n  \"CrisprModification\",\n  \"CuratedSet\",\n  \"DegronModification\",\n  \"Document\",\n  \"Gene\",\n  \"HumanDonor\",\n  \"Image\",\n  \"ImageFile\",\n  \"InVitroSystem\",\n  \"IndexFile\
     … +5 lines (ctrl+o to expand)

● The IGVF portal has 57 item types:

  Files
  - AlignmentFile, ConfigurationFile, ImageFile, IndexFile, MatrixFile, ModelFile, ReferenceFile, SequenceFile, SignalFile, TabularFile

  Sets / Collections
  - AnalysisSet, AuxiliarySet, ConstructLibrarySet, CuratedSet, ModelSet, MeasurementSet, PredictionSet

  Samples / Biospecimens
  - InVitroSystem, MultiplexedSample, PrimaryCell, TechnicalSample, Tissue, WholeOrganism

  Donors
  - HumanDonor, RodentDonor

  Genomics / Biology
  - Gene, OpenReadingFrame, Biomarker, CrisprModification, DegronModification

  Terms / Ontologies
  - AssayTerm, PhenotypeTerm, PlatformTerm, SampleTerm, PhenotypicFeature

  Quality Metrics
  - MpraQualityMetric, PerturbSeqQualityMetric, SingleCellAtacSeqQualityMetric, SingleCellRnaSeqQualityMetric, StarrSeqQualityMetric

  Analysis / Workflows
  - AnalysisStep, AnalysisStepVersion, Software, SoftwareVersion, Workflow

  Administrative / Metadata
  - AccessKey, Award, Document, Image, InstitutionalCertificate, Lab, Page, Publication, Source, Treatment, User
```

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

### Look up an assay term

```
❯ What is assay term OBI:0002762?

● igvf-portal-mcp - igvf_portal_search (MCP)(query: "OBI:0002762", type: ["AssayTerm"])
  ⎿  {
       "result": "{\"total\": 1, \"returned\": 1, \"results\": [{\"preferred_assay_titles\": [\"SHARE-seq\",
         \"10x multiome\", \"10x multiome with MULTI-seq\", \"miDOGMA-seq\", \"scMultiome-NT-seq\",
         \"10x snATAC-seq with Scale pre-indexing\"], \"term_id\": \"OBI:0002762\",
         \"term_name\": \"single-nucleus ATAC-seq\", ...
     … +10 lines (ctrl+o to expand)

● OBI:0002762 is single-nucleus ATAC-seq (snATAC-seq).

  - Definition: An ATAC-seq assay in which single nuclei are isolated from frozen tissue samples,
    through a protocol designed to maximally preserve nucleus integrity during sample processing
    and optimize transposase-mediated fragmentation of chromatin in individual nuclei.
  - Assay slim: chromatin accessibility
  - Preferred assay titles on IGVF: SHARE-seq, 10x multiome, 10x multiome with MULTI-seq,
    miDOGMA-seq, scMultiome-NT-seq, 10x snATAC-seq with Scale pre-indexing
```

### Get a facet breakdown

```
❯ Give me a breakdown of measurement sets by preferred assay title

● igvf-portal-mcp - igvf_portal_facets (MCP)(type: ["MeasurementSet"])
  ⎿  Error: result (120,385 characters) exceeds maximum allowed tokens. Output has been saved to ...
     Format: JSON with schema: {result: string}
     … +6 lines (ctrl+o to expand)

● Bash(cat .../tool-results/mcp-igvf-portal-mcp-igvf_portal_facets-....txt | python3 -c "...")
  ⎿  Total MeasurementSets: 5129

       1470  10x multiome
     … +39 lines (ctrl+o to expand)

● MeasurementSets by preferred assay title (total: 5,129):

  ┌───────┬───────────────────────────────────┐
  │ Count │       Preferred Assay Title       │
  ├───────┼───────────────────────────────────┤
  │ 1,470 │ 10x multiome                      │
  ├───────┼───────────────────────────────────┤
  │   798 │ SGE                               │
  ├───────┼───────────────────────────────────┤
  │   519 │ SHARE-seq                         │
  ├───────┼───────────────────────────────────┤
  │   488 │ Variant-EFFECTS                   │
  ├───────┼───────────────────────────────────┤
  │   333 │ Parse SPLiT-seq                   │
  ├───────┼───────────────────────────────────┤
  │   268 │ CRISPR FlowFISH screen            │
  ├───────┼───────────────────────────────────┤
  │   196 │ Perturb-seq                       │
  ├───────┼───────────────────────────────────┤
  │   144 │ VAMP-seq (MultiSTEP)              │
  ├───────┼───────────────────────────────────┤
  │   118 │ 10x multiome with MULTI-seq       │
  ├───────┼───────────────────────────────────┤
  │   108 │ CRISPR FACS screen                │
  ├───────┼───────────────────────────────────┤
  │    95 │ RNA-seq                           │
  ├───────┼───────────────────────────────────┤
  │    76 │ mtscMultiome                      │
  ├───────┼───────────────────────────────────┤
  │    54 │ MPRA                              │
  ├───────┼───────────────────────────────────┤
  │    48 │ TAP-seq                           │
  ├───────┼───────────────────────────────────┤
  │    48 │ scNT-seq2                         │
  ├───────┼───────────────────────────────────┤
  │    41 │ ATAC-seq                          │
  ├───────┼───────────────────────────────────┤
  │    40 │ Proliferation CRISPR screen       │
  ├───────┼───────────────────────────────────┤
  │    36 │ VAMP-seq                          │
  ├───────┼───────────────────────────────────┤
  │    36 │ snM3C-seq                         │
  ├───────┼───────────────────────────────────┤
  │    34 │ snMCT-seq                         │
  ├───────┼───────────────────────────────────┤
  │    27 │ lentiMPRA                         │
  ├───────┼───────────────────────────────────┤
  │    23 │ WGS                               │
  ├───────┼───────────────────────────────────┤
  │    20 │ HiCAR                             │
  ├───────┼───────────────────────────────────┤
  │    19 │ Parse Perturb-seq                 │
  ├───────┼───────────────────────────────────┤
  │    15 │ STARR-seq                         │
  ├───────┼───────────────────────────────────┤
  │     8 │ ONT Fiber-seq                     │
  ├───────┼───────────────────────────────────┤
  │     8 │ ONT dRNA                          │
  ├───────┼───────────────────────────────────┤
  │     8 │ ONT direct WGS                    │
  ├───────┼───────────────────────────────────┤
  │     8 │ scCRISPR screen                   │
  ├───────┼───────────────────────────────────┤
  │     6 │ MPRA (scQer)                      │
  ├───────┼───────────────────────────────────┤
  │     6 │ Migration CRISPR screen           │
  ├───────┼───────────────────────────────────┤
  │     6 │ electroporated MPRA               │
  ├───────┼───────────────────────────────────┤
  │     4 │ Arrayed semi-qY2H v1/v2/v3        │
  ├───────┼───────────────────────────────────┤
  │     4 │ scATAC-seq                        │
  ├───────┼───────────────────────────────────┤
  │     4 │ scNT-seq                          │
  ├───────┼───────────────────────────────────┤
  │     3 │ scRNA-seq                         │
  ├───────┼───────────────────────────────────┤
  │     1 │ DUAL-IPA                          │
  ├───────┼───────────────────────────────────┤
  │     1 │ Variant painting via fluorescence │
  └───────┴───────────────────────────────────┘

  10x multiome dominates at 1,470 (29%), followed by SGE (798) and SHARE-seq (519).
```

### Discover filter parameters

```
❯ What can I filter on for analysis sets?

● igvf-portal-mcp - igvf_portal_get_endpoint_params (MCP)(endpoint: "analysis_sets")
  ⎿  {"result":"{\n  \"endpoint\": \"analysis_sets\",\n  \"standard_params\": [\n    \"limit\",\n    \"query\",\n    \"sort\"\n  ],\n  \"filter_params\": [\n    {\n      \"collection_param\": \"id\",\n      \"search_field\":
     \"@id\",\n      \"type\": \"list[str]\"\n    },\n    {\n      \"collection_param\": \"accession\",\n      \"search_field\": \"accession\",\n      \"type\": \"list[str]\"\n    },\n    {\n      \"collection_param\": \"alia
     ses\",\n      \"search_field\": \"aliases\",\n      \"type\": \"list[str]\"\n    },\n    {\n      \"collection_param\": \"alternate_accessions\",\n      \"search_field\": \"alternate_accessions\",\n      \"type\": \"list
     … +119 lines (ctrl+o to expand)

● Here are all filterable fields for AnalysisSet, grouped by category:

  Identity: @id, accession, uuid, aliases, alternate_accessions, doi, status,
    controlled_access, data_use_limitation_summaries, is_on_anvil

  Assay: assay_titles, preferred_assay_titles, file_set_type,
    uniform_pipeline_status, enrichment_designs,
    functional_assay_mechanisms.term_name

  Samples: samples.@id, samples.accession, samples.summary, sample_summary,
    samples.classifications, samples.taxa, samples.sample_terms.term_name,
    samples.disease_terms.term_name, samples.targeted_sample_term.term_name,
    samples.modifications.modality, samples.treatments.treatment_term_name,
    samples.treatments.treatment_type, samples.treatments.purpose,
    samples.growth_medium, samples.cellular_sub_pool,
    samples.institutional_certificates.data_use_limitation

  Donors: donors.@id, donors.accession, donors.taxa, donors.sex,
    donors.strain_background

  Files: files.@id, files.accession, files.content_type, files.file_format,
    files.file_format_type, files.assembly, files.transcriptome_annotation,
    files.file_size, files.status, files.upload_status,
    files.controlled_access, files.sequencing_platform.term_name,
    files.cell_type_annotation.term_name

  Input / linked sets: input_file_sets.@id, input_file_sets.accession,
    input_file_sets.file_set_type, input_for, construct_library_sets.@id,
    construct_library_sets.file_set_type,
    construct_library_sets.selection_criteria,
    construct_library_sets.small_scale_gene_list.symbol,
    construct_library_sets.associated_phenotypes.term_name,
    targeted_genes.symbol, demultiplexed_samples

  Workflows / pipeline: workflows.@id, workflows.accession, workflows.name,
    workflows.uniform_pipeline, workflows.workflow_version, pipeline_parameters

  Lab / award: lab.@id, lab.title, award.@id, award.component, award.title,
    award.contact_pi.title, publications.publication_identifiers

  Timestamps: creation_timestamp, release_timestamp,
    submitted_files_timestamp, preview_timestamp
```

### Search with field filters

```
❯ Give me an example 10x multiome analysis set

● igvf-portal-mcp - igvf_portal_search (MCP)(type: ["AnalysisSet"], field_filters: {"preferred_assay_titles":"10x multiome"}, limit: "1")
  ⎿  {
       "result": "{\n  \"total\": 726,\n  \"returned\": 1,\n  \"results\": [\n    {\n      \"doi\": \"10.65695/IGVFDS9564JXGL\",\n      \"input_file_sets\": [\n        \"/measurement-sets/IGVFDS2443ZQHK/\",\n        \"/measur
     ement-sets/IGVFDS9885KGYZ/\"\n      ],\n      \"release_timestamp\": \"2025-11-12T18:17:10.823135+00:00\",\n      \"lab\": \"/labs/ryan-corces/\",\n      \"award\": \"/awards/HG012076/\",\n      \"accession\": \"IGVFDS95
     … +11 lines (ctrl+o to expand)

● Here's an example 10x multiome AnalysisSet:

  IGVFDS9564JXGL — https://data.igvf.org/analysis-sets/IGVFDS9564JXGL/

  ┌───────────────────┬──────────────────────────────────────────────────────────────────────────────────────────┐
  │       Field       │                                          Value                                           │
  ├───────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
  │ Type              │ intermediate analysis                                                                    │
  ├───────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
  │ Status            │ released                                                                                 │
  ├───────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
  │ Lab               │ Ryan Corces                                                                              │
  ├───────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
  │ Assays            │ single-nucleus ATAC-seq + single-nucleus RNA-seq (10x multiome, genetically multiplexed) │
  ├───────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
  │ Sample            │ Homo sapiens multiplexed sample — posterior cingulate gyrus, putamen, substantia nigra   │
  ├───────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
  │ Donors            │ 8 human donors                                                                           │
  ├───────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
  │ Pipeline          │ uniform pipeline (completed)                                                             │
  ├───────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
  │ Controlled access │ No                                                                                       │
  └───────────────────┴──────────────────────────────────────────────────────────────────────────────────────────┘

  Files (6):
  - IGVFFI3882BXBL — alignment file
  - IGVFFI6307SAFZ, IGVFFI9552YLAE — index files
  - IGVFFI6617CCIB, IGVFFI8348ZDXP — matrix files
  - IGVFFI0795NBVQ — tabular file

  Input MeasurementSets: IGVFDS2443ZQHK, IGVFDS9885KGYZ
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

### Download and preview a file

```
❯ Download IGVFFI7253BTIQ and give me a preview

● Let me first get info on this file, then download it.

● igvf-portal-mcp - igvf_portal_get_by_id (MCP)(resource_id: "IGVFFI7253BTIQ")
  ⎿  {
       "result": "{\"controlled_access\": false, \"assembly\": \"GRCh38\", \"transcriptome_annotation\": \"GENCODE 43\",
         \"filtered\": true, \"accession\": \"IGVFFI7253BTIQ\", \"status\": \"released\", \"file_format\": \"tsv\",
         \"file_size\": 50518, \"content_type\": \"differential gene expression quantifications\", ...
     … +10 lines (ctrl+o to expand)

● It's a TSV file (~50 KB). Downloading now.

● igvf-portal-mcp - igvf_portal_download (MCP)(file_id: "IGVFFI7253BTIQ", save_path: "/tmp/IGVFFI7253BTIQ.tsv.gz")
  ⎿  {"saved_to": "/tmp/IGVFFI7253BTIQ.tsv.gz", "bytes": 50518}

● Here's a preview of IGVFFI7253BTIQ:

  File: differential gene expression quantifications (TSV, GRCh38 GENCODE 43, Parse Perturb-seq)
  Description: Analysis results for direct targeting (filtered)
  Rows: 969 data rows + 1 header

  Columns:

  ┌─────────────────────────┬─────────────────────────────────────────┐
  │         Column          │               Description               │
  ├─────────────────────────┼─────────────────────────────────────────┤
  │ intended_target_name    │ CRISPR target gene name                 │
  ├─────────────────────────┼─────────────────────────────────────────┤
  │ guide_id(s)             │ Guide RNA identifiers (comma-separated) │
  ├─────────────────────────┼─────────────────────────────────────────┤
  │ targeting_chr/start/end │ Genomic coordinates of the target       │
  ├─────────────────────────┼─────────────────────────────────────────┤
  │ gene_id                 │ Ensembl gene ID (the tested gene)       │
  ├─────────────────────────┼─────────────────────────────────────────┤
  │ gene_symbol             │ Gene symbol                             │
  ├─────────────────────────┼─────────────────────────────────────────┤
  │ sceptre_log2_fc         │ Log2 fold change (SCEPTRE method)       │
  ├─────────────────────────┼─────────────────────────────────────────┤
  │ sceptre_p_value         │ Raw p-value                             │
  ├─────────────────────────┼─────────────────────────────────────────┤
  │ sceptre_adj_p_value     │ Adjusted p-value                        │
  ├─────────────────────────┼─────────────────────────────────────────┤
  │ significant             │ TRUE/FALSE significance call            │
  ├─────────────────────────┼─────────────────────────────────────────┤
  │ type                    │ Direct_Targeting for all rows           │
  └─────────────────────────┴─────────────────────────────────────────┘

  Sample rows:

  ┌─────────────────┬────────┬─────────┬──────────┬─────────────┐
  │ intended_target │  gene  │ log2_fc │  adj_p   │ significant │
  ├─────────────────┼────────┼─────────┼──────────┼─────────────┤
  │ BAD             │ BAD    │ 0       │ 1        │ FALSE       │
  ├─────────────────┼────────┼─────────┼──────────┼─────────────┤
  │ TFPI            │ TFPI   │ -0.876  │ 1.52e-9  │ TRUE        │
  ├─────────────────┼────────┼─────────┼──────────┼─────────────┤
  │ SLC7A2          │ SLC7A2 │ -1.927  │ 1.57e-18 │ TRUE        │
  ├─────────────────┼────────┼─────────┼──────────┼─────────────┤
  │ HSPB6           │ HSPB6  │ -2.223  │ 1.06e-6  │ TRUE        │
  ├─────────────────┼────────┼─────────┼──────────┼─────────────┤
  │ CSDE1           │ CSDE1  │ -2.317  │ 5.60e-34 │ TRUE        │
  ├─────────────────┼────────┼─────────┼──────────┼─────────────┤
  │ MGST1           │ MGST1  │ -2.333  │ 1.98e-21 │ TRUE        │
  └─────────────────┴────────┴─────────┴──────────┴─────────────┘

  Most perturbations show negative log2 FC (gene knockdown via CRISPRi/dCas9-KRAB),
  with SCEPTRE used for differential expression testing.
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
