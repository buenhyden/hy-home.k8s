---
title: "Claude Executable Option Abbreviations"
version: "0.2.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0215-TSK-0001"
parent_ids: ["SPEC-0215-PLAN-0001"]
---

# Task: Claude Executable Option Abbreviations

## Overview

This Task records, for [SPEC-0215](../spec.md) under its [Plan](../plan.md):

- the failing-first and passing results of the five prefix denies, their pin and the decision regressions;
- the document checks and the exact-index QA;
- the criterion decisions.

The implementation is staged and uncommitted. The Spec and Plan are approved (EVD-005 and EVD-006).

## Inputs

- **Request:** the user's answers of 2026-11-14 (Asia/Seoul), quoted verbatim in the Spec's Decisions: "Fix before merge (Recommended)" and "New package, same PR (Recommended)". They approve no Spec bytes, no criterion and no commit, push or merge. Open question: none.
- **Finding:** an automated security review of the SPEC-0214 pull request, relayed by the coordinating session on 2026-11-14. It found that unique long-option abbreviations bypass the exact-name executable-option denies once push is allowed, and rated the gap HIGH.
- **Base:** `83d3f5c1` (SPEC-0214 closed). The four changed files equal the bytes first tested on `da799ae4`, and those files are unchanged between `da799ae4` and `83d3f5c1`.
- **Derivation input (not evidence of record):** the Git 2.43 `--help-all` output of the push, fetch, pull, clone and ls-remote commands, captured in the session scratchpad and not tracked.
  - push: line 22 `--[no-]receive-pack`, line 19 `--[no-]recurse-submodules`, and line 24 `--[no-]exec`; no other push option starts with `e`.
  - fetch: line 12 `--[no-]upload-pack`; `--update-head-ok` and `--update-shallow` share `--up`.
  - pull: line 39 `--[no-]upload-pack`; `--update-shallow` shares `--up`.
  - clone: line 32 `-u, --[no-]upload-pack`.
  - ls-remote: line 6 `--[no-]upload-pack`, line 8 `--[no-]exec`, and line 14 `--[no-]exit-code`.

  No push or fetch was run with these options.
- **Drafting observations (inputs, not evidence of record; the evidence rows below re-run them after approval):**
  - Failing first:
    - The decision test, run in a scratch root that held the edited test module and `HEAD:.claude/settings.json`, exited 1. 12 of 195 expectations failed: exactly the 11 abbreviation deny cases and the `feat/a--edit` over-denial. The three guards passed.
    - With the new pin, and the five settings lines removed with the structured edit tool and then restored (sha256 prefix `57a0576a9c68` before and after), the governance validator exited 1 with `ERR AGENT-NATIVE-PERMISSION`.
    - The same red results were first observed on `da799ae4` with the same file bytes. Since the red run, the validator and test files changed only in comments (the review's wording and wrapping fixes).
  - Passing, with sha256 prefixes `.claude/settings.json` `57a0576a9c68`, `scripts/validate-agent-governance.py` `203247b5ddca` and `tests/test_agent_governance.py` `db6f8c5e8472`:
    - The validator exited 0, and the two unittest modules ran 89 tests, OK.
    - ruff 0.16.10 check was clean and reported `2 files already formatted`.
    - The deny list holds 262 unique rules: the 257 at `HEAD` unchanged and in order, then the five prefix rules.
- **Wave relation:** a direct user request in the SPEC-0214 pull request, outside the SPEC-0161 wave plan. No W03 decision number, no SPEC-0161 row and no residue ledger entry.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-EXECOPT-001](../spec.md#success-criteria--verification-plan) | Write the failing decision regressions and the validator pin, then append the five rules to the settings. | platform | completed | PASS | EVD-007, EVD-008 |
| WORK-002 | [VAL-EXECOPT-002](../spec.md#success-criteria--verification-plan) | Correct the provider-note sentence, add the Stage 03 README entry, and run the document and exact-index checks. | platform | completed | PASS | EVD-009, EVD-010 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-EXECOPT-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Failing-first: decision test on the settings before this change; whole governance validator with the new pin on those settings | Base named in Inputs plus the test and pin edits | NOT_RUN | Pending; the drafting observation is in Inputs | yes | none |
| EVD-002 | [VAL-EXECOPT-001](../spec.md#success-criteria--verification-plan) | WORK-001 | `python3 scripts/validate-agent-governance.py --root .`; `python3 -m unittest tests.test_agent_governance tests.test_validate_agent_registry`; `ruff check` and `ruff format --check` on the two edited Python files | Implementation snapshot | NOT_RUN | Pending; the drafting observation is in Inputs | yes | none |
| EVD-003 | [VAL-EXECOPT-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Four strict document validators; staged lifecycle check; `python3 scripts/validation/repository/quality.py --root .`; `markdownlint-cli2` on the edited Markdown; `git diff --check` and `git diff --cached --check` | Implementation snapshot with this package | NOT_RUN | Pending; the drafting run is in the Verification Summary | yes | none |
| EVD-004 | [VAL-EXECOPT-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Exact-index QA: `python3 scripts/validate-affected-surfaces.py --root .`, `ruff check scripts tests`, `python3 scripts/qa.py staged` and the commit hooks | Exact index at commit time | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-EXECOPT-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"493556b6c153ffe0160b91042b1d80054d56dc8a02c37b41386519ec4b9288e3","plan_sha256":"61e51e1baed8cbc28c67ca16b116dbfb10c3a4e9e0e3d409b9020eed6a877fae"} | PASS | Independent read-only review of these bytes, 2026-11-14: APPROVE; prefix derivation correct against Git 2.43 --help-all for push, fetch, pull, ls-remote and clone; every program option reachable from an allowed command covered; counts 29 allow, 2 ask, 262 deny with the first 257 unchanged; residuals and over-denials recorded honestly; the four NITs (test comments, comment wrap, residual list and recorded checks, README opening clause) applied before these digests. | yes | none |
| EVD-006 | [VAL-EXECOPT-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes (Recommended) to the SPEC-0215 approval question naming spec.md 493556b6 and plan.md 61e51e1b, 2026-11-14","review_ref":"EVD-005","scope":["SPEC-0215","SPEC-0215-PLAN-0001"],"reviewed_spec_sha256":"493556b6c153ffe0160b91042b1d80054d56dc8a02c37b41386519ec4b9288e3","reviewed_plan_sha256":"61e51e1baed8cbc28c67ca16b116dbfb10c3a4e9e0e3d409b9020eed6a877fae","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-007 | [VAL-EXECOPT-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Failing-first: decision test on the settings before this change; whole governance validator with the new pin on those settings | `HEAD` `e3ae23a6` (approved Spec `493556b6`, Plan `61e51e1b`) with the worktree test and pin edits (sha256 prefixes `tests/test_agent_governance.py` `db6f8c5e8472`, `scripts/validate-agent-governance.py` `203247b5ddca`); the decision test ran in a scratch root holding that test module and `HEAD:.claude/settings.json` (257 deny rules); for the validator, the five settings lines were removed with the structured edit tool and then restored (`.claude/settings.json` sha256 prefix `57a0576a9c68` before and after); pinned `hyhome-validation` environment; 2026-11-14T13:12Z | PASS | Red as required. (1) `python3 -m unittest tests.test_agent_governance.NativeDenyCoverageTests.test_delivery_commands_are_allowed_and_raw_api_asks` exit 1, 12 of 195 expectations failed, exactly the 11 abbreviation deny cases (push `--rece=sh`, `--recei sh`, `--e=sh`, `--ex=sh`, `--exe sh`; fetch `--upl=sh`, `--uplo sh`; pull `--upl=sh`; ls-remote `--u=sh`, `--up=sh`, `--exe=sh`) and the `feat/a--edit` over-denial, each decided `allow` or, for pull, the default prompt; the three guards passed. (2) With the settings equal to `HEAD`, `python3 scripts/validate-agent-governance.py --root .` exit 1, `ERR AGENT-NATIVE-PERMISSION agent registry validation failed`. | yes | EVD-001 |
| EVD-008 | [VAL-EXECOPT-001](../spec.md#success-criteria--verification-plan) | WORK-001 | `python3 scripts/validate-agent-governance.py --root .`; `python3 -m unittest tests.test_agent_governance tests.test_validate_agent_registry`; `ruff check` and `ruff format --check` on the two edited Python files | Worktree on `e3ae23a6`; sha256 prefixes `.claude/settings.json` `57a0576a9c68`, `scripts/validate-agent-governance.py` `203247b5ddca`, `tests/test_agent_governance.py` `db6f8c5e8472`; ruff 0.16.10, not the v0.16.5 hook pin; 2026-11-14T13:13Z | PASS | Validator exit 0, `[PASS] agent registry validation passed: providers=2 roles=17 permissionClasses=4 skills=17 handoffs=67 projections=51`; the two modules ran 89 tests, OK; ruff check clean and `2 files already formatted`. The deny list holds 262 unique rules: the 257 at `HEAD` unchanged and in order, then the five prefix rules; allow, ask and the keys outside `permissions` are unchanged. Repository-static only: native rule matching by a Claude client is not observed. | yes | EVD-002 |
| EVD-009 | [VAL-EXECOPT-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Four strict document validators; staged lifecycle check; `python3 scripts/validation/repository/quality.py --root .`; `markdownlint-cli2` on the edited Markdown; `git diff --check` and `git diff --cached --check` | `e3ae23a6` with the four fix files staged by explicit paths (`.claude/provider.md` sha256 prefix `c9f33028e467`), then also this Task; `markdownlint-cli2` v0.23.3, not the v0.22.1 hook pin, over the package's three documents, `docs/03.specs/README.md` and `.claude/provider.md`; 2026-11-14T13:14Z | PASS | The four strict validators exited 0 (contract registry `295 paths`; markdown profiles, links and owners, and lifecycle with no violation); `python3 scripts/validate-document-lifecycle.py --root . --mode staged` exit 0; the repository quality check exit 0, `[PASS] repository quality gates passed`, no ERR line; markdownlint 0 issues in 5 files; `git diff --check` and `git diff --cached --check` clean. | yes | EVD-003 |
| EVD-010 | [VAL-EXECOPT-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Exact-index QA: `python3 scripts/validate-affected-surfaces.py --root .`, `ruff check scripts tests`, `python3 scripts/qa.py staged` and the commit hooks | Pre-commit hooks over the final index of `de8a69ac` in the pinned validation environment: the workspace hook ran `scripts/qa.py staged` (affected-surface routing, selected style including ruff over the staged Python, strict document validators, staged lifecycle, selected non-style hooks) on the exact index, 2026-11-14 | PASS | The workspace hook ran `scripts/qa.py staged` on the exact index and passed, then commitizen and the generated message check passed; the commit was created. | yes | EVD-004 |
| EVD-011 | [VAL-EXECOPT-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Manual package-exit decision freeze | This package's `spec.md`, `plan.md` and Task; the consumers named below; the user's 2026-11-13 approval of commit, push, PR and merge; Git-history-only method | PASS | The consumer, preservation, hold, authority and method decision is frozen below before this package's final source commit. Each file's committed `commit:path`, retained-ref reachability and byte comparison are recorded in REQ-0003 Archived Lineage before deletion. An unresolved condition defers the affected deletion. | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-EXECOPT-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-007, EVD-008 | Accepted by the user on 2026-11-14 (direct answer "Accept (Recommended)" to the SPEC-0215 acceptance question naming commit `de8a69ac`) | platform |
| [VAL-EXECOPT-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-009, EVD-010 | Accepted by the user on 2026-11-14 (direct answer "Accept (Recommended)" to the SPEC-0215 acceptance question naming commit `de8a69ac`) | platform |

### Frozen Package Disposition Decision

- **Target and method**: After the final source commit, retire only this Stage 03 package (`spec.md`, `plan.md` and this Task) through Git-history-only recovery. No other document is selected.
- **Consumers and preservation**: No other document cites this package by path; the settings, the validator pin, the tests and the provider note state the rules on their own. Current consumers: the Stage 03 README entry and this Task's `.secrets.baseline` entries, which the closure change removes.
- **Hold and authority**: The current repository documents and the user's request identify no hold on these files. The user's 2026-11-13 approval of commit, push, PR and merge is the disposition authority. If a hold or unmet consumer is identified before deletion, the affected deletion is deferred and its source kept. Remote retention is not inferred from local refs.
- **Proof handoff**: This Task freezes the decision before its final source commit. After that commit, each file's exact `commit:path`, blob availability, reachability from the retained local ref and a byte comparison with the source still in the tree are recorded in REQ-0003 Archived Lineage before any file is deleted.

## Approval and Safety Boundaries

- **Allowed Paths**: `.claude/settings.json` (`permissions.deny` only), `scripts/validate-agent-governance.py` (`CLAUDE_REQUIRED_DENY_PERMISSIONS` and the comment above `CLAUDE_ASK_PERMISSIONS`), `tests/test_agent_governance.py`, `.claude/provider.md` (the executable-option sentence and frontmatter), this package, `docs/03.specs/README.md`, `.secrets.baseline` (reviewed digest entries only)
- **Forbidden Paths**: `.claude/settings.local.json` and other ignored personal settings, `.codex/`, `.claude/hooks/`, `scripts/provider_write_guard.py`, `scripts/release.py`, `.github/`, `.agents/governance/`, `docs/02.architecture/`, `docs/99.templates/registry.json`, `.agents/roles/registry.json`, the SPEC-0161 package and `docs/03.specs/work-residue-ledger.json`, `docs/98.archive/`
- **Approval Required**: Spec and Plan approval; criterion acceptance; any commit, push, PR or merge.
- **Static Validation**: governance validator, `tests.test_agent_governance` and `tests.test_validate_agent_registry`, the four strict document validators, the staged lifecycle check, `python3 scripts/validation/repository/quality.py --root .`, `python3 scripts/validate-affected-surfaces.py --root .`, `ruff check scripts tests`, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface. Native rule matching by a Claude client is a separate evidence lane and stays unobserved unless recorded.
- **Secret / Vault Handling**: no secret read or printed; the secret-path denies stay
- **Rollback Plan**: revert the implementation commit. The five rules, the pin lines, the regressions and the provider-note sentence leave together.
- **Evidence Location**: this Task

## Verification Summary

Risk class `high` (permission change). The Spec and Plan are approved: EVD-005 records the review and EVD-006 the user's approval of spec.md `493556b6` and plan.md `61e51e1b`.

Evidence was re-run after approval:

- EVD-007 resolves EVD-001: red as required.
- EVD-008 resolves EVD-002: the validator, the unittest modules and ruff pass.
- EVD-009 resolves EVD-003: the document checks pass.

EVD-004, the exact-index QA, stays NOT_RUN until the commit hooks run on the exact index. The implementation is staged and not committed. Native rule matching is unobserved.

Core-diff checklist of changed permissions:

- Added to the deny list (5 rules): `--receive-pack` from `--rece` on, push `--exec` from `--e` on, `--upload-pack` from `--upl` on, ls-remote `--upload-pack` from `--u` on and ls-remote `--exec` from `--exe` on.
- Unchanged: every other allow, ask and deny rule.

Residual risk: a receive-pack or upload-pack program set in configuration, and a quoted or variable option, stay uncovered, as the Spec records.

Open question: none. Next owner:

1. the reviewer and the user, for the Spec and Plan review and approval;
2. platform, for the exact-index QA and the commit hooks;
3. the operator, for criterion acceptance. Implementation commit `de8a69ac` passed exact-index QA in the hooks (EVD-010); the user accepted the package on 2026-11-14, and the approval of commit, push, PR and merge covers the package exit (EVD-011).
