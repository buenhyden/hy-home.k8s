# evals

## Overview

`evals/`는 Agent 평가 하니스(evaluation harness)가 놓일 자리다. 저장소의 역할
정의는 [`.agents/registry.json`](../.agents/README.md)이 소유하지만, 그 역할이
실제로 기대한 품질로 동작하는지는 별도의 평가 증적이 있어야 확인할 수 있다.
이 폴더가 그 증적의 소유 경로다.

현재 이 폴더에는 이 README 외에 추적되는 파일이 없다. 하니스는 아직 구현되지
않았고, 이 문서는 경계를 먼저 고정해 다른 영역이 평가 자산을 흡수하지 않도록
한다.

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

하니스가 추가되면 평가 케이스, 실행기, 결과 스키마를 이 표에 등록한다.

## Configuration Boundary

- 이 폴더는 평가 자산만 소유한다. 역할 정의를 여기에 복제하지 않는다.
- 평가 결과는 저장소에 남기는 증적이므로 재현 가능한 입력과 함께 기록한다.
  재현 불가능한 일회성 출력은 `_workspace/`에 둔다.
- 비밀값, 자격 증명, 개인 식별 정보를 평가 입력에 포함하지 않는다.
- 하니스를 추가할 때는 `scripts/validation/registry.json`의 `evals` surface에
  필요한 검증기를 함께 등록한다.

## Validation

| 검증기 | 확인 대상 |
| --- | --- |
| `repository-quality` | 저장소 전역 품질 규칙 |

실행: `bash scripts/validate-repo-quality-gates.sh .`

평가 하니스가 생기기 전까지 이 폴더의 PASS는 문서 정합성만을 뜻한다. 어떤
Agent 품질도 주장하지 않는다.

## Operations

- 평가 케이스를 추가하기 전에 어떤 역할의 어떤 책임을 측정하는지 먼저 적는다.
  측정 대상이 없는 케이스는 추가하지 않는다.
- 평가 결과를 근거로 역할 정의를 바꿀 때는 `.agents/`와 두 공급자 투영을 함께
  갱신한다.
- 하니스 도입은 surface 등록과 검증기 선택을 포함하므로 한 변경에서 함께 처리한다.

## Related Documents

- [Agent Registry](../.agents/README.md)
- [Roles](../docs/00.agent-governance/roles/README.md)
- [Quality Policy](../docs/00.agent-governance/policies/quality.md)
- [Model Selection Policy](../docs/00.agent-governance/policies/model-selection.md)
- [Tests](../tests/README.md)
