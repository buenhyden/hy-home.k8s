---
title: "W03 Operations Policy Rule IDs"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0202-TSK-0001"
parent_ids: ["SPEC-0202-PLAN-0001"]
---

# Task: W03 Operations Policy Rule IDs

## Overview

This Task records Policy package 4 of handoff W03-H29 (W03-D42 to W03-D44, W03-D53, W03-D58, W03-D62): the amended coverage floor, and the definition tokens, the Rules table and the `adopted` state for the operations policies POL-0001, POL-0003, POL-0004 and POL-0005, with no prose reworded, for [SPEC-0202](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 and 2026-11-14 (Asia/Seoul) the user asked to continue the remaining W03 items and approved commit, push, PR and merge in those requests. The requests approve no Spec bytes or criterion.
- **Base:** set at commit time; the Spec and Plan facts were read on `main` `4bcda456` (after PR #254, SPEC-0188) and from the approved texts of SPEC-0194, SPEC-0199 and SPEC-0201, and are checked against `main` before delivery. The package needs SPEC-0194 implemented and merges after SPEC-0201.
- **Decisions reused:** SPEC-0161 W03-D27, W03-D42, W03-D43, W03-D44, W03-D53, W03-D58, W03-D65 and W03-H29.
- **Decision recorded with this package:** W03-D62 (POL-0007 and the gate retirement move to the following package; the W03-D58 rules and the SPEC-0199 contracts are reused unchanged; each nested item of POL-0003 and POL-0004 is one rule, 30 and 27 IDs, and the coverage floor accepts a label item whose every nested item carries a token; POL-0007 takes 45 IDs under a binding table in its own package; the Level is read by meaning and by the labels, each reading listed for review before a record flips; Evidence cites the control ID, then the runbook or guide named under `Enforcement`, then an existing check, otherwise the judging review; `Always` is one ASCII value); user answer of 2026-11-14, copied in exact words at commit time.
- **Binding unit table:** read under `Requirements` at `main` `4bcda456`. It is the binding reading under W03-D62, not a preliminary one: the IDs are issued in document order as listed, the nested items of POL-0003 and POL-0004 in the order they stand, and a label item carries no token. Control rows keep their control IDs and take no rule ID. If a policy at the implementation base no longer matches a row, the work stops and goes to the user before any ID is issued.

| Policy | H4 group | Label | Units | Rule IDs | IDs |
| --- | --- | --- | --- | --- | --- |
| POL-0001 | Control Register | none | 6 control rows | 0 | none |
| POL-0001 | Required | none | 10 top-level items | 10 | `GITOPS-R001` to `GITOPS-R010` |
| POL-0001 | Allowed | none | 3 top-level items | 3 | `GITOPS-R011` to `GITOPS-R013` |
| POL-0001 | Disallowed | none | 5 top-level items | 5 | `GITOPS-R014` to `GITOPS-R018` |
| POL-0003 | TLS / cert-manager | Required | 5 nested items | 5 | `MESH-R001` to `MESH-R005` |
| POL-0003 | TLS / cert-manager | Allowed | 2 nested items | 2 | `MESH-R006` to `MESH-R007` |
| POL-0003 | TLS / cert-manager | Disallowed | 2 nested items | 2 | `MESH-R008` to `MESH-R009` |
| POL-0003 | Istio / Service Mesh | Required | 4 nested items | 4 | `MESH-R010` to `MESH-R013` |
| POL-0003 | Istio / Service Mesh | Allowed | 1 nested item | 1 | `MESH-R014` |
| POL-0003 | Istio / Service Mesh | Disallowed | 4 nested items | 4 | `MESH-R015` to `MESH-R018` |
| POL-0003 | Kiali / Observability | Required | 7 nested items | 7 | `MESH-R019` to `MESH-R025` |
| POL-0003 | Kiali / Observability | Disallowed | 2 nested items | 2 | `MESH-R026` to `MESH-R027` |
| POL-0003 | CI Governance | none | 3 top-level items | 3 | `MESH-R028` to `MESH-R030` |
| POL-0004 | Argo Rollouts | Required | 7 nested items | 7 | `ROLLOUT-R001` to `ROLLOUT-R007` |
| POL-0004 | Argo Rollouts | Allowed | 3 nested items | 3 | `ROLLOUT-R008` to `ROLLOUT-R010` |
| POL-0004 | Argo Rollouts | Disallowed | 2 nested items | 2 | `ROLLOUT-R011` to `ROLLOUT-R012` |
| POL-0004 | Argo Notifications | Required | 4 nested items | 4 | `ROLLOUT-R013` to `ROLLOUT-R016` |
| POL-0004 | Argo Notifications | Allowed | 2 nested items | 2 | `ROLLOUT-R017` to `ROLLOUT-R018` |
| POL-0004 | Argo Notifications | Disallowed | 2 nested items | 2 | `ROLLOUT-R019` to `ROLLOUT-R020` |
| POL-0004 | Headlamp | Required | 4 nested items | 4 | `ROLLOUT-R021` to `ROLLOUT-R024` |
| POL-0004 | Headlamp | Allowed | 2 nested items | 2 | `ROLLOUT-R025` to `ROLLOUT-R026` |
| POL-0004 | Headlamp | Disallowed | 1 nested item | 1 | `ROLLOUT-R027` |
| POL-0005 | Control Register | none | 6 control rows | 0 | none |
| POL-0005 | Service Port Naming | none | whole group | 1 | `OBSERV-R001` |
| POL-0005 | In-Cluster Metric Collection | none | whole group | 1 | `OBSERV-R002` |
| POL-0005 | Logs, Rules, and Access | none | 5 top-level items | 5 | `OBSERV-R003` to `OBSERV-R007` |
| Total | | | 12 control rows; 26 top-level items; 54 nested items; 2 groups | 82 | 18 `GITOPS`, 30 `MESH`, 27 `ROLLOUT`, 7 `OBSERV` |

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-OPSRULE-001](../spec.md#criteria) | The amended coverage floor and its six tests; the sentence that states the floor, where one exists. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-OPSRULE-002](../spec.md#criteria) | Tokens, Rules table and the `adopted` state for each of the four policies, as the binding table lists them. | platform | ready | NOT_RUN | Pending |
| WORK-003 | [VAL-OPSRULE-003](../spec.md#criteria) | The map of each ID to its unit with its Level, Condition and Evidence, listed for review before each record flips; the stripped-body comparison; the anchor and slug checks; the lookup of every named control, artifact and check; the version steps. | platform | ready | NOT_RUN | Pending |
| WORK-004 | [VAL-OPSRULE-004](../spec.md#criteria) | W03-D62, the W03-H29 state cell and the ledger entry; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-OPSRULE-001](../spec.md#criteria) | WORK-001 | Independent semantic review | {"spec_sha256":"1dda77e250282d77c24337ab27560ac09fe3435b18db45df09f2b34c786631ce","plan_sha256":"c89e76b873f57b4f72ddab674c88948ddf420aba1d4e76d6ed0b23bdbee6561c"} | PASS | Independent reviewer, round 3 on 2026-11-14: the round-1 and round-2 FIX items on the coverage-floor amendment resolved (refusal only for an untokened parent; pure label equal to Required:, Allowed: or Disallowed:; six tests); the 82-ID binding table confirmed at 4bcda456; APPROVE over the bytes named here. This row records a review, not an approval. | yes | none |
| EVD-002 | [VAL-OPSRULE-001](../spec.md#criteria) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve bytes to the SPEC-0202 approval question naming spec.md 1dda77e2 and plan.md c89e76b8 dated 2026-11-14 Asia/Seoul","review_ref":"EVD-001","scope":["SPEC-0202","SPEC-0202-PLAN-0001"],"reviewed_spec_sha256":"1dda77e250282d77c24337ab27560ac09fe3435b18db45df09f2b34c786631ce","reviewed_plan_sha256":"c89e76b873f57b4f72ddab674c88948ddf420aba1d4e76d6ed0b23bdbee6561c","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-003 | [VAL-OPSRULE-001](../spec.md#criteria) | WORK-001 | Independent semantic review | {"spec_sha256":"4f23e12bd1b7204e30ffe9bfaa5b536b3c080afed41336e39516a747fa68a6eb","plan_sha256":"c89e76b873f57b4f72ddab674c88948ddf420aba1d4e76d6ed0b23bdbee6561c"} | PASS | Independent review on 2026-11-14 of the W03-D65 revision (conditional Rules table with four common columns and a registered Status extension per REQ:37, 310, 486, 742; Q-07 bound on permanence per REQ:143): APPROVE, with the reviewers' FIX and NIT items applied and confirmed over the bytes named here. This row records a review, not an approval. | yes | none |
| EVD-004 | [VAL-OPSRULE-001](../spec.md#criteria) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve all six to the policy package re-approval question naming spec.md 4f23e12b and plan.md c89e76b8 dated 2026-11-14 Asia/Seoul","review_ref":"EVD-003","scope":["SPEC-0202","SPEC-0202-PLAN-0001"],"reviewed_spec_sha256":"4f23e12bd1b7204e30ffe9bfaa5b536b3c080afed41336e39516a747fa68a6eb","reviewed_plan_sha256":"c89e76b873f57b4f72ddab674c88948ddf420aba1d4e76d6ed0b23bdbee6561c","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-018 | [VAL-OPSRULE-001](../spec.md#criteria) | WORK-001 | Independent semantic review | {"spec_sha256":"d73f83ec428727a2968707947fa531425350c5d2414a217d64e0469534ab9b22","plan_sha256":"1aedcaccb6474744f7d08b7f78dea1f1131c5fd459c8087391b596b4c8edc021"} | PASS | Mechanical form move of the approved Spec and Plan (4f23e12b, c89e76b8) to the SPEC-0200 forms by its heading map, version 1.0.0 to 2.0.0 and updated 2026-11-15 (W03-D59 Q4, W03-D84). The sorted non-heading lines of the old and new files are equal except the listed added or changed lines: in the Spec the criteria table header (Criterion, Acceptance evidence to Criterion ID, Expected Result), five label lines (Contracts, Data modeling and storage strategy, Interfaces and data structures, Edge cases and error handling, Failure modes and fallback or human escalation) and two References pointer lines; in the Plan three label lines (Goals and in-scope, Non-goals and out-of-scope, Completion criteria), the Dependencies, Change and Rollback, Escalation and Durable Meaning pointer lines, the Work Breakdown criterion anchors repointed to spec.md#criteria, and the Promotion table moved to the four-column form with one Acceptance cell added per row. No sentence was reworded. Task links to the Spec criteria are repointed to #criteria. This row records a mechanical check, not an approval. | yes | none |
| EVD-019 | [VAL-OPSRULE-001](../spec.md#criteria) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Mechanical move + check, blanket OK (Recommended) to the question on moving each remaining package's approved Spec and Plan to the SPEC-0200 forms with a major raise to 2.0.0 and a mechanical check, dated 2026-11-15 Asia/Seoul","review_ref":"EVD-018","scope":["SPEC-0202","SPEC-0202-PLAN-0001"],"reviewed_spec_sha256":"d73f83ec428727a2968707947fa531425350c5d2414a217d64e0469534ab9b22","reviewed_plan_sha256":"1aedcaccb6474744f7d08b7f78dea1f1131c5fd459c8087391b596b4c8edc021","validity":"confirmed","revocation":"none"} | PASS | Approves the form move of the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-OPSRULE-001](../spec.md#criteria) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-OPSRULE-002](../spec.md#criteria) | pending | none | Implement WORK-002 and record PASS evidence | platform |
| [VAL-OPSRULE-003](../spec.md#criteria) | pending | none | Implement WORK-003 and record PASS evidence | platform |
| [VAL-OPSRULE-004](../spec.md#criteria) | pending | none | Implement WORK-004 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the four policies the Spec names under `docs/05.operations/policies/` (definition tokens, one Rules table, frontmatter `version` and `updated`); the `state` values of their four records of `policy_rule_ids` in `docs/99.templates/registry.json`; `scripts/validate-markdown-profiles.py` for the coverage floor of `POLICY-RULE-COVERAGE` only; `tests/test_policy_rule_ids.py`; the sentence that states the coverage floor in `.agents/governance/document-authoring.md`, `docs/99.templates/README.md` and the two Policy templates, where one exists; this package, `docs/03.specs/README.md`, the W03-D62 row, an evidence row, the W03-H29 state cell and the frontmatter `version` and `updated` of the SPEC-0161 Task, the W03-H29 entry of `docs/03.specs/work-residue-ledger.json`, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: POL-0007, the governance policies, any existing sentence, heading or line break of an operations policy, the control registers and control IDs, the `Lifecycle Traceability` tables, any runbook, guide or manifest, the `state` field, `POLICY-RULE-ADOPTION` and `minimum_rows`, any other rule, the schema or other registry content of SPEC-0194, the shared Policy form, the glossary, any recorded Task row, EVD row, decision or handoff rewrite, `.github/`, the external task package under `_workspace/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; the map of each policy before its record flips; any unit whose Level, Condition or Evidence cannot be read without adding meaning; any change beyond the Spec's named scope, which stops the work and goes to the user; push, PR and merge are approved by the user's requests in Inputs
- **Static Validation**: strict document validators, the `document`, `document-lifecycle`, `agent-governance`, `validation-routing` and `tooling` suites, `python3 scripts/validate-document-contract-registry.py --root .`, `python3 scripts/validate-affected-surfaces.py --root .`, `ruff check scripts tests`, markdownlint over the edited Markdown, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface is changed, and no cluster evidence is claimed for any Evidence cell
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert an adoption commit, or set one policy's record back to `pending` with its body; revert the floor amendment commit once POL-0003 and POL-0004 are back to `pending`; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan drafted with the W03-D62 answers written in; no review, approval or implementation is recorded yet.
