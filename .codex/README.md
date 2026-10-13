---
title: "Codex Native Adapter"
version: "2.4.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-14"
---

# Codex Native Adapter

## Overview

공통 정책, 역할 의미, 절차는 [공통 권한 원본](../.agents/README.md)에 있다.
이 디렉터리는 Codex 문법, 지원 메모, native 연결만 소유한다.

## Scope

공통 계약은 [roles/registry.json](../.agents/roles/registry.json)과 선택한
정규 역할에서 고친다. [bindings.json](bindings.json)은 이 provider의 등급별
model, effort, native scope, 역할별 예외를 소유하고 중립 registry는 그 경로를
참조한다. 역할 TOML 파일은 이 표를 소비하며 검증받는 소비자이고, 중립 등급
상한의 제약을 받는다. 경로가 바뀌면 영향받는 참조를 함께 고친다. 정적 일치는
model 접근, 역할 발견, 권한 강제를 증명하지 않는다. 생성기는 쓰지 않는다.

## Structure

- `agents/`: 공통 파일을 명시적으로 읽는 native 역할 정의.
- `bindings.json`: 검증되는 역할 projection이 소비하는 Codex model, effort,
  skill, 권한의 정규 값.
- `CODEX.md`: 명시적으로 읽는 provider baseline.
- [provider.md](provider.md): provider별 적재·지원 계약.
- `hooks.json`: 사전 동작 guard 등록. Claude 쪽과 같은 validator 규칙
  family로 판정한다. 등록은 추적되는 설정일 뿐이며, 설치된 client가 hook을
  발견·적재·전달했다는 근거가 아니다.
- `hooks/pre-tool-use.sh`: 공유 쓰기 경계의 Codex adapter. 자기 provider
  이름을 붙여 payload를 넘길 뿐이고, 경계 자체는
  `scripts/provider_write_guard.py`가 소유한다. 이 디렉터리에는 공유 logic이
  없다.
- 프로젝트 `commands/`나 `prompts/` 디렉터리는 채택하지 않는다. 중립
  `.agents/prompts/` 계약은 명시적으로 읽고 `scripts/prompt-input.py`가
  소비한다. Claude는 이를 native command로도 투영하지만 그것은 Claude의 편의
  기능이지 공유 정책이 아니므로, 여기에 없는 것은 누락이 아니라 선언된
  차이다.
- `config.toml`: native memory를 끄는 `[memories]` 표와, 승인 정책, sandbox,
  workspace network, 비밀 환경변수 필터(`[shell_environment_policy]`)를 담는다.
  validator가 정확히 이 값만 허용하고 다른 key나 표(특히 `[hooks]`)를 거부한다.
  hook 등록은 계속 `hooks.json` 한 파일이 소유한다. Codex는 신뢰된
  프로젝트에서만 프로젝트 설정을 적용한다.
- `rules/default.rules`: 비밀 출력, cluster 변경, 삭제·이력 파괴 명령을 argv
  prefix로 금지하는 execpolicy 규칙. validator가 digest로 고정한다.
- 프로젝트 `skills/`는 채택하지 않는다. Codex 프로젝트 skill은
  client가 문서화한 프로젝트 skill root인 `.agents/skills/`에 있다. 각 능력
  주장이 어떤 client 판본에서 관측되었는지는 [provider.md](provider.md)를 본다.

## Usage

[provider baseline](CODEX.md)을 읽은 뒤 선택한 공통 역할과 그 역할에 필요한
절차를 읽는다. 공통 skill은 명시적으로만 호출하며 추가 도구나 승인을 주지
않는다. 절차는 `.agents/skills/`에서 한 번만 고친다. 개인 로컬 설정과 memory는
공통 정책이 아니며, 재사용할 맥락은 공유 workspace memory store에 둔다.

## Verification

`python3 scripts/validate-agent-governance.py --root .`는 registry, native
문법, 정확한 역할·skill 참조, 링크 경계, 권한 일치를 검사한다. 선택된
affected, staged, 이름 있는 목적 검사가 각자 선언한 입력을 다룬다. 퇴역한
`full`/`ci` sweep과 일괄 unit discovery는 로컬 완료 조건이 아니다. 실제 native
적재, 호출, hook 이벤트는 새 세션과 해당 승인이 필요한 별도 검사다.

## Related Documents

- [Common work lifecycle](../.agents/workflows/work-lifecycle.md)
- [Approval and safety](../.agents/governance/approval-and-safety.md)
- [Quality](../.agents/governance/quality.md)
- [Model selection](../.agents/governance/model-selection.md)
