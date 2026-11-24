---
title: "scripts"
version: "1.0.1"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---
# scripts

## 문서 개요

### 목적과 독자

이 README는 scripts의 사용·연결·검사 위치를 찾는 운영자와 기여자를 안내한다. 현재 역할은 [Service](#service)와 [Usage](#usage)에 기록한다.

### 책임과 적용 범위

platform은 scripts의 진입 경로를 유지한다. 이 경로의 파일과 경계는 [Purpose](#purpose), 사용 조건은 [Usage](#usage), 검사는 [Checks](#checks)가 설명한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙


#### Service

##### Purpose

`scripts/`는 저장소의 문서, Agent governance, GitOps, CI, 보안 경계를
repository-static 방식으로 검증하는 실행 코드의 소유 경로다. 사람에게 보이는
규칙은 각 canonical 문서가 소유하고, 이 폴더는 그 규칙의 machine enforcement와
검증 routing만 구현한다.

검증 선택과 command mapping의 단일 machine owner는
`validation/registry.json`이다. 개별 validator는 자기 진단 의미를 소유하며,
`qa.py`와 `run-validation-lane.py`는 선택된 owner를
호출하고 결과를 정규화한다. production module은 top-level `tests/`를 import하거나
`tests/fixtures/`를 runtime input으로 읽지 않는다.

- Validation ownership ADR (`docs/02.architecture/02.decisions/README.md`)
- [Tests](../tests/README.md)

검증 책임의 현재 owner는 공통 Quality policy와 `scripts/validation/registry.json`이다.
과거 결정과 완료 기록은 Git history 탐색을 통해 확인하는 배경 증거이며,
현재 실행 절차의 선행 조건이 아니다.

###### Audience

- Platform maintainers
- Quality engineers
- Documentation maintainers

###### Routing and orchestration

| Path | Purpose |
| --- | --- |
| `validation/registry.json`과 그 schema | validator, surface, lane, 인자, fallback 계약 |
| `AGENTS.md` | 이 폴더의 에이전트 지시. 실행 코드가 아니다. |
| `select-affected-surfaces.py` | 경로를 surface로 고르는 순수 선택 projection |
| `githooks/chained-hook.sh`와 그 `pre-commit`, `commit-msg`, `pre-push` 링크 | 사용자의 전역 Git hook을 먼저 실행한 뒤 이 workspace의 hook을 실행하고, 처음 나온 0이 아닌 상태를 반환 |
| `commit-message-exceptions.py` | `.pre-commit-config.yaml`의 commit-msg stage에서 pinned Commitizen 뒤에 실행한다. `.cz.toml`의 생성 메시지 pattern으로 Git Merge/Revert 생성 형식의 구문만 예외로 인정하며 prefix 위조를 거부한다. 같은 형식의 수동 메시지도 통과하므로 실제 생성·merge/revert·provenance를 증명하지 않는다. 일반 메시지 문법은 Commitizen, PR title은 trusted-base authored schema가 소유하고 이 guard를 쓰지 않는다. hook 등록만으로 실제 로딩·실행을 주장하지 않는다. |
| `validate-affected-surfaces.py` | registry와 추적 경로 coverage 검증 |
| `run-validation-lane.py` | 현재 v4 소스의 affected·staged 선택 입력을 제한해 실행하고 결과를 정규화한다. PR은 `pull-request` profile의 cumulative base-to-merge 계획을 `--plan-output`으로 한 번 만들고 `--plan-file`로 소비한다. `--combine-documents`는 links/profile의 invocation parse를 공유하며 manifest는 변경 의존 root를 받는다. 선택된 변경 경로를 문서 reader에 전달하며, 인자 수나 크기 한계를 넘으면 reader의 전체 검사를 사용한다. 구형 all-files 집계 경로 제거의 검증·수용 상태는 [Stage 03 Spec navigation](../docs/03.specs/README.md)에서 찾는 SPEC-0107 Task가 기록한다. |
| `validate-selected-style.py` | 변경 경로에 검토된 style hook을 일회용 저장소에서 실행해 검사한다. |
| `validate-selected-nonstyle.py` | 검토된 non-style hook을 격리된 QA 스냅샷의 선택 경로에 실행한다. |
| `qa.py` | 지원되는 QA 진입점. profile의 gate ID를 registry에서 해석해, 격리된 작업 트리나 정확한 index 스냅샷에서 실행한다. 한 실행에서 캡처한 스냅샷 트리를 gate 입력 identity에도 재사용한다. validator argv나 규칙 구현은 담지 않는다. |
| `validation/` 규칙 module | 전용 validator가 아직 소유하지 않은 저장소 전체 규칙(repository/quality.py)과, 현재 실행 대상과 Git 우선 역사 복구의 구분(current_executable_references.py) |

###### Document owners

| 경로 묶음 | 책임 |
| --- | --- |
| `document_contracts.py`, `validate-document-contract-registry.py`, `validate-markdown-profiles.py` | route·profile 분류와 작성된 Markdown의 의미 검증. affected·staged의 변경 경로가 본문 검사 대상을 정하며, 현재 문서의 metadata·identity 검사와 English-only 파일 검사는 유지한다. 생산자·reader helper 변경은 Registry의 문서 검사 owner로 연결한다. |
| `document_authority.py`, `validate-links-and-owners.py` | 현재 owner와 문서 간 관계의 의미 검증. 링크 검사 한 실행의 context가 Registry와 문서 inventory를 보유해 같은 입력의 재조회에 쓰인다. |
| `document_lifecycle.py`, `validate-document-lifecycle.py` | registry가 분류한 lifecycle과 staged index 전이 |
| `request_brief.py` | provider `UserPromptSubmit` 요청 접수, 모델이 표시한 브리핑 기록, 쓰기 guard의 첫 변경 허용을 현재 요청·workspace·branch·정책 digest에 결합하는 로컬 상태 도구 (SPEC-0231) |
| `validate-execution-brief.py` | 작업자 인계·재개·상태 변경 직전 현재 요청과 브리핑의 대응 및 범위를 확인하는 명시적 읽기 전용 진입점 |
| `document_language.py` | 문서의 언어를 판정하는 순수 규칙 |
| `validate-knowledge-surface.py` | knowledge owner 포인터, Repository Vocabulary 용어 표와 제한된 관찰 출처 검증 |
| `document-backlinks.py` | 정방향 링크에서 한 문서를 가리키는 추적 문서 목록을 파생하는 탐색 도구(gate 아님) |
| `document-generator.py` | registry와 form에서 새 문서 한 개를 만들고 공통 value marker 다섯 개를 채우는 도구(gate 아님, 호출될 때만 한 파일을 쓰며 번호를 할당하지 않는다) |
| `validate-work-residue-ledger.py` | work residue ledger와 Task의 `Residue Handoff` 행이 식별자·상태·소유자·재개 조건에서 일치하는지, 닫힌 항목이 PASS EVD 행을 가리키는지 검증하는 gate |
| `work-residue-ledger.py` | ledger를 종류·상태·소유자로 걸러 한 항목당 한 줄로 출력하는 탐색 도구(gate 아님, 파일을 쓰지 않는다) |
| `json_schema_validation.py` | production validator가 함께 쓰는 오프라인 JSON Schema 로딩 |
| `frontmatter_yaml.py` | 거버넌스 문서와 native 에이전트 frontmatter 다섯 loader가 함께 쓰는 YAML 1.2 loader(`ruamel.yaml`, 중복 key·directive·anchor·alias·explicit tag·merge key·복수 문서 거부, timestamp는 text로 유지) |
| `run-contract-tests.py` | 이름 있는 suite 하나의 계약 회귀를 그 suite의 목적 gate로 실행한다. suite별 모듈 목록은 `validation/contract-suites/<suite>.json` 파일 하나가 소유하며, 그 파일의 변경은 해당 suite와 등록 검사만 선택한다. 이 실행기 자체의 변경은 모든 suite를 선택한다. 각 gate는 Registry에서 `--suite`로 suite 하나를 지정한다. 긴 blanket unit discovery의 간접 `coveredBy`를 현재 완료 조건으로 삼지 않는다. |

`docs/98.archive/`는 검증 대상이 아니다. 문서 검사는 그 경로를 inventory에서
제외하고, 변경 시에는 secret 검사만 실행한다. 이 경로를 가리키는 링크도 검사하지 않는다.

###### Agent governance owners

| 경로 | 책임 |
| --- | --- |
| `validate-agent-governance.py` | role·schema, native metadata, 권한, skill |
| `prompt-input.py` | 선언된 계약에서 모델 호출 없이 prompt 요청을 조립 |
| `workspace_memory.py` | Claude와 Codex 세션이 공유하는 workspace memory 저장소. memory는 결정 맥락일 뿐 Task 상태나 증거가 아니다. |
| `session_capture.py` | 이 workspace의 Claude·Codex 세션 수명주기 hook과 transcript cursor scan으로 위치·구조만 기록하는 로컬 세션 수집기. 본문은 복사하지 않으며 memory나 Task 증거가 아니다. |
| `session_analysis.py` | 세션 수집 기록을 Asia/Seoul 날짜별로 결정론적으로 집계해 개선 후보를 만드는 예약 분석. lease·재시도·취소·따라잡기를 갖추며, 후보는 검토 뒤에만 memory 후보나 Task 참조가 된다. |
| `test_cluster.py` | 선택한 GitOps 앱 closure를 이 workspace 소유의 일회성 k3d 시험 클러스터에 올리고, 소유가 입증된 자원만 지우는 CLI 진입점. 전체·와일드카드·root 선택과, 운영자 승인을 `--authority`로 이름 붙이지 않은 `up`은 거부한다. `up`은 생성 전에 공용 자원을 예약하며, 제품 디스크 제한이 필요한 선택은 검증된 VM capsule을 요구한다. `--vm`은 아래 VM 보조 모듈로 연결한다. |
| `environment_admission.py` | 클러스터와 병렬 작업자가 함께 쓰는 계정 범위 CPU·메모리·디스크 예약 및 소유 확인 후 해제 저장소. 예약은 실제 프로세스나 컨테이너의 물리적 자원 격리를 입증하지 않는다. |
| `test_cluster_environment.py` | 선택형 클러스터의 소유 네트워크·만료 타이머·노드 CPU 설정, VM capsule 검증과 선택한 namespace의 네트워크 probe를 담당하는 보조 모듈. 직접 host k3d 실행의 제품 디스크 제한은 검증된 capsule 없이 거부한다. |
| `test_cluster_vm.py` | `test_cluster.py --vm` 경로의 소유 VM 이미지·디스크 준비, 게스트 시작·검증·정리와 guest 제품 실행을 담당하는 보조 모듈. 실제 VM 실행과 자원 격리의 인수 근거는 별도로 확인한다. |
| `test_cluster_vm_lifecycle.py` | `--vm` 호스트 경로의 예약, 소유 VM 시작·종료, 실패 정리와 소유 확인 후 lease 해제를 조정하는 보조 모듈. |
| `test_cluster_vm_transport.py` | VM의 크기·시간 제한을 둔 공용 이미지 수신, 공개 입력 전송과 네트워크 probe를 담당하는 보조 모듈. |
| `work_forecast.py` | 작업 시작 전에 P30/P50/P80 예측을 도구 시계로 고정하고, 시작·결과를 한 번씩 기록한 뒤 유형·시간기준·단위별 coverage와 pinball 손실을 N과 함께 보고하는 로컬 저장소. 수정은 새 revision이며, 취소·실패는 censored로 따로 센다. 예측은 승인·기한·timeout이 아니다. |
| `work_parallel.py` | 계획의 work unit을 입력·출력·의존성·공유 자원과 함께 받아, 겹치지 않는 unit만 각자의 clone에서 동시에 실행하고 통합 clone에서 통합 검사를 다시 실행하는 dispatcher. 잠금마다 fencing generation을 두어 만료·취소된 시도의 결과를 거부하고, 소유 경로 밖 변경을 거부하며, 동시 서비스 합집합을 `test_cluster.py` 한도로 묶는다. worker와 통합 실행은 clone 생성 전에 공용 자원을 예약하고, 소유 프로세스의 부재를 확인한 뒤 예약을 해제한다. 결과는 `candidate.patch`이며 원본 checkout은 쓰지 않는다. `sweep`은 죽은 dispatcher가 남긴 worker와 clone을 정리한다. unit은 command 대신 provider(`claude` 또는 `codex`)와 prompt, model, claude의 지출 상한 `budget_usd`를 지정할 수 있다. dispatcher는 설치된 CLI 고유의 argv(`claude -p --output-format json --safe-mode --tools Read,Edit,Write`, `codex exec --json --ephemeral --sandbox workspace-write`)를 만들어 prompt를 stdin으로 넘기며, provider unit은 `run --request <id>`가 브리핑이 기록되고 현재인 P08 요청을 가리킬 때만 시작한다. provider worker는 각자 systemd user scope에서 실행되어 메모리, CPU 1개, task 수, 실행 시간을 제한하고, 종료·timeout·취소·sweep 때 scope를 멈추면 `setsid` 후손까지 모두 끝난다. 그 안에서 bwrap이 clone과 비공개 `/tmp`를 제외한 host를 읽기 전용으로 마운트하고, 별도의 PID·IPC namespace와 빈 환경에서 시작하며, 읽기 전용 마운트로는 막히지 않는 socket 연결을 막으려고 `/run`과 그 밖의 listening path socket을 가린다. provider가 API를 쓰므로 host 읽기와 네트워크는 열려 있어 abstract socket과 local TCP 서비스에는 닿을 수 있고, 디스크 사용량은 quota가 아니라 결과 수집 시점에 확인한다. 보고서는 provider unit별 scope, session ID, CLI가 보고한 추정 비용(실제 청구액은 관측하지 않아 null), turn 수, usage를 기록하고, 원문 출력은 해석한 뒤 지운다. command worker는 바뀌지 않아 호출자 자신의 권한으로 sandbox 밖에서 실행되며, clone은 파일 분리일 뿐 sandbox가 아니다. |
| `work_observe.py` | 이미 남아 있는 예측 기록, 병렬 실행 보고서, 해당 Task로 승격된 세션 분석 후보를 artifact key로 읽기 전용 연결하는 보고 도구. 새 저장소나 원문 사본을 만들지 않고, 기록이 없는 출처는 0이 아니라 null과 이유로 표시하며, 비용은 CLI 추정과 실제 청구(null)를 나눈다. hosted CI 시간은 run ID로 인용한다. |
| `review_delta.py` | 검토한 commit 이후의 변경을 판정한다. 기존 Task의 사실형 Evidence 행 추가와 필요한 `version`·`updated` 교체만 `EVIDENCE_ONLY`로 분류한다. 새 Task, 잔여 원장 변경, 승인·수용·요구 추가, 기존 행 수정, mode 변경·symlink·gitlink·이력 재작성은 `REREVIEW`다. 이 도구는 제한된 형식의 증거를 보수적으로 분류하며, 자연어의 모든 의미를 증명하지 않는다. 전이 영향과 불명확한 의미는 검토자가 판정한다(QUAL-R054). |

###### Platform and supply-chain owners

| 경로 | 책임 |
| --- | --- |
| `validate-gitops-change-set.py`, `validate-gitops-structure.sh` | GitOps identity와 구조 검증 |
| `validate-k8s-manifests.sh`, `validate-policy-gates.sh` | manifest 문법과 저장소 정책 검사 |
| `validate-infrastructure-contracts.sh` | 저장소 정적 infrastructure 계약 검사. live cluster 검사는 `infrastructure/verify/`에 있다. |
| `validate-vault-eso-contracts.py`, `check-secret-handling.sh` | Vault·ESO 참조 계약과, 값을 가린 secret 패턴 검사 |
| `validate-github-actions-security.py`, `validate-ci-python-contract.py`, `validate-pr-metadata.py` | workflow 공급망과 Python 의존성 계약. `validate-pr-metadata.py`는 `ci-summary`의 PR metadata 검사 원본으로, 신뢰된 base의 `.cz.toml` 문법에 따라 PR title과 새 commit 범위를 확인한다. hosted 결과는 로컬 QA를 대체하지 않는다. |
| `validate-workspace-boundary.py` | staged workspace 경계와 ignore 경로 계약 |
| `render-platform-chart-kinds.sh` | 운영자가 직접 실행하는 chart kind 리뷰 보조 도구 |
| `release.py` | main changelog PR을 준비하고 SemVer GitHub Release 하나를 명시적으로 게시한다. 기본은 로컬 읽기 전용 미리보기이며 `publish --execute`는 운영자, 또는 version과 asset을 명시한 운영자의 현재 요청에 따른 agent가 실행하는 operator-approved 작업이다. |
| `semver_grammar.py` | 문서·계약에는 ASCII 숫자 세 요소 판본 문법과 숫자 비교를 제공한다. `release.py`는 별도의 제품 SemVer 문법과 우선순위 비교로 태그 패턴과 순서를 정한다. |

##### Interfaces

- [Agent execution policy](../.agents/governance/agent-execution.md)
- [Quality policy](../docs/00.workspace/04.quality/quality.md)
- [Document authoring policy](../docs/00.workspace/03.process/document-authoring.md)

###### Security Boundary

이 문서는 secret, credential, 권한 경계만을 다루는 내용을 따로 두지 않는다. 그런 내용을 두게 되면 여기에 적는다.

#### Usage

##### Prerequisites

- 문서 route·profile 값은 [Stage 99 계약](../docs/99.templates/README.md)에서만 온다.
- Agent role, 권한, skill, handoff, projection은
  `.agents/roles/registry.json`에서만 온다.
- 검증 선택과 명령 인자는 `scripts/validation/registry.json`에서만 온다.
- `.github/workflows/ci.yml`과 `.pre-commit-config.yaml`은 projection이며
  선언되지 않은 validator나 중복된 규칙 owner를 들여오면 안 된다.
- 구조화 쓰기 경로 검사는 `provider_write_guard.py`가 소유하고 각 provider
  adapter가 native event를 등록한다. shell 관찰은 advisory이며, 실제 전달과
  native 강제는 [승인 정책](../docs/00.workspace/04.quality/approval-and-safety.md)과
  provider note의 관측 경계를 따른다. 품질 검증은 명시적으로 실행하는 QA 작업이다.
- 테스트와 제한된 합성 데이터는 `tests/`와 `tests/fixtures/`에 둔다.
- 기본 복구 출처는 Git history다. digest는 외부에서 바뀌지 않는 의존성
  identity나 과거 복구 좌표가 있을 때만 쓴다.

Python validator의 모든 subprocess 호출은 유한한 timeout을 쓴다. 텍스트
입력은 명시적으로 UTF-8로 읽고 소유 계약이 요구하는 곳에서는 symlink나
일반 파일이 아닌 경계를 닫힌 쪽으로 실패시킨다. 진단 메시지에는 secret 값을
담지 않는다.

###### Scope

<a id="in-scope"></a>
**In Scope**

- 문서 profile, lifecycle, link, owner 검증
- Agent registry, provider projection, loop, CI 계약 검증
- 선택된 affected·staged routing과 목적별 제한된 subprocess 실행
- GitOps, Kubernetes, Vault/ESO, GitHub Actions, CI Python 검사
- 아직 더 좁은 전용 owner가 없는 저장소 전체 계약

<a id="out-of-scope"></a>
**Out of Scope**

- hosted CI, branch protection, provider runtime, credential, 배포, live cluster 증거
- test fixture, 합성 mutation, 고정된 negative case inventory
- branch tip, 현재 문서, 현재 스크립트, 줄 번호, corpus 개수를 고정하는 pin
- Stage 00, SDLC stage, Operations에서 옮겨 온 정책 문장

##### Selected Start

###### Working Procedure

1. `validation/registry.json`에서 규칙과 그 전용 의미 owner를 찾는다.
2. 동작을 바꾸기 전에 독립적인 top-level 테스트를 추가하거나 고친다.
3. production 데이터는 production owner 옆에 두고 합성 데이터는 독립적인
   테스트 소비자와 함께 `tests/fixtures/` 아래에 둔다.
4. validator는 routing owner 한 곳에 추가하고 선언된 lane이 요구하는 곳에만
   hook·CI로 projection한다.
5. 일회성 또는 오래된 검사는 지속 보장을 현재 owner로 이전하고 caller와
   등록을 제거한 뒤 전용 wrapper·fixture·test의 소비자 0개를 확인한다.
   필요한 과거 결과는 기존 Task 위치에 남기고 복구는 Git history로 한다.
6. 커밋 전에 `git diff --check`, 관련 전용 테스트, affected·staged 선택,
   전체 결과를 검토한다.

없어진 구현 형태를 지키려는 목적만으로 호환 CLI, 중복 registry, 고정된 스크립트
inventory, 내장 mutation suite를 만들지 않는다. 호스팅 check 이름과 원격
branch protection의 활성 상태는 실제 원격에서 확인해야 하며, 저장소 파일만으로
required-check 성공이나 설정을 주장하지 않는다.

#### Checks

##### Readiness

###### 요청 브리핑 사전 확인

요청을 받은 호출자는 원본 상호작용에서 현재 요청을 다시 확인하고,
Task의 Inputs and Authority에 요청 참조·판본·범위를 기록한다.
독립적으로 구성한 현재 요청 JSON과 작업자가 소비할 BriefRecord JSON을
검사에 함께 넘긴다. 메모리나 브리핑을 복사해 현재 요청 입력을 만들지 않는다.

```bash
python3 scripts/validate-execution-brief.py --root . \
  --brief "$brief_file" --current-request "$current_request_file" \
  --operation dispatch --action "$action_id" --path "$target_file"
```

위 변수는 호출자가 실제 입력에 맞게 준비한다. 읽기 전용 인계에는
`--path`를 생략한다. 변경 대상은 워크스페이스 상대 파일 경로를
`--path`로 각각 지정한다. 현재 요청에는 목표, 요청 참조·SHA-256·판본,
실제 작업 루트와 HEAD, 범위·제약·인수 기준·검사 목록, 위험,
권한 참조, 허용 변경, 파일별 상태를 담는다. `material_inputs`에는
선택한 모든 변경 대상의 현재 SHA-256을 기록한다. 아직 없는 경로에는
`"absent"`를 기록한다. 누락된 대상, 달라진 내용, 예상과 달리 생기거나
사라진 파일, 안전하게 읽을 수 없는 경로는 검사에 실패한다. 현재 요청의
`allowed_actions`는 호출자가 확인한 행동 ID별 `operation`과 정확한
`paths`의 매핑이다. 행동이 선택적 `inputs`로 자신이 읽는 material 입력을
밝히면 그 입력과 대상 경로만 비교하므로, 관련 없는 입력(예: Task의 증거 행
추가)의 변경은 그 행동을 막지 않는다. `inputs`가 없으면 모든 material 입력을
비교한다. `state`는 호출자가 확인한 최신 유효 상태다.
최신 브리핑 ID·판본과 미해결 질문은 양쪽 입력에서 일치해야 한다.
브리핑에 확인된 사실과 출처, 가정을 따로 담는다. 파일은 임시 입력으로
사용하고 원문 권한 확인은 기존 절차를 따른다.

재개나 상태 변경에는 `--operation resume` 또는 `--operation state-change`를
사용한다. 요청 수정·철회, 작업 대상 또는 입력 변경으로 실패하면 해당
행동을 멈추고 최신 원본에 연결한다. 범위와 판본 일치 결과는 로컬 사전
검사 증거다. 실행 직전에 호출하고, 검사 이후 파일 변경이 관찰되면 다시
확인한다. 원본 승인, 네이티브 훅 전달과 실제 실행은 각각 확인한다.

가장 작은 owner부터 실행하고 현재 작업에 필요한 affected·staged lane을
선택한다. 로컬 커밋마다 정확한 index 기준의 staged QA가 필요하다. 이 public
저장소의 목적·단위 QA는 로컬에서 실행한다. GitHub Actions의 branch
metadata와 PR style 결과는 로컬 QA의 대체 증거가 아니다. global QA 계약을
바꾸거나 한정 감사를 수행해도 해당 목적 gate와 명명된 단위 회귀만 선택한다.
긴 full/ci 일괄 검사와 blanket unit discovery는 현재 완료 조건이 아니다.
나머지 선택과 인계는
[Quality policy](../docs/00.workspace/04.quality/quality.md#delivery-ownership)가 소유한다.

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

###### Reproducing the local dependency identity

검토된 hash lock으로 checkout 밖의 환경을 준비하고 실제 interpreter·도구
identity를 확인하는 방법은 [local validation environment guide](../docs/00.workspace/05.environment/0011-local-validation-environment.md)가
소유한다. 준비한 Python으로 `scripts/qa.py quick` 또는 `scripts/qa.py staged`를
현재 입력에 맞춰 실행한다. Python gate는 호출한 interpreter를 쓰고,
selected style·nonstyle gate는 그 Python의 `pre_commit` module이 없으면
`STYLE-TOOL` 또는 `NONSTYLE-TOOL`로 실패한다. shell validator는 닫힌 시스템
`PATH`를 사용한다. gitleaks와 conftest의 신뢰할 수 있는 interpreter 인접
경로 또는 계정 소유 fallback 선택은 실행 구현이 소유한다. lock의 존재나
환경 준비만으로 검증 PASS 또는 hosted identity를 주장하지 않는다.

커밋 hook은 Git 설정 `hyhome.validationVenv`가 가리키는 환경을 `PATH` 맨 앞에
두고 실행한다. hook 연결과 `HOOK-ENV` 실패 조건은
[Git policy](../docs/00.workspace/03.process/git.md)가 소유한다.

staged QA는 첫 commit부터 정확한 index와 staged 설정을 읽으며, 무관한
unstaged·미추적 파일을 입력으로 삼지 않는다. 구현 회귀 suite는 affected quick과
PR CI가 실행한다. 로컬 commit은 선택된 syntax·style·secret·내용 계약을 검사하고,
변경이 없으면 snapshot 준비 없이 종료한다. manifest·render·policy는 기존 변경
범위 선택기를 사용하되 전역 GitOps identity 보호는 유지한다.

formatter는 직접 호출하지 말고 `pre-commit`으로 실행한다. hook 설정은 일부러
`ruff-format`을 Python으로만 좁혀 둔다. 그냥 명령을 실행하면 Markdown까지
대상으로 삼아, 작성된 문서와 보관된 문서 안의 fenced snippet을 다시 쓴다.
shfmt와 공백 수정도 리뷰를 거친 소스 경로에 대해 명시적으로 `--files`로 실행하는
작업이다. 선택된 staged style은 격리된 정확한 index에서 실행하며 formatter가
무언가를 바꾸면 검증이 실패한다. 수정과 검사는 분리한다. 명시적 수정은
리뷰한 소스 경로만 지정해 아래처럼 실행하고, diff를 확인한 뒤 다시 stage하고
검사를 새로 돌린다. 검증하지 않는 Archive와 raw 평가 출력은 hook의 `exclude`가 막으며,
그 목록은 `tests/test_validation_tooling_ownership.py`가 Registry와 대조한다.

```bash
pre-commit run <hook-id> --hook-stage manual --files <reviewed-path>...
```

commit-msg는 별도이며 실제 후보 UTF-8 메시지에는 pinned Commitizen과
`commit-message-exceptions`를 같은 파일로 적용하는
[공통 Git 정책](../docs/00.workspace/03.process/git.md#commit-message-validation)을 따른다.
활성 hook에서 같은 입력의 leaf가 실제 실행되었다면 수동으로 반복하지 않는다.
수동 fallback 검증은 hook 설치·전달 증거를 대신하지 않는다.

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

##### Failure Handling

이 문서에는 운영 관측과 복구만을 다루는 별도 내용이 없으며, 기본 복구 출처는 Git history다.

공유 workspace memory 저장소(`.workspace-memory/memory.sqlite3`)를 백업에서
되돌릴 때는 다음 순서를 따른다.

1. 저장소에 쓰는 모든 세션을 멈춘다.
2. 저장소 옆에 남은 `memory.sqlite3-journal`을 지운다.
3. `memory.backup.sqlite3`을 저장소 파일 위에 복사한다.
4. `pragma integrity_check`가 `ok`인지 확인한다. 복원한 저장소는 같은 기록을 읽는다.

`erase`로 지운 기억은 백업을 갱신한 뒤에는 백업에도 없다. `MEMORY_ERASE_BACKUP_STALE`이 보고된 이전 백업으로 되돌리면 지운 기억이 다시 나타나므로, 그 백업은 복원에 쓰지 않는다. 다른 schema 판본의
저장소는 열리지 않으며, 변환은 운영자가 명시적으로 수행한다.

###### Runbook Links

이 문서는 runbook이나 운영 가이드 링크를 따로 두지 않는다. 연결할 운영 문서가 생기면 여기에 연결한다.

## 적용과 확인

### 적용 방법

아래 역할별 본문에 기록된 사용 조건과 절차를 적용한다.

### 확인 기준

아래 역할별 본문의 검증·확인 조건과 그 한계에 따른다.

## 관계와 출처

### 관련 문서

관련 문서와 정본 링크는 아래 역할별 본문에서 확인한다.

### 외부 근거

외부 근거가 사용된 경우 아래 역할별 본문의 출처와 적용 범위에서 확인한다.
