---
title: 'Task: Authority and Lineage Foundation'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-15
---

# Task: Authority and Lineage Foundation

## Overview

This Task is the durable execution and review record for Spec 034. It tracks
registry v6 lineage, cross-document admission, Stage 00 authority cleanup,
Current audit dispositions, and tranche closure without claiming remote or live
evidence.

## Inputs

- **Plan**: [Authority and Lineage Foundation Implementation Plan](../plans/2026-07-15-authority-and-lineage-foundation.md)
- **Spec**: [Spec 034](../../03.specs/034-authority-and-lineage-foundation/spec.md)
- **PRD**: [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **ARD**: [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- **Decision**: [ADR-0017](../../02.architecture/decisions/0017-program-follow-up-lineage-semantics.md)
- **Current audit**: [2026-07-11 WEIA remediation roadmap](../../90.references/audits/2026-07-11-weia/remediation-roadmap.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| ALF-001 | VAL-ALF-001 through VAL-ALF-004 | Introduce typed registry v6 program relations. | platform | Done | Implemented; independent re-review returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`. | Initial RED: the v6 `valid-minimal` fixture failed with `REGISTRY_SCHEMA` against the v5 loader. Review RED: duplicate `status` was accepted with no diagnostic. GREEN: registry self-test passes 78 cases, including 19 lineage mutations and the isolated legacy migration proof; strict mode loads two programs with 430 classified paths, baseline 433, new 58, uncovered 0, and ambiguous 0. |
| ALF-002 | VAL-ALF-002, VAL-ALF-004, VAL-ALF-006, VAL-ALF-007 | Enforce cross-document lineage and predecessor-gated execution; retire duplicate Stage 00 lifecycle tables. | platform | Queued | Not executed | Cross-document fixtures, Stage 00 diff, strict result, and logical commit will be recorded here. |
| ALF-003 | VAL-ALF-005 | Add the evidence-backed Current audit disposition overlay. | platform | Queued | Not executed | Observation-row preservation, overlay links, validators, and logical commit will be recorded here. |
| ALF-004 | VAL-ALF-001 through VAL-ALF-007 | Run full QA, independent review, and atomic lifecycle closure. | platform | Queued | Not executed | Command matrix, review verdicts, rollback parent, and closure commit will be recorded here. |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/00.agent-governance/**`, `docs/03.specs/034-authority-and-lineage-foundation/**`, `docs/03.specs/README.md`, this Plan/Task and Stage 04 indexes, `docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md`, `docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md`, `docs/99.templates/support/document-profiles.{json,schema.json}`, `scripts/document_contracts.py`, `scripts/validate-document-contract-registry.py`, `scripts/validate-links-and-owners.py`, `scripts/README.md`, and the two named fixture files.
- **Forbidden Paths**: Kubernetes/GitOps desired state, infrastructure, policies, secrets, provider runtime adapters, unrelated audit observations, completed/accepted PRD-005/ARD-0008/ADR-0016/Specs 026-033/Plan/Task bodies, and Specs 035-040 bodies except read-only verification.
- **Approval Required**: Any live system, secret, remote GitHub setting, push, publication, or scope expansion requires separate explicit approval.
- **Static Validation**: Registry, Markdown-profile, cross-document, repository-quality, Markdown lint, staged diff, and all-files pre-commit commands from the Plan.
- **Live Validation**: DEFER. This tranche has no authorized live lane.
- **Secret / Vault Handling**: Do not read, print, move, or infer secret values, tokens, auth files, or Vault data.
- **Rollback Plan**: Revert the newest logical ALF commit first; if the v6 cutover must be removed, revert ALF-002 before ALF-001 so no validator consumes the removed typed interface.
- **Evidence Location**: This Task, the logical Git commits, registry/cross-document fixtures, and the dated Current audit overlay.

## Verification Summary

ALF-001 is implemented and independently approved. Its test-first RED run
failed because schema/loader v5 rejected the new closed-v6 fixture. After the
implementation, `python3 scripts/validate-document-contract-registry.py --root
. --self-test` passes 78 cases and the strict command passes 430 classified
paths while exposing two typed programs. Production loading rejects v5; its
only converter is private to the self-test migration fixture. Quality review
then added fail-closed duplicate-key parsing, explicit ADR timestamp rejection,
and consecutive follow-up approval-order validation. The approved design
baseline remains `daf0636` plus review correction `0f67e9c`. The current
environment has one known all-files limitation: `validate-gitops-change-set.py
--self-test` calls `os.mkfifo`, which returns `Errno 95` in this filesystem and
is independently reproducible on unchanged main. Spec 039 owns its portability
remediation. Requirements re-review returned `REQUIREMENTS COMPLIANT`; quality
re-review returned `QUALITY APPROVED` after the three fail-closed fixes.

| ALF-001 command | Result |
| --- | --- |
| `python3 scripts/validate-document-contract-registry.py --root . --self-test` before implementation | RED: exit 1; `valid-minimal` expected no diagnostics and received `REGISTRY_SCHEMA`. |
| Quality-review RED fixture run | RED: duplicate `status` expected `REGISTRY_PROGRAM_STATE` and received no diagnostic because the last YAML value was accepted. |
| `python3 scripts/validate-document-contract-registry.py --root . --self-test` after review remediation | PASS: 78 cases, 64 profiles, 30 templates, duplicate `status`/`updated`, timestamp rejection, follow-up approval order, legacy-v5 migration fixture, and mutation probes. |
| `python3 scripts/validate-document-contract-registry.py --root . --mode strict` | PASS: baseline 433, new 58, programs 2, uncovered 0, ambiguous 0, and 430 classified paths. |
| Markdown-profile and cross-document self-test plus strict commands | PASS: both self-tests and both current-corpus strict integrations. |
| `ruff check` for the two Python owners; Python AST parse; JSON parse; `git diff --check` | PASS. The optional repository-wide Ruff formatter baseline remains outside this work package; no Ruff lint or syntax issue exists in the changed Python. |
| Changed-file pre-commit with `strict-repository-quality` skipped | PASS for affected-surface validation, JSON, EOF, line endings, whitespace, gitleaks, detect-secrets, and Markdown lint. The skipped aggregate is the already bounded FIFO limitation owned by Spec 039, not an ALF-001 PASS claim. |

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [ALF-001](../plans/2026-07-15-authority-and-lineage-foundation.md#task-1-introduce-typed-registry-v6-program-relations) | Done. | Closed-v6 schema/data, `Registry.program_lineage`, duplicate-key/timestamp/approval-order review remediation, 78-case self-test, strict 430-path PASS, and independent requirements/quality approval provide repository-static evidence. |
| [ALF-002](../plans/2026-07-15-authority-and-lineage-foundation.md#task-2-enforce-cross-document-lineage-and-execution-admission) | Queued. | This Task will record cross-document, Stage 00, review, and commit evidence. |
| [ALF-003](../plans/2026-07-15-authority-and-lineage-foundation.md#task-3-normalize-the-current-audit-remediation-overlay) | Queued. | This Task will record observation-preservation, overlay, review, and commit evidence. |
| [ALF-004](../plans/2026-07-15-authority-and-lineage-foundation.md#task-4-validate-and-close-the-authority-foundation) | Queued. | This Task will record full QA, review verdicts, rollback, and closure evidence. |
