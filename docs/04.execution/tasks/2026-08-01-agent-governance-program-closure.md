---
title: 'Task: Agent Governance Program Closure'
type: sdlc/task
status: active
owner: platform
updated: 2026-08-01
---

# Task: Agent Governance Program Closure

## Overview

This Task is the canonical execution-evidence owner for Spec 046 activation,
closure-contract implementation, QA routing, final independent review,
reciprocal closure/postflight, local `main` merge, and isolated-worktree
cleanup.

Provider runtime/auth/model discovery, hosted CI, branch protection, remote
execution, live platform state, actual evaluation/admission/promotion, and
actual model fitness remain separate `DEFER` or `ABSENT` lanes unless a later
approved action observes them.

## Inputs

- Parent [Spec 046](../../03.specs/046-agent-governance-program-closure/spec.md)
- Parent [Implementation Plan](../plans/2026-08-01-agent-governance-program-closure.md)
- [PRD 003](../../01.requirements/003-workspace-agent-governance-platform.md),
  [ARD 0006](../../02.architecture/requirements/0006-workspace-agent-governance-platform.md),
  and [ADR 0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- Spec 045 closure `de9a88e4550b87542eb7221c5ae7416fe5075763`,
  sole parent `ed89228546501dd11a7f4abad28e8ebb094fbd97`, and observed
  postflight `060396112abaddbbcf79a33c8a04ae775cce66a1`
- Fixed cutoff `2026-07-10T10:00:00+09:00` /
  `2026-07-10T01:00:00Z`
- Observed Spec 046 activation
  `c6bae0227acd3e4f57b591c14a88e31b6f2e553f` with sole parent
  `060396112abaddbbcf79a33c8a04ae775cce66a1`
- Observed ADR-0019 and program-design activation
  `ff66dd933e00def085b4c0319a67c6651356b116`

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| AGPC-000 | VAL-AGPC-001, VAL-AGPC-010 | Activate reciprocal Spec/Plan/Task, three indexes, program lineage, and progress | platform | Done | Exact eight-file activation is committed and observed without a self-SHA preclaim in the activation content | `c6bae0227acd3e4f57b591c14a88e31b6f2e553f`; sole parent `060396112abaddbbcf79a33c8a04ae775cce66a1`; staged lifecycle/runner, strict docs, pre-commit, all-files, and diff PASS |
| AGPC-001 | VAL-AGPC-002 | Implement closure contract/schema/fixture/validator/tests | platform | Done | Closed repository-static contract package with fail-closed schema, source-bound predecessor/provider/model projections, four-class memory lifecycle, and value-free diagnostics | `c4457fa01ae41013ba56db3d3591da845529cf2b`; focused 28/28, staged lane, full pre-commit, Ruff, diff, requirements review, and quality review PASS |
| AGPC-002 | VAL-AGPC-003..007 | Route closure gate and reconcile harness/provider/loop/roster/model/memory owners | platform | Done | One existing CI job now owns 18 delegated checks; validation remains 22 surfaces with 22 validators and exactly 12 closure route classes; human owner docs point to one closure classification contract without external-lane promotion | `4fdea6a068aec6c65681bae32c44b67a5e95f09e`; focused, 20-path staged, aggregate, full pre-commit, requirements, and quality/security review PASS |
| AGPC-003 | VAL-AGPC-008, VAL-AGPC-009 | Run local QA and whole-branch requirements plus quality/security review | platform | Done | Verified local QA and independent review evidence is recorded without external-lane promotion | Final fix `1e2bd0744b5213d5004c34aac028b9642cc60028`; 774 Python tests, 15 Spec 046 validators, affected/staged/aggregate/pre-commit/Ruff/diff PASS, and resolved re-review PASS |
| AGPC-004 | VAL-AGPC-010 | Record reciprocal closure and observed postflight | platform | Pending | Not executed | Planned exact closure and postflight commits |
| AGPC-005 | VAL-AGPC-010 | Locally merge to `main` and clean isolated worktree/branch | platform | Pending | Not executed | Planned local-only integration evidence; no push or remote action |

## Approval and Safety Boundaries

- **Allowed Paths**: Spec 046 reciprocal documents/indexes, agent-governance
  contracts/docs, `.github/**`, `.pre-commit-config.yaml`, scripts, tests, and
  provider shims/adapters required by the closure route.
- **Forbidden Paths**: actual `.agent-work/checkpoint.json`, ignored/private
  provider state, auth caches/files, credentials, tokens, shell history,
  private transcripts, provider response bodies, secret values, and live
  Kubernetes/GitOps state.
- **Approval Required**: provider login/authenticated run, provider-native
  runtime discovery, hosted workflow dispatch, remote GitHub mutation, push,
  PR, remote merge, release, paid action, credential change, or live mutation.
- **Static Validation**: focused contract tests, affected/staged runners,
  strict document checks, repository aggregate, all-files pre-commit, and both
  diff checks.
- **Live Validation**: `DEFER`; every external lane requires a separate owner,
  limitation, retry trigger, approval, and observation.
- **Secret / Vault Handling**: no secret reads or prints and only synthetic or
  redacted tracked fixtures.
- **Rollback Plan**: revert only the current AGPC unit in reverse dependency
  order and preserve unrelated user work; revert activation last.
- **Evidence Location**: this Task and
  `../../00.agent-governance/memory/progress.md`.

## Verification Summary

AGPC-000 activation `c6bae0227acd3e4f57b591c14a88e31b6f2e553f`
has sole parent `060396112abaddbbcf79a33c8a04ae775cce66a1` and exactly eight
paths. Staged lifecycle, strict registry/Markdown/links, the exact-path staged
runner, plain staged pre-commit, repository-wide all-files pre-commit, and both
diff checks passed without formatter mutation. The activation content did not
preclaim its own SHA.

AGPC-001 implementation `c4457fa01ae41013ba56db3d3591da845529cf2b`
adds the closure contract, closed schema, production validator, duplicate-safe
fixture, focused tests, corpus-role registration, and narrowly scoped
secret-scanner exclusions for integrity metadata. The package binds actual
predecessor files and provider/model evidence by descriptor-relative reads and
SHA-256, keeps every non-repository lane `ABSENT` or `DEFER`, and rejects
secret-like durable keys or values without echoing them. The 28 focused tests,
exact ten-path staged lane, full pre-commit suite, Ruff, both diff checks, and
independent requirements and quality reviews passed. At that observation,
AGPC-002 through AGPC-005 remained pending.

AGPC-002 implementation `4fdea6a068aec6c65681bae32c44b67a5e95f09e`
routes closure self-test and production validation through the existing single
`agent-governance-static` job and through pre-commit before affected-surface
and repository-quality aggregation. The synchronized CI contract is `1.3.0`
with 18 delegated checks. Validation remains 22 surfaces and increases to 22
validators, with closure selected by exactly the 12 existing agent-governance
route classes. The implementation map, catalog, four provider notes, and
GitHub hub now route to one program result-classification owner while retaining
provider, hosted, actual-evaluation, remote, and live separation.

Focused CI and affected-surface tests first passed, then the repository
aggregate identified stale runner and provider-hook expected sets. Those
expectations were corrected, the affected 49 and 3 tests passed, and the full
aggregate, exact 20-path staged lane, full pre-commit, Ruff, diff checks, and
final requirements plus quality/security re-reviews passed. AGPC-003 through
AGPC-005 remain pending.

AGPC-003 final QA/review fix `1e2bd0744b5213d5004c34aac028b9642cc60028`
passed the full Python suite (774 tests with zero failures or errors), all 15
explicit Spec 046 validator commands, and affected-surface production (822
paths, 22/22 surfaces, 22 validators). The exact 12-path staged and affected
lanes passed, as did the repository aggregate with its unique PASS marker,
staged and all-files pre-commit without formatter mutation, and both diff
checks. Scoped Ruff was clean for every amended Python file; four E702
findings remain only in unchanged
`scripts/validate-active-corpus-eligibility.py` and were independently
adjudicated non-blocking for this fix diff. Initial whole-branch requirements
review found one current-owner issue, initial quality review found one
pathname-reopen TOCTOU issue, and independent security review found no blocking
issue. The final fix resolved those findings and two branch-introduced Ruff
findings; one scoped re-review approved all three original findings as resolved
with no new blocking finding. Provider/runtime, hosted, actual-evaluation,
remote, and live results remain `DEFER` or `ABSENT`; AGPC-004 and AGPC-005
remain pending.

Decision-readiness activation `ff66dd933e00def085b4c0319a67c6651356b116`
used the governed `draft -> active` edge for ADR-0019 and the program
agent-design while retaining accepted ADR-0013 as the current decision. It
reconciled the fixed `2026-07-10T10:00:00+09:00` /
`2026-07-10T01:00:00Z` source cutoff across current program authorities and
updated five source-bound predecessor digests. The exact 14-path unit passed
closure 28/28, staged lifecycle, strict documents, affected 22/22, the full
repository aggregate, staged pre-commit, Ruff, both diff checks, independent
requirements `COMPLIANT`, and quality/security `APPROVED`. This postflight
records the observed activation SHA; it does not accept ADR-0019 or make it the
current decision.

The closure design preserves working short-term, durable long-term,
domain-scoped, and provider-local auxiliary memory as the four classes. It
also distinguishes configured provider model/reasoning completeness from
actual evaluation, fitness, admission, and promotion.

## Traceability

- **Spec**: Agent Governance Program Closure
- **Plan**: Agent Governance Program Closure Implementation Plan
- **Successor state**: repository-local closure, local merge, and worktree cleanup

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [AGPC-000](../plans/2026-08-01-agent-governance-program-closure.md#work-breakdown) | Done | Activation `c6bae022`; exact eight paths, sole parent `06039611`, staged lifecycle/runner, strict docs, staged/all-files pre-commit, and diff PASS. |
| [AGPC-001](../../03.specs/046-agent-governance-program-closure/spec.md#success-criteria--verification-plan) | Done | Implementation `c4457fa0`; closed contract/schema/fixture/validator/tests, exact ten-path staged lane, full pre-commit, focused 28/28, Ruff, diff, and both independent reviews PASS. |
| N/A — AGPC-002 shares the Plan and Spec sources above | Done | Implementation `4fdea6a0`; one CI job, 18 delegated checks, 22/22 surface-validator inventory, exact 12 closure routes, 20-path staged/aggregate/pre-commit PASS, and final reviews approved. |
| N/A — AGPC-003 shares the Plan and Spec sources above | Done | Final fix `1e2bd0744b5213d5004c34aac028b9642cc60028`; 774-test suite, 15 Spec 046 validators, affected/staged/aggregate/all-files/Ruff/diff PASS, and scoped re-review approval with no blocking finding. |
| N/A — AGPC-004 shares the Plan and Spec sources above | Pending | Reciprocal closure and postflight pending. |
| N/A — AGPC-005 shares the Plan and Spec sources above | Pending | Local merge and cleanup pending. |
