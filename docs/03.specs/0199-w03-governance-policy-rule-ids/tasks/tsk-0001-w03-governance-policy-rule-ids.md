---
title: "W03 Governance Policy Rule IDs"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0199-TSK-0001"
parent_ids: ["SPEC-0199-PLAN-0001"]
---

# Task: W03 Governance Policy Rule IDs

## Overview

This Task records Policy package 3 of handoff W03-H29 (W03-D42 to W03-D44, W03-D53): the definition tokens, the Rules table and the `adopted` state for nine governance policies, with no prose reworded, for [SPEC-0199](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 and 2026-11-14 (Asia/Seoul) the user asked to continue the remaining W03 items and approved commit, push, PR and merge in those requests. The requests approve no Spec bytes or criterion.
- **Base:** set at commit time; the Spec and Plan facts were read on `main` `8daf643f` (after PR #253, SPEC-0187) and are checked against `main` before delivery. The package needs SPEC-0194 implemented and merges after SPEC-0198.
- **Decisions reused:** SPEC-0161 W03-D27, W03-D42, W03-D43, W03-D44, W03-D53, W03-D65 and W03-H29.
- **Decision to record with this package:** W03-D58 (the split that gives `quality.md` its own package, the unit rule for H4 groups and for paragraphs outside every unit, the Level rule and the Condition and Evidence rule); the user's exact words are copied at commit time and the number is re-read then.
- **Rule-unit inventory:** read under `Requirements` at `main` `8daf643f`; the pre-approval review confirms it and the implementation records the final map of each ID to its unit. The lower figure counts items, rows, groups without a list or table and one group for the paragraphs outside a unit; the upper figure adds a group token for every mixed group and a group for every such paragraph.

| Policy | Code | Top-level items | Table rows | H4 groups without list or table | Mixed H4 groups | Paragraphs outside a unit | Rule IDs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `agent-execution.md` | `EXEC` | 11 | 0 | 1 | 0 | 0 | 12 |
| `approval-and-safety.md` | `SAFE` | 13 | 6 | 1 | 1 | 0 | 20 to 21 |
| `context-and-memory.md` | `CTX` | 17 | 0 | 2 | 1 | 0 | 19 to 20 |
| `document-authoring.md` | `AUTHOR` | 14 | 0 | 0 | 0 | 9 | 15 to 23 |
| `document-lifecycle.md` | `DOCLIFE` | 21 | 0 | 0 | 0 | 0 | 21 |
| `formatting-and-linting.md` | `FMT` | 12 | 0 | 0 | 0 | 0 | 12 |
| `git.md` | `GIT` | 8 | 0 | 3 | 0 | 0 | 11 |
| `model-selection.md` | `MODEL` | 4 | 0 | 3 | 0 | 0 | 7 |
| `sdlc.md` | `SDLC` | 10 | 22 | 1 | 3 | 1 | 34 to 37 |
| Nine policies of this package | | 110 | 28 | 11 | 5 | 10 | 151 to 164 |
| `quality.md` (next package) | `QUAL` | 33 | 7 | 5 | 6 | 0 | 45 to 51 |

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-GOVRULE-001](../spec.md#success-criteria--verification-plan) | Tokens, Rules table, added headings and the `adopted` state for each of the nine policies. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-GOVRULE-002](../spec.md#success-criteria--verification-plan) | The final map of each ID to its unit with its Level, Condition and Evidence reading; the stripped-body comparison; the version steps. | platform | ready | NOT_RUN | Pending |
| WORK-003 | [VAL-GOVRULE-003](../spec.md#success-criteria--verification-plan) | W03-D58, the W03-H29 state cell and the ledger entry; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-GOVRULE-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"2ed29e8e2358ae50c0ac00ddbcf248b3210074fa44687e245a7cc9e99deeaa6f","plan_sha256":"cd9ed1c09d1cdd9917c2e08cce1fb24f9ec1820d48c36a0175020d1de7918853"} | PASS | Independent reviewer on 2026-11-14: APPROVE with three NITs (anchor counts 34 of 42 plus 17 capability_tier_ref values, unique H4 slugs, exact stripped-body removal), all applied over the bytes named here; no BLOCK and no FIX. This row records a review, not an approval. | yes | none |
| EVD-002 | [VAL-GOVRULE-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve bytes to the SPEC-0199 approval question naming spec.md 2ed29e8e and plan.md cd9ed1c0 dated 2026-11-14 Asia/Seoul","review_ref":"EVD-001","scope":["SPEC-0199","SPEC-0199-PLAN-0001"],"reviewed_spec_sha256":"2ed29e8e2358ae50c0ac00ddbcf248b3210074fa44687e245a7cc9e99deeaa6f","reviewed_plan_sha256":"cd9ed1c09d1cdd9917c2e08cce1fb24f9ec1820d48c36a0175020d1de7918853","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-003 | [VAL-GOVRULE-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"2b7ffcb4bdd8f853f89eb9be11119edf7cf728afcd3bc98a2c09e09f2b320179","plan_sha256":"cd9ed1c09d1cdd9917c2e08cce1fb24f9ec1820d48c36a0175020d1de7918853"} | PASS | Independent review on 2026-11-14 of the W03-D65 revision (conditional Rules table with four common columns and a registered Status extension per REQ:37, 310, 486, 742; Q-07 bound on permanence per REQ:143): APPROVE, with the reviewers' FIX and NIT items applied and confirmed over the bytes named here. This row records a review, not an approval. | yes | none |
| EVD-004 | [VAL-GOVRULE-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve all six to the policy package re-approval question naming spec.md 2b7ffcb4 and plan.md cd9ed1c0 dated 2026-11-14 Asia/Seoul","review_ref":"EVD-003","scope":["SPEC-0199","SPEC-0199-PLAN-0001"],"reviewed_spec_sha256":"2b7ffcb4bdd8f853f89eb9be11119edf7cf728afcd3bc98a2c09e09f2b320179","reviewed_plan_sha256":"cd9ed1c09d1cdd9917c2e08cce1fb24f9ec1820d48c36a0175020d1de7918853","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-GOVRULE-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-GOVRULE-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |
| [VAL-GOVRULE-003](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-003 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the nine policies the Spec names under `.agents/governance/` (definition tokens, one Rules table, headings over ruled paragraphs outside a unit, frontmatter `version` and `updated`), the nine `state` values of `policy_rule_ids` in `docs/99.templates/registry.json`, `tests/test_policy_rule_ids.py` where it pins those states, this package, `docs/03.specs/README.md`, the W03-D58 row, an evidence row, the W03-H29 state cell and the frontmatter `version` and `updated` of the SPEC-0161 Task, the W03-H29 entry of `docs/03.specs/work-residue-ledger.json`, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: `.agents/governance/quality.md`, the operations policies, any existing sentence, heading or line break of a policy, any validator, schema, template, form, profile or other registry content, the glossary, any recorded Task row, EVD row, decision or handoff rewrite, `.github/workflows/`, the external task package under `_workspace/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any unit whose Level, Condition or Evidence cannot be read without adding meaning; any change beyond the Spec's named scope, which stops the work and goes to the user; push, PR and merge are approved by the user's requests in Inputs
- **Static Validation**: strict document validators, the `document`, `document-lifecycle`, `agent-governance`, `validation-routing` and `tooling` suites, `python3 scripts/validate-document-contract-registry.py --root .`, markdownlint over the edited Markdown, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit, or set one policy's record back to `pending` with its body; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan drafted; no review, approval or implementation is recorded yet.
