---
title: 'Audit: Legacy, Deprecated, and One-shot Disposition Ledger'
type: content/reference
status: draft
owner: platform
updated: 2026-08-09
---

# Audit: Legacy, Deprecated, and One-shot Disposition Ledger

## Overview

This report owns candidate provenance, consumer evidence, replacement routing,
Keep/Integrate/Correct/Delete/DEFER decisions, and post-delete gates for
Legacy, Deprecated, duplicate, and one-shot artifacts. WGIA-001 establishes the
fail-closed record form; WGIA-009 inventories and decides candidates, and
WGIA-013 alone performs proof-complete deletion.

## Reference Type

Dated repository-static cleanup disposition ledger. It is not a delete list,
retirement policy, compatibility owner, or authorization for removal.

## Authority Boundary

Candidate classification follows current policy, provenance, consumers, and
replacement ownership rather than names. Existing audit packs are historical
evidence and Stage 98 is immutable. No candidate may receive `Delete` until the
full gate is evidenced and independently reviewed.

## Scope

Included: exact tracked candidate paths, source commits, candidate classes,
current consumers, replacement owners, decisions, evidence, historical routes,
and post-delete gates. Excluded: name-only classification, historical pack
deletion, Stage 98 edits, unproven removal, and candidate conclusions before
WGIA-009 review.

## Definitions / Facts

### Legacy and Deprecated Documents

`docs/99.templates/support/legacy-cleanup-rules.md` and current legacy-cutover
contracts/validators are candidate-classification inputs. A filename or body
containing `Legacy` or `Deprecated` can still be an active owner or validator;
the consumer and authority inventory must decide its status.

### One-shot Documents and Scripts

One-shot status requires evidence that an artifact is temporary, has no unique
durable evidence left, has zero current consumers after migration, and has a
surviving replacement/history route. WGIA-001 makes no candidate-specific
deletion decision.

### Cleanup Disposition Convention

Every candidate row requires: candidate path, full source commit, candidate
class, exact current consumers, surviving replacement owner, one decision from
`Keep`, `Integrate`, `Correct`, `Delete`, or `DEFER`, supporting evidence, and
focused plus aggregate post-delete gates. Any missing field fails closed to
`DEFER`. `Delete` additionally requires zero current consumers, valid rendered
links, exact historical recovery, green post-delete checks, and independent
review.

| Candidate set | Source basis | Initial decision | Reason |
| --- | --- | --- | --- |
| Legacy/Deprecated vocabulary hits | Observation commit and exact tracked-path scan | `DEFER` | Authority and consumer classification belongs to WGIA-009. |
| Suspected duplicates | Observation commit and canonical-owner comparison | `DEFER` | Content similarity alone is not replacement or zero-consumer proof. |
| Suspected one-shot documents/scripts | Observation commit and invocation/link/import inventory | `DEFER` | Unique evidence and consumer checks are not yet complete. |
| Existing audit pack bodies | Source-commit-bounded historical snapshots | `Keep` | Spec 054 protects their observation bodies; navigation changes belong to later cutover work. |
| `docs/98.archive/**` | Protected archive corpus | `Keep` | Explicit immutable boundary; Stage 98 branch delta must remain zero. |

### Finding Convention

Every material finding uses the complete pack field set and closed verdict/depth
vocabularies. A cleanup decision is separate from a finding verdict; neither
field can be inferred from the other.

#### WGA-DSP-001 — Fail-closed cleanup ledger established

- **Request IDs**: Legacy/Deprecated documents and one-shot documents/scripts coverage rows in the pack index.
- **Scope**: candidate provenance, consumer, replacement, decision, evidence, and post-delete record contract.
- **Expected state**: later tasks reject deletion unless every proof field is complete and reviewed.
- **Observed state**: the record shape and protected categories are established; candidate-specific consumer and replacement evidence is pending.
- **Evidence**: `docs/03.specs/054-workspace-governance-audit-and-remediation/spec.md#c-wga-007--deletion-by-proof`; `docs/99.templates/support/legacy-cleanup-rules.md#active-vs-historical-references`; `docs/00.agent-governance/contracts/agent-legacy-cutover.json#scanPolicy`; `docs/00.agent-governance/contracts/agent-legacy-cutover.json#replacementSurfaces`; `scripts/validate-agent-legacy-cutover.py#main`; `scripts/README.md#script-inventory`; `docs/98.archive/README.md#stage-contract`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Partial`.
- **Impact**: cleanup can fail closed, but no candidate can yet be deleted or called proof-complete.
- **Disposition**: `Keep`.
- **Canonical owner**: this dated disposition ledger for candidate evidence; current policy and replacement surfaces retain implementation authority.
- **Verification**: candidate-table completeness, zero-consumer, replacement, history, post-delete, link, and Stage 98 diff checks in WGIA-009/WGIA-013.
- **Uncertainty**: exact candidate set, consumers, replacements, unique evidence, and post-delete behavior are not yet reviewed.
- **Blocker**: none for the foundation; every candidate-specific deletion remains `DEFER` until proof closes.

## Sources

Source roles are closed to `policy owner`, `machine owner`, `human index`,
`evidence producer`, and `historical snapshot`.

| Source ID | Source role | Evidence at the observation commit | Use |
| --- | --- | --- | --- |
| SRC-WGA-DSP-001 | policy owner | `docs/03.specs/054-workspace-governance-audit-and-remediation/spec.md#c-wga-007--deletion-by-proof`; `docs/99.templates/support/legacy-cleanup-rules.md#active-vs-historical-references` | Classification and proof boundary. |
| SRC-WGA-DSP-002 | machine owner | `docs/00.agent-governance/contracts/agent-legacy-cutover.json#scanPolicy`; `docs/00.agent-governance/contracts/agent-legacy-cutover.json#replacementSurfaces`; `docs/00.agent-governance/contracts/agent-legacy-cutover.schema.json#properties` | Exact current cutover evidence shape. |
| SRC-WGA-DSP-003 | evidence producer | `scripts/validate-agent-legacy-cutover.py#main`; `scripts/validate-links-and-owners.py#main`; `scripts/archive_validation.py#ARCHIVE_ROOT`; `scripts/README.md#script-inventory` | Consumer, history, and boundary evidence. |
| SRC-WGA-DSP-004 | historical snapshot | `docs/90.references/audits/2026-05-24-whga/README.md#snapshot-contract`; `docs/90.references/audits/2026-07-02-whia/README.md#snapshot-contract`; `docs/90.references/audits/2026-07-03-wdgh/README.md#snapshot-contract`; `docs/90.references/audits/2026-07-04-wdcn/README.md#snapshot-contract`; `docs/90.references/audits/2026-07-05-wea/README.md#snapshot-contract`; `docs/90.references/audits/2026-07-11-weia/README.md#snapshot-contract`; `docs/98.archive/README.md#document-index` | Historical interpretation and recovery only. |

## Review and Freshness

- Review status: `Pending` for WGIA-009 disposition review.
- Review disposition: `DEFER`; no candidate-specific delete decision exists.
- Evidence observed: 2026-08-09 at the exact observation commit.
- Current-truth owners: current cleanup policy, legacy-cutover machine contract,
  exact candidate consumers/replacements, and this dated evidence ledger.
- Refresh triggers: candidate, source commit, class, consumer, replacement,
  decision, evidence, post-delete gate, historical route, observation commit,
  or protected-boundary change.
- Hosted, provider-runtime, remote, credential-bearing, and live evidence
  remains `DEFER` unless a later authorized decision requires it.

## Related Documents

- [Pack Index](README.md)
- [Spec 054](../../../03.specs/054-workspace-governance-audit-and-remediation/spec.md)
- [Legacy Cleanup Rules](../../../99.templates/support/legacy-cleanup-rules.md)
- [Implementation Task](../../../04.execution/tasks/2026-08-09-workspace-governance-audit-and-remediation.md)
- [Prior Current Audit](../2026-07-11-weia/README.md)
