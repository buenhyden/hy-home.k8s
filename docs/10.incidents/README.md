# 10.incidents

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## 목적

이 폴더는 사고 사실 기록(Incident Record)과 사고 후 회고(Postmortem)를 저장한다.
Incident는 실시간 또는 최근 종료된 대응 흐름을 기록하는 문서이고, Postmortem은 시스템이 왜 그런 사고를 허용했는지와 무엇을 바꿔야 재발 가능성을 줄일 수 있는지를 기록한다.

## 문서 책임

- 영향과 상태를 기록한다.
- 타임라인과 대응 조치를 기록한다.
- 증거와 후속 액션을 연결한다.
- 사실과 가설을 구분해 남긴다.

## 포함할 내용

### Incident Record

- Incident ID
- 영향 범위
- 타임라인
- 현재 가설
- 대응 및 완화 조치
- 증거
- 후속 액션
- 관련 Runbook / Postmortem 링크

### Postmortem

- 사건 요약
- 영향
- 타임라인
- 근본 원인
- 기여 요인
- 감지 공백
- 액션 아이템
- 재발 방지와 검증
- 관련 Incident / Runbook / ADR / Spec / Operation 링크

## 포함하지 말아야 할 내용

- 일반 운영 정책
- 실행 절차 중심 런북
- 기능 요구사항 또는 상세 설계

위 내용은 각각 `08.operations/`, `09.runbooks/`, `01.prd/`, `04.specs/`로 분리한다.

## Agent 사고 시 추가 메타데이터

- Model Version
- Prompt Version
- Tool Set / Config
- Guardrail State
- Trace IDs
- Eval Run IDs

## 권장 하위 구조

- `10.incidents/YYYY/YYYY-MM-DD-<incident-title>.md`
- `10.incidents/postmortems/YYYY/YYYY-MM-DD-<incident-title>.md`

## Templates

- `../99.templates/incident.template.md`
- `../99.templates/postmortem.template.md`

## 관련 폴더

- `08.operations/`: 운영 정책과 통제 기준
- `09.runbooks/`: 실행 가능한 복구 절차
- `99.templates/`: Incident/Postmortem 템플릿

## 예시

- 장애 대응 중에는 `10.incidents/2026/2026-05-09-argocd-sync-delay.md`를 작성한다.
- 사고 종료 후 구조 분석이 필요하면 `10.incidents/postmortems/2026/2026-05-09-argocd-sync-delay.md`를 작성한다.
