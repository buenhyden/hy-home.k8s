---
title: "Final verification and handoff"
version: "0.1.2"
type: "sdlc/task"
status: "completed"
owner: "platform"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0102-TSK-0008"
---

# Task: Final verification and handoff

## Overview

Execute WP-007 of the approved [Plan](../plan.md). The request owner approved
the Spec and ADR, then approved Plan execution on 2026-09-29.
The current session implements this bounded unit under its assigned role;
the final branch received independent review; all findings were closed.

## Inputs

- [Spec](../spec.md)
- [Plan and work breakdown](../plan.md#work-breakdown)
- [ADR-0047](../../../02.architecture/decisions/0047-agent-contract-and-resource-ownership.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-008 | VAL-ACS-011, VAL-ACS-030, VAL-ACS-033 | WP-007: Final verification and handoff | platform | Completed | 23 full QA gates passed; independent review closed; external DEFER retained | This Task |

## Approval and Safety Boundaries

- **Allowed Paths**: exact files and owner delegation in WP-007 of the linked Plan; this Task
- **Forbidden Paths**: retained historical bodies, personal/global configuration, credentials, live resources, unrelated changes
- **Approval Required**: Plan execution and logical local commits approved; push, PR, merge, live changes and governance-steward self-entry remain separately operator-owned
- **Static Validation**: Plan command set C7, affected QA, exact-index staged QA, normal Git hooks; final full QA in TSK-0008
- **Live Validation**: DEFER; no authorized runtime session
- **Secret / Vault Handling**: no secret values read, printed or retained
- **Rollback Plan**: reverse this unit's reviewed logical commit together with its consumers, after dependent changes are reversed; preserve unrelated work
- **Evidence Location**: this Task

## Verification Summary

Repository-static verification completed. Branch `codex/agent-contracts`, initial base
`efc3643fdce17e0c5f454c3046e7ec8a3c37d13d`. Next owner: the request owner/operator for the separately reserved R35 and
external DEFER items. Static evidence
never establishes hosted, provider, account-limit or live behavior.

### Snapshot and review

Scope is local branch `codex/agent-contracts`, base
`efc3643fdce17e0c5f454c3046e7ec8a3c37d13d`; approved implementation and logical
local commits only. No push, PR, merge, global configuration or live mutation.
Observed tools: Python 3.12.3, Git 2.43.0, pre-commit 4.6.1.

Independent reviewer `final_contract_review` read the implementation and security
boundaries without editing. Initial result: no Critical finding; one Important
R23 gap for URL autolinks and relative/absolute plain paths. Added three RED
cases, repaired the shared extraction path, and all 38 link/document-routing
tests passed. Independent bounded re-review found no remaining Critical/Important/Minor issue and ran eight focused checks successfully.
No permission widening or secret exposure was found in the initial review.

The Plan's C1–C6 command sets and each unit's RED/GREEN evidence are recorded in
Tasks 0002–0007. WP-004 staged QA had 13 gates, WP-005 had 9; exact counts follow
selection, not the previous broader change set. Final static results are
recorded below; external DEFER items are not counted as PASS.

The first final staged candidate found two further owner/navigation errors:
root README exceeded its deep-link budget, and the shared executable-reference
checker treated a synthetic response's old command as current guidance. The
README now routes through the agent root; the shared checker excludes only
response data, with a RED/GREEN test proving the owner README remains current.
A separate RED/GREEN profile test gives the new evaluation README document gates
while cases/responses remain evaluation data. The first full run was interrupted
with exit 130 after this new mapping defect was identified; it is not PASS.
The final narrow re-review found no Critical/Important/Minor issue and passed
three focused data/README/route checks. The corrected candidate passed all
15 staged gates over 104 changed paths, then was committed as `c80fd050`.
That candidate used tree `f313097650d0429054307e7d47ca2690273b5346`;
its unit-test budget is the existing central 2,400 seconds, unchanged.
No percentage line-coverage or provider-quality claim is made.

The completed full attempt on the corrected candidate returned 1: 21 gates
passed, while unit-tests and pre-commit failed. The unit failures were the normal
and isolated CLI variants of one migration fixture that omitted the new required
skill owner registry/checker files; the fixture now supplies real registered
owner inputs. Markdown lint found two extra blank lines, repaired at source.
Independent security review verified both secret-scanner warnings as non-secret:
operator-approval prose and the exact digest of its declared public manifest.
The prose was clarified and the checksum uses the existing admitted integrity
metadata layout. No scan rule, baseline, allowlist or threshold was widened.
These failures remain recorded. The required fresh full run passed after the repairs.

### Final verification result

The final implementation snapshot is commit `a8c483de`, tree
`27e091cf2112535ba7490b65e3fbd34f9e4ad62b`. The branch keeps all logical commits;
no history rewrite, remote action or live operation occurred.

| Check | Actual result | Scope / limit |
| --- | --- | --- |
| `python3 -m unittest tests.test_affected_surface_migration` | Exit 0; 16 tests passed | Both normal and isolated CLI fixture variants preserve NUL inputs/output |
| `pre-commit run --all-files --hook-stage manual` | Exit 0; all selected hooks passed | Includes both secret scanners, Markdown, Python, workflow and manifest lint |
| `python3 scripts/qa.py quick` | Exit 0; 8/8 gates PASS | Six repair/evidence paths, working-tree snapshot |
| `python3 scripts/qa.py staged` | Exit 0; 8/8 gates PASS | Same six paths, exact-index snapshot, before `a8c483de` |
| `python3 scripts/qa.py full` | Exit 0; 23/23 gates PASS; no SKIP/DEFER | All 1,251 paths in the immutable implementation snapshot |
| Full unit-test gate | Exit 0; complete stdout/stderr and cleanup | `python3 -m unittest discover -s tests -t .`; actual full suite, not only repaired tests |
| Full pre-commit gate | Exit 0; complete output and cleanup | All files in the same full-QA snapshot |
| Independent final review and bounded repair reviews | No unresolved Critical/Important/Minor finding | Correctness, security, owner routing and fixture repairs; no native/live verdict |

The final full run log is `/tmp/hy-home-k8s-final-full-repaired.log`; the durable
result and reproducible snapshot are recorded here. This final evidence update
changes only Tasks 0007/0008. Its separate quick/staged results and actual
message validation are recorded in the closing commit message, after execution.
No further implementation change follows the full PASS.

### Original scenario dispositions

`PASS static` below means the listed focused check or explicit manual review,
not native enforcement. C1–C7 are the Plan's exact command sets. All tests run
with the Python version above. External DEFER remains incomplete until the named
owner can observe the stated environment.

| Scenario | Actual evidence / disposition | Deferred owner and retry trigger |
| --- | --- | --- |
| T01 | PASS static: C2 reachable nested references/scripts/assets and exact gate owner | None |
| T02 | PASS static: C2/C3 escape, symlink, malformed/unsafe input negatives | Native permission enforcement: operator, authorized provider session |
| T03 | PASS static: central gate/owned checker/shared helper review; C2/C5 | None |
| T04 | Manual trigger review: direct selectorless audit and paraphrased database/OTLP contract request select the new explicit skill; general Argo diagnosis routes to gitops-workflow; ambiguous live health asks for scope. No automatic-selection experiment | Provider discovery/automatic selection: operator, fresh trusted session |
| T05 | PASS static: required failure/timeout/skip aggregation tests in C2/C4/C5 | Account/tool availability outside this checkout: operator, actual environment |
| T06 | PASS static: C3 malformed input and bounded diagnostics; C4/C5 cwd and timeout/partial-output tests | Native invocation: operator, fresh session |
| T07 | PASS static: C1 normalized links; final autolink/relative/absolute regression repair | None |
| T08 | PASS static: C1 README/docs-internal and exact machine exceptions | None |
| T09 | Manual review: current individual-stage authority callers converted to current owner/README; machine exceptions exact; retained examples unchanged | Semantic review is bounded to changed/current consumers, not a general NLP guarantee |
| T10 | PASS static: C5 registry/projection/role matrix; 17 role dispositions in Task 0006 | Native delegated sandbox inheritance: operator, provider session |
| T11 | PASS static: C5 manual projection parity, model overrides and unsupported-model negatives | Native resolved model: operator, authenticated session |
| T12 | PASS static: all 54 hook regression cases including isolated linked-worktree fixtures | Native hook delivery: operator, installed trusted hook session |
| T13 | Static configuration reviewed; native CLI trust/discovery/model/sandbox/hook observations DEFER | Operator, fresh authorized provider sessions |
| T14 | Manual resume decision matrix in Task 0005, not an implemented approval authenticator | Native stop enforcement: operator, recorded interrupted/resumed session |
| T15 | PASS static: C4 fact hash/expiry/deletion/review/sensitivity checks; promotion/cache obligations manually reviewed | Cross-session derived-cache behavior: operator, recorded session |
| T16 | PASS static: C5 index/commit contracts; explicit Commitizen on actual messages; normal configured hook chain invoked | Workspace hook files absent: no workspace pre-commit/commit-msg delivery claim |
| T17 | DEFER: no observed editor installation or command consumer; no settings invented | Operator, actual editor/extension/OS and scoped request |
| T18 | Manual synthetic response contract review in Task 0006; no runtime quota enforcement claimed | Operator, measured account and recorded rate/retry/concurrency observation |
| T19 | PASS static: C5 CI trust/required-check fixtures; five workflow dispositions | Hosted checks/ticket integration: operator, approved remote consumer |
| T20 | PASS static: C6 frozen 19 expectation sets, 12 negatives, byte-preserved responses and single moved runner | Model quality is not established by synthetic data |
| T21 | PASS static/manual: Task lifecycle, current owner disposition and resume contracts; no archived success rewriting | Operator-only self-entry still DEFER |
| T22 | PASS static/manual: new skill gap, consumer protocol references and C3 join tests; primary source links in owned reference | Live availability/authentication: operator, scoped live approval |
| T23 | PASS static: C5 sidecar/symlink/projection/CI routing; no new generator or distribution mode | Different-product distribution: operator, actual target and scope |
| T24 | PASS static: no network/cluster/secret-value operations in checker and prompt tests; read-only review | Live service/cluster validation: operator, separate scope |
| T25 | PASS static: C4 bounded eight-field provenance, tracked source/hash/currentness | Future refresh at source/scope/approval/validity change: knowledge owner |
| T26 | PASS static: C4 prompt missing/type/command/cwd/overflow/timeout and no-write checks; four adapter review | Native adapter delivery: operator, session observation |
| T27 | Manual shared result fields/provider precedence review; unsupported style not invented | Native style behavior: operator, supported provider observation |
| T28 | PASS static for 16 operator-unrestricted roles; role map and permissions preserved; R35 self-entry DEFER | Operator, explicit governance-steward own-entry scope |
| T29 | PASS static: C2/C3 all 17 prior skills plus new skill dispositions, owned resource transition | Native invocation: operator, fresh session |
| T30 | PASS static: C5 17 IDs/51 projections and removed skill-reference callers; no role rename/deletion | Runtime agent_type/permission inheritance: operator, session |
| T31 | Manual two common workflows and five hosted workflow dispositions; C5 required-summary fixtures | Remote branch protection: operator, approved hosted observation |
| T32 | PASS static: C4/C5 args/help/cwd/failure/timeout and four adapter caller review | Editor/native command delivery: operator, observed installation |
| T33 | C6 new path consumers and baseline equality passed; C7 full QA passed all 23 gates | Native/hosted/live lanes remain separately DEFER |

### Criterion evidence routing

Each criterion retains its original meaning. Combined static/DEFER rows are not
reported as unconditional acceptance. R35 remains incomplete because the Plan
reserves the governance-steward self-entry for the operator; the Spec and Plan
remain active until that dependent criterion is resolved.

| Criterion | Original scenario evidence | Current disposition |
| --- | --- | --- |
| VAL-ACS-001 | T10, T28 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-002 | T03, T04, T22, T29 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-003 | T21 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-004 | T12, T24 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-005 | T10, T30 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-006 | T25 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-007 | T26 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-008 | T21, T26, T31 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-009 | T06, T32 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-010 | T27 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-011 | T03 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-012 | T01, T02, T04, T05, T06, T24, T29 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-013 | T11, T13, T30 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-014 | T14, T15, T25 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-015 | T11, T12, T23, T30 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-016 | T13, T27 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-017 | T16, T32 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-018 | T17, T32 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-019 | T05, T18 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-020 | T12, T16, T19, T23, T24, T31 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-021 | T19 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-022 | T14, T15, T26 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-023 | T07, T08, T09 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-024 | T04 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-025 | T01, T02 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-026 | T01, T02, T03, T29 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-027 | T04, T22, T29 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-028 | T10, T28 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-029 | T10, T22, T30 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-030 | T21, T24 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-031 | T07, T08, T11, T13, T23 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-032 | T20 | See scenario dispositions above; static checks passed, explicit DEFER retained |
| VAL-ACS-033 | T09, T21, T25, T33, T05, T06 | See scenario dispositions above; static checks passed, explicit DEFER retained |

### Logical commits, rollback and next owner

| Unit | Local commit | Reversal dependency |
| --- | --- | --- |
| Authored package | `8e811506` | Last, after dependent implementation and activation |
| Approved activation | `79c97514` | After implementation is reversed |
| R23 document authority | `1a6e089e` | After consumers and later normalization repair |
| Skill resource owner | `f9e0dafa` | After the new checker and its gate |
| External service checker | `025ada90` | After consumers and later role dispositions |
| Knowledge/prompt bounds | `68fd0d64` | After dependent handoff/evidence updates |
| Role/provider fit | `0442efc7` | After evaluation consumers |
| Evaluation cutover and review repairs | `c80fd050` | Reverse with moved corpus, grader and every consumer together |
| Final fixture and evidence-format repairs | `a8c483de` | Reverse before the affected checker-owner contract |

Rollback is a reviewed reverse sequence preserving unrelated changes, not an
authorized reset, forced push or live rollback. The worktree and local branch
remain available for review. The request owner/operator owns R35's separately
reserved self-entry and all native/hosted/live follow-up; the reviewer owns any
new finding, routed back to the owning WP before another implementation change.
The Spec/Plan remain active because dependent R35 acceptance is still DEFER.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-008](../plan.md#work-breakdown) | Completed | Independent findings closed; full QA 23/23 PASS on `a8c483de`; final record receives its own staged check before commit |
