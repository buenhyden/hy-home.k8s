---
title: "00.workspace"
version: "0.3.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---
# 00.workspace

## Responsibility

### Purpose

> 사람과 에이전트가 함께 따르는 작업 시스템 기준(W 계층)의 정본 stage다.

`00.workspace/`는 이 저장소에서 일하는 방식 자체를 소유한다. 범위와 공통
어휘, 작업 시스템 구조, 개발·문서·Git 절차, 품질·승인 기준, 반복 유지보수
절차가 여기에 있다. 책임 계층의 정의는 SDLC 정책(`03.process/sdlc.md`)의
SDLC-R036이 소유하며, 2026-11-19 경로 전환으로 W 계층 문서가 이곳으로 옮겨졌다.

#### Inputs and Outputs

##### In Scope

- 공통 어휘(TERM)와 프로젝트 범위의 진입점
- 작업 시스템(문서·역할·QA Registry, 도구, CI) 구조와 지속 결정
- SDLC, 문서 작성·수명주기, Git, 저장소 전달 절차
- 품질·형식·승인과 보호 행위 기준, QA 안내
- 재현 가능한 로컬 검증 환경 준비 안내
- 참고 자료와 도구의 반복 유지보수 절차

##### Out of Scope

- 제품(k8s GitOps 플랫폼) 요구·구조·운영 문서
- 에이전트 실행 절차, 역할, Skill과 제공자 설정
- 요청별 Spec·Plan·Task와 실행 증거

### Excluded Responsibilities

제품 요구는 [`../01.requirements/`](../01.requirements/), 제품 구조와 결정은
[`../02.architecture/`](../02.architecture/), 제품 운영은
[`../05.operations/`](../05.operations/)가 소유한다. 에이전트의 실행 차이(A 계층)는
[`.agents/`](../../.agents/), 제공자 고유 값은 `.claude/`와 `.codex/`,
문서 형식·profile·양식은 [`../99.templates/`](../99.templates/)가 소유한다.
이 stage는 그 내용을 복사하지 않고 링크한다.

## Current Contents

### Paths

| Path | Purpose |
| --- | --- |
| [01.project/](./01.project/) | 범위·소유 정본(SDLC-R036, REQ-0003)으로 가는 진입점과 K8s 로컬 용어 정본 |
| [02.architecture/](./02.architecture/) | 작업 시스템 Architecture Description(AD-0006)과 작업 시스템 ADR. 제품 플랫폼 구조와 결정은 `docs/02.architecture/` |
| [03.process/](./03.process/) | SDLC·문서 작성·문서 수명주기·Git 정책과 main 릴리스 준비 Runbook(RUN-0012) |
| [04.quality/](./04.quality/) | 품질·형식·승인과 안전 정책과 CI/CD QA 안내(GDE-0010) |
| [05.environment/](./05.environment/) | checkout 밖의 잠긴 로컬 검증 환경 준비 안내(GDE-0011) |
| [06.maintenance/](./06.maintenance/) | 참고 자료 유지보수 Runbook(RUN-0011) |
| [AGENTS.md](./AGENTS.md) | 이 stage에 적용되는 AI 에이전트 지시 |
| [CLAUDE.md](./CLAUDE.md) | Claude가 이 stage의 `AGENTS.md`를 불러오게 하는 한 줄 `@AGENTS.md` import |

### Owners

#### Reader Route

| 찾는 것 | 먼저 볼 위치 | 판단 기준 |
| --- | --- | --- |
| 범위·소유·로컬 용어 | [01.project](./01.project/README.md) | 책임 계층은 SDLC-R036, 장기 요구는 REQ-0003, K8s 로컬 용어는 이 영역의 glossary가 소유한다. |
| 공통 작업·거버넌스 용어 | [Repository Vocabulary](../../.agents/knowledge/glossary.md) | 공통 의미의 정본이며 각 정책은 운영 규칙을 소유한다. |
| 작업 시스템 구성·결정 | [02.architecture](./02.architecture/README.md) | AD-0006과 작업 시스템 ADR. 제품 결정과 섞지 않는다. |
| 변경의 단계와 완료 기준 | [SDLC](03.process/sdlc.md), 04.quality의 quality 정책 | 단계는 SDLC, 완료와 검증은 quality가 소유한다. |
| 보호 행위와 승인 | [approval and safety](04.quality/approval-and-safety.md) | 에이전트의 실행 직전 확인은 [agent safety execution](../../.agents/governance/approval-and-safety.md)이 소유한다. |
| 로컬 검증 환경 준비 | [05.environment](./05.environment/README.md) | lock과 실제 interpreter identity로 checkout 밖의 환경을 준비한다. lock은 `.github/requirements/`가 소유한다. |
| 검증 선택·결과 | [04.quality](./04.quality/README.md)와 [scripts README](../../scripts/README.md) | quality는 의무와 판정, scripts는 실행 진입점을 소유한다. |

## Usage

### Entry Points

1. 일하는 방식 자체를 바꿀 때는 해당 정책을 개정하고 규칙 ID를 유지한다.
2. 하나의 규칙 ID는 한 문서만 소유한다. W와 A로 나뉜 SAFE·GIT 규칙의 소유는
   `docs/99.templates/registry.json`의 `policy_rule_ids` 기록이 나열한다.
3. 새 분류 폴더는 실제 문서가 생길 때만 만든다.

#### Upstream and Downstream

- [Docs README](../README.md)
- [Requirements README](../01.requirements/README.md)
- [Specs README](../03.specs/README.md)
- [Agents README](../../.agents/README.md)

#### Policy and Templates

- Document Authoring (`03.process/document-authoring.md`)
- [Templates README](../99.templates/README.md)

### Checks

문서 상태 전이와 처분은 문서 수명주기 정책(`03.process/document-lifecycle.md`)을 따른다.
