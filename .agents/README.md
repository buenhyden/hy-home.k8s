---
title: "Common Agent Governance"
version: "2.4.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-13"
---

# Common Agent Governance

## Overview

이 디렉터리는 이 GitOps 작업 공간의 공통 정책, 역할, skill에 대한 유일한
권한 원본이다. 파일은 명시적인 gateway나 native skill loader를 통해 읽히며,
디렉터리 전체가 자동으로 지침으로 적재되지는 않는다.

## Scope

provider별 차이와 native adapter는 [.claude/](../.claude/)와
[.codex/](../.codex/)에 있다. 공통 역할, 권한 등급, skill, 인계의 의미는
여기서 고치고, 구체적인 model, effort, native 권한 매핑은 각 provider의
`bindings.json`이 소유한다. 검증되는 역할 projection은 그 값을 소비할 뿐이며,
공통 registry나 생성기가 native 값의 두 번째 소유자가 되지 않는다.
[Governance](governance/)와 prompt 계약이 `knowledge/`와 `prompts/`를
소유한다. 각각 Stage 99 profile, affected-surface 범위, 이름 있는 소비자를
하나 이상 갖춰 도입되므로 읽는 쪽이 없는 디렉터리는 만들지 않는다.
[Evaluations](evaluations/README.md)는 같은 작업을 skill 없이와 skill을 써서
실제로 짝지어 실행한 근거, 즉 원시 관측, 작업 맥락, 기준, 점수, 집계 결과로
안내한다. 평가는 agent evaluator가, 문서 양식은 Stage 99가 소유한다. 이것은
근거 영역이지 상시 합성 채점기나 저장소 QA 관문이 아니다.
gate 선택은 여전히 `scripts/validation/registry.json`이, 공용 검증 helper는
`scripts/`가 소유한다. rule 디렉터리는 `governance/`와 중복되므로 두지 않고,
쓰이지 않는 script나 rule 뼈대도 도입하지 않는다. MIG-0009의 memory 퇴역은
여전히 유효하다.

## Structure

| Path | Purpose |
| --- | --- |
| [governance/](governance/) | 규범 lifecycle과 용어(sdlc.md), 승인·안전·품질·Git·문서·맥락·model 정책 |
| [roles/](roles/) | 책임 선택과 공통 인계 계약. `roles/registry.json`이 역할 ID, 중립 권한, skill 참조, native binding 경로를 담는다 |
| `skills/<id>/` | 호출 가능한 공통 절차 package. 구성은 registry가 정한다 |
| `workflows/` | 명시적으로 읽는 일반 lifecycle·위임 절차 |
| `knowledge/` | 정규 소유자를 가리키는 수동 관리 포인터. 자체 정책은 없다 |
| `prompts/` | 반복 작성 요청의 입력·출력 계약 |
| [evaluations/](evaluations/) | 관측된 짝 실행 agent 평가 근거의 라우터. 역할, skill, QA 관문 권한은 없다 |

### Skill package

package는 `SKILL.md`와 두 provider가 함께 읽는 `agents/` sidecar를 담는다.
절차에 필요할 때만 디렉터리 세 개를 더 둘 수 있다. 단계가 다시 서술하지 않고
가리키는 Markdown은 `references/`, 단계가 실행하는 helper는 `scripts/`, 출력을
만드는 데 쓰는 파일은 `assets/`에 둔다. 어디에 둘지는 자료의 성격으로
판단한다. 단계는 `SKILL.md`에 두고, 나머지는 읽는 사람이 건너뛸 수 있는 곳에
둔다.

package는 닫힌 집합으로 유지한다. 모든 자원은 `SKILL.md`에서 직접 또는 다른
package 자원을 거쳐 도달할 수 있어야 한다. 범위가 정해진 탐색은 중첩
디렉터리를 허용하고 순환을 끊으며, 빈 디렉터리, 고아 파일, symlink, 일반
파일이 아닌 것을 거부한다. reference는 Markdown, script는 Python 또는 shell,
asset은 출력 전용 자원이다.

QA gate 선택은 `scripts/validation/registry.json`만 한다. registry는 등록된
skill의 `scripts/` 아래 검사기를 선택할 수 있지만, 검사기를 가지고 있다는
사실만으로 등록되거나 실행 권한을 얻지는 않는다. 전용 asset에는
`*.template.md` 출력 양식이 포함될 수 있다. 공용 문서 profile과 template의
권한은 여전히 Stage 99에 있으며 package asset이 이를 대신할 수 없다.

## Usage

작업 전에 [work lifecycle](workflows/work-lifecycle.md),
[agent execution](governance/agent-execution.md), `governance/`의 승인·안전
정책을 읽는다. [roles](roles/README.md)에서 책임을 고른 뒤 선택한 역할과 그
역할이 요구하는 skill을 명시적으로 읽는다. 두 provider는 같은 공통 skill
package를 명시 호출용으로 노출한다. skill은 쓰기, 전송, 배포, secret 열람
권한을 주지 않는다. 근거의 의미는 `governance/`의 quality 정책이, 바뀌는 gate
명령과 한도는 실행 registry가 소유한다.

## Verification

역할, skill, 권한, native binding, routing 계약이 선택되면
`python3 scripts/validate-agent-governance.py --root .`를 실행한다. 이것은
schema·projection·중립 상한에 대한 정적 근거이며 native 강제의 근거가 아니다.
실제 변경 범위에는 로컬 affected와 exact-index profile을 쓴다. 공용 QA
machinery를 바꾸거나 범위가 명시된 감사를 할 때는 자원 사전 점검 뒤 등록된
목적 gate와 이름 있는 동작·Archive·보안 회귀를 고른다. 퇴역한 full/ci
sweep은 완료 명령이 아니다. 역할 projection 생성기는 쓰지 않는다. native
발견, 호출, 권한, hook 전달은 새 세션에서 따로 근거를 얻어야 한다.

## Related Documents

- Document profiles and templates (`docs/99.templates/README.md`)
- [Repository documentation](../docs/README.md)
- Memory retirement: MIG-0009 through the archive index (`docs/98.archive/README.md`)
- [Governance contracts](governance/)
