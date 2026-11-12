---
title: "W01 Governance Alignment"
version: "0.2.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0166-TSK-0001"
parent_ids: ["SPEC-0166-PLAN-0001"]
---

# Task: W01 Governance Alignment

## Overview

This Task records the W01 governance alignment for [SPEC-0166](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-12 (Asia/Seoul) the user entered the v14.7 W01 prompt (package `_workspace/workspace_execution_tasks/tasks/TASK-hy-home-k8s-W01.md`). The prompt approves no Spec bytes, criterion, push, PR or merge.
- **Base:** branch `claude/w00-v14-7-intake` at `e3d72466`; worktree clean; hook environment `hyhome.validationVenv` set.
- **Decisions reused:** SPEC-0161 EVD-018 (current v14.7 requirements prevail; CI-SCOPE and POLICY-ROLE adopted; Q-07 display numbering; Q-08 path kept).

### Gap Survey

Read-only survey at `e3d72466`. Read fully: the glossary, `sdlc.md`, `quality.md`, `git.md`, `document-authoring.md`, package `REPOSITORY-VOCABULARY.md` and `QA-CHANGE-PROTOCOL.md`. Read partially: the package W01 task, `COMMON-SECTION-CONTRACT.md`, `STAGE-QA-MATRIX.md`, `REGISTRY-REFORM-IMPLEMENTATION.md`, `REQUIREMENTS.json`, the SPEC-0161 Task, `agent-execution.md`, `approval-and-safety.md`, `document-lifecycle.md`, `work-lifecycle.md`, the profile schema, `scripts/document_contracts.py` and the registry `shared_contract`. Not read: `TEMPLATE-DEFINITION-CONTRACT.md` and the tests; the reviewer read `.github/workflows/ci.yml` in round 2 (jobs `ci-summary` and `style-pr` only).

| Item | Current owner | Finding | Action | Writer |
| --- | --- | --- | --- | --- |
| Glossary structure, columns, 33 common IDs, RFC statement | glossary | H1, seven H2 in order, required columns, 33 of 33 IDs with matching meaning, RFC 2119/8174 statement present | KEEP | W01 |
| Glossary `TERM-CI` | glossary | Says CI checks branch metadata; contradicts CI-SCOPE | CHANGE | W01 |
| Glossary Policy Owner cells | glossary | Backticked paths, all existing; not links | CHANGE | W01 |
| GOV-02 extension points | `document-authoring.md` | No list of allowed extension points; no ban on weakening extensions | ADD | W01 |
| GOV-03, QA-C01 contract record | registry `shared_contract`; `document-authoring.md` | No approver, date, scope, effective point, migration, rollback or consumer edition; no `approved` state | CHANGE policy; registry to W03 | W01, W03 |
| GOV-04, R147-03 approval versus adoption | `document-authoring.md` | No statement that an approved edition stays a reform target; no partial-adoption rule | ADD | W01 |
| GOV-05 single-operator roles | `git.md:84`, `quality.md:259-260`, `approval-and-safety.md:66-68` | Fits | KEEP | none |
| GOV-06 derived copies | `document-authoring.md` | Only reverse links and generated files covered | ADD; drift check to W05 | W01, W05 |
| GOV-07 conflict order | `sdlc.md` | No order; no one-change-set rule | CHANGE | W01 |
| GOV-08 low-risk approval reuse | `approval-and-safety.md:59-61`, `sdlc.md:109` | Text fits; tests are W07 | KEEP text | W07 tests |
| SUP-12 | `agent-execution.md:68-73`, `document-authoring.md:236-246` | Fits | KEEP | none |
| R147-20 result reuse | `quality.md:72-75` | No environment, guarantee or consumer in the equivalence; no pre-block versus post-observation sentence | CHANGE | W01; `qa.py` W05 |
| R147-07 three axes | `sdlc.md` | Not distinguished | ADD | W01 |
| CI-SCOPE | `quality.md`, `sdlc.md`, `git.md`, `work-lifecycle.md`, glossary; REQ-0003 FR-0017 and criterion 11; ADR-0048 | Hosted CI is metadata and style only, as FR-0017 and ADR-0048 require | Record the adopted target in `quality.md` and `TERM-CI`; contract change is one W06 change set | W01 target text; W06 |
| POLICY-ROLE | `sdlc.md`, `document-authoring.md` | Never says both profiles are one Policy role | CHANGE; form to W03 | W01, W03 |
| Integration "accepted" | `git.md` | Conflicts with Acceptance | CHANGE | W01 |
| Adoption "independent review" | `document-authoring.md` | Conflicts with the single-maintainer review | CHANGE | W01 |
| ADR approval row | `sdlc.md` | Uses ADR status as authoring approval | CHANGE | W01 |
| Lowercase must/should | `quality.md`, `git.md` | No RFC meaning in lowercase | KEEP | none |

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-GOVALIGN-001](../spec.md#success-criteria--verification-plan), [VAL-GOVALIGN-002](../spec.md#success-criteria--verification-plan) | Edit the W01 files the Spec names; `work-lifecycle.md` needs no W01 edit because its hosted-lane text is the W06 change set. | platform | in-progress | PASS | EVD-004, EVD-006 |
| WORK-002 | [VAL-GOVALIGN-003](../spec.md#success-criteria--verification-plan) | Record the handoffs and the exact-index QA. | platform | in-progress | PASS | EVD-005, EVD-006; exact-index QA and hooks run on the implementation commit |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-GOVALIGN-001](../spec.md#success-criteria--verification-plan), [VAL-GOVALIGN-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review rounds | Read-only code-reviewer that wrote none of the package; round 1 over spec.md `497c60ea…`, plan.md `622d518f…`; 2026-11-12 | PASS | Round 1 REJECT: one BLOCK (CI-SCOPE text contradicted REQ-0003 FR-0017, criterion 11 and accepted ADR-0048 with no owner for amending them) and six FIXes (conflict order beside the old rule and no protected-action clause; incomplete handoffs; approval text partly already present and GOV-03 missing; thin extension rule; no pre-block versus post-observation text; owners and ADR links). Resolved by keeping the hosted contract, stating CI-SCOPE as a target and handing the successor ADR, FR-0017 amendment and `ci.yml` to W06 as one change. | no | none |
| EVD-002 | [VAL-GOVALIGN-001](../spec.md#success-criteria--verification-plan), [VAL-GOVALIGN-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"d4f467d2835eef6572e3cef577d40960f7d094ee1c8a7aed2e50885a93eec0a8","plan_sha256":"f282a67828999ee799332bcbca3fdacb27541ab85e0c15b1c5553f4535829fd5"} | PASS | Same reviewer, round 2, 2026-11-12: both hashes matched; every round-1 finding resolved; verdict APPROVE with no BLOCK or FIX. Five optional NOTEs remain (scope sentence still lists `work-lifecycle.md`; W06 later edits `quality.md` again; the target sentence must say target, not runs; `guarantee` and `consumer` not glossary terms; `ci.yml` now read). The reviewer is independent of the author; this row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-GOVALIGN-001](../spec.md#success-criteria--verification-plan), [VAL-GOVALIGN-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0166 question naming spec.md d4f467d2 and plan.md f282a678 dated 2026-11-12 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0166","SPEC-0166-PLAN-0001"],"reviewed_spec_sha256":"d4f467d2835eef6572e3cef577d40960f7d094ee1c8a7aed2e50885a93eec0a8","reviewed_plan_sha256":"f282a67828999ee799332bcbca3fdacb27541ab85e0c15b1c5553f4535829fd5","validity":"confirmed","revocation":"none"} | PASS | No message UUID was supplied or invented. This receipt accepts no criterion and authorizes no push, PR or merge. | yes | none |
| EVD-004 | [VAL-GOVALIGN-001](../spec.md#success-criteria--verification-plan), [VAL-GOVALIGN-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Owner edits, phrase and anchor search, document checks | Working tree over `4300d7c6`: `document-authoring.md` 3.6.0, `sdlc.md` 3.5.0, `quality.md` 2.5.0, `git.md` 2.5.1, glossary 1.1.0; 2026-11-12 | PASS | Phrase search over `.agents`, `.claude`, `CLAUDE.md`, `AGENTS.md`: no hit for `checks branch metadata`, `calling an integration accepted`, `neither side is presumed correct`; no `independent review` in `document-authoring.md`. Anchor search: each of the seven anchors has one hit in its named owner; `one document role` also appears in the glossary `TERM-PROFILE` definition with another meaning (profile scope), not a Policy-role statement. 54 of 54 Policy Owner cells are relative links to existing files; `TERM-CI` reads "runs the hosted checks the quality policy selects" with the quality policy as owner. Strict registry (291 paths), Markdown profile, link/owner and lifecycle validators PASS; knowledge surface PASS (3 documents, 0 violations); agent governance PASS; `document` suite 313 tests OK; `agent-governance` suite 104 tests OK. | yes | none |
| EVD-005 | [VAL-GOVALIGN-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Handoff record | Spec Interfaces and the Handoffs table below | PASS | W03, W04, W05, W06 and W07 each have owner, interface and resume condition; none was started here. | yes | none |
| EVD-006 | [VAL-GOVALIGN-001](../spec.md#success-criteria--verification-plan), [VAL-GOVALIGN-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Semantic review: risk class and core-diff checklist | Diff of the five W01 files over `4300d7c6` | PASS | Risk class `medium` (policy change). Checklist: acceptance alignment holds (each Contracts item in its named owner); one writer per file (this Task); consistent with FR-0017 and ADR-0048, which the hosted target sentence names as governing; no check removed or weakened; no secret read or printed; recovery is reverting the implementation commit. No permission, trigger or protected action changed. Findings: none `BLOCK` or `FIX`; NOTE: the `quality.md` reuse key now names environment, guarantee and consumer while `scripts/qa.py` does not yet (W05). | yes | none |

### Handoffs

| Stage | Owner | Interface | Resume condition |
| --- | --- | --- | --- |
| W03 | Stage 99 registry and template author | Add `approved_by`, `approved_at`, `scope`, `effective_from`, `migration`, `rollback`, `consumer_version` and an `approved` stage to `shared_contract`; map `owner` and `extensions` (condition, owner, verification, review, removal); bind `governance/rule` and `operation/policy` to one Policy form | This change accepted |
| W04 | Lifecycle policy author | Status, acceptance, promotion and exit per role and per axis in `document-lifecycle.md` | W04 starts |
| W05 | Validator and test author | Derived-copy drift check; `shared_contract` binding tests; refusal of contradictory approval text; `scripts/qa.py` reuse key with environment, guarantee and consumer | W03 lands |
| W06 | Hosted CI owner | One change set: successor to ADR-0048, FR-0017 and criterion 11 amendment, `.github/workflows/ci.yml`, mirrored CI scripts and tests, hosted-lane text in `quality.md`, `sdlc.md`, `git.md` and `work-lifecycle.md` | W06 starts and the user accepts the successor ADR |
| W07 | Verification owner | Allow and deny tests for low-risk approval reuse | W07 starts |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-GOVALIGN-001](../spec.md#success-criteria--verification-plan) | pending | none | Owner edits and phrase search | platform |
| [VAL-GOVALIGN-002](../spec.md#success-criteria--verification-plan) | pending | none | Glossary links and knowledge checks | platform |
| [VAL-GOVALIGN-003](../spec.md#success-criteria--verification-plan) | pending | none | Handoffs and exact-index QA | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the six W01 files the Spec names (no edit planned in `work-lifecycle.md`), this package, `docs/03.specs/README.md`, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: registry, schema, templates, `scripts/`, `tests/`, `.github/`, `document-lifecycle.md`, accepted ADR bodies
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any push, PR or merge; `.secrets.baseline` digest entries are reviewed before their own commit
- **Static Validation**: strict document validators, knowledge and agent-governance validators, `document` and `agent-governance` suites, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit
- **Evidence Location**: this Task

## Verification Summary

WORK-001 and WORK-002 done; all checks in EVD-004 PASS; semantic review in EVD-006 has no `BLOCK` or `FIX`. Risk class `medium` (policy change). Criterion acceptance is pending the operator. Not run: live checks (no live surface). Rollback: revert the implementation commit. Residual risk: the W03, W05 and W06 targets are policy text without enforcement until those stages land. Next owner: the operator for acceptance, then W02 or W03 per the package order.
