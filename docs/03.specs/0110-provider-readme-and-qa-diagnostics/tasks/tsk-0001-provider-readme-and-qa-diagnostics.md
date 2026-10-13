---
title: "Provider README Language and QA Tool Diagnostics"
version: "1.0.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0110-TSK-0001"
parent_ids: ["SPEC-0110-PLAN-0001"]
---

# Task: Provider README Language and QA Tool Diagnostics

## Overview

Execute the three work units of the [Plan](../plan.md) for
[SPEC-0110](../spec.md) and record their evidence here.

## Inputs

- [SPEC-0110](../spec.md) and its [Plan](../plan.md).
- Operator instruction on 2026-10-13: approve SPEC-0108 and continue with
  the README translations, the SPEC-0109 review and K-P0, K-P3, K-P4 and
  K-P5.
- Branch head `c59940d8` before this package.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-PRQA-001](../spec.md#success-criteria--verification-plan) | Translate the eight pending READMEs | platform | completed | PASS | EVD-004 in commits `4860b64db1c7226690dd7f717319a35c52a1e275` and `4df73c2671a57ce73ee6e5b1924e95fb40f39f2c` |
| WORK-002 | [VAL-PRQA-002](../spec.md#success-criteria--verification-plan) | Missing-tool diagnostics and README sentence | platform | completed | PASS | EVD-005, EVD-006 in commit `af5d11b7cfe7e43eb2dd345b03ff425a85e01d07` |
| WORK-003 | [VAL-PRQA-003](../spec.md#success-criteria--verification-plan) | Record keep decisions for satisfied findings | platform | completed | PASS | EVD-007 and EVD-008 in this Task |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-PRQA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Profile validator and staged QA | WORK-001 commit index | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-PRQA-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Focused tests and staged QA | WORK-002 commit index | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-PRQA-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Keep-decision source review | Current source lines named in the evidence | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-PRQA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Profile validator and staged QA | Eight README bodies translated with headings, links and identifiers kept; `pending_paths` emptied. The Registry line shift needed the secret-scan baseline moved first in its own commit because the nonstyle gate reads the HEAD baseline. `scripts/validate-markdown-profiles.py` PASS; `qa.py staged` from the validation environment passed all 11 selected gates for `4df73c2671a57ce73ee6e5b1924e95fb40f39f2c` | PASS | This Task; commits `4860b64db1c7226690dd7f717319a35c52a1e275` and `4df73c2671a57ce73ee6e5b1924e95fb40f39f2c` | yes | EVD-001 |
| EVD-005 | [VAL-PRQA-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Focused tests and staged QA | New tool, hook-line and rule-label tests failed before repair (3 errors, 2 failures) and 110 tests passed after in the validation environment. Under the system interpreter, three existing nonstyle tests now fail with `NONSTYLE-TOOL`: before this change they reported `NONSTYLE-HOOK-FAIL` only because `pre_commit` was absent. Staged QA showed `rule=STYLE-FORMAT-MUTATION` on an unformatted draft and then passed all 15 selected gates | PASS | This Task; commit `af5d11b7cfe7e43eb2dd345b03ff425a85e01d07` | yes | EVD-002 |
| EVD-006 | [VAL-PRQA-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Independent read-only security review | A security-auditor subagent found no Critical, High or Medium issue. L2 (unbounded rule token on any lane) was fixed by bounding segments with a failing-then-passing test; L1 (a hook may echo a line shaped like `- hook id:` from author-controlled content, restricted to `[a-z0-9-]` and digits) is accepted | PASS | This Task; commit `af5d11b7cfe7e43eb2dd345b03ff425a85e01d07` | yes | none |
| EVD-007 | [VAL-PRQA-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Keep-decision source review | Read-only review of current files: F05 `docs/99.templates/README.md` separates the `WGOV-CORE / 3.0.0` approval reference from the local `candidate` stage; F39 `.agents/governance/quality.md` separates the retired full/ci sweep, ordinary document selection, local purpose versus hosted style and technical timeout versus business timebox; F18 `.github/repository-surface.md` names labeler and greetings maintenance only; F22 formatters run in a private copy where any byte change fails as `STYLE-FORMAT-MUTATION`; F02 `AGENTS.md` is the registered Codex gateway and Claude never reads it. No change | PASS | Current source at `af5d11b7cfe7e43eb2dd345b03ff425a85e01d07` | yes | EVD-003 |
| EVD-008 | [VAL-PRQA-003](../spec.md#success-criteria--verification-plan) | WORK-003 | F21 hosted style trigger decision | `.github/workflows/ci.yml` runs `style-pr` on `edited`; a job-level skip on title-only edits would publish a `skipped` required check that GitHub treats as satisfied and could mask an earlier failure, and `cancel-in-progress` could drop the real result. Kept unchanged; splitting the title check into its own required workflow needs a remote ruleset change by the operator | PASS | `.github/workflows/ci.yml`, `.github/rulesets/main-protection.md` at `af5d11b7cfe7e43eb2dd345b03ff425a85e01d07` | no | none |
| EVD-009 | [VAL-PRQA-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Branch-wide style gate | The validation environment's selected style gate rejected three Python files from SPEC-0108 commit `9cadabdd` that an earlier `~/.local` pre-commit run had reported as passing, and a Markdown MD038 issue in this Spec; both were fixed before or by commit `06045ad5e1a185b997f39bf99a76ed0388d52981`, after which all 29 branch-changed files passed `STYLE-PASS` | PASS | This Task; commit `06045ad5e1a185b997f39bf99a76ed0388d52981` | no | none |
| EVD-010 | [VAL-PRQA-003](../spec.md#success-criteria--verification-plan) | WORK-003 | F21 operator decision | On 2026-10-13 the operator chose to keep `style-pr` on the `edited` trigger (option A) after reviewing four options: keep; split the title check into its own required workflow with a ruleset change; skip on title-only edits (rejected: GitHub reports a skipped required job as Success); reuse an earlier result (rejected). Measured PR CI runs took 19 to 34 seconds | PASS | This Task; `.github/workflows/ci.yml` unchanged | no | none |
| EVD-011 | [VAL-PRQA-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Hosted PR checks | PR #140 at head `b81a095ef2f1bd5dc0958ce222ea120ef5a79bf8`: `ci-summary`, `style-pr`, `greeting`, `label` and GitGuardian completed SUCCESS on 2026-10-13. Later branch commits need their own hosted run | PASS | PR #140 checks | no | none |
| EVD-012 | [VAL-PRQA-002](../spec.md#success-criteria--verification-plan) | WORK-002 | CI contract after main integration | Merging main brought Dependabot #139 (`actions/checkout` v7.0.1, `3d3c42e5aac5ba805825da76410c181273ba90b1`, verified against the upstream tag). `scripts/validate-ci-python-contract.py` then failed `CI-STYLE-TOPOLOGY` on main as well, because hosted CI does not run this local contract. Commit `2bc0dc89` updated the pinned action; the contract and its 1 test module passed and staged QA returned rc 0 | PASS | This Task; commit `2bc0dc89459cac5ac7e54a0825b985c5a299dc5e` | no | none |
| EVD-013 | [VAL-PRQA-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Correction of hosted evidence scope | Correction recorded by SPEC-0113 on 2026-10-13: EVD-011 listed `greeting` and `label` beside the hosted checks. Those are notification and metadata automation (`.github/workflows/greetings.yml`, `labeler.yml`), and their success is not QA evidence for any criterion. The hosted style and summary results are `style-pr` and `ci-summary`, and local `qa.py staged` stays the purpose QA. EVD-011 is kept as history | PASS | This Task; [SPEC-0113](../../0113-sdlc-sync-and-v9-gaps/spec.md) | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-PRQA-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-004 | Accept the Korean README bodies and empty pending list | platform |
| [VAL-PRQA-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-005, EVD-006 | Accept the explicit tool and hook diagnostics; L1 accepted as low residual risk | platform |
| [VAL-PRQA-003](../spec.md#success-criteria--verification-plan) | accepted | EVD-007 | Accept the keep decisions; the operator kept F21 unchanged (EVD-010) | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, `docs/03.specs/README.md`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`
  (reciprocal links), the eight READMEs, `docs/99.templates/registry.json`,
  `.secrets.baseline`, `scripts/validate-selected-{style,nonstyle}.py`,
  `scripts/run-validation-lane.py`, `scripts/README.md` and their tests.
- **Forbidden Paths**: `.github/` workflows and rulesets, frozen Archive
  payloads, other Spec packages, live cluster, Vault and secret material.
- **Approval Required**: the operator directed this follow-up on
  2026-10-13 and approved SPEC-0110 and its Plan after reviewing the result
  at `8b56cb82`; push, pull request, merge and any ruleset change await the
  operator.
- **Static Validation**: focused tests, the profile validator and staged QA
  from the documented validation environment.
- **Live Validation**: DEFER — no live surface is touched; hosted CI is not
  observed.
- **Secret / Vault Handling**: no secret is read or printed.
- **Rollback Plan**: forward revert of the package commits.
- **Evidence Location**: this Task and Git history.

## Verification Summary

All three work units are complete. Every commit in this package passed
`qa.py staged` from the documented validation environment, including the
selected style and nonstyle gates that the system interpreter cannot run.
Two independent reviews covered the riskiest code (SPEC-0108 status reader,
this package's diagnostics). Limitations: hosted CI, push and pull request
are not executed; under the system interpreter the style tests fail
explicitly with `NONSTYLE-TOOL`. Next owner: the operator for SPEC-0110
approval, the F21 ruleset alternative, push and pull request; platform for
SPEC-0109 once approved.
