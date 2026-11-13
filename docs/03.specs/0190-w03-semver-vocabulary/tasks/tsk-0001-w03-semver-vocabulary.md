---
title: "W03 SemVer Vocabulary and Version Fields"
version: "0.3.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
artifact_id: "SPEC-0190-TSK-0001"
parent_ids: ["SPEC-0190-PLAN-0001"]
---

# Task: W03 SemVer Vocabulary and Version Fields

## Overview

This Task records the SemVer delta of the v14.7 2026-11-13 revision of the W03 task for [SPEC-0190](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to review the remaining W03 items against the current requirements, to fix anything decided or built differently from the requirements up to W03, to follow the requirements when a choice is needed, to start work that can run in parallel, and approved commit, push, PR and merge. The request approves no Spec bytes or criterion.
- **Base:** branch `claude/w03-semver-vocabulary` from `8231f782` (`main` after PR #250, SPEC-0185).
- **Decisions recorded with this package:** W03-D45 (the eight glossary terms are common rows at `repository-vocabulary v14.7`; user answer "Common, v14.7 (Recommended)") and W03-D46 (the `adopted` contract-version guard keeps the numeric core of the same grammar, and the validation surface registry and `tests/test_frontmatter_key_contract.py` are edited as consumers; user answer "Accept both (Recommended)"), both 2026-11-13.
- **Source:** the revision's `dependencies/contracts/SEMVER-POLICY.md` and `SEMVER-CASES.json` (read-only input; not copied into the repository).

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SEMVER-001](../spec.md#success-criteria--verification-plan) | Module, release tag pattern, skill envelope check, schema patterns and tests. | platform | completed | PASS | EVD-006, EVD-007 |
| WORK-002 | [VAL-SEMVER-002](../spec.md#success-criteria--verification-plan) | Glossary terms, version paragraph, scripts README; regression and exact-index QA. | platform | completed | PASS | EVD-008, EVD-009 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-SEMVER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only reviewer that wrote none of the package, over spec.md `7dd10cb7…` and plan.md `ca951bf8…`; 2026-11-13 | FAIL | REJECT: FIX 1, `document-profile.schema.json` has three contract `version` patterns (lines 48, 163, 845), not two; FIX 2, new tests are not run unless registered in a suite, and the `release` suite was missing; FIX 3, the glossary edition `repository-vocabulary v14.7` had no recorded decision and the Korean cells were not named. NITs on capture groups, anchors, precedence cases and the module name. Round 2 confirmed the three fixes and found one more (the Open question sentence); round 3 approved. | no | none |
| EVD-002 | [VAL-SEMVER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"a88a04e8903de04e2591adb43a13922266ada92b9ebfb4141e2cd8fc3f7d5203","plan_sha256":"36a48a841d0daf8650585936e65ef07a14e1625cb729bba6f0785ef64a688590"} | PASS | Same reviewer, rounds 2 and 3, 2026-11-13: the three FIX items of EVD-001 and the round-2 FIX (Open question sentence) and NITs are applied; round 3 APPROVE over the bytes named here. This row records a review, not an approval. | yes | none |
| EVD-003 | [VAL-SEMVER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0190 approval question naming spec.md a88a04e8 and plan.md 36a48a84 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0190","SPEC-0190-PLAN-0001"],"reviewed_spec_sha256":"a88a04e8903de04e2591adb43a13922266ada92b9ebfb4141e2cd8fc3f7d5203","reviewed_plan_sha256":"36a48a841d0daf8650585936e65ef07a14e1625cb729bba6f0785ef64a688590","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-004 | [VAL-SEMVER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"479777c2e3f04d47d4e20cad42b63ca28d2dff56ea842991a4a245714140d265","plan_sha256":"36a48a841d0daf8650585936e65ef07a14e1625cb729bba6f0785ef64a688590"} | PASS | Same reviewer, 2026-11-13: the package commit over the EVD-003 bytes was refused by `LANG-ENGLISH-FIRST` (spec.md Glossary bullet with bare Korean term names); the fix wraps the eight Korean names in code spans, and a character diff shows those 16 backticks as the only change. APPROVE over the bytes named here; this row records a review, not an approval. | yes | none |
| EVD-005 | [VAL-SEMVER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0190 re-approval question naming spec.md 479777c2 and plan.md 36a48a84 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-004","scope":["SPEC-0190","SPEC-0190-PLAN-0001"],"reviewed_spec_sha256":"479777c2e3f04d47d4e20cad42b63ca28d2dff56ea842991a4a245714140d265","reviewed_plan_sha256":"36a48a841d0daf8650585936e65ef07a14e1625cb729bba6f0785ef64a688590","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-006 | [VAL-SEMVER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | SemVer grammar module, consumers and case tests, red then green | Implementer quality-engineer subagent in an isolated worktree over `c54eed50`, applied by the author over `84f3891a` with a 3-way merge (only the `document-authoring.md` version line conflicted; 3.20.2 raised to 3.21.0); pinned validation environment; 2026-11-13 | PASS | Red: with `scripts/semver_grammar.py` present and the old consumers, `tests.test_semver_grammar` failed (failures=31, errors=3): the four schema pin tests, 24 schema accept/refuse cases and the skill envelope case. Green: `tests.test_semver_grammar` with `tests.test_release` ran 28 tests OK. `release.py` builds `v` + `SEMVER_PATTERN` + `\Z` and `tests/test_release.py` is unchanged; the skill envelope check uses `re.fullmatch`; the frontmatter schema and the `shared_contract` and `common_forms` patterns equal `^` + `SEMVER_PATTERN` + `$`. | yes | none |
| EVD-007 | [VAL-SEMVER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | W03-D46 deviations applied | Same diff | PASS | The `adopted` contract-version guard of `document-profile.schema.json` is `^` + the numeric core of `SEMVER_PATTERN` + `$`, so `3.0.0-draft.3` and `01.2.3` stay refused there (`test_shared_contract_binding` passes); the pin test expects full, full and core for the three profile patterns. `scripts/validation/registry.json` registers the new module and test in the document-reader surface and, after exact-index QA first refused `SURFACE-PATH-AMBIGUOUS` on the module, adds it to the exclusion list of the generic `scripts` surface beside `frontmatter_yaml.py`, as SPEC-0183 did (`validate-affected-surfaces.py` uncovered=0, ambiguous=0); `tests/test_frontmatter_key_contract.py` asserts `SEMVER_PATTERN` instead of the old `[0-9]+` pattern. | yes | none |
| EVD-008 | [VAL-SEMVER-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Glossary terms, version paragraph, scripts README; regression | Same diff; pinned validation environment, 2026-11-13 | PASS | `.agents/knowledge/glossary.md` 1.2.0 gains TERM-PUBLIC-CONTRACT, TERM-COMPATIBILITY, TERM-CONTRACT-VERSION, TERM-REGISTRY-SCHEMA-VERSION, TERM-DOCUMENT-REVISION, TERM-PRERELEASE, TERM-BUILD-METADATA and TERM-BASELINE-NAMESPACE at `repository-vocabulary v14.7` (W03-D45), no existing row changed; `document-authoring.md` 3.21.0 adds the version sentences; `scripts/README.md` 0.15.0. The four strict document validators equal their before output; suites `document` 674, `agent-governance` 105, `release` 29, `tooling` 166 OK; `validate-knowledge-surface.py` PASS; `ruff check` and `ruff format --check` clean; all 205 Markdown `version` values match the grammar; `graphify update .` done. The glossary Maintenance sentence on editions is unchanged; mixed v14.5 and v14.7 rows follow W03-D45. | yes | none |
| EVD-009 | [VAL-SEMVER-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Exact-index QA and commit hooks on the implementation commit | Pre-commit hooks over the final index of `9f016de1` in the pinned validation environment, 2026-11-14 | PASS | The workspace hook ran `scripts/qa.py staged` on the exact index and passed, then commitizen and the generated message check passed; the commit was created. | yes | none |
| EVD-010 | [VAL-SEMVER-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Manual package-exit decision freeze | This package's `spec.md`, `plan.md` and Task; the consumers named below; the user's 2026-11-13 approval of commit, push, PR and merge; Git-history-only method | PASS | The consumer, preservation, hold, authority and method decision is frozen below before this package's final source commit. Each file's committed `commit:path`, retained-ref reachability and byte comparison are recorded in REQ-0003 Archived Lineage before deletion. An unresolved condition defers the affected deletion. | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-SEMVER-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-006, EVD-007 | Accepted by the user on 2026-11-14 (direct answer "Accept both" to the SPEC-0190 criterion question naming commit `9f016de1`) | platform |
| [VAL-SEMVER-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-008, EVD-009 | Accepted by the user on 2026-11-14 (direct answer "Accept both" to the SPEC-0190 criterion question naming commit `9f016de1`) | platform |

### Frozen Package Disposition Decision

- **Target and method**: After the final source commit, retire only this Stage 03 package (`spec.md`, `plan.md` and this Task) through Git-history-only recovery. No other document is selected.
- **Consumers and preservation**: The durable contract is promoted to the document authoring policy version paragraph, `scripts/semver_grammar.py` and the glossary rows (Plan Promotion rows). No new handoff arises. Current consumers: the Stage 03 README entry and this Task's `.secrets.baseline` entries, which the closure change removes. Code and test comments that name SPEC-0190 use it as an identifier, not a link, and stay.
- **Hold and authority**: The current repository documents and the user's request identify no hold on these files. The user's 2026-11-13 approval of commit, push, PR and merge is the disposition authority. If a hold or unmet consumer is identified before deletion, the affected deletion is deferred and its source kept. Remote retention is not inferred from local refs.
- **Proof handoff**: This Task freezes the decision before its final source commit. After that commit, each file's exact `commit:path`, blob availability, reachability from the retained local ref and a byte comparison with the source still in the tree are recorded in REQ-0003 Archived Lineage before any file is deleted.

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: existing version values, existing glossary rows, `.github/workflows/`, `_workspace/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; push, PR and merge are approved by the user's 2026-11-13 request in Inputs
- **Static Validation**: strict document validators, the `document`, `agent-governance`, `release` and `tooling` suites, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001 FAIL, EVD-002 PASS) and approved by the user at their exact bytes (EVD-003); after the package commit was refused for bare Korean text, the code-span fix was reviewed (EVD-004) and approved again (EVD-005), and these are the committed bytes. The implementation is applied with PASS evidence (EVD-006 to EVD-008), including the W03-D46 deviations; implementation commit `9f016de1` passed exact-index QA in the hooks (EVD-009). The user accepted both criteria on 2026-11-14, and the approval of commit, push, PR and merge covers the package exit (EVD-010). Risk class `low`. Risk class `low`.
