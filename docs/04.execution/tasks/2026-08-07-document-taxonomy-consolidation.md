---
title: 'Task: Document Taxonomy Consolidation'
type: sdlc/task
status: active
owner: platform
updated: 2026-08-08
---

# Task: Document Taxonomy Consolidation

## Overview

This task records execution evidence for the sixteen work packages of the
document taxonomy consolidation program. Each row closes when its package is
committed with a passing repository quality gate and its named evidence is
recorded here.

Completion evidence is repository-static. No hosted CI, provider-runtime,
remote, live-cluster, or credential-bearing result is produced or claimed.

## Inputs

- **Plan**:
  [Document Taxonomy Consolidation Implementation Plan](../plans/2026-08-07-document-taxonomy-consolidation.md)
- **Specification**:
  [Spec 052](../../03.specs/052-document-taxonomy-consolidation/spec.md)
- **Program requirement**:
  [PRD-008](../../01.requirements/008-workspace-document-taxonomy-consolidation.md)
- **Architecture**:
  [ARD-0011](../../02.architecture/requirements/0011-document-taxonomy-consolidation-architecture.md)
- **Decision**:
  [ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- **External evidence**:
  `docs/90.references/research/2026-08-07-wer/documentation-architecture-and-diataxis.md`; [current lookup](../../90.references/research/2026-08-08-wer/documentation-architecture-and-diataxis.md)
- **Baseline commit**: `dd54f844` — the program definition commit against which
  every per-asset reduction delta is measured.

## Task Table

| ID       | Upstream criterion         | Work item                                                                                                                        | Owner    | Status | Result       | Evidence                                                                        |
| -------- | -------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | -------- | ------ | ------------ | ------------------------------------------------------------------------------- |
| WORK-000 | VAL-WDTC-010               | Activate the Spec 052 reciprocal execution path and record the PRD-007 execution pause                                           | platform | Done   | PRD-008, ARD-0011, Spec 052, and the Spec 052 plan and task are `active`; Spec 047 and its plan and task are `draft`; PRD-007 stays `active` and records why its execution is paused and how it resumes; no PRD-007 tranche executed | Implementation commit `b5d7d07b`; program lineage registry now declares the PRD-008/ARD-0011/Spec-052 relation; repository quality gate PASS |
| WORK-001 | VAL-WDTC-006               | Delete the completed migration census, its five exclusive validators, their tests, and the zero-referent cutover manifest script | platform | Queued | Not executed | Zero-referent search output and the deletion commit                             |
| WORK-002 | VAL-WDTC-006               | Superseded — delegate the 2026-07-04, 2026-07-07, and 2026-08-07 research-pack replacement to Spec 053                           | platform | Superseded | No WDTC execution; human-approved Spec 053 owns integration, Git/ledger provenance, and deletion in WERPC-008 without new Stage 98 copies | `Spec 053` and `WERPC-008` in `docs/04.execution/tasks/2026-08-08-workspace-engineering-research-pack-consolidation.md` |
| WORK-003 | VAL-WDTC-006               | Rotate the shared progress ledger to a bounded retention window                                                                  | platform | Queued | Not executed | Recovery listing per rotated period and archive validation result               |
| WORK-004 | VAL-WDTC-001               | Archive the 24 orphan plans and 3 orphan tasks                                                                                   | platform | Queued | Not executed | Status enumeration proving every member is done, plus archive validation        |
| WORK-005 | VAL-WDTC-001               | Build the enumerated migration tool with one test per abort condition                                                            | platform | Queued | Not executed | Focused unit test result showing RED before GREEN                               |
| WORK-006 | VAL-WDTC-001               | Co-locate the 39 work units and retire the execution stage                                                                       | platform | Queued | Not executed | Dry-run change set, post-migration inventory, zero live execution-path search   |
| WORK-007 | VAL-WDTC-003               | Renumber the operations stage and rewrite every non-archive reference                                                            | platform | Queued | Not executed | Reference counts before and after with the archive exclusion set enumerated     |
| WORK-008 | VAL-WDTC-002, VAL-WDTC-005 | Enforce work-unit locality, filename dates, and stage sequence; retire the date-based rule                                       | platform | Queued | Not executed | Focused test result and zero-hit search for the retired sentence                |
| WORK-009 | VAL-WDTC-004               | Declare and validate reciprocal cross-stage lineage in frontmatter                                                               | platform | Queued | Not executed | Lineage validation over the full Stage 03 corpus                                |
| WORK-010 | VAL-WDTC-005               | Collapse the ten authoring-rule documents into three owners                                                                      | platform | Queued | Not executed | Sentence-level rule inventory and the rule-uniqueness check result              |
| WORK-011 | VAL-WDTC-006               | Remove the 24 template mirror profiles and route template forms to their authored profile                                        | platform | Queued | Not executed | Route coverage diff proving unchanged uncovered and ambiguous counts            |
| WORK-012 | VAL-WDTC-006               | Consolidate the agent governance role evaluation contracts                                                                       | platform | Queued | Not executed | Test count floor comparison and the recorded size delta                         |
| WORK-013 | VAL-WDTC-007               | Disposition documentation gaps DOC-G1 through DOC-G10                                                                            | platform | Queued | Not executed | Per-gap implemented control or dated recorded decision                          |
| WORK-014 | VAL-WDTC-008               | Reconcile the script surface with the validator selection contract                                                               | platform | Queued | Not executed | Enforcement closure check result                                                |
| WORK-015 | VAL-WDTC-009, VAL-WDTC-011 | Measure per-asset deltas, verify every criterion, prove archive inviolability, review, and close                                 | platform | Queued | Not executed | Delta table, criterion walk, zero-modification archive diff, review disposition |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/**` except `docs/98.archive/**` for modification, `scripts/**`, `tests/**`, `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.claude/**`, `.agents/**`, `.codex/**`, `.gemini/**`
- **Forbidden Paths**: `docs/98.archive/**` for modification of existing records, `gitops/**`, `infrastructure/**`, `traefik/**`, `policy/**`, `secrets/**`
- **Approval Required**: Human approval before modifying any existing archive record, renumbering any existing stage identifier, removing an enforced rule whose negative fixture cannot be located, or taking any action outside the local repository.
- **Static Validation**: `bash scripts/validate-repo-quality-gates.sh .` before every commit; expected PASS. Package-specific focused checks are listed in the Plan's Verification Plan.
- **Live Validation**: DEFER — this program performs no live, hosted, remote, or credential-bearing action, and claims no such evidence.
- **Secret / Vault Handling**: No secret, token, kubeconfig, credential file, or ignored state is read or printed. Secret-handling gates run unchanged.
- **Rollback Plan**: Each work package is one revertible commit. Migration packages run only against a clean working tree, so `git checkout` of the affected paths restores the prior state. WORK-012 is isolated so it can be reverted without disturbing any predecessor.
- **Evidence Location**: This task document and `docs/00.agent-governance/memory/progress.md`.

## Verification Summary

WORK-000 is closed. `bash scripts/validate-repo-quality-gates.sh .` returned
PASS on the staged WORK-000 tree, and the strict links/owners, Markdown profile,
and document contract registry lanes each returned PASS. The result is
repository-static. WORK-001 through WORK-015 are not executed. Each remaining
package records its own lane outcome here as it closes, including any
limitation, SKIP, or DEFER with its reason and owner.

Known limitations declared in advance:

- Hosted CI, provider-runtime, remote, and live evidence are `DEFER` for the
  whole program.
- Archive records are excluded from every rewrite; their historical links
  resolve against each record's `source_commit` and are not re-verified against
  the working tree.
- Stage 90 dated observations retain retired paths by design; those retained
  paths are annotated, not corrected.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result        | Evidence                                                             |
| --------------------- | ------------- | -------------------------------------------------------------------- |
| [WORK-000](../plans/2026-08-07-document-taxonomy-consolidation.md#work-breakdown) | Done. | Status diff for PRD-007, Spec 047, and the Spec 052 triad in commit `b5d7d07b`, with the repository quality gate PASS. |
| N/A — WORK-001 shares the Plan and Spec sources above | Not executed. | Zero-referent search output and the deletion commit. |
| N/A — WORK-002 shares the Plan and Spec sources above | Superseded; no WDTC execution. | Spec 053 and WERPC-008 own the reviewed three-pack cutover. |
| N/A — WORK-003 shares the Plan and Spec sources above | Not executed. | Recovery listing per rotated period and archive validation result. |
| N/A — WORK-004 shares the Plan and Spec sources above | Not executed. | Status enumeration and archive validation result. |
| N/A — WORK-005 shares the Plan and Spec sources above | Not executed. | Focused unit test result showing RED before GREEN. |
| N/A — WORK-006 shares the Plan and Spec sources above | Not executed. | Dry-run change set and zero live execution-path search. |
| N/A — WORK-007 shares the Plan and Spec sources above | Not executed. | Reference counts before and after with the exclusion set enumerated. |
| N/A — WORK-008 shares the Plan and Spec sources above | Not executed. | Focused test result and zero-hit retired-sentence search. |
| N/A — WORK-009 shares the Plan and Spec sources above | Not executed. | Lineage validation over the full Stage 03 corpus. |
| N/A — WORK-010 shares the Plan and Spec sources above | Not executed. | Rule inventory and rule-uniqueness check result. |
| N/A — WORK-011 shares the Plan and Spec sources above | Not executed. | Route coverage diff with unchanged uncovered and ambiguous counts. |
| N/A — WORK-012 shares the Plan and Spec sources above | Not executed. | Test count floor comparison and recorded size delta. |
| N/A — WORK-013 shares the Plan and Spec sources above | Not executed. | Per-gap implemented control or dated recorded decision. |
| N/A — WORK-014 shares the Plan and Spec sources above | Not executed. | Enforcement closure check result. |
| N/A — WORK-015 shares the Plan and Spec sources above | Not executed. | Delta table, criterion walk, archive diff, and review disposition. |
