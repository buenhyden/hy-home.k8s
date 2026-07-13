---
title: 'Docs Governance Full A+B Hardening Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-13
---

# Docs Governance Full A+B Hardening Plan

## Overview

This document is the implementation plan for aligning the `hy-home.k8s`
documentation lifecycle, README template conformance, agent/runtime
governance, hook boundaries, and repo-static validation gates.

## Context

The repository already has thin gateways, structure templates based on
`docs/99.templates`, lifecycle hooks, Claude/Codex runtime mirrors, and a repo
quality gate. The purpose of this improvement is not to add new runtime
surface; it ensures every README and authored lifecycle document follows the
same template rules and that the validation gate prevents recurrence.

At the current baseline, repo quality, LLM Wiki freshness, static contract,
GitOps structure, manifest syntax, and secret-handling checks passed. The
detected drift is limited to legacy `deprecated README heading` headings in some
README files, missing `Link Basis` sections, and insufficient clarity around
the shared enforcement boundary for Hookify local rules in docs and validation.

## Goals & In-Scope

- **Goals**:
  - Align every README with the base structure in `docs/99.templates/templates/common/readme.template.md`.
  - Align lifecycle documents from `docs/01.requirements` through `docs/05.operations` with template rules and cross-link criteria.
  - Reflect Agent gateway and runtime hook/mirror boundaries in the latest governance docs and validation gates.
  - Keep Hookify `.local.md` as an ignored local warning layer, while tracked hooks and the quality gate own shared enforcement.
- **In Scope**:
  - `docs/99.templates/**`
  - `README.md` files under root, docs, gitops, infrastructure, scripts, tests, traefik, and examples
  - `docs/01.requirements/**`, `docs/02.architecture/**`, `docs/03.specs/**`, `docs/04.execution/**`, `docs/05.operations/**`
  - `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/**`, `.codex/**`, `docs/00.agent-governance/**`
  - `scripts/validate-repo-quality-gates.sh`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - live k3d, ArgoCD, Vault, PostgreSQL, Valkey runtime mutation
  - direct `kubectl apply`, ArgoCD forced sync, external secret write
  - Rewriting the meaning of historical PRD/ARD/Plan/Task documents
  - new top-level documentation tree or new provider-native instruction layer
- **Out of Scope**:
  - Changing real AWS/Azure accounts or cluster state
  - application business logic implementation
  - plaintext Kubernetes secret authoring

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Capture audit snapshot and implementation evidence docs | `docs/04.execution/plans`, `docs/04.execution/tasks` | REQ-DOC-001 | Plan/Task created from templates |
| PLN-002 | Tighten README template and template inventory guidance | `docs/99.templates/**` | REQ-TPL-001 | Template references and mapping remain valid |
| PLN-003 | Normalize all README files to canonical heading and link-basis rules | `**/README.md` | REQ-DOC-002 | No `## deprecated README heading`; no README missing `## Link Basis` |
| PLN-004 | Align lifecycle docs with template headings and cross-links while preserving historical meaning | `docs/01.requirements` through `docs/05.operations` | REQ-DOC-003 | Required heading, residue, and link scans pass |
| PLN-005 | Clarify agent/runtime and Hookify ownership boundaries | `docs/00.agent-governance/**`, `.claude/**`, `.codex/**` | REQ-AI-001 | Runtime mirror and hook boundary checks pass |
| PLN-006 | Harden repo quality gate for README and Hookify rules | `scripts/validate-repo-quality-gates.sh` | REQ-VAL-001 | Quality gate fails on legacy README/hook drift and passes current tree |
| PLN-007 | Record memory, release summary, and validation evidence | `docs/00.agent-governance/memory/progress.md` | REQ-MEM-001 | Progress entry includes evidence and handoff |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Repository quality gate | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | Static | LLM Wiki generated index freshness | `bash scripts/generate-llm-wiki-index.sh --check` | PASS |
| VAL-PLN-003 | Static | Static infrastructure contracts | `bash infrastructure/tests/verify-contracts-static.sh` | PASS |
| VAL-PLN-004 | Static | GitOps structure | `bash scripts/validate-gitops-structure.sh` | PASS |
| VAL-PLN-005 | Static | Kubernetes manifest syntax and optional kube-linter | `bash scripts/validate-k8s-manifests.sh .` | PASS or kube-linter-only skip |
| VAL-PLN-006 | Static | Secret handling | `bash scripts/check-secret-handling.sh .` | PASS |
| VAL-PLN-007 | Static | Shell syntax | `find infrastructure scripts docs/00.agent-governance/hooks -type f -name '*.sh' -exec bash -n {} +` | No syntax errors |
| VAL-PLN-008 | Static | Runtime JSON parse | `python3 -m json.tool .claude/settings.json` and `python3 -m json.tool .codex/hooks.json` | PASS |
| VAL-PLN-009 | Static | Whitespace and patch sanity | `git diff --check` | PASS |
| VAL-PLN-010 | Targeted | README heading migration | `rg -n "^## deprecated README heading$" -g "README.md"` and `rg --files-without-match "^## Link Basis$" -g "README.md"` | No output |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Historical docs are rewritten as current contracts | High | Limit historical documents to structure, links, metadata, and humanized wording without changing decision meaning |
| README normalization breaks relative links | Medium | Recalculate links from each README location and run repository link checks |
| Hookify local rules are mistaken for shared enforcement | Medium | Keep `.claude/*.local.md` ignored and untracked; document tracked hooks as shared enforcement |
| Validator becomes stricter than current docs | Medium | Apply README/template fixes before tightening the gate |
| Live cluster status is confused with repo-static readiness | Low | Keep live k3d/ArgoCD checks out of completion criteria and report the boundary |

### Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: repo-static verification commands in this plan must pass.
- **Sandbox / Canary Rollout**: not applicable; no runtime rollout is included.
- **Human Approval Gate**: required for any live cluster mutation, secret write, or new runtime surface outside this plan.
- **Rollback Trigger**: revert this documentation/governance change set if the quality gate or static validation cannot be restored.
- **Prompt / Model Promotion Criteria**: not applicable; no model change is included.

## Completion Criteria

- [x] All README files use `## Related Documents`.
- [x] All README files include `## Link Basis`.
- [x] `docs/99.templates` and generated documents are aligned without template residue.
- [x] Agent gateway/runtime/hook boundaries are current and non-duplicative.
- [x] Hookify `.local.md` files remain ignored local warnings, not tracked shared policy.
- [x] Repo-static validation commands pass or documented optional-tool limitations are reported.
- [x] `docs/00.agent-governance/memory/progress.md` records evidence and handoff.

## Traceability

- Parent Spec: N/A — pre-Spec execution record.
- **Task**: [../tasks/2026-05-22-docs-governance-full-ab-hardening.md](../tasks/2026-05-22-docs-governance-full-ab-hardening.md)
- **Templates**: [../../99.templates/README.md](../../99.templates/README.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Agentic Rules**: [../../00.agent-governance/rules/agentic.md](../../00.agent-governance/rules/agentic.md)
