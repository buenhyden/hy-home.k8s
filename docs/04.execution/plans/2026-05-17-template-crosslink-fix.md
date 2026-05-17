---
title: 'Template Cross-link Fix Implementation Plan'
type: plan
status: active
owner: 'platform-team'
updated: 2026-05-17
---

# Template Cross-link Fix Implementation Plan

> Use this plan to fix relative path placeholders in all `docs/99.templates/` files and
> to synchronise the display text (backtick code) in every generated document with its
> actual href.
>
> **For agentic workers:** Execute each `- [ ]` step in order. Use `superpowers:executing-plans`
> or `superpowers:subagent-driven-development` to implement task-by-task.

---

# Template Cross-link Fix Plan

## Overview (KR)

이 계획은 `docs/99.templates/` 템플릿 파일들의 Cross-link 플레이스홀더 경로를 Target 위치 기준 올바른 상대 경로로 수정하고,
이미 생성된 문서의 표시 텍스트(backtick 코드)를 실제 href와 일치시키는 작업을 정의한다.

현재 문제: 템플릿의 `Related Documents` 플레이스홀더가 `../` 한 단계 이동을 기준으로 작성되었으나,
대부분의 Target 위치(`decisions/`, `tasks/`, `runbooks/` 등)는 `docs/` 루트까지 2단계 이상 이동이 필요하다.
생성된 파일들의 실제 href는 올바르지만, 표시 텍스트(backtick)가 잘못된 플레이스홀더를 그대로 복사하여 불일치 상태다.

## Context

분석 결과:

- `spec.template.md`와 `prd.template.md`는 이미 올바른 상대 경로를 사용함 (변경 불필요)
- 나머지 10개 템플릿은 `../`을 `../../`로 또는 형제 디렉터리 상대 경로로 수정 필요
- 생성된 파일 약 30개의 표시 텍스트가 실제 href와 불일치 (링크 동작은 정상)
- 각 Template의 `<!-- Target: ... -->` 주석이 올바른 Target 위치를 명시하고 있으므로 이를 기준으로 상대 경로 계산

경로 계산 원칙:

- `docs/02.architecture/decisions/` → `docs/` 루트까지 `../../` 필요
- `docs/04.execution/tasks/` → `docs/` 루트까지 `../../` 필요, 형제 `plans/`는 `../plans/`
- `docs/05.operations/runbooks/` → `docs/` 루트까지 `../../`, 형제 `guides/`, `policies/`는 `../`
- `docs/05.operations/incidents/YYYY/` → `05.operations/`까지 `../../`, `docs/` 루트까지 `../../../`
- `docs/05.operations/incidents/postmortems/YYYY/` → `05.operations/`까지 `../../../`

## Goals & In-Scope

- **Goals**:
  - 10개 템플릿의 Cross-link 플레이스홀더를 Target 위치 기준 올바른 상대 경로로 수정
  - 30개 이상 생성 파일의 표시 텍스트(backtick 코드)를 실제 href와 일치시킴
- **In Scope**:
  - `docs/99.templates/` 내 Cross-link가 있는 10개 템플릿 파일
  - `docs/02.architecture/decisions/*.md` (ADR 9개)
  - `docs/02.architecture/requirements/*.md` (ARD 3개)
  - `docs/04.execution/plans/*.md` (Plan 6개)
  - `docs/04.execution/tasks/*.md` (Task 6개)
  - `docs/05.operations/guides/*.md` (Guide 5개 — 링크 불일치 있는 것)
  - `docs/05.operations/runbooks/*.md` (Runbook 4개)

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - 실제 href 링크 경로 변경 (href는 이미 올바름)
  - 문서 내용(Content) 변경
  - `docs/03.specs/` 파일 수정 (spec 파일들의 링크는 이미 올바름)
  - `docs/01.requirements/` 파일 수정 (prd 파일들의 링크는 이미 올바름)
- **Out of Scope**:
  - `docs/05.operations/incidents/` — 현재 incident 파일 없음
  - `docs/90.references/` — 현재 reference 파일 없음
  - `docs/00.agent-governance/` 거버넌스 파일

## Work Breakdown

| Task | Description                        | Files / Docs Affected                            | Target REQ  | Validation Criteria                                                       |
| ---- | ---------------------------------- | ------------------------------------------------ | ----------- | ------------------------------------------------------------------------- |
| T-01 | adr.template.md 경로 수정          | `docs/99.templates/adr.template.md`              | REQ-TMP-001 | Related Documents의 4개 경로가 `../../` 또는 `../requirements/` 패턴 사용 |
| T-02 | ard.template.md 경로 수정          | `docs/99.templates/ard.template.md`              | REQ-TMP-001 | Related Documents의 4개 경로 수정                                         |
| T-03 | plan.template.md 경로 수정         | `docs/99.templates/plan.template.md`             | REQ-TMP-001 | Related Documents의 4개 경로 수정                                         |
| T-04 | task.template.md 경로 수정         | `docs/99.templates/task.template.md`             | REQ-TMP-001 | Inputs + Related Documents 5개 경로 수정                                  |
| T-05 | guide.template.md 경로 수정        | `docs/99.templates/guide.template.md`            | REQ-TMP-001 | Related Documents 3개 경로 수정                                           |
| T-06 | runbook.template.md 경로 수정      | `docs/99.templates/runbook.template.md`          | REQ-TMP-001 | Canonical References 4개 + Related Documents 3개 수정                     |
| T-07 | incident.template.md 경로 수정     | `docs/99.templates/incident.template.md`         | REQ-TMP-001 | Runbook Link 셀 + Related Documents 2개 수정                              |
| T-08 | postmortem.template.md 경로 수정   | `docs/99.templates/postmortem.template.md`       | REQ-TMP-001 | Incident Document 셀 + Related Documents 3개 수정                         |
| T-09 | operation.template.md 경로 수정    | `docs/99.templates/operation.template.md`        | REQ-TMP-001 | Related Documents 3개 수정                                                |
| T-10 | reference.template.md 경로 수정    | `docs/99.templates/reference.template.md`        | REQ-TMP-001 | Related Documents 2개 수정                                                |
| T-11 | ADR 생성 파일 표시 텍스트 수정     | `docs/02.architecture/decisions/000{1-9}*.md`    | REQ-GEN-001 | backtick 표시 텍스트가 href와 일치                                        |
| T-12 | ARD 생성 파일 표시 텍스트 수정     | `docs/02.architecture/requirements/000{1-3}*.md` | REQ-GEN-001 | backtick 표시 텍스트가 href와 일치                                        |
| T-13 | Plan 생성 파일 표시 텍스트 수정    | `docs/04.execution/plans/2026-*.md` (6개)        | REQ-GEN-001 | backtick 표시 텍스트가 href와 일치                                        |
| T-14 | Task 생성 파일 표시 텍스트 수정    | `docs/04.execution/tasks/2026-*.md` (6개)        | REQ-GEN-001 | backtick 표시 텍스트가 href와 일치                                        |
| T-15 | Guide 생성 파일 표시 텍스트 수정   | `docs/05.operations/guides/000{1-4,8}*.md`       | REQ-GEN-001 | backtick 표시 텍스트가 href와 일치                                        |
| T-16 | Runbook 생성 파일 표시 텍스트 수정 | `docs/05.operations/runbooks/000{1-4}*.md`       | REQ-GEN-001 | backtick 표시 텍스트가 href와 일치                                        |
| T-17 | 최종 통합 검증                     | 전체 docs/                                       | REQ-VAL-001 | 스캔 명령 출력 없음                                                       |

## Verification Plan

| ID          | Level      | Description                       | Command / How to Run                                                                                                     | Pass Criteria                                                                                |
| ----------- | ---------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- |
| VAL-PLN-001 | Structural | 템플릿 경로 패턴 확인             | `grep -n "Related Documents" -A 6 docs/99.templates/adr.template.md`                                                     | `../../01.requirements/`, `../requirements/`, `../../03.specs/`, `../../04.execution/plans/` |
| VAL-PLN-002 | Structural | 생성 파일 불일치 스캔             | `grep -rn "\x60\.\./0[0-9]\." docs/ --include="*.md" \| grep -v "99.templates"`                                          | 출력 없음                                                                                    |
| VAL-PLN-003 | Structural | 생성 파일 05.operations 경로 스캔 | `grep -rn "\x60\.\./05\.operations/" docs/ --include="*.md" \| grep -v "99.templates"`                                   | 출력 없음                                                                                    |
| VAL-PLN-004 | Content    | 실제 파일 존재 확인               | `ls docs/02.architecture/requirements/0001-wsl-k3d-argocd-platform.md docs/03.specs/001-wsl-k3d-argocd-platform/spec.md` | 두 파일 모두 존재                                                                            |

## Risks & Mitigations

| Risk                                 | Impact | Mitigation                                                      |
| ------------------------------------ | ------ | --------------------------------------------------------------- |
| 표시 텍스트 수정 중 href 실수로 변경 | High   | Edit 도구의 old_string/new_string을 표시 텍스트만 정확히 타겟팅 |
| 파일 수가 많아 일부 누락             | Medium | Task 17 통합 검증 스캔으로 전수 확인                            |
| hook이 다른 품질 게이트 위반 감지    | Low    | 각 Task 완료 후 즉시 검증 명령 실행                             |

## Completion Criteria

- [ ] 10개 템플릿 파일의 Cross-link 플레이스홀더가 Target 위치 기준 올바른 상대 경로 사용
- [ ] 30개 이상 생성 파일의 표시 텍스트(backtick)가 실제 href와 일치
- [ ] `grep -rn "\x60\.\./0[0-9]\." docs/ --include="*.md" | grep -v "99.templates"` 출력 없음
- [ ] `grep -rn "\x60\.\./05\.operations/" docs/ --include="*.md" | grep -v "99.templates"` 출력 없음
- [ ] `docs/00.agent-governance/memory/progress.md`에 작업 완료 entry 추가

## Related Documents

- **Templates**: [`../../99.templates/README.md`](../../99.templates/README.md)
- **Documentation Protocol**: [`../../00.agent-governance/rules/documentation-protocol.md`](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Authoring Matrix**: [`../../00.agent-governance/rules/stage-authoring-matrix.md`](../../00.agent-governance/rules/stage-authoring-matrix.md)

---

## Task Detail: 각 Task별 상세 실행 지침

> 이 섹션은 Work Breakdown 표의 각 Task를 단계별로 실행하기 위한 상세 지침이다.
> `superpowers:executing-plans` 또는 `superpowers:subagent-driven-development`로 실행한다.

### T-01: adr.template.md 수정

Target: `docs/02.architecture/decisions/####-<short-title>.md`

경로 계산:

- `decisions/` → `../` → `02.architecture/` → `../../` → `docs/`
- PRD (`01.requirements/`): `../../01.requirements/`
- ARD (`requirements/`): `../requirements/` (형제 디렉터리)
- Spec (`03.specs/`): `../../03.specs/`
- Plan (`04.execution/plans/`): `../../04.execution/plans/`

- [ ] **Step 1: adr.template.md Related Documents 수정**

`docs/99.templates/adr.template.md` 라인 67-71을 다음으로 교체:

```
- **PRD**: `[../../01.requirements/YYYY-MM-DD-<feature-or-system>.md]`
- **ARD**: `[../requirements/####-<system-or-domain>.md]`
- **Spec**: `[../../03.specs/<feature-id>/spec.md]`
- **Plan**: `[../../04.execution/plans/YYYY-MM-DD-<feature>.md]`
- **Related ADR**: `[./####-<related-decision>.md]`
```

- [ ] **Step 2: 검증**

```bash
grep -n "Related Documents" -A 6 docs/99.templates/adr.template.md
```

기대 결과: `../../01.requirements/`, `../requirements/`, `../../03.specs/`, `../../04.execution/plans/` 포함

---

### T-02: ard.template.md 수정

Target: `docs/02.architecture/requirements/####-<system-or-domain>.md`

경로 계산:

- `requirements/` → `../` → `02.architecture/` → `../../` → `docs/`
- PRD: `../../01.requirements/`
- Spec: `../../03.specs/`
- Plan: `../../04.execution/plans/`
- ADR: `../decisions/` (형제 디렉터리)

- [ ] **Step 1: ard.template.md Related Documents 수정**

`docs/99.templates/ard.template.md` 라인 75-78을 다음으로 교체:

```
- **PRD**: `[../../01.requirements/YYYY-MM-DD-<feature-or-system>.md]`
- **Spec**: `[../../03.specs/<feature-id>/spec.md]`
- **Plan**: `[../../04.execution/plans/YYYY-MM-DD-<feature>.md]`
- **ADR**: `[../decisions/####-<short-title>.md]`
```

- [ ] **Step 2: 검증**

```bash
grep -n "Related Documents" -A 5 docs/99.templates/ard.template.md
```

---

### T-03: plan.template.md 수정

Target: `docs/04.execution/plans/YYYY-MM-DD-<feature>.md`

경로 계산:

- `plans/` → `../` → `04.execution/` → `../../` → `docs/`
- PRD: `../../01.requirements/`
- ARD: `../../02.architecture/requirements/`
- Spec: `../../03.specs/`
- ADR: `../../02.architecture/decisions/`

- [ ] **Step 1: plan.template.md Related Documents 수정**

`docs/99.templates/plan.template.md` 라인 76-79를 다음으로 교체:

```
- **PRD**: `[../../01.requirements/YYYY-MM-DD-<feature-or-system>.md]`
- **ARD**: `[../../02.architecture/requirements/####-<system-or-domain>.md]`
- **Spec**: `[../../03.specs/<feature-id>/spec.md]`
- **ADR**: `[../../02.architecture/decisions/####-<short-title>.md]`
```

- [ ] **Step 2: 검증**

```bash
grep -n "Related Documents" -A 5 docs/99.templates/plan.template.md
```

---

### T-04: task.template.md 수정

Target: `docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md`

경로 계산:

- `tasks/` → `../` → `04.execution/` → `../../` → `docs/`
- Spec: `../../03.specs/`
- Plan (형제 `plans/`): `../plans/`
- Tests: `../../03.specs/<feature-id>/tests.md`

- [ ] **Step 1: task.template.md Inputs 섹션 수정**

`docs/99.templates/task.template.md` Inputs 섹션(라인 30-32 근처)을 다음으로 교체:

```
## Inputs

- **Parent Spec**: `[../../03.specs/<feature-id>/spec.md]`
- **Parent Plan**: `[../plans/YYYY-MM-DD-<feature>.md]`
```

- [ ] **Step 2: task.template.md Related Documents 섹션 수정**

`docs/99.templates/task.template.md` Related Documents 섹션(라인 80-83 근처)을 다음으로 교체:

```
## Related Documents

- **Spec**: `[../../03.specs/<feature-id>/spec.md]`
- **Plan**: `[../plans/YYYY-MM-DD-<feature>.md]`
- **Tests**: `[../../03.specs/<feature-id>/tests.md]`
```

- [ ] **Step 3: 검증**

```bash
grep -n "Inputs\|Related Documents" -A 4 docs/99.templates/task.template.md
```

---

### T-05: guide.template.md 수정

Target: `docs/05.operations/guides/####-<topic>.md`

경로 계산:

- `guides/` → `../` → `05.operations/` → `../../` → `docs/`
- Spec: `../../03.specs/`
- Operation (형제 `policies/`): `../policies/`
- Runbook (형제 `runbooks/`): `../runbooks/`

- [ ] **Step 1: guide.template.md Related Documents 수정**

`docs/99.templates/guide.template.md` 라인 61-63을 다음으로 교체:

```
- **Spec**: `[../../03.specs/<feature-id>/spec.md]`
- **Operation**: `[../policies/<policy-or-standard>.md]`
- **Runbook**: `[../runbooks/<topic>.md]`
```

- [ ] **Step 2: 검증**

```bash
grep -n "Related Documents" -A 4 docs/99.templates/guide.template.md
```

---

### T-06: runbook.template.md 수정

Target: `docs/05.operations/runbooks/####-<topic>.md`

경로 계산:

- `runbooks/` → `../` → `05.operations/` → `../../` → `docs/`
- ARD: `../../02.architecture/requirements/`
- ADR: `../../02.architecture/decisions/`
- Spec: `../../03.specs/`
- Plan: `../../04.execution/plans/`
- incidents (형제): `../incidents/YYYY/`
- postmortems (형제): `../incidents/postmortems/YYYY/`
- policies (형제): `../policies/`

- [ ] **Step 1: runbook.template.md Canonical References 수정**

`docs/99.templates/runbook.template.md` 라인 36-39를 다음으로 교체:

```
- `[../../02.architecture/requirements/####-<system-or-domain>.md]`
- `[../../02.architecture/decisions/####-<short-title>.md]`
- `[../../03.specs/<feature-id>/spec.md]`
- `[../../04.execution/plans/YYYY-MM-DD-<feature>.md]`
```

- [ ] **Step 2: runbook.template.md Related Documents 수정**

`docs/99.templates/runbook.template.md` 라인 83-85를 다음으로 교체:

```
- **Incident examples**: `[../incidents/YYYY/YYYY-MM-DD-<incident-title>.md]`
- **Postmortem examples**: `[../incidents/postmortems/YYYY/YYYY-MM-DD-<incident-title>.md]`
- **Operation**: `[../policies/<policy-or-standard>.md]`
```

- [ ] **Step 3: 검증**

```bash
grep -n "Canonical References\|Related Documents" -A 5 docs/99.templates/runbook.template.md
```

---

### T-07: incident.template.md 수정

Target: `docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident-title>.md`

경로 계산 (Target: `docs/05.operations/incidents/YYYY/`):

- `YYYY/` → `../` → `incidents/` → `../../` → `05.operations/` → `../../../` → `docs/`
- runbooks (형제): `../../runbooks/`
- policies: `../../policies/`
- postmortems: `../postmortems/YYYY/`

- [ ] **Step 1: incident.template.md Runbook Link 테이블 셀 수정**

`docs/99.templates/incident.template.md` 라인 39의 테이블 셀에서
`../../05.operations/runbooks/####-<topic>.md` → `../../runbooks/####-<topic>.md`

- [ ] **Step 2: incident.template.md Related Documents 수정**

`docs/99.templates/incident.template.md` 라인 83-84를 다음으로 교체:

```
- **Runbook**: `[../../runbooks/####-<topic>.md]`
- **Operation**: `[../../policies/<policy-or-standard>.md]`
```

- [ ] **Step 3: 검증**

```bash
grep -n "Runbook Link\|Related Documents" -A 5 docs/99.templates/incident.template.md
```

---

### T-08: postmortem.template.md 수정

Target: `docs/05.operations/incidents/postmortems/YYYY/YYYY-MM-DD-<incident-title>.md`

경로 계산 (Target: `docs/05.operations/incidents/postmortems/YYYY/`):

- `YYYY/` → `../` → `postmortems/` → `../../` → `incidents/` → `../../../` → `05.operations/`
- Incident (형제 `incidents/YYYY/`): `../../YYYY/`
- runbooks: `../../../runbooks/`
- policies: `../../../policies/`

- [ ] **Step 1: postmortem.template.md Incident Document 테이블 셀 수정**

`docs/99.templates/postmortem.template.md` 라인 29의 테이블 셀에서
`../../05.operations/incidents/YYYY/YYYY-MM-DD-<incident-title>.md`
→ `../../YYYY/YYYY-MM-DD-<incident-title>.md`

- [ ] **Step 2: postmortem.template.md Related Documents 수정**

`docs/99.templates/postmortem.template.md` 라인 97-99를 다음으로 교체:

```
- **Runbook**: `[../../../runbooks/####-<topic>.md]`
- **Operation**: `[../../../policies/<policy-or-standard>.md]`
- **Incident**: `[../../YYYY/YYYY-MM-DD-<incident-title>.md]`
```

- [ ] **Step 3: 검증**

```bash
grep -n "Incident Document\|Related Documents" -A 5 docs/99.templates/postmortem.template.md
```

---

### T-09: operation.template.md 수정

Target: `docs/05.operations/policies/<policy-or-standard>.md`

경로 계산:

- `policies/` → `../` → `05.operations/` → `../../` → `docs/`
- ARD: `../../02.architecture/requirements/`
- runbooks (형제): `../runbooks/`
- incidents/postmortems (형제): `../incidents/postmortems/YYYY/`

- [ ] **Step 1: operation.template.md Related Documents 수정**

`docs/99.templates/operation.template.md` 라인 65-67을 다음으로 교체:

```
- **ARD**: `[../../02.architecture/requirements/####-<system-or-domain>.md]`
- **Runbook**: `[../runbooks/####-<topic>.md]`
- **Postmortem**: `[../incidents/postmortems/YYYY/YYYY-MM-DD-<incident-title>.md]`
```

- [ ] **Step 2: 검증**

```bash
grep -n "Related Documents" -A 4 docs/99.templates/operation.template.md
```

---

### T-10: reference.template.md 수정

Target: `docs/90.references/<category>/<item>.md`

경로 계산:

- `<item>/` → `../` → `<category>/` → `../../` → `docs/`
- ARD: `../../02.architecture/requirements/`
- Spec: `../../03.specs/`

- [ ] **Step 1: reference.template.md Related Documents 수정**

`docs/99.templates/reference.template.md` 라인 61-62를 다음으로 교체:

```
- **ARD**: `[../../02.architecture/requirements/####-<system-or-domain-name>.md]`
- **Spec**: `[../../03.specs/<feature-id>/spec.md]`
```

- [ ] **Step 2: 검증**

```bash
grep -n "Related Documents" -A 3 docs/99.templates/reference.template.md
```

---

### T-11: ADR 생성 파일 표시 텍스트 수정

**대상 패턴:** `docs/02.architecture/decisions/`에서의 올바른 표시 텍스트

| 현재 잘못된 표시 텍스트                        | 올바른 표시 텍스트                      |
| ---------------------------------------------- | --------------------------------------- |
| `` `../01.requirements/<file>` ``              | `` `../../01.requirements/<file>` ``    |
| `` `../02.architecture/requirements/<file>` `` | `` `../requirements/<file>` ``          |
| `` `../03.specs/<path>` ``                     | `` `../../03.specs/<path>` ``           |
| `` `../04.execution/plans/<file>` ``           | `` `../../04.execution/plans/<file>` `` |

- [ ] **Step 1: 0001-k3d-topology-and-network.md Related Documents 수정 (라인 68-71)**

```markdown
- **PRD**: [`../../01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../../01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **ARD**: [`../requirements/0002-wsl2-k3d-argocd-ha-platform.md`](../requirements/0002-wsl2-k3d-argocd-ha-platform.md)
- **Spec**: [`../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Related ADR**: [`./0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](./0005-wsl2-ha-baseline-and-external-endpoint-contract.md)
```

- [ ] **Step 2: 0002-argocd-helm-and-gitops-model.md Related Documents 수정 (라인 49-53)**

```markdown
- **PRD**: [`../../01.requirements/2026-03-27-wsl-k3d-argocd-platform.md`](../../01.requirements/2026-03-27-wsl-k3d-argocd-platform.md)
- **ARD**: [`../requirements/0001-wsl-k3d-argocd-platform.md`](../requirements/0001-wsl-k3d-argocd-platform.md)
- **Spec**: [`../../03.specs/001-wsl-k3d-argocd-platform/spec.md`](../../03.specs/001-wsl-k3d-argocd-platform/spec.md)
- **Plan**: [`../../04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md`](../../04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md)
- **Related ADR**: [`./0004-external-services-endpoints-and-valkey-backend.md`](./0004-external-services-endpoints-and-valkey-backend.md)
```

- [ ] **Step 3: 0003-eso-vault-k8s-auth.md Related Documents 수정 (라인 49-53)**

```markdown
- **PRD**: [`../../01.requirements/2026-03-27-wsl-k3d-argocd-platform.md`](../../01.requirements/2026-03-27-wsl-k3d-argocd-platform.md)
- **ARD**: [`../requirements/0001-wsl-k3d-argocd-platform.md`](../requirements/0001-wsl-k3d-argocd-platform.md)
- **Spec**: [`../../03.specs/001-wsl-k3d-argocd-platform/spec.md`](../../03.specs/001-wsl-k3d-argocd-platform/spec.md)
- **Plan**: [`../../04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md`](../../04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md)
- **Related ADR**: [`./0004-external-services-endpoints-and-valkey-backend.md`](./0004-external-services-endpoints-and-valkey-backend.md)
```

- [ ] **Step 4: 0004-external-services-endpoints-and-valkey-backend.md Related Documents 수정 (라인 62-66)**

```markdown
- **PRD**: [`../../01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../../01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **ARD**: [`../requirements/0002-wsl2-k3d-argocd-ha-platform.md`](../requirements/0002-wsl2-k3d-argocd-ha-platform.md)
- **Spec**: [`../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Related ADR**: [`./0001-k3d-topology-and-network.md`](./0001-k3d-topology-and-network.md)
- **Related ADR**: [`./0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](./0005-wsl2-ha-baseline-and-external-endpoint-contract.md)
```

- [ ] **Step 5: 0005-wsl2-ha-baseline-and-external-endpoint-contract.md Related Documents 수정 (라인 68-73)**

```markdown
- **PRD**: [`../../01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../../01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **ARD**: [`../requirements/0002-wsl2-k3d-argocd-ha-platform.md`](../requirements/0002-wsl2-k3d-argocd-ha-platform.md)
- **Spec**: [`../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Plan**: [`../../04.execution/plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../../04.execution/plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **Related ADR**: [`./0001-k3d-topology-and-network.md`](./0001-k3d-topology-and-network.md)
- **Related ADR**: [`./0004-external-services-endpoints-and-valkey-backend.md`](./0004-external-services-endpoints-and-valkey-backend.md)
```

- [ ] **Step 6: 0006-cert-manager-mkcert-ca-issuer.md Related Documents 수정 (라인 61-65)**

```markdown
- **PRD**: [`../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md`](../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md)
- **ARD**: [`../requirements/0003-platform-expansion-mesh-dashboard.md`](../requirements/0003-platform-expansion-mesh-dashboard.md)
- **Spec**: [`../../03.specs/003-platform-expansion/spec.md`](../../03.specs/003-platform-expansion/spec.md)
- **Related ADR**: [`./0007-kubernetes-dashboard-v3.md`](./0007-kubernetes-dashboard-v3.md)
- **Related ADR**: [`./0008-istio-install-and-ingress-coexist.md`](./0008-istio-install-and-ingress-coexist.md)
```

- [ ] **Step 7: 0007-kubernetes-dashboard-v3.md Related Documents 수정 (라인 59-62)**

```markdown
- **PRD**: [`../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md`](../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md)
- **ARD**: [`../requirements/0003-platform-expansion-mesh-dashboard.md`](../requirements/0003-platform-expansion-mesh-dashboard.md)
- **Spec**: [`../../03.specs/003-platform-expansion/spec.md`](../../03.specs/003-platform-expansion/spec.md)
- **Related ADR**: [`./0006-cert-manager-mkcert-ca-issuer.md`](./0006-cert-manager-mkcert-ca-issuer.md)
```

- [ ] **Step 8: 0008-istio-install-and-ingress-coexist.md Related Documents 수정 (라인 66-69)**

```markdown
- **PRD**: [`../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md`](../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md)
- **ARD**: [`../requirements/0003-platform-expansion-mesh-dashboard.md`](../requirements/0003-platform-expansion-mesh-dashboard.md)
- **Spec**: [`../../03.specs/003-platform-expansion/spec.md`](../../03.specs/003-platform-expansion/spec.md)
- **Related ADR**: [`./0009-kiali-external-observability.md`](./0009-kiali-external-observability.md)
```

- [ ] **Step 9: 0009-kiali-external-observability.md Related Documents 수정 (라인 67-71)**

```markdown
- **PRD**: [`../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md`](../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md)
- **ARD**: [`../requirements/0003-platform-expansion-mesh-dashboard.md`](../requirements/0003-platform-expansion-mesh-dashboard.md)
- **Spec**: [`../../03.specs/003-platform-expansion/spec.md`](../../03.specs/003-platform-expansion/spec.md)
- **Related ADR**: [`./0008-istio-install-and-ingress-coexist.md`](./0008-istio-install-and-ingress-coexist.md)
- **Related ADR**: [`./0001-k3d-topology-and-network.md`](./0001-k3d-topology-and-network.md)
```

- [ ] **Step 10: 검증**

```bash
grep -rn "\`\.\./0[0-9]\.requirements/\|\`\.\./02\.architecture/requirements/\|\`\.\./03\.specs/\|\`\.\./04\.execution/plans/" docs/02.architecture/decisions/
```

기대 결과: 출력 없음

---

### T-12: ARD 생성 파일 표시 텍스트 수정

**대상 패턴:** `docs/02.architecture/requirements/`에서의 올바른 표시 텍스트

| 현재 잘못된 표시 텍스트                     | 올바른 표시 텍스트                      |
| ------------------------------------------- | --------------------------------------- |
| `` `../01.requirements/<file>` ``           | `` `../../01.requirements/<file>` ``    |
| `` `../02.architecture/decisions/<file>` `` | `` `../decisions/<file>` ``             |
| `` `../03.specs/<path>` ``                  | `` `../../03.specs/<path>` ``           |
| `` `../04.execution/plans/<file>` ``        | `` `../../04.execution/plans/<file>` `` |

- [ ] **Step 1: 0001-wsl-k3d-argocd-platform.md Related Documents 수정 (라인 75-78)**

```markdown
- **PRD**: [`../../01.requirements/2026-03-27-wsl-k3d-argocd-platform.md`](../../01.requirements/2026-03-27-wsl-k3d-argocd-platform.md)
- **Spec**: [`../../03.specs/001-wsl-k3d-argocd-platform/spec.md`](../../03.specs/001-wsl-k3d-argocd-platform/spec.md)
- **Plan**: [`../../04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md`](../../04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md)
- **ADR**: [`../decisions/0001-k3d-topology-and-network.md`](../decisions/0001-k3d-topology-and-network.md), [`../decisions/0002-argocd-helm-and-gitops-model.md`](../decisions/0002-argocd-helm-and-gitops-model.md), [`../decisions/0003-eso-vault-k8s-auth.md`](../decisions/0003-eso-vault-k8s-auth.md), [`../decisions/0004-external-services-endpoints-and-valkey-backend.md`](../decisions/0004-external-services-endpoints-and-valkey-backend.md)
```

- [ ] **Step 2: 0002-wsl2-k3d-argocd-ha-platform.md Related Documents 수정 (라인 95-98)**

```markdown
- **PRD**: [`../../01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../../01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **Spec**: [`../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Plan**: [`../../04.execution/plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../../04.execution/plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **ADR**: [`../decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](../decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md)
```

- [ ] **Step 3: 0003-platform-expansion-mesh-dashboard.md Related Documents 수정 (라인 115-121)**

```markdown
- **PRD**: [`../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md`](../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md)
- **ADR**: [`../decisions/0006-cert-manager-mkcert-ca-issuer.md`](../decisions/0006-cert-manager-mkcert-ca-issuer.md), [`../decisions/0007-kubernetes-dashboard-v3.md`](../decisions/0007-kubernetes-dashboard-v3.md), [`../decisions/0008-istio-install-and-ingress-coexist.md`](../decisions/0008-istio-install-and-ingress-coexist.md), [`../decisions/0009-kiali-external-observability.md`](../decisions/0009-kiali-external-observability.md)
- **Spec**: [`../../03.specs/003-platform-expansion/spec.md`](../../03.specs/003-platform-expansion/spec.md)
- **Plan**: [`../../04.execution/plans/2026-03-29-platform-expansion.md`](../../04.execution/plans/2026-03-29-platform-expansion.md)
```

- [ ] **Step 4: 검증**

```bash
grep -rn "\`\.\./0[0-9]\.requirements/\|\`\.\./02\.architecture/decisions/\|\`\.\./03\.specs/\|\`\.\./04\.execution/" docs/02.architecture/requirements/
```

기대 결과: 출력 없음

---

### T-13: Plan 생성 파일 표시 텍스트 수정

**대상 패턴:** `docs/04.execution/plans/`에서의 올바른 표시 텍스트

| 현재 잘못된 표시 텍스트                        | 올바른 표시 텍스트                                |
| ---------------------------------------------- | ------------------------------------------------- |
| `` `../01.requirements/<file>` ``              | `` `../../01.requirements/<file>` ``              |
| `` `../02.architecture/requirements/<file>` `` | `` `../../02.architecture/requirements/<file>` `` |
| `` `../02.architecture/decisions/<file>` ``    | `` `../../02.architecture/decisions/<file>` ``    |
| `` `../03.specs/<path>` ``                     | `` `../../03.specs/<path>` ``                     |
| `` `../04.execution/tasks/<file>` ``           | `` `../tasks/<file>` ``                           |
| `` `../00.agent-governance/<path>` ``          | `` `../../00.agent-governance/<path>` ``          |
| `` `../../.github/<file>` ``                   | `` `../../../.github/<file>` ``                   |

- [ ] **Step 1: 2026-03-27-wsl-k3d-argocd-platform.md Related Documents 수정 (라인 71-74)**

```markdown
- **PRD**: [`../../01.requirements/2026-03-27-wsl-k3d-argocd-platform.md`](../../01.requirements/2026-03-27-wsl-k3d-argocd-platform.md)
- **ARD**: [`../../02.architecture/requirements/0001-wsl-k3d-argocd-platform.md`](../../02.architecture/requirements/0001-wsl-k3d-argocd-platform.md)
- **Spec**: [`../../03.specs/001-wsl-k3d-argocd-platform/spec.md`](../../03.specs/001-wsl-k3d-argocd-platform/spec.md)
- **ADR**: [`../../02.architecture/decisions/0001-k3d-topology-and-network.md`](../../02.architecture/decisions/0001-k3d-topology-and-network.md), [`../../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md`](../../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md), [`../../02.architecture/decisions/0003-eso-vault-k8s-auth.md`](../../02.architecture/decisions/0003-eso-vault-k8s-auth.md), [`../../02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md`](../../02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md)
```

- [ ] **Step 2: 2026-03-28-wsl2-k3d-argocd-ha-platform.md Related Documents 수정 (라인 115-119)**

```markdown
- **PRD**: [`../../01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../../01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **ARD**: [`../../02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md`](../../02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md)
- **ADR**: [`../../02.architecture/decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](../../02.architecture/decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md)
- **Spec**: [`../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Tasks**: [`../tasks/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../tasks/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
```

- [ ] **Step 3: 2026-03-29-platform-expansion.md Related Documents 수정 (라인 96-100)**

```markdown
- **PRD**: [`../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md`](../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md)
- **ARD**: [`../../02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md`](../../02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md)
- **Spec**: [`../../03.specs/003-platform-expansion/spec.md`](../../03.specs/003-platform-expansion/spec.md)
- **ADR**: [`../../02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md`](../../02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md)
- **Tasks**: [`../tasks/2026-03-29-platform-expansion.md`](../tasks/2026-03-29-platform-expansion.md)
```

- [ ] **Step 4: 2026-05-09-github-qa-ci-remediation.md Related Documents 수정 (라인 121-124)**

```markdown
- **Task**: [`../tasks/2026-05-09-github-qa-ci-remediation.md`](../tasks/2026-05-09-github-qa-ci-remediation.md)
- **Git Workflow**: [`../../00.agent-governance/rules/git-workflow.md`](../../00.agent-governance/rules/git-workflow.md)
- **GitHub Hub**: [`../../../.github/ABOUT.md`](../../../.github/ABOUT.md)
- **PR Template**: [`../../../.github/PULL_REQUEST_TEMPLATE.md`](../../../.github/PULL_REQUEST_TEMPLATE.md)
```

- [ ] **Step 5: 2026-05-09-k3d-agent-first-remediation.md Related Documents 수정 (라인 127-130)**

```markdown
- **Governance**: [`../../00.agent-governance/harness-catalog.md`](../../00.agent-governance/harness-catalog.md)
- **Agent-first Rules**: [`../../00.agent-governance/rules/agentic.md`](../../00.agent-governance/rules/agentic.md)
- **Document Routing**: [`../../00.agent-governance/rules/document-stage-routing.md`](../../00.agent-governance/rules/document-stage-routing.md)
- **Task**: [`../tasks/2026-05-09-k3d-agent-first-remediation.md`](../tasks/2026-05-09-k3d-agent-first-remediation.md)
```

- [ ] **Step 6: 2026-05-09-scripts-inventory-remediation.md Related Documents 수정**

```markdown
- **Task**: [`../tasks/2026-05-09-scripts-inventory-remediation.md`](../tasks/2026-05-09-scripts-inventory-remediation.md)
- **Agent Governance Memory**: [`../../00.agent-governance/memory/progress.md`](../../00.agent-governance/memory/progress.md)
```

- [ ] **Step 7: 검증**

```bash
grep -rn "\`\.\./0[0-9]\.requirements/\|\`\.\./02\.architecture/\|\`\.\./03\.specs/\|\`\.\./04\.execution/tasks/\|\`\.\./00\.agent-governance/\|\`\.\./\.\./\.github/" docs/04.execution/plans/
```

기대 결과: 출력 없음

---

### T-14: Task 생성 파일 표시 텍스트 수정

**대상 패턴:** `docs/04.execution/tasks/`에서의 올바른 표시 텍스트

| 현재 잘못된 표시 텍스트                  | 올바른 표시 텍스트                          |
| ---------------------------------------- | ------------------------------------------- |
| `` `../03.specs/<path>` ``               | `` `../../03.specs/<path>` ``               |
| `` `../04.execution/plans/<file>` ``     | `` `../plans/<file>` ``                     |
| `` `../05.operations/runbooks/<file>` `` | `` `../../05.operations/runbooks/<file>` `` |
| `` `../00.agent-governance/<path>` ``    | `` `../../00.agent-governance/<path>` ``    |
| `` `../../.github/<file>` ``             | `` `../../../.github/<file>` ``             |
| `` `../../scripts/<file>` ``             | `` `../../../scripts/<file>` ``             |

- [ ] **Step 1: 2026-03-27-wsl-k3d-argocd-platform.md Inputs (라인 9-10) + Related Documents (라인 79-81) 수정**

Inputs:

```markdown
- **Parent Spec**: [`../../03.specs/001-wsl-k3d-argocd-platform/spec.md`](../../03.specs/001-wsl-k3d-argocd-platform/spec.md)
- **Parent Plan**: [`../plans/2026-03-27-wsl-k3d-argocd-platform.md`](../plans/2026-03-27-wsl-k3d-argocd-platform.md)
```

Related Documents:

```markdown
- **Spec**: [`../../03.specs/001-wsl-k3d-argocd-platform/spec.md`](../../03.specs/001-wsl-k3d-argocd-platform/spec.md)
- **Plan**: [`../plans/2026-03-27-wsl-k3d-argocd-platform.md`](../plans/2026-03-27-wsl-k3d-argocd-platform.md)
- **Runbook**: [`../../05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md`](../../05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md)
```

- [ ] **Step 2: 2026-03-28-wsl2-k3d-argocd-ha-platform.md 수정**

Inputs:

```markdown
- **Parent Spec**: [`../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Parent Plan**: [`../plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
```

Related Documents (라인 97, 101-103):

```markdown
- Ops 증적: [`../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md`](../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md)
- **Spec**: [`../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Plan**: [`../plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **Runbook**: [`../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md`](../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md)
```

- [ ] **Step 3: 2026-03-29-platform-expansion.md 수정**

Inputs:

```markdown
- **Parent Spec**: [`../../03.specs/003-platform-expansion/spec.md`](../../03.specs/003-platform-expansion/spec.md)
- **Parent Plan**: [`../plans/2026-03-29-platform-expansion.md`](../plans/2026-03-29-platform-expansion.md)
```

Related Documents:

```markdown
- **Spec**: [`../../03.specs/003-platform-expansion/spec.md`](../../03.specs/003-platform-expansion/spec.md)
- **Plan**: [`../plans/2026-03-29-platform-expansion.md`](../plans/2026-03-29-platform-expansion.md)
- **Runbook**: [`../../05.operations/runbooks/0003-platform-expansion-bootstrap-runbook.md`](../../05.operations/runbooks/0003-platform-expansion-bootstrap-runbook.md)
```

- [ ] **Step 4: 2026-05-09-github-qa-ci-remediation.md 수정**

Inputs:

```markdown
- **Parent Plan**: [`../plans/2026-05-09-github-qa-ci-remediation.md`](../plans/2026-05-09-github-qa-ci-remediation.md)
```

Related Documents:

```markdown
- **Plan**: [`../plans/2026-05-09-github-qa-ci-remediation.md`](../plans/2026-05-09-github-qa-ci-remediation.md)
- **GitHub Hub**: [`../../../.github/ABOUT.md`](../../../.github/ABOUT.md)
- **PR Template**: [`../../../.github/PULL_REQUEST_TEMPLATE.md`](../../../.github/PULL_REQUEST_TEMPLATE.md)
- **Git Workflow**: [`../../00.agent-governance/rules/git-workflow.md`](../../00.agent-governance/rules/git-workflow.md)
```

- [ ] **Step 5: 2026-05-09-k3d-agent-first-remediation.md 수정**

Inputs:

```markdown
- **Parent Plan**: [`../plans/2026-05-09-k3d-agent-first-remediation.md`](../plans/2026-05-09-k3d-agent-first-remediation.md)
```

Related Documents:

```markdown
- **Plan**: [`../plans/2026-05-09-k3d-agent-first-remediation.md`](../plans/2026-05-09-k3d-agent-first-remediation.md)
- **Governance**: [`../../00.agent-governance/harness-catalog.md`](../../00.agent-governance/harness-catalog.md)
- **Agent-first Rules**: [`../../00.agent-governance/rules/agentic.md`](../../00.agent-governance/rules/agentic.md)
```

- [ ] **Step 6: 2026-05-09-scripts-inventory-remediation.md 수정**

Inputs:

```markdown
- **Parent Plan**: [`../plans/2026-05-09-scripts-inventory-remediation.md`](../plans/2026-05-09-scripts-inventory-remediation.md)
```

Related Documents:

```markdown
- **Plan**: [`../plans/2026-05-09-scripts-inventory-remediation.md`](../plans/2026-05-09-scripts-inventory-remediation.md)
- **Scripts README**: [`../../../scripts/README.md`](../../../scripts/README.md)
- **Root README**: [`../../README.md`](../../README.md)
```

- [ ] **Step 7: 검증**

```bash
grep -rn "\`\.\./03\.specs/\|\`\.\./04\.execution/plans/\|\`\.\./05\.operations/runbooks/\|\`\.\./00\.agent-governance/\|\`\.\./\.\./\.github/\|\`\.\./\.\./scripts/" docs/04.execution/tasks/
```

기대 결과: 출력 없음

---

### T-15: Guide 생성 파일 표시 텍스트 수정

**대상 패턴:** `docs/05.operations/guides/`에서의 올바른 표시 텍스트

| 현재 잘못된 표시 텍스트                     | 올바른 표시 텍스트                             |
| ------------------------------------------- | ---------------------------------------------- |
| `` `../03.specs/<path>` ``                  | `` `../../03.specs/<path>` ``                  |
| `` `../04.execution/plans/<file>` ``        | `` `../../04.execution/plans/<file>` ``        |
| `` `../05.operations/policies/<file>` ``    | `` `../policies/<file>` ``                     |
| `` `../05.operations/runbooks/<file>` ``    | `` `../runbooks/<file>` ``                     |
| `` `../02.architecture/decisions/<file>` `` | `` `../../02.architecture/decisions/<file>` `` |

- [ ] **Step 1: 0001-wsl-k3d-argocd-bootstrap-guide.md Related Documents 수정 (라인 119-122)**

```markdown
- **Spec**: [`../../03.specs/001-wsl-k3d-argocd-platform/spec.md`](../../03.specs/001-wsl-k3d-argocd-platform/spec.md)
- **Operation**: [`../policies/0001-k8s-gitops-operations-policy.md`](../policies/0001-k8s-gitops-operations-policy.md)
- **Runbook**: [`../runbooks/0001-argocd-platform-bootstrap-runbook.md`](../runbooks/0001-argocd-platform-bootstrap-runbook.md)
- **Plan**: [`../../04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md`](../../04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md)
```

- [ ] **Step 2: 0002-wsl2-k3d-argocd-ha-setup-guide.md 수정 (라인 138, 264-266)**

라인 138 (본문 내 링크):

```markdown
- 재발급 절차: [`../runbooks/0002-argocd-eso-vault-recovery-runbook.md#troubleshooting-signatures`](../runbooks/0002-argocd-eso-vault-recovery-runbook.md#troubleshooting-signatures)
```

Related Documents (라인 264-266):

```markdown
- **Spec**: [`../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Operation**: [`../policies/0002-wsl2-k3d-gitops-ha-operations-policy.md`](../policies/0002-wsl2-k3d-gitops-ha-operations-policy.md)
- **Runbook**: [`../runbooks/0002-argocd-eso-vault-recovery-runbook.md`](../runbooks/0002-argocd-eso-vault-recovery-runbook.md)
```

- [ ] **Step 3: 0003-platform-expansion-bootstrap-guide.md Related Documents 수정 (라인 229-232)**

```markdown
- **Spec**: [`../../03.specs/003-platform-expansion/spec.md`](../../03.specs/003-platform-expansion/spec.md)
- **Operation**: [`../policies/0003-service-mesh-cert-manager-policy.md`](../policies/0003-service-mesh-cert-manager-policy.md)
- **Runbook**: [`../runbooks/0003-platform-expansion-bootstrap-runbook.md`](../runbooks/0003-platform-expansion-bootstrap-runbook.md)
- **ADR-0010**: [`../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md`](../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md)
```

- [ ] **Step 4: 0004-headlamp-auth-oidc-guide.md Related Documents 수정 (라인 350-353)**

```markdown
- **Runbook**: [`../runbooks/0005-headlamp-keycloak-runbook.md`](../runbooks/0005-headlamp-keycloak-runbook.md)
- **ADR-0010**: [`../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md`](../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md)
- **Operations**: [`../policies/0004-rollouts-notifications-headlamp-policy.md`](../policies/0004-rollouts-notifications-headlamp-policy.md)
- **Bootstrap Runbook**: [`../runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../runbooks/0004-rollouts-notifications-headlamp-runbook.md)
```

- [ ] **Step 5: 0008-github-app-gitops-onboarding-guide.md Related Documents 수정 (라인 417-418)**

```markdown
- **Runbook**: [`../runbooks/0010-github-app-gitops-onboarding-runbook.md`](../runbooks/0010-github-app-gitops-onboarding-runbook.md)
- **Operations 정책**: [`../policies/0007-app-gitops-onboarding-policy.md`](../policies/0007-app-gitops-onboarding-policy.md)
```

- [ ] **Step 6: 검증**

```bash
grep -rn "\`\.\./03\.specs/\|\`\.\./04\.execution/\|\`\.\./05\.operations/\|\`\.\./02\.architecture/decisions/" docs/05.operations/guides/
```

기대 결과: 출력 없음

---

### T-16: Runbook 생성 파일 표시 텍스트 수정

**대상 패턴:** `docs/05.operations/runbooks/`에서의 올바른 표시 텍스트

| 현재 잘못된 표시 텍스트                        | 올바른 표시 텍스트                                |
| ---------------------------------------------- | ------------------------------------------------- |
| `` `../02.architecture/requirements/<file>` `` | `` `../../02.architecture/requirements/<file>` `` |
| `` `../02.architecture/decisions/<file>` ``    | `` `../../02.architecture/decisions/<file>` ``    |
| `` `../03.specs/<path>` ``                     | `` `../../03.specs/<path>` ``                     |
| `` `../04.execution/plans/<file>` ``           | `` `../../04.execution/plans/<file>` ``           |
| `` `../05.operations/guides/<file>` ``         | `` `../guides/<file>` ``                          |
| `` `../05.operations/policies/<file>` ``       | `` `../policies/<file>` ``                        |

- [ ] **Step 1: 0001-argocd-platform-bootstrap-runbook.md Canonical References 수정 (라인 15-21)**

```markdown
- [`../../02.architecture/requirements/0001-wsl-k3d-argocd-platform.md`](../../02.architecture/requirements/0001-wsl-k3d-argocd-platform.md)
- [`../../02.architecture/decisions/0001-k3d-topology-and-network.md`](../../02.architecture/decisions/0001-k3d-topology-and-network.md)
- [`../../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md`](../../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md)
- [`../../02.architecture/decisions/0003-eso-vault-k8s-auth.md`](../../02.architecture/decisions/0003-eso-vault-k8s-auth.md)
- [`../../02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md`](../../02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md)
- [`../../03.specs/001-wsl-k3d-argocd-platform/spec.md`](../../03.specs/001-wsl-k3d-argocd-platform/spec.md)
- [`../../04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md`](../../04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md)
```

- [ ] **Step 2: 0002-argocd-eso-vault-recovery-runbook.md 수정**

Canonical References (라인 21-24):

```markdown
- [`../../02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md`](../../02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md)
- [`../../02.architecture/decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](../../02.architecture/decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md)
- [`../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- [`../../04.execution/plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../../04.execution/plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
```

Related Documents (라인 177-178):

```markdown
- **Guide**: [`../guides/0002-wsl2-k3d-argocd-ha-setup-guide.md`](../guides/0002-wsl2-k3d-argocd-ha-setup-guide.md)
- **Operations Policy**: [`../policies/0002-wsl2-k3d-gitops-ha-operations-policy.md`](../policies/0002-wsl2-k3d-gitops-ha-operations-policy.md)
```

- [ ] **Step 3: 0003-platform-expansion-bootstrap-runbook.md 수정**

Canonical References (라인 18-21):

```markdown
- [`../../03.specs/003-platform-expansion/spec.md`](../../03.specs/003-platform-expansion/spec.md)
- [`../guides/0003-platform-expansion-bootstrap-guide.md`](../guides/0003-platform-expansion-bootstrap-guide.md)
- [`../policies/0003-service-mesh-cert-manager-policy.md`](../policies/0003-service-mesh-cert-manager-policy.md)
- [`../../02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md`](../../02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md)
```

Related Documents (라인 251-255):

```markdown
- **Guide**: [`../guides/0003-platform-expansion-bootstrap-guide.md`](../guides/0003-platform-expansion-bootstrap-guide.md)
- **Spec**: [`../../03.specs/003-platform-expansion/spec.md`](../../03.specs/003-platform-expansion/spec.md)
- **Operations**: [`../policies/0003-service-mesh-cert-manager-policy.md`](../policies/0003-service-mesh-cert-manager-policy.md)
- **ADR-0010**: [`../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md`](../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md)
- **Previous Runbook**: [`./0001-argocd-platform-bootstrap-runbook.md`](./0001-argocd-platform-bootstrap-runbook.md)
```

- [ ] **Step 4: 0004-rollouts-notifications-headlamp-runbook.md 수정**

Canonical References (라인 17-20):

```markdown
- [`../policies/0004-rollouts-notifications-headlamp-policy.md`](../policies/0004-rollouts-notifications-headlamp-policy.md)
- [`../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md`](../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md)
- [`../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md`](../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md)
- [`../../02.architecture/decisions/0012-argo-notifications-slack.md`](../../02.architecture/decisions/0012-argo-notifications-slack.md)
```

Related Documents (라인 184-187):

```markdown
- **Operations**: [`../policies/0004-rollouts-notifications-headlamp-policy.md`](../policies/0004-rollouts-notifications-headlamp-policy.md)
- **ADR-0010**: [`../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md`](../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md)
- **ADR-0011**: [`../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md`](../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md)
- **ADR-0012**: [`../../02.architecture/decisions/0012-argo-notifications-slack.md`](../../02.architecture/decisions/0012-argo-notifications-slack.md)
```

- [ ] **Step 5: 검증**

```bash
grep -rn "\`\.\./02\.architecture/\|\`\.\./03\.specs/\|\`\.\./04\.execution/\|\`\.\./05\.operations/" docs/05.operations/runbooks/
```

기대 결과: 출력 없음

---

### T-17: 최종 통합 검증 및 progress.md 업데이트

- [ ] **Step 1: 전체 cross-link 불일치 전수 스캔**

```bash
grep -rn "\`\.\./0[0-9]\." docs/ --include="*.md" | grep -v "99.templates" | grep -v "^Binary"
```

기대 결과: 출력 없음

- [ ] **Step 2: 05.operations 경로 불일치 전수 스캔**

```bash
grep -rn "\`\.\./05\.operations/" docs/ --include="*.md" | grep -v "99.templates"
```

기대 결과: 출력 없음

- [ ] **Step 3: 실제 href 파일 존재 확인 (샘플)**

```bash
ls docs/01.requirements/2026-03-27-wsl-k3d-argocd-platform.md
ls docs/02.architecture/requirements/0001-wsl-k3d-argocd-platform.md
ls docs/03.specs/001-wsl-k3d-argocd-platform/spec.md
ls docs/04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md
ls docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md
```

기대 결과: 모든 파일 존재

- [ ] **Step 4: progress.md 업데이트**

`docs/00.agent-governance/memory/progress.md`의 `## Work Entries` 섹션에 다음 entry를 추가:

```markdown
### 2026-05-17 — Template Cross-link Fix

- **Layer**: docs
- **Status**: complete
- **Tags**: #docs #templates #cross-links

## Progress

- `docs/99.templates/` 내 10개 템플릿 파일의 Cross-link 플레이스홀더 경로 수정
- `docs/02.architecture/decisions/` ADR 9개 표시 텍스트 수정
- `docs/02.architecture/requirements/` ARD 3개 표시 텍스트 수정
- `docs/04.execution/plans/` Plan 6개 표시 텍스트 수정
- `docs/04.execution/tasks/` Task 6개 표시 텍스트 수정
- `docs/05.operations/guides/` Guide 5개 표시 텍스트 수정
- `docs/05.operations/runbooks/` Runbook 4개 표시 텍스트 수정

## Memory

- 템플릿 플레이스홀더 경로는 Target 위치 기준으로 작성해야 한다 (`docs/99.templates/` 위치 기준이 아님)
- `decisions/`, `tasks/`, `runbooks/` 등 2단계 깊이의 Target은 `../../` 필요
- 형제 디렉터리 참조는 `../sibling/` 패턴 사용 (`../05.operations/sibling/` 아님)
- spec.template.md와 prd.template.md는 이미 올바른 패턴을 사용 중

## Evidence

- `grep -rn "\`\.\./0[0-9]\." docs/ --include="\*.md" | grep -v "99.templates"` → 출력 없음
- `grep -rn "\`\.\./05\.operations/" docs/ --include="\*.md" | grep -v "99.templates"` → 출력 없음

## Handoff

None
```

- [ ] **Step 5: 커밋**

```bash
git add docs/99.templates/ docs/02.architecture/ docs/04.execution/ docs/05.operations/ docs/00.agent-governance/memory/progress.md
git commit -m "docs: fix cross-link relative paths in templates and generated files

- Fix 10 template files: correct relative paths from Target location
  - adr, ard, plan, task, guide, runbook, incident, postmortem, operation, reference
- Fix display text (backtick code) in ~30 generated files to match actual href
  - ADR (9 files), ARD (3), Plan (6), Task (6), Guide (5), Runbook (4)
- Templates now show correct paths from Target position
- No actual href links were broken; only display text was inconsistent"
```
