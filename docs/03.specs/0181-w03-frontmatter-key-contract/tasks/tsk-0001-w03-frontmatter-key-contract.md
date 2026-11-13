---
title: "W03 Frontmatter Key Contract"
version: "0.3.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0181-TSK-0001"
parent_ids: ["SPEC-0181-PLAN-0001"]
---

# Task: W03 Frontmatter Key Contract

## Overview

This Task records handoffs W03-H07, W03-H14 and W03-H17 and two conformance-audit corrections for [SPEC-0181](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items, to investigate remaining, unverified, unreviewed, unconfirmed, unstarted, conflicting and missing items, to review whether anything was decided or built differently from the W00 to W03 requirements and fix it to them, to present decisions with options, to check existing work first, to do now anything due before W03, to start work that can run in parallel, and approved commit, push, PR and merge in that same request. The request approves no Spec bytes or criterion.
- **Base:** branch `claude/w03-frontmatter-keys` from `2842579e` (`main` merge of PR #245); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W03-D05, W03-D22, W03-D23 and EVD-018 (current v14.7 requirements prevail).
- **Decisions recorded with this package:** the user's direct 2026-11-13 answers W03-D25 (adopt the GOV-06 machine ledger), W03-D26 (build local forms for the nine local roles), W03-D27 (move `sdlc.md` to the Policy role and add rule IDs), W03-D28 (keep CI-SCOPE staged for W06), W03-D29 (move the YAML loaders to YAML 1.2.2), W03-D30 (Q-07 renumbering only after all `docs/` work, with the current numbering kept until then) and W03-D31 (keep accurate pointer lines); the follow-up handoff rows; the 2026-11-13 conformance-audit rows.
- **Requirement basis:** the W03 task's metadata table, W03-A, line 18 (extension conditions) and the TemplateDefinition contract; read-only inputs under `_workspace/workspace_execution_tasks/`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-KEYS-001](../spec.md#success-criteria--verification-plan) | Authority admission, key entries, dialect, key-table projection, Codex twin, registry checks and tests. | platform | completed | PASS | EVD-004 |
| WORK-002 | [VAL-KEYS-002](../spec.md#success-criteria--verification-plan) | Extension texts; policy texts; regression and exact-index QA. | platform | completed | PASS | EVD-005, EVD-006, EVD-007; implementation commit `6d8624a1` passed exact-index QA and the hooks |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-KEYS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `997fa118…`, plan.md `daa6ec08…`, with simulations in a scratch copy of the tree; 2026-11-13 | FAIL | REJECT: BLOCK the registry authority guard refuses new top-level sections, so `scripts/document_authority.py` must be in scope; BLOCK the full TemplateDefinition record cannot validate without invented heading content for the form-less and provider-native templates, and the six SDLC templates were unaddressed; BLOCK the WGOV-CORE count is seven, a binding test pins `unverified`, and `scope`, `migration` and `rollback` have no source. FIXes on the TOML twin (feasible), key tests, the four loaders, follow-up handoff rows and the policy paragraphs; NITs on risk scoring, the Task, native allowed values and the approval citation. | no | none |
| EVD-002 | [VAL-KEYS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"8941ea5b7122b9bfd6ec4e91b26fcc651730162473c01231a4d450547c59776b","plan_sha256":"f258872826f29f16a29feb6517ace22df773bccc84059008acd07bc656b00ca9"} | PASS | Same reviewer, rounds 2 and 3, 2026-11-13: every round-1 finding verified fixed, with W03-H15 handed to the local-forms package and phase 3 and the extension texts left for the user's acceptance; round 3 confirmed by diff that only four requested edits changed; verdict APPROVE. The acceptance question must show the actual extension texts, and VAL-KEYS-002 is not met by the Spec's approval alone. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-KEYS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0181 approval question naming spec.md 8941ea5b and plan.md f2588728 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0181","SPEC-0181-PLAN-0001"],"reviewed_spec_sha256":"8941ea5b7122b9bfd6ec4e91b26fcc651730162473c01231a4d450547c59776b","reviewed_plan_sha256":"f258872826f29f16a29feb6517ace22df773bccc84059008acd07bc656b00ca9","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion and no extension text. | yes | none |
| EVD-004 | [VAL-KEYS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Authority admission, key entries, dialect, key table, Codex twin, registry checks and tests, red then green | Working tree over `e6ec3d3f`; implementer quality-engineer subagent, staged and re-checked by the author with `hyhome.validationVenv/bin` on `PATH`; 2026-11-13 | PASS | Red (implementer log `scratchpad/red81/key.txt`): the new `tests/test_frontmatter_key_contract.py` 49 tests with 28 errors before the code; `tests/test_shared_contract_binding.py` 1 failure and `tests/test_common_form_tree.py` 2 failures and 2 errors before. Green: all pass. `frontmatter_keys` holds 22 entries with condition, consumers and both tests; 36 key tests were added (22 accepted, 14 refused) and the rest reuse existing tests; `frontmatter_key_table` derives the 14 columns; the registry checks run in `current_registry_diagnostics` from the strict registry validator, so a comparison-base registry without the sections still loads; `frontmatter_dialect` records YAML 1.1 through PyYAML 6 with target YAML 1.2.2 unasserted; the Codex twin `common/template-exception-provider-native-codex` and its source are `provider-native`. Deviations from the Spec text, each the observed fact: five frontmatter loaders, not four (the fifth, `scripts/validation/repository/quality.py`, reads Hookify local-rule frontmatter); `scripts/document_lifecycle.py` resolves timestamps rather than removing the resolver, and a test checks each recorded loader against the loader itself; `scripts/validation/registry.json` gained one exact route for the new test module, which the pre-edit hook required; `argument-hint` and `allowed-tools` are read through the profile check's key lists and `supersedes` and `superseded_by` only by the profile check; `_UniqueKeySafeLoader` in `scripts/document_contracts.py` is unused and left in place. | yes | none |
| EVD-005 | [VAL-KEYS-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Extension texts and policy texts | Staged diff over `3dceace4` | PASS | The seven WGOV-CORE extensions hold a stated condition, owner `buenhyden` (the recorded `shared_contract.owner`), and verification, review and removal texts, listed in the acceptance question; `approved_by`, `approved_at`, `effective_from`, `scope`, `migration` and `rollback` stay `unverified`; the registry check refuses `unverified` in an extension field and the binding test pins the new values. `document-authoring.md` 3.18.0 drops the stale Policy clause and names `frontmatter_keys` and `frontmatter_dialect`; `docs/99.templates/README.md` 0.30.0 adds one Korean sentence. | yes | none |
| EVD-006 | [VAL-KEYS-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Regression over the tree, suites and lint | Author run over the staged index after `3dceace4`, 2026-11-13 | PASS | The four strict document validators give output byte-identical to the before run at `e6ec3d3f`. Staged lifecycle PASS; `python3 scripts/qa.py staged` 19 gates PASS or reused. Suites (implementer): `document` 635 (3 skipped), `document-lifecycle` 24, `agent-governance` 105, `validation-routing` 173, `tooling` 166 OK; `quality.py` and `validate-affected-surfaces` PASS; `ruff check` and `ruff format --check` clean; markdownlint 0 issues; `graphify update .` rc 0. `.secrets.baseline` registry line 8730 moved to 8809 in `3dceace4`. | yes | none |
| EVD-007 | [VAL-KEYS-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Semantic review: risk class and core-diff checklist | Diff of 12 files over `3dceace4` | PASS | Risk class `medium` (registry, schema, authority guard, registry checks, tests and two policy texts). Checklist: scope matches the Spec apart from the routing entry in EVD-004; one writer per file; W03-H07, W03-H14 and W03-H17 applied, W03-H15 handed on; no document or template body changed; approval facts stay `unverified`; the ignored read-only contract input was read only; no secret read; recovery is reverting the implementation commit. No permission, trigger, hook or workflow file changed. | yes | none |
| EVD-008 | [VAL-KEYS-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Manual package-exit decision freeze | This package's `spec.md`, `plan.md` and Task; the consumers named below; the user's 2026-11-13 approval of commit, push, PR and merge; Git-history-only method | PASS | The consumer, preservation, hold, authority and method decision is frozen below before this package's final source commit. Each file's committed `commit:path`, retained-ref reachability, temporary restoration and byte comparison are recorded in REQ-0003 Archived Lineage before deletion. An unresolved condition defers the affected deletion. | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-KEYS-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-004 | Accepted by the user on 2026-11-13 (direct answer "Accept both" to the SPEC-0181 criterion question naming implementation commit `6d8624a1` and listing the seven extension texts) | platform |
| [VAL-KEYS-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-005, EVD-006, EVD-007 | Accepted by the user on 2026-11-13 (direct answer "Accept both" to the SPEC-0181 criterion question naming implementation commit `6d8624a1` and listing the seven extension texts) | platform |

### Frozen Package Disposition Decision

- **Target and method**: After the final source commit, retire only this Stage 03 package (`spec.md`, `plan.md` and this Task) through Git-history-only recovery. No other document is selected.
- **Consumers and preservation**: The durable contract is promoted to the document authoring policy and the registry (Plan Promotion row). The follow-up handoffs W03-H25 to W03-H32 stay in the SPEC-0161 Task. Current consumers: the Stage 03 README entry and this Task's `.secrets.baseline` entries, which the closure change removes. Registry text, code comments and test docstrings that name SPEC-0181 use it as an identifier, not a link, and stay.
- **Hold and authority**: The current repository documents and the user's request identify no hold on these files. The user's 2026-11-13 approval of commit, push, PR and merge is the disposition authority. If a hold or unmet consumer is identified before deletion, the affected deletion is deferred and its source kept. Remote retention is not inferred from local refs.
- **Proof handoff**: This Task freezes the decision before its final source commit. After that commit, each file's exact `commit:path`, blob availability, reachability from the retained local ref and a temporary byte comparison with the source still in the tree are recorded in REQ-0003 Archived Lineage before any file is deleted. This Task cannot contain that proof without changing its own bytes.

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, the W03-D25 to W03-D31, handoff, conformance-audit and evidence rows and the frontmatter `version` and `updated` of the completed SPEC-0161 Task (appended rows only), `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: every document and template body other than the two policy texts, `_workspace/workspace_execution_tasks/`, `.github/`, `.claude/`, `.codex/`, hooks, accepted ADR bodies, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance with the extension texts; push, PR and merge are approved by the user's 2026-11-13 request in Inputs
- **Static Validation**: strict document validators, `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, repository quality gate, markdownlint, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). WORK-001 and WORK-002 implemented with PASS evidence (EVD-004 to EVD-007); implementation commit `6d8624a1`. The user accepted both criteria with the seven extension texts on 2026-11-13, and the approval of commit, push and PR covers the package exit (EVD-008). Risk class `medium`. Next owner: W03 for SPEC-0182.
