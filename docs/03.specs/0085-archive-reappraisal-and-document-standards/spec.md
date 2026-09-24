---
title: "Archive Reappraisal and Document Standards Technical Specification"
version: "0.3.0"
type: "sdlc/spec"
status: "done"
owner: "platform"
updated: "2026-09-24"
layer: "specs"
artifact_id: "SPEC-0085"
---

# Archive Reappraisal and Document Standards Technical Specification (Spec)

## Overview

This Spec owns the cutover that
[ADR-0040](../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md)
decides, together with the current-navigation corrections and the two
follow-up standards that the same survey found. It delivers a reviewed exit and
a current judgment for retained units, envelope verification against the
default branch, README navigation that matches the tree, and ordered plans for
a common lifecycle vocabulary and a common validation result vocabulary.

Consumers are the lifecycle, link, archive, and cutover gates; the Archive,
Architecture, decision, Spec, Templates, and documentation hub indexes; the
Stage 99 registry; and the quality policy.

**Closure (2026-09-24).** WP-001 to WP-004 are complete with committed evidence (`5d382767`, and `11664e49` through PR #95). WP-005 and WP-006 stay recorded, each waiting for its own approval, as the completion criteria allow. The final full profile passed on `main` at `a264ebad` (hosted `qa`). PR #95 was merged before its hosted `qa` finished. `main` then failed until PR #96 kept the default branch in the QA snapshot and PR #98 re-measured the archive Git budget.

## Strategic Boundaries & Non-goals

In scope: ADR-0040 and its registry, catalog, validator, and test cutover; the
README navigation drift the survey records; REQ-0003-FR-0020; and the plans for
the lifecycle and result vocabularies.

Out of scope: removing or reappraising any real retained unit; rewriting a
frozen body, sealed record, ledger, or catalog row; retaining ADR-0039 or any
waiting Stage 03 package; changing a lifecycle state or edge before its own
decision is accepted; any history purification; any live cluster, Helm, Argo CD,
Vault, secret, kubeconfig, network, or storage action; and push, pull request,
and merge.

## Contracts

- **C-ARS-001 — frozen, not permanent.** An unapproved edit, rename, recreation,
  or partial deletion of a retained unit fails. Whole-unit removal is admitted
  only with a matching `Retention Assessment` row whose availability is
  `git-history-only`, whose Hold is `none`, and whose Decision is a current
  governed document.
- **C-ARS-002 — judgment beside the catalog.** The registry owns the assessment
  and availability values and their conditions. A row names an existing catalog
  record once, and a missing row means `unreviewed` and `retained`.
- **C-ARS-003 — availability precedes citation.** The ordered citation table
  rejects a link from outside Stage 98 to a retained body that is `withdrawn`,
  `invalidated`, or not `retained`, before the Incident exemption applies.
  Every citation judge still consumes that one decision.
- **C-ARS-004 — verifiable envelope.** A catalog commit has the repository's
  object-format length and is reachable from the registry-named default branch.
  An unresolvable branch, shallow clone, missing object, or wrong object type
  fails.
- **C-ARS-005 — navigation is current.** A README table or code-fenced tree that
  presents the current inventory matches the tracked tree.
- **C-ARS-006 — vocabulary migrations never invent facts.** A lifecycle or
  result spelling change maps each current document by its evidence. A mapping
  never creates an approval, execution, or publication that did not happen, and
  frozen bodies keep their spelling.

## Core Design

The work runs as separate integrations because the lifecycle gate admits one
state edge per document per integration. The proposal creates ADR-0040 and this
package. The acceptance integration takes ADR-0040 to `accepted` and ADR-0039 to
`superseded`, activates this package, amends REQ-0003-FR-0020, and cuts the
registry, parser, gates, and tests over together. Navigation corrections that
need no decision land separately under the current contract.

The assessment parser sits beside `parse_catalog` in `archive_dispositions`, and
`citation_decision` receives the parsed assessment so that the link and archive
gates keep sharing one decision. The removal transition extends the base-row
comparison in the lifecycle gate instead of adding an exemption list. Default
branch resolution and object-format length join the Git primitives in
`archive_objects` and `archive_recovery`, which the cutover and lifecycle gates
already import.

The lifecycle vocabulary and the result vocabulary are planned here and executed
only after their own approval, because each changes meaning that many consumers
and pinned historical checks read.

## Data Modeling & Storage Strategy

Git holds every byte. The catalog row stays the only recovery reference. The
`Retention Assessment` table holds current judgment only, keyed by the record
path, and its history is the Git history of the Archive index. No digest, blob
pin, redirect, path ledger, or copy of a removed unit is added.

## Interfaces & Data Structures

- `docs/99.templates/registry.json` gains a top-level `archive_assessment`
  object: the table heading and columns, the assessment and availability value
  lists, their defaults, which values need a Decision or a Current Owner, the
  reserved values, and the default branch name. The profile schema and the
  registry key list in `document_authority` declare it.
- The `archive_citation` rules gain an assessment and availability condition,
  evaluated by `citation_decision` in its existing order.
- The Archive index gains the `Retention Assessment` heading and an empty table.
  No row is added by this Spec.
- The catalog commit grammar accepts the repository object-format length.

## Edge Cases & Error Handling

A row naming a record that has no catalog row, a duplicate row, an unknown
value, a missing Decision, a `superseded` row without a current owner, a Hold
that is not `none` on removal, a partial unit removal, availability returning to
`retained`, and any `purged` row each fail with a distinct diagnostic. A catalog
row whose unit is `git-history-only` is not a missing payload, but its envelope
is still verified. A retained unit without a catalog row cannot be reappraised
or removed.

## Failure Modes & Fallback / Human Escalation

A failing gate stops the integration; no check, test pin, or contract is
weakened to pass. When the default branch or the named history is unavailable,
the check fails, and the report names the missing reference. Whether a Decision
document's approval is real is a reviewer's judgment and is escalated to the
request owner, never inferred from the document's presence.

## Verification Commands

```bash
python3 scripts/run-archive-contract-tests.py --root .
python3 scripts/validate-document-lifecycle.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/qa.py staged
python3 scripts/qa.py full
```

## Success Criteria & Verification Plan

| ID          | Criterion                                                                                                                                                                                                                                  | Evidence                        |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------- |
| VAL-ARS-001 | The survey records the current contract, implementation, and navigation findings with their files and lines, and separates observed defects from intended future behavior                                                                  | Proposal Task                   |
| VAL-ARS-002 | ADR-0040 is proposed without changing any validator, and every gate still enforces ADR-0039                                                                                                                                                | Staged QA on the proposal       |
| VAL-ARS-003 | Every README inventory, table, and tree that presents current state matches the tracked tree, including the ADR-0038 residue                                                                                                               | Link gate and navigation review |
| VAL-ARS-004 | The registry declares the assessment contract, and a real temporary Git repository proves approved whole-unit removal passes while unapproved edit, rename, recreation, partial removal, held removal, and removal without a Decision fail | Archive contract tests          |
| VAL-ARS-005 | A `git-history-only` unit is not reported as a missing payload, and its envelope is still verified                                                                                                                                         | Archive contract tests          |
| VAL-ARS-006 | A citation from outside Stage 98 to a `withdrawn`, `invalidated`, or non-retained unit fails, a `superseded` unit stays citable, and a Stage 98 source is unaffected                                                                       | Citation decision tests         |
| VAL-ARS-007 | A `purged` row fails, so a plain removal can never claim purification                                                                                                                                                                      | Archive contract tests          |
| VAL-ARS-008 | Envelope checks use the default branch and the object-format length, and fail on an unresolvable branch, shallow clone, missing object, wrong type, mode change, symlink change, missing native member, and empty tree                     | Git fixture tests               |
| VAL-ARS-009 | ADR-0040 is accepted, ADR-0039 is superseded reciprocally, and REQ-0003-FR-0020 names the approved exit                                                                                                                                    | Lifecycle gate                  |
| VAL-ARS-010 | The lifecycle vocabulary plan maps every current document by evidence, keeps frozen spellings readable, and waits for its own decision                                                                                                     | Plan review                     |
| VAL-ARS-011 | The result vocabulary plan maps `DEFER` to `BLOCKED` or `NOT_RUN` by cause, adds `N/A`, and names scope, snapshot, and place without rewriting past evidence                                                                               | Plan review                     |
| VAL-ARS-012 | This package closes with observed staged and full results and names any unexecuted lane                                                                                                                                                    | Task evidence                   |

### Document Impact

| Document or family                                                     | Change needed                | Profile                         | Standard item                    | Owning work    | Verification               | Reason when not applied                                                                   |
| ---------------------------------------------------------------------- | ---------------------------- | ------------------------------- | -------------------------------- | -------------- | -------------------------- | ----------------------------------------------------------------------------------------- |
| REQ-0003                                                               | FR-0020 amendment            | `sdlc/requirement`              | Acceptance boundary              | WP-003         | Lifecycle and link gates   | —                                                                                         |
| ADR-0039 / ADR-0040                                                    | Supersession                 | `sdlc/architecture-decision`    | One decision, reciprocal lineage | WP-001, WP-003 | Lifecycle gate             | —                                                                                         |
| AD-0006                                                                | Review only                  | `sdlc/architecture-description` | Current structure                | WP-003         | Review                     | Units, catalog, and gates keep their structure; a table is added inside the Archive index |
| Stage 98 index                                                         | Assessment table             | `common/readme-stage-index`     | Catalog and navigation           | WP-003         | Archive and link gates     | —                                                                                         |
| Stage 01, 02, decisions, descriptions, 03, 05, 90, 99, and hub indexes | Drift correction where found | `common/readme-*`               | README meaning                   | WP-002         | Link gate and review       | An index with no finding is left unchanged                                                |
| Stage 99 registry and schema                                           | Assessment contract          | Registry                        | Single machine owner             | WP-003, WP-004 | Registry and archive tests | —                                                                                         |
| Quality policy                                                         | Result vocabulary            | `governance/rule`               | Result meaning                   | WP-006         | Plan review                | Planned only in this round                                                                |
| Operations documents                                                   | None                         | `operation/*`                   | Role boundaries                  | —              | —                          | No operations contract changes                                                            |

## Traceability

The [Implementation Plan](plan.md) owns order and risk. The
[proposal Task](tasks/tsk-0001-propose-archive-reappraisal-and-document-standards.md)
owns the survey and the proposal evidence.

### Lifecycle Traceability

| Requirement ID                                                                        | Spec criterion | Verification method         |
| ------------------------------------------------------------------------------------- | -------------- | --------------------------- |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARS-001    | Survey recorded in the Task |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARS-002    | Staged QA                   |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARS-003    | Link gate and review        |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARS-004    | Archive contract tests      |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARS-005    | Archive contract tests      |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARS-006    | Citation decision tests     |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARS-007    | Archive contract tests      |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARS-008    | Git fixture tests           |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARS-009    | Lifecycle gate              |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARS-010    | Plan review                 |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARS-011    | Plan review                 |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARS-012    | Staged and full QA          |
