---
title: "Claude Native Adapter"
version: "2.5.3"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-18"
---

# Claude Native Adapter

## Service

### Purpose

공통 정책, 역할 의미, 절차는 [공통 권한 원본](../.agents/README.md)에 있다.
이 디렉터리는 Claude 문법, 지원 메모, native 연결만 소유한다.

- `agents/`: 공통 파일을 명시적으로 읽는 native 역할 정의.
- `bindings.json`: 검증되는 역할 projection이 소비하는 Claude model, effort,
  skill, 권한의 정규 값.
- `CLAUDE.md`: 명시적으로 읽는 provider baseline.
- [provider.md](provider.md): provider별 적재·지원 계약.
- `settings.json`: 현재 권한(allow, ask, deny), bypass 모드 비활성화, 등록된
  사전 동작 hook과 세션 수집 hook, native 자동 memory 비활성화(`autoMemoryEnabled: false`).
  권한 범위와 남은 한계는 [provider.md](provider.md)가 소유한다.
- `hooks/k8s-pre-edit.sh`: shell과 구조화 파일 도구에 대한 동기식 쓰기
  경계의 Claude adapter. 자기 provider 이름을 붙여 payload를 넘길 뿐이고,
  경계 자체는 `scripts/provider_write_guard.py`가 소유한다. provider마다 자기
  adapter를 등록하므로 두 provider가 함께 의존하는 통제를 한 provider
  디렉터리가 소유하지 않는다.
- 같은 hook 디렉터리의 `session-capture.sh`: 세션 수명주기 이벤트를 로컬 세션 수집기
  `scripts/session_capture.py`에 넘기는 adapter. 위치와 구조만 기록하고 본문은
  복사하지 않으며, 실패해도 세션을 멈추지 않는다.
- `skills/<id>`: 공통 skill package마다 상대 링크 하나.
- `commands/<id>.md`: 공통 prompt 계약마다 진입점 하나. 각 진입점은 자기
  식별자로 `scripts/prompt-input.py`를 호출할 뿐 자체 계약을 갖지 않으며,
  입력, 출력, 거절 조건은 `.agents/prompts/`가 유지한다.

### Interfaces

- [Common work lifecycle](../.agents/workflows/work-lifecycle.md)
- [Approval and safety](../.agents/governance/approval-and-safety.md)
- [Quality](../.agents/governance/quality.md)
- [Model selection](../.agents/governance/model-selection.md)

#### Security Boundary

이 문서에는 secret, credential, 권한 경계만을 다루는 별도 내용이 없으며, 권한 관련 설명은 Purpose의 `settings.json` 항목에 적혀 있다.

## Usage

### Prerequisites

공통 계약은 [roles/registry.json](../.agents/roles/registry.json)과 선택한
정규 역할에서 고친다. [bindings.json](bindings.json)은 이 provider의 등급별
model, effort, native 도구, 역할별 예외를 소유하고 중립 registry는 그 경로를
참조한다. 역할 Markdown 파일은 이 표를 소비하며 검증받는 소비자이고, 중립
등급 상한의 제약을 받는다. 경로가 바뀌면 영향받는 참조를 함께 고친다. 정적
일치는 model 접근, 역할 발견, 권한 강제를 증명하지 않는다. 생성기는 쓰지
않는다.

### Selected Start

Claude 세션은 [provider baseline](CLAUDE.md)에서 시작해 선택된 공통 역할과
그 역할에 필요한 절차를 적용한다. 공통 skill은 명시적으로만 호출되며 추가
도구나 승인을 주지 않는다. 절차의 원본은 `.agents/skills/` 한 곳이다. 개인 로컬 설정과 memory는
공통 정책이 아니며, 재사용할 맥락은 공유 workspace memory store에 둔다.

## Checks

### Readiness

`python3 scripts/validate-agent-governance.py --root .`는 registry,
binding 표 문법, 정확한 역할·skill 참조, 링크 경계, 중립 상한 권한 일치를
검사한다. affected와 staged gate는 현재 validation registry에서 실제 입력에
맞게 선택된다. 퇴역한 full/ci sweep은 완료 명령이 아니다. 실제 native 적재,
호출, hook 이벤트는 승인된 새 세션에서 따로 얻는 근거다.

### Failure Handling

이 문서는 운영 관측과 복구만을 다루는 내용을 따로 두지 않는다. 그런 내용을 두게 되면 여기에 적는다.

#### Runbook Links

이 문서는 runbook이나 운영 가이드 링크를 따로 두지 않는다. 연결할 운영 문서가 생기면 여기에 연결한다.
