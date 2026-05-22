---
title: 'Docs Governance Full A+B Hardening Plan'
type: plan
status: done
owner: 'platform'
updated: 2026-05-22
---

# Docs Governance Full A+B Hardening Plan

## Overview (KR)

이 문서는 `hy-home.k8s`의 문서 lifecycle, README 템플릿 준수, agent/runtime governance,
hook 경계, repo-static 검증 게이트를 함께 정합화하기 위한 실행 계획서다.

## Context

저장소는 이미 thin gateway, `docs/99.templates` 기반 구조 템플릿, lifecycle hooks,
Claude/Codex runtime mirrors, repo quality gate를 갖추고 있다. 현재 개선의 목적은 새
runtime surface를 늘리는 것이 아니라, 전체 README와 authored lifecycle 문서가 같은
템플릿 규칙을 따르고 그 규칙이 검증 게이트에서 재발 방지되도록 만드는 것이다.

현재 기준선에서 repo quality, LLM Wiki freshness, static contract, GitOps structure,
manifest syntax, secret handling 검증은 통과했다. 발견된 drift는 일부 README의
`Related References` legacy heading, `Link Basis` 누락, Hookify local rule의 공유
집행 경계가 문서와 검증에서 충분히 명확하지 않은 점이다.

## Goals & In-Scope

- **Goals**:
  - 모든 README를 `docs/99.templates/readme.template.md`의 base structure와 맞춘다.
  - `docs/01.requirements`부터 `docs/05.operations`까지의 lifecycle 문서를 템플릿 규칙과 cross-link 기준에 맞춘다.
  - Agent gateway와 runtime hook/mirror 경계를 최신 governance 문서와 검증 게이트에 반영한다.
  - Hookify `.local.md`는 ignored local warning layer로 유지하고, 공유 집행은 tracked hooks와 quality gate가 소유하게 한다.
- **In Scope**:
  - `docs/99.templates/**`
  - root, docs, gitops, infrastructure, scripts, tests, traefik, examples 하위 `README.md`
  - `docs/01.requirements/**`, `docs/02.architecture/**`, `docs/03.specs/**`, `docs/04.execution/**`, `docs/05.operations/**`
  - `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/**`, `.codex/**`, `docs/00.agent-governance/**`
  - `scripts/validate-repo-quality-gates.sh`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - live k3d, ArgoCD, Vault, PostgreSQL, Valkey runtime mutation
  - direct `kubectl apply`, ArgoCD forced sync, external secret write
  - historical PRD/ARD/Plan/Task의 의미 재작성
  - new top-level documentation tree or new provider-native instruction layer
- **Out of Scope**:
  - AWS/Azure 실제 계정 또는 cluster 상태 변경
  - application business logic implementation
  - plaintext Kubernetes secret authoring

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Capture audit snapshot and implementation evidence docs | `docs/04.execution/plans`, `docs/04.execution/tasks` | REQ-DOC-001 | Plan/Task created from templates |
| PLN-002 | Tighten README template and template inventory guidance | `docs/99.templates/**` | REQ-TPL-001 | Template references and mapping remain valid |
| PLN-003 | Normalize all README files to canonical heading and link-basis rules | `**/README.md` | REQ-DOC-002 | No `## Related References`; no README missing `## Link Basis` |
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
| VAL-PLN-007 | Static | Shell syntax | `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` | No syntax errors |
| VAL-PLN-008 | Static | Runtime JSON parse | `python3 -m json.tool .claude/settings.json` and `python3 -m json.tool .codex/hooks.json` | PASS |
| VAL-PLN-009 | Static | Whitespace and patch sanity | `git diff --check` | PASS |
| VAL-PLN-010 | Targeted | README heading migration | `rg -n "^## Related References$" -g "README.md"` and `rg --files-without-match "^## Link Basis$" -g "README.md"` | No output |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Historical docs are rewritten as current contracts | High | Limit historical documents to structure, links, metadata, and humanized wording without changing decision meaning |
| README normalization breaks relative links | Medium | Recalculate links from each README location and run repository link checks |
| Hookify local rules are mistaken for shared enforcement | Medium | Keep `.claude/*.local.md` ignored and untracked; document tracked hooks as shared enforcement |
| Validator becomes stricter than current docs | Medium | Apply README/template fixes before tightening the gate |
| Live cluster status is confused with repo-static readiness | Low | Keep live k3d/ArgoCD checks out of completion criteria and report the boundary |

## Agent Rollout & Evaluation Gates (If Applicable)

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

## Related Documents

- **Task**: [../tasks/2026-05-22-docs-governance-full-ab-hardening.md](../tasks/2026-05-22-docs-governance-full-ab-hardening.md)
- **Templates**: [../../99.templates/README.md](../../99.templates/README.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Agentic Rules**: [../../00.agent-governance/rules/agentic.md](../../00.agent-governance/rules/agentic.md)
