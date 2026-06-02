---
title: 'Codex Governance Harness Alignment Plan'
type: plan
status: done
owner: platform
updated: 2026-05-31
---

# Codex Governance Harness Alignment Plan

---

## Overview (KR)

이 문서는 Stage 00 공통 에이전트 거버넌스와 Codex/GPT 하네스를 정합화하기 위한 실행 계획이다.
Phase 1 조사에서 확인한 모델 정책 충돌, Template Contract drift, Codex TOML reasoning-effort 누락,
operations policy frontmatter drift를 Phase 3에서 안전하게 고치는 순서와 검증 기준을 정의한다.

## Context

첨부 작업 지시는 3단계 파이프라인을 요구했다.

- Phase 1: 읽기 전용 조사와 분석.
- Phase 2: 계획 문서 작성만 수행.
- Phase 3: 승인된 계획에 따라 governance, template, config, validation surface를 구현.

Phase 1에서 확인한 주요 사실은 다음과 같다.

- `docs/00.agent-governance/model-policy.md`는 Codex worker를 `GPT-5.4-mini`로 설명하지만,
  `docs/00.agent-governance/harness-catalog.md`와 `.codex/agents/*.toml`은 `gpt-5.3-codex`를 사용한다.
- 사용자는 Codex worker 표준을 `gpt-5.3-codex`로 유지하도록 결정했다.
- `.codex/agents/*.toml`은 `model`만 선언하고 `model_reasoning_effort`를 선언하지 않는다.
- 사용자는 Codex TOML에 `model_reasoning_effort`를 명시하도록 결정했다.
- `AGENTS.md`는 실제로 Codex/GPT provider shim으로 쓰인다.
- 사용자는 `AGENTS.md`를 Codex/GPT 전용 shim으로 정리하도록 결정했다.
- `docs/05.operations/policies/*.md`는 `type: operation`을 사용하지만
  `docs/99.templates/policy.template.md`는 `type: policy`를 요구한다.
- 사용자는 operations policy 문서 frontmatter를 `type: policy`로 정규화하도록 결정했다.
- OpenAI 공식 모델 문서는 `gpt-5.5`, `gpt-5.4-mini`, `gpt-5.3-codex` 모델 ID와 reasoning effort 지원 범위를 현재 문서화한다.

## Goals & In-Scope

- **Goals**:
  - Stage 00이 하나의 공유 governance, QA/CI/CD policy, Template Contract, Model Policy를 갖도록 정리한다.
  - Codex 하네스가 별도 governance를 만들지 않고 Stage 00을 구현하는 adapter임을 명확히 한다.
  - Codex agent TOML의 `model`과 `model_reasoning_effort`가 Stage 00 Model Policy와 검증 스크립트로 추적되게 한다.
  - Policy template, routing skill, edit hook, authored policy 문서의 타입과 경로 명칭을 일관되게 정리한다.
  - Phase 3 변경과 QA/CI/CD 실행 결과를 Plan/Task 문서로 추적 가능하게 만든다.
- **In Scope**:
  - `docs/00.agent-governance/**` governance, provider, hook-routing 문서 정합화.
  - `.codex/CODEX.md`, `.codex/agents/*.toml`, `AGENTS.md` Codex harness 정합화.
  - `.agents/skills/docs-stage-routing/skill.md` policy template routing 보정.
  - `docs/00.agent-governance/hooks/k8s-pre-edit.sh` authored-doc template hint 보정.
  - `docs/05.operations/policies/*.md` frontmatter `type` 정규화.
  - `scripts/validate-repo-quality-gates.sh`에 필요한 static validation 보강.
  - Phase 3 task record와 `docs/00.agent-governance/memory/progress.md` 기록.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Kubernetes manifests, ArgoCD applications, Vault, ESO, live cluster state 변경.
  - 새 runtime agent, 새 skill, 새 docs taxonomy stage 추가.
  - 정책 문서의 운영 의미를 재작성하는 대규모 내용 변경.
  - GitHub Actions job topology 변경.
- **Out of Scope**:
  - 직접 `kubectl apply`, `kubectl patch`, `argocd app sync`, Vault write 실행.
  - secret value 읽기 또는 출력.
  - 기존 완료 계획의 historical evidence 재작성.

## Concept Alignment Plan

| Concept | Current State | Desired State | Planned Action |
| --- | --- | --- | --- |
| Agent | `.agents/` SSoT와 `.claude/agents` primary 표현이 혼재한다. | `.agents/`는 shared content SSoT, provider agent files는 runtime mirrors로 표현한다. | `common-governance.md`, `harness-catalog.md`, `subagent-protocol.md` 용어를 정리한다. |
| Skill | `.codex/skills` symlink와 `.claude/skills` reference가 혼재하고, docs-stage-routing은 `operation.template.md`를 가리킨다. | `.agents/skills` SSoT와 provider symlink 관계를 명확히 하고 policy template을 `policy.template.md`로 통일한다. | `.agents/skills/docs-stage-routing/skill.md`와 catalog routing 문구를 보정한다. |
| Rule | JIT, GitOps-first, Template-first 규칙은 존재하나 AGENTS gateway 설명이 provider 범위와 충돌한다. | 공통 규칙은 Stage 00에 두고 `AGENTS.md`는 Codex/GPT shim으로만 둔다. | `providers/agents-md.md`, `providers/codex.md`, `AGENTS.md` 포인터를 정리한다. |
| Hook | `.codex/hooks.json`은 `docs/00.agent-governance/hooks/*.sh`를 호출하지만 일부 문서는 legacy provider-local hook script paths로 설명했다. | shared hook scripts는 `docs/00.agent-governance/hooks/*.sh`, provider configs는 event wiring으로 표현한다. | `.codex/CODEX.md`, provider docs, hook boundary text를 보정한다. |
| Sub-agent | Codex TOML mirrors exist, but no explicit reasoning-effort policy exists. | `supervisor` and workers declare model and reasoning effort according to Model Policy. | `.codex/agents/*.toml`와 validator를 업데이트한다. |
| Output Style | Common governance says fully supported; catalog says Codex/Gemini are tone-only. | Native support vs behavioral/tone-only support를 분리한다. | `common-governance.md`와 `harness-catalog.md` support matrix를 맞춘다. |
| Workflow | QA/CI/CD workflow exists, but model/config drift is not fully checked. | Phase 3 workflow includes static gates for model and template drift. | `scripts/validate-repo-quality-gates.sh` checks를 추가한다. |
| Memory | `progress.md` ledger exists and is required for repo-changing work. | Phase 3 implementation writes a concise progress entry with evidence. | Task implementation에 `progress.md` update를 포함한다. |
| QA | Repo quality gate passes, but semantic drift is not fully covered. | Validator catches Codex model effort, policy type, and template route drift. | Add focused static checks in quality gate. |
| CI/CD | GitHub Actions runs repo gates; no topology change is needed. | Existing CI inherits strengthened repo quality gate. | No workflow topology change; rely on script hardening. |
| Model Policy | `model-policy.md` conflicts with `harness-catalog.md`. | Top: `gpt-5.5`; Codex worker: `gpt-5.3-codex`; allowed efforts documented. | Update model policy and catalog as one source-aligned pair. |
| Template Contract | `operation.template.md` references remain, while actual template is `policy.template.md`. | Policy docs and routing use `policy.template.md` and `type: policy`. | Update routing skill, hook hint, policy docs, and validator. |

## Codex Model and Reasoning-Effort Assignment

| Codex Agent | Model | Planned `model_reasoning_effort` | Rationale |
| --- | --- | --- | --- |
| `supervisor` | `gpt-5.5` | `xhigh` | Governance routing and multi-agent orchestration are high-risk planning tasks. |
| `code-reviewer` | `gpt-5.3-codex` | `high` | Review findings can block merge and need strong reasoning. |
| `gitops-reviewer` | `gpt-5.3-codex` | `high` | GitOps structure and release safety are cluster-affecting. |
| `k8s-implementer` | `gpt-5.3-codex` | `high` | Kubernetes manifest authoring has operational blast radius. |
| `security-auditor` | `gpt-5.3-codex` | `high` | RBAC, secrets, and network findings are security-sensitive. |
| `incident-responder` | `gpt-5.3-codex` | `high` | Incident reconstruction needs careful causal reasoning. |
| `doc-writer` | `gpt-5.3-codex` | `medium` | Template-aligned documentation is bounded by repo validators. |
| `wiki-curator` | `gpt-5.3-codex` | `medium` | LLM Wiki curation is link-map and reference maintenance work. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Create Phase 3 task record before implementation | `docs/04.execution/tasks/2026-05-31-codex-governance-harness-alignment.md` | G2, Traceability | Task uses `task.template.md`, links this plan, and defines evidence. |
| PLN-002 | Align Stage 00 model policy | `docs/00.agent-governance/model-policy.md`, `docs/00.agent-governance/harness-catalog.md` | G3, Model Policy | Codex worker is `gpt-5.3-codex`; allowed reasoning efforts are documented. |
| PLN-003 | Align Codex harness model config | `.codex/agents/*.toml`, `.codex/CODEX.md` | G3, Codex config correctness | Every TOML declares allowed `model` and `model_reasoning_effort`. |
| PLN-004 | Clarify `AGENTS.md` provider role | `AGENTS.md`, `docs/00.agent-governance/providers/agents-md.md`, `docs/00.agent-governance/providers/codex.md` | G3, Single governance | `AGENTS.md` is Codex/GPT shim and points to shared Stage 00 without duplicating policy. |
| PLN-005 | Normalize hook and provider script references | `.codex/CODEX.md`, `docs/00.agent-governance/providers/*.md`, `docs/00.agent-governance/common-governance.md`, `docs/00.agent-governance/harness-catalog.md` | G3, Hook boundary | Docs consistently describe shared scripts under `docs/00.agent-governance/hooks/*.sh`. |
| PLN-006 | Normalize Template Contract policy naming | `.agents/skills/docs-stage-routing/skill.md`, `docs/00.agent-governance/hooks/k8s-pre-edit.sh`, `docs/00.agent-governance/rules/document-stage-routing.md` | G3, Template Contract | Policy routing uses `docs/99.templates/policy.template.md`; no `operation.template.md` references remain in active routing. |
| PLN-007 | Normalize authored policy frontmatter | `docs/05.operations/policies/*.md` | G3, Template compliance | All policy docs use `type: policy`; no `^type: operation$` remains under policies. |
| PLN-008 | Strengthen repo quality gates for recurring drift | `scripts/validate-repo-quality-gates.sh` | G3, QA and CI/CD | Gate fails on Codex TOML model/effort drift, policy type drift, and active `operation.template.md` routing drift. |
| PLN-009 | Update required indexes and memory | `docs/04.execution/plans/README.md`, `docs/04.execution/tasks/README.md`, `docs/00.agent-governance/memory/progress.md` | Traceability | README indexes are current and progress entry records files changed and verification evidence. |
| PLN-010 | Run validation and record limitations | validation commands below | QA and CI/CD | Required repo-static checks pass or limitations are documented. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Repository quality gate | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | Docs index | LLM Wiki generated index freshness if docs references change | `bash scripts/generate-llm-wiki-index.sh --check` | PASS or not affected with rationale |
| VAL-PLN-003 | Targeted model | Codex worker model remains canonical | `rg -n "GPT-5.4-mini\|gpt-5.4-mini" docs/00.agent-governance .codex AGENTS.md -g '!docs/00.agent-governance/memory/**'` | No active policy/config reference |
| VAL-PLN-004 | Targeted effort | Codex TOML effort fields exist | `rg -n "model_reasoning_effort" .codex/agents` | Eight agent TOMLs report explicit values |
| VAL-PLN-005 | Targeted policy type | Policy docs use policy type | `rg -n "^type: operation$" docs/05.operations/policies` | No output |
| VAL-PLN-006 | Targeted template route | Active routing uses `policy.template.md` | `rg -n "operation\\.template\\.md" .agents docs/00.agent-governance .codex` | No active routing or hook references remain |
| VAL-PLN-007 | Shell syntax | Hook and validator syntax | `bash -n docs/00.agent-governance/hooks/k8s-pre-edit.sh scripts/validate-repo-quality-gates.sh` | PASS |
| VAL-PLN-008 | Diff hygiene | Whitespace and accidental churn | `git diff --check` | PASS |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Model policy wording drifts again between `model-policy.md` and `harness-catalog.md` | High | Make one table authoritative for concrete IDs and add validator coverage for `.codex/agents/*.toml`. |
| `model_reasoning_effort` is not accepted by future Codex TOML schema | Medium | Keep the value explicit only after local TOML parsing and quality gate pass; document as Codex mirror metadata if runtime-native support is behavioral. |
| README sync expands the diff beyond the model/template fix | Medium | Limit README changes to index rows required by file additions or changed document status. |
| Policy frontmatter type change is semantically misread as policy content rewrite | Low | Change only the frontmatter `type`; do not alter policy body semantics. |
| Hook template hint changes affect authored-doc edit warnings | Medium | Run shell syntax and repository hook payload simulation through the quality gate. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: repo-static validators and targeted `rg` checks must pass before handoff.
- **Sandbox / Canary Rollout**: not applicable; this is repository governance/config documentation work.
- **Human Approval Gate**: required before Phase 3 implementation begins, because governance and Codex config will change.
- **Rollback Trigger**: any failing quality gate that cannot be fixed within the approved scope rolls back the affected Phase 3 file set.
- **Prompt / Model Promotion Criteria**: Codex worker remains `gpt-5.3-codex`; `supervisor` remains `gpt-5.5`; reasoning-effort values must be one of the documented allowed values for each model.

## Completion Criteria

- [x] Phase 3 task record exists and links this plan.
- [x] Stage 00 model policy and harness catalog agree on Codex model tiers.
- [x] `.codex/agents/*.toml` declares allowed model and `model_reasoning_effort`.
- [x] `AGENTS.md` is a Codex/GPT shim and does not duplicate shared governance.
- [x] Template routing uses `policy.template.md` for operations policy documents.
- [x] Policy authored docs use `type: policy`.
- [x] Validator covers the recurring drift points.
- [x] Required README and memory updates are complete.
- [x] Verification commands pass or limitations are recorded.

## Related Documents

- [Governance Hub](../../00.agent-governance/README.md)
- [Model Policy](../../00.agent-governance/model-policy.md)
- [Harness Catalog](../../00.agent-governance/harness-catalog.md)
- [Codex Provider Notes](../../00.agent-governance/providers/codex.md)
- [Codex Runtime Baseline](../../../.codex/CODEX.md)
- [Template README](../../99.templates/README.md)
- [Plan Template](../../99.templates/plan.template.md)
- [OpenAI Models](https://developers.openai.com/api/docs/models)
- [GPT-5.5 Model](https://developers.openai.com/api/docs/models/gpt-5.5)
- [GPT-5.3-Codex Model](https://developers.openai.com/api/docs/models/gpt-5.3-codex)
- [Phase 3 Task Record](../tasks/2026-05-31-codex-governance-harness-alignment.md)
