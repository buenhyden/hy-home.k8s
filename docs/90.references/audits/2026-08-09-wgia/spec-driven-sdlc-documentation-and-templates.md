---
title: 'Audit: Spec-driven SDLC, Documentation, and Templates'
type: content/reference
status: draft
owner: platform
updated: 2026-08-09
---

# Audit: Spec-driven SDLC, Documentation, and Templates

## Overview

This report owns the audit of spec-driven development, Stage 01-05 lifecycle,
document families, templates, profile and README contracts, authoring routes,
integration guides, and documentation drift. WGIA-001 freezes the owner
inventory; WGIA-003 owns the complete audit and independent review.

## Reference Type

Dated repository-static documentation and SDLC audit. It does not own document
routes, frontmatter, lifecycle transitions, templates, or active SDLC policy.

## Authority Boundary

The Stage 99 registry, schema, routing, lifecycle, and template forms retain
their declared ownership. Stage 00 retains execution policy, and Stage 01-05
documents retain feature and operations truth. This report identifies evidence
and drift without publishing a competing route table or transition set.

## Scope

Included: spec-driven development, SDLC families, documentation and README
forms, templates, relationship contracts, integration guides, and current
owner/evidence producers. Excluded: changing profile routes, rewriting
historical packs, canonical remediation, unreviewed semantic conclusions, and
hosted/provider/live behavior.

## Definitions / Facts

### Spec-driven Development

`docs/03.specs/`, the agentic execution rule, Spec 054, and its reciprocal Plan
and Task are tracked at the observation commit. Their existence establishes a
current execution relation for this work, but not complete semantic lineage
for every repository feature.

### Templates

`docs/99.templates/support/document-profiles.json` is the exact route and
profile owner; the schema, template-routing contract, frontmatter support, and
physical templates are supporting current surfaces. The new reports select the
`content/reference` form, while this pack README selects the frontmatter-free
snapshot-pack form.

### Integration Guides

`docs/05.operations/guides/README.md` indexes tracked operator and integration
guides. WGIA-003 must test guide purpose, route, freshness, and consumer links;
the foundation does not infer guide correctness from presence.

### Documents and Documentation

The tracked `docs/` tree contains 461 files at the observation commit, spanning
the Stage 00, 01, 02, 03, 04, 05, 90, 98, and 99 families. Counts are inventory
facts and do not establish profile, link, semantic, or freshness conformance.

### SDLC

Stage 01 through Stage 05 current owners are routed by the stage-authoring
matrix, document-profile registry, lifecycle governance, and stage indexes.
WGIA-003 must distinguish an existing route from validated requirement-to-
evidence meaning.

### Canonical-owner Inventory

| Role | Current evidence surface | Foundation use |
| --- | --- | --- |
| Machine owner | `docs/99.templates/support/document-profiles.json` and schema | Exact profile, heading, metadata, and route evidence. |
| Policy/procedure owner | `docs/99.templates/support/sdlc-governance.md`; Stage 00 authoring rules | Lifecycle and authoring procedure. |
| Canonical form owner | `docs/99.templates/templates/**` | Physical document forms. |
| Human index | stage and collection README files | Reader routing, not machine ownership. |
| Evidence producer | document registry, Markdown profile, and link validators | Local conformance evidence. |

### Finding Convention

Material findings require ID, request IDs, scope, expected state, observed
state, exact evidence, evidence depth, verdict, impact, disposition, canonical
owner, verification, uncertainty, and blocker state. Verdict and depth use only
the closed pack vocabularies.

#### WGA-DOC-001 — Document-contract inventory established

- **Request IDs**: spec-driven development, templates, integration guides, documents/documentation, and SDLC coverage rows in the pack index.
- **Scope**: pinned profile, lifecycle, template, index, guide, and validator inventory.
- **Expected state**: WGIA-003 can compare every requested documentation topic against one current owner and direct evidence producer.
- **Observed state**: current owner families and the 461-file `docs/` inventory are identified; semantic completeness and drift review remain pending.
- **Evidence**: `docs/99.templates/support/document-profiles.json#profiles[id=content/reference]`; `docs/99.templates/support/document-profiles.json#profiles[id=readme/snapshot-pack]`; `docs/99.templates/support/template-routing.md#owned-contract`; `docs/99.templates/support/sdlc-governance.md#sdlc-profile-handoff`; `docs/05.operations/guides/README.md#item-index`; `scripts/validate-document-contract-registry.py#main`; `scripts/validate-markdown-profiles.py#main`; `scripts/validate-links-and-owners.py#main`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Partial`.
- **Impact**: route and form evidence can be tested, but no broad document-family conclusion is yet admissible.
- **Disposition**: `Keep`.
- **Canonical owner**: Stage 99 document contracts and the owning Stage 01-05 documents.
- **Verification**: strict registry, Markdown profile, and link/owner checks plus WGIA-003 content review.
- **Uncertainty**: template consumers, README freshness, integration-guide usability, and semantic lineage are not yet fully assessed.
- **Blocker**: none; later audit work is explicitly queued.

## Sources

Source roles are closed to `policy owner`, `machine owner`, `human index`,
`evidence producer`, and `historical snapshot`.

| Source ID | Source role | Evidence at the observation commit | Use |
| --- | --- | --- | --- |
| SRC-WGA-DOC-001 | machine owner | `docs/99.templates/support/document-profiles.json#profiles`; `docs/99.templates/support/document-profiles.schema.json#properties.profiles` | Exact path-to-form contract. |
| SRC-WGA-DOC-002 | policy owner | `docs/99.templates/support/template-routing.md#exact-one-profile-procedure`; `docs/99.templates/support/sdlc-governance.md#sdlc-profile-handoff` | Selection and lifecycle procedure. |
| SRC-WGA-DOC-003 | human index | `docs/README.md#document-index`; `docs/03.specs/README.md#current-spec-index`; `docs/05.operations/guides/README.md#item-index` | Reader routing and inventory entrypoints. |
| SRC-WGA-DOC-004 | evidence producer | `scripts/validate-document-contract-registry.py#main`; `scripts/validate-markdown-profiles.py#main`; `scripts/validate-links-and-owners.py#main` | Deterministic local conformance. |

## Review and Freshness

- Review status: `Pending` for WGIA-003 independent topic review.
- Review disposition: `DEFER`; inventory is not a completed documentation audit.
- Evidence observed: 2026-08-09 at the exact observation commit.
- Current-truth owners: Stage 99 machine contracts and the owning Stage 01-05 documents.
- Refresh triggers: route, profile, schema, template, lifecycle, README, guide,
  observation commit, finding, or canonical-owner change.
- Deeper evidence: hosted, provider-runtime, remote, credential-bearing, and
  live lanes remain `DEFER`.

## Related Documents

- [Pack Index](README.md)
- [Spec 054](../../../03.specs/054-workspace-governance-audit-and-remediation/spec.md)
- [Document Profile Registry](../../../99.templates/support/document-profiles.json)
- [Template Routing Contract](../../../99.templates/support/template-routing.md)
- [Implementation Task](../../../04.execution/tasks/2026-08-09-workspace-governance-audit-and-remediation.md)
