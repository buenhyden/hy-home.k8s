---
title: 'Task: Language Boundary Alignment'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-13
---

# Task: Language Boundary Alignment

## Overview

This task tracks the document language policy alignment requested for AI-agent
documents, human-facing documents, and mixed-audience documents. The current
change strengthens the canonical policy and templates, applies the policy to
legacy Stage 03/04 artifacts, reinforces operations and reference folder roles,
and adds deterministic validation for English-first execution artifacts.

## Inputs

- **Parent Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Parent Plan**: [../plans/2026-06-05-harness-governance-v2-overlay.md](../plans/2026-06-05-harness-governance-v2-overlay.md)
- **Requested Skills**:
  - `/home/hy/gstack/.agents/skills/gstack-document-release/SKILL.md`
  - `/home/hy/im-not-ai/codex/skills/humanize-korean/SKILL.md`

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| ------- | ----------- | ---- | --------------------- | ------------------- | --------------------- | ----- | ------ |
| LANG-001 | Read requested document-release and humanize-korean skills | doc | Language policy | Intake | Skill files inspected | platform | Done |
| LANG-002 | Audit language boundary across specs, plans, tasks, operations docs, references, and entrypoint READMEs | eval | Language policy | Audit | Language Boundary Audit table | platform | Done |
| LANG-003 | Strengthen canonical language policy and stage matrix | guardrail | Governance | Policy | `documentation-protocol.md`, `stage-authoring-matrix.md`, `standards.md` | platform | Done |
| LANG-004 | Align spec, plan, and task templates with English-first rule | doc | Templates | Template update | `spec.template.md`, `plan.template.md`, `task.template.md`, `docs/99.templates/README.md` | platform | Done |
| LANG-005 | Reinforce operations folder role and language boundary | doc | Operations | Operations docs | `docs/05.operations/README.md` | platform | Done |
| LANG-006 | Convert new Stage 04 risk closure evidence to English | doc | Stage 04 tasks | Current worktree | `2026-06-05-harness-connective-layer-risk-closure.md` | platform | Done |
| LANG-007 | Translate legacy spec/plan/task documents to English | doc | Stage 03/04 legacy docs | Remediation | Ripgrep scans return no Korean syllables in English-first artifacts | platform | Done |
| LANG-008 | Add deterministic language-boundary gate after legacy remediation | test | Repo validators | Validator | `validate-repo-quality-gates.sh` rejects Korean syllables in Stage 03/04 English-first artifacts | platform | Done |
| LANG-009 | Reinforce reference folder roles and language boundary | doc | References | Reference docs | `docs/90.references/README.md` and subfolder READMEs | platform | Done |
| LANG-010 | Apply language policy to root and docs entrypoints | doc | Entrypoints | README docs | `README.md`, `docs/README.md` | platform | Done |

### Completion Notes

- Legacy Stage 03 spec documents have been translated to English.
- Legacy Stage 04 implementation plans have been translated to English.
- Legacy Stage 04 task records have been translated to English.
- The repo quality gate now enforces the English-first Stage 03/04 paths.
- Operations and references remain mixed-audience areas with explicit language
  boundaries.

## Approval and Safety Boundaries

- **Allowed Paths**: `LANG-001 through LANG-010` is limited to these Language Boundary Alignment owners and Task-Table surfaces:
  - `docs/04.execution/tasks/2026-06-05-language-boundary-alignment.md`
  - `docs/03.specs/006-workspace-harness-gap-analysis/spec.md`
  - `docs/04.execution/plans/2026-06-05-harness-governance-v2-overlay.md`
  - `docs/99.templates/README.md`
  - `docs/05.operations/README.md`
  - `docs/90.references/README.md`
  - `docs/README.md`
- **Forbidden Paths**: provider account settings, live agent sessions, credentials, model/runtime policy outside the parent Plan, and repository paths outside the Language Boundary Alignment surfaces.
- **Approval Required**: Human approval is required before Language Boundary Alignment provider configuration, model-policy promotion, remote agent action, credential access, protected-file expansion, push, merge, or publication.
- **Static Validation**: Preserve the Language Boundary Alignment outcomes and limitations recorded in Verification Summary; use these recorded checks:
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `git diff --check`
  - `bash -n scripts/validate-repo-quality-gates.sh`
- **Live Validation**: DEFER — Language Boundary Alignment is closed by repository-static/documentation evidence; historical live commands, if any, are not authority for a new cluster, provider, external-service, or deployment claim.
- **Secret / Vault Handling**: Use only redacted repository contracts for Language Boundary Alignment; do not read or print provider tokens, auth files, memory stores, private logs, kubeconfigs, secret values, or shell history.
- **Rollback Plan**: Revert the logical Language Boundary Alignment change set for `LANG-001 through LANG-010` and restore its allowed implementation/evidence paths with this Task and parent Plan; documentation rollback does not authorize live mutation.
- **Evidence Location**: Durable Language Boundary Alignment evidence remains in:
  - `docs/04.execution/tasks/2026-06-05-language-boundary-alignment.md`
  - `docs/03.specs/006-workspace-harness-gap-analysis/spec.md`
  - `docs/04.execution/plans/2026-06-05-harness-governance-v2-overlay.md`
  - `docs/03.specs/**/spec.md`
  - `docs/04.execution/plans/*.md`

## Verification Summary

- **Test Commands**:
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `git diff --check`
  - `bash -n scripts/validate-repo-quality-gates.sh`
- **Eval Commands**:
  - Ripgrep scan for Korean syllables in `docs/03.specs/**/spec.md`.
  - Ripgrep scan for Korean syllables in `docs/04.execution/plans/*.md`.
  - Ripgrep scan for Korean syllables in `docs/04.execution/tasks/*.md`.
- **Logs / Evidence Location**:
  - This task document.
  - [Progress Ledger](../../00.agent-governance/memory/progress.md)

## Traceability

- **Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Plan**: [../plans/2026-06-05-harness-governance-v2-overlay.md](../plans/2026-06-05-harness-governance-v2-overlay.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Authoring Matrix**: [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Templates README**: [../../99.templates/README.md](../../99.templates/README.md)
- **Operations README**: [../../05.operations/README.md](../../05.operations/README.md)
- **References README**: [../../90.references/README.md](../../90.references/README.md)
- **Root README**: [../../../README.md](../../../README.md)
