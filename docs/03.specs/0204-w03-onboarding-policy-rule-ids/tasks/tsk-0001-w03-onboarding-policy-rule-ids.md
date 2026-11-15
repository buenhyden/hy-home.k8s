---
title: "W03 Onboarding Policy Rule IDs"
version: "0.2.0"
type: "sdlc/task"
status: "ready"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0204-TSK-0001"
parent_ids: ["SPEC-0204-PLAN-0001"]
---

# Task: W03 Onboarding Policy Rule IDs

## Scope

### Objective and Parent

This Task records Policy package 4b of handoff W03-H29 (W03-D42 to W03-D44, W03-D53, W03-D58, W03-D62): the definition tokens, the Rules table and the `adopted` state for the app GitOps onboarding policy POL-0007, with no prose reworded, and the retirement of the adoption gate, for [SPEC-0204](../spec.md) under its [Plan](../plan.md).

### Inputs and Authority

- **Request:** on 2026-11-13 and 2026-11-14 (Asia/Seoul) the user asked to continue the remaining W03 items and approved commit, push, PR and merge in those requests. The requests approve no Spec bytes or criterion.
- **Base:** set at commit time; the Spec and Plan facts were read on `main` `4bcda456` (after PR #254, SPEC-0188) and from the approved texts of SPEC-0194, SPEC-0199, SPEC-0201 and SPEC-0202, and are checked against `main` before delivery. The package needs SPEC-0194 implemented and merges after SPEC-0202.
- **Decisions reused:** SPEC-0161 W03-D27, W03-D42, W03-D43, W03-D44, W03-D53, W03-D58, W03-D62, W03-D65 and W03-H29. W03-D62 is recorded by the SPEC-0202 package commit; this package records no new decision.
- **Binding unit table:** read under `Requirements` at `main` `4bcda456`. It is the binding reading under W03-D62, not a preliminary one: the IDs are issued in document order as listed, a group token before the members of its group. The opening paragraph, the four chapter headings and the two items labelled `Required evidence` take no ID. The chapter headings hold no rule text, so none is an H4 rule group as SPEC-0194 reads the term. The opening paragraph is worded as an imperative summary, so the review list for the user names it as a no-ID reading before the flip. If the policy at the implementation base no longer matches a row, the work stops and goes to the user before any ID is issued.

| H4 group | Kind | Units | Group token | Rule IDs | IDs |
| --- | --- | --- | --- | --- | --- |
| Opening paragraph (no heading) | introduction | 1 paragraph | no | 0 | none |
| `1. 배포 리소스 정책` | chapter heading | none | no | 0 | none |
| `1-1. Rollout 필수` | prose | 3 paragraphs | whole group | 1 | `ONBOARD-R001` |
| `1-2. AnalysisTemplate 필수` | mixed | 1 paragraph; 3 items; 1 `Required evidence` item | yes | 4 | `ONBOARD-R002` to `ONBOARD-R005` |
| `1-3. 이미지 태그` | table | 3 rows | no | 3 | `ONBOARD-R006` to `ONBOARD-R008` |
| `2. 네트워킹 정책` | chapter heading | none | no | 0 | none |
| `2-1. Istio 포트 명명 규칙` | prose | 2 paragraphs | whole group | 1 | `ONBOARD-R009` |
| `2-2. Ingress 설정` | prose | 1 paragraph | whole group | 1 | `ONBOARD-R010` |
| `2-3. k8s router 경로` | mixed | 1 paragraph; 2 items; 1 `Required evidence` item | yes | 3 | `ONBOARD-R011` to `ONBOARD-R013` |
| `3. 보안 정책` | chapter heading | none | no | 0 | none |
| `3-1. Istio mTLS` | mixed | 1 paragraph; 3 items | yes | 4 | `ONBOARD-R014` to `ONBOARD-R017` |
| `3-2. NetworkPolicy` | mixed | 2 paragraphs; 5 items | yes | 6 | `ONBOARD-R018` to `ONBOARD-R023` |
| `3-3. 시크릿 관리` | table | 5 rows | no | 5 | `ONBOARD-R024` to `ONBOARD-R028` |
| `4. GitOps 워크플로우 정책` | chapter heading | none | no | 0 | none |
| `4-1. 파일 배치 규칙` | prose | 1 paragraph | whole group | 1 | `ONBOARD-R029` |
| `4-2. 네이밍 규칙` | table | 5 rows | no | 5 | `ONBOARD-R030` to `ONBOARD-R034` |
| `4-3. 금지 사항` | list | 4 items | no | 4 | `ONBOARD-R035` to `ONBOARD-R038` |
| `5. 온보딩 통제 체크리스트` | mixed | 1 paragraph; 6 rows | yes | 7 | `ONBOARD-R039` to `ONBOARD-R045` |
| Total | 17 headings | 17 items; 19 rows; 4 whole groups; 5 group tokens | 5 of 5 mixed | 45 | `ONBOARD-R001` to `ONBOARD-R045` |

- **Allowed Paths**: `docs/05.operations/policies/0007-app-gitops-onboarding-policy.md` (definition tokens, one Rules table, frontmatter `version` and `updated`); in `docs/99.templates/registry.json` the `state` values of `policy_rule_ids`; the `state` property in `docs/99.templates/contracts/document-profile.schema.json`; `scripts/document_contracts.py` and `scripts/validate-markdown-profiles.py` for the gate only; `tests/test_policy_rule_ids.py` and `tests/test_document_generator.py` where they test the gate or pin states; the sentences that name the state or the gate in `.agents/governance/document-authoring.md`, `docs/99.templates/README.md` and the two Policy templates; this package, `docs/03.specs/README.md`, an evidence row, the W03-H29 state cell and the frontmatter `version` and `updated` of the SPEC-0161 Task, the W03-H29 entry of `docs/03.specs/work-residue-ledger.json`, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: the fourteen policies adopted earlier, any existing sentence, heading, table padding or line break of the onboarding policy, its `Lifecycle Traceability` table, the runbook, the sample app and the manifests it names, the coverage floor and every other rule of SPEC-0194, the `minimum_rows` of the Rules table and `rules_table`, the shared Policy form, any other profile, lifecycle domain or frontmatter key, the glossary, any recorded Task row, EVD row, decision or handoff rewrite, `.github/`, the external task package under `_workspace/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; the map of the policy before its record flips; any unit whose Level, Condition or Evidence cannot be read without adding meaning; any change beyond the Spec's named scope, which stops the work and goes to the user; push, PR and merge are approved by the user's requests in Inputs
- **Static Validation**: strict document validators, the `document`, `document-lifecycle`, `agent-governance`, `validation-routing` and `tooling` suites, `python3 scripts/validate-document-contract-registry.py --root .`, `python3 scripts/validate-affected-surfaces.py --root .`, `ruff check scripts tests`, markdownlint over the edited Markdown, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface is changed, and no cluster evidence is claimed for any Evidence cell
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the final source commit to restore the gate; revert the adoption commit, which sets the record back to `pending` with the body; before that, delete the package commit
- **Evidence Location**: this Task

## Execution Log

### Work Performed

The work of this Task is recorded in the rows of [Lifecycle Traceability](#lifecycle-traceability) below and in the evidence rows under Verification Evidence.

### Blockers and Decisions

No separate blocker or decision list is kept here; a blocker and its resume condition are recorded in the Result and Evidence cells of the work rows, and each decision in the evidence rows and tables under Verification Evidence.

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-ONBRULE-001](../spec.md#criteria) | Tokens, the Rules table and the `adopted` state for the policy, as the binding table lists them. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-ONBRULE-002](../spec.md#criteria) | The map of each ID to its unit with its Level, Condition and Evidence, listed for review before the record flips with the opening paragraph as a no-ID reading; the stripped-body comparison; the anchor and slug checks; the lookup of every named artifact and check; the version step. | platform | ready | NOT_RUN | Pending |
| WORK-003 | [VAL-ONBRULE-003](../spec.md#criteria) | The gate retirement in the final source commit: `state`, `POLICY-RULE-ADOPTION` and their tests removed, the sentences that name the gate, the three refusal tests and the acceptance of a policy without normative rules. | platform | ready | NOT_RUN | Pending |
| WORK-004 | [VAL-ONBRULE-004](../spec.md#criteria) | The W03-H29 state cell and the ledger entry; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Verification Evidence

### Results

| Evidence ID | Consumer | Work Unit | Command | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-ONBRULE-001](../spec.md#criteria) | WORK-001 | Independent semantic review | {"spec_sha256":"6d8423817ef8619c876a66b27973e3b579aafefe59c919a183f6b9c6e18b9139","plan_sha256":"6016bf614bca5e7f7ff21db8a9959cc8cc24509f5f40f7677a3937ff877b481c"} | PASS | Independent reviewer, round 2 on 2026-11-14: both round-1 NITs resolved (opening paragraph listed as a no-ID reading; empty chapter headings not H4 rule groups by reading); the 45-ID table, the gate-retirement order and the decision-row handling confirmed at 4bcda456; APPROVE over the bytes named here. This row records a review, not an approval. | yes | none |
| EVD-002 | [VAL-ONBRULE-001](../spec.md#criteria) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve bytes to the SPEC-0204 approval question naming spec.md 6d842381 and plan.md 6016bf61 dated 2026-11-14 Asia/Seoul","review_ref":"EVD-001","scope":["SPEC-0204","SPEC-0204-PLAN-0001"],"reviewed_spec_sha256":"6d8423817ef8619c876a66b27973e3b579aafefe59c919a183f6b9c6e18b9139","reviewed_plan_sha256":"6016bf614bca5e7f7ff21db8a9959cc8cc24509f5f40f7677a3937ff877b481c","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-003 | [VAL-ONBRULE-001](../spec.md#criteria) | WORK-001 | Independent semantic review | {"spec_sha256":"68df117d0d95f9469fb2af9db01022c842402f5524b7ec195e1dd8f8a32770e7","plan_sha256":"57cc868ddf8a4b6b00a50d1657f8bf432486f2173bdf4969ea7bc911fe1950c5"} | PASS | Independent review on 2026-11-14 of the W03-D65 revision (conditional Rules table with four common columns and a registered Status extension per REQ:37, 310, 486, 742; Q-07 bound on permanence per REQ:143): APPROVE, with the reviewers' FIX and NIT items applied and confirmed over the bytes named here. This row records a review, not an approval. | yes | none |
| EVD-004 | [VAL-ONBRULE-001](../spec.md#criteria) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve all six to the policy package re-approval question naming spec.md 68df117d and plan.md 57cc868d dated 2026-11-14 Asia/Seoul","review_ref":"EVD-003","scope":["SPEC-0204","SPEC-0204-PLAN-0001"],"reviewed_spec_sha256":"68df117d0d95f9469fb2af9db01022c842402f5524b7ec195e1dd8f8a32770e7","reviewed_plan_sha256":"57cc868ddf8a4b6b00a50d1657f8bf432486f2173bdf4969ea7bc911fe1950c5","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-013 | [VAL-ONBRULE-001](../spec.md#criteria) | WORK-001 | Independent semantic review | {"spec_sha256":"c0e722db427615bd87bdd5b2f2c2501783b934e593205b553a99e1f67d186fb4","plan_sha256":"b22019e6cb4d837152014d79972d68e18f930a4c5c659f6f8fbb55e162db6936"} | PASS | Mechanical form move of the approved Spec and Plan (68df117d, 57cc868d) to the SPEC-0200 forms by its heading map, version 1.0.0 to 2.0.0 and updated 2026-11-15 (W03-D84). The sorted non-heading lines of the old and new files are equal except the listed added or changed lines: in the Spec the criteria table header (Criterion, Acceptance evidence to Criterion ID, Expected Result), five label lines (Contracts, Data modeling and storage strategy, Interfaces and data structures, Edge cases and error handling, Failure modes and fallback or human escalation) and two References pointer lines; in the Plan three label lines (Goals and in-scope, Non-goals and out-of-scope, Completion criteria), the Dependencies, Change and Rollback, Escalation and Durable Meaning pointer lines, the Work Breakdown criterion anchors repointed to spec.md#criteria, and the Promotion table moved to the four-column form with one Acceptance cell added per row. No sentence was reworded. Task links to the Spec criteria are repointed to #criteria. This row records a mechanical check, not an approval. | yes | none |
| EVD-014 | [VAL-ONBRULE-001](../spec.md#criteria) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Mechanical move + check, blanket OK (Recommended) to the question on moving each remaining package's approved Spec and Plan to the SPEC-0200 forms with a major raise to 2.0.0 and a mechanical check, dated 2026-11-15 Asia/Seoul (W03-D84)","review_ref":"EVD-013","scope":["SPEC-0204","SPEC-0204-PLAN-0001"],"reviewed_spec_sha256":"c0e722db427615bd87bdd5b2f2c2501783b934e593205b553a99e1f67d186fb4","reviewed_plan_sha256":"b22019e6cb4d837152014d79972d68e18f930a4c5c659f6f8fbb55e162db6936","validity":"confirmed","revocation":"none"} | PASS | Approves the form move of the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-018 | [VAL-ONBRULE-001](../spec.md#criteria) | WORK-001 | Move of this Task to the SPEC-0203 Task form | {"task_before":"file eb2a3ee971a741be, 101 lines, version 0.1.1","heading_map":"SPEC-0203"} | PASS | Form-only move by the SPEC-0203 heading map (W03-D01, W03-D50) with the converter move_task.py of SPEC-0203: the old H2 removed, every body under its form H3 (Overview, Inputs, Approval and Safety Boundaries under Scope; Task Table under Execution Log; Task Evidence under Verification Evidence; Criterion Acceptance under Acceptance Decision; Verification Summary under Handoff), and five pointer lines added (Work Performed, Blockers and Decisions, Resolution Links, Remaining Conditions, Promotion Receipt). Every data row of the four tables is byte-identical and in the same order (each table's data-row hash equal before and after); only the evidence header line changed (Evidence, Criteria, Check to Evidence ID, Consumer, Command). Links to the Spec criteria stay `#criteria`; the frontmatter takes `status` ready, equal to the four WORK rows, and version 0.2.0. No evidence row was rewritten. | yes | none |

### Resolution Links

The Resolves column of the evidence table under Results names the earlier evidence row that each PASS row closes.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-ONBRULE-001](../spec.md#criteria) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-ONBRULE-002](../spec.md#criteria) | pending | none | Implement WORK-002 and record PASS evidence | platform |
| [VAL-ONBRULE-003](../spec.md#criteria) | pending | none | Implement WORK-003 and record PASS evidence | platform |
| [VAL-ONBRULE-004](../spec.md#criteria) | pending | none | Implement WORK-004 and record PASS evidence | platform |

### Remaining Conditions

No separate remaining-condition list is kept here; the Disposition and Current owner columns of the criterion decisions state what remains and who owns it.

## Handoff

### Promotion Receipt

No separate promotion receipt is kept here; the receipt of each Plan promotion row, where the Plan has one, is recorded in the evidence rows under Results.

### Next Owner

Spec and Plan drafted with the W03-D62 answers written in; no review, approval or implementation is recorded yet.
