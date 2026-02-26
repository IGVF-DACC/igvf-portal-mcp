---
name: igvf-portal-facet-filter
description: Summarize an IGVF item type by facets and guide the user through progressive filtering
argument-hint: <ItemType>
---

Use the `igvf_portal_facets` MCP tool to fetch a summary of the IGVF item type provided in $ARGUMENTS.

Call: `igvf_portal_facets(type=["$ARGUMENTS"])`

**Note on filtering scope**

Facets only cover a *select subset* of fields. Filtering is not limited to facet fields — any field or embedded field available on the item type can be used as a filter. Use `igvf_portal_get_endpoint_params` to discover the full set of filterable fields for the collection.

**Step 1 — Progressive disclosure (facet names only)**

The facets response can be very large. Do NOT dump all facet values at once. Instead:

1. Show the **total item count**.
2. Show only the **list of available facet names/titles** (field name + title, no term values yet) — skip facets with 0 or 1 terms. This gives the user a menu to choose from without overwhelming output.
3. Note that additional fields beyond the facets are also filterable (via endpoint params).
4. Ask the user which facet(s) they want to explore or filter on, or whether they want to see all available filter fields.

**Step 2 — Expand on demand**

When the user picks one or more facets:
- Show the top term values and counts **only for those selected facets**.
- Ask if they want to apply a filter value, explore another facet, or fetch results.

If the user asks to see all filterable fields, call `igvf_portal_get_endpoint_params` for the collection and present the full field list.

**Step 3 — Iterative filtering**

When the user picks a filter value, call `igvf_portal_facets` again with the chosen `field_filters` applied:
- Show the updated total count.
- Show the facet name list again (updated distribution), skipping single-value facets.
- Repeat the loop: user picks facets to expand → picks filter values → re-query.

**Step 4 — Fetch results**

Once the user is satisfied with filters, fetch the actual records using `igvf_portal_search` or `igvf_portal_get_collection` with the accumulated filters.

This is an iterative loop: total + facet menu → user picks facets to expand → show values → user picks filter → re-query → repeat until user wants results.

Keep the output concise. If $ARGUMENTS is empty, ask the user which item type they want to summarize and mention they can call `igvf_portal_list_item_types` to see options.
