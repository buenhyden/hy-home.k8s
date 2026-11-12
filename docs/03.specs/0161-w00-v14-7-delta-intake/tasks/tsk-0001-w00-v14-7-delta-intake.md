---
title: "W00 v14.7 Delta Intake"
version: "0.1.9"
type: "sdlc/task"
status: "completed"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0161-TSK-0001"
parent_ids: ["SPEC-0161-PLAN-0001"]
---

# Task: W00 v14.7 Delta Intake

## Overview

This Task records the W00 v14.7 delta tables for [SPEC-0161](../spec.md) under its [Plan](../plan.md). EVD-001 to EVD-006, EVD-010 and EVD-011 were observed before approval and are marked not required. The user approved the Spec and Plan on 2026-11-12 (EVD-013) and confirmed the exact reviewed bytes (EVD-015, EVD-016).

## Inputs

- **Request:** on 2026-11-12 (Asia/Seoul) the user pasted the v14.7 W00 prompt (`TASK-hy-home-k8s-W00.md`) and named the package directory `_workspace/workspace_execution_tasks/{dependencies, reports, tools}`. The request does not approve this Spec or Plan, accept a criterion, or authorize a commit, push or merge.
- **Workspace:** WORKSPACE_ROOT is the repository root; PACKAGE_ROOT `_workspace/workspace_execution_tasks/`, git-ignored by `.gitignore` line 74. Base `main` at `4a47cb40`, clean worktree and index, no open pull request; branch `claude/w00-v14-7-intake`.
- **Inputs (SHA-256):** W00 prompt `65d1cc62db9e2aae2476138d4285d4138a65202309bb4e6167b694758abbd1e7`; `INPUT-REPORT-ORIGINAL.txt` `dc348e7fc67f77ab8667cc4b1eecb50dbac2857d30617eff1246dd23d8748d23` (same as SPEC-0154); `REQUIREMENTS.json` `4c9da241ba185310048f3231815c04ed42dc7ce54c44e201f97e469f5945084b`; `PROFILE-REQUIREMENTS.json` `079f07c13b7c54391366185d0fd0ce543ec81c4877a4fbef9df0a82790ed2e75` (same as SPEC-0154); `REVISION-v14_7.json` `67c42631cf48f3fc4e7c84329c0eb87dfb7775fb000a7381696c931161541463`; `REQUEST-AMENDMENTS-v14_5.json` `02342b6b15d12de00e7880c8a161a3e418acd12324e3b8330eb66594adc90a27`; `COMMON-SECTION-CONTRACT.json` `4f79183d59c34ee87d1cab35c5ffc86eb7012f5df1db4dc4b91a8fd412e8c618`; `STAGE-QA-MATRIX.json` `12d8962c96c769cd3bbc12bcc2e9d29b31d4e60e9a48190c2d1ad6934030e873`; `QA-CHANGE-PROTOCOL.md` `106ee35cba6b2ea0313168541cce11f4b73573125b261be296f854d295f8826d`; `REPOSITORY-VOCABULARY.json` `b03ae3c00a4228de90d90b48c9a7af4b716492651d83b6deab128d9e3bc92fce`; `TEMPLATE-DEFINITION-CONTRACT.md` `ff7e35b8b75406c9bedb603f8fb4d0449401564b3eae79138b9f9b222c61eb10`; `OPEN-01-14.json` `4dde48c427323cd6a1cdef9280fd281f1bab019c07ea5fd947728639aa6b8677`.
- **Upstream:** completed SPEC-0154 to SPEC-0160, recoverable from the REQ-0003 Archived Lineage.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan), [VAL-DELTA-002](../spec.md#success-criteria--verification-plan) | Record the delta tables, check completeness, obtain independent review. | platform | frontmatter | PASS | Required checks pass: EVD-014 (completeness, resolves EVD-007), EVD-012 and EVD-015 (independent review, EVD-012 resolves EVD-008), EVD-017 (exact-index QA, resolves EVD-009). The user accepted both criteria on 2026-11-12. |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval edition comparison | Package v14.7 against the v14.1, v14.4, v14.5 and v14.6 history archives; prompt diff against v14.6; workspace HEAD `4a47cb40`; 2026-11-12 | PASS | Edition Delta table below. The exact v14.2 `REQUIREMENTS.json` (SPEC-0154 input, prefix `8af753f1`) is not in any history archive; v14.1 is the base. Same 106 IDs since v14.1; 16 rows changed only `implementation` or `verification` text (18 field changes). | no | none |
| EVD-002 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval requirement-change links | `REVISION-v14_7.json`, `REQUEST-AMENDMENTS-v14_5.json`, the 16 changed rows, REQ-0003 Scope and Non-goals, and repository searches at `4a47cb40`; 2026-11-12 | PASS | Requirement Changes table below: 50 rows (16 changed requirements, 12 R45, 20 R147, RS-09, CI-SCOPE). | no | none |
| EVD-003 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval pull-request table | `gh pr list --state all --limit 10` metadata at HEAD `4a47cb40`; 2026-11-12 | PASS | Related Pull Requests table below. Only metadata was read; no diff, check run or review was re-read. | no | none |
| EVD-004 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval document-form survey | Read-only agent over `COMMON-SECTION-CONTRACT`, `TEMPLATE-DEFINITION-CONTRACT`, `REPOSITORY-VOCABULARY`, `docs/99.templates/registry.json`, 18 templates, `scripts/document_contracts.py`, `scripts/validate-markdown-profiles.py`; HEAD `4a47cb40`; 2026-11-12 | PASS | Document Form Handoff table below. No file changed. | no | none |
| EVD-005 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval stage-QA survey | Read-only agent over `STAGE-QA-MATRIX`, `QA-CHANGE-PROTOCOL`, `.pre-commit-config.yaml`, `scripts/githooks/`, `scripts/qa.py`, `.github/workflows/ci.yml`, `.github/rulesets/main-protection.md`, `.claude/settings.json`, parts of `quality.md` and `git.md`; HEAD `4a47cb40`; 2026-11-12 | PASS | Stage QA Handoff table below. No hook, QA lane or network call was run. | no | none |
| EVD-006 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval OPEN dispositions and read denominator | `OPEN-01-14.json`, SPEC-0158 OPEN table at `6a519871`, the two surveys, `git ls-files` counts at `4a47cb40` | PASS | OPEN Dispositions and Read Denominator tables below. | no | none |
| EVD-007 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Completeness check under approved parents | The tables in this Task plus a negative copy | NOT_RUN | Pending Spec and Plan approval. | yes | none |
| EVD-008 | [VAL-DELTA-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent read-only semantic review | Change links, handoff writers and OPEN dispositions | NOT_RUN | Pending; a reviewer that produced none of the tables. | yes | none |
| EVD-009 | [VAL-DELTA-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Strict document checks and exact-index QA | Strict document validators, the staged lifecycle check and the active commit hooks on the exact index | NOT_RUN | Pending an authorized commit. | yes | none |
| EVD-010 | [VAL-DELTA-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval independent review, round 1 | A read-only code-reviewer that produced no table, over the staged package at HEAD `4a47cb40`; 2026-11-12 | FAIL | Two BLOCKs: OPEN-05 and OPEN-06 verdicts weaker than SPEC-0158 Review Corrections; files with two primary writers and rows without paths. Seven FIXes: OPEN-09 and OPEN-13 overstated, Root README Getting Started, R45-07 mixed state, `.secrets.baseline` scope, README status sentence, REQ-0003 sentence at exit. | no | none |
| EVD-011 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval verification of unverified survey items | Read-only agent over the named tests, `scripts/validate-document-lifecycle.py` 660-889, Stage 90 profiles and validators, generator search, README navigation, `.git/hooks/pre-commit` and `scripts/githooks/chained-hook.sh`; `gh api` branch protection, check runs and repository merge settings, read only, 2026-11-11T23:46Z; direct fetch of the LambdaDB article and the agency-agents and SillyMemory licences | PASS | Corrections from EVD-010 applied; OPEN-05 and OPEN-13 closed by evidence, OPEN-09 confirmed, PUSH-DURING and MERGE-BEFORE observed, PROMOTION and DOC-S90 gaps and the missing generator recorded. Local environment: `chained-hook.sh` runs `.git/hooks/pre-commit`, whose interpreter `/tmp/hyhome-r10-validation` is absent, so it falls back to a `pre-commit` without `jsonschema`; QA uses a scratch venv built from `.github/requirements/ci-validation.txt`. | no | none |
| EVD-012 | [VAL-DELTA-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent read-only semantic review | Same reviewer as EVD-010 over Task SHA-256 `66a730d289e68179c7cec6f84a023e57369fd07504a1b674804f3f324f09ea09`, Spec `8acb1507…`, Plan `5fe718c6…`; it re-ran the `gh api` protection, settings and check-run reads; 2026-11-12 | PASS | No BLOCK. Two FIXes (R147-07 and R147-20 writer wording, MERGE-BEFORE wording) and two NOTEs applied before approval; no other content changed. | yes | EVD-008 |
| EVD-013 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan), [VAL-DELTA-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec and Plan approval receipt | The user's answer "Approve and commit" to the SPEC-0161 approval question in this session, 2026-11-12, after the batch review EVD-010 and EVD-012 | PASS | Spec and Plan set to `approved` 1.0.0 together at first Git record (first-record approval extension). Approval does not accept a criterion or authorize push, PR or merge. | no | none |
| EVD-014 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Completeness check under approved parents | Single-use checker SHA-256 `e5136c1915d677d97ecc33f32fd5d57cd74c628df2dbe1c6ae0a7fb5820a10c2` over this Task (SHA-256 `64c32724eac714252479260cfa60a83d9dc998f48501392ee1668fdbf6b88961`) after approval; negative copy without R147-05, with GOV-01 writer `none` and OPEN-07 verdict `OPEN`; 2026-11-12 | PASS | Positive: 50 rows (21 COVERED, 27 OPEN, 1 REJECTED_BY_CONTRACT, 1 DECISION_NEEDED), OPEN-01..14 once each with an allowed verdict, every cited path tracked except the declared CREATE target `.agents/knowledge/glossary.md`. Negative: all three injected faults reported, exit 1. | yes | EVD-007 |
| EVD-015 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan), [VAL-DELTA-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"5b304a9dfdc190752a3afad4f8088a748c2f0215a906a13fbf4f0afb1e23ad4f","plan_sha256":"e388f9e724ba5beabd088272fee6aaf39d18a360eeb4e6a1908a0747afed2620"} | PASS | Same read-only reviewer as EVD-010 and EVD-012, round 3, 2026-11-12: both exact hashes matched; reverting only the version, status and approved wording reproduces the round-2 bytes `8acb1507…` and `5fe718c6…`; verdict APPROVE, no BLOCK, no FIX on Spec or Plan. | yes | none |
| EVD-016 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan), [VAL-DELTA-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Confirm approval to the SPEC-0161 exact-byte reconfirmation question dated 2026-11-12 Asia/Seoul","review_ref":"EVD-015","scope":["SPEC-0161","SPEC-0161-PLAN-0001"],"reviewed_spec_sha256":"5b304a9dfdc190752a3afad4f8088a748c2f0215a906a13fbf4f0afb1e23ad4f","reviewed_plan_sha256":"e388f9e724ba5beabd088272fee6aaf39d18a360eeb4e6a1908a0747afed2620","validity":"confirmed","revocation":"none"} | PASS | The user first answered Approve and commit (EVD-013) before review; after the review changes listed in the reconfirmation question the user confirmed these exact bytes. No message UUID was supplied or invented. This receipt accepts no criterion and authorizes no push, PR or merge. | yes | none |
| EVD-017 | [VAL-DELTA-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Strict document checks and exact-index QA | Package commit `9697d99c` (tree `e1985935dfb9d4f9f7a8f7ba17f0dcece578dae9`) on baseline commit `2c687402`; `python3 scripts/qa.py staged` (profile staged, snapshot index) and the commit hooks, with the scratch venv from `.github/requirements/ci-validation.txt` (pre-commit 4.6.1, jsonschema 4.26.0, Python 3.12) first on PATH; 2026-11-12 | PASS | Staged QA on the full index passed agent-governance, ci-python-contract, document-contract-registry, document-lifecycle, links-and-owners, markdown-profiles, repository-quality and selected-style; selected-nonstyle failed only because it trusts `HEAD:.secrets.baseline` before the baseline commit, so the baseline was committed first (`2c687402`). Both commits then passed the Staged QA Snapshot, commitizen and commit-message-exception hooks (exit 0). | yes | EVD-009 |
| EVD-018 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | User decisions on conflicts | Direct user messages in this session, 2026-11-12 Asia/Seoul: (1) where an existing rule conflicts with the current v14.7 requirement, change it to match the current requirement; (2) Q-07: renumber Stage 01, 02 and 03 as display numbers only, keeping `artifact_id` | PASS | RS-09 (DOC-09), GIT-09 and CI-SCOPE are adopted and replace the SPEC-0156 rejections; the machine-ledger rejection agrees with v14.7 and stays; POLICY-ROLE follows the same-role rule; DOC-12 is display-number renumbering after the open work closes. Rows and Conflicts updated. | no | none |
| EVD-019 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | W00 re-check after SPEC-0162 to SPEC-0164 | This Task's tables against commits `f0aa80cf` (SPEC-0162), `a84381dd` (SPEC-0163), `09293928` (SPEC-0164) and their Task evidence; `gh pr list` shows no PR after #227; 2026-11-12 | PASS | Updated: GOV-01, R45-08, R147-09 (glossary), GIT-09 (review path), RS-09 (derived reverse view) to COVERED; the Vocabulary handoff row closed; the GIT-09 and RS-09 conflicts marked implemented. New finding: the COMMIT-BEFORE surface selection gap, handed to W06. Still open in W00 scope: OPEN-01 and OPEN-02 (UNVERIFIED, not reopened), OPEN-04 (BLOCKED_EVIDENCE), OPEN-06 (UNVERIFIED until a stage proposes adoption), OPEN-07 (whole tree not selected); criterion acceptance pending. | no | none |
| EVD-020 | [VAL-DELTA-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Core-diff checklist | Diff `4a47cb40..af7484ec` and `9546baeb` for this package (6 files, 458 insertions, 2 deletions, then this Task only); risk class `low`: documents and reviewed `.secrets.baseline` digest entries, no policy, registry, validator, hook, workflow or permission file; 2026-11-12 | PASS | Acceptance matches VAL-DELTA-001 (EVD-014, EVD-019) and VAL-DELTA-002 (EVD-012, EVD-015, EVD-017). One writer per file (W00: this package, Stage 03 README, REQ-0003 sentence). No check removed or weakened. No secret; the baseline adds digests of this package's lines only. No permission, trigger or protected action changed. Recovery: revert the package commits. Findings: NOTE, the Next owners sentence named W01 for vocabulary, review path and DOC-09, which SPEC-0162 to SPEC-0164 have since done; updated in the Verification Summary. No BLOCK or FIX open. | yes | none |
| EVD-021 | [VAL-DELTA-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Hosted PR checks | PR #228 head `8bdbc3fcbccee2269bc3023216b321248035da44`; workflow `CI` run `43139364138` (jobs `ci-summary` `130922323793`, `style-pr` `130922323380`); `gh pr checks 228`; 2026-11-12 | PASS | `ci-summary` and `style-pr`, the two required contexts, passed; GitGuardian, greeting and label passed too. This observes the hosted result for that head only; later commits need their own run. | no | none |
| EVD-022 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | W00 follow-up OPEN correction | User W00 follow-up correction request of 2026-11-12; `OPEN-01-14.json`; a file-name and content search of `_workspace/workspace_execution_tasks/` and a path search of all 21 Git refs for the OPEN-04 originals; `git ls-files` at `d623681f` (659 files) | PASS | Added OPEN Disposition Corrections: OPEN-01 and OPEN-02 stay UNVERIFIED without blocking product work or asking for user acceptance; OPEN-04 BLOCKED_EVIDENCE is limited to the direct comparison and names the searched scope; OPEN-06 split into a closed licence row and a conditional perspective row; OPEN-07 split into inventory, read, consumer and verification denominators with owners. Earlier rows and tables are unchanged. | no | none |
| EVD-023 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | W02 follow-up survey | `scripts/document_lifecycle.py:408-445` (`artifact_identity_reuse_diagnostics`) and `.agents/governance/document-lifecycle.md:26` at `1e12f9fd`; code reading, not executed; 2026-11-12 | PASS | Found a W02 hand-off that SPEC-0167 did not record: identity reservation for documents that left the tree. The policy says stable identities are never reused, but `LIFECYCLE-IDENTITY-REUSE` reserves only identities present in the comparison base, so an ID retired through Git history is not protected by any check. Recorded in Stage Follow-up Handoffs below for W03 and W05. Also checked and kept: `context-and-memory.md:88` (memory never deleted by Task completion) matches the W02 scope rule; `tests/test_document_lifecycle_cumulative_history.py` does not read `docs/98.archive/` (active-document replay, ARC-07); ADR-0031's archive and retention clauses are already marked not current by ADR-0055 and ADR-0053, so it stays accepted. | no | none |
| EVD-024 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Isolated probe of the identity reuse check | `python3 -I` calling `scripts/document_lifecycle.py` `artifact_identity_reuse_diagnostics` with synthetic in-memory documents at `24492613`; no repository file read as input or written; 2026-11-12 | PASS | Control: a new document reusing `SPEC-0161`, present in the base, returned `LIFECYCLE-IDENTITY-REUSE`. Probe: a new document reusing `SPEC-0165`, which left the tree through Git history, returned 0 diagnostics. The W02-H01 gap is observed, not only read; the hand-off owner and resume condition are unchanged. It confirms EVD-023's code reading; EVD-023 was not a failure, so nothing is resolved. | no | none |
| EVD-025 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | W03 user decisions on form migration | Direct current-session user answers, 2026-11-12 Asia/Seoul, to two questions after a read-only W03 inventory at `0281409b` (84 profiles; about 129 current documents in the 16 common roles, 30 more in unclear roles) | PASS | (1) "Migrate all except ADRs": every current document moves to the COMMON-DOC-FORM-1 headings form-only (decisions, criteria, evidence values and IDs unchanged; Git history keeps the original bytes), except the 33 accepted ADRs, which keep their current form as a recorded exception until a successor replaces each one. (2) "Conditional local extension": `Archived Lineage` and the `Lifecycle Traceability` table stay as named conditional H3 extensions under the role's Traceability or References H2, each with condition, owner, verification, review point and removal criterion. Recorded in W03 Decisions below. | no | none |
| EVD-026 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | W03 user decisions on trace host and contract approval facts | Direct current-session user answers, 2026-11-12 Asia/Seoul, after the W03 phase-1 design | PASS | (1) "Nearest owning H2": Plan carries `Lifecycle Traceability` in the common H3 Implementation Strategy > Work Breakdown; Task, Guide, Runbook and Policy host it as a conditional local H3 under Execution Log, Verification, Validation and Ownership. (2) "Record as unverified": WGOV-CORE 3.0.0 stays `adopted` with its existing `approval_ref`; `approved_by`, `approved_at` and `effective_from` hold the literal `unverified`, allowed only with an `approval_ref`. Recorded as W03-D04 and W03-D05. | no | none |
| EVD-027 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | W03 phase-2 user decisions | Direct current-session user message, 2026-11-12 Asia/Seoul: "Governance policies: splitting the 9 core policies 적용, SKILL.md 적용. Table columns 적용. Unclassified READMEs 분석 진행" | PASS | (1) The 9 `governance/rule` policies move to the common Policy form (Purpose; Scope; Rules; Exceptions; Ownership), splitting their current sections form-only. (2) Every `SKILL.md` takes the common Skill form within provider format limits. (3) Table column contracts are added. (4) The unclassified README profiles are analysed first; their role mapping is a later decision. Recorded as W03-D06 to W03-D09. | no | none |
| EVD-028 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | W03 phase-2 decisions restated from current requirements | User instruction, 2026-11-12 Asia/Seoul: "W03-D06, W03-D07, W03-D08, W03-D09 등에 대한 Decision은 현재 요구 사항을 바탕으로 작성되어야 한다."; W03 package sections 4, 7 and COMMON-DOC-FORM-1 1.0.0 | PASS | W03-D06 to D09 in W03 Decisions now state the requirement source (POLICY-ROLE, COMMON-DOC-FORM-1, DOC-01, DOC-02, DOC-03, DOC-05, R45-10, R147-04, SUP-11) and the exact form, mapping, empty-section rule and table fields each requirement sets; the user's EVD-027 choices are unchanged. | no | none |
| EVD-029 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | W03 phase-2 user answers | Direct current-session user answers, 2026-11-12 Asia/Seoul, after the phase-2 design survey at `bfd3a05f`: D09 mapping "Recommended mapping"; link lists "요청 사항에 작성된 내용에 맞춰서"; Incident and Postmortem trace host "요청 사항에 맞춰서" | PASS | The last two are derived from COMMON-DOC-FORM-1 1.0.0 text, not chosen: every form's `extension_policy` forbids unregistered H2/H3, and every H3's `required_content` connects its own facts to real references; Incident Evidence ("근거와 후속") and Postmortem Evidence (Source Records, "사건·로그·결정 연결") are the only source-and-link sections. Recorded as W03-D10 to W03-D12. | no | none |
| EVD-030 | [VAL-DELTA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | W03-D10 to D12 re-review approved | User request, 2026-11-12 Asia/Seoul, to re-review D10 not-bound profiles, D11 link lists and D12 Incident and Postmortem host against the requirements; recommendation presented; user answer "승인" | PASS | D10: no profile is left without a role except the native `CLAUDE.md` files; Workspace README and Reference Pack README become own roles, the agent and provider READMEs join Stage README, the runtime-governance surface joins Service README, the root `AGENTS.md` joins AGENTS. D11: links placed inline by DOC-07 type. D12: Postmortem host changed from `Evidence` to `Corrective Actions`; Incident stays `Evidence`. EVD-029's earlier D10 to D12 text is superseded by these rows. | no | none |

### Edition Delta

| Input | v14.2 consumed by SPEC-0154..0160 | v14.7 | Effect |
| --- | --- | --- | --- |
| Original input report | `dc348e7f…` | same | No new source atoms. |
| 106 requirement IDs | 106 | 106, same IDs | No ID added or removed. |
| Requirement text | v14.1 base used (v14.2 bytes absent) | 16 rows changed in `implementation` or `verification` only (18 field changes) | Linked below. |
| Profile requirements K8S-01..03 | `079f07c1…` | same | No new profile duty. |
| Clauses | none | R45-01..12 (v14.5), R147-01..20 (v14.7) | Linked below. |
| Contracts | none | COMMON-DOC-FORM-1, QA-STAGES-1, QA-ALIGNMENT-v14_7, Repository Vocabulary, TemplateDefinition, Q-08 path decision | Handoff tables below. |

### Requirement Changes

State: COVERED (current owner already conforms, evidence named; for a clause a later stage also applies, COVERED means only that W00's own conduct conforms and that stage still applies it), OPEN (writer stage named), REJECTED_BY_CONTRACT (an accepted requirement and a same-scope user decision exclude it), DECISION_NEEDED (an unresolved conflict for the named stage).

| ID | Change | Current owner | State | Writer |
| --- | --- | --- | --- | --- |
| SCOPE-02 | Acceptance waiting is no reason to reimplement; KEEP and residual acceptance are separate axes | This Task; `docs/03.specs/AGENTS.md` rule 6 | COVERED | none |
| SCOPE-04 | Compare conditions, exceptions, negations and consumers, not only ID counts | This Task, Requirement Changes table | COVERED | none |
| SCOPE-10 | Distinguish current-copy migration of completed documents from historical bytes | `docs/AGENTS.md` rule 6; `docs/03.specs/AGENTS.md` rule 4 | OPEN | W03 (migration map in the same change as the form change) |
| GOV-01 | Define Repository Vocabulary in `.agents/knowledge/glossary.md` | Absent; terms live in `.agents/governance/sdlc.md` "Shared terminology and ownership" | COVERED | none (SPEC-0163, EVD-019) |
| GOV-04 | Approved registry is still a reform target | `docs/99.templates/registry.json` (`schema_version` 10) | OPEN | W01 policy, W03 registry |
| GOV-06 | Single-writer registry reformed; derived consumers read the new contract | `docs/99.templates/registry.json`, `scripts/document_contracts.py` | OPEN | W03 |
| DOC-04 | Profile field, state, relation and table definitions reformed | `docs/99.templates/registry.json` | OPEN | W03 |
| DOC-05 | Section and body contracts match target H2/H3 and tables | `docs/99.templates/registry.json` `sections`, `relationships.body_contract` | OPEN | W03 |
| DOC-11 | Every real template has a TemplateDefinition; Release role removed; Q-08 path kept | No TemplateDefinition equivalent; no Release role remains; path kept | OPEN | W03 |
| SDLC-01 | Remove an independent Release document role | REQ-0003 Scope excludes a Release family; no Release profile, template or validator rule exists | COVERED | none |
| SDLC-07 | Transition rules in the registry reformed with W03 | `.agents/governance/document-lifecycle.md` (semantics); `docs/99.templates/registry.json` `lifecycle` (W03 writes) | OPEN | W04 (policy semantics only) |
| SDLC-08 | Old approved registry edition is not a pass basis | `scripts/validate-document-lifecycle.py`, `scripts/document_lifecycle.py` | OPEN | W05 |
| ARC-05 | Recover real attachments when LFS, submodule or filters are used | No LFS, submodule or filter in use (no `.gitattributes` filter, no `.gitmodules`) | COVERED | none |
| QA-03 | Validator input is the reformed registry edition | `scripts/validate-document-contract-registry.py` | OPEN | W05 |
| QA-17 | Validators changed for the reformed registry; new violations fail | `scripts/validate-markdown-profiles.py`, `tests/test_*section*`, `tests/test_task_*` | OPEN | W05 |
| AGENT-04 | Separate direct, wrapper and nested hook delivery on the installed client | `.claude/hooks/k8s-pre-edit.sh`; provider note | OPEN | W07 |
| R45-01 | Trace prior instruction to current change per request | This Task, Edition Delta and this table | COVERED | none |
| R45-02 | Compare HEAD, files and recent PRs | This Task, Related Pull Requests | COVERED | none |
| R45-03 | Ask only real local conflicts | This Task, Conflicts | COVERED | none |
| R45-04 | Link external evidence to change and test | This Task, External Evidence | COVERED | none |
| R45-05 | Run only the selected stage in this workspace | This package scope | COVERED | none |
| R45-06 | Reform the approved registry itself | `docs/99.templates/registry.json` | OPEN | W03 |
| R45-07 | Keep `docs/99.templates/`; reform forms and consumers in place | Path unchanged; forms not yet reformed | OPEN | W03 |
| R45-08 | Repository Vocabulary in the glossary | Absent | COVERED | none (SPEC-0163, EVD-019) |
| R45-09 | Release role removal without removing tags, releases or CHANGELOG | Same as SDLC-01; `scripts/release.py` and runbook 0012 kept | COVERED | none |
| R45-10 | TemplateDefinition per real template | Absent | OPEN | W03 |
| R45-11 | OPEN-01..14 as historical identifiers | This Task, OPEN Dispositions | COVERED | none |
| R45-12 | Verify common adoption across four purposes | Other workspaces out of scope (package decision D-04) | OPEN | W11, this workspace only |
| R147-01 | Link sources, prior reports and ownership by ID | This Task with SPEC-0154/0158 reuse | COVERED | none |
| R147-02 | Read the workspace with a read denominator | This Task, Read Denominator (partial, stated) | COVERED | none |
| R147-03 | Approved norms are reform targets | Same as GOV-04 | OPEN | W01 |
| R147-04 | Common H2/H3 forms in templates and consumers | Document Form Handoff | OPEN | W03 |
| R147-05 | Tests, QA and scripts follow QA-ALIGNMENT | Stage QA Handoff and Document Form Handoff | OPEN | W05 |
| R147-06 | Bind Git before/during/after cells | Stage QA Handoff | OPEN | W06 |
| R147-07 | Separate SDLC stage from document STAGE | `.agents/governance/document-lifecycle.md` (W04 writes); `.agents/governance/sdlc.md` (W01 writes, W04 supplies semantics) | OPEN | W04 |
| R147-08 | Safe archive and exit | `LIFECYCLE-PACKAGE-EXIT` (SPEC-0159), ADR-0056 manual review | COVERED | none (W02 reuses) |
| R147-09 | Vocabulary owner alignment; keep Release role removed | Glossary absent | COVERED | none (SPEC-0163, EVD-019) |
| R147-10 | Keep path; migrate registry to CI chain | Path unchanged | OPEN | W03 |
| R147-11 | External sources linked to files and tests | This Task, External Evidence | COVERED | none |
| R147-12 | Protect completed work; link only new differences | This Task reuses SPEC-0154..0160 | COVERED | none |
| R147-13 | Self-contained stage prompts | Package property, not a workspace file | COVERED | none |
| R147-14 | Project-Template dev/main | Other purpose | COVERED | none (not applicable here) |
| R147-15 | blog-data domains | Other purpose | COVERED | none (not applicable here) |
| R147-16 | Kubernetes impact of governance changes | Manifests and their consumers | OPEN | W10 |
| R147-17 | Harness: static versus live provider evidence | `.claude/provider.md`, `.codex/provider.md` | OPEN | W07 |
| R147-18 | OPEN items' currentness | This Task, OPEN Dispositions | COVERED | none |
| R147-19 | Ask only unresolved conflicts | This Task, Conflicts | COVERED | none |
| R147-20 | Reuse only equivalent results | `.agents/governance/quality.md` validation runner envelope (W01 writes); `scripts/qa.py` result reuse | OPEN | W05 (`scripts/qa.py`); W01 writes the policy text |
| RS-09 | Generated reverse traceability (DOC-09: derive the reverse index from the single child-to-parent link) | REQ-0003 IF-0001 and Scope and Non-goals; `BODY-LINK-RECIPROCAL` in `scripts/validate-links-and-owners.py` | COVERED | none (SPEC-0164, EVD-019); parent-side link columns go with DOC-05 and R147-04 |
| GIT-09 | An extra agent API call is not a mandatory reviewer in single-maintainer review | REQ-0003 FR-0018; `.agents/governance/quality.md` Semantic review; `.agents/workflows/work-lifecycle.md` Completion | COVERED | none (SPEC-0162, EVD-019) |
| DOC-12 | Contiguous display numbers for Stage 01, 02 and 03 after the open work closes; `artifact_id` stays the stable trace ID; no retired ID reissued | File and folder names under `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`; registry `path_pattern` and identity rules | OPEN | W03 (last, after open packages close); decision EVD-018 |
| CI-SCOPE | PR-DURING runs affected implementation and product leaves in hosted CI | `.agents/governance/quality.md` hosted lane; `git.md`; `.github/workflows/ci.yml` | OPEN | W06 (`ci.yml`), W01 (policy text); decision EVD-018 |

### Related Pull Requests

| PR | Base | Head branch | Head | Merge | Merged (UTC) | Scope | Read |
| --- | --- | --- | --- | --- | --- | --- | --- |
| #227 | main | claude/exit-0159-0160 | `44f46944` | `4a47cb40` | 2026-11-11T14:10:07Z | Close SPEC-0159, SPEC-0160 | metadata |
| #226 | main | claude/w03-document-forms | `ab436a92` | `bebed75b` | 2026-11-11T14:01:17Z | W03 document form gaps (v14.2) | metadata |
| #225 | main | claude/w02-package-exit | `78bab1dd` | `6a82354b` | 2026-11-11T13:59:58Z | W02 package exit shape check | metadata |
| #224 | main | claude/w01-edition-check | `e84a954d` | `83abcad6` | 2026-11-11T12:35:09Z | W01 shared-edition check | metadata |
| #223 | main | claude/w00-closure | `18ef5024` | `6a519871` | 2026-11-11T11:50:22Z | SPEC-0158 W00 closure | metadata |
| #222 | main | claude/w01-governance-standards | `7963dd04` | `facb787e` | 2026-11-11T11:41:44Z | SPEC-0156 rejected clauses | metadata |
| #221 | main | claude/requirement-owner-crosswalk | `ff6bcdb2` | `6949179f` | 2026-11-11T11:04:14Z | SPEC-0154, SPEC-0155 | metadata |
| #220 | main | codex/manual-document-disposition-policy | `7b2b2e0c` | `b7497ee1` | 2026-11-10T22:44:28Z | Disposition review and lifecycle replay (ADR-0056) | metadata |

All eight are merged; merge is not criterion acceptance. Their acceptance lives in the archived Tasks. PR #220's lifecycle replay and ADR-0056 manual review are kept, as the prompt directs, and not re-registered.

### Document Form Handoff

Target: COMMON-DOC-FORM-1 1.0.0. Every current template lacks the target H3 set; the registry models H2 names only.

| Role | Current owner | Difference | Writer | Consumers to move together |
| --- | --- | --- | --- | --- |
| Requirement | `sdlc/requirement`, `templates/requirements/requirement-package.template.md` | 10 H2 against 5; Scope at 8 not 2; no conditional Quality Requirements | W03 | W05 section tests |
| Architecture | `sdlc/architecture-description`, `templates/architecture/description.template.md` | Only Overview and Traceability match | W03 | W05 |
| ADR | `sdlc/architecture-decision`, `templates/architecture/decision.template.md` | Extra Overview and Explicit Non-goals; Alternatives after Consequences; Supersession only in frontmatter | W03 | W04 lifecycle (supersession) |
| Spec | `sdlc/spec`, `templates/specs/spec.template.md` | 11 H2 against 5; only Overview matches | W03 | W05 (`scripts/document_lifecycle.py`, tests) |
| Plan | `sdlc/plan`, `templates/specs/plan.template.md` | Promotion optional against required Promotion Map; Dependencies and Implementation Strategy missing | W03 | W04 promotion receipts |
| Task | `sdlc/task`, `templates/specs/task.template.md` | No H2 matches; body contract binds "Task Table" and "Lifecycle Traceability" | W03 | W04; W05 `test_task_execution_contract.py`, `test_task_acceptance_contract.py`; W01 `work-lifecycle.md` and `quality.md` name current Task headings |
| Guide, Runbook, Policy | `operation/{guide,runbook,policy}`, `templates/operations/` | H2 names differ; Policy lacks Ownership | W03 | W05 `test_operations_section_contract.py` |
| Incident, Postmortem | `operation/{incident,postmortem}` | 10 and 12 H2 against 5 | W03 | W05 |
| Root README | `common/readme-repository` | Only the optional Getting Started matches; Purpose, Repository Map and References differ | W03 | W05 README navigation |
| Stage README | `common/readme-stage-index` | Only Related Documents matches | W03 | W05 |
| Service README | No such role; nearest `common/readme-implementation` | Role scope undecided | W03 | none yet |
| AGENTS | `common/folder-agents-guide`, no template | Template absent | W03 | W07 loaders |
| Skill | `common/native-skill-package`, no template | Template absent; `governance/skill` governs workflows, not `SKILL.md` | W03 | W07 |
| Registry model | `docs/99.templates/registry.json`, `docs/99.templates/contracts/document-profile.schema.json`, `scripts/document_contracts.py` `HeadingContract` | No H3, section_id, parent_id, condition, empty_policy, TemplateDefinition or template version | W03 | W05 |
| H3 and empty rules | `scripts/validate-markdown-profiles.py` `_body_diagnostics`, `_scan_required_h2_content` | No parent-aware H3, order, duplicate or conditional checks; empty rule only on required H2; `ordered` only on 6 profiles | W05 | W03 registry flags |
| Fenced fake headings | `scan_headings` | Handled; no negative test | W05 | none |
| Generator | None: no script fills `{{TITLE}}` placeholders; forms are copied by hand | Target chain names a Generator; create it or record why none is needed | W03 | W05 |
| Link-only section | `_LINK_ONLY_SECTIONS = {"Related Documents"}` hard-coded in `scripts/validate-markdown-profiles.py` | Must follow the registry when headings change | W05 | W03 |
| Vocabulary | `.agents/knowledge/glossary.md` (SPEC-0163) | Done: 33 common terms, local extensions, validator check | none | W05 consumers in place |
| Policy versus `governance/rule` | `operation/policy`, `governance/{role,rule,skill}` | Target Policy role owner undecided; `governance/*` not in the 16 target roles | W01 then W03 | none yet |

### Stage QA Handoff

Target: QA-STAGES-1. PASS means the current binding already gives the target guarantee.

| Cell or row | Current binding | State | Writer |
| --- | --- | --- | --- |
| COMMIT-BEFORE | `staged-qa` → `scripts/qa.py staged` on the index snapshot; partial stage covered by `tests/test_qa_runner.py`. Selection gap found 2026-11-12: a change to `.agents/governance/*.md` alone does not select `document-contract-tests`, although `tests/test_document_frontmatter_negatives.py` reads `.agents/governance/document-lifecycle.md`; SPEC-0162 commit `f0aa80cf` broke that suite unseen (SPEC-0163 EVD-009) | PASS for input; GAP in surface selection | W06 (`scripts/validation/registry.json` surfaces), W05 consumer |
| COMMIT-DURING | commitizen and `scripts/commit-message-exceptions.py`; no prepare-commit-msg or pre-merge-commit | PASS, low gap | W06 |
| COMMIT-AFTER | No post-commit; Task evidence is the record | GAP, low; decide no blocking hook | W06 (`scripts/githooks/`) |
| PUSH-BEFORE | `scripts/githooks/pre-push` has no target | GAP or N/A by `git.md` | W06 |
| PUSH-DURING | Branch protection read back 2026-11-11T23:46Z: force push and deletion disabled, admins enforced | PASS | none |
| PUSH-AFTER | Push-event `ci-summary` reports NOT_APPLICABLE | PASS | none |
| PR-BEFORE | `git.md` and PR template only | PASS, policy only | W06 (`.github/PULL_REQUEST_TEMPLATE.md`) |
| PR-DURING | `pull_request`, checks `refs/pull/N/merge`, base and head identity asserted, tools from trusted base | PASS for identity; scope DECISION_NEEDED (CI-SCOPE) | W01, then W06 |
| PR-AFTER | No `workflow_run`; manual readiness | N/A | none |
| MERGE-BEFORE | Read back: required contexts `ci-summary`, `style-pr` with `strict: true` (branch must be up to date), merge commit only, 0 required reviews | PASS; `main-protection.md` does not mention `strict` | W06 (should record `strict` in `.github/rulesets/main-protection.md`) |
| MERGE-DURING | No merge queue | N/A | none |
| MERGE-AFTER | No post-merge regression; `cancel-in-progress` on main | GAP, policy-accepted | W06 |
| SDLC rows | `PLAN-PROMOTION` (`scripts/validate-document-lifecycle.py` 665-786) checks table shape, one link to an approved `.agents/` or Stage 01/02/05 owner and duplicates; not the anchor or member, and no Task receipt cross-check seen (lines after 889 unread) | GAP | W05 (`scripts/validate-document-lifecycle.py`) |
| DOC-S00 | Agent-governance and knowledge checks; vocabulary rule_id binding absent | GAP | W01 (`.agents/knowledge/glossary.md`); W05 consumes |
| DOC-S01 to S03, S05 | Profile, lifecycle, links, package exit | Survey PASS (validators not read) | none |
| DOC-S90 | Profiles `reference/*`, `ARTIFACT-IDENTITY`, pack topology and README navigation are checked; source, edition and freshness are prose only and no generated-snapshot freshness check exists | GAP | W05 (`scripts/validate-markdown-profiles.py`) |
| DOC-S98 | No body re-check; archive excluded | Survey PASS | none |
| DOC-S99 | Registry checks pass today; tests hard-code current headings (see OPEN-09) | CONFLICT with COMMON-DOC-FORM-1 | W03 (`docs/99.templates/`); W05 consumes |
| DOC-DOMAINS | Vault ESO surfaces; no content or site domain | PASS; N/A for site | none |
| Old-rule tests | `tests/test_validate_ci_python_contract.py`, `scripts/validate-ci-python-contract.py`, `tests/test_ci_branch_metadata.py`; `scripts/validate-pr-metadata.py` mirrors the `ci.yml` inline script | Move only with CI-SCOPE | See Primary Writers |

### Primary Writers

One primary writer per file; other stages consume through the named interface.

| Files | Primary writer | Interface consumers |
| --- | --- | --- |
| `.agents/knowledge/glossary.md` (create), `.agents/governance/sdlc.md`, `quality.md`, `git.md`, `document-authoring.md`, `.agents/workflows/work-lifecycle.md` | W01 | W03, W04, W05, W06, W07 |
| `.agents/governance/document-lifecycle.md` | W04 | W03 registry `lifecycle`, W05 lifecycle validator |
| `docs/99.templates/registry.json`, `docs/99.templates/contracts/document-profile.schema.json`, `docs/99.templates/templates/`, `docs/99.templates/README.md`, `scripts/document_contracts.py`, current documents under `docs/01`, `02`, `03`, `05` and READMEs | W03 | W04, W05 |
| `scripts/validate-markdown-profiles.py`, `scripts/validate-document-contract-registry.py`, `scripts/validate-document-lifecycle.py`, `scripts/document_lifecycle.py`, `scripts/validate-links-and-owners.py`, `scripts/validate-ci-python-contract.py`, `scripts/qa.py` and `tests/` | W05 | W03, W04, W06 |
| `.github/workflows/ci.yml`, `scripts/validate-pr-metadata.py`, `.pre-commit-config.yaml`, `scripts/githooks/`, `.github/rulesets/main-protection.md`, `.github/PULL_REQUEST_TEMPLATE.md` | W06 | W05 |
| `.claude/hooks/`, `.claude/provider.md`, `.codex/provider.md` | W07 | none |
| Kubernetes manifests and their consumers | W10 | none |

### External Evidence

| Source | Access | Applied to | Result |
| --- | --- | --- | --- |
| RS-09 NASA SWE-052 | Inherited, not re-queried | Bidirectional links | Single forward link; reverse index to be derived (adopted, EVD-018) |
| RS-18 | Inherited | Survey before change | This package records; writers change |
| RS-22 Git worktree | Inherited | Workspace boundary | Single worktree, no new worktree |
| RS-39 | Inherited | Selective reading | Unchanged inputs reused from SPEC-0154..0158 |
| RS-49 `git diff --cached` | Direct relevant sections (package) | COMMIT-BEFORE | Index snapshot and partial-stage test exist |
| RS-50 GitHub events | Direct relevant sections (package) | PR-DURING | Merge SHA checked out; head and base asserted |

### OPEN Dispositions

| ID | Verdict | Basis | Next owner |
| --- | --- | --- | --- |
| OPEN-01 | UNVERIFIED | Source bytes unchanged; preserved, not certified (SPEC-0158) | Package reviewer |
| OPEN-02 | UNVERIFIED | Same as OPEN-01 | Package reviewer |
| OPEN-03 | RESIDUAL_CONFIRMED | 52 local packages linked in SPEC-0155: 37 DELTA open at their stages | Named stages |
| OPEN-04 | BLOCKED_EVIDENCE | `SOURCE_BYTES_NOT_AVAILABLE`; no history archive holds them | Holder of the original reports |
| OPEN-05 | CLOSED_BY_EVIDENCE | Article retrieved directly on 2026-11-12 (HTTP 200, published 2026-10-25, SHA-256 `41115ffd3c337d24a6d41f58af0b55ee65c9a3d279e64ff261e93240c3944482`); the article's companion repository SillyMemory has licence AGPL-3.0 (`LICENSE` blob `0ad25db4`), `main` now `32ce8464`; nothing adopted | none |
| OPEN-06 | UNVERIFIED | Licence caveat closed: agency-agents `LICENSE` is MIT (blob `523078c0`, `main` still `8ae61646`). The 13 UNVERIFIED and 10 reference-for-stage perspective rows of SPEC-0155 stay open until a stage proposes adopting one | Stage that proposes adoption |
| OPEN-07 | RESIDUAL_CONFIRMED | Cited files plus `scripts/`, `tests/`, hooks and workflows listed; whole tree not read | W00 on request |
| OPEN-08 | UNVERIFIED | No live, native or cluster authority in this scope | W10 |
| OPEN-09 | RESIDUAL_CONFIRMED | Hard-coded current headings: `tests/test_task_execution_contract.py` (Task, Spec and Plan fixtures, `section == "Task Table"`), `tests/test_task_acceptance_contract.py` (`#success-criteria--verification-plan`, `## Task Evidence`), `tests/test_document_terminal_contract.py` (incident and postmortem H2); registry-driven or synthetic: `test_operations_section_contract.py`, `test_repository_form_contracts.py`, `test_document_frontmatter_negatives.py` | W05 |
| OPEN-10 | NOT_APPLICABLE | hy-home-docker only | none |
| OPEN-11 | NOT_APPLICABLE | hy-home-docker only | none |
| OPEN-12 | NOT_APPLICABLE | hy-home-docker SPEC-0212 only | none |
| OPEN-13 | CLOSED_BY_EVIDENCE | Read back 2026-11-11T23:46Z: required `ci-summary` and `style-pr` (app 15368, strict); both passed on PR #227 head; on `main` `4a47cb40` `ci-summary` succeeded and `style-pr` skipped by design | none |
| OPEN-14 | NOT_APPLICABLE | hy-home-docker runner only | none |

### OPEN Disposition Corrections

Added 2026-11-12 under the user's W00 follow-up correction request (EVD-022). The table above stays as recorded; for the IDs below, this section replaces its `Basis` and `Next owner` wording. OPEN-01..14 are historical audit identifiers of the earlier prompt packages, not open product work: the historical verdict, the current product effect, execution state and user acceptance are separate fields, and no historical verdict blocks W01..W11.

| ID | Historical meaning | Checked | Prior decision | W00 scope | Current product effect | Owner | Verdict | Next action | Only blocked scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OPEN-01 | Full semantic atomization of the 1,250 original lines | `OPEN-01-14.json`; SPEC-0158 OPEN table at `6a519871`; source bytes unchanged | SPEC-0158: preserved, not certified | Reuse of prior evidence only; no new atomization | None shown: no current contract, manifest or document gap traced to an unreviewed line | Shared source research (W00 package level), not a k8s Task | UNVERIFIED | Hand over only a difference shown to affect a current owner, to that owner's stage | Claims that the 1,250 lines are fully atomized |
| OPEN-02 | Review of 14,028 relation candidates | Same as OPEN-01 | SPEC-0158: preserved, not certified | Same as OPEN-01 | None shown | Same as OPEN-01 | UNVERIFIED | Same as OPEN-01 | Claims that the relation candidates are reviewed |
| OPEN-04 | Byte comparison with the exact WMC-20261110-03 and 20261102 v4 originals | Searched: file names and contents under `_workspace/workspace_execution_tasks/` (only the package's own references in `OPEN-01-14.json`, `SUPPLEMENTS.json`, `v11-SUPPLEMENT-CLAUSES.json`, `PRIOR-V11-REMAINING-WORK.json` and the guide, no original); every path in this repository's Git history over all 21 refs (no match). Not searched: other machines, accounts or archives | None | Located originals only | None: the current k8s contracts do not depend on those bytes | Holder of the original reports, if one is found | BLOCKED_EVIDENCE (direct comparison only) | None now; compare if the originals are supplied | The direct byte comparison of those two originals |
| OPEN-06 (licence) | Licence caveat of the agency-agents source | agency-agents `LICENSE` blob `523078c0` (MIT), `main` `8ae61646` | None | Read once on 2026-11-12 | None; nothing adopted | none | CLOSED_BY_EVIDENCE | None; not repeated | None |
| OPEN-06 (perspectives) | 13 UNVERIFIED and 10 reference-for-stage perspective rows of SPEC-0155 | SPEC-0155 tables via SPEC-0158 | None | Not reviewed | None; no stage plans to adopt an external source | W01, W03 or W07, only when that stage plans to adopt a named source | UNVERIFIED | Research only the source that stage proposes to adopt | Adoption of an unreviewed perspective |
| OPEN-07 | Full survey of the local workspace | `git ls-files` at `d623681f`; the Read Denominator above; SPEC-0162 to SPEC-0165 work | No recorded user decision narrows the survey to cited files | Inventory complete; reading, consumer tracing and verification partial (counts below) | Unread files may hold differences the writer stages must find before editing | W03, W05, W06, W07, W10 by file set (below) | RESIDUAL_CONFIRMED | Each writer stage reads its whole file set before editing | Claims about unread file content |

OPEN-07 denominators at `d623681f`:

| Measure | Denominator | Done | Not done | Owner of the rest |
| --- | --- | --- | --- | --- |
| Inventory (tracked files) | 659 | 659 listed by top-level path | none | none |
| Content read at intake (Read Denominator sets) | 202 listed | 16 read, 39 partial | 147 listed only | W03 templates and registry, W05 `scripts/` and `tests/`, W06 workflows and hooks, W07 `.claude/hooks/` |
| Files outside the intake sets | 457 | Files read later by SPEC-0162 to SPEC-0165 only (governance policies, Stage 03 documents, `chained-hook.sh`, link and knowledge validators and their tests) | the rest, including `gitops/` 88, `infrastructure/` 18, `examples/` 40, `policy/` 5 | W10 for Kubernetes manifests and their consumers; W07 for `.agents/`, `.claude/`, `.codex/`; W03 for `docs/` |
| Consumer tracing | Files changed on this branch | Link search, `document-backlinks.py` and validation-registry routes for the changed files | tree-wide consumer map | Each writer stage for its files |
| Product verification | Changed paths | Staged repository-static QA on every commit | live, cluster or native runtime checks (OPEN-08) | W10 |

The other IDs keep the verdicts above: OPEN-03 RESIDUAL_CONFIRMED at the named stages, OPEN-05 and OPEN-13 CLOSED_BY_EVIDENCE, OPEN-08 UNVERIFIED for W10, OPEN-09 RESIDUAL_CONFIRMED for W05, and OPEN-10 to OPEN-12 and OPEN-14 NOT_APPLICABLE.

### Conflicts

| ID | Files | Current | Package | Decision |
| --- | --- | --- | --- | --- |
| RS-09 | REQ-0003 Scope and Non-goals and IF-0001; `BODY-LINK-RECIPROCAL` | Hand-written back-links required | Reverse index derived from the single child-to-parent link | Adopted and implemented by SPEC-0164 (EVD-019) |
| CI-SCOPE | `.agents/governance/quality.md` hosted lane; `git.md`; `.github/workflows/ci.yml`; `tests/test_validate_ci_python_contract.py` | Hosted CI runs metadata and style only | PR-DURING runs affected leaves under trusted configuration and least privilege | Adopt (EVD-018): PR code runs with a read-only token and no secrets |
| POLICY-ROLE | `docs/99.templates/registry.json` `operation/policy`, `governance/rule` | Two shapes | One Policy role | Adopt (EVD-018): both profiles implement the common Policy form; W03 |
| GIT-09 | REQ-0003 FR-0018 and Scope and Non-goals; `quality.md` Semantic review | An independent agent reviewer is required | No extra agent API call as a mandatory reviewer | Adopted and implemented by SPEC-0162 (EVD-019) |
| DOC-12 | Stage 01/02/03 file and folder numbers | Number equals stable ID; gaps kept | Contiguous numbering from 1 | Adopt as display numbers only (Q-07, EVD-018); `artifact_id` unchanged; after open work closes |
| LEDGER | REQ-0003 Scope and Non-goals (FR-0019, FR-0022) | No machine ledger | v14.7 also forbids a competing ledger (GOV-03, SDLC-04) | No conflict; existing rule kept |

### Read Denominator

| Set | Listed | Read | Partial | Listed only |
| --- | --- | --- | --- | --- |
| Package v14.7 contracts and source deltas | 12 | 7 | 3 | 2 |
| `docs/99.templates/registry.json` and schema | 2 | 0 | 2 | 0 |
| Templates under `docs/99.templates/templates/` | 37 | 0 | 18 (headings) | 19 |
| `scripts/` tracked files | 65 | 4 (`qa.py`, `githooks/chained-hook.sh`, `githooks/pre-push`, `githooks/pre-commit`) | 8 | 53 |
| `tests/` tracked files | 76 | 3 | 5 | 68 |
| `.github/workflows/` | 3 | 1 (`ci.yml`) | 0 | 2 |
| `.claude/hooks/` and settings hooks | 3 | 1 (settings block) | 0 | 2 |
| Governance policy files | 4 | 0 | 3 (`quality.md`, `git.md`, `sdlc.md`) | 1 |

Listed-only files are not semantically reviewed. Each writer stage re-reads its files before editing.

### Stage Follow-up Handoffs

Added 2026-11-12 under the user's W02 follow-up request (EVD-023). SPEC-0167 left the tree with its Task frozen, so a hand-off found afterwards is recorded here, the open owner of the W01 to W10 hand-off tables.

| ID | Source requirement | Gap | Owner | Interface | Resume condition |
| --- | --- | --- | --- | --- | --- |
| W02-H01 | W02 section 3 item 1 (registry retention and identity reservation reviewed, changes to W03); `document-lifecycle.md:26` | `LIFECYCLE-IDENTITY-REUSE` reserves only identities present in the comparison base; an ID whose document left through Git history can be minted again | W03 registry author, then W05 validator author | W03 decides where retired identities are reserved (for example the owners' `Archived Lineage` rows or a registry key); W05 extends the reuse check to that source with a refusal test for a retired SPEC ID | W03 starts |

### W03 Decisions

Added 2026-11-12 under the user's W03 request (EVD-025). W03 runs as several Stage 03 packages; each reads these decisions.

| ID | Decision | Effect on current rules | Owner |
| --- | --- | --- | --- |
| W03-D01 | Form-only migration of current documents to COMMON-DOC-FORM-1, except accepted ADRs | The append-only Task evidence and `TASK-EVIDENCE-RETENTION` rules gain a recorded form-only route that maps old to new headings and keeps every row value; Stage 02 `AGENTS.md` rule 3 stays for ADR bodies | W03 (registry, forms, documents), W05 (retention check) |
| W03-D02 | Accepted ADRs keep their current form until replaced | The ADR profile accepts the current form for an `accepted` ADR as a conditional extension with removal criterion "replaced by a successor ADR"; a new ADR uses the common form | W03, W05 |
| W03-D03 | `Archived Lineage` and `Lifecycle Traceability` are conditional local extensions | Kept under the role's Traceability or References H2; the package-exit check and recovery commands keep their heading | W03, W05 |
| W03-D04 | `Lifecycle Traceability` host where no Traceability or References H2 exists | Plan: common H3 Implementation Strategy > Work Breakdown; Task: Execution Log; Guide: Verification; Runbook: Validation; Policy: Ownership; each a conditional local H3 except Plan | W03 |
| W03-D05 | Shared contract approval facts not on record stay `unverified` | WGOV-CORE keeps stage `adopted` and its `approval_ref`; new approver and date fields hold `unverified`; nothing is inferred from the owner name | W03 |
| W03-D06 | Policy form (POLICY-ROLE; COMMON-DOC-FORM-1 Policy; R147-04; SUP-11) | The 9 `governance/rule` and 5 `operation/policy` documents are one Policy role and move together to Purpose (Objective, Authority), Scope (Applies To, Exclusions), Rules (Requirements, Enforcement), Exceptions (Exception Conditions, Approval and Review), Ownership (Responsibilities, Change and Adoption). Old sections map without meaning loss (Overview to Objective, Authority Boundary to Authority, Governance Context to Applies To, Current Contract and Controls to Requirements with their H3 as H4, Validation and Refresh and Verification and Review to Enforcement). Where no source text exists, the section states none with its reason (`explain_none_or_not_applicable`); no new rule is invented. `REGISTRY_POLICY_ROLE` stays strict | W03 |
| W03-D07 | Skill form (COMMON-DOC-FORM-1 Skill; DOC-02; DOC-03) | Every `SKILL.md` moves to Purpose and Trigger (When to Use, When Not to Use), Procedure (Steps, Failure Handling), Inputs and Outputs, Verification (Checks, Completion and Handoff). Provider frontmatter and loader paths stay unchanged (DOC-02); the body stays an invoked procedure, not a standing rule (DOC-03). Missing content is stated as none with its reason; native discovery is W07 evidence | W03; W07 |
| W03-D08 | Table contracts (R45-10 TemplateDefinition `tables`; DOC-05; COMMON-DOC-FORM-1 conditional tables) | Each role's tables are recorded with name, section, ordered columns (key, meaning, data type, required), minimum rows and row identity. Phase-2 tables are the contract's conditional ones (Guide step/action/check, Runbook trigger/action/rollback, Policy rule/condition/evidence, Incident timestamp/event/actor, Postmortem action/owner/verification, README path/purpose, AGENTS rule/trigger/effect, Skill step/input/output) plus the existing `Lifecycle Traceability` and README index columns at their new headings. The validator checks column order and count | W03, W05 |
| W03-D09 | Profiles without a clear common role (W03 package section 7.4: the role table is not a closed list; DOC-01; R45-10) | A profile maps to a common role only when its readers and purpose match that role; otherwise it keeps its current form as its own role and gains a TemplateDefinition. No profile is merged or reformatted to fit the count. The per-profile analysis goes to the user before any binding | W03; user decision |
| W03-D10 | Role for every unclear profile (DOC-01 README kinds root, stage, collection, service, workspace and reference package; TEMPLATE-DEFINITION-CONTRACT: the 16 roles are not a closed list and every real role gets a TemplateDefinition; DOC-02) | Stage README: `common/readme-collection-index` and the 4 agent and provider READMEs (`.agents/`, `.claude/`, `.codex/`, `.agents/evaluations/`), whose readers and purpose (routing a document or configuration tree) match. Service README: the 16 code and configuration READMEs of `common/readme-implementation` (the `gitops`, `infrastructure`, `scripts`, `tests`, `policy`, `secrets` and `examples` directories) and `.github/repository-surface.md`. Skill: `governance/skill` (`.agents/workflows/*.md`) with one registered local H3 `Authority Boundary`. AGENTS: the root `AGENTS.md`, moved with the 15 folder files. Own role with its own form and TemplateDefinition: Workspace README (`common/readme-workspace-staging`) and Reference Pack README (research, audit and data pack READMEs, one form; `Research Contract` and `Audit Contract` become `Pack Contract`; `Refresh and Succession` and `Review and Closure` become conditional). Native, no common role: root `CLAUDE.md` and the folder `CLAUDE.md` imports (DOC-02) | W03; W07 for native discovery |
| W03-D11 | `Related Documents` link lists in Guide, Runbook and Policy (COMMON-DOC-FORM-1 `extension_policy`; each H3 `required_content` "실제 참조로 연결한다"; DOC-07 link types) | No unregistered `Related Documents` heading: a generic link list has no unique meaning to register. Each link moves inline by its DOC-07 type: normative to Policy Purpose > Authority or Rules > Requirements, Guide Prerequisites > Permissions, Runbook Preconditions > Authority and Access; evidence to Policy Rules > Enforcement, Guide Verification, Runbook Validation > Evidence; navigation to Guide Purpose > Outcome, Runbook Purpose > Scope, Policy Scope > Applies To; historical beside its fact, marked non-authoritative. `Lifecycle Traceability` stays a registered local H3 (W03-D03, W03-D04) | W03 |
| W03-D12 | `Lifecycle Traceability` host for Incident and Postmortem (W03-D03; COMMON-DOC-FORM-1 section content; current table columns) | Incident: a conditional local H3 under `Evidence` (columns Timeline or action, Evidence, Follow-up Task match "근거와 후속" and Follow-up Owners). Postmortem: a conditional local H3 under `Corrective Actions` (columns Root cause or action, Owner and due state, Follow-up Task, Feedback target match Actions and Verification "후속 Task 참조") | W03 |
| W03-H01 | Phase 2 forms: Guide, Runbook, Policy, Incident, Postmortem, READMEs, `AGENTS.md`, `SKILL.md`; table column contracts; README rule IDs in tree mode; roles for the unclear profiles | One role form per change in `common_forms`, TemplateDefinitions filled, documents moved form-only | W03; resume now (SPEC-0168 accepted) |
| W03-H02 | Phase 3 forms: Requirement, Architecture, ADR with W03-D02, Spec, Plan, Task; delete the H2-list model, list-built `HeadingContract.allowed` and `BODY-HEADING-EMPTY` for form profiles | Consumer renames and the `TASK-EVIDENCE-RETENTION` heading map | W03; resume after phase 2 is accepted; if W04 starts first, record the slip here |
| W03-H03 | Retired-identity reservation (W02-H01) | Reserve IDs named in the owners' `Archived Lineage`; refusal test for a retired SPEC ID | W05; resume now |
| W03-H04 | Generator reason | Verify that template parity and the template-mode tree check stand in for a generator | W05; resume now |
| W03-H05 | ADR `rejected` state | Keep or remove the stored state given the W02 exit rule | W04; resume when W04 starts |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-DELTA-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-014, EVD-015, EVD-016 | Accepted by the user on 2026-11-12 (direct answer "ok" to the 12-criterion acceptance question) | platform |
| [VAL-DELTA-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-012, EVD-015, EVD-016, EVD-017, EVD-020 | Accepted by the user on 2026-11-12 (direct answer "ok" to the 12-criterion acceptance question) | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/0161-w00-v14-7-delta-intake/`, `docs/03.specs/README.md`, one back-link sentence in `docs/01.requirements/0003-workspace-agent-governance-platform.md` Traceability, `.secrets.baseline` (reviewed digest entries only, if the secret scan flags this Task's digests)
- **Forbidden Paths**: every file named in a handoff table; `_workspace/workspace_execution_tasks/` (read-only input)
- **Approval Required**: Spec and Plan approval; any commit, push, PR, merge or package exit; the CI-SCOPE and POLICY-ROLE decisions belong to W01
- **Static Validation**: strict document validators, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface in scope
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: delete the branch `claude/w00-v14-7-intake`; `main` is unchanged
- **Evidence Location**: this Task

## Verification Summary

Required completeness (EVD-014), independent review (EVD-012, EVD-015) and exact-index QA (EVD-017) pass; the user accepted every criterion on 2026-11-12. Residual risk: the survey read large validators and tests in part; writers must re-read before editing. The core-diff checklist is EVD-020 (risk class `low`). GOV-01 vocabulary, GIT-09 review path and DOC-09 are done in SPEC-0163, SPEC-0162 and SPEC-0164. Next owners: W01 (GOV-02 to GOV-08, CI-SCOPE policy text, POLICY-ROLE), then W03, W04, W05, W06, W07 and W10 per the handoff tables; DOC-12 display renumbering last.
