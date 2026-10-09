---
title: "scripts"
version: "0.7.3"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-09"
---
# scripts

## Overview

`scripts/`는 저장소의 문서, Agent governance, GitOps, CI, 보안 경계를
repository-static 방식으로 검증하는 실행 코드의 소유 경로다. 사람에게 보이는
규칙은 각 canonical 문서가 소유하고, 이 폴더는 그 규칙의 machine enforcement와
검증 routing만 구현한다.

검증 선택과 command mapping의 단일 machine owner는
`validation/registry.json`이다. 개별 validator는 자기 진단 의미를 소유하며,
`qa.py`와 `run-validation-lane.py`는 선택된 owner를
호출하고 결과를 정규화한다. production module은 top-level `tests/`를 import하거나
`tests/fixtures/`를 runtime input으로 읽지 않는다.

### Audience

- Platform maintainers
- Quality engineers
- Documentation maintainers
- AI agents

### Scope

#### In Scope

- 문서 profile, lifecycle, link, owner, archive 검증
- Agent registry, provider projection, loop, CI 계약 검증
- 선택된 affected·staged routing과 목적별 제한된 subprocess 실행
- GitOps, Kubernetes, Vault/ESO, GitHub Actions, CI Python 검사
- 아직 더 좁은 전용 owner가 없는 저장소 전체 계약

#### Out of Scope

- hosted CI, branch protection, provider runtime, credential, 배포, live cluster 증거
- test fixture, 합성 mutation, 고정된 negative case inventory
- branch tip, 현재 문서, 현재 스크립트, 줄 번호, corpus 개수를 고정하는 pin
- Stage 00, SDLC stage, Operations에서 옮겨 온 정책 문장

## Scope

- 문서 route·profile 값은 [Stage 99 계약](../docs/99.templates/README.md)에서만 온다.
- Agent role, 권한, skill, handoff, projection은
  `.agents/roles/registry.json`에서만 온다.
- 검증 선택과 명령 인자는 `scripts/validation/registry.json`에서만 온다.
- `.github/workflows/ci.yml`과 `.pre-commit-config.yaml`은 projection이며
  선언되지 않은 validator나 중복된 규칙 owner를 들여오면 안 된다.
- 구조화 쓰기 경로 검사는 `provider_write_guard.py`가 소유하고 각 provider
  adapter가 native event를 등록한다. shell 관찰은 advisory이며, 실제 전달과
  native 강제는 [승인 정책](../.agents/governance/approval-and-safety.md)과
  provider note의 관측 경계를 따른다. 품질 검증은 명시적으로 실행하는 QA 작업이다.
- 테스트와 제한된 합성 데이터는 `tests/`와 `tests/fixtures/`에 둔다.
- 기본 복구 출처는 Git history다. digest는 외부에서 바뀌지 않는 의존성
  identity나 봉인된 역사 복구 좌표가 있을 때만 쓴다.

Python validator의 모든 subprocess 호출은 유한한 timeout을 쓴다. 텍스트
입력은 명시적으로 UTF-8로 읽고 소유 계약이 요구하는 곳에서는 symlink나
일반 파일이 아닌 경계를 닫힌 쪽으로 실패시킨다. 진단 메시지에는 secret 값을
담지 않는다.

## Structure

### Routing and orchestration

| Path | Purpose |
| --- | --- |
| `validation/registry.json`과 그 schema | validator, surface, lane, 인자, fallback 계약 |
| `select-affected-surfaces.py` | 경로를 surface로 고르는 순수 선택 projection |
| `githooks/chained-hook.sh`와 그 `pre-commit`, `commit-msg`, `pre-push` 링크 | 사용자의 전역 Git hook을 먼저 실행한 뒤 이 workspace의 hook을 실행하고, 처음 나온 0이 아닌 상태를 반환 |
| `validate-affected-surfaces.py` | registry와 추적 경로 coverage 검증 |
| `run-validation-lane.py` | 현재 v4 소스의 affected·staged 선택 입력을 제한해 실행하고 결과를 정규화한다. 선택된 변경 경로를 문서 reader에 전달하며, 인자 수나 크기 한계를 넘으면 reader의 전체 검사를 사용한다. 구형 all-files 집계 경로 제거의 검증·수용 상태는 [Stage 03 Spec navigation](../docs/03.specs/README.md)에서 찾는 SPEC-0107 Task가 기록한다. |
| `qa.py` | 지원되는 QA 진입점. profile의 gate ID를 registry에서 해석해, 격리된 작업 트리나 정확한 index 스냅샷에서 실행한다. 한 실행에서 캡처한 스냅샷 트리를 gate 입력 identity에도 재사용한다. validator argv나 규칙 구현은 담지 않는다. |
| `validation/` 규칙 module | 전용 validator가 아직 소유하지 않은 저장소 전체 규칙(repository/quality.py)과, 현재 실행 대상과 Git 우선 역사 복구의 구분(current_executable_references.py) |

### Document and archive owners

| 경로 묶음 | 책임 |
| --- | --- |
| `document_contracts.py`, `validate-document-contract-registry.py`, `validate-markdown-profiles.py` | route·profile 분류와 작성된 Markdown의 의미 검증. affected·staged의 변경 경로가 본문 검사 대상을 정하며, 현재 문서의 metadata·identity 검사와 English-only 파일 검사는 유지한다. 생산자·reader helper 변경은 Registry의 문서 검사 owner로 연결한다. |
| `document_authority.py`, `validate-links-and-owners.py` | 현재 owner와 문서 간 관계의 의미 검증. 링크 검사 한 실행의 context가 Registry와 문서 inventory를 보유해 같은 입력의 재조회에 쓰인다. |
| `document_lifecycle.py`, `validate-document-lifecycle.py` | registry가 분류한 lifecycle과 staged index 전이 |
| `validate-archive-integrity.py`, `archive_recovery.py`, `archive_validation.py` | 현재 Archive 보관 무결성·catalog·Git 복구 검사. `archive_recovery.py`의 공용 MIG-0001 reader가 현재 원장 bytes의 고정 digest와 canonical 형식을 확인하며, Archive·link 소비자가 그 결과를 읽는다. 필요할 때 역사 envelope은 bounded Git reader로 복구한다. 과거 cutover 완료 증명은 원래 Task/Archive 증거에 남긴다. |
| `json_schema_validation.py` | production validator가 함께 쓰는 오프라인 JSON Schema 로딩 |
| `run-archive-contract-tests.py` | Stage 98 Archive 계약 회귀를 해당 입력의 quick·staged 또는 명시적으로 선택된 목적 gate에서 실행한다. 긴 blanket unit discovery의 간접 `coveredBy`를 현재 완료 조건으로 삼지 않는다. |

현재 MIG-0001 원장이 없거나 그 bytes가 바뀌면 Archive 검사는 실패한다.
고정 digest는 현재 원장 identity를, canonical parser와 현재 record 검사는
형식·source/blob/provenance를, 필요할 때 실행하는 Git reader는 역사
envelope 복구를 맡는다. 승인된 현재 경로에서는 과거 93행을 Git에서 매번
재생성하는 builder/checker와 과거 완료 census만 지키던 namespace guard,
전용 manifest·테스트를 제거했다. 현재 원장의 누락·변조, record source와
provenance 오류, alias·링크 오류는 각각의 현재 owner가 계속 거부한다.
원장 digest나 AST 소비자 조사는 과거 모든 Git object의 존재 또는 보관
단위의 처분 승인을 증명하지 않는다. 실제 전체 단위 처분은
[Archive Retention Assessment](../docs/98.archive/README.md)가
별도로 소유한다.

### Agent governance owners

| 경로 | 책임 |
| --- | --- |
| `agent_registry_loader.py` | governance 검증이 함께 쓰는 제한된 common role registry 로딩 |
| `validate-agent-governance.py` | role·schema, native metadata, 권한, skill, 소비자 무결성 |
| `agent_governance_consumers.py` | 제한된 현재 소비자 검사와 Git 기반 역사 복구 검사 |

### Platform and supply-chain owners

| 경로 | 책임 |
| --- | --- |
| `validate-gitops-change-set.py`, `validate-gitops-structure.sh` | GitOps identity와 구조 검증 |
| `validate-k8s-manifests.sh`, `validate-policy-gates.sh` | manifest 문법과 저장소 정책 검사 |
| `validate-infrastructure-contracts.sh` | 저장소 정적 infrastructure 계약 검사. live cluster 검사는 `infrastructure/verify/`에 있다. |
| `validate-vault-eso-contracts.py`, `check-secret-handling.sh` | Vault·ESO 참조 계약과, 값을 가린 secret 패턴 검사 |
| `validate-github-actions-security.py`, `validate-ci-python-contract.py` | workflow 공급망과 Python 의존성 계약 |
| `validate-workspace-boundary.py` | staged workspace 경계와 ignore 경로 계약 |
| `render-platform-chart-kinds.sh` | 운영자가 직접 실행하는 chart kind 리뷰 보조 도구 |

## Usage

### Working Procedure

1. `validation/registry.json`에서 규칙과 그 전용 의미 owner를 찾는다.
2. 동작을 바꾸기 전에 독립적인 top-level 테스트를 추가하거나 고친다.
3. production 데이터는 production owner 옆에 두고 합성 데이터는 독립적인
   테스트 소비자와 함께 `tests/fixtures/` 아래에 둔다.
4. validator는 routing owner 한 곳에 추가하고 선언된 lane이 요구하는 곳에만
   hook·CI로 projection한다.
5. 일회성 또는 오래된 검사는 지속 보장을 현재 owner로 이전하고 caller와
   등록을 제거한 뒤 전용 wrapper·fixture·test의 소비자 0개를 확인한다.
   필요한 과거 결과는 기존 Task/Archive 위치에 보존하고 복구는 Git으로 한다.
6. 커밋 전에 `git diff --check`, 관련 전용 테스트, affected·staged 선택,
   전체 결과를 검토한다.

없어진 구현 형태를 지키려는 목적만으로 호환 CLI, 중복 registry, 고정된 스크립트
inventory, 내장 mutation suite를 만들지 않는다. 호스팅 check 이름과 원격
branch protection의 활성 상태는 실제 원격에서 확인해야 하며, 저장소 파일만으로
required-check 성공이나 설정을 주장하지 않는다.

## Verification

가장 작은 owner부터 실행하고 현재 작업에 필요한 affected·staged lane을
선택한다. 로컬 커밋마다 정확한 index 기준의 staged QA가 필요하다. 이 public
저장소의 목적·단위 QA는 로컬에서 실행한다. GitHub Actions의 branch
metadata와 PR style 결과는 로컬 QA의 대체 증거가 아니다. global QA 계약을
바꾸거나 한정 감사를 수행해도 해당 목적 gate와 명명된 단위 회귀만 선택한다.
긴 full/ci 일괄 검사와 blanket unit discovery는 현재 완료 조건이 아니다.
나머지 선택과 인계는
[Quality policy](../.agents/governance/quality.md#delivery-ownership)가 소유한다.

```bash
git diff --check
```

나머지 검사는 변경 경로와 입력에 맞춰 현재 Registry와 Quality policy가
선택한 gate만 실행한다. 구현·validator 계약을 바꾼 경우에는 해당 동작의
focused 회귀를 추가로 선택한다.

현재 선택된 필수 목적 gate나 명명된 회귀를 실행하지 못했다면 `NOT_RUN`
또는 권한·환경 공백의 `DEFER`와 다음 owner를 기록한다. 퇴역한 full/ci와
blanket discovery의 과거 `NOT_RUN`·FAIL·PASS는 당시 입력의 역사로 보존한다.
`NOT_APPLICABLE`는 검사 대상이 없는 경우에만 사용한다. 호스팅 branch나
style 결과를 로컬 목적 QA PASS로 승격하지 않는다.

QA는 추적 경로와, 해당하는 ignore되지 않은 미추적 경로를 직접 고른다. 숨김
경로, 삭제, 이름 변경도 포함한다. 작업 트리 변경에는 `qa.py quick`을, 정확한
index에는 `qa.py staged`를 쓴다. 하위 runner는 진단용 인터페이스이며 QA의
스냅샷 격리를 대신하지 않는다. runner에 넘기는 명시적 경로 파일은 크기가
제한되고 NUL로 구분되어야 한다. 문서 reader의 `--change-scope`는 이 선택
입력이 있을 때만 쓰며, 명시적 전체 감사에서는 사용하지 않는다.

### Reproducing the local dependency identity

validator는 자신을 호출한 interpreter에서 실행된다. 다른 로컬 머신의
library 차이를 통제하려면 검토된 lock으로 task-owned 환경을 구성하고
실제로 선택된 interpreter와 도구 identity를 Task에 기록한다. lock의
존재만으로 검증 실행이나 hosted identity를 주장하지 않는다.

```bash
# Choose a task-owned environment outside the checkout being validated,
# under account-owned directories with no group/other write permission.
python3 -m venv "$VALIDATION_VENV"
"$VALIDATION_VENV/bin/python" -m pip install --disable-pip-version-check \
  --only-binary :all: --require-hashes \
  --requirement .github/requirements/ci-validation.txt
# After staging the reviewed logical input:
"$VALIDATION_VENV/bin/python" scripts/qa.py staged
```

먼저 `VALIDATION_VENV`를 승인된 환경 경로로 설정한다. Python gate에는 호출한
Python이 그대로 쓰인다. 다른 도구는 고정된 시스템 경로를 쓰며 pre-commit은
신뢰할 수 있는 interpreter 인접 경로나 계정 소유의 정확한 fallback도 허용한다.
저장소 로컬 venv나 namespace가 매핑된 상위 디렉터리 소유권 때문에 그 fallback이
달라질 수 있으므로, venv 활성화 여부가 아니라 실제로 해석된 실행 파일을
기록한다. shell validator의 `python3`는 닫힌 시스템 PATH를 따르므로 그 library
identity도 따로 관찰해야 한다. HOME은 닫힌 상태로 두고 리뷰를 거친
pre-commit·Go·Rust·Node cache는 계정 소유의 cache 디렉터리 아래에 둔다.

잠긴 의존성이 소유하는 module을 바꾸기 전이나 로컬 도구 재현성이 필요한
경우에 이 방법을 쓴다. 실제 실행 결과도 검증한 입력과 로컬 환경에만
적용된다.

formatter는 직접 호출하지 말고 `pre-commit`으로 실행한다. hook 설정은 일부러
`ruff-format`을 Python으로만 좁혀 둔다. 그냥 명령을 실행하면 Markdown까지
대상으로 삼아, 작성된 문서와 보관된 문서 안의 fenced snippet을 다시 쓴다.
shfmt와 공백 수정도 리뷰를 거친 소스 경로에 대해 명시적으로 `--files`로 실행하는
작업이다. 선택된 staged style은 격리된 정확한 index에서 실행하며 formatter가
무언가를 바꾸면 검증이 실패한다. commit-msg는 별도이며 실제 후보 메시지에는
공통 Git 정책을 따른다.

NUL로 구분된 명시적 변경 경로 집합에는 다음을 쓴다.

```bash
python3 scripts/run-validation-lane.py \
  --root . \
  --lane affected \
  --paths-file /tmp/hy-home-k8s-paths.nul \
  --delimiter nul
```

저장소 정적 PASS는 검사한 저장소 상태만 증명한다. hosted 실행, provider native
강제, credential, 원격 상태, 배포, live cluster 동작은 증명하지 않는다.

## Related Documents

- [Agent execution policy](../.agents/governance/agent-execution.md)
- [Quality policy](../.agents/governance/quality.md)
- [Document authoring policy](../.agents/governance/document-authoring.md)
- Validation ownership ADR (`docs/02.architecture/decisions/README.md`)

검증 책임의 현재 owner는 공통 Quality policy와 `scripts/validation/registry.json`이다.
과거 결정과 완료 기록은 문서·archive 탐색을 통해 확인하는 배경 증거이며,
현재 실행 절차의 선행 조건이 아니다.
- [Tests](../tests/README.md)
