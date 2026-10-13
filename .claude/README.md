---
title: "Claude Native Adapter"
version: "2.3.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-13"
---

# Claude Native Adapter

## Overview

공통 정책, 역할 의미, 절차는 [공통 권한 원본](../.agents/README.md)에 있다.
이 디렉터리는 Claude 문법, 지원 메모, native 연결만 소유한다.

## Scope

공통 계약은 [roles/registry.json](../.agents/roles/registry.json)과 선택한
정규 역할에서 고친다. [bindings.json](bindings.json)은 이 provider의 등급별
model, effort, native 도구, 역할별 예외를 소유하고 중립 registry는 그 경로를
참조한다. 역할 Markdown 파일은 이 표를 소비하며 검증받는 소비자이고, 중립
등급 상한의 제약을 받는다. 경로가 바뀌면 영향받는 참조를 함께 고친다. 정적
일치는 model 접근, 역할 발견, 권한 강제를 증명하지 않는다. 생성기는 쓰지
않는다.

## Structure

- `agents/`: 공통 파일을 명시적으로 읽는 native 역할 정의.
- `bindings.json`: 검증되는 역할 projection이 소비하는 Claude model, effort,
  skill, 권한의 정규 값.
- `CLAUDE.md`: 명시적으로 읽는 provider baseline.
- [provider.md](provider.md): provider별 적재·지원 계약.
- `settings.json`: 현재 권한(allow, ask, deny), 등록된 사전 동작 hook, native 자동
  memory 비활성화(`autoMemoryEnabled: false`).
- `hooks/k8s-pre-edit.sh`: shell과 구조화 파일 도구에 대한 동기식 쓰기
  경계의 Claude adapter. 자기 provider 이름을 붙여 payload를 넘길 뿐이고,
  경계 자체는 `scripts/provider_write_guard.py`가 소유한다. provider마다 자기
  adapter를 등록하므로 두 provider가 함께 의존하는 통제를 한 provider
  디렉터리가 소유하지 않는다.
- `skills/<id>`: 공통 skill package마다 상대 링크 하나.
- `commands/<id>.md`: 공통 prompt 계약마다 진입점 하나. 각 진입점은 자기
  식별자로 `scripts/prompt-input.py`를 호출할 뿐 자체 계약을 갖지 않으며,
  입력, 출력, 거절 조건은 `.agents/prompts/`가 유지한다.

## Usage

[provider baseline](CLAUDE.md)을 읽은 뒤 선택한 공통 역할과 그 역할에 필요한
절차를 읽는다. 공통 skill은 명시적으로만 호출하며 추가 도구나 승인을 주지
않는다. 절차는 `.agents/skills/`에서 한 번만 고친다. 개인 로컬 설정과 memory는
공통 정책이 아니며, 재사용할 맥락은 공유 workspace memory store에 둔다.

## Verification

`python3 scripts/validate-agent-governance.py --root .`는 registry,
binding 표 문법, 정확한 역할·skill 참조, 링크 경계, 중립 상한 권한 일치를
검사한다. affected와 staged gate는 현재 validation registry에서 실제 입력에
맞게 고른다. 퇴역한 full/ci sweep은 완료 명령이 아니다. 실제 native 적재,
호출, hook 이벤트는 승인된 새 세션에서 따로 근거를 얻어야 한다.

## Related Documents

- [Common work lifecycle](../.agents/workflows/work-lifecycle.md)
- [Approval and safety](../.agents/governance/approval-and-safety.md)
- [Quality](../.agents/governance/quality.md)
- [Model selection](../.agents/governance/model-selection.md)
