---
title: 'Harness Governance V2 Overlay Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-06-05
---

# Harness Governance V2 Overlay Implementation Plan

## Overview

This document is the implementation plan for layering ECC DAILY/LIBRARY
classification, workflow skill quality criteria, Hookify local advisory
boundaries, deterministic eval completion contracts, and `progress.md`
single-source rules on top of the already-implemented four-element harness
contract.

## Context

The baseline four-element harness contract is already implemented in Stage 00,
Claude, and Codex. This overlay does not create a new runtime surface. It
extends the existing `docs/00.agent-governance` SSOT so future sessions can
distinguish always-relevant DAILY surfaces from explicitly requested LIBRARY
skills, prove eval completion with deterministic command evidence, and keep the
canonical progress ledger unique.

## Goals & In-Scope

- **Goals**:
  - Add ECC DAILY/LIBRARY surface classification to the harness catalog.
  - Refactor `workspace-harness-audit` into numbered phases with entry, exit,
    and verification criteria.
  - Record Hookify local advisory and shared enforcement boundaries for Claude
    and Codex.
  - Add the Agent Eval Completion Contract to common governance.
  - Enforce `docs/00.agent-governance/memory/progress.md` as the only tracked
    `progress.md`.
  - Add deterministic regression gates for the new overlay contract.
- **In Scope**:
  - `docs/00.agent-governance/harness-catalog.md`
  - `docs/00.agent-governance/rules/agentic.md`
  - `docs/00.agent-governance/rules/documentation-protocol.md`
  - `.claude/CLAUDE.md`
  - `.codex/CODEX.md`
  - `.agents/skills/workspace-harness-audit/skill.md`
  - `scripts/validate-repo-quality-gates.sh`
  - Stage 04 Plan/Task indexes and memory progress ledger

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Create a new `skill-library` router.
  - Add new runtime agents, provider-local skill trees, tracked Hookify rules,
    or `.claude/evals`.
  - Rewrite the existing four-element implementation commits.
- **Out of Scope**:
  - Live k3d, ArgoCD, Vault, ESO, Kubernetes resource mutation, secret-value
    inspection, CI topology changes, model policy changes, and provider-local
    eval directory creation.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| ---- | ----------- | --------------------- | ---------- | ------------------- |
| V2-PLN-001 | Add ECC DAILY/LIBRARY and eval completion contracts | `harness-catalog.md` | REQ-V2-001 | Catalog contains DAILY, LIBRARY, Agent Eval Completion Contract, and Hookify local advisory boundary |
| V2-PLN-002 | Refactor harness audit skill into workflow phases | `.agents/skills/workspace-harness-audit/skill.md` | REQ-V2-002 | Skill has numbered phases, Entry Criteria, Exit Criteria, and Verification Criteria |
| V2-PLN-003 | Add provider adapter pointers | `.claude/CLAUDE.md`, `.codex/CODEX.md` | REQ-V2-003 | Baselines point to canonical progress ledger, eval evidence, and hook boundary |
| V2-PLN-004 | Add common progress/eval rules | `agentic.md`, `documentation-protocol.md` | REQ-V2-004 | Governance states only tracked `progress.md` path and deterministic eval completion rule |
| V2-PLN-005 | Extend regression gate | `scripts/validate-repo-quality-gates.sh` | REQ-V2-005 | Quality gate fails on missing overlay phrases or non-canonical tracked `progress.md` |
| V2-PLN-006 | Record execution evidence | paired Task, README indexes, `memory/progress.md` | REQ-V2-006 | Stage 04 indexes and canonical progress ledger reference this overlay |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| -- | ----- | ----------- | -------------------- | ------------- |
| VAL-V2-001 | Structural | Repository governance overlay contract | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-V2-002 | Hygiene | Patch whitespace and conflict markers | `git diff --check` | PASS |
| VAL-V2-003 | Shell | Quality gate syntax | `bash -n scripts/validate-repo-quality-gates.sh` | PASS |
| VAL-V2-004 | JSON | Runtime hook JSON parseability | `python3 -m json.tool .claude/settings.json`, `.codex/hooks.json`, `.agents/hooks.json` | PASS |
| VAL-V2-005 | Shell | Hook and infrastructure shell syntax | `find infrastructure scripts docs/00.agent-governance/hooks -type f -name '*.sh' -exec bash -n {} +` | PASS |
| VAL-V2-006 | Generated docs | LLM Wiki index freshness | `bash scripts/generate-llm-wiki-index.sh --check` | PASS |
| VAL-V2-007 | Memory singleton | Canonical progress ledger uniqueness | `rg --files \| rg '(^\|/)progress\.md$'` | Only `docs/00.agent-governance/memory/progress.md` |
| VAL-V2-008 | Hookify boundary | Local advisory ignore rule | `git check-ignore -v .claude/hookify.postflight-reminder.local.md` | `.claude/*.local.md` rule is reported |
| VAL-V2-009 | Changed-file eval | Pre-commit on modified files | `/home/hy/.local/bin/pre-commit run --files <changed files>` | PASS or sandbox boundary reported |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| Provider adapters start carrying independent policy | Medium | Keep durable policy in Stage 00 and use `.claude/CLAUDE.md` / `.codex/CODEX.md` only for runtime-specific pointers |
| DAILY/LIBRARY becomes an extra install system | Medium | State that no `skill-library` router is created and `.agents/skills` remains the shared SSoT |
| Hookify local rules are mistaken for shared enforcement | Medium | Keep `.claude/*.local.md` ignored and require tracked enforcement in hooks/settings/validators |
| Eval completion is overstated | High | Require explicit deterministic command evidence or human/operator approval |
| Progress memory drifts into multiple ledgers | Medium | Quality gate fails any tracked non-canonical `progress.md` |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Use deterministic repo-static validators and
  changed-file pre-commit as completion evidence.
- **Sandbox / Canary Rollout**: Not applicable; this is governance and
  validation wiring only.
- **Human Approval Gate**: Required for live runtime probes, direct mutation,
  CI topology, model policy, secret handling, provider-local eval trees, or new
  runtime surfaces.
- **Rollback Trigger**: Revert the overlay change set if repo quality gates
  cannot be made to pass without weakening the Stage 00 contract.
- **Prompt / Model Promotion Criteria**: Not applicable.

## Completion Criteria

- [x] Scoped governance overlay completed.
- [x] Regression gate covers the overlay contract.
- [x] Required docs, indexes, and canonical progress ledger updated.

## Related Documents

- **Task**: [../tasks/2026-06-05-harness-governance-v2-overlay.md](../tasks/2026-06-05-harness-governance-v2-overlay.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Agentic Rules**: [../../00.agent-governance/rules/agentic.md](../../00.agent-governance/rules/agentic.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Progress Ledger**: [../../00.agent-governance/memory/progress.md](../../00.agent-governance/memory/progress.md)
