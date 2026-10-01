---
title: "Integration, review, and handoff"
version: "0.4.0"
type: "sdlc/task"
status: "completed"
owner: "platform"
updated: "2026-10-02"
layer: "specs"
artifact_id: "SPEC-0103-TSK-0006"
---

# Task: Integration, review, and handoff

## Overview

Execute [Plan WP-006](../plan.md) against [SPEC-0103](../spec.md). This Task
completes the local integration handoff: implementation reconciliation, the final
script/test audit, independent review and repository-static validation evidence.
Protected hosted activation remains DEFER; the Spec and Plan stay active, and
Tasks 3–5 stay in progress. No local result establishes remote enforcement.

## Inputs

- [Plan](../plan.md), [Spec](../spec.md), [REQ-0003](../../../01.requirements/0003-workspace-agent-governance-platform.md),
  and [quality policy](../../../../.agents/governance/quality.md).
- [Task 1](tsk-0001-local-evidence.md), [Task 2](tsk-0002-delivery-and-github.md),
  [Task 3](tsk-0003-protected-proof.md), [Task 4](tsk-0004-main-reuse.md),
  [Task 5](tsk-0005-main-tags.md), and [Task 7](tsk-0007-test-disposition.md).
- Criteria: VAL-QER-001–012. Profile: `sdlc/task`; form:
  `docs/99.templates/templates/specs/task.template.md`.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-006 | VAL-QER-001–012 | Reconcile final local validation, independent review and hosted deferrals | platform | Completed | Local integration handoff complete; hosted activation DEFER | Criterion, disposition and snapshot tables below |

## Approval and Safety Boundaries

- **Allowed Paths**: this Task; Spec/Plan lifecycle metadata; explicitly delegated
  stale review/evidence lines in Tasks 1/2; Task 7 historical-census wording;
  the stale Requirement navigation adjective, GitHub hub and branch-protection
  guidance.
  Implementation defects return to their owning Task through the controller.
- **Forbidden Paths**: implementation/workflow/test changes; private credentials,
  global hooks, archived bodies, live Kubernetes/Vault resources and unrelated work.
- **Approval Required**: this document worker performs no push, PR, merge or
  cleanup; the controller handles delivery under the existing user authorization
  and Git policy. App/environment configuration, remote settings, rulesets and
  tag activation still require their operator-owned authorization and evidence.
  No external mutation occurred in this Task.
- **Static Validation**: frozen full QA attempts on distinct recorded inputs;
  final discovery census without test execution; affected quick and exact-index
  staged QA per document commit;
  whitespace, document/schema/links and actual-message checks with active hooks.
- **Live Validation**: DEFER with operator/PR owner and retry triggers below.
- **Secret / Vault Handling**: no private values read or recorded. Setting names,
  intended permission ceilings and static references are not installed settings.
- **Rollback Plan**: operator disables tag publication and reuse first, retaining
  full main QA and required protection; forward-revert reviewed implementation
  units in reverse dependency order. Never move/delete tags or rewrite history.
  Task-only wording corrections can be reverted as their own logical unit.
- **Evidence Location**: this Task and linked owning Tasks; ignored handoff report
  `.superpowers/sdd/plan/task-6-report.md` records the final document commit identity
  without a self-SHA rewrite loop.

## Verification Summary

### Initial full snapshot and repaired input

Branch `codex/qa-evidence-implementation`, clean HEAD
`7ef7c3a945390bc98272a3103bad72afcbb85e9c`, tree
`ca1f11d0c6031addbd0359a30be28b93d728151a`, diverges from
`0ed105b832d85c88b1000ad58959531d1ae23cae`. The initial full branch diff contained 44 paths. That frozen full QA failed
as recorded below. The authorized repair is now committed at
`0820ee0ef015d45edd4e6919e3f0d1c7f5c3deba`, tree
`bd10d2eb1cd8f1cd04b5fd120f61f960015b4a42`; the resumed checkout was clean.
The later scanner-fixture repair is `b8438e5736c3445c1bd137fd580556a722eebe3a`.
This handoff changes documentation only. Its quick/staged evidence is separate
from the controller-coordinated final full run on the repaired near-final input.
No unchanged full/unit/manual-pre-commit aggregate is repeated independently.

The final registry has 23 unique full IDs and `ci` aliases `full`. PR CI derives
one isolated `agent-evaluation-cases` gate plus its 22-gate complement; main/manual
fallback executes 23, and authenticated main reuse executes 22 plus one REUSED.
The [Task 4 gate matrix](tsk-0004-main-reuse.md#per-gate-disposition-matrix) names
every ID. `unit-tests`, archive/history/GitOps gates and manual pre-commit always
execute on main. No test partition or aggregate-unit reuse is introduced.

The current local opt-in is also `agent-evaluation-cases`, whose stdlib import
closure replaced Task 1's initial external-service candidate after dependency-byte
review. Local identity binds exact whole-tree bytes/modes, path scope, argv,
configuration, interpreter/distribution metadata, closed environment, HEAD,
base and named refs. Its mode-0600 atomic cache is a same-user local optimization;
full/CI never use it. The provider-looking runner-candidate negative test retains
execution and failure propagation instead of accepting a fabricated source string.

PR record v1 remains parseable but its unattested shared runtime cannot authorize
hosted reuse. Current protected PR proof is v3, with an isolated immutable image,
raw committed checkout and job/input identity. Main v2 means 23 fresh PASS results;
v4 means 22 PASS plus one independently reauthenticated original PR result.
Main records cannot become PR sources. App author, exact run/attempt/job, durable
merge checkout, entire PR/push control history and complete registry union are
required; artifacts, QA logs and green names are not authority.

### Criterion and requirement reconciliation

The local column maps retained runnable evidence; owning Tasks record its prior
focused results. The first two full attempts remain FAIL; the third frozen run
passed all 23 repository-static gates on the repaired input. This completes the
local handoff, while every named hosted/settings DEFER remains open.
Requirement lineage is the full stable ID in the owning Spec's traceability table.

| Criterion | Requirement lineage | Local evidence | Hosted/settings disposition and retry owner |
| --- | --- | --- | --- |
| VAL-QER-001 | REQ-0003-FR-0016; REQ-0003-NFR-0002 | `test_validation_profiles`, `test_validation_tooling_ownership`, hosted partition test: one registry; 23 unique IDs; disjoint 1+22 union | No remote claim required for registry ownership |
| VAL-QER-002 | REQ-0003-FR-0016; REQ-0003-FR-0028; REQ-0003-NFR-0002 | `test_qa_runner`, `test_run_validation_lane`: exact repeat/quick-to-index execution counts; same-path bytes/modes, untracked/formatter/config/tool/scope/history changes invalidate; invalid cache/missing tool executes | Local-only optimization; never offered as hosted evidence |
| VAL-QER-003 | REQ-0003-FR-0018; REQ-0003-FR-0026; REQ-0003-NFR-0002 | `test_ci_qa_workflow`, policy/PR-template contract and document quick/staged/full evidence: PR hosted full owns PR delivery; local-only handoff owns local full | DEFER PR owner: create an authorized PR, then retain exact SHA and `ci-summary` run/attempt |
| VAL-QER-004 | REQ-0003-FR-0017; REQ-0003-FR-0026 | `test_qa_provenance`, `test_qa_provenance_hosted`: actual synthetic checkout, successful complete partitions, isolated mutation denial, bounded malformed/expired proof and App author | DEFER operator: authenticated App/environment/source read-back and successful v3 PR trial, including hostile mutation |
| VAL-QER-005 | REQ-0003-FR-0017; REQ-0003-FR-0026; REQ-0003-NFR-0004 | Hosted-proof merge/squash/rebase/multi-commit/before-anchor, changed-tree/runtime/lock/ref/history fixtures; 23 fallback or 22+1 authenticated routing | DEFER operator: activated source check, real merged PR/main source relationship and exact v2/v4 main verdict trial |
| VAL-QER-006 | REQ-0003-FR-0018; REQ-0003-NFR-0002 | Final loader census 59 modules / 1,365 unique cases / zero errors; `unit-tests` stays whole and always executes; partition count fixture | Hosted discovery must be observed with final PR run; no aggregate reuse is enabled |
| VAL-QER-007 | REQ-0003-FR-0017; REQ-0003-FR-0028; REQ-0003-NFR-0004 | Missing/cancelled/failed/forged/expired/ambiguous source, wrong App, every-commit control edit/revert including `.gitattributes`, runner spoof and failing-summary tests | DEFER operator: hostile PR/name-spoof and control-transition trial after protected App setup; main remains full until activation |
| VAL-QER-008 | REQ-0003-FR-0017 | Actions security, verifier ceiling/key-order tests, independent static security review; default-off guards and separate read-only lookup | DEFER operator: main-only `qa-control`, exact installation ceiling and App-ID-pinned required check, denial/hostile trial; static workflow references prove none of those settings |
| VAL-QER-009 | REQ-0003-FR-0017; REQ-0003-NFR-0002 | CI event/branch/isolated-summary tests and full/CI marker-process counts 23/23/22; ordinary feature push adds no hosted full; manual full and no tag | DEFER PR owner/operator: observed event matrix on approved hosted runs |
| VAL-QER-010 | REQ-0003-FR-0029 | `test_publish_main_tag` 20 cases: independent exact v2/v4 App verdict, separate App, main-tip-only creation, authenticated retry/noop after main advances, conflict/concurrency/failure/no force, local update/delete denial; workflow tag-filter tests | DEFER operator: separate publisher installation and main-only `qa-tag-publish`, complete two-ruleset/bypass read-back, normal token denied update/delete, exact-SHA publication and same-target retry |
| VAL-QER-011 | REQ-0003-FR-0030 | Task 2 script audit plus final additions and all GitHub surfaces below; manifest missing/empty negatives, separate scanners, updated delivery and control guidance | Task 2 records authenticated 2026-10-01 destination/label/private-reporting state; refresh and fork-labeler/private-report UI observation DEFER to operator at delivery |
| VAL-QER-012 | REQ-0003-FR-0030 | Task 7 preserved-negative retirement proof plus final 59-module/1,365-case census and added-module audit below; no later removed tests or unique failure meaning | Repository-static audit; hosted execution remains separate under VAL-QER-003/009 |

### Final script and GitHub surface disposition

Task 2's full active-script table remains the one-time baseline. Its standalone
archive quick/staged caller, manifest presence checks, global-before-workspace hook
chain, security scanners and history readers retain distinct meanings and callers.
No script is retired. The imported validation libraries continue through their
existing CLI owners; no second execution inventory is introduced.

| Added or changed execution owner | Actual caller and distinct contract | Disposition / tests |
| --- | --- | --- |
| `qa.py`, `run-validation-lane.py`, registry/schema, affected selector | Local hooks/profiles and CI; exact snapshots, bounded subprocess verdicts, local evidence and registry-derived complement | Keep; runner/profile/ownership/negative identity tests |
| `qa_provenance.py` | Protected verifier authenticate/publish; hosted lookup and publisher import it | Keep; bounded provider authentication, control history and narrow App check token; provenance tests |
| `qa_provenance_records.py` | Protected verifier imports parser; publisher uses it through verifier | Keep; closed v1/v3 PR and v2/v4 main schema/size/age/type separation; provenance and publisher malformed-record tests |
| `qa_provenance_hosted.py` | CI isolated job and read-only source lookup; QA partition and verifier import | Keep; raw checkout/runtime identity, 1+22 partition, original-before/source proof and conservative full fallback; hosted tests |
| `publish_main_tag.py` | Separate protected main publisher job | Keep; authenticated exact-tip create/noop and restricted writer token; publisher tests |
| `validate-ci-python-contract.py` | Registry `ci-python-contract` | Keep; exactly three mutually exclusive direct QA commands, locked dependencies and checkout contract; missing/duplicate/overlap negatives |

All 18 tracked `.github/` files were inspected. The CI and verifier workflows
retain separate ordinary QA, read-only lookup, verifier-App and publisher-App
roles. Greetings, labeler, stale maintenance and version-tag changelog remain
non-QA functions; changelog artifact retention remains seven days. Action pins,
branch-only QA push filtering, separate tag trigger, workflow concurrency and
job-local write permissions remain visible to the existing Actions security gate.
No `pull_request_target`, PR key access or workflow commit push was added.

The dependency input/lock still owns the three direct validation pins. CODEOWNERS
remains ownership guidance, with required enforcement separately unobserved.
Bug/feature issue forms retain their distinct inputs; the issue contact points to
documentation, Dependabot uses `github_actions`, cluster labels use `area/gitops`,
and SECURITY points to private reporting. The PR template routes to quality
policy. The GitHub hub describes all six workflows and the default-off publisher.
The branch-protection note preserves its dated observed settings while correcting
current CI dependencies and linking the protected activation boundary. No remote
settings are inferred from that note.

### Test disposition since Task 7

Task 7's 56-module / 1,288-case final census belongs to its recorded historical
snapshot. At initial HEAD and repaired `0820ee0e`, the exact registry discovery argv remains
`python3 -m unittest discover -s tests -t .`. A nonexecuting loader census found
59 modules, 1,365 cases, 1,365 unique IDs and zero loader errors. The original
56 modules remain. Tasks 3–5 add 77 cases: 66 in three new modules and 11 in
existing modules. The integration repair removes one obsolete count-only
assertion and its unused YAML import, while preserving and renaming the same
rename-range test case. No discovered case, fixture or standalone caller is lost;
the authoritative command-partition negative checks remain in the CI contract suite.

| Module (caller: full/CI unit discovery) | Task 7 → final cases | Distinct failure meaning / decision |
| --- | --- | --- |
| `test_qa_provenance.py` | 0 → 29 | Retain: actual checkout versus head, fork lookup, all-commit control closure, bounded schema/API, isolated mutation, App ceiling/key order, full main and PR/main proof separation |
| `test_qa_provenance_hosted.py` | 0 → 17 | Retain: exact raw tree/index/modes, runtime, partitions, merge/rebase/before anchors, historical fork/stale/ambiguous source, wrong App and full fallback |
| `test_publish_main_tag.py` | 0 → 20 | Retain: exact independent main proof, separate App, create/noop/conflict/concurrency, advanced-tip retry, denied local update/delete and token lifecycle |
| `test_ci_qa_workflow.py` | 14 → 20 | Retain: workflow source/environment entry, distinct publisher access, tag event filters, push-before and isolated summary failure |
| `test_qa_runner.py` | 39 → 41 | Retain: tree equality cannot substitute Git/ref identity; full/CI/complement gate execution counts and failed-gate propagation without nested full QA |
| `test_run_validation_lane.py` | 74 → 75 | Retain: provider-shaped unauthenticated candidate never skips a failing child |
| `test_validate_ci_python_contract.py` | 70 → 72 | Retain: exact partition forms; missing/duplicate/overlapping/unconditional commands rejected |
| `test_validation_profiles.py` | 20 → 20 | Retain adapted candidate assertion: current registry opt-in is stdlib evaluator; no discovered case removed |
| `test_validate_affected_surfaces.py` | 11 → 11 | Retain rename-range semantics as `test_ci_rename_range`; retire only obsolete one-command assertion, now owned by canonical mutually exclusive CI-partition negatives |

The remaining 50 module case counts match Task 7. Standalone Conftest negatives,
19 synthetic agent evaluation cases and six archive early-check modules remain
owned as recorded there. Parser tests, provider-authentication tests, writer tests
and workflow tests exercise different trust boundaries, not equivalent assertions.
The 929-line provenance test module is retained: its independent PR/main and
credential-denial families have no proved replacement. Size alone does not justify
deleting coverage. No new permanent inventory or speculative test split is added.

### Review and delivery evidence

Independent whole-branch reviews inspect `0ed105b8..7ef7c3a9`:
`task6_whole_security_review` returned repository-static security PASS with hosted
DEFER. `task6_whole_code_review` found no code defect, but requested the latest
test census/dispositions (MEDIUM) and correction of the hub claim that ci-summary
checks the qa-source result (LOW). This handoff adds the census and corrects the
hub: qa-source is an ordering dependency; required result checks are branch-policy,
qa and qa-isolated. Scoped review of the first document commit `3d3d10bb`
returned Spec PASS / quality Approved from `task6_whole_code_review`, with both
findings resolved; `task6_whole_security_review` reported no findings. These
review results are separate from the successful final full QA recorded below.

Authenticated read-only GitHub observations supplied by the controller on
2026-10-02: repository environments, rulesets and Actions variables lists were
empty; no verifier/publisher App secret name was present. Main protection required
only `ci-summary` from App ID `15368`, with strict checks enabled and code-owner
approval disabled. These observations support inactive hosted DEFER, not protection
readiness. No credential values or raw API payload are retained. Re-read all
required effective settings and installation identities at operator activation.

The initial `python3 scripts/qa.py full` on `7ef7c3a9` returned exit 1:
21 of 23 gates PASS, `unit-tests` and `pre-commit` FAIL, scope
`all-files:paths=1268`. Unit discovery failed only
`test_ci_workflow_and_rename_range` with `AssertionError: 3 != 1`: an older
count assertion contradicted the reviewed three mutually exclusive QA commands.
The pre-commit gate failed detect-secrets (hook rc=3) after changing baseline
line metadata in the isolated snapshot; QA also rejected snapshot mutation.
Both failed gates completed their pipes and cleanup. This is retained FAIL,
not a passing baseline; an initial tail-only 22/23 report was corrected against
the complete log to 21/23.

Repair `0820ee0e` changes only `tests/test_validate_affected_surfaces.py` and
`.secrets.baseline`. The obsolete command-count assertion and unused YAML import
were removed; rename-range behavior remains. The canonical CI validator tests
already reject missing, duplicate, overlapping and unconditional partitions.
Owner-reported RED reproduced 3 != 1; GREEN focused 3/3, affected module 11/11,
quick 3/3 and staged 3/3 passed. Independent `task6_whole_code_review` accepted
the repair. Scanner-generated baseline updates changed two line numbers to
155/165 and its generation timestamp; fingerprints, types and dispositions
stayed identical. The focused detect-secrets hook returned rc=0 without changing
bytes, combined staged passed 3/3, and `task6_whole_security_review` accepted
that metadata-only repair. No secret was added, exposed or allowlisted.

The first document commit `3d3d10bb83df88f8a260507014101fef63edfd4b`, tree
`4e0bc0baa5f195b387aacd9c5bedb6ce27ea7cc7`, passed affected quick and exact-index
staged 6/6 across nine documentation paths. Both selected agent-governance,
document-contract-registry, document-lifecycle, links-and-owners,
markdown-profiles and repository-quality. Markdown lint, whitespace and the
actual Commitizen message check passed; normal active hooks were preserved.

A second frozen `python3 scripts/qa.py full` on that clean commit returned exit 1,
scope `all-files:paths=1268`: 22 of 23 gates PASS and `pre-commit` FAIL. Unlike
the initial run, `unit-tests` passed and no snapshot-mutation diagnostic appeared;
source HEAD/tree stayed unchanged and the worktree remained clean. All 23 gate
records matched registry order and had complete stdout, stderr and cleanup.
The pre-commit gate returned rc=1, with detect-secrets hook rc=1. The bounded log
is `/tmp/qa-task6-final-full.log`; it is local diagnostic evidence, not hosted proof.

Sanitized diagnosis located a Secret Keyword candidate at
`tests/test_publish_main_tag.py:612`. Independent security AST review confirmed
that the key-order fixture uses a six-character lowercase dummy for
`QA_PUBLISHER_PRIVATE_KEY`, not a credential. The initial hook rc=3 and snapshot
mutation did not establish absence of this separate candidate: partition return
code aggregation could have masked rc=1. The earlier baseline-only repair and
focused check therefore did not prove the whole all-files scanner would pass.

Task 5 repair `b8438e5736c3445c1bd137fd580556a722eebe3a` adds only an exact inline
scanner allowlist pragma on that dummy fixture line; no baseline entry, broad
exclude or runtime behavior changed. Owner-reported detect-secrets GREEN,
publisher suite 20/20, quick 3/3 and staged 3/3 passed. Controller-reported
independent code review returned Spec PASS / quality Approved and security
review PASS. Both failed full attempts remain recorded FAIL; the narrow repair
is not represented as a successful replacement full run.

The second in-progress evidence commit
`162e10f82fa34e5daa74cf8ca67eff5f659b62f5`, tree
`328a2d6390107879e97db6a808fdfdb3d1a456b9`, changed only this Task. Quick and
exact-index staged each passed the same six document gates listed above;
Markdown lint, whitespace and the actual Commitizen message check passed.
Independent `task6_whole_code_review` returned Spec PASS / quality Approved after
rechecking both failed full logs; `task6_whole_security_review` found no issue.
The normal commit preserved active hooks and left a clean worktree.

The final `python3 scripts/qa.py full` ran once on that frozen clean HEAD/tree
and returned exit 0, profile `full`, snapshot `working-tree`, scope
`all-files:paths=1268`. All 23 unique gate records matched the registry's full
membership and order: 23 PASS, zero FAIL/SKIP/DEFER/REUSED. This includes one
successful whole `unit-tests` discovery and one successful all-files `pre-commit`
invocation at the manual stage. Every gate returned rc=0 with complete stdout,
stderr and cleanup. The QA snapshot integrity check succeeded; no snapshot
mutation diagnostic occurred, source HEAD/tree stayed unchanged and the source
worktree remained clean. The bounded log is `/tmp/qa-task6-final3-full.log`.
This is local repository-static PASS; it establishes no hosted App, environment,
required-check, ruleset, denied-operation or tag-publication result. The two
previous failed runs and their corrective commits remain part of this evidence.

Tools: Python 3.12.3, pre-commit 4.6.1, RTK 0.49.0. Initial sandbox startup
failed before executing a command (`bwrap` network namespace setup); scoped
local commands used approved escalation. Existing `core.hooksPath` remained
`scripts/githooks`; no bypass or private/global configuration change occurred.
Task 6 is completed as a local integration handoff. This subsequent Task-only
completion record is outside the frozen full-QA snapshot; it uses affected quick,
exact-index staged, Markdown and actual-message validation plus independent
review. Its exact checks, review disposition and commit identity are retained in
the ignored Task 6 report. Quality policy step 6 permits this evidence-only
update without repeating unchanged full/unit/manual-pre-commit aggregates.
Final hosted PR validation still belongs to the controller/PR owner.
The controller owns review reconciliation; the operator owns every hosted deferral
in the criterion table.

Residual limitations: conservative whole-tree identity can reject valid reuse,
unattested shared QA cannot be reused, bounded/ambiguous provider lookup falls back,
and same-user local cache editing is outside the hosted trust boundary. The tag
publisher rechecks main before creation but the provider offers no atomic
compare-main-and-create operation; a race can tag the authenticated tested source
commit, never an unvalidated target. No automatic tag cleanup is authorized.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-006](../plan.md#work-breakdown) | Completed: local integration handoff; hosted DEFER | Criterion matrix, final script/test dispositions and checked snapshot above |
