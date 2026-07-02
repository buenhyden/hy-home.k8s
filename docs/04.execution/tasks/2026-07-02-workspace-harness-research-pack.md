---
title: 'Task: Workspace Harness Research Pack'
type: task
status: draft
owner: platform
updated: 2026-07-02
---

# Task: Workspace Harness Research Pack

---

## Overview

This document tracks implementation and verification work for the integrated
workspace harness research pack under `docs/90.references/research/`.

The task is documentation-only. Repo-static validation is required, but live
k3d, ArgoCD, Vault, ESO, Kubernetes, cloud, provider runtime, and secret checks
are out of scope unless separately approved by a human.

## Inputs

- **Parent Spec**: `../../03.specs/009-workspace-harness-research-pack/spec.md`
- **Parent Plan**: `../plans/2026-07-02-workspace-harness-research-pack.md`

## Working Rules

- Documentation-only work still needs validation evidence.
- External source claims must be checked before writing current provider status.
- Market scan findings must be labeled non-authoritative.
- Reference documents must not redefine active governance policy.
- Repo-static validation must not be reported as live runtime readiness unless
  a separate live check was approved and run.
- Logical-unit commits are required.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Scaffold research folder README and parent reference index | doc | VAL-SPC-001 | PLN-001 | `git diff --check`; `bash scripts/validate-repo-quality-gates.sh .` | Codex | Todo |
| T-002 | Write workspace governance baseline reference | doc | VAL-SPC-003, VAL-SPC-005 | PLN-002 | Reference template check; repo quality gate | Codex | Todo |
| T-003 | Write harness and loop engineering reference | doc | VAL-SPC-004, VAL-SPC-005 | PLN-003 | Source attribution review; repo quality gate | Codex | Todo |
| T-004 | Write provider implementation status reference | doc | VAL-SPC-004, VAL-SPC-005 | PLN-004 | Current official-source review; repo quality gate | Codex | Todo |
| T-005 | Write spec/SDLC/CI/QA/formatting reference | doc | VAL-SPC-003, VAL-SPC-004, VAL-SPC-005 | PLN-005 | Source attribution review; repo quality gate | Codex | Todo |
| T-006 | Final integration, validation, memory, and handoff | doc | VAL-SPC-006 | PLN-006 | Final validation bundle | Codex | Todo |

## Suggested Types

- `doc`
- `eval`
- `ops`

## Agent-specific Types (If Applicable)

- `memory`
- `guardrail`
- `eval`
- `observability`

## Phase View

### Phase 1

- [ ] T-001 Scaffold research folder README and parent reference index.
- [ ] T-002 Write workspace governance baseline reference.

### Phase 2

- [ ] T-003 Write harness and loop engineering reference.
- [ ] T-004 Write provider implementation status reference.
- [ ] T-005 Write spec/SDLC/CI/QA/formatting reference.

### Phase 3

- [ ] T-006 Final integration, validation, memory, and handoff.

## Verification Summary

- **Test Commands**:
  - `git diff --check`
  - `bash scripts/generate-llm-wiki-index.sh --check`
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `rg --files | rg '(^|/)progress\.md$'`
- **Eval Commands**:
  - Manual source-attribution review for each reference document.
  - Manual checklist coverage review against the parent Spec success criteria.
- **Logs / Evidence Location**:
  - This task record.
  - `../../00.agent-governance/memory/progress.md`.

## Related Documents

- **Spec**: `../../03.specs/009-workspace-harness-research-pack/spec.md`
- **Plan**: `../plans/2026-07-02-workspace-harness-research-pack.md`
- **Reference README**: `../../90.references/README.md`
- **Research folder**: `../../90.references/research/README.md`
