---
title: 'Audit: Remediation and Integration Roadmap'
type: content/reference
status: draft
owner: platform
updated: 2026-08-09
---

# Audit: Remediation and Integration Roadmap

## Overview

This report owns cross-report finding normalization, dependencies, priorities,
target state, canonical implementation owners, cutover sequence, rollback, and
the residual `DEFER` backlog. WGIA-001 establishes the integration form only;
WGIA-009 populates the reviewed roadmap after the topical audits.

## Reference Type

Dated repository-static integrated audit roadmap. It is not an implementation
owner, permission grant, deletion authority, Current-pointer owner, or approval
to change active policy and operations.

## Authority Boundary

Source reports retain their findings and evidence. This roadmap may deduplicate
and order only reviewed findings, then route accepted work to canonical owners.
It cannot rescore source evidence, resolve an ambiguous approved decision,
change Current navigation, or promote deeper evidence.

## Scope

Included: cross-report identifiers, dependencies, priorities, target-state
outcomes, implementation owners, verification, blockers, cutover, rollback,
and residual uncertainty. Excluded: unreviewed topic conclusions, direct
canonical remediation, Current cutover, deletion, remote actions, and closure.

## Definitions / Facts

### Integration Inputs

The eight focused reports are draft inputs. Each currently contains one
foundation finding and a report-local owner/source boundary. WGIA-009 may admit
a finding here only after its required fields and source-report review are
complete.

### Roadmap Record Convention

Each integrated row requires: integrated ID, source finding IDs, affected
request scopes, problem statement, dependency, priority, target state,
canonical implementation owner, validation, verification, rollback, blocker,
evidence depth, and status. Unknown owners or unresolved approved-decision
conflicts fail closed to `DEFER`.

### Foundation Dependency Map

| Phase | Inputs | Output boundary | Initial state |
| --- | --- | --- | --- |
| Topical audit | WGIA-002 through WGIA-008 | Reviewed report-local findings | `DEFER` pending those tasks. |
| Integrated disposition | Reviewed source findings plus cleanup candidates | Deduplicated roadmap and candidate decisions in WGIA-009 | `DEFER` pending review. |
| Canonical remediation | Accepted unambiguous roadmap rows | Owner changes in WGIA-010 and WGIA-011 | `DEFER` pending approval/evidence. |
| Atomic cutover | Complete pack plus machine/current projections | Sole Current transition in WGIA-012 | `DEFER` pending cutover gates. |
| Cleanup | Proof-complete `Delete` rows | Exact removals in WGIA-013 | `DEFER` pending zero-consumer proof. |
| Closure | Re-audit, full QA, reviews, and logical history | WGIA-014 terminal handoff | `DEFER` pending all prior work. |

### WGIA-002 Provisional Inputs

These rows are candidate inputs for WGIA-009, not implementation approval.
Their source findings remain authoritative until independent review and
integrated admission complete.

| Candidate ID | Source findings | Request IDs | Problem | Dependency | Priority | Target state | Canonical implementation owner | Validation | Verification | Rollback | Blocker | Evidence depth | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WGA-RMP-GOV-001 | `WGA-GOV-002`, `WGA-GOV-003` | `REQ-WGA-001`, `REQ-WGA-002`, `REQ-WGA-012` | Root `README.md` presents thin `AGENTS.md` as a canonical owner and omits/misclassifies the `.gemini/` versus `.agents/` adapter boundary. | WGIA-002 reviews Approved; WGIA-009 deduplication/admission remains required before WGIA-010. | P1 owner-routing integrity | `README.md#canonical-owners` points to the Stage 00 policy SSoT; `README.md#top-level-areas` names all four tracked surface classes without promoting provider runtime. | `README.md` human onboarding owner; Stage 00 and `harness-contract.json` remain classification sources. | Deterministic root-routing regression plus governance closure, harness contract/semantics/currentness, strict profile, and strict link checks. | Reviewer confirms the human overview resolves to one policy owner, retains thin gateways, includes `.gemini/`, distinguishes `.agents/`, and keeps runtime claims `DEFER`. | Revert only the later bounded `README.md` correction; current Stage 00 and adapter files require no rollback. | WGIA-009 admission pending. | `repository-static` | `Provisional` |

### WGIA-003 Provisional Inputs

These rows are candidate inputs for WGIA-009, not implementation approval.
Their source findings remain authoritative until independent review and
integrated admission complete.

| Candidate ID | Source findings | Request IDs | Problem | Dependency | Priority | Target state | Canonical implementation owner | Validation | Verification | Rollback | Blocker | Evidence depth | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WGA-RMP-DOC-001 | `WGA-DOC-002` | `REQ-WGA-016`, `REQ-WGA-019`, `REQ-WGA-023` | The broad Release request has no current contract and is not explicitly mapped to approved DOC-G5, which already rejects the narrower release-notes type. | WGIA-003 specification and fix-round quality reviews Approved; WGIA-009 deduplication into DOC-G5 and queued WORK-013 remains pending; do not reopen the approved negative decision. | P1 semantic owner routing | Preserve no first-class release-notes type, execute WORK-013's deliberate-absence text, and record whether the broader Release request resolves to an existing evidence owner or remains explicitly unmapped. | Approved Spec 052 DOC-G5; WDTC Plan and Task WORK-013 for execution; current Stage 99/Stage 05 owners remain unchanged. | WORK-013 evidence plus registry/profile/lifecycle/links and the zero-dimension Release probe. | Reviewer confirms the broad-versus-narrow distinction, the DOC-G5 decision, and no new release-notes route. | Revert only later WORK-013 text if required; do not remove or reopen approved DOC-G5. | WORK-013 queued; broader semantic mapping absent. | `repository-static` | `Provisional` |
| WGA-RMP-DOC-002 | `WGA-DOC-003` | `REQ-WGA-018`, `REQ-WGA-019` | Approved DOC-G1 owns `how-to`, `tutorial`, `concept`; heading/template/current-guide evidence exists, but registry enum enforcement and all-eight-guide validation remain unimplemented. | WGIA-003 specification and fix-round quality reviews Approved; WGIA-009 deduplication and routing to queued WORK-013 remains pending; no fresh taxonomy design. | P1 approved-control completion | Execute WORK-013: enforce the three-value registry enum, validate all eight `how-to` guides, and record DOC-G2/DOC-G3 deliberate absences without creating routes. | Approved Spec 052 DOC-G1 through DOC-G3; WDTC Plan/Task WORK-013 and Stage 99 registry/template owners. | Invalid-value negative fixture, registry/profile/lifecycle/links, and explicit eight-guide migration/validation evidence. | Reviewer confirms the approved enum is enforced, all eight guides pass, and no tutorial/explanation route was created. | Revert only the bounded WORK-013 registry/template/lifecycle implementation while preserving approved Spec 052. | WORK-013 queued; deterministic enum and migration evidence absent. | `repository-static` | `Provisional` |

### WGIA-005 Provisional Inputs

This row is a candidate input for WGIA-009, not implementation approval. The
source finding remains authoritative until quality re-review and integrated
admission complete; no script, validator, fixture, or disposition changes here.

| Candidate ID | Source findings | Request IDs | Problem | Dependency | Priority | Target state | Canonical implementation owner | Validation | Verification | Rollback | Blocker | Evidence depth | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WGA-RMP-HAR-001 | `WGA-HAR-003` | `REQ-WGA-017` | The canonical `scripts/README.md` human inventory omits tracked import-only helpers `scripts/archive_cutover_manifest.py` and `scripts/reference_information_architecture.py`; observation inventory is 47 scripts = 41 CLI + six helpers. | WGIA-005 specification/content and fix-round quality reviews Approved; WGIA-009 deduplication/admission is required before WGIA-011 or the current human-index owner changes. | P2 human inventory completeness | `scripts/README.md` names all 47 tracked script files, identifies the six import-only helpers, and preserves the existing production semantic owners/callers. | `scripts/README.md` human inventory owner; current scripts, contracts, validators, tests, and fixtures retain production ownership. | Re-run the deterministic observation/current 47 = 41 + 6 probe with zero missing human-index paths, then strict registry/profile/link and focused harness checks. | Reviewer confirms both missing helper rows are present, no CLI/helper is misclassified, and no aggregate/helper is promoted to a duplicate semantic owner. | Revert only the later bounded `scripts/README.md` inventory correction; production scripts/contracts/tests require no rollback. | WGIA-009 admission pending. | `repository-static` | `Provisional` |

### WGIA-006 Provisional Inputs

This row is a candidate input for WGIA-009, not implementation approval. The
source finding remains authoritative until WGIA-006 independent review and
integrated admission complete. Generated output must be changed only through
its producer.

| Candidate ID | Source findings | Request IDs | Problem | Dependency | Priority | Target state | Canonical implementation owner | Validation | Verification | Rollback | Blocker | Evidence depth | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WGA-RMP-KNW-001 | `WGA-KNW-002` | `REQ-WGA-022` | LLM-WIKI README and generated output retain 2026-05-10 source/review metadata although all six RIA-declared inputs and the producer/output changed later; byte equality alone does not prove on-source-change review. | WGIA-006 specification/content and quality reviews Approved; WGIA-009 deduplication/admission is required before WGIA-010 changes the current knowledge owners. | P1 freshness evidence integrity | Review all six declared inputs and current owner links; record current review metadata in the README and generator; regenerate output through the producer without adding a runtime/search claim or hand editing. | `docs/90.references/llm-wiki/README.md` for review/freshness declaration; `scripts/generate-llm-wiki-index.sh` for emitted metadata; target documents retain fact/policy ownership. | Generator `--check`, three focused RIA generator-relation tests, strict profiles/links, and deterministic declared-input last-change versus review-date proof. | Reviewer confirms six-input review, current links, truthful metadata, generator-only output, and continued reference-only boundary. | Revert only the later bounded README/generator/generated-output logical unit; canonical targets and memory contracts require no rollback. | WGIA-009 admission pending. | `repository-static` | `Provisional` |

### Finding Convention

Every material roadmap finding keeps the complete pack field set and closed
audit verdict/depth vocabularies. Integrated priority and status never replace
the source verdict, evidence, uncertainty, blocker, or canonical owner.

#### WGA-RMP-001 — Integrated roadmap foundation established

- **Request IDs**: all request rows through their primary source-report owners.
- **Scope**: cross-report admission, dependency, remediation, cutover, rollback, and residual-backlog structure.
- **Expected state**: WGIA-009 can integrate only complete, reviewed source findings and route each accepted action to one current owner.
- **Observed state**: source-report identities, execution dependencies, and fail-closed admission rules are established; no topical finding is yet integrated.
- **Evidence**: `docs/03.specs/054-workspace-governance-audit-and-remediation/spec.md#audit-pack-components`; `docs/03.specs/054-workspace-governance-audit-and-remediation/spec.md#success-criteria--verification-plan`; `docs/04.execution/plans/2026-08-09-workspace-governance-audit-and-remediation.md#detailed-tasks`; `docs/04.execution/tasks/2026-08-09-workspace-governance-audit-and-remediation.md#task-table`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Partial`.
- **Impact**: later integration has a bounded structure, but no remediation, cutover, deletion, or closure conclusion is approved.
- **Disposition**: `Keep`.
- **Canonical owner**: source reports for findings; current Stage 00-05/90/99, workflow, script, test, and manifest surfaces for implementation.
- **Verification**: finding-field completeness, unique owner, dependency, strict link, rollback, blocker, and independent roadmap review in WGIA-009.
- **Uncertainty**: topical findings, deduplication, priority, accepted target states, blockers, and remediation deltas are pending.
- **Blocker**: none for the foundation; all downstream roadmap phases remain explicit `DEFER`.

## Sources

Source roles are closed to `policy owner`, `machine owner`, `human index`,
`evidence producer`, and `historical snapshot`.

| Source ID | Source role | Evidence at the observation commit | Use |
| --- | --- | --- | --- |
| SRC-WGA-RMP-001 | policy owner | `docs/03.specs/054-workspace-governance-audit-and-remediation/spec.md#c-wga-003--canonical-authority-preservation`; `docs/03.specs/054-workspace-governance-audit-and-remediation/spec.md#finding-record` | Admission and implementation boundary. |
| SRC-WGA-RMP-002 | human index | `docs/90.references/audits/README.md#audit-pack-registry`; `docs/03.specs/054-workspace-governance-audit-and-remediation/spec.md#traceability`; `docs/04.execution/plans/2026-08-09-workspace-governance-audit-and-remediation.md#new-audit-pack` | Request routing and planned report ownership. |
| SRC-WGA-RMP-003 | evidence producer | `scripts/validate-document-contract-registry.py#main`; `scripts/validate-markdown-profiles.py#main`; `scripts/validate-links-and-owners.py#main`; `docs/04.execution/tasks/2026-08-09-workspace-governance-audit-and-remediation.md#verification-summary` | Admission and closure evidence. |
| SRC-WGA-RMP-004 | historical snapshot | `docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md#target-operating-model` | Dated comparison only; no current priority authority. |

## Review and Freshness

- Review status: `Pending` for WGIA-009 independent integration review.
- Review disposition: `DEFER`; no topical roadmap item is admitted yet.
- Evidence observed: 2026-08-09 at the exact observation commit.
- Current-truth owners: source reports for dated findings and canonical active
  surfaces for implementation.
- Refresh triggers: source finding, review, dependency, priority, target state,
  canonical owner, validation, verification, rollback, blocker, cutover,
  deletion, observation commit, or residual-risk change.
- Hosted, provider-runtime, remote, credential-bearing, and live evidence
  remains `DEFER`.

## Related Documents

- [Pack Index](README.md)
- [Spec 054](../../../03.specs/054-workspace-governance-audit-and-remediation/spec.md)
- [Implementation Plan](../../../04.execution/plans/2026-08-09-workspace-governance-audit-and-remediation.md)
- [Implementation Task](../../../04.execution/tasks/2026-08-09-workspace-governance-audit-and-remediation.md)
- [Disposition Ledger](legacy-deprecated-and-one-shot-disposition-ledger.md)
