---
title: 'Stage 00 Canonical Adapter Redesign Plan'
type: plan
status: done
owner: platform
updated: 2026-06-01
---

# Stage 00 Canonical Adapter Redesign Implementation Plan

---

## Overview (KR)

이 문서는 Stage 00 agent governance를 canonical adapter 모델로 재설계하기 위한 실행 계획서다.
Phase 1 조사에서 확인한 governance, provider harness, hook, template, model policy, QA/CI,
skill/workflow, local runtime drift를 변경 단위별로 분리하고, Phase 3에서 어떤 순서와 검증
기준으로 보정할지 정의한다.

Phase 2의 산출물은 이 계획과 Plan stage 인덱스 갱신이다. 실제 governance, template,
provider config, hook, validator 변경은 Phase 3에서 별도 task record를 만든 뒤 수행한다.

## Context

현재 Stage 00은 이미 공통 governance와 provider별 adapter 구조를 갖고 있지만, "무엇이 정본이고
무엇이 adapter mirror인가"를 한 장의 canonical contract로 설명하지 못한다. 그 결과 같은 규칙이
여러 문서에 반복되고, 일부 문서가 과거 경로나 provider-specific 표현을 active contract처럼
노출한다.

### Upstream Traceability Overlay (2026-06-01)

이 계획은 처음 작성될 때 Phase 1 조사 결과를 직접 입력으로 삼은 governance plan이었다.
현재 upstream SDD 추적성은
[Workspace Agent Governance Platform PRD](../../01.requirements/2026-06-01-workspace-agent-governance-platform.md),
[Workspace Agent Governance Platform ARD](../../02.architecture/requirements/0006-workspace-agent-governance-platform.md),
and [ADR-0013](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)이 소유한다.
이 overlay는 기존 Phase 2/Phase 3 증적을 소급 재작성하지 않고 현재 요구/아키텍처 링크만 보강한다.

Phase 1 조사에서 확인한 핵심 gap은 다음과 같다.

| Gap ID | Finding | Desired Direction |
| --- | --- | --- |
| GAP-001 | `common-governance.md`, `harness-catalog.md`, `model-policy.md`, documentation rules가 Stage 00 ownership을 반복 설명한다. | Stage 00 canonical adapter ownership map을 만들고 문서별 책임을 단일화한다. |
| GAP-002 | Template routing, documentation protocol, hook guidance가 서로 다른 위치에서 반복된다. | Template Contract 정본과 provider/hook adapter 책임을 분리한다. |
| GAP-003 | 실제 shared hook scripts는 `docs/00.agent-governance/hooks/*.sh`인데 일부 docs는 `.claude/hooks/*.sh`를 참조한다. | shared hook path와 provider event wiring을 명확히 나눈다. |
| GAP-004 | `.agents/hooks.json`의 실제 역할과 문서상 placeholder/behavioral 표현이 어긋난다. | Gemini/Antigravity adapter의 실제 hook support 상태를 disk evidence 기준으로 정리한다. |
| GAP-005 | Subagent readiness가 `common-governance.md`와 `harness-catalog.md`에서 다르게 표현된다. | provider-specific native support, mirror support, behavioral support를 별도 status로 표현한다. |
| GAP-006 | `.agents/skills` SSoT와 `.claude/skills` symlink/mirror 표현이 문서마다 다르다. | shared asset SSoT와 provider adapter mount를 canonical schema에 포함한다. |
| GAP-007 | Model policy가 `model-policy.md`, `harness-catalog.md`, provider config에 중복된다. | concrete model ID 정본과 provider config verification 위치를 분리한다. |
| GAP-008 | Model tier 용어에서 `top`, `supervisor`, `worker`, review/security usage가 혼재한다. | tier vocabulary와 exception rule을 한곳에 고정한다. |
| GAP-009 | `docs/00.agent-governance/README.md`가 hooks, model policy, common governance, Codex provider entry를 빠뜨린다. | Stage 00 README를 canonical entry map으로 보강한다. |
| GAP-010 | `.codex/rules/`는 placeholder이고 shared rules는 `.agents/rules`와 Stage 00에 있다. | Codex adapter가 shared rules를 어떻게 로드하는지 명확히 한다. |
| GAP-011 | `.agents/workflows/qa-cicd-workflow.md`가 Gemini/Antigravity 중심 표현으로 Codex에도 노출된다. | workflow body를 provider-neutral로 만들거나 adapter boundary를 명시한다. |
| GAP-012 | `workspace-harness-audit` skill은 현재 task에 맞지만 catalog routing은 외부 skill만 노출한다. | repo-local skill routing과 external skill availability ledger를 보강한다. |
| GAP-013 | pre-commit, post-validate, CI guide가 실제 shared hook path와 GitHub Actions job name을 완전히 따라가지 못한다. | validator, pre-commit coverage, CI documentation을 같은 QA contract로 묶는다. |
| GAP-014 | Templates의 owner/status/lifecycle/headings가 authored docs와 일부 어긋난다. | template defaults와 lifecycle vocabulary를 문서 stage별로 정리한다. |
| GAP-015 | branch completion workflow가 Stage 00 git/postflight strategy로 정리되어 있지 않다. | finishing-a-development-branch strategy를 git/postflight workflow에 통합한다. |
| GAP-016 | `/home/hy/.local/bin/{node,npm,rtk}`는 존재하지만 `rtk`가 PATH에 없고 `rtk gain` DB 초기화가 실패한다. | local runtime discovery, PATH, RTK DB failure를 Codex/runtime baseline에서 재현 가능한 점검으로 남긴다. |
| GAP-017 | 2026-05-30 active plans/tasks와 2026-05-31/2026-06-01 completed follow-up이 일부 중첩된다. | 새 canonical adapter plan으로 변경 단위를 재분류하고, 기존 active 계획은 Phase 3에서 close/supersede 여부를 판단한다. |

## Goals & In-Scope

- **Goals**:
  - Stage 00을 `canonical core + provider adapter + validation evidence` 모델로 재정의한다.
  - 공통 규칙, template contract, model policy, skill/workflow routing, hook/QA contract의 정본 위치를 분리한다.
  - Claude, Codex/GPT, Gemini/Antigravity가 같은 Stage 00 contract를 각 runtime 특성에 맞게 수행하도록 adapter 책임을 명시한다.
  - Phase 1 gap을 변경 단위별로 쪼개서 Phase 3 구현 순서와 검증 기준을 만든다.
  - 기존 active/stale 계획과 task를 무단 재작성하지 않고, supersede/close 판단을 Phase 3 task evidence로 남긴다.
- **In Scope**:
  - `docs/00.agent-governance/**` canonical ownership, provider notes, rules, hook, model, catalog 문서 정합화 계획.
  - `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.codex/CODEX.md`, `.claude/CLAUDE.md`, `.agents/GEMINI.md` adapter boundary 정합화 계획.
  - `.agents/skills`, `.agents/workflows`, provider skill/workflow mirrors의 SSoT/mirror 관계 정리 계획.
  - `docs/99.templates/**` template lifecycle, owner/status, heading contract 보강 계획.
  - `scripts/validate-repo-quality-gates.sh`, `.pre-commit-config.yaml`, hook scripts, CI docs의 static validation 보강 계획.
  - `/home/hy/.local/bin` runtime tool discovery와 `rtk` availability failure 조사 계획.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Phase 2에서 governance, template, provider config, hook, validation script를 직접 수정하지 않는다.
  - 새 docs taxonomy stage, 새 runtime provider, 새 agent role을 추가하지 않는다.
  - 기존 historical plan/task evidence를 소급 편집하지 않는다.
  - 모델 정책을 비공식 추정으로 갱신하지 않는다.
- **Out of Scope**:
  - Kubernetes manifest, ArgoCD application, Vault, External Secrets, live cluster state 변경.
  - secret value 읽기, 출력, commit, PR description 포함.
  - GitHub Actions topology 변경이나 deployment/publish action.
  - Phase 3 승인 전 destructive git operation, rebase, reset, force-push, merge.

## Canonical Adapter Model

| Layer | Canonical Responsibility | Adapter Responsibility | Evidence / Validation |
| --- | --- | --- | --- |
| Stage 00 Core | Governance principles, scope rules, template routing, model/tier policy, QA contract. | Provider docs import the core and state only runtime-specific differences. | `docs/00.agent-governance/**`, repo quality gate. |
| Shared Assets | Shared agents/skills/rules/workflows/output-styles ownership and lifecycle. | `.claude`, `.codex`, `.agents` expose native files, symlinks, or behavioral mirrors. | Harness catalog, subagent protocol, provider configs. |
| Provider Adapter | Runtime-specific loading order, model config, tool permissions, hook/event wiring. | Claude, Codex/GPT, Gemini/Antigravity each document native support vs mirror support. | Provider notes, runtime baseline files, static drift checks. |
| Template Contract | Stage-to-template mapping, required headings, owner/status vocabulary, link basis. | Doc-writer agents and hooks use the same routing without redefining it. | `docs/99.templates/**`, stage routing skill, hook hint checks. |
| QA/CI Contract | Local static checks, pre-commit coverage, CI job naming, postflight expectations. | Provider postflight instructions call the same smallest relevant gates. | `scripts/validate-repo-quality-gates.sh`, CI docs, task evidence. |
| Completion Strategy | Branch finishing, PR readiness, cleanup boundaries, explicit discard confirmation. | Provider-specific handoff text follows the common postflight/git strategy. | `rules/git-workflow.md`, `rules/postflight-checklist.md`, task record. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Create Phase 3 task record and freeze implementation scope before edits | `docs/04.execution/tasks/2026-06-01-stage-00-canonical-adapter-redesign.md`, `docs/04.execution/tasks/README.md` | REQ-CAN-001 | Task uses `task.template.md`, links this plan, and states Phase 3 approval/scope boundaries. |
| PLN-002 | Define Stage 00 canonical ownership map | `docs/00.agent-governance/README.md`, `docs/00.agent-governance/common-governance.md`, `docs/00.agent-governance/harness-catalog.md` | REQ-CAN-002 | README lists hooks, model policy, common governance, Codex provider notes, and each doc has a non-overlapping responsibility. |
| PLN-003 | Consolidate Template Contract routing | `docs/00.agent-governance/rules/document-stage-routing.md`, `docs/00.agent-governance/rules/documentation-protocol.md`, `docs/99.templates/README.md`, `.agents/skills/docs-stage-routing/skill.md` | REQ-CAN-003 | One active mapping exists for each stage; provider/hook docs link to it instead of duplicating rules. |
| PLN-004 | Normalize provider gateway and adapter loading semantics | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.codex/CODEX.md`, `.claude/CLAUDE.md`, `.agents/GEMINI.md`, `docs/00.agent-governance/providers/*.md` | REQ-CAN-004 | Root gateways stay thin; provider files describe native support, mirror support, hook support, and limitations consistently. |
| PLN-005 | Reconcile hook path and event wiring drift | `docs/00.agent-governance/hooks/*.sh`, `.codex/hooks.json`, `.agents/hooks.json`, provider docs, `docs/00.agent-governance/rules/postflight-checklist.md` | REQ-CAN-005 | Active docs refer to shared hook scripts under `docs/00.agent-governance/hooks/*.sh`; provider configs are described as event wiring. |
| PLN-006 | Reconcile subagent, skill, workflow, and output-style status vocabulary | `docs/00.agent-governance/common-governance.md`, `docs/00.agent-governance/harness-catalog.md`, `docs/00.agent-governance/subagent-protocol.md`, `.agents/skills`, `.agents/workflows`, `.codex/skills`, `.claude/skills` | REQ-CAN-006 | Matrices distinguish native, mirror/symlink, behavioral, partial, and missing support without contradiction. |
| PLN-007 | Normalize model policy and tier vocabulary after official verification | `docs/00.agent-governance/model-policy.md`, `docs/00.agent-governance/harness-catalog.md`, provider agent configs | REQ-CAN-007 | Concrete model IDs and allowed effort/tier vocabulary match official provider docs and local configs. |
| PLN-008 | Harden QA/CI static gates for canonical adapter drift | `scripts/validate-repo-quality-gates.sh`, `.pre-commit-config.yaml`, `docs/00.agent-governance/hooks/post-validate.sh`, `.github/ABOUT.md`, `.github/workflows/ci.yml` | REQ-CAN-008 | Shared hook path, pre-commit file coverage, CI job names, model/config drift, and template routing drift are checked or explicitly documented. |
| PLN-009 | Update template lifecycle and required metadata contract | `docs/99.templates/*.template.md`, `docs/99.templates/README.md`, `docs/00.agent-governance/rules/stage-checklists.md`, `docs/00.agent-governance/rules/stage-authoring-matrix.md` | REQ-CAN-009 | Templates use consistent owner/status vocabulary and each stage documents required vs optional headings. |
| PLN-010 | Integrate branch completion strategy into Stage 00 workflow | `docs/00.agent-governance/rules/git-workflow.md`, `docs/00.agent-governance/rules/postflight-checklist.md`, provider docs, relevant local skills/workflows if needed | REQ-CAN-010 | Completion flow includes verification, base branch detection, PR/merge/keep/discard options, cleanup boundaries, and typed destructive confirmation. |
| PLN-011 | Investigate local runtime PATH and RTK availability | `.codex/CODEX.md`, `RTK.md`, provider runtime docs, task evidence | REQ-CAN-011 | Phase 3 records `command -v rtk`, `/home/hy/.local/bin/rtk --version`, PATH expectations, and the `rtk gain` DB failure cause or limitation. |
| PLN-012 | Reconcile active/stale plans and tasks without rewriting history | `docs/04.execution/plans/2026-05-30-common-agent-governance-refactoring.md`, `docs/04.execution/tasks/2026-05-30-governance-refactoring.md`, README indexes | REQ-CAN-012 | Existing active items are either left active with a clear remaining scope or marked superseded/done with dated evidence in Phase 3. |
| PLN-013 | Update traceability records after implementation | `docs/04.execution/plans/README.md`, `docs/04.execution/tasks/README.md`, `docs/00.agent-governance/memory/progress.md` | REQ-CAN-013 | README indexes and progress ledger identify files changed, checks run, limitations, and no-live-cluster boundary. |

## Change Unit Split

| Change Unit | Scope | Depends On | Phase 3 Commit Boundary |
| --- | --- | --- | --- |
| CU-001 Canonical Ownership | Stage 00 README, common governance, harness catalog responsibility map. | PLN-001 | One docs-only commit. |
| CU-002 Template Contract | Stage routing, documentation protocol, template README, routing skill. | CU-001 | One docs/skill commit with template validation. |
| CU-003 Provider Adapter Gateways | Root shims, provider notes, runtime baselines. | CU-001, CU-002 | One adapter docs commit. |
| CU-004 Hook and QA Contract | Shared hook path docs, post-validate coverage, pre-commit coverage, CI guide naming. | CU-003 | One validator/config/docs commit. |
| CU-005 Model Policy | Model policy, tier vocabulary, provider config verification. | CU-001 | One model-policy commit after official docs check. |
| CU-006 Skills and Workflows | Skill routing, external path availability, provider-neutral workflow wording. | CU-001 | One docs/asset catalog commit. |
| CU-007 Template Lifecycle | Owner/status defaults and stage heading requirements. | CU-002 | One template contract commit. |
| CU-008 Branch Completion | Git workflow and postflight completion strategy. | CU-003 | One workflow docs commit. |
| CU-009 Local Toolchain | `/home/hy/.local/bin` PATH and RTK DB investigation. | PLN-001 | One runtime baseline/task evidence commit, only if docs changes are needed. |
| CU-010 Plan/Task Reconciliation | Supersede/close overlapping 2026-05-30 records where evidence supports it. | CU-001-CU-009 | One traceability commit. |
| CU-011 Validation Evidence | README indexes, progress ledger, final quality gate evidence. | All prior CUs | Final traceability commit. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Phase 2 plan and README index pass repository governance checks | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | Diff hygiene | No whitespace or conflict marker issues | `git diff --check` | PASS |
| VAL-PLN-003 | Plan routing | New plan is discoverable from Plan README | `rg -n "stage-00-canonical-adapter-redesign" docs/04.execution/plans/README.md docs/04.execution/plans/2026-06-01-stage-00-canonical-adapter-redesign.md` | Both README and plan file are reported. |
| VAL-PLN-004 | Wiki index | LLM Wiki generated index remains fresh if doc references require it | `bash scripts/generate-llm-wiki-index.sh --check` | PASS or documented as not affected. |
| VAL-CAN-001 | Official model source | Provider model IDs and effort/tier claims are verified before Phase 3 edits | Official provider docs review plus local config scan | No model policy change is made from stale memory alone. |
| VAL-CAN-002 | Hook path drift | Shared hook path is the only active script path in docs/config after Phase 3 | `rg -n "\\.claude/hooks\|docs/00.agent-governance/hooks" docs .codex .agents .claude` | `.claude/hooks` appears only as historical/negative context, if at all. |
| VAL-CAN-003 | Template drift | Active routing has one template target per stage | `rg -n "operation\\.template\\.md\|policy\\.template\\.md\|plan\\.template\\.md" docs/00.agent-governance .agents .codex .claude docs/99.templates` | No stale active routing target remains. |
| VAL-CAN-004 | QA/CI drift | Local static gates cover shared hooks and CI docs match actual job names | `bash scripts/validate-repo-quality-gates.sh .` | Gate catches path/job drift or docs explain intentional exceptions. |
| VAL-CAN-005 | Local runtime | RTK and local toolchain availability are reproducibly documented | `command -v rtk`; `/home/hy/.local/bin/rtk --version`; `/home/hy/.local/bin/rtk gain` | PATH status, version, and DB result are recorded without exposing secrets. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Canonical adapter rewrite becomes a broad style refactor | High | Keep Phase 3 commits by CU boundary and require each changed line to map to a gap or validation rule. |
| Existing active plans are rewritten as if their historical evidence were wrong | Medium | Preserve historical content; add dated supersede/closure notes only when current evidence supports it. |
| Provider-specific native behavior is collapsed into a false common denominator | High | Matrices must distinguish native, mirror/symlink, behavioral, partial, and missing support. |
| Model policy is updated from stale assumptions | High | Verify current official provider documentation immediately before Phase 3 model-policy edits. |
| Validator hardening blocks unrelated work due to over-broad checks | Medium | Prefer targeted checks for documented drift classes; add explicit exceptions only with rationale. |
| RTK investigation touches credentials or private runtime state | High | Do not read auth files, shell history, tokens, or private DB contents; record only command availability and error class. |
| Branch completion guidance encourages destructive cleanup | High | Require explicit user approval and typed confirmation for discard/reset/delete actions. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Phase 3 starts with a task record and ends each CU with targeted `rg` checks plus `bash scripts/validate-repo-quality-gates.sh .`.
- **Sandbox / Canary Rollout**: Not applicable for live infrastructure. This plan affects repository governance, templates, adapter docs, hooks, and validators only.
- **Human Approval Gate**: Required before Phase 3 implementation, before external network verification beyond official docs, and before any destructive git or filesystem action.
- **Rollback Trigger**: If a CU introduces contradictory provider support claims, stale model IDs, broken template routing, or failing quality gates that cannot be fixed in scope, revert only that CU's files and keep the gap open in the task record.
- **Prompt / Model Promotion Criteria**: Model/tier changes require official provider documentation evidence, local config parity, and validator coverage; no promotion is accepted from memory or preference alone.
- **Branch Completion Gate**: Before PR/merge handoff, verify status, base branch, relevant tests, branch diff, and present explicit keep/PR/merge/discard options. Destructive discard requires typed confirmation.

## Completion Criteria

- [x] Phase 3 task record exists and links this plan.
- [x] Stage 00 canonical ownership map is documented and indexed.
- [x] Provider gateway files are thin adapters and do not duplicate common governance.
- [x] Hook path, event wiring, skill/workflow, and output-style support states are consistent across docs.
- [x] Model policy, harness catalog, and provider configs agree after official source verification.
- [x] Template owner/status/lifecycle and required heading contracts are consistent across `docs/99.templates`.
- [x] QA/CI gates cover the recurring drift classes found in Phase 1.
- [x] Local RTK/PATH limitation is recorded with a concrete follow-up boundary.
- [x] Overlapping 2026-05-30 plans/tasks have a dated superseded status rationale.
- [x] Required README indexes, task evidence, and progress ledger are updated.
- [x] No live cluster, secret, deployment, or destructive git action was performed without explicit approval.

## Related Documents

- **PRD**: [../../01.requirements/2026-06-01-workspace-agent-governance-platform.md](../../01.requirements/2026-06-01-workspace-agent-governance-platform.md)
- **ARD**: [../../02.architecture/requirements/0006-workspace-agent-governance-platform.md](../../02.architecture/requirements/0006-workspace-agent-governance-platform.md)
- **ADR**: [../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)
- **Task**: [../tasks/2026-06-01-stage-00-canonical-adapter-redesign.md](../tasks/2026-06-01-stage-00-canonical-adapter-redesign.md)
- **Prior Active Plan**: [./2026-05-30-common-agent-governance-refactoring.md](./2026-05-30-common-agent-governance-refactoring.md)
- **Codex Follow-up Plan**: [./2026-05-31-codex-governance-harness-alignment.md](./2026-05-31-codex-governance-harness-alignment.md)
- **Claude Surface Plan**: [./2026-06-01-claude-agent-surface-restoration.md](./2026-06-01-claude-agent-surface-restoration.md)
- **Governance Hub**: [../../00.agent-governance/README.md](../../00.agent-governance/README.md)
- **Common Governance**: [../../00.agent-governance/common-governance.md](../../00.agent-governance/common-governance.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Model Policy**: [../../00.agent-governance/model-policy.md](../../00.agent-governance/model-policy.md)
- **Document Stage Routing**: [../../00.agent-governance/rules/document-stage-routing.md](../../00.agent-governance/rules/document-stage-routing.md)
- **Postflight Checklist**: [../../00.agent-governance/rules/postflight-checklist.md](../../00.agent-governance/rules/postflight-checklist.md)
- **Git Workflow**: [../../00.agent-governance/rules/git-workflow.md](../../00.agent-governance/rules/git-workflow.md)
- **Template README**: [../../99.templates/README.md](../../99.templates/README.md)
- **Plan Template**: [../../99.templates/plan.template.md](../../99.templates/plan.template.md)
- **RTK Runtime Notes**: [../../../RTK.md](../../../RTK.md)
- **Codex Runtime Baseline**: [../../../.codex/CODEX.md](../../../.codex/CODEX.md)
- **OpenAI Models**: [https://developers.openai.com/api/docs/models](https://developers.openai.com/api/docs/models)
- **OpenAI Reasoning Guide**: [https://developers.openai.com/api/docs/guides/reasoning](https://developers.openai.com/api/docs/guides/reasoning)
- **GPT-5.3-Codex Model**: [https://developers.openai.com/api/docs/models/gpt-5.3-codex](https://developers.openai.com/api/docs/models/gpt-5.3-codex)
