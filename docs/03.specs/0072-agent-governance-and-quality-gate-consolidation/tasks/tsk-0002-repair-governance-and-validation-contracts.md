---
title: "Repair Governance and Validation Contracts"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-09"
layer: "specs"
artifact_id: "SPEC-0072-TSK-0002"
---

# Task: Repair Governance and Validation Contracts

## Overview

Execute [WP-010](../plan.md#wp-010-repair-governance-and-validation-contracts)
as five bounded local repair units. This Task begins queued so its initial
document commit records the approved contract before implementation; later
commits may transition it only with observed evidence. It does not alter or
complete `SPEC-0072-TSK-0001`, whose `WORK-009` native follow-up remains an
operator-owned `In progress`/`DEFER` stream.

## Inputs

- [SPEC-0072](../spec.md), criteria `VAL-AGQ-015` through `VAL-AGQ-019`.
- [SPEC-0072-PLAN-0001](../plan.md), `WP-010A` through `WP-010E` and the
  dependency/ownership table.
- [REQ-0003](../../../01.requirements/0003-workspace-agent-governance-platform.md):
  `REQ-0003-FR-0007`, `REQ-0003-FR-0012`, `REQ-0003-FR-0023`,
  `REQ-0003-FR-0028`, and `REQ-0003-NFR-0002`.
- [ADR-0036](../../../02.architecture/decisions/0036-common-knowledge-and-prompt-surfaces.md)
  as the accepted historical decision whose current ownership clarification
  must preserve the original decision.
- Branch `codex/governance-contract-repairs`, clean baseline `66e297ee`.
- Dated hosted baseline: run `34286166198` on `66e297ee` reported QA and
  `ci-summary` success; branch-protection observation returned `403`. These are
  baseline evidence only and are not rerun authority or proof of new bytes.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-010 | VAL-AGQ-015 | Contain and bound evaluation registry, case, response and citation reads; add exactly one authority-negative case/response | platform | Queued | Not executed | Focused evaluation RED/GREEN and payload-free diagnostics |
| WORK-011 | VAL-AGQ-016 | Detect snapshot index mutation and align staged/unstaged review-input semantics and test entry guards | platform | Queued | Not executed | Focused QA/prompt RED/GREEN; deleted-path fixtures retained |
| WORK-012 | VAL-AGQ-017 | Bind numbered document paths to unique current IDs and refuse unproven retired reuse | platform | Queued | Not executed | Ten-family, partial-selection and Archive lineage RED/GREEN |
| WORK-013 | VAL-AGQ-018 | Replace predictable live-script `/tmp` files with private per-run cleanup | platform | Queued | Not executed | Stubbed no-live-command status/diagnostic/cleanup tests |
| WORK-014 | VAL-AGQ-019 | Correct current ownership, formatting and PR/commit prose through canonical owners | platform | Queued | Not executed | Focused governance and repository-quality assertions |

## Approval and Safety Boundaries

- **Allowed Paths**: `scripts/run-agent-evaluations.py`,
  `tests/test_agent_evaluations.py`, the one new
  `evals/cases/code-reviewer-unauthorized-write.json` and
  `evals/responses/code-reviewer-unauthorized-write.synthetic.md` pair, and
  optional `evals/README.md` only for minimal safe-input contract prose without
  adding an ownership framework;
  `scripts/qa.py`, `tests/test_qa_runner.py`,
  `.agents/prompts/change-review.md`, `scripts/prompt-input.py`,
  `tests/test_prompt_input.py`, `tests/test_agent_governance.py`,
  `tests/test_k8s_pre_edit_hook.py`, `tests/test_validate_agent_registry.py`,
  `tests/README.md`, and conditionally `scripts/validate-knowledge-surface.py`
  only when the existing prompt consumer requires the atomic contract update;
  `scripts/validate-markdown-profiles.py`, `scripts/document_lifecycle.py`,
  `scripts/validate-document-lifecycle.py`, optional
  `scripts/document_contracts.py` only if the shared helper is required, and new
  `tests/test_document_artifact_identity.py`; `infrastructure/tests/verify-gitops.sh`,
  `infrastructure/tests/verify-external-services.sh`,
  `infrastructure/tests/verify-ingress-tls.sh`, and new
  `tests/test_infrastructure_tempfiles.py`; `.agents/README.md`,
  `docs/02.architecture/decisions/0036-common-knowledge-and-prompt-surfaces.md`,
  `.agents/governance/formatting-and-linting.md`, `.editorconfig`, `.ruff.toml`,
  `RTK.md`, `.github/PULL_REQUEST_TEMPLATE.md`,
  `scripts/validation/repository/quality.py`, an existing focused test owner only
  if the implementation requires it, `docs/99.templates/README.md`,
  `docs/99.templates/templates/README.md`, and this package's `spec.md`,
  `plan.md`, and this Task under the separate coordinated document owner.
- **Read-only Dependency**: `scripts/validation/repository/bounded_io.py`,
  `docs/99.templates/registry.json`, Stage 99 Spec/Plan/Task forms, current
  lifecycle base and sealed migration/tombstone provenance, `.cz.toml`, the
  active hook configuration and `.worktrees/.agq-venv` tool identities.
- **Forbidden Paths**: native provider projections, global/private
  configuration, credentials, secret bodies, frozen Archive records and
  tombstone payloads, Stage 99 registry/forms, validation registry, CI workflow
  and unrelated user changes. No file deletion is approved.
- **Approval Required**: push, PR, merge, branch/worktree cleanup, deployment,
  live/remote/provider execution, native trust/configuration changes, credential
  access, history rewrite or any widened path. Current approval is local-only.
- **Static Validation**: targeted RED then GREEN for each behavior change and
  focused contract checks for prose-only `WORK-014`; inspect
  status and relevant diff, stage exact logical files, inspect the cached diff,
  run exact-index `staged`, validate the actual pinned candidate message, and
  commit through normal hooks. Run final `full` once after all final bytes;
  `ci` is membership-equivalent and is not rerun locally. Discovery and manual
  pre-commit remain distinct gates inside `full`; index/manual Gitleaks remain
  distinct checks. Do not form a self-SHA/full loop for Task-only evidence.
- **Live Validation**: `DEFER`; stub live-script commands locally. Hosted run,
  provider model/tool/hook delivery and live infrastructure need separate
  approval and evidence.
- **Secret / Vault Handling**: do not read or print credentials, tokens, private
  config, kubeconfig, secret bodies, environment dumps or process arguments.
- **Rollback Plan**: use one forward revert per logical WP-010 unit after
  checking later dependencies. Do not reset, amend, restore away user work or
  alter preserved Archive bytes. The initial Task document commit remains a
  factual approval record even if implementation is cancelled.
- **Evidence Location**: this Task records observed commands, versions, exact
  results, review disposition, rollback and residual risk. Git commits own the
  exact local bytes; no parallel ledger or README is created.

## Verification Summary

Status at creation: `WORK-010` through `WORK-014` are queued and no future test
result is claimed. The approved execution-tool selection is a bounded
`gpt-5.6-sol`/high local authoring and implementation task; it is not native
provider discovery, model resolution, permission enforcement or hook-delivery
evidence. The reusable environment is `.worktrees/.agq-venv` with Python
3.12.3 and 16 matching pins, subject to re-observation at execution time.

Required final handoff fields are branch/HEAD/base, exact commands and versions,
separate repository/hosted/provider/live lane results, current approval boundary,
independent reviewer disposition, rollback commits, residual risk and next
owner. The root supervisor owns overall QA, commits, review reconciliation and
finish decisions. The operator remains next owner for the older native
`WORK-009`; this Task cannot close it.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-010](../plan.md#wp-010-repair-governance-and-validation-contracts) | Queued; no implementation result yet. | `VAL-AGQ-015`; initial approved Task contract |
| [WORK-011](../plan.md#wp-010-repair-governance-and-validation-contracts) | Queued; no implementation result yet. | `VAL-AGQ-016`; initial approved Task contract |
| [WORK-012](../plan.md#wp-010-repair-governance-and-validation-contracts) | Queued; no implementation result yet. | `VAL-AGQ-017`; initial approved Task contract |
| [WORK-013](../plan.md#wp-010-repair-governance-and-validation-contracts) | Queued; no implementation result yet. | `VAL-AGQ-018`; initial approved Task contract |
| [WORK-014](../plan.md#wp-010-repair-governance-and-validation-contracts) | Queued; no implementation result yet. | `VAL-AGQ-019`; initial approved Task contract |
