---
title: "W03 Retired Identity Reservation"
version: "0.3.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0180-TSK-0001"
parent_ids: ["SPEC-0180-PLAN-0001"]
---

# Task: W03 Retired Identity Reservation

## Overview

This Task records handoff W03-H03 (from W02-H01), the reservation of retired identities named in `Archived Lineage`, for [SPEC-0180](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items, to investigate remaining, unverified, unreviewed, unconfirmed, unstarted, conflicting and missing items, to follow the W00 to W03 requirements where a choice or correction is needed, to present decisions with options, to check existing work first, to do now anything due before W03, to start work that can run in parallel, and approved commit, push, PR and merge. The request approves no Spec bytes or criterion.
- **Base:** branch `claude/w03-retired-identity` from `9308095a` (`main` merge of PR #244); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W02-H01, W03-H03 and EVD-018 (current v14.7 requirements prevail); EVD-023 and EVD-024 observed the gap.
- **Decisions recorded with this package:** W03-D22 (`layer`), W03-D23 (`title`) and W03-D24 (generator), from the user's 2026-11-13 answers, and the rows W03-H14 to W03-H24 from the 2026-11-13 read-only W03 gap audit; all appended to the SPEC-0161 Task.
- **Requirement basis:** the lifecycle policy rule that stable identities are append-only and never reused; REQ-0003-FR-0023; read-only inputs under `_workspace/workspace_execution_tasks/`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RETIRED-001](../spec.md#success-criteria--verification-plan) | Lineage-identity helper; evidence-context field; reuse check and callers; history memo; tests. | platform | completed | PASS | EVD-004 |
| WORK-002 | [VAL-RETIRED-002](../spec.md#success-criteria--verification-plan) | Policy sentence; regression and exact-index QA. | platform | completed | PASS | EVD-005, EVD-006, EVD-007; implementation commit `cb498bcf` passed exact-index QA and the hooks |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-RETIRED-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `7d0a1563…`, plan.md `a29f3710…`, with scratch simulations of the lineage tokens over the tracked tree and a replay over 120 first-parent commits; 2026-11-13 | FAIL | REJECT: BLOCK `compare_lifecycle` holds no text, so the retired set must travel on `LifecycleEvidenceContext` filled by `_evidence_context`; FIXes on the identity grammar (schema `terminalArtifactId` plus historical prefixes), a dangling decision reference, end-to-end tests, a per-commit memo and the risk scoring; NITs on the reservation source, table parsing, the keyword-only argument and the Task text. The reviewer found six lineage documents, about 200 tokens in three shapes, no live identity newly refused and no replay hit. | no | none |
| EVD-002 | [VAL-RETIRED-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"8d43328200a7f60f050eee01bffe239eda247130fe1a17b267852820e4a25464","plan_sha256":"ba7e926a3cb13eb987ca28bc841aae0433b9e49623e92930f6e89a5af47c60df"} | PASS | Same reviewer, rounds 2 and 3, 2026-11-13: every round-1 finding verified fixed; round 2 asked the Plan to name the SPEC-0161 rows and the Spec to define them, both verified in round 3 with no other change in meaning; verdict APPROVE. The package commit must append W03-D22 to W03-D24, which the Spec cites. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-RETIRED-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0180 approval question naming spec.md 8d433282 and plan.md ba7e926a dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0180","SPEC-0180-PLAN-0001"],"reviewed_spec_sha256":"8d43328200a7f60f050eee01bffe239eda247130fe1a17b267852820e4a25464","reviewed_plan_sha256":"ba7e926a3cb13eb987ca28bc841aae0433b9e49623e92930f6e89a5af47c60df","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-004 | [VAL-RETIRED-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Lineage-identity helper, evidence context, reuse check, history memo and tests, red then green | Working tree over `2646fd4f`; implementer quality-engineer subagent, then an author fix, re-run by the author with `hyhome.validationVenv/bin` on `PATH`; 2026-11-13 | PASS | Red (implementer log): the six new unit tests raised 12 errors before the helper and keyword existed; the two Git tests failed on behavior (explicit-ref returned `PASS lifecycle validation mode=explicit-ref` and the direct history call returned no diagnostic). Green: `tests.test_document_artifact_identity` and `tests.test_document_lifecycle_cumulative_history` 56 OK. `lineage_retired_identities` reads first cells of every `Archived Lineage` table with the schema `terminalArtifactId` grammar plus `OPS` and `MIG`, guarded on both sides, and maps each token to the first document naming it; `LifecycleEvidenceContext.retired_identities` is filled by `_evidence_context`; `compare_lifecycle` and the two direct history calls pass it, the cache memoizing per commit. The implementer's diagnostic named only "an Archived Lineage"; the author changed the set to a map so the observed text names the reserving document's path, as the Spec requires, and updated the tests. Modes reading lineage: staged, ci, explicit-ref and cumulative history; snapshot and completion run no reuse check. Replay over the last 120 first-parent commits: 164 new-at-path identities, 0 refused. Deriving the set over one snapshot (296 texts, 199 identities): 13 to 15 ms. | yes | none |
| EVD-005 | [VAL-RETIRED-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Policy sentence | Staged diff over `2646fd4f` | PASS | `.agents/governance/document-lifecycle.md` 2.9.0 adds one sentence after "Stable identities are append-only and never reused": retired identities are reserved by the first column of the owners' `Archived Lineage` and checked by `LIFECYCLE-IDENTITY-REUSE`. No other document text changed. | yes | none |
| EVD-006 | [VAL-RETIRED-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Regression over the tree, suites and lint | Author run over the staged index after `2646fd4f`, 2026-11-13 | PASS | The four strict document validators give output byte-identical to the before run at `2646fd4f`. Staged lifecycle PASS; `python3 scripts/qa.py staged` 12 gates PASS. Suites: `agent-governance` 105, `document` 586 (3 skipped), `document-lifecycle` 24, `tooling` 166, `validation-routing` 173 OK. `ruff check scripts tests` and `ruff format --check scripts tests` clean; markdownlint 0 issues; `graphify update .` rc 0. No registry line moved, so `.secrets.baseline` is unchanged. | yes | none |
| EVD-007 | [VAL-RETIRED-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Semantic review: risk class and core-diff checklist | Diff of 5 files over `2646fd4f` | PASS | Risk class `medium` (a lifecycle validator, its adapter, tests and one policy sentence). Checklist: scope matches the Spec; one writer per file; W03-H03 and W02-H01 applied; only first-cell tokens are read and only identities new at a path are judged, so the current `REQ-0001` to `REQ-0003` pass; the helper reads the identity grammar from the checkout's own `frontmatter.schema.json`; no lineage row or other document text changed; no secret read; recovery is reverting the implementation commit. No permission, trigger, hook or workflow file changed. | yes | none |
| EVD-008 | [VAL-RETIRED-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Manual package-exit decision freeze | This package's `spec.md`, `plan.md` and Task; the consumers named below; the user's 2026-11-13 standing approval of commit, push, PR and merge; Git-history-only method | PASS | The consumer, preservation, hold, authority and method decision is frozen below before this package's final source commit. Each file's committed `commit:path`, retained-ref reachability, temporary restoration and byte comparison are recorded in REQ-0003 Archived Lineage before deletion. An unresolved condition defers the affected deletion. This package closes W03-H03 and W02-H01. | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-RETIRED-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-004 | Accepted by the user on 2026-11-13 (direct answer "Accept both" to the SPEC-0180 criterion question naming implementation commit `cb498bcf` and EVD-004 to EVD-007) | platform |
| [VAL-RETIRED-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-005, EVD-006, EVD-007 | Accepted by the user on 2026-11-13 (direct answer "Accept both" to the SPEC-0180 criterion question naming implementation commit `cb498bcf` and EVD-004 to EVD-007) | platform |

### Frozen Package Disposition Decision

- **Target and method**: After the final source commit, retire only this Stage 03 package (`spec.md`, `plan.md` and this Task) through Git-history-only recovery. No other document is selected.
- **Consumers and preservation**: The durable contract is promoted to the document lifecycle policy and `scripts/document_lifecycle.py` (Plan Promotion row). No new handoff arises; the SPEC-0161 rows this package added stay there. Current consumers: the Stage 03 README entry and this Task's `.secrets.baseline` entries, which the closure change removes. Code comments and test docstrings that name SPEC-0180 use it as an identifier, not a link, and stay.
- **Hold and authority**: The current repository documents and the user's request identify no hold on these files. The user's 2026-11-13 standing approval of commit, push, PR and merge is the disposition authority. If a hold or unmet consumer is identified before deletion, the affected deletion is deferred and its source kept. Remote retention is not inferred from local refs.
- **Proof handoff**: This Task freezes the decision before its final source commit. After that commit, each file's exact `commit:path`, blob availability, reachability from the retained local ref and a temporary byte comparison with the source still in the tree are recorded in REQ-0003 Archived Lineage before any file is deleted. This Task cannot contain that proof without changing its own bytes.

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, the W03-D22 to W03-D24, W03-H14 and later and evidence rows and the frontmatter `version` and `updated` of the completed SPEC-0161 Task (appended rows only), `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: every `Archived Lineage` row and other document body, `_workspace/workspace_execution_tasks/`, `.github/`, `.claude/`, `.codex/`, hooks, accepted ADR bodies, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; push, PR and merge are approved by the user's standing 2026-11-13 instruction
- **Static Validation**: strict document validators, `document-lifecycle`, `document` and `validation-routing` suites, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). WORK-001 and WORK-002 implemented with PASS evidence (EVD-004 to EVD-007); implementation commit `cb498bcf`. The user accepted both criteria on 2026-11-13, and the standing approval of commit, push and PR covers the package exit (EVD-008); this package closes W03-H03 and W02-H01. Risk class `medium`. Next owner: W03 for the H07 package.
