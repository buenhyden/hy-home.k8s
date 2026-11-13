---
title: "W03 Small Local Forms"
version: "0.3.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0186-TSK-0001"
parent_ids: ["SPEC-0186-PLAN-0001"]
---

# Task: W03 Small Local Forms

## Overview

This Task records the six small local forms of handoff W03-H28 (W03-D26), for [SPEC-0186](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items, to fix anything decided or built differently from the W00 to W03 requirements, to present decisions with options, to start work that can run in parallel, and approved commit, push, PR and merge in that request. The request approves no Spec bytes or criterion.
- **Base:** branch `claude/w03-small-local-forms` from `cd174848` (`main` after PR #251, SPEC-0190; SPEC-0182 to SPEC-0185 and SPEC-0190 merged); checked against `main` before delivery.
- **Decisions reused:** SPEC-0161 W03-D26, W03-D01 and W03-H28.
- **Decision recorded with this package:** W03-D33 to W03-D36 (provider-native stays form-less; governance-role split; research H3 registered as is; one reference-report form with link-only Sources); user answers of 2026-11-13 to the local-forms questions.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SMALLFORMS-001](../spec.md#success-criteria--verification-plan) | Form literal and schema; six forms; profile lists; table sections and definition texts; tests. | platform | completed | PASS | EVD-006 |
| WORK-002 | [VAL-SMALLFORMS-002](../spec.md#success-criteria--verification-plan) | Policy texts; unchanged-document proof; regression and exact-index QA. | platform | completed | PASS | EVD-007, EVD-008, EVD-009 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-SMALLFORMS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only reviewer that wrote none of the package, over the drafts of the Spec and Plan; 2026-11-13 | PASS | Conditional APPROVE over spec.md `d233c8d4…` and plan.md `d3c5fa20…` with FIX-1 (nine-role wording), FIX-2 (nine tables and table diagnostics), FIX-3 (four-step commit order) and NITs, applied to the drafts. | no | none |
| EVD-002 | [VAL-SMALLFORMS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"ec14697e2e313b1c2e5a32ba016f1c7196e5386583deedac394fdfa0dfbebf38","plan_sha256":"5eebb58dec8cf58545bd802af1fe3c6c2c4181568d01480b736dcd22ad6592d6"} | PASS | Same reviewer: round 2 APPROVE confirming the fixes over the final bytes named here. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-SMALLFORMS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0186 approval question naming spec.md ec14697e and plan.md 5eebb58d dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0186","SPEC-0186-PLAN-0001"],"reviewed_spec_sha256":"ec14697e2e313b1c2e5a32ba016f1c7196e5386583deedac394fdfa0dfbebf38","reviewed_plan_sha256":"5eebb58dec8cf58545bd802af1fe3c6c2c4181568d01480b736dcd22ad6592d6","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-004 | [VAL-SMALLFORMS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"b5e1a28f624adfbf5d2f74b0e7d16ff163e6518b0603bd2ae38e95582d5ae6ac","plan_sha256":"1bd6b6068c05dab8dac3fe1bdaa0bcde5ecd763f6e1c3e706ca6ac6d708d5703"} | PASS | Read-only reviewer that wrote none of the package, 2026-11-13: the only difference from the bytes approved in EVD-003 is the deleted frontmatter `layer` line in each file, required by SPEC-0184 (W03-D22) and announced by the open-package layer rule these bytes already named; facts re-checked on `main` with line drift only. APPROVE. | yes | none |
| EVD-005 | [VAL-SMALLFORMS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0185 to SPEC-0189 re-approval question naming spec.md b5e1a28f and plan.md 1bd6b606 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-004","scope":["SPEC-0186","SPEC-0186-PLAN-0001"],"reviewed_spec_sha256":"b5e1a28f624adfbf5d2f74b0e7d16ff163e6518b0603bd2ae38e95582d5ae6ac","reviewed_plan_sha256":"1bd6b6068c05dab8dac3fe1bdaa0bcde5ecd763f6e1c3e706ca6ac6d708d5703","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-006 | [VAL-SMALLFORMS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Form identifiers, schema, six forms, profile lists, section-id tables, TemplateDefinition texts and tests, red then green | Working tree over `d3fd3ff4`; quality-engineer subagent with `hyhome-validation/bin` on `PATH`; 2026-11-14 | PASS | Red: after the test edits and before any code, schema or registry change, `python3 -m unittest tests.test_common_form_tree tests.test_document_terminal_contract` ran 307 tests with 66 failures and 6 errors (3 skipped); among them `test_typed_form_identifier_matches_the_schema_form_enum` (18 identifiers against 24 expected), `test_schema_role_enum_is_twenty_seven_and_form_enum_is_twenty_four`, the registry form-list tests, and the new `SmallLocalFormTests` cases for the forms, the 12 empty profile lists, the section-id tables and each tree case; the reordered-H2 case failed for five forms and passed for `vocabulary`, the one profile that was ordered. Green: the same modules plus `tests.test_evaluation_document_profiles` ran 315 tests OK (3 skipped). `FormId` in `scripts/document_contracts.py` and the schema `form_id` enum gain the six identifiers after `reference-pack-readme` in role order (18 to 24); the `DocumentRole` and `FormId` comments are corrected. The registry holds six forms with 34 sections, no H3 and no extension, only `Related Documents` and `References` `link_only`, the 12 profiles with empty `required`, `optional` and `forbidden` lists and no `ordered`, and the six twins with nine section-id tables (columns, minimum rows and row identity unchanged) and new non-goal, consumer-path, validation and migration texts; `evaluation/raw-output` keeps its empty lists and no form. | yes | none |
| EVD-007 | [VAL-SMALLFORMS-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Policy texts and unchanged-document proof | Working tree over `d3fd3ff4`, 2026-11-14 | PASS | `.agents/governance/document-authoring.md` (3.22.0) lists the six roles among those that use their registry forms, names their tables by form section id and keeps the sentence that a role without a form keeps its H2 lists for `reference-report`, `governance-document` and `provider-native`; `docs/99.templates/README.md` (0.30.2) now says six roles use their own local forms and the three have none yet. `git diff --stat` over `.agents/knowledge/`, `.agents/prompts/`, `.agents/evaluations/` and `docs/99.templates/templates/` is empty, so the eight documents and six templates are byte-identical. | yes | none |
| EVD-008 | [VAL-SMALLFORMS-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict validators, suites, quality and lint before and after | Working tree over `d3fd3ff4`; outputs saved before and after the change and compared with `diff`; 2026-11-14 | PASS | The four strict validators give identical output before and after: `validate-document-contract-registry` PASS 295 paths (baseline=0 new=295), `validate-markdown-profiles` PASS, `validate-links-and-owners` PASS, `validate-document-lifecycle` PASS. Suites via `run-contract-tests.py`: `document` 688 tests OK (3 skipped), `document-lifecycle` 24, `agent-governance` 105, `validation-routing` 173, `tooling` 166 (includes the knowledge-surface and prompt-input tests), all OK. `validate-affected-surfaces.py` PASS (paths=669 surfaces=42/43 uncovered=0 ambiguous=0). `ruff check scripts tests` clean and `ruff format --check scripts tests` 113 files formatted; `markdownlint-cli2` on the two edited policy files 0 issues; `graphify update .` rc 0. `.secrets.baseline` registry line 8719 moves to 8661 (one line, for its own commit before the implementation, per the Plan); `detect-secrets-hook` over the edited files passes against it. Limitation: `python3 scripts/validation/repository/quality.py --root .` stopped with rc 1 on an ignored untracked file, `.claude/worktrees/agent-a260fbbd5fe4b5005/graphify-out/graph.json` (not a bounded strict UTF-8 regular file), before reaching this change; the staged quality gate and exact-index QA remain with the commit step. | yes | none |
| EVD-009 | [VAL-SMALLFORMS-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Exact-index QA and commit hooks on the implementation commit | Pre-commit hooks over the final index of `abbc1d26` in the pinned validation environment, 2026-11-14 | PASS | The workspace hook ran `scripts/qa.py staged` on the exact index and passed, then commitizen and the generated message check passed; the commit was created. | yes | none |
| EVD-010 | [VAL-SMALLFORMS-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Manual package-exit decision freeze | This package's `spec.md`, `plan.md` and Task; the consumers named below; the user's 2026-11-13 approval of commit, push, PR and merge; Git-history-only method | PASS | The consumer, preservation, hold, authority and method decision is frozen below before this package's final source commit. Each file's committed `commit:path`, retained-ref reachability and byte comparison are recorded in REQ-0003 Archived Lineage before deletion. An unresolved condition defers the affected deletion. | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-SMALLFORMS-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-006 | Accepted by the user on 2026-11-14 (direct answer "Accept both" to the SPEC-0186 criterion question naming commit `abbc1d26`) | platform |
| [VAL-SMALLFORMS-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-007, EVD-008, EVD-009 | Accepted by the user on 2026-11-14 (direct answer "Accept both" to the SPEC-0186 criterion question naming commit `abbc1d26`) | platform |

### Frozen Package Disposition Decision

- **Target and method**: After the final source commit, retire only this Stage 03 package (`spec.md`, `plan.md` and this Task) through Git-history-only recovery. No other document is selected.
- **Consumers and preservation**: The durable contract is promoted to the six local forms in `docs/99.templates/registry.json` and the document authoring forms sentence (Plan Promotion row). Decisions W03-D33 to W03-D36 stay recorded in the SPEC-0161 Task; SPEC-0188 and SPEC-0189 continue W03-H28. Current consumers: the Stage 03 README entry and this Task's `.secrets.baseline` entries, which the closure change removes.
- **Hold and authority**: The current repository documents and the user's request identify no hold on these files. The user's 2026-11-13 approval of commit, push, PR and merge is the disposition authority. If a hold or unmet consumer is identified before deletion, the affected deletion is deferred and its source kept. Remote retention is not inferred from local refs.
- **Proof handoff**: This Task freezes the decision before its final source commit. After that commit, each file's exact `commit:path`, blob availability, reachability from the retained local ref and a byte comparison with the source still in the tree are recorded in REQ-0003 Archived Lineage before any file is deleted.

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (`docs/99.templates/registry.json`, the profile schema form enum, `scripts/document_contracts.py` literals and comments, the named tests, the forms sentences of `.agents/governance/document-authoring.md` and `docs/99.templates/README.md`), this package, `docs/03.specs/README.md`, the W03-D33 to W03-D36 rows, an evidence row and the frontmatter `version` and `updated` of the SPEC-0161 Task (appended rows only), each edited document's `version` and `updated`, `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: the documents and templates of the six roles (form-only, no text change), `reference-report`, `governance-document` and `governance-role`, `provider-native`, `.github/workflows/`, `_workspace/workspace_execution_tasks/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; push, PR and merge are approved by the user's 2026-11-13 request in Inputs
- **Static Validation**: strict document validators, the registry check, the `document`, `document-lifecycle`, `agent-governance` and `tooling` suites, knowledge-surface and prompt-input tests, `ruff check scripts tests`, markdownlint, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). After SPEC-0184 removed the `layer` key, the bytes without that line were reviewed (EVD-004) and approved by the user again (EVD-005); these are the committed bytes. WORK-001 and WORK-002 implemented in the working tree with PASS evidence (EVD-006 to EVD-008); committed in `abbc1d26`. Risk class `medium`. Implementation commit `abbc1d26` passed exact-index QA in the hooks (EVD-009); the user accepted both criteria on 2026-11-14, and the approval of commit, push, PR and merge covers the package exit (EVD-010).
