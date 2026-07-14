---
title: 'Task: Workspace Harness Research Pack'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-13
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

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Scaffold research folder README and parent reference index | doc | VAL-SPC-001 | PLN-001 | `git diff --check`; `bash scripts/validate-repo-quality-gates.sh .` | Codex | Done |
| T-002 | Write workspace governance baseline reference | doc | VAL-SPC-003, VAL-SPC-005 | PLN-002 | Reference template check; repo quality gate | Codex | Done |
| T-003 | Write harness and loop engineering reference | doc | VAL-SPC-004, VAL-SPC-005 | PLN-003 | Source attribution review; repo quality gate | Codex | Done |
| T-004 | Write provider implementation status reference | doc | VAL-SPC-004, VAL-SPC-005 | PLN-004 | Current official-source review; repo quality gate | Codex | Done |
| T-005 | Write spec/SDLC/CI/QA/formatting reference | doc | VAL-SPC-003, VAL-SPC-004, VAL-SPC-005 | PLN-005 | Source attribution review; `git diff --check`; `bash scripts/validate-repo-quality-gates.sh .` | Codex | Done |
| T-006 | Final integration, validation, memory, and handoff | doc | VAL-SPC-006 | PLN-006 | Final validation bundle | Codex | Done |

### Phase View

### Phase 1

- [x] T-001 Scaffold research folder README and parent reference index.
- [x] T-002 Write workspace governance baseline reference.

### Phase 2

- [x] T-003 Write harness and loop engineering reference.
- [x] T-004 Write provider implementation status reference.
- [x] T-005 Write spec/SDLC/CI/QA/formatting reference.

### Phase 3

- [x] T-006 Final integration, validation, memory, and handoff.

## Approval and Safety Boundaries

- **Allowed Paths**: `T-001 through T-006` is limited to these Workspace Harness Research Pack owners and Task-Table surfaces:
  - `docs/04.execution/tasks/2026-07-02-workspace-harness-research-pack.md`
  - `docs/03.specs/009-workspace-harness-research-pack/spec.md`
  - `docs/04.execution/plans/2026-07-02-workspace-harness-research-pack.md`
- **Forbidden Paths**: active policy or runtime configuration not named by the Workspace Harness Research Pack Task Table, provider settings, secret values, local diagnostics, and remote publication surfaces.
- **Approval Required**: Human approval is required before publishing Workspace Harness Research Pack research, changing active policy/runtime behavior, deleting evidence, contacting providers, push, merge, or corpus expansion.
- **Static Validation**: Preserve the Workspace Harness Research Pack outcomes and limitations recorded in Verification Summary; use these recorded checks:
  - `git diff --check`
  - `bash scripts/generate-llm-wiki-index.sh --check`
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `rg --files | rg '(^|/)progress\.md$'`
- **Live Validation**: DEFER — Workspace Harness Research Pack is closed by repository-static/documentation evidence; historical live commands, if any, are not authority for a new cluster, provider, external-service, or deployment claim.
- **Secret / Vault Handling**: Workspace Harness Research Pack evidence must use public or repository-visible facts only; do not inspect or reproduce credentials, tokens, auth files, private logs, kubeconfigs, or shell history.
- **Rollback Plan**: Revert the logical Workspace Harness Research Pack change set for `T-001 through T-006` and restore its allowed implementation/evidence paths with this Task and parent Plan; documentation rollback does not authorize live mutation.
- **Evidence Location**: Durable Workspace Harness Research Pack evidence remains in:
  - `docs/04.execution/tasks/2026-07-02-workspace-harness-research-pack.md`
  - `docs/03.specs/009-workspace-harness-research-pack/spec.md`
  - `docs/04.execution/plans/2026-07-02-workspace-harness-research-pack.md`
  - `docs/00.agent-governance/memory/progress.md`
  - `docs/90.references/research/workspace-governance-baseline.md`

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

### Task Evidence

| Date | Task ID | Command | Result |
| --- | --- | --- | --- |
| 2026-07-02 | T-001 | `git diff --check` | PASS; no output |
| 2026-07-02 | T-001 | `bash scripts/validate-repo-quality-gates.sh .` | PASS; `[PASS] repository quality gates passed` |
| 2026-07-02 | T-002 | Manual template/source review | PASS; created `../../90.references/research/workspace-governance-baseline.md` from `../../99.templates/templates/common/reference.template.md` using repo-backed governance, CI, scripts, template, and adapter evidence |
| 2026-07-02 | T-002 | `git diff --check` | PASS; no output |
| 2026-07-02 | T-002 | `bash scripts/validate-repo-quality-gates.sh .` | PASS; `[PASS] repository quality gates passed` |
| 2026-07-02 | T-003 | Manual template/source review | PASS; created `../../90.references/research/harness-and-loop-engineering.md` from `../../99.templates/templates/common/reference.template.md` using required OpenAI, Anthropic, MCP, repo-backed, and non-authoritative market-scan sources checked on 2026-07-02 |
| 2026-07-02 | T-003 | `git diff --check` | PASS; no output |
| 2026-07-02 | T-003 | `bash scripts/validate-repo-quality-gates.sh .` | PASS; `[PASS] repository quality gates passed` |
| 2026-07-02 | T-004 | Manual template/source review | PASS; created `../../90.references/research/provider-implementation-status.md` from `../../99.templates/templates/common/reference.template.md` using required Claude Code, Claude Code release notes, Codex/OpenAI docs, OpenAI Codex agent-loop article, Gemini CLI, Gemini Code Assist agent mode, Google ADK, and repo-backed provider sources checked on 2026-07-02 |
| 2026-07-02 | T-004 | `git diff --check` | PASS; no output |
| 2026-07-02 | T-004 | `bash scripts/validate-repo-quality-gates.sh .` | PASS; `[PASS] repository quality gates passed` |
| 2026-07-02 | T-005 | Manual template/source review | PASS; created `../../90.references/research/spec-sdlc-ci-qa-formatting.md` from `../../99.templates/templates/common/reference.template.md` using required NIST SSDF, NIST SP 800-204D, GitHub Actions, GitHub Actions secure-use, pre-commit, GitHub Spec Kit, Martin Fowler CI, repo-backed validation, and non-authoritative market-scan sources checked on 2026-07-02 |
| 2026-07-02 | T-005 | `git diff --check` | PASS; no output |
| 2026-07-02 | T-005 | `bash scripts/validate-repo-quality-gates.sh .` | PASS; `[PASS] repository quality gates passed` |
| 2026-07-02 | T-006 | `git diff --check` | PASS; no output |
| 2026-07-02 | T-006 | `bash scripts/generate-llm-wiki-index.sh --check` | PASS; `[PASS] LLM WIKI generated index is current` |
| 2026-07-02 | T-006 | `bash scripts/validate-repo-quality-gates.sh .` | PASS; `[PASS] repository quality gates passed` |
| 2026-07-02 | T-006 | `rg --files \| rg '(^\|/)progress\.md$'` | PASS; returned only `docs/00.agent-governance/memory/progress.md` |
| 2026-07-02 | T-006 | Final review remediation | PASS; aligned plan/task frontmatter, Stage 04 indexes, plan checkboxes, and completion criteria to `Done` |

## Traceability

- **Spec**: `../../03.specs/009-workspace-harness-research-pack/spec.md`
- **Plan**: `../plans/2026-07-02-workspace-harness-research-pack.md`
- **Reference README**: `../../90.references/README.md`
- **Research folder**: `../../90.references/research/README.md`
