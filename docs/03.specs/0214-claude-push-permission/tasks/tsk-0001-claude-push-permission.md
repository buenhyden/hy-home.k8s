---
title: "Claude Delivery Permissions and CI/CD Governance"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0214-TSK-0001"
parent_ids: ["SPEC-0214-PLAN-0001"]
---

# Task: Claude Delivery Permissions and CI/CD Governance

## Overview

This Task records, for [SPEC-0214](../spec.md) under its [Plan](../plan.md):

- the failing-first and passing results of the permission pin and the decision regressions;
- the document and exact-index checks;
- the criterion decisions.

WORK-001 and WORK-002 are implemented in the worktree and uncommitted; the exact-index QA, the commit hooks and the criterion decisions are still open.

## Inputs

- **Request:** the user's successive wordings and answers of 2026-11-14 (Asia/Seoul), quoted verbatim in the Spec's Decisions. That includes the answers "Lift create/run denies", "Allow" and "Leave .codex unchanged (Recommended)". The request approves no Spec bytes, no criterion and no commit, push or merge. Scope change of 2026-11-14: the coordinating session relayed the user's approval to reword, with the same meaning, the Spec and Plan lines that the repository quality check reads as push examples, and to bring runbook 0012 Step 5 and the `release.py` row of `scripts/README.md` into scope; this records the request and is not an approval receipt, and the re-approval of the changed bytes is pending. Open question: none.
- **Base:** set at commit time; the Spec was drafted against `main` `511e106f`.
- **Drafting observations (inputs, not evidence of record):**
  - `push.default` is `current` in this clone, observed 2026-11-14.
  - A scratch probe of the final lists under the repository matcher model gave 29 allow and 2 ask rules, and 236 deny rules before the two hook-bypass rules (238 with them), with the decisions the Spec lists. The hook-bypass cases were checked by reading the model, because a local plugin hook refuses shell lines that carry them.
  - Dry runs of Git 2.43 against a scratch bare remote showed `--de`, `--m`, `--mi`, `--pru`, `--al`, `--b`, `--force-w`, `-uf` and `-ud` acting as the full options, `@` resolving to `refs/heads/main`, and `--d`, `--pr` and `--for` refused as ambiguous. A follow-up dry run was denied by the session's permission check and was not retried.
  - The hosted `main` protection read-back of 2026-11-11T23:46Z is in SPEC-0161 Task lines 230 and 235.
- **Wave relation:** a direct user request outside the SPEC-0161 wave plan. No W03 decision number, no SPEC-0161 row and no residue ledger entry.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-DELIVERYPERM-001](../spec.md#success-criteria--verification-plan) | Write the failing regressions and the validator pin, then the settings lists. | platform | draft | NOT_RUN | Pending |
| WORK-002 | [VAL-DELIVERYPERM-002](../spec.md#success-criteria--verification-plan) | Amend the git.md release text and add its delivery subsection; replace the Claude provider note lines and the Codex parity sentence; amend the runbook 0012 executor lines; add the Stage 03 README entry; run the document and exact-index checks. | platform | draft | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-DELIVERYPERM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Failing-first: decision and mutation tests on the old settings; whole governance validator with the new pin on the old settings | Base named in Inputs plus the test and pin edits | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-DELIVERYPERM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | `python3 scripts/validate-agent-governance.py --root .`; `python3 -m unittest tests.test_agent_governance tests.test_validate_agent_registry`; `agent-governance` suite | Implementation snapshot | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-DELIVERYPERM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Four strict document validators before and after; staged lifecycle check; affected-surface routing; ruff; `python3 scripts/qa.py staged` and the commit hooks | Exact index | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-DELIVERYPERM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Optional read-only read-back of `main` protection and tag rulesets through `gh api` (asks natively) | Remote state at the read time | NOT_RUN | Pending; DEFER to the operator if not approved | no | none |
| EVD-005 | [VAL-DELIVERYPERM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"c95b02fe245366ed9fa53325d367df8f2a9182511b6ef4988ba1865b9ad6bfe1","plan_sha256":"c6510ccfdf72305d87d298b46a811efdf151e29bc1ac727c9bacba60b027bf49"} | PASS | Independent review by the security-auditor role: round 1 APPROVE WITH FIXES (B1 abbreviated and clustered options, F1 heads/main, F2 implicit destinations, F3 residual code execution and gh pr ready, F4 git.md ban scope, F5 request limits, three NITs), round 2 APPROVE WITH FIXES (short hook-bypass residual, branch examples), all applied; read-only, 2026-11-14. | yes | none |
| EVD-006 | [VAL-DELIVERYPERM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes (Recommended) to the SPEC-0214 approval question naming spec.md c95b02fe and plan.md c6510ccf, 2026-11-14","review_ref":"EVD-005","scope":["SPEC-0214","SPEC-0214-PLAN-0001"],"reviewed_spec_sha256":"c95b02fe245366ed9fa53325d367df8f2a9182511b6ef4988ba1865b9ad6bfe1","reviewed_plan_sha256":"c6510ccfdf72305d87d298b46a811efdf151e29bc1ac727c9bacba60b027bf49","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-007 | [VAL-DELIVERYPERM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"8af948a85085849ce3dbee8c4d43c40cb145452b628cb9d6ccc1958b4103c42a","plan_sha256":"c6510ccfdf72305d87d298b46a811efdf151e29bc1ac727c9bacba60b027bf49"} | PASS | Read-only check of the corrected bytes, 2026-11-14: only repository-check fixes (promotion row, one-criterion traceability rows, code-span wrapping of Korean quotations, code-span spacing); no wording change (checked by diff). | yes | none |
| EVD-008 | [VAL-DELIVERYPERM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Re-approve both (Recommended) to the re-approval question naming the corrected bytes of SPEC-0213 and SPEC-0214, here spec.md 8af948a8 and plan.md c6510ccf, 2026-11-14","review_ref":"EVD-007","scope":["SPEC-0214","SPEC-0214-PLAN-0001"],"reviewed_spec_sha256":"8af948a85085849ce3dbee8c4d43c40cb145452b628cb9d6ccc1958b4103c42a","reviewed_plan_sha256":"c6510ccfdf72305d87d298b46a811efdf151e29bc1ac727c9bacba60b027bf49","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-009 | [VAL-DELIVERYPERM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Failing-first: decision and mutation tests on the old settings; whole governance validator with the new pin on the old settings | Linked worktree on branch `claude/claude-delivery-permissions` at base `4b5ba97d`, `.claude/settings.json` unchanged: first with only the `tests/test_agent_governance.py` edits, then also with the `scripts/validate-agent-governance.py` pin; pinned `hyhome-validation` environment; 2026-11-14 | PASS | Red as required. (1) `python3 -m unittest tests.test_agent_governance.NativeDenyCoverageTests.test_delivery_commands_are_allowed_and_raw_api_asks tests.test_agent_governance.NativeBoundaryTests.test_lost_native_denial_and_wildcard_allow_reject` exit 1: 2 tests, 99 failures, 2 errors; 99 of 124 decision expectations failed, every allow and deny the new lists change (the old settings decided ask, deny or the default prompt), and the `push-to-ask` and `main-push-deny` mutations errored with `ValueError` because their rule was absent. Two over-denial cases (push-option text with ` HEAD ` or ` @ `) were then added; the decision test alone, re-run in a scratch root holding the final test module and the base `.claude/settings.json`, exited 1 with 101 of 126 failing and the same 25 passing. Passed as regressions: the 13 earlier allows, the 3 asks, 9 denies under kept rules (both forced-merge orders, `--force-with-lease`, `-d`, `gh release delete`, `gh release delete-asset`, `gh run cancel`, `--amend`, trailing `--force-w`), the `admin-merge-deny` mutation and the default-prompt review guard. (2) `python3 scripts/validate-agent-governance.py --root .` with the new pin: exit 1, `ERR AGENT-NATIVE-PERMISSION agent registry validation failed`. | yes | EVD-001 |
| EVD-010 | [VAL-DELIVERYPERM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | `python3 scripts/validate-agent-governance.py --root .`; `python3 -m unittest tests.test_agent_governance tests.test_validate_agent_registry`; `agent-governance` suite | Uncommitted implementation snapshot on base `4b5ba97d`; sha256 prefixes `.claude/settings.json` `57dd30c06424`, `scripts/validate-agent-governance.py` `a0326b699200`, `tests/test_agent_governance.py` `76b7e2c4e759`; 2026-11-14 | PASS | Validator exit 0, `[PASS] agent registry validation passed: providers=2 roles=17 permissionClasses=4 skills=17 handoffs=67 projections=51`; the two modules ran 89 tests, OK; `python3 scripts/run-contract-tests.py --root . --suite agent-governance` exit 0, modules=4 tests=105. The lists hold 29 allow, 2 ask and 238 deny rules; against base `4b5ba97d` exactly `Bash(gh release create:*)` and `Bash(gh workflow run:*)` left the deny list, the other 195 deny rules and the 20 earlier allows keep their order, and the keys outside `permissions` are unchanged. Repository-static only: native rule matching by a Claude client is not observed. | yes | EVD-002 |
| EVD-011 | [VAL-DELIVERYPERM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Four strict document validators before and after; staged lifecycle check; `python3 scripts/validation/repository/quality.py --root .`; `markdownlint-cli2` on the edited Markdown; `ruff check` and `ruff format --check` on the two edited Python files; `git diff --check` and `git diff --cached --check` | Base `4b5ba97d` before any edit, then the EVD-010 snapshot after the scope change, with sha256 prefixes `.claude/provider.md` `d872c4705c01`, `.codex/provider.md` `299e9571b8fa`, `.agents/governance/git.md` `48b53a432bec`, runbook 0012 `764c7b248255`, `scripts/README.md` `509955d21c38`, and the package's spec.md, plan.md and this Task, staged by explicit paths; `markdownlint-cli2` v0.23.3 from the local Node install, not the v0.22.1 hook pin; ruff 0.16.10, not the v0.16.5 hook pin; 2026-11-14 | PASS | The four strict validators exited 0 before and after with identical output (contract registry `295 paths`; markdown profiles, links and owners, and lifecycle with no violation); `python3 scripts/validate-document-lifecycle.py --root . --mode staged` exit 0; the repository quality check exit 0, `[PASS] repository quality gates passed`, no ERR line (before the scope change it reported 14 push-example lines in spec.md and plan.md); markdownlint 0 issues in 8 files; ruff check clean and `2 files already formatted`; both diff checks clean. A subset of EVD-003: affected-surface routing, `ruff check scripts tests` over both directories, `python3 scripts/qa.py staged` and the commit hooks were not run because this delegated run was limited to focused checks, so EVD-003 stays NOT_RUN for the committing session. SPEC-0199 has not adopted rule IDs (`GIT` is `pending` in the Stage 99 registry), so the git.md text carries no `GIT-R###` row and SPEC-0199 picks it up. | no | none |
| EVD-012 | [VAL-DELIVERYPERM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"fdb81d0b60f22970a0f41abad587d055f1831c6a0b0847bef6e5a7b1bcbc028e","plan_sha256":"ac0b05b9c6d6879687030ea37715f27ed119bc648c69397f090f2d2012710e78"} | PASS | Independent read-only review of the reworded and scope-widened bytes, 2026-11-14: APPROVE with no blocking finding; the 40 push deny rules rebuilt from the table suffixes equal the staged settings in content and order; no gate obfuscation; scope consistent across Spec, Plan and Task; the three NITs (criterion names the README row, option-text note, Plan related-documents row) were applied before this digest. | yes | none |
| EVD-013 | [VAL-DELIVERYPERM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Re-approve bytes (Recommended) to the SPEC-0214 re-approval question naming spec.md fdb81d0b and plan.md ac0b05b9, 2026-11-14","review_ref":"EVD-012","scope":["SPEC-0214","SPEC-0214-PLAN-0001"],"reviewed_spec_sha256":"fdb81d0b60f22970a0f41abad587d055f1831c6a0b0847bef6e5a7b1bcbc028e","reviewed_plan_sha256":"ac0b05b9c6d6879687030ea37715f27ed119bc648c69397f090f2d2012710e78","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-014 | [VAL-DELIVERYPERM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"fdb81d0b60f22970a0f41abad587d055f1831c6a0b0847bef6e5a7b1bcbc028e","plan_sha256":"e39317fb69317a33d9ffe40efcca737b3cad19af0742c0e780ac2f36101036f9"} | PASS | Read-only check of the final bytes, 2026-11-14: plan.md equals the bytes the independent review approved (e39317fb, APPROVE); spec.md differs from the reviewed 5aa79b99 only by the reviewer's two applied NITs (the criterion names the scripts README row; a note on the paraphrased option text); the Plan Promotion row added for NIT 5 was removed because PLAN-PROMOTION accepts only .agents/ or Stage 01/02/05 owners (checked by diff). | yes | none |
| EVD-015 | [VAL-DELIVERYPERM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Re-approve (Recommended) to the SPEC-0214 re-approval question naming spec.md fdb81d0b and plan.md e39317fb, 2026-11-14","review_ref":"EVD-014","scope":["SPEC-0214","SPEC-0214-PLAN-0001"],"reviewed_spec_sha256":"fdb81d0b60f22970a0f41abad587d055f1831c6a0b0847bef6e5a7b1bcbc028e","reviewed_plan_sha256":"e39317fb69317a33d9ffe40efcca737b3cad19af0742c0e780ac2f36101036f9","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-DELIVERYPERM-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-DELIVERYPERM-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `.claude/settings.json` (`permissions.allow`, `permissions.ask` and `permissions.deny` only), `scripts/validate-agent-governance.py` (the three permission tuples and their comment), `tests/test_agent_governance.py`, `.claude/provider.md` (the permission bullet), `.codex/provider.md` (the parity sentence at lines 63-64 only), `.agents/governance/git.md` (Release ownership text, the new `#### Agent delivery commands` subsection, frontmatter), `docs/05.operations/runbooks/0012-main-release-preparation-runbook.md` (executor lines 35-38, Step 5 of the Actions table and lines 112-116, and frontmatter), `scripts/README.md` (the `release.py` row, line 94), this package, `docs/03.specs/README.md`, `.secrets.baseline` (reviewed digest entries only)
- **Forbidden Paths**: `.claude/settings.local.json` and other ignored personal settings, `.codex/rules/`, `.codex/config.toml`, `.codex/hooks.json`, `.codex/hooks/`, `.codex/bindings.json`, `.codex/agents/`, `.claude/hooks/`, `scripts/provider_write_guard.py`, `scripts/release.py`, `.github/`, `.agents/governance/approval-and-safety.md`, `.agents/governance/quality.md`, `docs/02.architecture/`, `docs/99.templates/registry.json`, `.agents/roles/registry.json`, the SPEC-0161 package and `docs/03.specs/work-residue-ledger.json`, `docs/98.archive/`
- **Approval Required**: Spec and Plan approval; criterion acceptance; any commit, push, PR or merge; the optional `gh api` read-back. This package runs no Release, tag or workflow command.
- **Static Validation**: governance validator, `tests.test_agent_governance` and `tests.test_validate_agent_registry`, the `agent-governance` suite, the four strict document validators, the staged lifecycle check, `python3 scripts/validate-affected-surfaces.py --root .`, `ruff check scripts tests`, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface. Native rule matching by a Claude client and hosted protection are separate evidence lanes and stay unobserved unless recorded.
- **Secret / Vault Handling**: no secret read or printed; `gh auth token` and the secret-path denies stay
- **Rollback Plan**: revert the implementation commit. Push returns to ask, the new allows return to the default prompt, the lifted denies return, and the added denies, the git.md text, both provider-note sentences, the runbook lines and the scripts README row leave together. Before that commit exists, delete the package commit.
- **Evidence Location**: this Task

## Verification Summary

Risk class `high` (permission change). WORK-001 and WORK-002 are implemented in the worktree, staged by explicit paths and not committed. EVD-009 resolves EVD-001 and EVD-010 resolves EVD-002. EVD-011 records the document checks; EVD-003 stays NOT_RUN until the committing session runs affected-surface routing, ruff, `python3 scripts/qa.py staged` and the commit hooks on the exact index. EVD-004 stays NOT_RUN and optional. Native rule matching and hosted protection are unobserved.

Core-diff checklist of changed permissions and protected actions:

- Allowed without a prompt on the user's request: commit, push, tag, pull request readiness and approval, Release and workflow commands, and the release producer.
- Removed from the deny list: `gh release create` and `gh workflow run`.
- Still asking: `gh api` and `git -C`.
- Added to the deny list (43 rules): the force, delete, mirror and prune forms with their unique prefixes and two-letter clusters, `main` as a destination, implicit destinations, the amend prefix and the two hook-bypass rules.

Residual risk: the Spec's residual list applies unchanged.

Scope change of 2026-11-14 (see Inputs):

- Runbook 0012 Step 5 in the Actions table (line 66 at base) and the `release.py` row of `scripts/README.md` (line 94) named the operator as the only executor of `publish --execute`. Both now match the governed release delivery.
- The Spec and Plan lines that the repository quality check read as push examples are reworded with the same meaning. `python3 scripts/validation/repository/quality.py --root .` refused them before.
- The Spec and Plan bytes changed, so their re-review and re-approval are pending. EVD-006 and EVD-008 approve the earlier bytes only.

Rollback: as in Approval and Safety Boundaries.

Open question: none. Next owner:

1. the reviewer and the user, for the re-review and re-approval of the changed Spec and Plan;
2. platform, for the exact-index QA and the commit hooks;
3. the operator, for criterion acceptance.
