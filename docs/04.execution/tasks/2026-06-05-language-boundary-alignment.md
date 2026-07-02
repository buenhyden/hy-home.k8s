---
title: 'Task: Language Boundary Alignment'
type: sdlc/task
status: done
owner: platform
updated: 2026-06-05
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

## Working Rules

- Governance and policy-control documents under `docs/00.agent-governance/**`
  remain English.
- `docs/03.specs/**/spec.md`, `docs/04.execution/plans/*.md`, and
  `docs/04.execution/tasks/*.md` are English-first execution artifacts.
- Human-facing README files and operations guidance may remain Korean.
- Reference hubs may use Korean for human-facing lookup context, while
  authority, source, freshness, generated-index, version-support, and AI-agent
  routing fields remain English-first.
- Mixed-audience documents keep human context in Korean and AI-agent execution
  contracts in English.
- Korean prose changes must preserve meaning, facts, paths, commands, dates,
  and proper nouns.

## Language Boundary Audit

| Area | Current Evidence | Result |
| ---- | ---------------- | ------ |
| `docs/00.agent-governance/**` | Existing validators keep tracked governance/runtime files English-only. | Policy reinforced. |
| `docs/03.specs/**/spec.md` | A ripgrep scan for Korean syllables now returns no matches. | English-first remediation complete. |
| `docs/04.execution/plans/*.md` | A ripgrep scan for Korean syllables now returns no matches outside the human-facing README index. | English-first remediation complete. |
| `docs/04.execution/tasks/*.md` | A ripgrep scan for Korean syllables now returns no matches outside the human-facing README index. | English-first remediation complete. |
| `docs/05.operations/{guides,policies,runbooks,incidents}` | Folder READMEs define guide, policy, runbook, incident, and postmortem roles. | Operations boundary reinforced in the operations hub. |
| `docs/90.references/**` | Root and subfolder READMEs define agents, learning, llm-wiki, and versions roles plus language boundaries. | Reference boundary reinforced. |
| Root `README.md` and docs hub | Both entrypoints state the language policy for human-facing docs, Stage 03/04 execution artifacts, operations docs, and references. | Human-facing entrypoints aligned. |

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

## Suggested Types

- `doc`
- `eval`
- `guardrail`
- `test`

## Agent-specific Types (If Applicable)

- `memory`
- `guardrail`
- `eval`

## Completion Notes

- Legacy Stage 03 spec documents have been translated to English.
- Legacy Stage 04 implementation plans have been translated to English.
- Legacy Stage 04 task records have been translated to English.
- The repo quality gate now enforces the English-first Stage 03/04 paths.
- Operations and references remain mixed-audience areas with explicit language
  boundaries.

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

## Related Documents

- **Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Plan**: [../plans/2026-06-05-harness-governance-v2-overlay.md](../plans/2026-06-05-harness-governance-v2-overlay.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Authoring Matrix**: [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Templates README**: [../../99.templates/README.md](../../99.templates/README.md)
- **Operations README**: [../../05.operations/README.md](../../05.operations/README.md)
- **References README**: [../../90.references/README.md](../../90.references/README.md)
- **Root README**: [../../../README.md](../../../README.md)
