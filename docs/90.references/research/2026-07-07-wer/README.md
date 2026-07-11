# Workspace Engineering Research Pack (2026-07-07)

## Overview

이 폴더는 `hy-home.k8s` 워크스페이스의 목적, 역할, 거버넌스, CI/CD, QA,
포맷팅, 자동화, 스펙 주도 개발, 쿠버네티스/인프라 보안, 그리고 AI 에이전트
비교 분석을 보존하는 `2026-07-07` dated research pack이다. 팩 이름은 최초
작성일을 보존하며, 아래 일곱 reference와 이 인덱스는 2026-07-10 fact-first
감사에서 현재 저장소 증적과 공식 외부 소스에 맞게 재검토되었다.

현재 파일 증적은 `observability-reviewer`와 `network-reviewer`를 포함한 10개
역할과 세 adapter surface의 30개 파일을 확인한다. 외부
`msitarzewski/agency-agents` 비교는 `2026-07-10 10:00 KST` 이전의 마지막
고정 commit을 사용한 비권위적 market scan이다.

이 폴더는 설명용 참고 문서로서, 실제 실행 정책, CI 설정, 인프라 권한, 배포 승인 절차를 직접 정의하거나 변경하지 않는다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- `2026-07-07` dated pack의 2026-07-10 재검토 인덱스
- 워크스페이스 거버넌스, 하네스/루프 엔지니어링, 프로바이더 구현 상태 분석
- 스펙 주도 개발, CI/CD, QA, 자동화, 파이프라인 분석
- 쿠버네티스/인프라/보안 분석
- 워크스페이스 에이전트와 `agency-agents` 간의 gap analysis

### Out of Scope

- 실 클러스터, 클라우드 리소스, Vault/ESO 런타임의 수정 및 생성
- secrets/credentials 정보의 노출 및 직접 조회
- 실제 GitHub remote 설정 또는 Actions 실행 방식 변경
- 시장 분석 자료를 워크스페이스 운영의 절대적인 기준으로 삼는 행위

## Structure

```text
2026-07-07-wer/
├── README.md                               # 이 파일 (인덱스 및 거버넌스 경계)
├── workspace-governance-baseline.md        # 워크스페이스 목적, 역할, 계약, 규칙 요약
├── harness-and-loop-engineering.md         # 하네스 및 루프 엔지니어링 개념 및 적용
├── provider-implementation-status.md       # Claude, Codex, Gemini 구현 비교 및 공통 체계
├── spec-sdlc-ci-qa-formatting.md           # 스펙 주도 개발, SDLC, CI/CD, 포맷팅 검증
├── kubernetes-infrastructure-security.md   # 쿠버네티스, 인프라, GitOps, 보안 분석
├── automation-pipeline-workflow-qa.md      # 자동화, 파이프라인, 워크플로우 구성
└── ai-agents-roster-and-gap-analysis.md    # 워크스페이스 AI 에이전트 로스터 및 gap analysis
```

## Source Priority

소스 간 내용 상충 시 다음 우선순위를 따른다:

1. Canonical repository owners (거버넌스, 정책, 스크립트 정본)
2. Official product, provider, standards documentation (공식 제품/프로바이더 문서)
3. Repo-backed evidence (커밋된 manifests, configs, templates)
4. Official issue trackers / release notes (공식 이슈/릴리즈 노트)
5. Market scan, vendor marketing, blog, benchmark (시장 분석 및 외부 아티클)

시장 분석 자료는 비권장/비공식(non-authoritative)으로 분류하며, 워크스페이스 정책을 덮어쓸 수 없다.

모든 로컬 구현 판단은 현재 repository owner와 tracked evidence가 지배한다.
모델, provider, 표준, upstream 사실은 아래 고정 cutoff에 확인한 공식/primary
source가 지배하며, cutoff 이후의 웹 페이지 변경을 이 스냅샷에 소급하지 않는다.

## How to Work in This Pack

1. 이 팩의 모든 수정 사항은 Parent Spec/Plan을 따르고, Stage 04 task에 증적을 남긴다.
2. 새 문서는 [reference.template.md](../../../99.templates/templates/common/reference.template.md)를 준수하여 작성한다.
3. 소스 체크 일자(Source checked)와 freshness trigger, 권한 경계를 매 문서마다 명확히 밝힌다.

## How to Work in This Area

이 영역의 모든 작업은 위의 `How to Work in This Pack` 수칙을 따른다.

## Link Basis

이 README의 링크 기준 위치는 `docs/90.references/research/2026-07-07-wer/`이다.

- 동기화된 파일은 상대 링크(예: `./workspace-governance-baseline.md`)로 연결한다.
- 상위 Research README는 `../README.md`로 연결한다.
- 상위 Stage 90 README는 `../../README.md`로 연결한다.
- canonical stages 경로는 `../../../<stage>/`로 계산한다.
- root level 소스는 `../../../../<path>`를 기준으로 삼는다.

## Pack Index

| Reference | Status | Role | Authority Boundary |
| --- | --- | --- | --- |
| [workspace-governance-baseline.md](workspace-governance-baseline.md) | Current | 워크스페이스 거버넌스 및 운영 baseline 요약 | 설명용 요약서; active governance 정책은 Stage 00이 소유 |
| [harness-and-loop-engineering.md](harness-and-loop-engineering.md) | Current | 하네스/루프 엔지니어링 개념 및 환경/체계 분석 | 개념 요약서; 런타임 제어나 실행 동작을 직접 변경하지 않음 |
| [provider-implementation-status.md](provider-implementation-status.md) | Current | Claude, Codex, Gemini 구현 현황 및 공통 체계 구축 | 프로바이더 비교서; 실제 프로바이더의 API/config 설정을 덮어쓰지 않음 |
| [spec-sdlc-ci-qa-formatting.md](spec-sdlc-ci-qa-formatting.md) | Current | 스펙 주도 개발, SDLC, CI/CD, QA, 포맷팅 분석 | 검증 방식 요약; 실제 Actions/pre-commit 구성은 관련 config가 소유 |
| [kubernetes-infrastructure-security.md](kubernetes-infrastructure-security.md) | Current | 쿠버네티스, 인프라, GitOps, 보안 및 secrets 분석 | 인프라 구조 분석; 실 클러스터 변경 및 Vault/secrets/reconciliation에 관여 불가 |
| [automation-pipeline-workflow-qa.md](automation-pipeline-workflow-qa.md) | Current | 자동화, 파이프라인, 워크플로우 구성 및 DORA metrics 분석 | 파이프라인 분석; 워크플로우 실행 로직이나 CI job 설정을 변경하지 않음 |
| [ai-agents-roster-and-gap-analysis.md](ai-agents-roster-and-gap-analysis.md) | Current | 에이전트 로스터 비교 및 `agency-agents`와의 gap analysis | 로스터 및 gap 분석; 실제 local agent configuration은 Stage 00/harness가 소유 |

## Model Source Cutoff

- **Provider/model cutoff**: `2026-07-10 10:00 KST`
- **Repository observation date**: `2026-07-10`
- **`agency-agents` snapshot**:
  `9f3e401ccd09aa0ee0ef8e015226d0647908e01e`, the last `main` commit before
  the cutoff.
- **Surface rule**: API publication, coding-agent product availability, CLI
  routing, account/auth entitlement, local adapter declaration, lifecycle, and
  recommendation remain separate claims.
- **Freshness rule**: provider model or lifecycle claims are refreshed from the
  exact official URLs in
  [Provider Implementation Status](provider-implementation-status.md) and
  [AI Agents Roster and Gap Analysis](ai-agents-roster-and-gap-analysis.md).
  The dated pack is not silently rewritten from pages changed after the cutoff.

The cutoff snapshot records Claude Fable 5, Opus 4.8, Sonnet 5, and Haiku 4.5;
Codex-product GPT-5.6 Sol/Terra/Luna, previous-generation GPT-5.5, GPT-5.4
Mini, and authentication-surface-specific GPT-5.3-Codex; and Gemini API 3.1
Pro Preview, 3.5 Flash Stable, and 3.1 Flash-Lite Stable. These official
catalog facts do not prove local availability, native resolution, or approval
to change the active model policy.

## Integrated Audit Snapshot Contract

The initial document inventory is fixed to repository commit
`ab3556b8d5a9ae6f469a751057d9ad5ef261cdf7` and observation date
`2026-07-11`. This is the baseline used to start the integrated audit; it is
not the final audit observation SHA. The completed audit pack records its final
observation SHA separately after all research and report changes are complete.

Counts below use the top-level frontmatter `status` of authored documents.
Folder and stage `README.md` indexes are inventory surfaces, but are excluded
from authored-document counts and status totals.

| Family and path basis | Authored inventory at the initial snapshot | Status basis |
| --- | --- | --- |
| PRD — `docs/01.requirements/*.md` | 4 | 4 `active` |
| ARD — `docs/02.architecture/requirements/*.md` | 4 | 4 `active` |
| ADR — `docs/02.architecture/decisions/*.md` | 9 | 9 `accepted` |
| Spec — `docs/03.specs/*/spec.md` | 20 | 16 `draft`; 4 `active` |
| Agent design — `docs/03.specs/*/agent-design.md` | 1 | 1 `draft` |
| Plan — `docs/04.execution/plans/*.md` | 41 | 41 `done` |
| Task — `docs/04.execution/tasks/*.md` | 43 | 43 `done` |
| Guide — `docs/05.operations/guides/*.md` | 8 | 8 `active` |
| Policy — `docs/05.operations/policies/*.md` | 7 | 7 `active` |
| Runbook — `docs/05.operations/runbooks/*.md` | 9 | 9 `active` |
| Incident — `docs/05.operations/incidents/*.md` | 0 | No authored incident record; `README.md` is index-only. |
| Postmortem — `docs/05.operations/incidents/` postmortem records | 0 | No authored postmortem record. |

### Shared Measurement Contract

Every applicable control uses the same maturity levels: `0 absent`,
`1 documented/routed`, `2 repository-static`,
`3 deterministic local+CI enforcement`, and
`4 runtime/operational evidence`. Category implementation is calculated as
`sum(maturity) / (4 * applicable controls)`. Every report must disclose the
numerator, denominator, and each N/A exclusion.

The human verdict vocabulary is `Implemented`, `Partial`, `Gap`, or
`Not in scope`. Evidence confidence is `Verified repo-static`,
`Unverified live`, or `Conditional`. A higher maturity score never upgrades
confidence beyond the evidence actually observed.

### Research-to-Audit Topic Ownership

Each requested topic has exactly one primary Current research owner and one
planned audit owner. Planned audit paths remain code literals until created.

| Requested topic | Primary Current research owner | Planned audit owner |
| --- | --- | --- |
| Frontmatter keys and values | `spec-sdlc-ci-qa-formatting.md` | `sdlc-document-lifecycle-frontmatter.md` |
| Document state transitions | `spec-sdlc-ci-qa-formatting.md` | `sdlc-document-lifecycle-frontmatter.md` |
| Semantic lineage | `spec-sdlc-ci-qa-formatting.md` | `sdlc-document-lifecycle-frontmatter.md` |
| Release readiness | `spec-sdlc-ci-qa-formatting.md` | `sdlc-document-lifecycle-frontmatter.md` |
| Incident readiness | `spec-sdlc-ci-qa-formatting.md` | `sdlc-document-lifecycle-frontmatter.md` |
| Postmortem readiness | `spec-sdlc-ci-qa-formatting.md` | `sdlc-document-lifecycle-frontmatter.md` |
| AI-agent `pre-commit run --all-files` obligation | `spec-sdlc-ci-qa-formatting.md` | `ci-qa-automation-pipeline-workflow.md` |
| Vibe coding | `ai-agents-roster-and-gap-analysis.md` | `ai-agents-model-routing-vibe-coding.md` |
| `agency-agents` comparison | `ai-agents-roster-and-gap-analysis.md` | `ai-agents-model-routing-vibe-coding.md` |
| Task-model routing | `ai-agents-roster-and-gap-analysis.md` | `ai-agents-model-routing-vibe-coding.md` |

## Requirement Coverage Matrix

`Primary Current owner` assigns exactly one research owner to each requirement.
Secondary references may summarize a boundary and link here or to the primary
section; active policy and procedure remain with the canonical repository owner
named by that reference.

| Requirement | Primary Current owner | Workspace evidence | External benchmark | Audit status | Follow-up route |
| --- | --- | --- | --- | --- | --- |
| Workspace purpose | [Workspace Governance: purpose](workspace-governance-baseline.md#workspace-purpose-and-operating-contract) | Root README defines document SSoT, GitOps desired state, bootstrap assets, and external-service boundary. | OpenGitOps four principles provide comparison context. | Sufficient repo-static. | Root README and Stage 00 bootstrap governance. |
| Roles | [Workspace Governance: owners](workspace-governance-baseline.md#owner-and-authority-matrix) | Persona protocol, scopes, and 10 matching stems on each of three adapter surfaces. | OpenGitOps ownership context plus provider-native role sources. | Needs strengthening: canonical catalog still has three stale eight-role phrases. | Stage 00 harness-catalog maintenance task. |
| Overview | [Workspace Governance](workspace-governance-baseline.md#overview) | Root gateway, stage taxonomy, GitOps hierarchy, and validation owners. | OpenGitOps is the external system-level benchmark. | Sufficient as dated synthesis. | Root README and Stage 00/99 owners. |
| Operating contract | [Workspace Governance: operating contract](workspace-governance-baseline.md#workspace-purpose-and-operating-contract) | Repo-first planning, explicit validation, GitOps-first desired-state flow, and approval boundaries. | OpenGitOps declarative/pull/reconcile principles. | Sufficient repo-static; live reconciliation Unverified. | Stage 00 agentic/approval rules and Stage 05 operations. |
| Governance | [Workspace Governance: owner matrix](workspace-governance-baseline.md#owner-and-authority-matrix) | Stage 00 rules, Stage 99 support contracts, Stage 04 evidence, and Stage 05 operations. | OpenGitOps separates desired state from observed convergence. | Needs strengthening where duplicate lifecycle summaries and currentness drift remain. | Governance Gap Register in the primary owner. |
| System / 체계 | [Workspace Governance: enforcement map](workspace-governance-baseline.md#enforcement-and-evidence-map) | Instructions, preventive controls, feedback evidence, and knowledge stores have explicit owners. | OpenAI harness guidance supports legible repository contracts and mechanical checks. | Sufficient architecture; runtime parity Unverified. | Stage 00 harness implementation map. |
| Rules | [Workspace Governance: enforcement map](workspace-governance-baseline.md#enforcement-and-evidence-map) | Bootstrap, agentic, approval, persona, routing, and postflight contracts are linked rather than copied. | OpenGitOps and provider-native permission guidance are comparison sources. | Sufficient descriptive routing. | Exact Stage 00 rule owner linked by the primary reference. |
| Templates | [Workspace Governance: owner matrix](workspace-governance-baseline.md#owner-and-authority-matrix) | Stage 99 route map assigns one template per authored target; no Release route exists. | Spec Kit and primary document practices inform the SDLC comparison. | Needs strengthening: release evidence contract is absent. | Stage 99 routing/support through a new approved Spec/Plan/Task. |
| Scripts | [Workspace Governance: enforcement map](workspace-governance-baseline.md#enforcement-and-evidence-map) | Scripts inventory and repository/harness/manifest/policy validators define static checks. | pre-commit and official tool documentation define their individual lanes. | Sufficient for encoded static contracts; regex-heavy areas need strengthening. | Scripts README and a scoped validator-quality task. |
| Integration guides | [Workspace Governance: owner matrix](workspace-governance-baseline.md#owner-and-authority-matrix) | Stage 05 guides/runbooks and provider notes connect canonical owners without moving policy into Stage 90. | OpenGitOps and provider-native setup documentation supply comparison context. | Sufficient routing; live procedures remain canonical-owner only. | Stage 05 guide/runbook or provider-note owner. |
| Spec-driven development | [SDLC: local flow](spec-sdlc-ci-qa-formatting.md#spec-driven-development-and-local-flow) | PRD/ARD/ADR feed Spec, Plan, Task, and stable operations knowledge. | GitHub Spec Kit and NIST SSDF. | Sufficient descriptive flow; semantic lineage automation needs strengthening. | Stage 99 SDLC governance and a scoped traceability task. |
| SDLC | [SDLC: lifecycle matrix](spec-sdlc-ci-qa-formatting.md#lifecycle-and-traceability-matrix) | Stage 01–05 routes, states, inputs, owners, and handoffs were re-counted. | NIST SSDF and incident-response guidance. | Needs strengthening: Spec/Task maturity asymmetry remains. | Document Maturity Gap Register in the primary owner. |
| PRD | [SDLC: PRD row](spec-sdlc-ci-qa-formatting.md#lifecycle-and-traceability-matrix) | Stage 01 route owns problem, value, requirements, and acceptance criteria. | Workspace/industry convention; Spec Kit provides adjacent practice. | Sufficient local contract. | Stage 01 and PRD template owner. |
| ARD | [SDLC: ARD row](spec-sdlc-ci-qa-formatting.md#lifecycle-and-traceability-matrix) | Stage 02 requirements route owns boundary and quality attributes. | Workspace/industry convention, not presented as a universal standard. | Sufficient local contract. | Stage 02 architecture requirements and ARD template owner. |
| ADR | [SDLC: ADR row](spec-sdlc-ci-qa-formatting.md#lifecycle-and-traceability-matrix) | Stage 02 decision route owns alternatives, decision, consequences, and supersession. | Nygard/Cognitect ADR primary practice. | Sufficient local contract. | Stage 02 decisions and ADR template owner. |
| Spec, Plan, and Task | [SDLC: lifecycle matrix](spec-sdlc-ci-qa-formatting.md#lifecycle-and-traceability-matrix) | Stage 03 contract and Stage 04 decomposition/evidence routes are present. | Spec Kit and NIST SSDF supply lifecycle context. | Needs strengthening: 16/20 Specs were draft while 42/43 Tasks were done at audit time. | Lifecycle-promotion audit under Stage 03/04 and Stage 99. |
| Guide | [SDLC: Guide row](spec-sdlc-ci-qa-formatting.md#lifecycle-and-traceability-matrix) | Stage 05 guide route owns stable explanation and reproducibility. | NIST SSDF knowledge/operation context. | Sufficient local contract. | Stage 05 guides and guide template owner. |
| Incident | [SDLC: Incident row](spec-sdlc-ci-qa-formatting.md#lifecycle-and-traceability-matrix) | Incident route/template exists; no actual tracked incident record was found. | NIST SP 800-61 Rev. 3. | Unverified readiness; absence of a record is not exercise evidence. | Approved tabletop/evidence design through Stage 05 and a new task. |
| Postmortem | [SDLC: Postmortem row](spec-sdlc-ci-qa-formatting.md#lifecycle-and-traceability-matrix) | Postmortem route/template exists; no tracked postmortem record was found. | Google SRE postmortem culture. | Unverified readiness. | Stage 05 incident owner and approved tabletop/postmortem task. |
| Policy | [SDLC: Policy row](spec-sdlc-ci-qa-formatting.md#lifecycle-and-traceability-matrix) | Stage 05 policy route owns required/allowed/disallowed controls and exceptions. | NIST SSDF/security sources by subject. | Sufficient local contract. | Stage 05 policies and policy template owner. |
| Release | [SDLC: Release row](spec-sdlc-ci-qa-formatting.md#lifecycle-and-traceability-matrix) | Tag workflow creates a changelog artifact; no dedicated Release route/template/readiness record exists. | GitHub secure-use and supply-chain benchmarks. | Implementation gap. | Architecture/governance decision, then Stage 99/05/workflow task if adopted. |
| Runbook | [SDLC: Runbook row](spec-sdlc-ci-qa-formatting.md#lifecycle-and-traceability-matrix) | Stage 05 runbooks own executable recovery, validation, and rollback. | NIST incident guidance and tool-owner operations guidance. | Sufficient local contract; execution evidence is per approved run. | Stage 05 runbook owner. |
| Security | [Kubernetes Security: control matrix](kubernetes-infrastructure-security.md#platform-security-control-matrix) | RBAC, AppProject, secret, network, policy, image, workflow, and supply-chain surfaces were inspected. | Kubernetes, Argo CD, Vault, NIST, SLSA, and OpenSSF primary sources. | Partial repo-static controls; live enforcement Unverified. | Security Gap Register in the primary owner. |
| Kubernetes | [Kubernetes Security: control matrix](kubernetes-infrastructure-security.md#platform-security-control-matrix) | Desired-state manifests, Kustomize structure, AppProjects, policies, ESO, and validators. | Kubernetes official Secrets, RBAC, NetworkPolicy, and Kustomize guidance. | Implemented desired state; cluster acceptance/readiness Unverified. | GitOps manifests and Stage 05 operations through an approved task. |
| Infrastructure | [Kubernetes Security: evidence boundary](kubernetes-infrastructure-security.md#static-and-live-evidence-boundary) | Bootstrap, Vault HCL, static contracts, and operator-run live-test scripts are separated. | Vault, ESO, Argo CD, NIST, SLSA, and Scorecard sources. | Needs strengthening; transport/bootstrap and live assertions have routed gaps. | Infrastructure/security gap owner named by each finding. |
| CI/CD | [Automation: CI/CD boundary](automation-pipeline-workflow-qa.md#automation-workflow-pipeline-ci-and-cd) | Five workflows, six CI jobs, no deploy job, and separate Argo CD pull/reconcile intent. | GitHub Actions and OpenGitOps. | CI static topology sufficient; CD/live reconciliation Unverified. | CI workflow/guide and Stage 05 GitOps owner. |
| QA | [SDLC: QA evidence lanes](spec-sdlc-ci-qa-formatting.md#qa-evidence-lane-matrix) | Nine separate formatting, lint, parse, structural, manifest, secret, policy, artifact, and live lanes. | pre-commit, EditorConfig, Prettier, CommonMark, YAML, and GitHub guidance. | Sufficient lane map; each PASS is scope-limited. | Exact tool/config/CI owner for the affected lane. |
| Formatting | [SDLC: formatting interpretation](spec-sdlc-ci-qa-formatting.md#formatting-linting-and-syntax-interpretation) | EditorConfig, Prettier config/ignore, file-hygiene hooks, shfmt, and diff check are distinguished. | EditorConfig and Prettier official guidance. | Needs strengthening: Prettier execution wiring was not found. | Formatting configs plus a scoped pre-commit/CI decision task. |
| Linting | [SDLC: formatting interpretation](spec-sdlc-ci-qa-formatting.md#formatting-linting-and-syntax-interpretation) | Markdown, shell, Actions, Dockerfile, and Kubernetes linters have distinct scopes. | Official tool documentation and GitHub secure-use guidance. | Sufficient for configured tool/file scope. | Pre-commit and consuming config owner. |
| Syntax validation | [SDLC: QA evidence lanes](spec-sdlc-ci-qa-formatting.md#qa-evidence-lane-matrix) | Data/manifest parsers are wired. Shell `bash -n` is explicit manual or consumed shared-hook evidence after matching edits, not a dedicated CI job or repo-quality/harness command; tracked provider wiring alone does not prove native consumption. | CommonMark and YAML specifications. | Sufficient with explicit shell-lane and provider-consumption limitations. | CI/QA guide, shared hooks, and a scoped syntax-gate task if needed. |
| Automation | [Automation: inventory](automation-pipeline-workflow-qa.md#current-automation-inventory) | Actions, Dependabot, pre-commit, and provider-wired hooks have named triggers/evidence. | GitHub Actions and pre-commit official sources. | Sufficient inventory; specialist path/hook gaps remain. | Automation Gap Register in the primary owner. |
| Pipeline | [Automation: CI DAG](automation-pipeline-workflow-qa.md#actual-ci-job-dag) | Two parallel roots, three conditional jobs, and one aggregate summary are exact. | GitHub workflow syntax and visualization graph. | Sufficient; previous serial-DAG defect corrected. | `.github/workflows/ci.yml` for any future change. |
| Workflow | [Automation: inventory](automation-pipeline-workflow-qa.md#current-automation-inventory) | Five workflow files and their triggers, permissions, and outputs were inspected. | GitHub workflow syntax, permissions, concurrency, and secure-use guidance. | Needs strengthening: Actions use tags rather than immutable SHAs. | Separate Actions supply-chain hardening task. |
| Harness engineering | [Harness: ownership boundary](harness-and-loop-engineering.md#harness-ownership-boundary) | Canonical core, provider adapters, shared scripts, validation evidence, memory, and template owners are separated. | OpenAI harness engineering and provider-native sources. | Sufficient provider-neutral model; runtime parity Unverified. | Stage 00 harness catalog/implementation map. |
| Loop engineering | [Harness: control loop](harness-and-loop-engineering.md#provider-neutral-control-loop-matrix) | Observe/Plan/Act/Verify/Learn plus retry, compaction, and approval rows define bounded evidence flow. | OpenAI agent-loop and provider subagent documentation. | Needs strengthening: no common attempt schema or retry budget. | Stage 00 agentic rules through a separate approved task. |
| Harness/loop application system, environment, and rules | [Harness: evaluation and recovery](harness-and-loop-engineering.md#evaluation-and-recovery-loop) | Evidence lanes, recovery state, termination modes, memory, approval, and follow-up owners are explicit. | OpenAI, Claude, Codex, Gemini, and MCP official sources. | Needs strengthening; native canaries and compaction checkpoint contract are absent. | Harness and Loop Gap Register. |
| Claude | [Provider implementation](provider-implementation-status.md#native-surface-and-local-adapter-matrix) | Ten native-path adapters and tracked settings/permissions; local model strings remain declarations. | Anthropic model, configuration, hook, and subagent documentation. | Implementation gaps in model syntax/currentness; runtime availability Unverified. | Claude provider/model-policy migration task after eval. |
| Codex | [Provider implementation](provider-implementation-status.md#native-surface-and-local-adapter-matrix) | Ten standalone TOML adapters, tracked hook wiring, no tracked project config, and surface-specific model declarations. | OpenAI Codex/API model, subagent, config, and hook documentation. | Implementation gaps in model lifecycle/auth surface; runtime availability Unverified. | Codex auth inventory and evaluated migration task. |
| Gemini | [Provider implementation](provider-implementation-status.md#native-surface-and-local-adapter-matrix) | Ten `.agents/agents` local adapters and `.agents/hooks.json`; no native `.gemini/agents`/settings surface. | Gemini API model and Gemini CLI agent/hook/settings documentation. | Implementation gap for Gemini CLI native registration; local behavior Unverified. | Decide intended runtime, then scoped native adapter/settings task. |
| Shared provider environment, rules, and system | [Provider implementation: interpretation](provider-implementation-status.md#interpretation) | Thin gateways, Stage 00 governance, shared `.agents` assets, hook scripts, task evidence, and validators form the common repository layer. | Each provider's native settings, permission, sandbox, hook, and subagent sources. | Sufficient repository contract; not one provider-native runtime. | Provider-specific canary and active owner, never Stage 90. |
| Provider implementation status | [Provider implementation](provider-implementation-status.md) | 10-role/30-path matrix, three JSON surfaces, validator coverage, and local declarations. | 21 official provider URLs at the fixed cutoff. | Needs strengthening/Unverified by surface as recorded. | Provider Gap Register and exact canonical routes. |
| Workspace-required AI Agents | [AI agents: local roster](ai-agents-roster-and-gap-analysis.md#local-roster-and-shared-body-contract) | Ten bounded local roles cover supervision, implementation, review, security, incident, network, observability, and documentation work. | Pinned upstream roles are discovery context only. | Sufficient roster breadth; no new Candidate met the bar. | Harness catalog; add a role only through a new agent-design Spec/Task. |
| AI Agents | [AI agents: adapter status](ai-agents-roster-and-gap-analysis.md#provider-native-adapter-status) | 10 stems x 3 local surfaces = 30 files; provider metadata and validator depth differ. | Claude/Codex/Gemini native subagent documentation. | Needs strengthening: stem parity is not behavioral parity. | Provider-native canaries and scoped validator task. |
| `agency-agents` | [AI agents: upstream snapshot](ai-agents-roster-and-gap-analysis.md) | Pinned comparison records 17 divisions, 254 recursive files, 15 install targets, and 13 generated conversions. | Fixed upstream commit/tree/linter/converter/tools/license sources. | Sufficient reproducible market scan; non-authoritative for local policy. | Refresh from the last pre-cutoff commit when upstream changes. |
| Task-model routing | [AI agents: role routing](ai-agents-roster-and-gap-analysis.md#default-escalation-and-fallback-routing) | Ten role rows separate active declarations from default/escalation/fallback hypotheses and eval gates. | Official provider model/lifecycle sources at the cutoff. | Needs strengthening until native availability and task evals pass. | Model policy plus provider-specific migration Spec/Plan/Task. |
| MCP currentness and security | [Harness: MCP boundary](harness-and-loop-engineering.md#mcp-version-and-security-boundary) | No tracked MCP config; server/scopes/runtime remain Unverified. | MCP `2025-11-25` is Current; `2025-06-18` is historical Final; eight-category security taxonomy is used. | Unverified local implementation. | Separate approved provider/security MCP inventory task. |
| Supply-chain security | [Kubernetes Security: supply chain](kubernetes-infrastructure-security.md#supply-chain-security-analysis) | Scoped workflow permissions, secret/static tooling, tagged Actions, and missing provenance lanes are explicit. | NIST SP 800-204D, SLSA v1.2, OpenSSF Scorecard, and GitHub secure use. | Implementation gaps; no SLSA level claimed. | Threat-modelled CI/release supply-chain task. |
| Static versus live evidence | [Kubernetes Security: evidence boundary](kubernetes-infrastructure-security.md#static-and-live-evidence-boundary) | Desired state, repo-static, optional tools, CI declarations, operator live scripts, and unverified enforcement are separate. | Tool-owner and platform guidance defines the live enforcement boundary. | Sufficient boundary; live/remote readiness not tested. | Approved Stage 05 runbook/task evidence only. |

## Audit Outcome Summary

### Changed-Document Summary

| Current artifact | 2026-07-10 audit outcome |
| --- | --- |
| `README.md` | Added the fixed model cutoff, 48-row single-owner requirement map, contradiction closure, changed-document summary, and pack-wide freshness rules. |
| [Workspace Governance Baseline](workspace-governance-baseline.md) | Re-established purpose/contract/owner/enforcement maps and routed seven governance gaps without changing active owners. |
| [Harness and Loop Engineering](harness-and-loop-engineering.md) | Corrected ownership, added bounded loop/eval/recovery/termination design, and made MCP `2025-11-25` currentness explicit. |
| [Provider Implementation Status](provider-implementation-status.md) | Reconciled all 30 adapter paths, native/local surfaces, 17 model-surface rows, 13 migration rows, and fixed-cutoff provider sources. |
| [Spec SDLC CI QA Formatting](spec-sdlc-ci-qa-formatting.md) | Added 14 lifecycle document rows, nine QA lanes, source-backed document roles, and non-mutating maturity gaps. |
| [Kubernetes Infrastructure Security](kubernetes-infrastructure-security.md) | Rechecked desired state, 12 control rows, six evidence lanes, 15 primary sources, and 14 routed security gaps. |
| [Automation Pipeline Workflow QA](automation-pipeline-workflow-qa.md) | Corrected the six-job DAG, five-workflow inventory, path/hook coverage, GitOps delivery ownership, and seven automation gaps. |
| [AI Agents Roster and Gap Analysis](ai-agents-roster-and-gap-analysis.md) | Reconciled 10 roles/30 adapters and pinned upstream 17/254/15/13 evidence, role overlap, gap decisions, and role-model eval routes. |

### Pack-Wide Contradiction Closure

- **Roster**: current repository fact is 10 stems on each of three local
  surfaces, for 30 adapters. The three stale `Eight`/`eight` phrases exist only
  in the active Stage 00 catalog and are recorded as a follow-up gap, not a
  competing Current-pack count.
- **Upstream**: the pinned `agency-agents` facts are 17 divisions, 254 recursive
  Markdown files, 15 install targets, and 13 generated conversion targets.
  README `230+` remains a non-authoritative self-description; `147+` is stale.
- **Automation**: there are five workflow files and six `ci.yml` jobs.
  `branch-policy` and `changes` are parallel roots, not a serial chain.
- **Models**: exact IDs and lifecycle are owned by the provider reference at
  `2026-07-10 10:00 KST`; local labels are declarations, not availability.
- **Provider paths**: `.gemini/agents/*.md` is the Gemini CLI native custom-agent
  path; `.agents/agents/*.md` is this repository's Gemini/Antigravity-facing
  local adapter path.
- **GitOps ownership**: `root-platform` owns platform Applications under
  `gitops/apps/root`; `apps-generator` owns workload discovery under
  `gitops/workloads/*`.
- **Hooks and QA**: Claude settings bind `session-start.sh`, `k8s-pre-edit.sh`,
  `post-validate.sh`, and `lifecycle-guard.sh`, not `validate-harness.sh`
  directly. Prettier is configured but not found wired into pre-commit/CI.
  Shell `bash -n` evidence comes from an explicit manual run or a consumed
  shared hook after matching edits; the tracked wiring does not prove native
  provider consumption, and no dedicated CI, repo-quality, or harness command
  owns it.
- **MCP**: `2025-11-25` is Current and `2025-06-18` is historical Final.
- **Evidence boundary**: repository and static PASS results never establish
  provider-native, remote GitHub, cluster, controller, secret, or live-runtime
  readiness.

## Authority Boundary

이 연구 팩은 참고용 lookup, 정의, 그리고 2026-07-10에 재검토한 dated source
분석만을 다룬다. 실제 워크스페이스의 실행 규칙, 인프라 manifests, secrets,
CI workflow, pre-commit config, provider adapter/model policy 등은 각 canonical
owner가 단독으로 지배한다. 이 팩의 권고나 `Sufficient` 판정은 활성 파일 변경,
provider-native 동작, remote CI, 또는 live readiness를 승인하거나 증명하지 않는다.

## Review and Freshness

- Review cadence: 소스 또는 거버넌스 체계 변경 시
- Last reviewed: 2026-07-10
- Provider/model source cutoff: `2026-07-10 10:00 KST`
- Next review trigger: 프로바이더 API/CLI 버전 범프, 거버넌스 규칙 변경, 에이전트 로스터 변경, `agency-agents` 구조 재개편

## Related Documents

- **Research README**: [../README.md](../README.md)
- **References README**: [../../README.md](../../README.md)
- **Harness Catalog**: [../../../00.agent-governance/harness-catalog.md](../../../00.agent-governance/harness-catalog.md)
- **Spec**: [../../../03.specs/017-workspace-engineering-research-pack/spec.md](../../../03.specs/017-workspace-engineering-research-pack/spec.md)
- **Plan**: [../../../04.execution/plans/2026-07-07-workspace-engineering-research-pack-refresh.md](../../../04.execution/plans/2026-07-07-workspace-engineering-research-pack-refresh.md)
- **Task**: [../../../04.execution/tasks/2026-07-07-workspace-engineering-research-pack-refresh.md](../../../04.execution/tasks/2026-07-07-workspace-engineering-research-pack-refresh.md)
- **Current hardening Plan**: [../../../04.execution/plans/2026-07-10-current-research-pack-fact-first-hardening.md](../../../04.execution/plans/2026-07-10-current-research-pack-fact-first-hardening.md)
- **Current hardening Task**: [../../../04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md](../../../04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md)
