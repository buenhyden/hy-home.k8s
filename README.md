# hy-home.k8s: 지능형 홈랩의 새로운 기준

`hy-home.k8s`는 단순한 서버 구축을 넘어, 사람과 AI가 문서와 코드로 협업하는 스마트 홈랩 프레임워크입니다. 모든 과정은 **Spec-Driven Development (SDD)**를 기반으로 하며, `docs/` 단계 체계로 설계부터 운영까지의 맥락을 추적합니다.

## 🚀 프로젝트의 심장, 문서 체계

프로젝트의 핵심 지식은 `docs/` 폴더의 단계 구조로 관리합니다.

- **00. 거버넌스 (Agent)**: AI 작업 방식과 규칙 ([상세 보기](docs/00.agent-governance/README.md))
- **01. 제품 요구사항 (PRD)**: 무엇을 왜 만드는지
- **02~03. 설계와 결정 (ARD/ADR)**: 아키텍처 구조와 기술 의사결정
- **04. 상세 명세 (Spec)**: 구현 기준이 되는 기술 명세
- **05~06. 계획과 작업 (Plan/Task)**: 실행 계획과 작업 증거
- **07~11. 운영 및 회고 (Guides/Ops/Runbooks/Incidents/Postmortems)**: 운영 기준, 대응, 학습

## 📐 문서 언어 정책 (중요)

문서의 독자에 따라 언어를 분리합니다.

1. **AI Agent 실행 문서: 영어**
- 대상: `docs/00.agent-governance/*` 및 AI가 직접 수행 기준으로 참조하는 거버넌스/제어 문서
- 목적: 에이전트 추론 정확도와 도구 실행 일관성 확보

2. **사람 중심 문서: 한글**
- 대상: 루트 `README.md`, `docs/README.md`, 각 단계 폴더의 인간 안내용 README
- 목적: 팀 온보딩과 운영 커뮤니케이션 효율 확보

3. **응답 언어**
- 사용자 대상 최종 응답은 항상 **한글**로 제공

## 🛠 시작하기

- AI 에이전트 진입점: [AGENTS.md](AGENTS.md)
- Claude 오버레이: [CLAUDE.md](CLAUDE.md)
- Gemini 오버레이: [GEMINI.md](GEMINI.md)
- 단계별 문서 안내: [docs/README.md](docs/README.md)

---
> [!NOTE]
> 이 프로젝트는 2026년 3월 기준 거버넌스/문서 운영 규칙을 반영합니다.
