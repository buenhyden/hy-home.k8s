---
title: 'Workspace Purpose Alignment Audit Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-05-22
---

# Workspace Purpose Alignment Audit Plan

## Overview

This document is the implementation plan for fully re-auditing whether
`hy-home.k8s` actually supports WSL2 native Docker, k3d, ArgoCD GitOps,
External Secrets/Vault, external PostgreSQL/Valkey contracts, the SDD document
lifecycle, and AI Agent governance, then hardening only the confirmed gaps.

## Context

The earlier `docs governance Full A+B hardening` work had already cleaned up
README structure, lifecycle document templates, Agent runtime mirrors, the
Hookify local boundary, and the repo quality gate. This work uses that result
as the baseline again, but does not limit the scope to docs and Agent rules; it
compares the full workspace purpose against GitOps, infrastructure contracts,
CI, validation scripts, examples, and external version baselines.

The baseline audit passed repo quality, LLM Wiki freshness, GitOps structure,
and static infrastructure contract validation. The confirmed hardening targets
are external version inventory freshness and explicit live-command deny
boundaries.

## Goals & In-Scope

- **Goals**:
  - Re-audit docs lifecycle, templates, READMEs, Agent governance, hooks, CI, GitOps, and infrastructure contracts against the workspace purpose.
  - Make only small fixes for confirmed drift and preserve the existing SSoT structure.
  - Update the review date and official baseline for the external version snapshot to 2026-05-22.
  - Harden the Claude/Hookify command boundary so it more clearly blocks direct cluster mutation and direct reconciliation.
- **In Scope**:
  - `docs/01.requirements` through `docs/05.operations`
  - `docs/90.references/data`
  - `docs/99.templates`
  - `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/**`, `.codex/**`
  - root, docs, GitOps, infrastructure, scripts, tests, examples README layers
  - repository validation scripts and static CI contracts

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - live k3d bootstrap, ArgoCD sync, Vault write, PostgreSQL/Valkey runtime mutation
  - Changing the Kubernetes manifest desired-state contract
  - Automatically upgrading cloud example version targets
  - Rewriting the meaning of historical PRD/ARD/Spec/Plan/Task documents
- **Out of Scope**:
  - Deploying real AWS/Azure accounts
  - plaintext Kubernetes secret authoring
  - new top-level documentation tree
  - new shared runtime surface without a concrete matrix gap

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Capture full-purpose audit plan and execution evidence | `docs/04.execution/plans`, `docs/04.execution/tasks` | REQ-SDD-001 | Plan/Task follow templates and are indexed |
| PLN-002 | Re-audit docs lifecycle, templates, and README layer | `docs/01.requirements` through `docs/05.operations`, `docs/99.templates`, `**/README.md` | REQ-DOC-001 | Repo quality gate passes with no template drift |
| PLN-003 | Re-audit Agent governance and runtime boundaries | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/**`, `.codex/**`, `docs/00.agent-governance/**` | REQ-AI-001 | Gateway thinness, mirror, hook, and local-rule checks pass |
| PLN-004 | Refresh external version basis without changing desired-state pins | `docs/90.references/data/tech-stack-version-inventory.md` | REQ-REF-001 | Official source date and snapshot notes reflect 2026-05-22 |
| PLN-005 | Harden shared and local advisory command boundaries | `.claude/settings.json`, `.claude/*.local.md` | REQ-HOOK-001 | JSON parse and quality gate pass; local rules remain ignored |
| PLN-006 | Record memory and validation handoff | `docs/00.agent-governance/memory/progress.md` | REQ-MEM-001 | Progress entry includes evidence and limitations |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Repository governance and docs quality gate | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | Static | LLM Wiki generated index freshness | `bash scripts/generate-llm-wiki-index.sh --check` | PASS |
| VAL-PLN-003 | Static | GitOps structure | `bash scripts/validate-gitops-structure.sh` | PASS |
| VAL-PLN-004 | Static | Kubernetes manifests and optional kube-linter | `bash scripts/validate-k8s-manifests.sh .` | PASS, with optional-tool skip reported if applicable |
| VAL-PLN-005 | Static | Secret handling | `bash scripts/check-secret-handling.sh .` | PASS |
| VAL-PLN-006 | Static | Static infrastructure contracts | `bash infrastructure/tests/verify-contracts-static.sh` | PASS |
| VAL-PLN-007 | Static | Runtime hook JSON parse | `python3 -m json.tool .claude/settings.json` and `python3 -m json.tool .codex/hooks.json` | PASS |
| VAL-PLN-008 | Static | Shell syntax | `find infrastructure scripts docs/00.agent-governance/hooks -type f -name '*.sh' -exec bash -n {} +` | PASS |
| VAL-PLN-009 | Static | Diff whitespace sanity | `git diff --check` | PASS |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Full audit becomes broad rewrite | High | Modify only evidence-backed drift and preserve current SSoT layout |
| External latest versions are mistaken for upgrade instructions | Medium | Refresh reference snapshot only; keep desired-state pins unchanged |
| Local Hookify rules are mistaken for shared enforcement | Medium | Keep `.claude/*.local.md` ignored and document shared enforcement in tracked settings/hooks/validators |
| Optional local tools are treated as passed when absent | Medium | Report absent tools as limitations and rely on repo-backed gates plus CI |
| Direct live mutation is normalized by examples | High | Keep direct commands behind human-approved bootstrap or break-glass boundaries |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: repo-static validation commands in this plan must pass.
- **Sandbox / Canary Rollout**: not applicable; no live runtime rollout is included.
- **Human Approval Gate**: required for any direct cluster mutation, ArgoCD forced sync, Vault write, cloud account change, or version pin upgrade outside this plan.
- **Rollback Trigger**: revert this documentation/governance change set if repo quality, static contracts, or JSON parse cannot be restored.
- **Prompt / Model Promotion Criteria**: not applicable; no model or prompt promotion is included.

## Completion Criteria

- [x] Docs lifecycle, templates, README layer, Agent governance, hooks, GitOps, infra contracts, CI, examples, and version references were audited against the workspace purpose.
- [x] External version inventory was refreshed without changing desired-state manifests or cloud example targets.
- [x] Claude direct-command deny boundary and local Hookify advisory wording were aligned.
- [x] Plan/Task evidence and progress memory were updated.
- [x] Verification commands passed or skipped optional tools were reported.

## Related Documents

- Parent Spec: N/A — pre-Spec execution record.
- **Task**: [../tasks/2026-05-22-workspace-purpose-alignment.md](../tasks/2026-05-22-workspace-purpose-alignment.md)
- **Previous Plan**: [./2026-05-22-docs-governance-full-ab-hardening.md](./2026-05-22-docs-governance-full-ab-hardening.md)
- **Templates**: [../../99.templates/README.md](../../99.templates/README.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Agentic Rules**: [../../00.agent-governance/rules/agentic.md](../../00.agent-governance/rules/agentic.md)
- **Version Inventory**: [../../90.references/data/tech-stack-version-inventory.md](../../90.references/data/tech-stack-version-inventory.md)
