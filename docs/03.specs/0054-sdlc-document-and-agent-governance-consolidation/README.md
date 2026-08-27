# SPEC-0054: Sdlc Document And Agent Governance Consolidation

## Overview

이 문서는 수명주기 권한을 복제하지 않고 패키지 소유 문서로 연결하며,
이 패키지의 모든 Task가 공유하는 실행 제약을 한 번만 소유합니다.

## Scope

이 라우터는 탐색과 공통 실행 계약만 담당하며, 개별 상태,
요구사항, WP 결과와 구현 증거는 해당 Spec, Plan, Task가 소유합니다.

## Item Index

- [Spec](spec.md)
- [Plan](plan.md)

## Add and Find

변경 계약은 Spec에서, 구현 순서와 공통 위험·검증 계약은 Plan에서, 행별 실행 증거는 아래 Task 기록에서 찾습니다.

## Common Execution Contract

### Common Inputs

- [Spec 0054](spec.md)
- [Plan 0054](plan.md)
- Predecessor Spec 0052 and its inherited WORK-109 evidence
- [ADR-0022 direct approval lineage](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [ADR-0024 historical terminal-taxonomy decision](../../02.architecture/decisions/0024-terminal-artifact-identity-and-archive-layout.md),
  superseded where ADR-0030 defines the new terminal authority
- [ADR-0030 authority-first convergence](../../02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md)
- The Git parent of the WP-001 design-authority commit and the exact inherited
  WORK-109 staged/unstaged inventory recorded by WP-002
- External primary-source basis embedded in [Spec 0054](spec.md#external-basis)

### Scheduling and Completion

- Only one Task may be `in-progress` at a time. A dependency-blocked Task is
  `blocked`, is not the active execution Task, and may resume only after its
  declared dependency closes.
- The closed successor order is
  `WP-004 → WP-003 → WP-005 → WP-006 → WP-007 → WP-008 → WP-009 → WP-010 → WP-011 → WP-012 → WP-013 → WP-014`.
  WP-001 and WP-002 are completed evidence and are not re-entered.
- A Task becomes `done` only after its focused RED/GREEN evidence, assigned
  broad gates, independent specification and code-quality review, any
  WP-specific domain reviews, and all ordered logical commits exist.
- Each independently testable logical unit gets one scoped commit. When a WP
  owns ordered commits, their order and exact commit subjects are defined by
  that WP's section in [Plan 0054](plan.md#work-breakdown).
- Each completed Task records exact commands, exit codes, finding counts,
  staged-path shape, mutation status, reviewer disposition, commit identity,
  and limitations. `PASS` without those bindings is insufficient.
- Task IDs and package-local sequences are append-only and are never reused.

### Approval, Safety, Rollback, and Review Boundaries

- **Allowed Paths**: repository files explicitly named by the active work
  package in [Plan 0054](plan.md#work-breakdown).
- **Forbidden Paths**: unrelated user changes; sealed Stage 98 payloads;
  unapproved live infrastructure, credentials, provider runtime, remote CI,
  release, push, merge, and publication surfaces.
- **Approval Required**: new document families, reintroducing a Release family,
  destructive history changes, credential access, live or remote mutation,
  scope beyond the approved B boundary (which already includes Stage 90), or
  deletion lacking consumer-zero and recovery evidence.
- **Static Validation**: focused unit/contract tests, affected and staged
  lanes, registry/Markdown/link/lifecycle/archive gates, aggregate quality,
  pre-commit, all-files fixed point, and diff checks as assigned by the Plan.
- **Live Validation**: DEFER. Repository-static evidence does not establish
  provider-runtime, hosted-CI, deployment, incident-response, or platform
  behavior.
- **Secret / Vault Handling**: no secret-value read or output. Only the existing
  redacted secret-handling validator and configured detect-secrets hooks may be
  used.
- **Rollback Plan**: stop at the failing work package; preserve the worktree;
  revert only that package's logical commit if authorized. Never edit sealed
  evidence as rollback.
- **Review Boundary**: use a fresh implementer, independent specification
  review, and independent code-quality review for each Task. Obtain the
  WP-specific domain reviews named in Plan 0054 and resolve every Critical or
  Important finding before committing.
- **Evidence Location**: append-only Spec Task records, bounded machine
  disposition ledgers, minimal Stage 98 Migration/Tombstone records, and Git
  commits.

Every Task record below inherits this contract without exception and links its
own Plan section for the exact file boundary, validation commands, reviews,
rollback implications, and ordered logical commit boundary.

## Task Records

- [`TSK-0054-0001`](tasks/tsk-0001-approved-design-authority.md)
- [`TSK-0054-0002`](tasks/tsk-0002-terminal-topology-and-four-digit-identity.md)
- [`TSK-0054-0003`](tasks/tsk-0003-codex-claude-only-ai-agent-governance.md)
- [`TSK-0054-0004`](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md)
- [`TSK-0054-0005`](tasks/tsk-0005-stage-05-responsibility-ledger.md)
- [`TSK-0054-0006`](tasks/tsk-0006-stage-05-ownership-cutover.md)
- [`TSK-0054-0007`](tasks/tsk-0007-stage-90-disposition-ledger.md)
- [`TSK-0054-0008`](tasks/tsk-0008-stage-90-ownership-cutover.md)
- [`TSK-0054-0009`](tasks/tsk-0009-global-stage-98-parity-and-recovery-closure.md)
- [`TSK-0054-0010`](tasks/tsk-0010-script-gate-fixture-and-sha-ownership-fixed-point.md)
- [`TSK-0054-0011`](tasks/tsk-0011-responsibility-topology-and-compatibility-cutover.md)
- [`TSK-0054-0012`](tasks/tsk-0012-progress-and-generated-current-cleanup.md)
- [`TSK-0054-0013`](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md)
- [`TSK-0054-0014`](tasks/tsk-0014-convergence-and-branch-completion.md)

## Related Documents

- [MIG-0004 recovery ledger](../../98.archive/migrations/0004-document-authority-convergence.md)
