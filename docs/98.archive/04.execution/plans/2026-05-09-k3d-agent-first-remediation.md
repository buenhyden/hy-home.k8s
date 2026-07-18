---
title: "Archive Record: k3d Workspace and Agent-first Remediation Implementation Plan"
type: "content/archive"
status: "archived"
owner: "platform"
updated: "2026-06-02"
original_type: "plan"
original_path: "docs/04.execution/plans/2026-05-09-k3d-agent-first-remediation.md"
archived_on: "2026-06-02"
archive_reason: "superseded"
replacement: "docs/04.execution/plans/2026-06-02-current-implementation-docs-alignment.md"
source_commit: "5e0221525450dbdacb585e6c98ade3f060ddc827"
source_blob: "824e8aa7899cae6ac02a4b43901eb2c55aa44a9d"
content_sha256: "bd0b22c7e2478a0241d38c0f2d397ca4c5ec654d7b1b1724334aa524166d3cfe"
---
<!-- archive-envelope:v1 payload=rest-of-file encoding=git-blob-bytes -->
---
title: 'k3d Workspace and Agent-first Remediation Implementation Plan'
type: plan
status: done
owner: 'platform'
updated: 2026-05-22
---

# k3d Workspace and Agent-first Remediation Plan

## Overview (KR)

이 문서는 `hy-home.k8s`의 k3d 운영 문서와 Agent-first 실행 계약을 보정하기 위한 실행 계획서다.
작업 분해, 검증, 롤아웃, 위험 관리, 완료 기준을 정의한다.

## Context

현재 저장소는 k3d/k3s, ArgoCD App-of-Apps, ESO/Vault, 외부 PostgreSQL/Valkey/Observability 계약, Headlamp, Istio/Kiali, Rollouts, CI/pre-commit, `.claude`/`.codex` 하네스를 갖추고 있다.

문서 taxonomy도 `docs/01.requirements`부터 `docs/05.operations/incidents`, `docs/90.references`, `docs/99.templates`까지 정리되어 있어 k3d 운영과 Agent-first 협업에 적절하다. 남은 문제는 구조 부족이 아니라 일부 가이드/운영/런북 문서에서 직접 `kubectl apply`/`kubectl patch` 절차가 기본 경로처럼 보이는 점과, 하네스 readiness를 한눈에 확인하기 어렵다는 점이다.

2026-05-09 추가 audit 결과, `AGENTS.md`, root `CLAUDE.md`, `GEMINI.md`, `.claude/CLAUDE.md`, local agents/skills, `.codex` mirrors, `docs/00.agent-governance/**`는 thin gateway, JIT governance, GitOps-first, mirror validation 구조를 이미 갖추고 있다. 따라서 추가 보정은 새 runtime surface 생성이 아니라 current catalog clarity와 regression gate 강화로 제한한다.

2026-05-09 하네스/Agent-first 구성요소 추가 조사 결과, 부족한 부분은 새 agent, skill, hook, script, workflow, manifest가 아니라 조사 결과를 명시적으로 남기는 audit matrix와 matrix-first 회귀 방지 기준이다.

2026-05-09 command-boundary follow-up 결과, 남은 구현 대상은 authored docs 안의 `kubectl apply/patch`, `argocd app sync`, `vault kv put`, direct `git push` 예시가 Agent 기본 실행 경로로 오해되지 않도록 문서 문맥과 repo quality gate를 함께 강화하는 것이다.

2026-05-09 follow-up review 결과, 기존 구현은 대체로 완료되어 있으나 `docs/05.operations/policies`가 risky-command marker gate에서 빠져 있고, 완료 증거가 대화 출력에 의존하며, matrix 검증과 direct push 차단 표현이 실제 검증 범위를 과장할 수 있는 gap이 확인되었다. 2026-05-09 final multi-agent disposition은 REVISE 후 승인 가능이며, 남은 objection은 readiness 의미 축소, matrix gap 표현 가능성, validator 범위 정합성, 검증 증거의 snapshot 성격이다. 이번 보강은 새 runtime surface 없이 기존 validator, catalog, Agent-first rule, plan/task evidence만 정밀화한다.

2026-05-22 follow-up은 governance, docs, lifecycle hook hardening을 같은 remediation stream에 누적한다. 범위는 tracked repository surface로 제한하고 `.agent-work/`는 제외한다. `docs/01~05` 검토는 template compliance, status drift, downstream links, execution evidence, operations boundary wording을 중심으로 분류하되, 문서 삭제는 기본 조치로 삼지 않는다.

2026-05-22 추가 요청에 따라 구조적 템플릿 누락 방지를 우선 반영한다. 품질 게이트는 이제 authored stage의 비-README Markdown이 정확히 하나의 structural template mapping에 포함되는지 확인하고, mapping이 가리키는 템플릿 파일 존재 여부와 required template headings를 함께 검증한다.

## Goals & In-Scope

- **Goals**:
  - GitOps-first 원칙과 직접 cluster mutation 절차의 충돌을 줄인다.
  - Agent 실행 경로에서 직접 cluster mutation이 기본값이 아님을 명확히 한다.
  - 역사적 Dashboard/`172.19.x` 문맥과 현재 Headlamp/`172.18.x` 실행 계약을 분리한다.
  - 하네스와 Agent-first Engineering 구현 상태를 readiness matrix로 정리한다.
- **In Scope**:
  - `docs/04.execution/plans`, `docs/04.execution/tasks` 보정 작업 추적 문서 추가
  - `docs/05.operations/guides`, `docs/05.operations/policies`, `docs/05.operations/runbooks`의 안전 경계 문구 보정
  - `docs/00.agent-governance/harness-catalog.md` 및 Agent-first 규칙 보강
  - 각 stage README 인덱스 갱신

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - docs taxonomy 축소 또는 stage 폴더 삭제
  - 새 Kubernetes manifest 추가 또는 기존 manifest 계약 변경
  - live cluster 검증 또는 직접 cluster mutation 수행
  - GitHub-native instruction 계층 추가
- **Out of Scope**:
  - 외부 Vault/PostgreSQL/Valkey/Observability 런타임 변경
  - `.claude`/`.codex` 에이전트 roster 변경
  - PRD/ARD/ADR/Spec 신규 작성

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | 보정 작업 plan/task 문서 추가 및 README 인덱스 갱신 | `docs/04.execution/plans/`, `docs/04.execution/tasks/` | REQ-DOC-001 | repo quality gate PASS |
| PLN-002 | 직접 cluster mutation 절차를 human-approved bootstrap/break-glass 경로로 격리 | `docs/05.operations/guides/`, `docs/05.operations/policies/`, `docs/05.operations/runbooks/` | REQ-OPS-001 | `kubectl apply/patch` 문맥 검토 |
| PLN-003 | Dashboard/`172.19.x` 역사적 문맥과 현재 Headlamp/`172.18.x` 계약 분리 강화 | canonical docs taxonomy 관련 문서 중 보정 대상 | REQ-DOC-002 | stale contract gate PASS |
| PLN-004 | 하네스 readiness matrix와 Agent-first execution boundary 보강 | `docs/00.agent-governance/` | REQ-AI-001 | harness catalog mirror gate PASS |
| PLN-005 | 최소 정적 검증 묶음 실행 | `scripts/`, `infrastructure/tests/` | REQ-VAL-001 | 모든 repo-backed command PASS 또는 제한 명시 |
| PLN-006 | gateway/runtime audit 결과를 반영해 hook boundary와 historical memory current-source 문맥 보강 | `docs/00.agent-governance/` | REQ-AI-002 | repo quality gate PASS |
| PLN-007 | root shim thinness, governance/runtime English-only, hook-boundary clarity를 repo quality gate로 고정 | `scripts/validate-repo-quality-gates.sh` | REQ-VAL-002 | regression checks PASS |
| PLN-008 | Harness component audit matrix와 Agent-first component audit matrix 추가 | `docs/00.agent-governance/harness-catalog.md` | REQ-AI-003 | matrix table structure and non-empty `Status`/`Gap`/`Remediation` fields validated as regression guards |
| PLN-009 | matrix-first change rule과 repo-local context hierarchy rule 추가 | `docs/00.agent-governance/rules/agentic.md` | REQ-AI-004 | repo quality gate validates matrix-first and context hierarchy rules |
| PLN-010 | Authored docs command-boundary follow-up 적용 | `docs/02.architecture/decisions/`, `docs/03.specs/`, `docs/05.operations/guides/`, `docs/05.operations/policies/`, `docs/05.operations/runbooks/`, `scripts/validate-repo-quality-gates.sh` | REQ-AI-005 | risky command examples require human/operator boundary markers; authored-doc push examples require PR-flow context, while broader Markdown direct-push examples fail |
| PLN-011 | 완료 증거를 repo-discoverable snapshot summary로 보강 | `docs/04.execution/plans/`, `docs/04.execution/tasks/` | REQ-AI-006 | task verification summary records date, command results, skipped optional tools, and future handoff rerun requirement |
| PLN-012 | Matrix status contract를 `Ready`/`Partial`/`Missing` enum으로 명시하고 gap consistency를 검증 | `docs/00.agent-governance/harness-catalog.md`, `scripts/validate-repo-quality-gates.sh` | REQ-AI-007 | Ready rows require `Gap=None`; Partial/Missing rows require concrete `Gap` and `Remediation` |
| PLN-013 | `Gap=None`과 provider hook boundary 의미를 Agent-first 규칙에 정밀화 | `docs/00.agent-governance/rules/agentic.md` | REQ-AI-008 | explicit human request or concrete matrix gap is required before new runtime surface review; Claude permissions/hooks and Codex context hook are not equivalent enforcement layers |
| PLN-014 | `docs/01~05` stage audit 결과를 구조적 템플릿 coverage와 lifecycle hardening 범위에 반영 | `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, `docs/99.templates/` | REQ-DOC-003 | every non-README authored stage Markdown matches exactly one structural template mapping |
| PLN-015 | Stop/SubagentStop/PreCompact lifecycle guard 추가 및 Claude/Codex wiring 반영 | `.claude/hooks/lifecycle-guard.sh`, `.claude/settings.json`, `.codex/hooks.json` | REQ-AI-009 | Stop/SubagentStop block objective repo-state failures; PreCompact remains advisory |
| PLN-016 | repo quality gate에 lifecycle hook wiring과 clean/failing/advisory payload simulation 추가 | `scripts/validate-repo-quality-gates.sh`, `scripts/README.md` | REQ-VAL-003 | quality gate simulates Stop, SubagentStop, and PreCompact payloads |
| PLN-017 | governance/runtime 문서에 lifecycle hook contract와 structural template coverage 반영 | `docs/00.agent-governance/`, `.claude/CLAUDE.md`, `.claude/agents/doc-writer.md`, `.codex/agents/doc-writer.toml` | REQ-AI-010 | provider, catalog, postflight, and doc-writer contracts stay aligned |
| PLN-018 | 변경 후 정적 검증 bundle 재실행 및 skipped live/optional checks 명시 | `scripts/`, `infrastructure/tests/`, `docs/04.execution/tasks/` | REQ-VAL-004 | all repo-backed checks PASS or limitations documented |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | repo governance quality gate | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | Static | k3d/GitOps static contracts | `bash infrastructure/tests/verify-contracts-static.sh` | PASS |
| VAL-PLN-003 | Static | GitOps structure | `bash scripts/validate-gitops-structure.sh` | PASS |
| VAL-PLN-004 | Static | YAML syntax and optional kube-linter | `bash scripts/validate-k8s-manifests.sh .` | PASS or tool limitation stated |
| VAL-PLN-005 | Security | plaintext secret scan | `bash scripts/check-secret-handling.sh .` | PASS |
| VAL-PLN-006 | Static | shell syntax | `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` | no syntax errors |
| VAL-PLN-007 | Static | diff whitespace check | `git diff --check` | no whitespace errors |
| VAL-PLN-008 | Static | runtime JSON parse | `python3 -m json.tool .claude/settings.json` and `python3 -m json.tool .codex/hooks.json` | both files parse |
| VAL-PLN-009 | Static | lifecycle hook payload simulation | Stop, SubagentStop, and PreCompact self-test payloads through `scripts/validate-repo-quality-gates.sh` and targeted hook commands | Stop/SubagentStop block forced failures; PreCompact reports advisory output only |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Direct mutation guidance remains ambiguous | High | Mark direct `kubectl apply/patch` paths as human-approved bootstrap/break-glass only |
| Authored docs normalize risky commands as agent-executable defaults | High | Gate risky command examples with explicit human/operator boundary markers and reject bare/main direct push or push examples without PR-flow context |
| Completed task evidence is not durable | Medium | Record current validation date, command outcomes, and skipped optional tools in the task verification summary |
| Matrix gate is mistaken for semantic readiness proof | Medium | State that matrix checks are regression/structure guards and keep CI/toolchain/live k3d readiness in separate evidence lanes |
| `Gap=None` is mistaken for a permanent ban on future runtime surfaces | Medium | Treat `Gap=None` as a current evidence snapshot; require an explicit human request or a matrix update to `Partial`/`Missing` before adding surfaces |
| Structural template mapping misses a new authored-doc path | High | Fail repo quality gate when a non-README authored Markdown file under `docs/01~05` or `docs/90.references` does not match exactly one template mapping |
| Lifecycle hook blocks for subjective or advisory conditions | Medium | Limit Stop/SubagentStop blocking to command exit failures from repo-backed validators; keep PreCompact advisory |
| Historical docs are mistaken for current runtime contract | Medium | Keep historical content but add current-contract notes pointing to Headlamp and `172.18.x` manifests |
| Documentation remediation expands into manifest changes | Medium | Keep Kubernetes manifests explicitly out of scope |
| New documents drift from templates | Medium | Start from `plan.template.md` and `task.template.md`; update stage README indexes |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: repo-backed validators must pass before handoff.
- **Sandbox / Canary Rollout**: not applicable; no live rollout or manifest change is planned.
- **Human Approval Gate**: direct cluster mutation, live cluster verification beyond read-only checks, and external runtime changes require explicit human approval.
- **Rollback Trigger**: revert only this documentation/governance change set if validation fails or safety language conflicts with existing governance.
- **Prompt / Model Promotion Criteria**: not applicable; no model or prompt roster change is planned.

## Completion Criteria

- [x] Scoped documentation and governance remediation completed
- [x] Stage README indexes updated
- [x] GitOps-first direct mutation boundaries clarified
- [x] Harness readiness matrix added
- [x] Gateway/runtime audit results reflected without adding new runtime surfaces
- [x] Regression gates cover gateway thinness, language boundaries, historical memory, and hook-boundary clarity
- [x] Harness and Agent-first component audits are captured as matrix artifacts
- [x] Matrix-first change rules prevent unnecessary new runtime surfaces
- [x] Authored docs command-boundary follow-up completed
- [x] `docs/05.operations/policies` is included in risky-command boundary scanning
- [x] Matrix checks are documented and validated as structure/regression guards, not semantic readiness proof
- [x] Matrix status contract allows `Ready`, `Partial`, and `Missing`, with gap/remediation consistency checks
- [x] Push-example checks distinguish authored-doc PR-flow expectations from broader Markdown direct-push blocking
- [x] Verification evidence is recorded as a 2026-05-09 repo-discoverable snapshot; future handoff claims require rerunning the validation bundle
- [x] Rewriting authored SSoT docs outside the current command-boundary hardening scope remains separate human-approved work
- [x] Structural template coverage prevents uncovered non-README authored Markdown under `docs/01~05` and `docs/90.references`
- [x] Lifecycle hook script and Claude/Codex wiring cover Stop, SubagentStop, and PreCompact
- [x] Repo quality gate simulates lifecycle clean/failing/advisory payloads
- [x] Governance/runtime docs describe Stop/SubagentStop blocking and PreCompact advisory boundaries
- [x] Required verification passed or limitations documented

## Related Documents

- **Governance**: [`../../00.agent-governance/harness-catalog.md`](../../00.agent-governance/harness-catalog.md)
- **Agent-first Rules**: [`../../00.agent-governance/rules/agentic.md`](../../00.agent-governance/rules/agentic.md)
- **Document Routing**: [`../../00.agent-governance/rules/document-stage-routing.md`](../../00.agent-governance/rules/document-stage-routing.md)
- **Task**: [`../tasks/2026-05-09-k3d-agent-first-remediation.md`](../tasks/2026-05-09-k3d-agent-first-remediation.md)
