---
title: "Agent Responsibilities"
version: "2.2.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-13"
---
# Agent Responsibilities

## Overview

작업에 필요한 책임을 먼저 고른 뒤, [agent registry](registry.json)에서 중립
역할을 찾고 선택한 provider의 구체 값은
[Codex bindings](../../.codex/bindings.json) 또는
[Claude bindings](../../.claude/bindings.json)에서 가져온다. 역할 projection은
이 값을 소비하며 검증을 받는 native 소비자다.
이 라우터는 역할 명단이나 권한 목록의 사본이 아니다.

## Scope

책임은 도메인 경계를 설명할 뿐이다. 실제로 허용되는 동작은 registry 권한과
명시적인 Task 소유권이 정한다. 검토 관점은 쓰기 권한이 아니다.

아래 일곱 경계는 별도 문서가 아니라 이 라우터의 절이다. 구체 역할 본문은 자기
guardrail·입력·출력·인계를 소유하고, 이 문서는 각 역할이 맥락으로 읽는 도메인
경계만 담는다.

### Architecture

시스템 구조와 중요한 결정을 지속 요구사항 및 변경별 계약과 일관되게 유지한다.
Architecture Description과 ADR은 구조 관점과 지속 선택을, Spec은 변경별 동작을
소유한다. 이 경계는 인프라 매니페스트도, 공통 거버넌스 정책도 소유하지 않는다.

- 구조 변경은 완결된 Requirement Package ID와 영향받는 Spec까지 추적한다.
- 승인된 결정을 바꿀 때는 후속 ADR을 쓴다. 대체된 ADR은 다른 family와 마찬가지로
  자기 처분 승인에 따라 Stage 02에서 `superseded/`로 옮긴다.
- 구현·운영·보안 영향은 각 책임 소유자에게 넘긴다. 모든 문서의 소유권을
  주장하지 않는다.

이 경계는 [architect](architect.md)가 맡는다.

### Documentation

작성 문서와 탐색 경로가 유용하고 추적 가능하며 올바른 소유자로 연결되도록
유지한다. 이 경계는 공통 작성·탐색 관심사와 배정된 문서 편집을 다루며, 모든
단계 내용에 대한 권한은 아니다. 실질 결정은 각 단계 소유자에게, 정확한 양식은
Stage 99에 있다. 더는 현행이 아닌 전체 본문은 Stage 98이 보관하고 원본 객체는
Git 이력으로 복구한다.

- 선택한 profile과 template, 문서 언어 경계를 적용한다.
- 이동·삭제에 맞춰 현행 링크와 README 탐색을 함께 고친다.
- 도메인 주장은 그 소유자에게, 조사 공백은 근거 수집 담당에게 넘긴다. 없는
  출처를 만들어내지 않는다.
- 완료되었거나 봉인된 증거는 보존한다. 이력을 다시 쓰지 말고 승인된 이행 복구
  경로를 쓴다.

### Infrastructure

Kubernetes와 GitOps desired state를 재현 가능하고 격리된 상태로, 승인된 시스템
계약에 맞게 유지한다. 배정된 범위의 구현은 지정된 인프라·GitOps 매니페스트와 그
자동화를 다룰 수 있고, 검토 역할은 읽기 전용이다. 이 경계는 live 변경 권한을
주지 않으며 상위 요구사항이나 거버넌스를 소유하지 않는다. 로컬 클러스터 자산은
`infrastructure/` 아래에 있고 reconciliation은
`gitops/clusters/local/root-application.yaml`에서 시작한다.

- secret 참조의 안전한 처리와 네트워크 격리를 유지한다.
- 영향받는 매니페스트의 구문·정책·reconciliation 구조를 저장소 검사로 확인한다.
- 운영 영향과 rollback은 소유 Plan 또는 Task에 기록하고 runbook 변경은 운영
  담당에게 넘긴다.
- 클러스터 기동과 reconciliation은 명시적 승인 아래 운영자가 수행한다.

### Operations

안전한 운영 절차, 복구 가능성, 장애 증거, 에스컬레이션을 보존한다. 이 경계는
배정된 운영 정책, runbook, 장애 지식을 소유한다. GitOps desired state나 live
서비스 변경 권한은 없으며 그런 변경은 해당 소유자와 승인이 필요하다. Guide는
사용법을, Policy는 운영 통제를, Runbook은 순서 있는 절차를, Incident 기록은
사실과 학습을 담는다. 별도의 release-record family는 만들지 않는다.

- 제안하는 운영 조치를 정책, Spec 또는 장애 맥락에 연결한다.
- 전제 조건, 영향, 확인 방법, rollback 또는 복구, 책임 운영자를 적는다.
- 승인된 관측, 권고 확인 항목, 실행하지 않은 조치를 구분한다.
- 지속적인 교정 조치는 소유자가 있는 요구사항, 결정, Spec 또는 운영 문서
  갱신으로 바꾼다.

### Quality

수용 기준을 재현 가능한 검사에 연결하고 실패, 한계, 회귀 위험을 보고한다. QA의
쓰기 범위는 registry 권한과 위임 범위가 정한다. QA는 배정된 테스트, fixture,
Python 검증기, validation-lane 내용을 작성할 수 있지만 제품, 매니페스트, 보안
승인, shell 검증기, 정책의 소유권은 얻지 않는다. CI trigger, 권한, concurrency,
lane 밖 job은 거버넌스가 소유한다.

- 의미 규칙 family에서 양성 사례와 독립적인 음성 사례를 도출한다.
- 복사한 대규모 fixture 행렬보다 범위가 정해진 mutation 테스트를 선호한다.
- 기대 결과와 관측 결과를 수용 ID에 연결하고 독립 구현 검토를 유지한다.
- 문서, 보안, 소유자 없는 구현 변경은 각 소유자에게 넘긴다. lane과 결과의
  의미는 quality policy를 따른다.

### Security

승인된 계약에 비추어 secret 노출, 접근 통제, 격리, 안전하지 않은 실행을
검토한다. 선택된 registry 역할이 읽기 전용이면 보안 검토도 읽기 전용이다. 발견
사항은 수정, live 조사, secret 접근, 더 넓은 파일 소유권을 허가하지 않는다.
저장소 정책, 매니페스트 참조, Spec, 승인된 비식별 장애 증거를 사용하고, 발견을
입증하려고 자격 증명이나 secret 값을 열람하지 않는다.

- 보안 영향이 있는 발견은 근거와 구체적인 실패 또는 위험에 연결한다.
- 권한 상승, 네트워크 격리, 신뢰할 수 없는 입력, 명령 경계, 데이터 보존을
  검토한다.
- 수정은 권한 있는 구현 소유자에게 넘기고 미해결 위험이나 필요한 운영자 조치를
  기록한다.
- 반복되는 장애 교훈은 과거 사실을 고쳐 쓰지 않고 지속 통제로 연결한다.

### Supervision

승인된 작업을 조정하고 소유권, 의존성, 검토, 증거를 대조한다. supervisor의
registry 권한 등급은 authoring이 아니라 orchestration이다. 거버넌스 유지보수에는
범위가 명시된 작성 소유자가 따로 필요하며, 작업 배정이 worker에게 새 도구나 쓰기
경로를 주지는 않는다. 사람용 정책은 공통 거버넌스가, 역할 명단과 인계는 중립
registry가, native 설정은 provider binding 표가 소유하고 projection은 검증받는
소비자다.

- 파일 책임과 의존성이 명시된 범위 있는 작업으로 나눈다.
- 기존 registry 역할과 skill을 고른다. 추측성 공백을 이유로 명단을 늘리지 않는다.
- 독립 검토를 유지하고 의견 충돌이나 승인 필요 사항은 사람에게 넘긴다.
- 돌아온 결과를 수용 기준과 현재 저장소 증거에 대조한 뒤 최종 인계한다.

## Structure

정규 역할 본문:

- [supervisor](supervisor.md)
- [architect](architect.md)
- [governance-steward](governance-steward.md)
- [ci-workflow-engineer](ci-workflow-engineer.md)
- [repo-tooling-engineer](repo-tooling-engineer.md)
- [agent-evaluator](agent-evaluator.md)
- [code-reviewer](code-reviewer.md)
- [doc-writer](doc-writer.md)
- [gitops-reviewer](gitops-reviewer.md)
- [incident-responder](incident-responder.md)
- [k8s-implementer](k8s-implementer.md)
- [network-reviewer](network-reviewer.md)
- [observability-reviewer](observability-reviewer.md)
- [security-auditor](security-auditor.md)
- [wiki-curator](wiki-curator.md)
- [docs-researcher](docs-researcher.md)
- [quality-engineer](quality-engineer.md)

## Usage

관련된 책임 소유자만 읽는다. 제품 의도는 Requirement Package에, backend와 API
동작은 Spec과 그 구현 Task에 있다. 이 인프라 작업 공간에서는 쓰이지 않는 독립
agent 범위로 이런 일반 의무를 따로 둘 필요가 없다.

역할이나 skill은 승인된 구체적 공백이 있을 때만 중립 registry와 검토된
projection을 통해 추가한다. 새 역할 본문은 `status: "draft"`로 만들고 이후의
별도 논리 변경에서 `active`로 올린다. `governance/role` lifecycle domain은 생성을
`draft`로만 허용하고, `active`에서 되돌아가는 edge가 없으며, 삭제는 고정된
migration 기록으로만 허용한다. 처음부터 `active`로 커밋한 본문은 앞으로 고칠 수
없으므로 그 커밋 전에 staged 검증 결과를 읽는다. 작업이 도메인을 넘을 때는 소유권
전환을 선언하고, 경계가 불분명하거나 충돌하면 에스컬레이션한다.

증거와 인계는 [quality policy](../governance/quality.md)에 따라 기록한다. 활성
Task의 범위가 바뀌면 책임을 다시 판단한다. 정확한 역할, 권한, skill, 인계
구성은 agent registry에 있다.

## Related Documents

- [Governance Hub](../README.md)
- [SDLC Flow](../governance/sdlc.md)
- [Delegated Development](../workflows/delegated-development.md)
- [Approval and Safety](../governance/approval-and-safety.md)
- [Document Authoring](../governance/document-authoring.md)
- Architecture Index (`docs/02.architecture/README.md`)
- Operations Index (`docs/05.operations/README.md`)
