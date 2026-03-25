# docs/ 문서 체계 안내

이 공간은 `hy-home.k8s` 프로젝트의 모든 비즈니스 요구, 아키텍처 설계, 기술 결정 및 운영 기록을 관리하는 중심지입니다.

## 우리의 목표

단순히 문서를 저장하는 공간이 아닙니다. 이 체계는 다음을 보장하기 위해 설계되었습니다.

1. **투명한 추적성**: 모든 기술적 결정(`ADR`)이 기획(`PRD`)부터 운영 기록까지 선명하게 연결되도록 합니다.
2. **검증 가능한 설계**: `TDD` 원칙에 따라, 모든 구현은 검증 가능한 명세를 먼저 갖추어야 합니다.
3. **AI 협업 최적화**: 인간과 AI Agent가 동일한 구조적 문맥을 공유하며 안전하게 협업할 수 있는 환경을 제공합니다.

## 문서의 흐름 (Lifecycle)

작업은 아래의 흐름을 따라 발전하며 구체화됩니다.

`01.prd` (기획) → `02.ard/03.adr` (설계/결정) → `04.specs` (상세 명세) → `05.plans/06.tasks` (실행/작업) → `07~09` (운영 지침) → `10~11` (사고/회고)

## 작성 가치 (SSoT Principles)

- **언어 원칙**:
  - **내부 지침**: AI Agent가 해석하는 내부 지침(`docs/00.agent-governance/`)은 추론 정확도를 위해 **English**로 작성합니다.
  - **외부 문서**: 인간이 읽고 검토하는 `README.md` 및 개요 문서는 **한국어** 작성을 원칙으로 합니다.
  - **응답 원칙**: 사용자의 모든 요청에 대한 응답은 **한국어(Korean)**로 합니다.
- **Spec-First**: 코드를 작성하기 전에 반드시 `PRD`와 `Spec`이 승인되어야 합니다.
- **Relativity**: 모든 경로는 상대 경로를 사용하여 이동성과 호환성을 확보합니다.

---

## 디렉터리 안내

- **[00.agent](00.agent/README.md)**: AI Agent 전용 지침 및 Governance (Lazy Loading)
- **[01.prd](01.prd/README.md)**: 기획서 (Vision, User Journey, Requirements)
- **[02.ard](02.ard/README.md)** / **[03.adr](03.adr/README.md)**: 아키텍처 모델 및 결정 기록
- **[04.specs](04.specs/README.md)**: 기능별 상세 설계 및 기술 명세 (SSoT)
- **[05.plans](05.plans/README.md)** / **[06.tasks](06.tasks/README.md)**: 구현 계획 및 개별 작업 현황
- **[07~11.Operations](08.operations/README.md)**: 운영 정책, 런북, 사고 대처 및 사후 분석
- **[99.templates](99.templates/README.md)**: 표준 문서 서식
