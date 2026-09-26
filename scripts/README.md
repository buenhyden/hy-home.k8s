---
title: "scripts"
version: "0.4.0"
type: "common/readme-implementation"
status: "active"
owner: "platform"
updated: "2026-09-26"
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
- affected·staged·all-files routing과 제한된 subprocess 실행
- GitOps, Kubernetes, Vault/ESO, GitHub Actions, CI Python 검사
- 아직 더 좁은 전용 owner가 없는 저장소 전체 계약

#### Out of Scope

- hosted CI, branch protection, provider runtime, credential, 배포, live cluster 증거
- test fixture, 합성 mutation, 고정된 negative case inventory
- branch tip, 현재 문서, 현재 스크립트, 줄 번호, corpus 개수를 고정하는 pin
- Stage 00, SDLC stage, Operations에서 옮겨 온 정책 문장

## Structure

### Routing and orchestration

| 경로 | 책임 |
| --- | --- |
| `validation/registry.json`과 그 schema | validator, surface, lane, 인자, fallback, CI routing 계약 |
| `select-affected-surfaces.py` | 경로를 surface로 고르는 순수 선택 projection |
| `githooks/chained-hook.sh`와 그 `pre-commit`, `commit-msg`, `pre-push` 링크 | 사용자의 전역 Git hook을 먼저 실행한 뒤 이 workspace의 hook을 실행하고, 처음 나온 0이 아닌 상태를 반환 |
| `validate-affected-surfaces.py` | registry와 추적 경로 coverage 검증 |
| `run-validation-lane.py` | affected, staged, all-files lane의 제한된 실행과 결과 정규화 |
| `qa.py` | 지원되는 QA 진입점. profile의 gate ID를 registry에서 해석해, 격리된 최종 트리나 정확한 index 스냅샷에서 실행한다. validator argv나 규칙 구현은 담지 않는다. |
| `validation/` 규칙 module | 전용 validator가 아직 소유하지 않은 저장소 전체 규칙(repository/quality.py)과, 현재 실행 대상과 Git 우선 역사 복구의 구분(current_executable_references.py) |

### Document and archive owners

| 경로 묶음 | 책임 |
| --- | --- |
| `document_contracts.py`, `validate-document-contract-registry.py`, `validate-markdown-profiles.py` | route·profile 분류와 작성된 Markdown의 의미 검증 |
| `document_authority.py`, `validate-links-and-owners.py` | 현재 owner와 문서 간 관계의 의미 검증 |
| `document_lifecycle.py`, `validate-document-lifecycle.py` | registry가 분류한 lifecycle과 staged index 전이 |
| `archive_recovery.py`, `archive_validation.py`, `archive_cutover.py`, `archive_cutover_manifest.py` | 제한된 역사 복구와 봉인된 Archive 검사 |
| `json_schema_validation.py` | production validator가 함께 쓰는 오프라인 JSON Schema 로딩 |
| `run-archive-contract-tests.py` | Stage 98 archive 계약 회귀 테스트를 quick·staged gate 하나로 실행한다. full에서는 `unit-tests`가 이를 포함한다(`coveredBy`). |

### Agent governance owners

| 경로 | 책임 |
| --- | --- |
| `agent_registry_loader.py` | governance 검증이 함께 쓰는 제한된 Stage 00 role registry 로딩 |
| `validate-agent-governance.py` | role·schema, native metadata, 권한, skill, 소비자 무결성 |
| `agent_governance_consumers.py` | 제한된 현재 소비자 검사와 Git 기반 역사 복구 검사 |
| `run-agent-evaluations.py` | 기록된 agent 응답을 registry에서 도출한 기준으로 채점 |

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

## Configuration Boundary

- 문서 route·profile 값은 `docs/99.templates/registry.json`에서만 온다.
- Agent role, 권한, skill, handoff, projection은
  `.agents/roles/registry.json`에서만 온다.
- 검증 선택과 명령 인자는 `scripts/validation/registry.json`에서만 온다.
- `.github/workflows/ci.yml`과 `.pre-commit-config.yaml`은 projection이며
  선언되지 않은 validator나 중복된 규칙 owner를 들여오면 안 된다.
- Claude 쓰기 경계 강제는 `.claude/hooks/`에 있고 provider 설정은 native
  event를 등록한다. 품질 검증은 명시적으로 실행하는 QA 작업이다.
- 테스트와 제한된 합성 데이터는 `tests/`와 `tests/fixtures/`에 둔다.
- 기본 복구 출처는 Git history다. digest는 외부에서 바뀌지 않는 의존성
  identity나 봉인된 역사 복구 좌표가 있을 때만 쓴다.

Python validator의 모든 subprocess 호출은 유한한 timeout을 쓴다. 텍스트
입력은 명시적으로 UTF-8로 읽고 소유 계약이 요구하는 곳에서는 symlink나
일반 파일이 아닌 경계를 닫힌 쪽으로 실패시킨다. 진단 메시지에는 secret 값을
담지 않는다.

## Validation

가장 작은 owner부터 실행하고 이어서 현재 작업에 필요한 affected·staged lane을
실행한다. 로컬 커밋마다 정확한 index 기준의 staged QA가 필요하며 full은 공통
품질 정책에 따라 최종 handoff 전에 실행한다.

```bash
python3 -m unittest tests.test_validation_tooling_ownership
python3 scripts/validate-affected-surfaces.py --root .
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-agent-governance.py --root .
python3 scripts/qa.py full
git diff --check
```

QA는 추적 경로와, 해당하는 ignore되지 않은 미추적 경로를 직접 고른다. 숨김
경로, 삭제, 이름 변경도 포함한다. 작업 트리 변경에는 `qa.py quick`을, 정확한
index에는 `qa.py staged`를 쓴다. 하위 runner는 진단용 인터페이스이며 QA의
스냅샷 격리를 대신하지 않는다. runner에 넘기는 명시적 경로 파일은 크기가
제한되고 NUL로 구분되어야 한다.

### Reproducing the hosted dependency identity

validator는 자신을 호출한 interpreter에서 실행된다. 그래서 CI와 다른 library
버전을 가진 머신에서는 CI가 실패하는 gate가 통과할 수 있고 그 차이는 hosted
실행이 보고하기 전까지 보이지 않는다. hosted identity는 여기에 버전 목록을
적어 두는 방식이 아니라, CI가 설치하는 것과 같은 lock을 설치해서 재현한다.

```bash
# Choose a task-owned environment outside the checkout being validated,
# under account-owned directories with no group/other write permission.
python3 -m venv "$VALIDATION_VENV"
"$VALIDATION_VENV/bin/python" -m pip install --disable-pip-version-check \
  --only-binary :all: --require-hashes \
  --requirement .github/requirements/ci-validation.txt
"$VALIDATION_VENV/bin/python" scripts/qa.py full
```

먼저 `VALIDATION_VENV`를 승인된 환경 경로로 설정한다. Python gate에는 호출한
Python이 그대로 쓰인다. 다른 도구는 고정된 시스템 경로를 쓰며 pre-commit은
신뢰할 수 있는 interpreter 인접 경로나 계정 소유의 정확한 fallback도 허용한다.
저장소 로컬 venv나 namespace가 매핑된 상위 디렉터리 소유권 때문에 그 fallback이
달라질 수 있으므로, venv 활성화 여부가 아니라 실제로 해석된 실행 파일을
기록한다. shell validator의 `python3`는 닫힌 시스템 PATH를 따르므로 그 library
identity도 따로 관찰해야 한다. HOME은 닫힌 상태로 두고 리뷰를 거친
pre-commit·Go·Rust·Node cache는 계정 소유의 cache 디렉터리 아래에 둔다.

gate가 로컬에서는 통과하고 hosted에서 실패할 때, 또는 잠긴 의존성이 소유하는
module을 바꾸기 전에 이 방법을 쓴다. 일반 로컬 실행보다 가까운 증거지만 여전히
로컬 증거이며 hosted runner에 대해서는 아무것도 증명하지 않는다.

formatter는 직접 호출하지 말고 `pre-commit`으로 실행한다. hook 설정은 일부러
`ruff-format`을 Python으로만 좁혀 둔다. 그냥 명령을 실행하면 Markdown까지
대상으로 삼아, 작성된 문서와 보관된 문서 안의 fenced snippet을 다시 쓴다.
shfmt와 공백 수정도 리뷰를 거친 소스 경로에 대해 명시적으로 `--files`로 실행하는
작업이다. full·ci는 manual stage를 격리된 스냅샷에서 한 번 실행하며 formatter가
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

## Operations

### Working Procedure

1. `validation/registry.json`에서 규칙과 그 전용 의미 owner를 찾는다.
2. 동작을 바꾸기 전에 독립적인 top-level 테스트를 추가하거나 고친다.
3. production 데이터는 production owner 옆에 두고 합성 데이터는 독립적인
   테스트 소비자와 함께 `tests/fixtures/` 아래에 둔다.
4. validator는 routing owner 한 곳에 추가하고 선언된 lane이 요구하는 곳에만
   hook·CI로 projection한다.
5. wrapper는 현재 소비자 0개와 고유 진단 0개를 증거로 확인한 뒤에만 없앤다.
   복구는 redirect가 아니라 Git으로 한다.
6. 커밋 전에 `git diff --check`, 관련 전용 테스트, affected·staged 선택,
   전체 결과를 검토한다.

없어진 구현 형태를 지키려는 목적만으로 호환 CLI, 중복 registry, 고정된 스크립트
inventory, 내장 mutation suite를 만들지 않는다. 확인된 필수 외부 CI check
이름은 `ci-summary`이며 로컬 workflow를 바꿀 때도 그 이름을 유지한다. 원격
branch protection 설정은 바꾸지 않는다.

## Related Documents

- [Agent execution policy](../.agents/governance/agent-execution.md)
- [Quality policy](../.agents/governance/quality.md)
- [Document authoring policy](../.agents/governance/document-authoring.md)
- Validation ownership ADR (`docs/02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md`)

위의 승인된 결정이 검증 책임의 현재 owner다. 그 결정을 처음 실행한 완료 Spec과
Task는 봉인된 증거이며 archive index로 계속 찾아갈 수 있다. 그 문서들은 한 번
실행한 일을 기록할 뿐, 지금 유효한 규칙을 다시 선언하는 문서가 아니다.
- [Tests](../tests/README.md)
