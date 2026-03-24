---
layer: "meta"
---
# Implementation Plan (PLAN.md)

_Target Location: `docs/plans/YYYY-MM-DD-<feature-name>.md`_
_Description: A project management document that breaks down a specification into executable tasks and phases. It tracks the progress and verification of each step._

## Overview (KR)
이 문서는 아키텍처 및 상세 설계를 실제 구현 단계로 나누어 관리하는 실행 계획서입니다. 단계별 작업 내용, 관련 파일, 검증 방법 및 진행 상황을 추적합니다.

---

## 1. Plan Metadata

- **Status**: [Planned | In Progress | Completed]
- **Owner**: [buenhyden]
- **layer**: [meta | infra | gitops | app | ops]
- **Related Spec**: `[../specs/YYYY-MM-DD-feature.md]`

## 2. Task Ledger (Execution Phases)

### Phase 1: Preparation & Setup
- [ ] TASK-001: [Action] (Affected: `file/path`)

### Phase 2: Core Implementation
- [ ] TASK-002: [Action] (Affected: `file/path`)

## 3. Checkpoints & Durable Execution (Senior)
[Define major points where progress is saved and verified before moving to the next phase.]

- **Checkpoint A**: [Phase 1 completion criteria]
- **Checkpoint B**: [Initial integration success]

## 4. Backtracking & Pivot Strategy (Senior)
[How to recover if the plan needs a major change mid-execution.]
- **Fallback Plan**: [e.g., Revert to previous branch if DB migration fails]
- **Pivot Rule**: [e.g., If API latency > 500ms, switch to [Alternative Approach]]

## 5. Verification Matrix

| Task ID | Level | Verification Command | Expected Result |
| :--- | :--- | :--- | :--- |
| **VAL-001** | Unit | `npm run test:unit` | 100% Pass |
| **VAL-002** | E2E | `npm run test:e2e` | Happy path success |

## 6. Completion Checklist
- [ ] Code committed and PR created.
- [ ] All verification steps passed.
- [ ] Documentation updated (ARD, Spec, Index).
