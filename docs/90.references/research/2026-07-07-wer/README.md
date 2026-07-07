# Workspace Engineering Research Pack (2026-07-07)

## Overview

이 폴더는 `hy-home.k8s` 워크스페이스의 목적, 역할, 거버넌스, CI/CD, QA, 포맷팅, 자동화, 스펙 주도 개발, 쿠버네티스/인프라 보안, 그리고 AI 에이전트의 비교 분석에 대한 2026-07-07 기준의 최신 연구 및 분석 자료를 보존하는 dated research pack이다.

WER-008 이후 추가된 `observability-reviewer`와 `network-reviewer` 에이전트의 구현 및 gap-closure 상태를 반영하며, 외부 소스인 `msitarzewski/agency-agents`와의 상세 비교 분석 결과를 담고 있다.

이 폴더는 설명용 참고 문서로서, 실제 실행 정책, CI 설정, 인프라 권한, 배포 승인 절차를 직접 정의하거나 변경하지 않는다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 2026-07-07 기준의 워크스페이스 연구 팩 파일 인덱스
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

## Authority Boundary

이 연구 팩은 참고용 lookup, 정의, 2026-07-07 기준의 소스 분석만을 다룬다. 실제 워크스페이스의 실행 규칙, 인프라 manifests, secrets, CI workflow, pre-commit config 등은 각 canonical owner가 단독으로 지배한다.

## Review and Freshness

- Review cadence: 소스 또는 거버넌스 체계 변경 시
- Last reviewed: 2026-07-07
- Next review trigger: 프로바이더 API/CLI 버전 범프, 거버넌스 규칙 변경, 에이전트 로스터 변경, `agency-agents` 구조 재개편

## Related Documents

- **Research README**: [../README.md](../README.md)
- **References README**: [../../README.md](../../README.md)
- **Harness Catalog**: [../../../00.agent-governance/harness-catalog.md](../../../00.agent-governance/harness-catalog.md)
- **Spec**: [../../../03.specs/017-workspace-engineering-research-pack/spec.md](../../../03.specs/017-workspace-engineering-research-pack/spec.md)
- **Plan**: [../../../04.execution/plans/2026-07-07-workspace-engineering-research-pack-refresh.md](../../../04.execution/plans/2026-07-07-workspace-engineering-research-pack-refresh.md)
- **Task**: [../../../04.execution/tasks/2026-07-07-workspace-engineering-research-pack-refresh.md](../../../04.execution/tasks/2026-07-07-workspace-engineering-research-pack-refresh.md)
