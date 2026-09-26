---
title: "Workspace Engineering Research Pack"
version: "0.2.1"
type: "common/readme-research-pack"
status: "active"
owner: "platform"
updated: "2026-09-26"
layer: "references"
---
# Workspace Engineering Research Pack

## Overview

이 pack은 날짜가 붙은 Workspace Engineering Research(WER) pack 세 개를 잇는 단일
후속 연구 경계다. 주제별 연구를 갱신하기 전에 소유권과 migration 인터페이스를
정한다. 서술 증거이며 정책, runtime, provider, 배포를 제어하는 surface가 아니다.

## Research Contract

- **Pack 날짜**: 2026-08-08.
- **기준선**: 선행 파일 25개는 정확한 처분과 소비자 cutover 증명을 거친 뒤
  WERPC-008이 삭제했다. 그 출처는 Git history와 source coverage가 보존한다.
- **권한**: 이름이 명시된 정본 workspace 문서가 계속 현재의 사실이다. 이 pack은
  관찰 날짜가 붙은 연구와 routing 증거를 기록한다.
- **발견 어휘**: 발견에는 `Verified`, `Partial`, `Unverified`, `DEFER`,
  `Contradicted`만 쓴다. 이를 뒷받침하는 증거와 남은 한계는 완료된 WERPC work
  package가 기록한다. 복합 상태 셀은 기본값을 먼저 적고, 그 뒤에 범위를 정하는
  한정어를 붙인다.
- **경로 약칭**: 이 보고서들에서 접두어 없이 쓴 `rules/`, `scopes/`,
  `providers/`, `contracts/`, `memory/`, `model-policy.md`, `harness-catalog.md`는
  각 관찰 날짜의 역사적 `docs/00.agent-governance/` 트리를 가리킨다. 역사적
  서술일 뿐 현재의 로드 지시가 아니다. 현재 공통 권한은
  [the common hub](../../../../.agents/README.md)에 있고 Git 기반 후속 그래프는
  [Archive](../../../98.archive/README.md)가 소유한다.
- **정정 기록**: 2026-08-10 coverage 재검증에서 Claude gateway import, 공통
  instruction topology, LLM-WIKI 최신성 서술을 바로잡고 CI/CD·QA 보고서 안의
  출처 날짜 자기모순을 해소했다. 출처와 주장 식별자는 다시 번호를 매기지 않았다.
- **최신성 기록**: 2026-08-10에 gap-only refresh가 손대지 않은 보고서 다섯 개의
  외부 출처를 다시 확인했다. 그중 네 개(harness와 loop, AI agents와 agency
  agents, model routing, memory)는 기간 안에 변화가 없었다. Diátaxis 출처는 HTTP
  429에 막혀 도달할 수 없었으므로 `unchanged`가 아니라 `unreachable`로 기록했고
  그 주장은 2026-08-08 관찰 날짜를 유지한다. 기존 주장을 다시 쓰지 않고 발견 두
  개를 날짜가 붙은 하위 절로 추가했다. 하나는 고정된 MCP `2025-11-25` revision이
  `2026-07-28`로 대체되었다는 것이며 `SRC-WERPC-066`으로 등록했다. 다른 하나는
  live Codex 페이지 두 곳이 model 식별자, reasoning-effort 값, model 우선순위를
  서로 다르게 적고 있다는 것이다. 요구사항 상태는 바뀌지 않았다.
- **출처 검증 기록**: 2026-08-11에 게시된 페이지를 세 번째로 요청했지만 다시
  HTTP 429가 돌아왔다. 그래서 Diátaxis 주장은 사이트를 빌드하는 upstream 소스로
  대신 검증했고, 이를 `SRC-WERPC-067`로 등록했다. 이 확인으로 tutorial과
  explanation이 없다는 기록도 승인된 Spec 052 `DOC-G2`, `DOC-G3`와 맞춰졌다. 그
  부재는 framework 자체의 지침에 근거한 결정이지 열린 질문이 아니다.
  `REQ-WERPC-020`은 `Partial` 상태를 유지하며 이제 그 상태는 결정되지 않은
  route가 아니라 아직 강제되지 않은 `DOC-G1` enum 작업을 반영한다.

### Structure

```text
0001-workspace-engineering/
├── README.md
├── m0011-agent-memory-tiers-and-management.md
├── m0010-agent-model-routing-and-configuration.md
├── m0009-ai-agents-and-agency-agents.md
├── m0008-ci-cd-github-actions-and-qa.md
├── m0005-documentation-architecture-and-diataxis.md
├── m0002-harness-and-loop-engineering.md
├── m0007-kubernetes-infrastructure-and-security.md
├── m0006-llm-wiki-and-knowledge-routing.md
├── m0003-provider-implementation-status.md
├── m0013-scope-application-index.md
├── m0012-source-coverage.md
├── m0004-spec-driven-sdlc-and-document-contracts.md
└── m0001-workspace-governance-and-common-agent-environment.md
```

## Report Index

| Reference                                                                    | Role                                                   |
| ---------------------------------------------------------------------------- | ------------------------------------------------------ |
| [workspace governance](m0001-workspace-governance-and-common-agent-environment.md) | 공통 workspace와 application routing |
| [harness and loop](m0002-harness-and-loop-engineering.md)                          | harness와 control loop 분석 |
| [provider status](m0003-provider-implementation-status.md)                         | Claude·Codex surface 분리 |
| [SDLC contracts](m0004-spec-driven-sdlc-and-document-contracts.md)                 | Spec 중심 lifecycle과 문서 family |
| [documentation architecture](m0005-documentation-architecture-and-diataxis.md)     | Diátaxis 대응 |
| [LLM-WIKI routing](m0006-llm-wiki-and-knowledge-routing.md)                        | 지식 routing과 최신성 |
| [platform security](m0007-kubernetes-infrastructure-and-security.md)               | Kubernetes, infrastructure, 보안 |
| [CI/CD and QA](m0008-ci-cd-github-actions-and-qa.md)                               | 전달 증거 lane |
| [AI agents](m0009-ai-agents-and-agency-agents.md)                                  | agent system과 agency agents 분석 |
| [model routing](m0010-agent-model-routing-and-configuration.md)                    | model 선택 제어 |
| [memory](m0011-agent-memory-tiers-and-management.md)                               | memory class lifecycle |
| [source coverage](m0012-source-coverage.md)                                         | 출처, 주장, 범위가 정해진 역사적 처분 |
| [scope application index](m0013-scope-application-index.md)                        | pack 발견에 대한 거버넌스 scope routing |

### Requirement Coverage Matrix

각 요청에는 주 연구 owner가 정확히 하나 있다. workspace 증거는 현재의 로컬
증거이며 외부 제품이나 live runtime에 대한 주장을 입증하지 않는다.

현재성 메모(2026-09-14): 아래 매트릭스의 증거 경로 중 몇 개는 그 뒤로 옮겨진
owner를 가리킨다. Agent governance는 이제 `docs/00.agent-governance/`나
`.agents/agents/`가 아니라 `.agents/governance/`와 `.agents/roles/registry.json`에
있다. 저장소 품질 검사는 `scripts/validate-repo-quality-gates.sh`가 아니라
`scripts/qa.py`와 `scripts/validation/registry.json`으로 실행된다. GitHub surface
소유권은 `.github/repository-surface.md`에 기록되어 있고 Plan과 Task는
`docs/04.execution/`이 아니라 각 `docs/03.specs/<package>/`에 있다. 각 행은 pack을
다음에 갱신할 때까지 관찰 시점의 경로를 유지한다.

| Request ID    | Requested topic         | Primary owner                                                                                                         | Workspace evidence                                                                                  | External source class                                                                                                                                                                                                                                   | Finding                                                                                                                                                                                                                                           |
| ------------- | ----------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| REQ-WERPC-001 | Harness                 | [Harness baseline](m0002-harness-and-loop-engineering.md#harness-baseline)                                                  | `.codex/CODEX.md`                                                                                   | Official OpenAI primary sources plus repository-static contracts, checked 2026-08-08                                                                                                                                                                    | Verified — static harness implementation; provider/runtime delivery remains DEFER                                                                                                                                                                |
| REQ-WERPC-002 | Loop                    | [Loop baseline](m0002-harness-and-loop-engineering.md#loop-baseline)                                                        | `docs/00.agent-governance/rules/agentic.md`                                                         | Repository-static machine contract plus official OpenAI product context, checked 2026-08-08                                                                                                                                                             | Verified — local state/retry contract; actual provider execution remains DEFER                                                                                                                                                                   |
| REQ-WERPC-003 | Workspace application   | [Workspace application baseline](m0001-workspace-governance-and-common-agent-environment.md#workspace-application-baseline) | `AGENTS.md`                                                                                         | Official Anthropic/OpenAI sources plus repository-static owners, checked 2026-08-08                                                                                                                                                                     | Verified — static control-plane application; native discovery/authentication remains DEFER                                                                                                                                                       |
| REQ-WERPC-004 | Claude                  | [Claude baseline](m0003-provider-implementation-status.md#claude-baseline)                                                  | `.claude/`                                                                                          | Official Anthropic provider documentation, checked 2026-08-08                                                                                                                                                                                           | Verified — bounded product surfaces and static adapter; local discovery/runtime remains DEFER                                                                                                                                                    |
| REQ-WERPC-005 | Codex                   | [Codex baseline](m0003-provider-implementation-status.md#codex-baseline)                                                    | `.codex/CODEX.md`                                                                                   | Official OpenAI provider documentation (manual cache first), checked 2026-08-08                                                                                                                                                                         | Verified — bounded product surfaces and static adapter; local discovery/runtime remains DEFER                                                                                                                                                    |
| REQ-WERPC-006 | Common system           | [Common-system baseline](m0001-workspace-governance-and-common-agent-environment.md#common-system-baseline)                 | `docs/00.agent-governance/harness-catalog.md`                                                       | Official provider sources plus repository-static control-plane evidence, checked 2026-08-08                                                                                                                                                             | Partial — static shared controls verified; provider parity/effective runtime remains DEFER                                                                                                                                                       |
| REQ-WERPC-007 | Spec-driven development | [Spec-driven baseline](m0004-spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline)                   | `docs/03.specs/`                                                                                    | GitHub Spec Kit primary documentation plus local contracts, checked 2026-08-08                                                                                                                                                                          | Verified — source-backed practice model and static local flow; generated-code/runtime outcomes remain DEFER                                                                                                                                      |
| REQ-WERPC-008 | Kubernetes              | [Kubernetes baseline](m0007-kubernetes-infrastructure-and-security.md#kubernetes-baseline)                                  | `gitops/` and `policy/`                                                                             | Official Kubernetes, kube-state-metrics v2.14.0, Argo CD, Helm, Gatekeeper, ESO, Vault, Sigstore, SLSA, and GitHub primary sources plus exact static selectors (`SRC-WERPC-023`–`034`, `SRC-WERPC-060`–`065`); admitted refresh checked 2026-08-10      | Partial — exact Secret collector/RBAC, Adminer token/hardening, and immutable delivery distinctions are source-backed; consumer need, compatibility, effective RBAC/admission/reconciliation, artifacts, registry, and runtime remain DEFER      |
| REQ-WERPC-009 | Infrastructure          | [Infrastructure baseline](m0007-kubernetes-infrastructure-and-security.md#infrastructure-baseline)                          | `infrastructure/` and `traefik/`                                                                    | Official Argo CD, SLSA, and NIST sources plus static/live boundary documentation, checked 2026-08-08                                                                                                                                                    | Partial — static bootstrap/GitOps/gateway boundary verified; k3d, gateway, registry, hosted CI, and cloud state remain DEFER                                                                                                                     |
| REQ-WERPC-010 | SDLC                    | [SDLC baseline](m0004-spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline)                          | `docs/01.requirements/`                                                                             | NIST SSDF, ISO official abstract, and local contracts, checked 2026-08-08                                                                                                                                                                               | Verified — external framework boundaries and static document lifecycle; conformance/effectiveness remains DEFER                                                                                                                                  |
| REQ-WERPC-011 | PRD                     | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `docs/01.requirements/`                                                                             | ISO requirements-engineering abstract, NASA systems guidance, and local profile/template/validator evidence (`SRC-WERPC-053`), checked 2026-08-10                                                                                                       | Verified gap — repository-defined product-intent contract with external requirements basis; current downstream terminology is AD, while stakeholder/product validation remains DEFER                                                             |
| REQ-WERPC-012 | Architecture Description (AD) | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)             | `docs/02.architecture/descriptions/`                                                                | ISO architecture-description abstract, NASA architecture guidance, and local profile/template/validator evidence (`SRC-WERPC-054`), checked 2026-08-10                                                                                                  | Verified gap — compact local architecture contract with proportional external review basis; current route and lineage use AD and `sdlc/ad`, while architecture effectiveness remains DEFER                                                     |
| REQ-WERPC-013 | ADR                     | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `docs/02.architecture/decisions/`                                                                   | AWS ADR guidance plus local profile/template evidence, checked 2026-08-08                                                                                                                                                                               | Verified gap — static contract and bounded ADR benchmark; current lineage is AD/ADR, while decision quality remains DEFER                                                                                                                       |
| REQ-WERPC-014 | Guide                   | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `docs/05.operations/guides/`                                                                        | Local profile/template plus Diátaxis guidance, checked 2026-08-08                                                                                                                                                                                       | Partial — typed how-to-shaped Guide; tutorial classification/usability remains DEFER                                                                                                                                                             |
| REQ-WERPC-015 | Incident                | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `docs/05.operations/incidents/`                                                                     | Google SRE guidance plus local profile/template evidence, checked 2026-08-08                                                                                                                                                                            | Verified — typed static incident contract; runtime response remains DEFER                                                                                                                                                                        |
| REQ-WERPC-016 | Postmortem              | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `docs/99.templates/templates/operations/postmortem.template.md`                                | Google SRE guidance plus local profile/template evidence, checked 2026-08-08                                                                                                                                                                            | Verified — typed static learning contract; action closure remains DEFER                                                                                                                                                                          |
| REQ-WERPC-017 | Policy                  | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `docs/05.operations/policies/`                                                                      | NIST policy/control/assessment guidance plus local profile/template/validator evidence (`SRC-WERPC-055`), checked 2026-08-10                                                                                                                            | Verified — normative policy, procedure, and assessment-evidence boundaries; enforcement remains DEFER                                                                                                                                            |
| REQ-WERPC-018 | Release                 | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `.github/workflows/`                                                                                | Google release engineering, GitHub immutable-release identity, existing SemVer/provenance sources, and local absence evidence (`SRC-WERPC-056`), checked 2026-08-10                                                                                     | Verified gap — broader auditable release-record semantics are sourced, but no family/approval/runtime is created; DOC-G5 remains intact                                                                                                          |
| REQ-WERPC-019 | Runbook                 | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `docs/05.operations/runbooks/`                                                                      | Google SRE playbook/toil guidance plus local profile/template/validator evidence (`SRC-WERPC-057`), checked 2026-08-10                                                                                                                                  | Verified — typed procedure and risk-aware automation boundary; rehearsal and live safety/execution remain DEFER                                                                                                                                  |
| REQ-WERPC-020 | Diátaxis                | [Diátaxis baseline](m0005-documentation-architecture-and-diataxis.md#diátaxis-baseline)                                     | `docs/99.templates/registry.json`                                                  | Official Diátaxis plus local profiles/templates, checked 2026-08-08                                                                                                                                                                                     | Partial — how-to/reference are partially expressed; tutorial/explanation typing and classification remain gap                                                                                                                                    |
| REQ-WERPC-021 | LLM-WIKI                | [Historical LLM-WIKI baseline](m0006-llm-wiki-and-knowledge-routing.md#llm-wiki-baseline)                                   | No current local owner; Git history preserves the retired generator and output                       | llms.txt proposal, MCP Resources specification, and historical local generator, checked 2026-08-08; local retirement recorded 2026-09-01                                                                                                                | Contradicted — the prior deterministic canonical-owner map was retired; external comparison remains descriptive, and publication, MCP, search, RAG, and retrieval remain DEFER                                                                  |
| REQ-WERPC-022 | CI/CD                   | [CI/CD baseline](m0008-ci-cd-github-actions-and-qa.md#cicd-baseline)                                                        | `.github/workflows/`, `.github/README.md`, and GitOps recovery owners                               | Official GitHub, SLSA, pre-commit, and pip primary sources plus static workflow/validation evidence, checked 2026-08-08                                                                                                                                 | Partial — static CI/release-review and QA controls verified; deployment/promotion/rollback execution remains DEFER                                                                                                                               |
| REQ-WERPC-023 | GitHub Actions          | [GitHub Actions baseline](m0008-ci-cd-github-actions-and-qa.md#github-actions-baseline)                                     | `.github/workflows/`, CI security and Python-contract validators                                    | Official GitHub Actions primary documentation plus static workflow inventory, checked 2026-08-08                                                                                                                                                        | Partial — workflow/permission/pinning/concurrency declarations verified; hosted runs, rulesets, secrets, environments, OIDC, artifacts, and effective permissions remain DEFER                                                                   |
| REQ-WERPC-024 | QA                      | [QA baseline](m0008-ci-cd-github-actions-and-qa.md#qa-baseline)                                                             | `scripts/validate-repo-quality-gates.sh`, `validation-surfaces.json`, and `.pre-commit-config.yaml` | Repository validation contract plus official pre-commit/pip sources, checked 2026-08-08                                                                                                                                                                 | Verified — static lane/result, formatter, contract, lint/syntax/test/security boundaries documented; hosted/browser/live outcome remains DEFER                                                                                                   |
| REQ-WERPC-025 | Security                | [Security baseline](m0007-kubernetes-infrastructure-and-security.md#security-baseline)                                      | `policy/`, GitOps, ESO/Vault contracts                                                              | Official Kubernetes, kube-state-metrics v2.14.0, Argo CD, Helm, Gatekeeper, ESO/Vault, Sigstore, SLSA, GitHub, and NIST sources plus exact static control selectors (`SRC-WERPC-023`–`034`, `SRC-WERPC-060`–`065`); admitted refresh checked 2026-08-10 | Partial — Secret-object RBAC, Adminer ServiceAccount/hardening, and identity/signature/attestation/provenance boundaries are source-backed; enforcement, Secret/backend state, compatibility, trust policy, artifacts, and recovery remain DEFER |
| REQ-WERPC-026 | AI-agent systems        | [AI-agent-system baseline](m0009-ai-agents-and-agency-agents.md#ai-agent-systems-baseline)                                  | `docs/00.agent-governance/harness-catalog.md`                                                       | Official OpenAI/Anthropic agent documentation plus local harness contracts, checked 2026-08-08                                                                                                                                                          | Partial — static role/control-plane design verified; discovery, permission enforcement, execution, and effectiveness remain DEFER                                                                                                                |
| REQ-WERPC-027 | agency-agents           | [Agency-agents baseline](m0009-ai-agents-and-agency-agents.md#agency-agents-baseline)                                       | `.agents/agents/`                                                                                   | Pinned upstream commit `ebe9c99acb5c96f9468de368d8bead775387d1a7`, checked 2026-08-08                                                                                                                                                                   | Verified — reproducible catalog/license/script comparison; adoption, conversion/install, provider discovery, and quality remain DEFER                                                                                                            |
| REQ-WERPC-028 | Model routing           | [Model-routing baseline](m0010-agent-model-routing-and-configuration.md#model-routing-baseline)                             | `docs/00.agent-governance/model-policy.md`                                                          | Official OpenAI/Anthropic configuration sources plus local model-fitness contract, checked 2026-08-08                                                                                                                                                   | Partial — static tier/configuration/routing gates verified; parsing, resolution, fitness, cost/latency, canary, and promotion remain DEFER                                                                                                       |
| REQ-WERPC-029 | Short-term memory       | [Short-term-memory baseline](m0011-agent-memory-tiers-and-management.md#short-term-memory-baseline)                         | `docs/00.agent-governance/contracts/agent-checkpoint.schema.json`                                   | Local checkpoint contract plus official provider memory/session sources, checked 2026-08-08                                                                                                                                                             | Verified — atomic redacted advisory lifecycle defined; actual checkpoint/provider-memory use remains DEFER                                                                                                                                       |
| REQ-WERPC-030 | Long-term memory        | [Long-term-memory baseline](m0011-agent-memory-tiers-and-management.md#long-term-memory-baseline)                           | `docs/00.agent-governance/memory/progress.md`                                                       | Local memory contract plus official provider memory/session sources, checked 2026-08-08                                                                                                                                                                 | Verified — durable canonical-owner/provenance lifecycle defined; provider persistence and runtime enforcement remain DEFER                                                                                                                       |
| REQ-WERPC-031 | Domain-scoped memory    | [Domain-memory baseline](m0011-agent-memory-tiers-and-management.md#domain-scoped-memory-baseline)                          | `docs/03.specs/`                                                                                    | Local memory/domain-owner contract plus official provider/MCP boundaries, checked 2026-08-08                                                                                                                                                            | Verified — Spec/Runbook/Incident/Postmortem authority and archive routing defined; actual retrieval and provider integration remain DEFER                                                                                                        |
| REQ-WERPC-032 | Memory management       | [Memory-management baseline](m0011-agent-memory-tiers-and-management.md#memory-management-baseline)                         | `docs/00.agent-governance/memory/README.md`                                                         | Official OpenAI, Anthropic, and MCP primary sources plus local memory contract, checked 2026-08-08                                                                                                                                                      | Partial — lifecycle/redaction/conflict rules verified; provider retention, deletion, compaction, and connected-resource behavior remain DEFER                                                                                                    |
| REQ-WERPC-033 | Verification/Validation | [Verification and Validation matrix](m0008-ci-cd-github-actions-and-qa.md#verification-and-validation-question-matrix)      | `docs/00.agent-governance/rules/quality-standards.md`                                               | NASA product verification, product validation, requirements validation, and traceability guidance plus local quality-lane evidence (`SRC-WERPC-058`–`SRC-WERPC-059`), checked 2026-08-10                                                                | Partial — external questions and static workspace mapping verified; stakeholder, intended-use, independent, hosted, remote, and live evidence remain DEFER                                                                                       |
| REQ-WERPC-034 | Spec                    | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `docs/03.specs/`                                                                                    | GitHub Spec Kit specification-driven and agentic SDD guidance plus local profile/template/validator evidence, checked 2026-08-08; re-observed 2026-08-14 (`SRC-WERPC-076`)                                                                              | Verified — structural contract (route, frontmatter, status domain, required H2 set, `bodyContract` reciprocity/identifier rule); content, implementation, and delivery effectiveness remain DEFER                                                |
| REQ-WERPC-035 | Task                    | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `docs/04.execution/tasks/`                                                                          | GitHub Spec Kit specification-driven and agentic SDD guidance plus local profile/template/validator evidence, checked 2026-08-08; re-observed 2026-08-14 (`SRC-WERPC-076`)                                                                              | Verified — structural contract (route, frontmatter, status domain, required H2 set, `bodyContract` reciprocity/identifier rule); content, implementation, and delivery effectiveness remain DEFER                                                |
| REQ-WERPC-036 | Plan                    | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `docs/04.execution/plans/`                                                                          | GitHub Spec Kit specification-driven and agentic SDD guidance plus local profile/template/validator evidence, checked 2026-08-08; re-observed 2026-08-14 (`SRC-WERPC-076`)                                                                              | Verified — structural contract (route, frontmatter, status domain, required H2 set, `bodyContract` reciprocity/identifier rule); content, implementation, and delivery effectiveness remain DEFER                                                |

### 2026-08-10 gap-only refresh reconciliation

WERG-004 종료 스냅샷은 pack 파일 정확히 13개, 고유 요청 owner 33개, 고유 출처
ID 65개, 고유 주장 ID 65개를 기록했다. 그 구성은 `SRC-WERPC-052`와
`CLM-WERPC-006-08`까지의 동결된 행, 문서와 Verification/Validation 추가분인
`SRC-WERPC-053`–`059`와 `CLM-WERPC-007-01`–`08`, Kubernetes/Security 추가분인
`SRC-WERPC-060`–`065`와 `CLM-WERPC-008-01`–`06`이다. 그 종료 시점에 바뀔 수
있었던 연구 owner 다섯은 이 README, SDLC 보고서, CI/CD·QA 보고서,
Kubernetes/Security 보고서, 출처·주장 원장이었다.

이후 scope index와 최신성·upstream 출처 행이 더해진 뒤, pack에는 이 README를
포함한 실제 Markdown 파일 14개, 고유 요청 owner 33개, 고유 출처 ID 67개, 고유
주장 ID 65개가 있었다. 정적 검증은 hosted, provider runtime, 원격, credential을
담은 증거, secret, artifact, live 증거를 `DEFER`에서 올려 주지 않는다.

### 2026-08-11 Partial/DEFER refresh reconciliation

2026-08-12에 실행·확인한 2026-08-11 Partial/DEFER 증분 refresh는 후보를 정확히
열두 개 받아들였다. `REQ-WERPC-006`, `008`, `009`, `014`, `020`, `022`, `023`,
`025`, `026`, `028`, `032`, `033`이다. 새 연구 폴더나 중복 보고서는 만들지 않았다.
발견은 기존 owner에 날짜가 붙은 2026-08-11 절로 덧붙였으며 대상은 다음과 같다.
[governance](m0001-workspace-governance-and-common-agent-environment.md#2026-08-11-partialdefer-incremental-refresh),
[AI agents](m0009-ai-agents-and-agency-agents.md#2026-08-11-partialdefer-incremental-refresh),
[model routing](m0010-agent-model-routing-and-configuration.md#2026-08-11-partialdefer-incremental-refresh),
[memory](m0011-agent-memory-tiers-and-management.md#2026-08-11-partialdefer-incremental-refresh),
[Kubernetes and security](m0007-kubernetes-infrastructure-and-security.md#2026-08-11-partialdefer-incremental-refresh),
[Diátaxis](m0005-documentation-architecture-and-diataxis.md#2026-08-11-partialdefer-incremental-refresh),
[SDLC and document contracts](m0004-spec-driven-sdlc-and-document-contracts.md#2026-08-11-partialdefer-incremental-refresh),
[CI/CD, Actions, and QA](m0008-ci-cd-github-actions-and-qa.md#2026-08-11-partialdefer-incremental-refresh).

열두 후보는 모두 `Partial`로 닫혔다. `Verified`로 올라간 것이 없으므로 위 요청
매트릭스의 Finding 셀은 모두 이전 값을 유지한다. `REQ-WERPC-014`와
`REQ-WERPC-020` 행에는 `exclude-duplicate`도 붙는다. Spec 052의 `DOC-G1`,
`DOC-G2`, `DOC-G3`가 이미 그 질문을 소유하기 때문이다.

이 refresh로 `SRC-WERPC-068`–`073`과 `CLM-WERPC-009-01`–`12`가 더해져 현재
pack에는 이 README를 포함한 실제 Markdown 파일 14개, 고유 요청 owner 33개, 고유
출처 ID 73개, 고유 주장 ID 77개가 있다. 기존 출처나 주장 행은 번호를 다시
매기거나 고쳐 쓰지 않았다. `SRC-WERPC-073`은 이미 등록된 출처를 package가
2026-08-12에 재검증한 결과를 기록한다. 그 출처의 기준 `Checked on` 값은 계약상
보존되므로 재검증 날짜보다 뒤처져 있다. hosted runtime, provider runtime, 제품과
이해관계자 검증, cluster, credential을 담은 증거, live 증거는 계속 `DEFER`다.

### 2026-08-14 consistency and Partial re-observation reconciliation

이 cycle(WRCP-000–WRCP-007)은 서로 다른 후보 집합 두 개를 받아들였다. 첫째로
WRCP-002, WRCP-003, WRCP-004, WRCP-005가 2026-08-11 refresh에서 넘어온 `Partial`
요구사항 행 열두 개를 모두 다시 관찰했다. `REQ-WERPC-006`, `008`, `009`, `014`,
`020`, `022`, `023`, `025`, `026`, `028`, `032`, `033`이다. 모두 다시 `Partial`로
닫혔고 올라간 것이 없으므로, **이 cycle의 결과로 위 요청 매트릭스의 Finding 셀은
하나도 바뀌지 않았다**. 둘째로 WRCP-004가 Spec, Task, Plan 문서 family인
`REQ-WERPC-034`, `035`, `036`을 따로 다시 관찰했다. 이 셋은 Spec 057 개정
`C-WRCP-010`이 받아들인 새 coverage 매트릭스 owner 행이다. 그 계약에 따르면
family를 받아들인다고 상태가 오르거나 내리지 않는다. 새 행의 Finding은 구조
계약(route, frontmatter, 상태 domain, 필수 H2 집합, `bodyContract`의 상호성·식별자
규칙)에 대해서는 `Verified`이고 내용, 구현, 전달 효과에 대해서는 `DEFER`다.
WRCP-004가
[SDLC and document contracts](m0004-spec-driven-sdlc-and-document-contracts.md#2026-08-14-consistency-and-partial-re-observation)의
날짜 절에 기록한 그대로다. `C-WRCP-010`은 이번 수용을 정확히 세 행으로 제한하며
네 번째 owner는 추가하지 않았다.

이 세 행이 이번 cycle 전에 없었던 이유는 다음과 같다.
[document-family contract matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)는
문서 family 열두 개(PRD, ARD, ADR, Spec, Plan, Task, Guide, Incident, Postmortem,
Policy, Release, Runbook)를 설명하지만 위 coverage 매트릭스는 이번 cycle 전까지
그중 아홉 개(PRD, ARD, ADR, Guide, Incident, Postmortem, Policy, Release,
Runbook)에만 owner 행을 두었다. 이전 WRCP 요청 줄 가운데 Spec, Task, Plan을
명시한 것이 없어서 요청에서 출발한 연구가 이들의 coverage 매트릭스 행을 만든
적이 없었다. 앞선 refresh cycle 세 번(2026-08-10 gap-only refresh, 2026-08-11
Partial/DEFER refresh, 그 사이의 최신성 점검)도 같은 이유로 이를 놓쳤다.

두 집합의 발견은 날짜가 붙은 2026-08-14 절에 기록되어 있으며 대상은 다음과 같다.
[governance](m0001-workspace-governance-and-common-agent-environment.md#2026-08-14-consistency-and-partial-re-observation),
[AI agents](m0009-ai-agents-and-agency-agents.md#2026-08-14-consistency-and-partial-re-observation),
[model routing](m0010-agent-model-routing-and-configuration.md#2026-08-14-consistency-and-partial-re-observation),
[memory](m0011-agent-memory-tiers-and-management.md#2026-08-14-consistency-and-partial-re-observation),
[Kubernetes and security](m0007-kubernetes-infrastructure-and-security.md#2026-08-14-consistency-and-partial-re-observation),
[Diátaxis](m0005-documentation-architecture-and-diataxis.md#2026-08-14-consistency-and-partial-re-observation),
[SDLC and document contracts](m0004-spec-driven-sdlc-and-document-contracts.md#2026-08-14-consistency-and-partial-re-observation),
[CI/CD, Actions, and QA](m0008-ci-cd-github-actions-and-qa.md#2026-08-14-consistency-and-partial-re-observation).

이 cycle은 `SRC-WERPC-074`–`077`(WRCP-002/003/004/005 package마다 하나)과
`CLM-WERPC-010-01`–`15`(각각 주장 네 개, 세 개, 다섯 개, 세 개)를 등록한다. 기존
출처나 주장 행은 번호를 다시 매기거나 고쳐 쓰지 않았다. 이전 값을 이어받지 않고
추적 파일을 직접 세어 보면, pack에는 이제 이 README를 포함한 실제 Markdown 파일
14개(변화 없음), 고유 요청 owner 36개(33개에 받아들인 세 행을 더함), 고유 출처
ID 77개(73개에 `SRC-WERPC-074`–`077`을 더함), 고유 주장 ID 92개(77개에
`CLM-WERPC-010-01`–`15`를 더함)가 있다. hosted runtime, provider runtime,
cluster, credential을 담은 증거, live 증거는 계속 `DEFER`다.

### 2026-08-17 full-corpus refresh reconciliation

이 cycle(WRFC-000–WRFC-012, Spec 058)은 `Partial` 열두 행 표본이 아니라 owner
행 **서른여섯 개 전부**를 다시 관찰한 첫 cycle이다. 범위가 Spec 057 요청과
바이트 단위로 같았으므로, cycle은 새 정보를 얻을 수 있는 두 곳으로 일부러 방향을
틀었다. 2026-08-08 이후 확인하지 않은 `Verified` 행 스물네 개, 그리고 남아 있는
모든 `Partial`·`DEFER` 행에 대한 최종 blocking class 종결이다.

**여섯 행이 외부에서 `changed`로 돌아왔다.** 그중 세 행인 `REQ-WERPC-004`,
`011`, `021`은 상태가 `Verified`여서 앞선 cycle 세 번이 다시 시험한 표본에
구조적으로 들어가지 않았다.

| Request ID    | Prior status  | External change observed 2026-08-17                                    |
| ------------- | ------------- | ---------------------------------------------------------------------- |
| REQ-WERPC-004 | Verified      | Claude Code advanced from observed `2.1.220` to `2.1.233` (2026-08-14) |
| REQ-WERPC-006 | Partial       | Claude memory and subagent pages grew beyond the adopted scope         |
| REQ-WERPC-008 | Partial       | kube-state-metrics pin `v2.14.0` versus upstream `v2.19.1`             |
| REQ-WERPC-011 | Verified      | `ISO/IEC/IEEE DIS 29148` entered ballot; 2018 edition not superseded   |
| REQ-WERPC-021 | Verified      | `llms.txt` reached v2; MCP `2026-07-28` superseded the cited path      |
| REQ-WERPC-025 | Partial       | Argo CD `sourceIntegrity` shipped GA in `3.5.0` and `3.5.1`            |

**이 pack이 스스로 기록해 둔 refresh trigger 두 개가 발동했다.**
`SRC-WERPC-060`은 kube-state-metrics 버전 변경을, `SRC-WERPC-063`은 Argo CD 소스
무결성 변경을 trigger로 선언했다. 두 조건이 이제 모두 충족되었다. 이는 판단의
문제가 아니라 계약이 보내는 신호이며 `REQ-WERPC-008`과 `REQ-WERPC-025`의 다음
조치는 받아들였지만 아직 실행하지 않은 대상 refresh라는 뜻이다.

**상태는 바뀌지 않았다.** 서른여섯 행 모두 `statusEffect`를 `no-change`로
기록했다. 올라가거나, 내려가거나, 반박된 행이 없으므로 **위 요청 매트릭스의
Finding 셀은 모두 이전 값을 유지한다**. Spec 058 `C-WRFC-004`에 따르면 변화분이
기록되는 한 이는 성공이며 `changed` 결과 여섯 개와 발동한 trigger 두 개가 바로
그 변화분이다.

**`unreachable`로 돌아온 행은 없었고,** 그 자체가 변화분이다. 이전 cycle들은
`diataxis.fr`이 세 번의 시도에서 HTTP 429에 막혔다고 기록하고 사이트를 빌드하는
upstream 소스(`SRC-WERPC-067`)로 대신 확인했다. 2026-08-17에는 게시된 페이지가
직접 응답했고 이를 `SRC-WERPC-089`로 등록했으므로 그 대체 경로가 필요 없었다. 다른
두 host인 `iso.org`와 한 번의 `docs.aws.amazon.com`은 HTTP 403을 돌려주었고
unreachable로 기록하지 않고 검색을 거친 대체 경로로 해결했다.

**최종 blocking class 종결**은
[scope application index](m0013-scope-application-index.md#2026-08-17-full-corpus-re-projection-and-blocking-class-closure)에
기록되어 있다. 열두 행은 막힌 것이 없고 열 행은 저장소 정적 작업으로 도달할 수
있으며 열네 행은 구조적으로 도달할 수 없다. 이 열네 행은 각각 이름 붙은 재개
조건을 두고 더 이상의 정적 재시험을 하지 않도록 닫았다. Spec 055, 056, 057이
아무것도 올리지 못한 이유가 여기에 있다. 그 표본은 막고 있는 증거에 도달할 수
있는지를 따지지 않고 뽑혔다.

발견은 날짜가 붙은 2026-08-17 절로 기록되어 있으며 대상은 다음과 같다.
[governance](m0001-workspace-governance-and-common-agent-environment.md#2026-08-17-full-corpus-refresh),
[harness and loop](m0002-harness-and-loop-engineering.md#2026-08-17-full-corpus-refresh),
[provider status](m0003-provider-implementation-status.md#2026-08-17-full-corpus-refresh),
[SDLC and document contracts](m0004-spec-driven-sdlc-and-document-contracts.md#2026-08-17-full-corpus-refresh),
[Diátaxis](m0005-documentation-architecture-and-diataxis.md#2026-08-17-full-corpus-refresh),
[LLM-WIKI](m0006-llm-wiki-and-knowledge-routing.md#2026-08-17-full-corpus-refresh),
[Kubernetes and security](m0007-kubernetes-infrastructure-and-security.md#2026-08-17-full-corpus-refresh),
[CI/CD, Actions, and QA](m0008-ci-cd-github-actions-and-qa.md#2026-08-17-full-corpus-refresh),
[AI agents](m0009-ai-agents-and-agency-agents.md#2026-08-17-full-corpus-refresh),
[model routing](m0010-agent-model-routing-and-configuration.md#2026-08-17-full-corpus-refresh),
[memory](m0011-agent-memory-tiers-and-management.md#2026-08-17-full-corpus-refresh).

이 cycle은 `SRC-WERPC-078`–`089`와 `CLM-WERPC-011-01`–`39`를 등록한다. 주장은
owner 행마다 하나씩이고, 여기에 cycle 수준 주장 세 개가 더해진다. 기존 출처, 주장,
요구사항 행은 번호를 다시 매기거나 고쳐 쓰지 않았다. 추적 파일을 직접 세어 보면
pack에는 이제 이 README를 포함한 **실제 Markdown 파일 14개**(변화 없음), **고유
요청 owner 36개**(변화 없음), **고유 출처 ID 89개**(77개에 열두 개를 더함), **고유
주장 ID 131개**(92개에 서른아홉 개를 더함)가 있다. 참조된 모든 식별자에는 등록된
원장 행이 있다. 출처 행 89개, 주장 행 131개다. hosted runtime, provider runtime,
cluster, credential을 담은 증거, live 증거는 계속 `DEFER`다.

한계 두 가지는 숨기지 않고 기록한다. 문서 family 행을 소유한 package가 shell
도구 없이 실행되었기 때문에 `Spec`, `Task`, `Plan`, `Guide` instance 수를 다시
세지 **않았고** 2026-08-14의 수치를 검증 없이 이어받았다. 또 당시의 LLM-WIKI
생성 index 검사를 실행하지 **않았으므로**, index 최신성은 증명된 것이 아니라
바뀌지 않은 frontmatter 날짜에서 추론한 것이다.

두 한계 모두 통합 전에 실행한 증거로 닫았으므로 후속 cycle로 넘어간 것은 없다.
역사적 drift 검사는 PASS를 돌려주어 당시 추론한 최신성을 확인했다. 생성 index와
그 생성기는 이후 현재 workspace에서 폐기되었다.
frontmatter를 새로 세어 보면 family마다 평범한 `active`→`done` 전이 하나를 빼고는
2026-08-14의 Spec, Task, Plan 기준선이 그대로 재현되며 `archived`를 쓴 경우가
없다는 점도 여전히 성립한다. 따라서 기록된 수치와 모순되는 것은 없다. 직접 열거는
보고는 되었지만 일부러 기록하지 않았던 수치 세 개도 바로잡았다. ARD, ADR,
Runbook의 날짜가 붙은 instance는 아홉, 열여덟, 열 개가 아니라 여덟, 열일곱, 아홉
개다. 셋 다 `README.md`를 instance로 센 탓에 하나씩 부풀어 있었다.

### 2026-08-18 correction reconciliation

2026-08-18의 후속 검증은 2026-08-17 cycle이 한 **주장 하나를 철회했다**. 그
cycle은 upstream kube-state-metrics가 `v2.14.0`에는 없던 `serviceaccounts`
리소스를 추가했다고 적었다. 두 tag에서 배포된 표준 `ClusterRole`을 받아 diff해
보면 버전 label을 빼고는 바이트 단위로 같다. 즉 `serviceaccounts`는 이미 있었고
그 범위에서 upstream은 ClusterRole 규칙을 하나도 바꾸지 않았다. 이 서술은
[Kubernetes and security report](m0007-kubernetes-infrastructure-and-security.md#2026-08-18-correction-to-the-2026-08-17-kube-state-metrics-statement)와
cycle Task 안에서 제자리 정정했고 상태 `Contradicted`인 `CLM-WERPC-012-01`로
등록했다. 이 pack에서 그 상태 값을 처음 쓴 사례다.

이 정정은 바탕의 발견을 약하게 하지 않고 오히려 더 분명하게 한다. 실제 차이는
이 저장소가 손으로 관리하는 ClusterRole이 처음부터 upstream의 것을 줄인 부분
집합이었다는 점이다. 빠진 것 가운데 두 개인
`certificates.k8s.io/certificatesigningrequests`와
`coordination.k8s.io/leases`는 문서화된 기본 리소스인데, 배포는 현재 pin이 유지된
기간 내내 필요한 권한 없이 이것들을 수집해 왔다. 이는 upgrade의 결과가 아니라
이미 있던 실제 결함이다. upgrade로 새로 생기는 RBAC 요구사항은 정확히 하나,
`discovery.k8s.io/endpointslices`다. `v2.18.0`이 이를 기본값으로 바꿔 넣었고
Deployment에는 `args:`가 선언되어 있지 않기 때문이다.

이 정정은 `SRC-WERPC-090`과 `CLM-WERPC-012-01`–`04`를 등록한다. 기존 출처,
주장, 요구사항 행은 번호를 다시 매기지 않았고 요구사항 owner도 새로 만들지
않았다. 추적 파일을 세어 보면 pack에는 이제 실제 Markdown 파일 14개, 고유 요청
owner 36개, **고유 출처 ID 90개**, **고유 주장 ID 135개**가 있으며 원장에는 출처
행 90개와 주장 행 135개가 등록되어 있다. `REQ-WERPC-008`은 `Partial`을 유지한다.
주장을 철회해도 상태는 바뀌지 않으며 hosted runtime, provider runtime, cluster,
live 증거는 계속 `DEFER`다.

### 2026-08-20 full-corpus reverification reconciliation

| Field | Value |
| --- | --- |
| Census | markdownFiles=14, requests=36, sources=91, claims=141 |
| External results | changed=3, unchanged=32, unreachable=1 |
| Workspace results | confirmed=29, drifted=6, absent=1 |
| Dispositions | Verified=20, Verified gap=4, Partial=12 |
| Evidence depths | repository-static=28, public-documentation=8 |
| Blocking classes | none=12, repo-static=10, provider-runtime=5, hosted-ci=2, live-cluster=3, human-judgement=4 |
| Changed requests | REQ-WERPC-004, REQ-WERPC-006, REQ-WERPC-008, REQ-WERPC-009, REQ-WERPC-011, REQ-WERPC-012, REQ-WERPC-013, REQ-WERPC-018, REQ-WERPC-025 |
| Unreachable requests | REQ-WERPC-033 |
| Allocated K3s observation | SRC-WERPC-091; request=REQ-WERPC-009 |
| Allocated claims | CLM-WERPC-013-01, CLM-WERPC-013-02, CLM-WERPC-013-03, CLM-WERPC-013-04, CLM-WERPC-013-05, CLM-WERPC-013-06 |
| Terminology claims | CLM-WERPC-013-01, CLM-WERPC-013-02, CLM-WERPC-013-03 |
| Drift claims | CLM-WERPC-013-04, CLM-WERPC-013-05, CLM-WERPC-013-06 |
| Out-of-ledger observations | observed proposals=1; allocated=1; unallocated=0; outside-request/new-owner=0; SRC-WERPC-091->REQ-WERPC-009 |

### 2026-09-05 external-only reverification reconciliation

승인된 2026-09-05 후속 cycle은 owner 서른여섯 개 전부의 외부 증거 층을 다시
관찰했고 요청자의 지시에 따라 workspace 재관찰은 일부러 제외했다. 주제별 owner마다
날짜가 붙은 하위 절을 하나씩 덧붙였고 원장을 `SRC-WERPC-154`까지 늘렸으며 주장
구간 `CLM-WERPC-016-01`부터 `CLM-WERPC-016-18`까지를 열었다. 요구사항 상태는 바꾸지
않았다.

보고된 결과는 다음과 같다.

- **이전 서술이 대체된 변화.** 서술 세 개가 2026-09-05부로 대체되었고 이전
  형태는 각자의 날짜에서는 여전히 사실이다. 2026-08-14에 기록한 subagent model
  해석 순서, upstream agent catalogue의 기본 branch가 보존해 둔 비교 pin과
  바이트 단위로 같다는 주장, 직접 요청으로 끊긴 것이 확인되어 현재 위치로 다시
  연결한 전달 관련 인용 하나다.
- **coverage 확대에 따른 변화.** agent harness와 loop 유형에 대한 공식 정의가
  이제 존재하며 처음으로 등록되었다. 두 provider 모두 provider 간 instruction
  import 연결을 문서화했다. permission mode와 hook surface는 이 pack이 열거했던
  어떤 목록보다도 훨씬 넓다. upstream spec-driven 프로젝트는 1.0 계열에 도달했고
  명령 family가 더 늘었다.
- **현재성에 따른 변화.** 지난 증분 이후 orchestrator의 새 minor가 나와 지원
  범위가 옮겨졌다. node 배포판과 로그 수집 agent는 기록된 pin에서 더 멀어졌다.
  secret 관리 operator의 release를 처음으로 기록했다.
- **변화 없음.** instruction 탐색 체인과 그 크기 제한, 설정 reference, sandbox와
  승인 어휘, 두 번째 provider의 memory 기본값, 문서 framework의 네 가지 mode,
  현재 protocol revision과 그 리소스 의미, index 제안의 비공식 상태, 접근 경로만
  바뀐 표준 내용, 전달 플랫폼의 권한·동시성·보존·연합 identity·API 버전 계약이다.
- **도달 불가.** vendor agent 가이드 하나를 읽지 못했다. HTML mirror가 HTTP
  403을 돌려주었고 문서 본문을 추출하지 못했다. 이는 `unchanged`가 아니라
  `unreachable`로 기록했으며 여기에 기대는 주장은 없다. 공개 index 두 곳이 한
  표준 후속 초안의 단계를 서로 다르게 적고 있고 이를 가려 줄 페이지는 HTTP
  403을 돌려주었다. 이 불일치는 미해결로 기록했다.
- **할당 전 기각.** 수집 중에 제기된 link rot 후보 세 개는 직접 요청 결과와
  맞지 않아 철회했다. 검색 결과로만 뒷받침되는 redirect 모순 하나는 발견이 아니라
  미검증으로 기록했다.

이 cycle은 외부 관찰만 기록한다. 이전 full-corpus cycle이 기대했던 이중 관찰을
충족하지 않으며 모든 workspace selector는 이전 관찰 날짜를 유지한다. 여기의 어떤
서술도 pack이 현재 저장소 트리와 맞춰져 있다고 주장하지 않는다.

## Refresh and Succession

WERPC-002부터 WERPC-006까지는 배정된 owner에 날짜가 붙은, 출처에 근거한 발견을
추가한다. WERPC-007은 바뀔 수 있는 소비자를 분류한다. 선행 파일은 WERPC-008만이
닫힌 쪽으로 실패하는 준비 증명을 거친 뒤에 삭제할 수 있다.

## Evidence Boundary

이 기준선은 저장소 정적 경로와 역사적 선행 증거를 기록한다. hosted CI,
provider runtime, 인증, 원격, credential을 담은 증거, secret 값, live cluster
증거를 주장하지 않는다.

## Related Documents

- [Archive index](../../../98.archive/README.md)는 이 pack을 만든 통합 Plan을
  안내한다. 계보일 뿐 현재 owner가 아니다.
- [Source coverage](m0012-source-coverage.md)
