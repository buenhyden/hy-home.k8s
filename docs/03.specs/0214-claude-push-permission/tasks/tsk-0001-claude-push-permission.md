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

This Task will record, for [SPEC-0214](../spec.md) under its [Plan](../plan.md):

- the failing-first and passing results of the permission pin and the decision regressions;
- the document and exact-index checks;
- the criterion decisions.

It is a stub: nothing has run.

## Inputs

- **Request:** the user's successive wordings and answers of 2026-11-14 (Asia/Seoul), quoted verbatim in the Spec's Decisions. That includes the answers "Lift create/run denies", "Allow" and "Leave .codex unchanged (Recommended)". The request approves no Spec bytes, no criterion and no commit, push or merge. Open question: none.
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

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-DELIVERYPERM-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-DELIVERYPERM-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `.claude/settings.json` (`permissions.allow`, `permissions.ask` and `permissions.deny` only), `scripts/validate-agent-governance.py` (the three permission tuples and their comment), `tests/test_agent_governance.py`, `.claude/provider.md` (the permission bullet), `.codex/provider.md` (the parity sentence at lines 63-64 only), `.agents/governance/git.md` (Release ownership text, the new `#### Agent delivery commands` subsection, frontmatter), `docs/05.operations/runbooks/0012-main-release-preparation-runbook.md` (executor lines 35-38 and 112-116, and frontmatter), this package, `docs/03.specs/README.md`, `.secrets.baseline` (reviewed digest entries only)
- **Forbidden Paths**: `.claude/settings.local.json` and other ignored personal settings, `.codex/rules/`, `.codex/config.toml`, `.codex/hooks.json`, `.codex/hooks/`, `.codex/bindings.json`, `.codex/agents/`, `.claude/hooks/`, `scripts/provider_write_guard.py`, `scripts/release.py`, `.github/`, `.agents/governance/approval-and-safety.md`, `.agents/governance/quality.md`, `docs/02.architecture/`, `docs/99.templates/registry.json`, `.agents/roles/registry.json`, the SPEC-0161 package and `docs/03.specs/work-residue-ledger.json`, `docs/98.archive/`
- **Approval Required**: Spec and Plan approval; criterion acceptance; any commit, push, PR or merge; the optional `gh api` read-back. This package runs no Release, tag or workflow command.
- **Static Validation**: governance validator, `tests.test_agent_governance` and `tests.test_validate_agent_registry`, the `agent-governance` suite, the four strict document validators, the staged lifecycle check, `python3 scripts/validate-affected-surfaces.py --root .`, `ruff check scripts tests`, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface. Native rule matching by a Claude client and hosted protection are separate evidence lanes and stay unobserved unless recorded.
- **Secret / Vault Handling**: no secret read or printed; `gh auth token` and the secret-path denies stay
- **Rollback Plan**: revert the implementation commit. Push returns to ask, the new allows return to the default prompt, the lifted denies return, and the added denies, the git.md text, both provider-note sentences and the runbook lines leave together. Before that commit exists, delete the package commit.
- **Evidence Location**: this Task

## Verification Summary

Draft; no check has run. Risk class `high` (permission change). Open question: none. Next owner: the user, for Spec and Plan approval; then platform, for WORK-001.
