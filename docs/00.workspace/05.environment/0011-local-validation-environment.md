---
title: "로컬 검증 환경 준비 가이드"
version: "1.0.0"
type: "operation/guide"
status: "draft"
owner: "platform"
updated: "2026-11-20"
artifact_id: "GDE-0011"
---

# 로컬 검증 환경 준비 가이드

## 문서 개요

### 목적과 독자

이 가이드는 로컬 검증 환경 준비 가이드에 따라 절차를 준비하고 결과를 해석할 작업자와 검토자를 위한 안내다. 독자와 결과는 [Audience](#audience) 및 [Outcome](#outcome)에 기록한다.

### 책임과 적용 범위

platform은 이 안내의 범위를 유지한다. 실행 전제는 [Prerequisites](#prerequisites), 실행 흐름은 [Procedure](#procedure)에서 확인한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Purpose

##### Audience

로컬 QA나 Git hook을 실행하는 개발자와 검증 담당자가 대상 독자다. 독자는
현재 checkout, 계정이 소유한 환경 경로, 선택할 Python을 알고 있어야 한다.

##### Outcome

이 가이드는 검토된 hash lock으로 checkout 밖의 Python 환경을 준비하고,
실제로 선택된 interpreter·도구 identity를 확인하도록 돕는다. 주된 학습 목적은
`how-to`다. 검증 의무와 결과 판정은 [Quality Policy](../04.quality/quality.md)가
소유한다.

###### Boundaries

이 절차는 로컬 환경 준비에 한정한다. [Git Policy](../03.process/git.md)는
hook 연결과 `hyhome.validationVenv`의 fail-closed 조건을,
[scripts README](../../../scripts/README.md)는 QA 진입점과 실행 범위를
소유한다. [Codex provider note](../../../.codex/provider.md)와
[Claude provider note](../../../.claude/provider.md)는 각자의 native
sandbox·permission 설정을 소유한다. 이 가이드는 비밀 값, live cluster
상태나 provider-native 실행 결과를 다루지 않는다.

#### Prerequisites

##### Environment

- 현재 checkout의 [검토된 hash lock](../../../.github/requirements/ci-validation.txt).
  헤더는 Python 3.12에서 생성되었다고 명시한다. 선택한 Python의 버전과
  실제 경로를 확인하고, lock과 대상 플랫폼에서 설치 가능한 wheel인지
  준비 단계에서 확인한다.
- 계정이 소유하고 group·other가 쓸 수 없는 checkout 바깥의 환경 경로.
  사용 가능한 `python3`, `pip` 또는 이미 설치된 `uv`가 필요하다.
- 필요한 도구 cache는 계정 소유 경로에 둔다. hook과 QA가 다른 Python이나
  shell 도구를 해석할 수 있으므로 가상환경 활성화 여부만으로 identity를
  판단하지 않는다.

##### Authority

[Approval and Safety Policy](../04.quality/approval-and-safety.md)에 따라
자신의 계정 환경과 저장소 로컬 검증만 준비한다. 전역 Git 설정을 변경하거나
외부 서비스에 접근하기 전에 해당 행위의 현재 권한을 확인한다. 이 문서에 적힌
명령은 실행 증거 또는 별도의 승인 자체가 아니다.

#### Procedure

##### Steps

1. checkout에서 lock과 Python을 확인하고, checkout 바깥의 계정 소유
   환경 경로를 정한다. 다음 예시는 환경을 `$HOME/.venvs/hyhome-validation`에
   둔다. 이 경로의 기존 환경과 사용자 설정은 덮어쓰지 말고 먼저 확인한다.
2. 해당 경로에 환경을 만들고 hash lock을 설치한다. `umask`는 새 파일의
   group·other 쓰기를 막는다. `pip`가 제공되지 않는 Python이라면 이미 설치된
   `uv`의 `uv venv`와 `uv pip install --require-hashes`로 같은 lock을 설치할 수
   있다. 둘 중 실제 선택한 도구와 판본을 기록한다.

   ```bash
   python3 --version
   python3 -c 'import sys; print(sys.executable)'
   umask 022
   python3 -m venv "$HOME/.venvs/hyhome-validation"
   "$HOME/.venvs/hyhome-validation/bin/python" -m pip install \
     --disable-pip-version-check --only-binary :all: --require-hashes \
     --requirement .github/requirements/ci-validation.txt
   ```

3. 검증에 쓸 Python과 `pre-commit`의 실제 경로·판본, 환경 내부 파일의 소유자와
   쓰기 권한을 확인한다. 선택한 환경의 경로, lock revision, interpreter와 도구 identity를
   소유 Task에 기록한다. QA의 Python gate는 호출한 interpreter를 사용하지만
   shell validator는 닫힌 시스템 `PATH`를 사용하므로 두 identity를 구분한다.

   ```bash
   "$HOME/.venvs/hyhome-validation/bin/python" -c 'import sys; print(sys.executable)'
   "$HOME/.venvs/hyhome-validation/bin/python" --version
   "$HOME/.venvs/hyhome-validation/bin/pre-commit" --version
   stat -c '%U %a %n' "$HOME/.venvs/hyhome-validation"
   find "$HOME/.venvs/hyhome-validation" \( ! -user "$(id -un)" -o -perm /022 \) -print
   ```

4. hook에서 이 환경을 쓸 때는 [Git Policy](../03.process/git.md)의
   `hyhome.validationVenv` 연결 절차와 fail-closed 조건을 확인한다. QA는
   [scripts README](../../../scripts/README.md)의 현재 변경 입력에 맞는 진입점을
   선택한다. lock이 바뀌면 기존 환경을 그대로 재사용하지 말고 새 lock으로
   재구성한 뒤 identity와 선택된 검사를 다시 확인한다.

##### Expected Results

checkout 밖의 계정 소유 환경에서 lock 설치가 성공하고, 기록한 interpreter와
`pre-commit` 경로가 실제 선택된 실행 파일과 일치한다. lock만 존재하거나
환경만 만들어진 상태는 QA PASS가 아니다. 실제 QA 결과는 명령·입력·환경과
함께 해당 Task에 따로 기록한다.

#### Troubleshooting

##### Symptoms

- `ensurepip` 또는 `pip`가 없다면 이미 설치된 `uv`의 동일 hash lock 설치
  경로를 사용하거나 환경 담당에게 도구 준비를 요청한다.
- hash 또는 wheel 설치가 실패하면 lock·Python·플랫폼의 조합을 확인한다.
  hash 검사를 끄거나 다른 미고정 의존성을 섞지 않는다.
- `HOOK-ENV`는 Git option 누락, checkout 안의 환경, 실행 파일 누락,
  소유자 또는 mode 불일치 중 하나를 뜻한다. 정확한 조건은
  [Git Policy](../03.process/git.md)가 소유한다.
- `STYLE-TOOL`/`NONSTYLE-TOOL`은 선택한 Python의 `pre_commit` module
  부재 등을 확인할 신호다. QA의 자세한 진단은
  [scripts README](../../../scripts/README.md)를 따른다.

##### Next Action

환경 오류가 있으면 해당 검증을 실패 또는 미실행으로 기록하고 환경을
재구성한 뒤 같은 입력으로 다시 검사한다. 권한·설정·live 접근 문제가 있으면
그 대상 작업만 중단하고 [Approval and Safety Policy](../04.quality/approval-and-safety.md)의
담당자에게 넘긴다. 문서나 합성 검사의 성공을 native 실행 관측으로 대체하지 않는다.

##### Lifecycle Traceability

| Promoted owner | Audience outcome | Operating surface |
| --- | --- | --- |
| [SPEC-0223 Task](../../03.specs/0223-work-residue-handoff/01.tasks/tsk-0001-work-residue-handoff.md) | 현재 P03 요청에 따라 개발자와 검증 담당자가 동일 lock과 실제 interpreter identity로 로컬 검증 환경을 준비한다. 원래 Spec·Plan의 승인 범위와 이번 요청의 실행 권한은 Task에서 구분한다. | 이 checkout의 로컬 Python 검증 환경과 Git hook 연결 전 준비 |

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
