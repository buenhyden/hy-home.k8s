---
title: "tests"
version: "0.3.0"
type: "common/readme-implementation"
status: "active"
owner: "platform"
updated: "2026-09-26"
---

# tests

## Overview

`tests/`는 저장소 검증 코드의 독립적인 동작 coverage와 합성 fixture를
소유한다. production validator는 현재 저장소 상태만 검사하고 mutation, 잘못된
입력, timeout, staged index 모호성, 소비자 0개, 실패 진단 같은 경우는 이 폴더의
테스트가 구성한다.

이 폴더의 PASS는 저장소 정적 증거다. hosted CI, provider runtime, credential,
배포, 원격 상태, live cluster 준비 상태를 주장하지 않는다.

### Audience

- Quality engineers
- Platform maintainers
- Validator authors
- AI agents

### Scope

#### In Scope

- production module의 공개 함수·CLI·진단 동작 회귀
- 임시 저장소와 합성 mutation을 쓰는 실패 경계 검증
- staged index와 작업 트리 권한의 구분
- fixture 소비자 소유권과 고아 fixture 방지
- hook, routing, 문서, archive, Agent, CI, GitOps 정적 계약

#### Out of Scope

- production runtime 데이터 API
- 고정된 test case 수나 fixture 수 정책
- secret, credential, kubeconfig, provider 토큰, live 진단 정보
- live cluster bootstrap, ArgoCD sync, Vault 변경, 원격 CI 재실행

## Structure

### Test families

| Family                           | Representative modules                                                                                                                                                                                                                                                                              |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Validation ownership and routing | `test_validation_tooling_ownership.py`, `test_affected_surface_migration.py`, `test_validate_affected_surfaces.py`, `test_run_validation_lane.py`, `test_current_executable_references.py`                                                                                                          |
| Document contracts and lifecycle | `test_document_strict_cutover.py`, `test_document_lifecycle_migration.py`, `test_document_lifecycle_cumulative_history.py`, `test_document_lifecycle_archive_cutover.py`, `test_document_lifecycle_agent_roster_cutover.py`, `test_reference_pack_routes.py`, `test_documentation_link_boundary.py` |
| Archive and recovery             | `test_archive_recovery.py`, `test_archive_validation.py`, `test_archive_cutover.py`, `test_archive_historical_proof.py`, `test_generic_migration_recovery.py`                                                                                                                                       |
| Agent governance                 | `test_agent_governance.py`, `test_agent_governance_consumers.py`, `test_validate_agent_registry.py`, `test_validate_agent_core_cutover.py`, `test_agent_evaluations.py`                                                                                    |
| CI, GitOps, Vault, and workspace | `test_validate_ci_python_contract.py`, `test_validate_github_actions_security.py`, `test_validate_gitops_change_set.py`, `test_validate_vault_eso_contracts.py`, `test_workspace_boundary.py`                                                                                                       |
| Hook boundaries                  | `test_k8s_pre_edit_hook.py`                                                                                                                                                                                                                                                                         |

### Shared helper modules

| Module | 책임 |
| --- | --- |
| `git_fixture.py` | archive와 lifecycle 회귀 테스트를 위해 임시 root에 정확한 Git 객체를 만든다 |
| `affected_surface_mutations.py` | affected surface 선택을 위한 routing mutation 사례 |
| `gitops_change_set_cases.py` | GitOps diff rendering을 위한 change set 사례 |
| `vault_eso_contract_cases.py` | Vault·ESO 계약과 보안 사례 |

helper module은 공유 입력이나 구성 코드만 담는다. helper를 쓰려고 test module을
import하면 그 module의 테스트가 다시 실행되므로, 둘 이상의 suite가 필요로 하는
helper는 이곳에 둔다.

### Fixture families

[fixtures/](./fixtures/)에는 GitHub Actions 보안, GitOps change set,
validation surface, Vault·ESO 계약 fixture가 있다. 각 fixture는 같은 주제의
validator 테스트가 사용한다.

fixture는 범위가 제한된 예시이며 production registry가 아니다. fixture는
독립적인 테스트가 사용하는 동안에만 남는다. 조합이 필요하면 보통 영구
매트릭스를 늘리지 말고 임시 디렉터리에서 생성한다.

## Configuration Boundary

- 테스트는 `scripts/`의 production module을 import할 수 있다. 반대 방향의
  의존은 금지한다.
- 테스트는 `tests/fixtures/`를 읽을 수 있지만 production module은 읽을 수 없다.
- 임시 Git 저장소와 디렉터리는 버려도 되는 것이어야 하며 credential이나 사용자
  데이터를 담지 않는다.
- 네트워크, provider 인증, hosted CI 변경, live cluster 접근은 기본 테스트
  경계 밖이다.
- 단언의 대상은 동작, 진단 ID, 의미상 소유권이다. 영구적인 파일 수, 줄 수, 현재
  SHA 값, mutation 수를 단언하지 않는다.
- 이 저장소가 등록된 validator를 통과하는지는 그 gate 자신의 결과다. 통과만
  단언하는 테스트는 같은 바이트에 같은 검사를 다른 이름으로 한 번 더 돌리는
  것이므로, 여기가 아니라 gate에 속한다. 실제 corpus를 읽는 테스트가 맞는 경우는
  gate가 하지 않는 일을 할 때다. 의존성을 patch해 실패 경로에 도달하거나, 정확한
  진단 문자열을 고정하거나, validator가 routing되는지 자체를 증명하는 경우다.

## Validation

반복 작업 중에는 전용 suite를 실행하고 마지막에 full profile을 한 번 실행한다.

```bash
python3 -m unittest tests.test_reference_pack_routes
python3 -m unittest tests.test_validation_tooling_ownership
python3 -m unittest tests.test_validate_affected_surfaces tests.test_run_validation_lane
python3 -m unittest tests.test_agent_governance tests.test_ci_qa_workflow
python3 -m unittest tests.test_document_strict_cutover
python3 scripts/qa.py full
git diff --check
```

전체 suite에 대한 discovery 실행은 `full` profile이 한 번 소유한다. 같은
바이트에 `unittest discover`를 따로 돌리면 증거가 늘지 않고 profile이 이미 한
일을 반복할 뿐이다. discovery는 profile 밖에서 실패를 재현할 때만 직접 실행한다.

완료 순서와 PASS/FAIL/SKIP/DEFER의 의미는
[Quality policy](../.agents/governance/quality.md)가 소유한다. 이 README는 현재
테스트 진입점을 나열할 뿐 그 정책을 다시 정의하지 않는다.

## Operations

### Working Procedure

1. 결함은 가장 좁은 독립 테스트에서 재현한다.
2. 한 번 쓰는 mutation에는 임시 데이터를 쓴다. 영구 fixture는 여러 사례가
   오래 유지되는 같은 의미의 입력을 공유할 때만 추가한다.
3. production 변경은 이 트리를 import하거나 읽지 않고 한다.
4. 전용 suite, 소유권 검사, affected·staged 검증, 바뀐 surface가 요구하는 넓은
   검증을 실행한다.
5. 마지막 독립 소비자가 없어지면 그 fixture도 삭제한다.
6. 실행할 수 없는 hosted·provider·live 검사는 `DEFER`로 보고하며 로컬 PASS로
   보고하지 않는다.

test module은 책임이 바뀌면 추가, 병합, 폐기될 수 있다. module 수와 정확한
method 목록은 관찰 결과일 뿐 거버넌스가 아니다.

## Related Documents

- [Scripts](../scripts/README.md)
- [Quality policy](../.agents/governance/quality.md)
- [Work lifecycle](../.agents/workflows/work-lifecycle.md)
- Validation ownership ADR (`docs/02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md`)

위의 승인된 결정이 검증 책임의 현재 owner다. 그 결정을 처음 실행한 완료 Spec과
Task는 봉인된 증거이며 archive index로 계속 찾아갈 수 있다. 그 문서들은 한 번
실행한 일을 기록할 뿐, 지금 유효한 규칙을 다시 선언하는 문서가 아니다.
