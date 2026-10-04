---
title: "Stage 99 Lifecycle Normalization Task"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-10-04"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0001"
---

# Task: Stage 99 Lifecycle Normalization

## Overview

This Task owns the single P02 execution item and its observed results. Intake
documents the approved local scope; implementation, review, tests and delivery
are still queued. The [Spec](../spec.md) owns behavior and acceptance; the
[Plan](../plan.md) owns ordered work and dependencies.

## Inputs

- Direct P02 request and approved implementation plan, recorded as the scoped
  user input for this work; no actor identity or authentication is inferred.
- [SPEC-0106](../spec.md), [Plan](../plan.md), completed
  [P01](../../0105-authority-and-safe-authoring/spec.md),
  [Stage 99 Registry](../../../99.templates/registry.json), and
  [quality policy](../../../../.agents/governance/quality.md).
- Preflight: clean `codex/p02-stage99-lifecycle` at
  `50890376ddef88de69f7df4204fc72dfc265c051`; local `main` base
  `f6501e46a0d35858c598c207e726a0e89c92d7d7`. SPEC-0106 was vacant;
  SPEC-0104 is archived.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-P02-001](../spec.md#success-criteria--verification-plan) | Implement and verify the atomic Stage 99 lifecycle acceptance set | platform | Queued | NOT-RUN | Intake source inspection only; focused and delivery checks pending |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/0106-stage99-lifecycle-normalization/`; `docs/03.specs/README.md` (wiki-curator navigation owner); `docs/99.templates/registry.json` and both files in `docs/99.templates/contracts/`; selected forms in `docs/99.templates/templates/`; `scripts/document_contracts.py`, `scripts/validate-document-contract-registry.py`, `scripts/validate-markdown-profiles.py`, `scripts/validate-links-and-owners.py`, `scripts/document_lifecycle.py`, `scripts/validate-document-lifecycle.py`; their direct fixtures under `tests/`; and exact current documents or consumer guidance identified by `VAL-P02-001` inventory. A writer needs explicit file ownership before editing any path beyond this Task's three intake files.
- **Forbidden Paths**: frozen `docs/98.archive/` bodies, sealed records, historical contracts, private/global configuration, secrets, live cluster/cloud resources, and unrelated changes.
- **Approval Required**: The P02 request approved scoped local implementation, review, validation and three logical local commits: intake, atomic implementation and acceptance. Push, PR, merge, archive cutover, live/secret actions, and worktree removal need separate authority. No authenticated approving actor, trusted reference, or revocation verification has been supplied or claimed.
- **Static Validation**: Focused RED/GREEN fixtures; affected `python3 scripts/qa.py quick`; exact-index `python3 scripts/qa.py staged` and actual commit-message validation for each logical commit; one final local `python3 scripts/qa.py full`; closing-doc affected and completion-mode checks. No P02 execution result exists at intake.
- **Live Validation**: DEFER — not requested or authorized; repository-static results do not prove runtime behavior.
- **Secret / Vault Handling**: No read, print, or mutation of secret values. References and fixed public artifact identities only.
- **Rollback Plan**: Review P02 commit boundaries and use forward reverts where authorized; preserve unrelated work, historical records and this evidence ledger.
- **Evidence Location**: This Task, with exact branch/HEAD/index or worktree snapshot per result.

## Verification Summary

Intake source inspection selected the existing forms and profiles; no P02 test,
quick, staged, full, message, completion-mode, provider-runtime, hosted or live
check has run. Preflight observed Python 3.12.3, pre-commit 4.6.1, Kustomize
5.8.1 digest `f7b1605aa5143e0dcbd754a4d43c47ad7a560c540b1356b064d69fe236164494`
and fixed Conftest digest
`a38ba21668929a00dce2fe6ee43d1312228340bce5fd243f47dd0ce90516e558`, consumed at
`scripts/validate-policy-gates.sh:57`; re-observe identities at actual run.
Shell reads required bounded native escalation after `bwrap` loopback startup
failure. Independent review, residual risk disposition and final next owner
remain pending; the next owner is the P02 implementation writer after intake
review. This is repository-static planning evidence only. An attempted focused
`python3 scripts/validate-markdown-profiles.py --mode strict --include-path`
call for these three intake documents was rejected by automatic approval review
before execution because validation precedes intake review; it has no test
result and will not be retried before that review.

The current direct consumer inventory is
`scripts/document_contracts.py` (registry decoding),
`scripts/validate-document-contract-registry.py` (registry/form agreement),
`scripts/validate-markdown-profiles.py` (frontmatter, sections and body tables),
`scripts/validate-links-and-owners.py` (resolved source/target ownership),
`scripts/document_lifecycle.py` and
`scripts/validate-document-lifecycle.py` (state/Git history and archive routes),
and `scripts/validation/registry.json` with `scripts/qa.py` (affected and
delivery routing). Direct negative/historical fixtures already live under
`tests/test_document_lifecycle_*.py`, `tests/test_archive_*.py`,
`tests/test_document_strict_cutover.py`, and related document route tests;
implementation must select exact files by changed behavior, not by this
inventory shorthand. Human consumers are Stage 99 author guidance,
`docs/03.specs/README.md`, and the current P01/P02 package documents.

Source inspection mapped the current 37 physical forms under
`docs/99.templates/templates/` to their logical source profiles. Each form
also has a distinct `common/template-*` wrapper profile in the registry;
these pairs are an observed inventory, not fixed acceptance counts.

| Physical form under `templates/` | Logical source profile |
| --- | --- |
| `architecture/decision.template.md` | `sdlc/architecture-decision` |
| `architecture/description.template.md` | `sdlc/architecture-description` |
| `archive/migration.template.md` | `archive/migration` |
| `archive/route-tombstone.template.md` | `archive/route-tombstone` |
| `archive/scope-migration.template.md` | `archive/scope-migration` |
| `archive/tombstone.template.md` | `archive/tombstone` |
| `common/readme-collection-index.template.md` | `common/readme-collection-index` |
| `common/readme-implementation.template.md` | `common/readme-implementation` |
| `common/readme-repository.template.md` | `common/readme-repository` |
| `common/readme-runtime-governance.template.md` | `common/readme-runtime-governance` |
| `common/readme-stage-index.template.md` | `common/readme-stage-index` |
| `common/readme-workspace-staging.template.md` | `common/readme-workspace-staging` |
| `governance/contract.template.md` | `governance/contract` |
| `governance/knowledge.template.md` | `governance/knowledge` |
| `governance/prompt.template.md` | `governance/prompt` |
| `governance/provider.template.md` | `governance/provider` |
| `governance/role.template.md` | `governance/role` |
| `governance/rule.template.md` | `governance/rule` |
| `governance/skill.template.md` | `governance/skill` |
| `operations/guide.template.md` | `operation/guide` |
| `operations/incident.template.md` | `operation/incident` |
| `operations/policy.template.md` | `operation/policy` |
| `operations/postmortem.template.md` | `operation/postmortem` |
| `operations/runbook.template.md` | `operation/runbook` |
| `references/audit-pack.template.md` | `common/readme-audit-pack` |
| `references/audit.template.md` | `reference/audit` |
| `references/data-pack.template.md` | `common/readme-data-pack` |
| `references/data.template.md` | `reference/data` |
| `references/research-pack.template.md` | `common/readme-research-pack` |
| `references/research.template.md` | `reference/research` |
| `requirements/requirement-package.template.md` | `sdlc/requirement` |
| `runtime/claude-agent.template.md` | `common/provider-native-metadata` |
| `runtime/claude-command.template.md` | `common/provider-native-command` |
| `runtime/codex-agent.template.toml` | `common/codex-agent-binding` |
| `specs/plan.template.md` | `sdlc/plan` |
| `specs/spec.template.md` | `sdlc/spec` |
| `specs/task.template.md` | `sdlc/task` |

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [VAL-P02-001](../spec.md#success-criteria--verification-plan) | NOT-RUN | Intake scope and queued WORK-001 Task Table row; implementation evidence pending |
