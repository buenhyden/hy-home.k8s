---
title: 'Task: Docs Governance Full A+B Hardening'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-13
---

# Task: Docs Governance Full A+B Hardening

## Overview

This document tracks implementation and verification tasks for aligning the
documentation lifecycle, README template conformance, agent/runtime governance,
hook boundaries, and repo-static validation gates.

## Inputs

- **Parent Spec**: not applicable; this work hardens documentation and agent governance contracts.
- **Parent Plan**: [../plans/2026-05-22-docs-governance-full-ab-hardening.md](../plans/2026-05-22-docs-governance-full-ab-hardening.md)

## Approval and Safety Boundaries

- Keep gateway files thin and route durable policy to `docs/00.agent-governance/**`.
- Keep historical PRD/ARD/Plan/Task meaning and evidence intact.
- Use `docs/99.templates` before touching authored lifecycle documents.
- Keep Hookify `.local.md` ignored and local-only; shared enforcement belongs in tracked hooks and validators.
- Documentation-only work still needs repo-static validation evidence.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Capture drift snapshot for README headings, link basis, template residue, and runtime mirrors | doc | n/a | PLN-001 | `rg` targeted scans | Platform | Done |
| T-002 | Add implementation Plan/Task records and update execution indexes | doc | n/a | PLN-001 | Plan/Task files and README indexes updated | Platform | Done |
| T-003 | Improve template guidance for README and hook/runtime boundaries | doc | n/a | PLN-002 | Quality gate and template checks pass | Platform | Done |
| T-004 | Normalize every README to `Related Documents` and `Link Basis` | doc | n/a | PLN-003 | Targeted README scans return no output | Platform | Done |
| T-005 | Align `docs/01~05` lifecycle documents with safe template/cross-link rules | doc | n/a | PLN-004 | Required heading and link checks pass | Platform | Done |
| T-006 | Clarify tracked hook, Codex hook, and Hookify local warning ownership | guardrail | n/a | PLN-005 | Runtime/hook validator checks pass | Platform | Done |
| T-007 | Harden repo quality gate for README and Hookify drift | test | n/a | PLN-006 | `bash scripts/validate-repo-quality-gates.sh .` PASS | Platform | Done |
| T-008 | Run full repo-static validation matrix | test | n/a | PLN-007 | Verification Summary updated | Platform | Done |
| T-009 | Update progress memory and handoff evidence | memory | n/a | PLN-007 | `progress.md` entry added | Platform | Done |

### Suggested Types

- `impl`
- `test`
- `eval`
- `doc`
- `ops`

### Agent-specific Types

- `prompt`
- `tool`
- `memory`
- `guardrail`
- `eval`
- `observability`

### Phase View

### Phase 1

- [x] T-001 Capture drift snapshot
- [x] T-002 Add implementation evidence records

### Phase 2

- [x] T-003 Improve template guidance
- [x] T-004 Normalize README files
- [x] T-005 Align lifecycle documents

### Phase 3

- [x] T-006 Clarify hook ownership
- [x] T-007 Harden quality gate
- [x] T-008 Run validation matrix
- [x] T-009 Update progress memory

## Verification Summary

- **Test Commands**:
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `bash scripts/generate-llm-wiki-index.sh --check`
  - `bash infrastructure/tests/verify-contracts-static.sh`
  - `bash scripts/validate-gitops-structure.sh`
  - `bash scripts/validate-k8s-manifests.sh .`
  - `bash scripts/check-secret-handling.sh .`
  - `find infrastructure scripts docs/00.agent-governance/hooks -type f -name '*.sh' -exec bash -n {} +`
  - `python3 -m json.tool .claude/settings.json`
  - `python3 -m json.tool .codex/hooks.json`
  - `git diff --check`
- **Eval Commands**: not applicable; no prompt/model behavior is changed.
- **Logs / Evidence Location**: this task document and `docs/00.agent-governance/memory/progress.md`.
- **Result**: PASS for the full repo-static matrix. `kube-linter` was not installed, so `validate-k8s-manifests.sh` completed YAML syntax validation and reported the optional kube-linter skip.
- **Targeted Scans**: README legacy heading, README `Link Basis` omission, lifecycle template residue, and tracked `.claude/*.local.md` scans returned no findings.

## Traceability

- **Plan**: [../plans/2026-05-22-docs-governance-full-ab-hardening.md](../plans/2026-05-22-docs-governance-full-ab-hardening.md)
- **Templates**: [../../99.templates/README.md](../../99.templates/README.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Postflight Checklist**: [../../00.agent-governance/rules/postflight-checklist.md](../../00.agent-governance/rules/postflight-checklist.md)
