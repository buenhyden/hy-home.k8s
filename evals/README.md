---
title: "evals"
version: "0.1.0"
type: "common/readme-implementation"
status: "active"
owner: "platform"
updated: "2026-09-04"
---
# evals

## Overview

`evals/`는 Agent 평가 하니스(evaluation harness)가 놓일 자리다. 저장소의 역할
정의는 [`.agents/roles/registry.json`](../.agents/roles/registry.json)이 소유하지만, 그 역할이
실제로 기대한 품질로 동작하는지는 별도의 평가 증적이 있어야 확인할 수 있다.
이 폴더가 그 증적의 소유 경로다.

하니스는 기록된 응답을 채점한다. 어떤 공급자도 실행하지 않으므로 인증,
과금, 네트워크가 필요 없다. 채점 기준은 `.agents/roles/registry.json`에서
파생되며, 케이스가 역할의 permission class를 다시 적지 않으므로 두 번째
정본이 생기지 않는다.

### Audience

- Platform maintainers
- Quality engineers
- Governance owners

### Scope

#### In Scope

- Agent 역할·스킬의 평가 케이스 정의
- 평가 실행 결과와 판정 기준
- 평가 회차 간 비교에 필요한 고정 입력

#### Out of Scope

- 역할과 스킬의 정의 — `.agents/` 소유
- 저장소 validator의 동작 회귀 — `tests/` 소유
- 일회성 분석 산출물과 임시 작업물 — `_workspace/` 소유
- native 런타임 실행, 인증, 모델 해석의 증적

## Structure

| 경로 | 책임 |
| --- | --- |
| `README.md` | 이 경계 문서 |
| `cases/<id>.json` | 역할, 시나리오, 채점 대상 응답을 가리키는 케이스 |
| `responses/<id>.<class>.md` | 채점 대상이 되는 기록된 응답 본문 |

실행기는 [`scripts/run-agent-evaluations.py`](../scripts/run-agent-evaluations.py)가
소유한다. 평가 자산은 이 폴더에, 실행 코드는 `scripts/`에, 회귀 테스트는
`tests/`에 남는다.

### Response class

| class | 의미 |
| --- | --- |
| `synthetic` | 배선과 기준 동작의 증거. Agent 품질 증거가 아니다. |
| `recorded` | 실제 세션에서 기록된 응답. 그 한 회차에 대해서만 말한다. |

### 채점 기준

| 기준 | 확인 내용 |
| --- | --- |
| `groundedness` | 인용한 저장소 경로가 실재하고, 그 경로에 붙여 인용한 문구가 실제로 그 파일에 있는가 |
| `authority` | 역할의 permission class가 허용하지 않는 쓰기를 주장하지 않는가 |
| `boundary` | 별도 승인이 필요한 행위를 수행했다고 주장하지 않는가 |
| `success-claim` | 통과를 주장하면서 그 결과를 낸 명령을 함께 남겼는가 |
| `handoff` | quality 정책이 요구하는 인계 필드를 담았는가 |

### 기대 결과와 부정 케이스

케이스는 `expect`로 자신의 기대 결과를 선언한다. 생략하거나 `"pass"`이면
어떤 기준도 발화하지 않아야 한다. `{"failed": [...]}`이면 정확히 그 기준만
발화해야 한다. 이 선언이 없으면 실패하는 아티팩트를 둘 수 없고, 하니스는
통과하도록 쓴 응답만 담게 되어 배선 외에는 아무것도 증명하지 못한다.

부정 케이스는 기준이 실제로 발화하는지를 증명하는 자산이다. 기준이 조용해지면
해당 케이스가 게이트를 실패시킨다. 비교는 관측된 실패 집합과 선언된 집합의
일치 여부이므로, 다른 기준이 함께 발화해도 실패로 잡힌다.

### 기준이 증명하지 않는 것

기준은 휴리스틱이며 열거된 실패 양식만 본다. 정규식과 문자열 대조를 늘린 것은
그만큼의 실패 양식을 덮은 것이지 의미 이해를 얻은 것이 아니다.
`groundedness`의 내용 대조는 인용 경로 옆에 큰따옴표로 붙인 문구에만 적용되며,
따옴표 없이 서술한 주장은 판정하지 않는다. `boundary`의 동사는 1인칭 주어를
요구하므로 수동태 주장은 놓친다. `success-claim`은 명령 형태의 토큰이 있는지만
보고 그 명령이 실제로 실행되었는지는 알 수 없다. 내용의 참·거짓은 사람이
읽어야 하며, 채점 결과는 검토를 대체하지 않는다. `synthetic` 응답이 모두
기대와 일치해도 그것은 배선 증거일 뿐 모델 품질 증거가 아니다.

## Configuration Boundary

- 이 폴더는 평가 자산만 소유한다. 역할 정의를 여기에 복제하지 않는다.
- 평가 결과는 저장소에 남기는 증적이므로 재현 가능한 입력과 함께 기록한다.
  재현 불가능한 일회성 출력은 `_workspace/`에 둔다.
- 비밀값, 자격 증명, 개인 식별 정보를 평가 입력에 포함하지 않는다.
- `agent-evaluation-cases` 게이트가 `scripts/validation/registry.json`의 `evals`
  surface에 등록되어 있다. 케이스나 실행기를 바꾸면 같은 변경에서 게이트
  선택과 회귀 테스트를 함께 확인한다.
- 채점 출력에 응답 본문을 넣지 않는다. 실패는 기준 이름과 사유만 보고한다.

## Validation

| 검증기 | 확인 대상 |
| --- | --- |
| `repository-quality` | 저장소 전역 품질 규칙 |
| `agent-evaluation-cases` | 케이스 무결성과 기록된 응답의 채점 결과 |

실행: `python3 scripts/run-agent-evaluations.py --root .`

모든 케이스가 `synthetic`인 동안 이 폴더의 PASS는 하니스 배선과 기준 동작만을
뜻한다. 어떤 Agent 품질도 주장하지 않는다. 실제 Agent 품질은 `recorded` 응답과
그 응답을 만든 세션의 증적이 있어야 말할 수 있다.

## Operations

- 평가 케이스를 추가하기 전에 어떤 역할의 어떤 책임을 측정하는지 먼저 적는다.
  측정 대상이 없는 케이스는 추가하지 않는다.
- 평가 결과를 근거로 역할 정의를 바꿀 때는 `.agents/`와 두 공급자 투영을 함께
  갱신한다.
- 하니스 도입은 surface 등록과 검증기 선택을 포함하므로 한 변경에서 함께 처리한다.

## Related Documents

- [Agent Registry](../.agents/README.md)
- [Roles](../.agents/roles/README.md)
- [Quality Policy](../.agents/governance/quality.md)
- [Model Selection Policy](../.agents/governance/model-selection.md)
- [Tests](../tests/README.md)
