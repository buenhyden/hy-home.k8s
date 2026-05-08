# docs: 프로젝트의 모든 것

> [!NOTE]
> All AI agent interactions with this documentation suite must comply with the [Agent Governance Hub](./00.agent-governance/README.md).

여기는 `hy-home.k8s` 프로젝트가 어떻게 돌아가는지, 어떤 고민을 거쳐 지금의 모습이 되었는지를 기록하는 저장소입니다. 기획부터 아키텍처, 실제 구현 작업과 운영 기록까지 모든 정보가 이곳에 모입니다.

## 우리가 문서를 대하는 방식

단순히 기록을 남기기 위해 쓰는 문서는 지양합니다. 우리는 다음 가치에 집중합니다.

1. **이어지는 맥락 (Traceability)**: 기획(`PRD`) 단계의 고민이 아키텍처 결정(`ADR`)을 거쳐 실제 작업(`Task`)까지 어떻게 연결되는지 한눈에 볼 수 있어야 합니다.
2. **먼저 설계하고 나중에 구현 (Spec-First)**: 무작정 코드부터 짜기보다는, 무엇을 만들고 어떻게 검증할지 명세(`Spec`)를 먼저 고민합니다.
3. **인간과 AI의 팀플레이**: AI 에이전트와 사람이 같은 구조와 맥락을 공유하며 안전하고 효율적으로 협업할 수 있는 환경을 만듭니다.

## 문서의 흐름 (Lifecycle)

모든 작업은 아이디어에서 시작해 회고까지 선형적인 흐름을 따라 구체화됩니다.

`01.prd` (기획) → `02.ard/03.adr` (설계/결정) → `04.specs` (상세 명세) → `05.plans/06.tasks` (실행/작업) → `07~09` (운영 지침) → `10.incidents` (사고/회고)

## 언어 및 협업 원칙

소통의 효율을 위해 역할을 나눴습니다.

- **AI 에이전트용 (Internal English)**: 에이전트의 정확한 추론을 돕기 위해 내부 지침(`00.agent-governance/`)과 기술 명세 상세는 **영어**로 작성합니다.
- **사람용 (External Korean)**: 프로젝트 전체를 이해하기 위한 `README.md`와 개요 문서는 **한국어**가 기본입니다.
- **응답 원칙**: 사용자의 요청에 대한 모든 답변은 항상 **한글**로 합니다.

---

## 디렉터리 안내

- **[00.agent-governance](00.agent-governance/README.md)**: AI 에이전트 전용 지침 및 거버넌스 (Lazy Loading)
- **[01.prd](01.prd/README.md)**: 프로젝트 기획 및 요구사항 (Vision, Requirements)
- **[02.ard](02.ard/README.md)** / **[03.adr](03.adr/README.md)**: 아키텍처 모델 및 의사결정 기록
- **[04.specs](04.specs/README.md)**: 기술 명세 및 상세 설계 (SSoT)
- **[05.plans](05.plans/README.md)** / **[06.tasks](06.tasks/README.md)**: 구현 계획 및 작업 현황 관리
- **[07.guides](07.guides/README.md)** / **[08.operations](08.operations/README.md)**: 가이드라인 및 운영 정책
- **[09.runbooks](09.runbooks/README.md)** / **[10.incidents](10.incidents/README.md)**: 운영 절차, 사고 대응 기록, 장애 회고
- **[90.references](90.references/README.md)** / **[99.templates](99.templates/README.md)**: 참고 자료와 공통 템플릿
