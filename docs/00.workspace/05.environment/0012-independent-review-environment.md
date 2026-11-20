---
title: "독립 검토 읽기 전용 환경 가이드"
version: "0.1.1"
type: "operation/guide"
status: "in-review"
owner: "platform"
updated: "2026-11-20"
artifact_id: "GDE-0012"
---

# 독립 검토 읽기 전용 환경 가이드

## 문서 개요

### 목적과 독자

이 가이드는 현재 지원되는 Codex·Claude 검토 실행면의 읽기 전용 경계를
준비하고 확인하는 작업자와 운영자를 위한 안내다.

### 책임과 적용 범위

이 문서는 환경의 준비와 확인 순서를 소유한다. 위험·완료 판정은
[Quality Policy](../04.quality/quality.md), 보호 행위는
[agent approval and safety](../../../.agents/governance/approval-and-safety.md),
native 설정과 사실은 [Codex](../../../.codex/provider.md)·[Claude](../../../.claude/provider.md)
note가 소유한다. 원 Desktop 경로의 실패와 재개 조건은 현행
[SPEC-0223 Task](../../03.specs/0223-work-residue-handoff/01.tasks/tsk-0001-work-residue-handoff.md)에
있다. P06의 새 Spec·Task는 이 최초 draft 기록 이후 게시된다.

## 내용 계약

### 입력과 전제

현재 checkout의 실제 후보 diff, 원 요구·설계·소비자, 설치된 client와
현재 계정의 비밀이 아닌 인증 상태가 입력이다. P06의 기존 계정 내 한정
관측은 현재 사용자 요청에 포함된다. 실제 credential, 운영 kubeconfig,
Docker socket과 production endpoint는 검토 입력이 아니다.

### 본문과 규칙

#### Purpose

##### Audience

검토 실행자, 비구현 검토자와 결과를 판정하는 품질 담당자가 독자다.
각자는 Git 후보와 별도 임시 source의 범위를 알아야 한다.

##### Outcome

이 문서는 `how-to` 가이드다. 독자는 선택한 실행면의 실제 판본·부모
권한·도구와 source 읽기/쓰기 결과, focused review의 판단을 각각
확인한다. 동일한 version·설정·권한 경계의 관측만 재사용한다.

###### Boundaries

[Quality Policy](../04.quality/quality.md)의 판단·문맥·권한
독립성을 모두 확인한다. 별도 role 이름, 설정 파일, 합성 fixture, hook
호출이나 OS preflight 하나만으로 실제 모델 검토를 주장하지 않는다.
CLI 성공은 이전 Desktop→SSH workspace-write/null-profile 실패를 고치지
않는다. 서비스 전체 기동, 운영 비밀 읽기와 P07 구현은 이 가이드 밖이다.

#### Prerequisites

##### Environment

`command -v codex`, `codex --version`, `codex sandbox --help`,
`command -v claude`, `claude --version`, `claude --help`로 사용될 binary와
기능을 확인한다. P06 조사 시 PATH Codex CLI는 0.169.0, Desktop daemon은
0.171.0, Claude는 2.1.328이었다. 다음 실행은 그때의 실제 판본을 다시
기록한다. Codex ChatGPT login과 Claude claude.ai firstParty Max는
인증 메타데이터이며 무료 호출이나 정확한 청구액의 증거가 아니다.

계정 소유 임시 경로에 작은 dummy source와 가짜 secret sentinel을 만든다.
실제 비밀이나 개인 원문은 복사하지 않는다. 임시 source, 검토용 diff
packet과 결과 경로를 따로 정하고 관측 후 임시물을 삭제한다.

##### Authority

현재 P06 요청은 기존 계정·모델·기능 한도에서 한정한 실제 검증을
허용한다. 전역 trust·credential·구독 변경, source 수정·배포·merge는
검토 권한이 아니다. 공급자 모델 통신과 검토 작업 도구의 외부 통신은
구분한다. 비용을 관측하지 못하면 `null`과 이유를 기록한다.

#### Procedure

##### Steps

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | 실제 client, parent, account metadata, model, candidate revision과 이전 동일 조건 근거를 기록한다. | 선택한 경로 하나와 다른 경로의 결과가 분리된다. | 설치·인증 문제를 해당 provider owner에게 넘기고 실제 시도 여부를 적는다. |
| 2 | 새 비구현자 문맥에 원 요구·설계·후보 diff·소비자·실패 조건만 전달한다. | 검토 판단과 문맥의 독립성이 확인된다. | 구현자 결론만 전달된 packet은 다시 구성한다. |
| 3 | Codex는 실제 read-only 부모 또는 전체 프로세스 경계를, Claude는 shell 밖 파일 도구·MCP·hook까지 포함한 제한을 선택한다. | 적용된 도구·filesystem·network scope가 확인된다. | role projection 또는 advisory hook만 있으면 고위험 검토를 시작하지 않는다. |
| 4 | 같은 경계에서 임시 source 정상 읽기와 금지된 source 쓰기, 가짜 외부 파일 및 필요한 network 제한을 확인한다. | source write가 거절되고 금지 대상에 접근하지 못한다. | `allowed`면 해당 경계는 `failed`; 별도 검증된 route를 선택하거나 수리한다. |
| 5 | Codex와 Claude의 대표 focused review를 순차 실행한다. 실행당 최대 600초, 지원되면 최대 여섯 작업 턴, 최초 1회와 수리 후 확인 1회를 한도로 한다. | 실제 diff에 대한 finding·판단·미관측이 도착한다. | 같은 원인을 반복 호출하지 않는다. |
| 6 | boundary state와 source-write 결과, 사용량과 임시물 삭제를 Task에 기록한다. | 정적 검사·native 권한·검토·사용자 인수가 구분된다. | 다른 경로 성공으로 실패 경로를 지우지 않는다. |

Codex 0.169.0의 제한된 CLI profile 사전 점검은 `codex sandbox -P`
경로에서 임시 source 읽기 성공, 쓰기 `EROFS` 거절, 가짜 외부 파일
은닉, AF_INET socket 생성 `EPERM`을 보였다. 정확한 profile에는
root deny, 최소 실행 기반 read, Codex binary와 dummy source read,
network false가 있었다. 같은 경계로 실제 모델을 실행할 때는
`--ignore-user-config`, 해당 profile을 가리키는 `default_permissions`,
검토용 복사본의 CWD를 사용한다. legacy `--sandbox`를 함께 넣어 두
설정이 합쳐졌다고 가정하지 않는다. 2026-11-20의 실제 Codex 모델
검토는 CLI 0.169.0, `gpt-6-sol`/high, fresh parent와 아래 flag 구성을
사용해 310.418초에 종료됐다. 임시 source 읽기 성공, source 쓰기
거절, 외부 가짜 sentinel 은닉, socket 생성 거절을 모델이 호출한 도구에서
확인했다. 한 하위 검토자의 `apply_patch`도 read-only sandbox와 승인
설정 때문에 거절됐지만 그 하위 검토자의 등록 role/model binding은
노출되지 않아 확인됐다고 쓰지 않는다. 해당 실행의 상세 증거는 후속
P06 Task가 게시될 때 연결한다. 원 Desktop 경로의 실패는 유지된다.

다음은 그 Codex 경로에서 사용한 flag 집합이다. 실행자는 각 변수를
현재 설치 binary와 task-owned 절대경로로 채우고, 임시 packet이
`.codex/config.toml`을 포함하지 않는지 확인한다. `REVIEW_OUTPUT`은
source 밖의 출력 위치다. prompt는 이 packet에 대한 실제 검토를
요청하는 작은 입력이며, 빈 호출을 성공 증거로 사용하지 않는다.

```bash
timeout --kill-after=5s 595s "$CODEX_BIN" --no-daemon -a never exec \
  --ignore-user-config --ephemeral --skip-git-repo-check --strict-config \
  -C "$PACKET_DIR" -m "$REVIEW_MODEL" \
  -c 'model_reasoning_effort="high"' \
  -c 'default_permissions="p06-review"' \
  -c "permissions.p06-review.filesystem={\":root\"=\"deny\", \":minimal\"=\"read\", \"$CODEX_BIN\"=\"read\", \"$PACKET_DIR\"=\"read\"}" \
  -c 'permissions.p06-review.network.enabled=false' \
  -c 'web_search="disabled"' \
  --disable apps --disable plugins --disable hooks \
  --enable skip_host_skill_discovery --json -o "$REVIEW_OUTPUT" - \
  < "$PROMPT_FILE"
```

실제 실행에서는 `:minimal`을 사용했다. 위 인용의 TOML 문자열은
native client가 지원하는지 현재 버전에서 확인하고, 경계의 실제
거절 결과로 판정한다.

Claude 2.1.328에서 준비한 대표 진단 후보는 다음과 같다.
`--restricted`는 shell/code 도구와 WebFetch를 제외하고 파일 도구를
현재 작업 디렉터리로 제한한다. `--safe-mode`는 사용자 정의 hook·skill·
plugin 등을 제외한다. 빈 MCP 설정과 `--strict-mcp-config`는 다른
MCP 구성을 제외하며, 명시적인 MCP deny를 더한다. managed 설정과
hook은 남을 수 있으므로 실제 도구 목록과 경계를 관측해야 한다.
`Read,Write` 중 Read만 허용하여 임시 dummy source에 대한 Write 시도가
실제 permission denial으로 나타나는지 확인한다. 진단 후 평상시
검토는 `--tools Read`로 더 좁힐 수 있지만, Write 도구가 없는 것만으로
실제 쓰기 거절 시도를 관측했다고 기록하지 않는다. 아래 후보의
성공 여부는 명령이 아닌 Task의 실제 실행 결과가 정한다.

```bash
cd "$PACKET_DIR"
timeout --kill-after=5s 595s "$CLAUDE_BIN" -p --restricted --safe-mode \
  --strict-mcp-config --mcp-config '{"mcpServers":{}}' \
  --settings '{"disableAllHooks":true}' \
  --tools 'Read,Write' --allowedTools Read --disallowedTools 'mcp__*' \
  --permission-mode dontAsk --permission-prompts none \
  --no-session-persistence --output-format stream-json --verbose \
  --include-hook-events --max-turns 6 --model "$CLAUDE_MODEL" \
  --effort high < "$PROMPT_FILE"
```

`--max-turns`는 설치된 CLI의 실제 파서와 print 경로에서 확인하고
사용한다. 선택된 모델은 현재 계정에서 허용된 것으로 한정한다. 실제
Claude 결과와 비용은 후속 P06 Task의 Results에 남기며 이 절차
문서의 status로 표현하지 않는다.
두 예시의 595초 실행과 최장 5초 강제 종료는 합계 600초 이내의
로컬 호출 제한이다. 이 제한만으로 다른 프로세스의 악의적인 탈출이나
P12 작업자 격리를 증명하지 않는다.

##### Expected Results

실제 경계와 검토를 확인한 경로만 `enforced`다. 금지된 쓰기가 허용되면
`failed`, 실행하지 않았으면 `unobserved`, 설치 client가 필요한 기능을
지원하지 않는 근거가 있으면 `unsupported`다. source-write 결과는
`denied`·`allowed`·`unobserved`로 따로 적는다. 모델 검토가 없거나
비용을 모르면 성공·무료로 채우지 않는다.

#### Troubleshooting

##### Symptoms

외부 managed tool 안의 Codex sandbox 사전 점검은
`app-server socket directory must be a user-owned directory with mode 0700`
오류로 시작하지 못했다. 같은 profile을 호스트의 허용된 실행면에서
검사한 결과와 구분한다. Codex profile에서 실제 binary 읽기가 빠지면
시작이 실패하므로 정확한 실행 파일 읽기만 추가한다. Desktop reviewer의
workspace-write/null-profile은 아직 읽기 전용 증거가 아니다.

##### Next Action

환경이 없으면 P06에서 정책·route·강제 경계를 구현하고 실제 쓰기
거절 관측만 P07 준비 직후 재개한다. 관측한 실패는
[SPEC-0223 Task](../../03.specs/0223-work-residue-handoff/01.tasks/tsk-0001-work-residue-handoff.md)에
남기고 사용 가능한 별도 CLI route의 결과와 섞지 않는다. 추가 계정·비용·
권한 변경이 현재 요청을 벗어날 때만 운영자에게 해당 차이를 제시한다.

##### Lifecycle Traceability

| Promoted owner | Audience outcome | Operating surface |
| --- | --- | --- |
| [SPEC-0223 Task](../../03.specs/0223-work-residue-handoff/01.tasks/tsk-0001-work-residue-handoff.md) | 최초 draft 시점에 원 Desktop 경로의 실패와 재개 조건을 확인한다. 후속 P06 Task가 별도 실행 결과를 받는다. | 이 checkout의 Codex·Claude 검토 경로와 P07 환경 인계 |

## 적용과 확인

### 적용 방법

단계별 실제 결과를 Task에 남기고 실패한 경계만 수리한다. 명령과
profile 값은 설치 판본에서 실제 지원되는 표면을 확인한 뒤 기록한다.

### 확인 기준

정적 문서 검사, OS 사전 점검과 실제 모델 검토는 서로 다른 증거다.
사용자 인수는 세 결과와도 별도다.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| cites | [SPEC-0223 Task](../../03.specs/0223-work-residue-handoff/01.tasks/tsk-0001-work-residue-handoff.md) |
| cites | [Quality policy](../04.quality/quality.md) |

### 외부 근거

동봉 D06/D07의 공식 Codex·Claude 자료 요약을 설계 입력으로 사용했다.
설치 판본의 실제 동작은 provider note와 Task의 한정된 관측으로 판정한다.
