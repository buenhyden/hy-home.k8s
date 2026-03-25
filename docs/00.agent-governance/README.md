# 00. Agent Governance (AI 에이전트 거버넌스)

이 폴더는 `hy-home.k8s` 프로젝트 내에서 활동하는 AI 에이전트들을 위한 전용 실행 지침과 규칙을 담고 있습니다. 우리의 에이전트들은 이 가이드라인을 최상위 원칙으로 삼아 정확하고 안전한 작업을 수행합니다.

## 1. 언어 및 운영 원칙 (Language Strategy)

에이전트의 사고 효율성과 사용자의 편의성을 모두 잡기 위해 다음과 같은 이원화 전략을 사용합니다.

- **내부 지침 (Internal Docs)**: AI 에이전트가 직접 읽고 실행하는 규칙(`Rules`, `Scopes`, `Providers`)은 무조건 **English**로 작성합니다. 이는 모델의 추론 성능을 극대화하고 토근 사용량을 최적화하기 위함입니다.
- **사용자 가이드 (User-Facing)**: 인간이 읽는 `README.md` 및 개요 문서는 **한국어(Korean)**로 핵심 지침을 제공합니다.
- **응답 원칙 (Response Mandate)**: 에이전트가 내부적으로 어떤 언어를 사용하든, 사용자와의 대화는 항상 **한국어**로 진행합니다.

## 2. 지능형 지연 로딩 (Lazy Loading Protocol - JIT)

모든 문서를 한꺼번에 읽는 것은 비효율적입니다. 에이전트는 필요한 순간에만 필요한 정보를 로드하는 **Just-In-Time (JIT)** 전략을 따릅니다.

1. **의도 파악 (Intent Identification)**: 요청받은 작업의 성격을 먼저 조율합니다.
2. **부트스트랩 (Bootstrap)**: [rules/bootstrap.md](rules/bootstrap.md)를 통해 기본 분류 체계와 거버넌스를 확인합니다.
3. **스코프 로딩 (Scope Loading)**: 작업 레이어에 맞는 상세 지침을 [scopes/](scopes/)에서 동적으로 로드합니다.

## 3. 주요 구성 요소

- **[agent-instructions.md](agent-instructions.md)**: 에이전트 실행의 통합 관문(Gateway).
- **[rules/persona-matrix.md](rules/persona-matrix.md)**: 작업 성격별 페르소나 및 규칙 매핑 테이블.
- **[claude-provider.md](claude-provider.md) / [gemini-provider.md](gemini-provider.md)**: 각 모델 엔진에 최적화된 실행 가이드.

---
> [!IMPORTANT]
> 에이전트 운영 정책의 변경은 반드시 [08.operations/](../08.operations/README.md)에 정의된 통제 절차를 준수해야 합니다.
