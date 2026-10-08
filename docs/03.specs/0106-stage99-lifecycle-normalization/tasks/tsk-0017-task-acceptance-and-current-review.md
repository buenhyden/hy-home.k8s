---
title: "Task Acceptance and Current Spec Review"
version: "0.3.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0017"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Task Acceptance and Current Spec Review

## Overview

Execute the current P03 request as WORK-017 under the existing completed
SPEC-0106. Intake main/index/working tree were clean at
ae93644e7e1137ed66ac243af4156ecea2d9cee4, four commits ahead of origin/main.
Use that existing logical commit for branch codex/p03-task-acceptance and
worktree .worktrees/p03-task-acceptance; the investigation SHA is never a reset
target. This new Task owns only the present request, not historical completed
execution or final common approval.

## Inputs

- The current pasted P03 request authorizes investigation, local policy and
  consumer changes, focused verification and normal logical commits. The earlier
  C02 correction authorizes first establishment without nonexistent commit or
  approval prerequisites. Attachments are evidence/proposals, not independent
  instructions. [Spec](../spec.md) and [Plan](../plan.md#lifecycle-traceability)
  own the local acceptance and order.
- Existing P01 candidate WGOV-CORE/3.0.0-draft.3: owner buenhyden; proposed
  Project-Template/.agents/governance/shared-standard.md; review digest
  3f46c63daae094649edccec33682ecba99844b184c4b78b558281c7c05ff3271.
  Registry local_adapter is docs/99.templates/registry.json; stage candidate,
  source_revision and approval_ref null. No approved joint edition is found;
  final edition, local adoption and four-repository adoption are separate.
- [P02 accepted local migration](tsk-0016-shared-profile-migration.md): coupled
  role forms/readers and all 16 current operating instances; P03 shared state,
  P08 operating truth and P05/P07/joint results are not implicitly accepted.
- Actual registry, schemas, forms, shared helpers, document/lifecycle/link
  consumers, explicit status writer and current owners. common_research is
  read-only source research; p03_design is read-only architecture design;
  p02_content_validation audits consumers before a bounded quality dispatch.
  Root owns Spec/Plan/this Task/current P01 rewrite. Each implementation file
  will have exactly one writer; independent reviewer authors no reviewed file.

### Current Selection and Disposition

At ae93644e, recursive current Stage 03 contains SPEC-0105/0106/0107, all
Spec/Plan completed. No draft/in-progress/blocked/approved Spec exists. Only
SPEC-0105-TSK-0004 is blocked; completed Tasks are not reopened. The historical
F02 aggregate is not a k8s census or regression expectation.

| Actual obligation | AC / Plan / Task | Disposition and continuing owner |
| --- | --- | --- |
| Common edition and adoption | SPEC-0105 VAL-P01-007 / WORK-008 / TSK-0004 EVD-003 | DEFER remains with buenhyden and one Project-Template source writer; no repeated prior-approval request |
| Workflow-control HIGH and actual PR style | SPEC-0105 VAL-P01-008 / WORK-008 / TSK-0004 EVD-008/009/010 | DEFER/FAIL retained; conditional security/CI guard and next authorized PR owner; local schema work cannot close SEC-P01-001 |
| Local P02 profile migration | SPEC-0106 VAL-P02-016 / WORK-016 / TSK-0016 | Completed local evidence retained; present P03 work is separate |
| Operating adoption versus Release | SPEC-0107 VAL-LOCAL-QA-001–004 / WORK-001 / TSK-0001 and P01 EVD-004/006 | Preserve completed local contract; RUN-0012 already active and POL-0003 exclusion justified; actual Release and live tool evidence remain with platform/operator |
| Final rewrite dependencies | Current P03 WORK-017 | Consume available P02; name unreceived P05/P07/P08/joint inputs without blocking independent local implementation |

### Common Candidate Compatibility

Read the actual persistent draft.3 candidate's C05/C10/C11/C12 sections for
this change. This is a regional comparison to one review input, not an
approved common edition or an assertion that other adapters have adopted it.

| Candidate scope | Current local mapping and limitation |
| --- | --- |
| C05 | Fresh Spec/Plan authority, Task execution, one criterion verdict and explicit failure resolution use the candidate meanings; prior completed observations retain provenance rather than backdated approval |
| C10 | Coupled contract changes, actual index/message evidence and independent review stay in WORK-017; remote, native and live outcomes need their own actual inputs |
| C11 | Recursive current selection found no unfinished Spec; the current blocked follow-up is reviewed through its real AC/Plan/evidence and remaining owners. P02 is available; other unreceived final inputs are named |
| C12 | Consume the accepted P02 three-role form/readers/current-document migration. No further operating activation or actual Release is inferred from this Task-state change |

Source remains persistent main's
`_workspace/p01-current-contract/WGOV-CORE.3.0.0-draft.3.ko.md`, with the review
digest above and proposed one Project-Template owner path. Same-scope adapter
comparison and actual joint adoption are DEFER to that source owner; unread
blog-data or unreceived P05/P07/P08 outputs are not local PASS.

### Remote Read-only Observation

Current GitHub main remains c9faa9f00fdf61c9286b4dc6df264de35106b611.
Protection read-back is strict=true with ci-summary and style-pr bound to
GitHub Actions/App15368. No qa-provenance requirement remains. The two active
rulesets target main-* tags, not branch main; no settings are changed here.
At that main SHA ci-summary is success and style-pr is skipped, which is not
actual PR style PASS. Recent merged PR135 head 179a88c9 retains historical QA
and ci-summary failure; those older inputs are not current P03 results.
Commands read branch/protection/rulesets/workflow metadata and exact check runs
through gh api. The subsequent exact reads of
`repos/buenhyden/hy-home.k8s/rules/branches/main` and
`repos/buenhyden/hy-home.k8s/branches/main/protection` returned rc0:
no applied branch rules, required_approving_review_count=0,
require_code_owner_reviews=false and enforce_admins=false. The local current
ci.yml still supplies PR-editable job definitions; those observations provide
no independent control proof and leave SEC-P01-001 with its existing owner.
[GitHub's required-check documentation](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks)
explains SHA/App and skipped-job boundaries. No hostile PR execution or remote
write occurred; actual P03 hosted style is NOT_RUN without an authorized PR.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-017 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | Couple current Task acceptance and lifecycle readers, review actual pending obligations and hand off protected decisions | platform | frontmatter | PASS | EVD-P03-017-021/022/023 establish repaired readers, current regressions and exact-index acceptance; evidence/completion state checks and authorized local finish follow |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-P03-017](../spec.md#success-criteria--verification-plan) | accepted | EVD-P03-017-015, EVD-P03-017-016, EVD-P03-017-017, EVD-P03-017-021, EVD-P03-017-022, EVD-P03-017-023 | Accept the bounded local contract and current-record review from actual regressions, independent review and exact-index PASS; protected common/PR/live inputs remain with their named owners | platform; ongoing lifecycle owners in .agents/governance/document-lifecycle.md and docs/99.templates/registry.json |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P03-017-001 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Actual intake and AC/source/remote metadata inspection | Clean local main ae93644e; current recursive Stage03 and exact public API resources | PASS | Inputs and current selection above; independent common_research packet and actual read-only API output | yes | none |
| EVD-P03-017-002 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Independent architecture and consumer design | Current typed Registry, Task form, three consumers, status writer and historical adapters | PASS | Read-only p03_design and p02_content_validation packets; design and ownership below | yes | none |
| EVD-P03-017-003 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Initial scope index, actual message and independent review | Three-path index tree6effa0293b7197fa623f3c3392ee7cdd349c603f | PASS | Verification Summary; six selected gates rc0, pinned Commitizen rc0 and p01_review no required finding; normal commit da51f9332865c61721b2fe8e29ebad9cfc97abf7 | yes | none |
| EVD-P03-017-004 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Bounded shared-candidate meaning comparison | Actual persistent WGOV-CORE/3.0.0-draft.3 C05/C10/C11/C12 sections | PASS | Common Candidate Compatibility above; read-only regional mapping, no approval or joint adoption claimed | yes | none |
| EVD-P03-017-005 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Current AC semantics independent review | First P03 P01 criterion migration and its initial follow-up AC wording | FAIL | AC Review Correction below; p01_review MEDIUM found literal local ACs mixed with protected outcomes, then a setting-transition or-proof ambiguity; server_security_review also found the old handoff's conflicting condition | yes | none |
| EVD-P03-017-006 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Coupled lifecycle security review | Initial current disposition and evidence-history implementation draft | FAIL | Security Review Correction below; server_security_review found same-status terminal disposition could lose its Plan successor and prior adverse Evidence could be deleted without resolution | yes | none |
| EVD-P03-017-007 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Coupled lifecycle security review | Post-handoff declared initial_states admission draft | FAIL | Security Review Correction below; semantic validation allowed a nonterminal active initial state instead of requiring draft for modern Spec/Plan and Task | yes | none |
| EVD-P03-017-008 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Coupled contract independent review | First integrated 23-path P03 source and document diff after focused 37-test PASS | FAIL | Independent p01_review confirmed documented scope-cancelled not-required was unconditionally denied, and actual FAIL could retain a placeholder location; bounded corrective implementation and recheck follow | yes | none |
| EVD-P03-017-009 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Scoped changed-function coverage measurement | Five changed production Python files against da51f933; four selected test targets under stdlib trace | PASS | Focused Verification below; actual 37 tests PASS, 608/764 changed executable function lines observed, 79.6 percent in the current interpreter only; child validators and module-level changes excluded, no repository-wide coverage claim | yes | none |
| EVD-P03-017-010 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Coupled lifecycle security review | Corrected cancellation proof parser after focused 43-test PASS | FAIL | Security reviewer found word-boundary matching could count VAL-P01-001-extra as VAL-P01-001; require full criterion-token boundaries with a longer-token negative before final source acceptance | yes | none |
| EVD-P03-017-011 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Final scoped changed-function coverage measurement | First final four-target trace started before the subsequent Unicode token-boundary correction | DEFER | Deliberately interrupted by SIGINT, rc130, because its input was superseded before acceptance; ignored partial JSON/tests log retained as interrupted output, not final coverage proof | yes | none |
| EVD-P03-017-012 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Coupled lifecycle security review | Expanded concrete Evidence predicate compared with the actual ae93644 historical binding | FAIL | Security reviewer confirmed old accepted Evidence checked placeholder Location only; modern Check/Input requirements must not be applied retroactively to the real legacy binding; bounded compatibility regression and correction required | yes | none |
| EVD-P03-017-013 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Coupled lifecycle security review | Modern current-terminal disposition guard with malformed Criterion Acceptance body | FAIL | Source review found standalone lifecycle could retain a valid disposition while the other registered consumers rejected the malformed body; fail closed on body validity for cancelled/superseded Tasks, with no registered aggregate bypass or attack claimed | yes | none |
| EVD-P03-017-014 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Final scoped changed-function coverage measurement | Second final four-target trace after Unicode correction, before legacy/disposition corrections | DEFER | Deliberately interrupted by SIGINT, rc130; ignored interrupted2 JSON/tests log retained, not final coverage proof; rerun only after all source writers and security review release | yes | none |
| EVD-P03-017-015 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Coupled lifecycle security review | Final corrected production snapshot, document_contracts 4aee2367 and lifecycle validator 95fc8268 SHA-256 prefixes | PASS | Independent server_security_review verified released source hashes and found no remaining required issue in evidence retention, initial states, current terminal disposition, exact scope waiver, historical binding or immutable-source archive closure; source review only, SEC-P01-001 remains open | yes | EVD-P03-017-006, EVD-P03-017-007, EVD-P03-017-010, EVD-P03-017-012, EVD-P03-017-013 |
| EVD-P03-017-016 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Current AC semantics independent review | Corrected current P01 Spec/Plan/Task criteria 001/003/005/006/007/008 and preserved original evidence | PASS | Independent p01_review final source/prose PASS: literal local criteria accepted, joint candidate criterion pending, actual PR/control criterion rejected, settings read-back cannot replace independent control proof; historical adverse facts and remaining owners preserved | yes | EVD-P03-017-005 |
| EVD-P03-017-017 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Coupled contract independent review | Corrected cancelled-Spec waiver and concrete modern PASS/FAIL Evidence source and current guidance | PASS | Independent p01_review final source/prose PASS; cancelled-only candidate needs exact same-package scope proof in lifecycle, modern actual results need concrete provenance, NOT_RUN/DEFER remain distinct; final security review additionally confirms legacy semantics and malformed terminal body rejection | yes | EVD-P03-017-008 |
| EVD-P03-017-018 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Focused changed-behavior regressions and Python style | Final four-target unittest selection; released test hashes fd4a97f6 and 72283715 SHA-256 prefixes | PASS | Focused Verification below; 44/44 tests PASS in 27.804 seconds after final source fixes and two-file test organization; selected Ruff check/format-check PASS, no broad unit discovery or unrelated product suite | yes | none |
| EVD-P03-017-019 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Final scoped changed-function coverage measurement | Final security-reviewed five-source/four-target trace against da51f933 | PASS | _workspace/p03-coverage-final.json and .tests.log; 44/44 tests PASS in 317.592 seconds, 673/806 changed executable function lines observed, 83.5 percent; exact source/test hashes and uncovered lines retained, current interpreter only | yes | EVD-P03-017-011, EVD-P03-017-014 |
| EVD-P03-017-020 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Coupled implementation index QA | First frozen 23-path index tree086b5ec087d642e4a3534a18798fa72da8ad3c3b | FAIL | _workspace/p03-implementation-qa.log; aggregate rc1, 10/12 gates PASS; archive-contract-tests failed with 45 old-generation errors and selected-nonstyle rc2; index was not committed | yes | none |
| EVD-P03-017-021 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Repaired history adapter, public identity and focused checks | Source hashes document_contracts 6a288963, lifecycle validator cb35ca41 and contract tests c57e173f SHA-256 prefixes | PASS | Modern-binding-only criterion maps preserve actual generation 9 readers; affected Archive module 46/46 and P03 four-target 45/45 PASS, renamed identity targeted 3/3 PASS, Ruff PASS and independent security source PASS; aggregate index QA remains pending | yes | none |
| EVD-P03-017-022 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Final scoped changed-function coverage measurement | Repaired security-reviewed five-source/four-target trace against da51f933; exact hashes in final-v2 artifact | PASS | _workspace/p03-coverage-final-v2.json and .tests.log; 45/45 tests PASS in 325.631 seconds, 673/806 changed executable function lines observed, 83.5 percent; earlier artifacts preserved, current interpreter only | yes | none |
| EVD-P03-017-023 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Coupled implementation index QA | Repaired frozen 23-path index treefff1efcad28be61faddbb6c5db5f7589325e1974 | PASS | _workspace/p03-implementation-qa-final.log; all 12 selected gates rc0, diff checks PASS, unchanged exact implementation message's pinned Commitizen proof reused; normal commit 6327c3d395a105fe9ba11aaee48f7e52c1f5c120 has that exact tree | yes | EVD-P03-017-020 |

## Approval and Safety Boundaries

- **Allowed Paths**: owning SPEC-0106 Spec/Plan/new Task; selected current P01
  Task and its existing Spec/Plan criterion clarification; Stage 99 profile/schema/forms/guidance; current lifecycle/authoring/QA
  policy consumers; exact document readers/status writer and focused tests/routes;
  task-owned ignored scratch. Final architecture design fixes exact ownership.
- **Forbidden Paths**: completed Task rewrites, frozen Archive payloads, private
  or global/native trust state, credentials, live cluster and unrelated product
  implementations. No whole retention unit is removed or moved here.
- **Approval Required**: current P03 local scope and earlier generic main merge/
  owned branch/worktree cleanup remain authorized. The later evidence-update
  approval authorizes selective actual-result acceptance, never fabricated PASS.
  No push, PR, server-setting, tag, Release, secret or live authority is inferred.
- **Static Validation**: meaningful synthetic changed-behavior boundaries,
  retained history/status-writer controls, selected exact-index lint/format and
  actual Commitizen messages; independent read-only review before local finish.
- **Live Validation**: DEFER to the operating owner; actual PR style NOT_RUN
  until an authorized PR exists. Local static output cannot certify either.
- **Secret / Vault Handling**: no credential or secret value read/printed; public
  source/API metadata only; external PR code never runs on this host.
- **Rollback Plan**: forward corrective commit on this isolated branch; original
  states, approvals and evidence remain available through normal Git history.
- **Evidence Location**: this Task and actual commits; no second progress ledger.

## Verification Summary

### Scope and Design

The initial three-path index (this Task, Spec and Plan) passed
`_workspace/qa-venv/bin/python scripts/qa.py staged`, rc0, at tree
6effa0293b7197fa623f3c3392ee7cdd349c603f. All six selected gates passed:
document-contract-registry, document-lifecycle, links-and-owners,
markdown-profiles, selected-nonstyle and selected-style. The exact message
file `_workspace/p03-scope-message.txt` passed pinned
`python -m pre_commit run commitizen --hook-stage commit-msg --commit-msg-filename`
with that filename; normal commit was da51f9332865c61721b2fe8e29ebad9cfc97abf7.
Independent p01_review found no required finding on this intake scope.

The architect's design and consumer audit select a seven-column Task execution
table, one Criterion Acceptance table, and factual Evidence with Required and
Resolves. Current readers share one evidence resolver, binding work and
criterion IDs, rejecting unrelated success or unresolved required adverse
results, and retaining explicit later same-check resolution. Cancellation and
supersession preserve remaining criteria through current Plan successors or
actual authorized scope change. Read-only lifecycle validation checks the
current Plan, successor and Spec-scope relationships. The explicit status
writer validates single-document content and the allowed edge, then writes
only the status scalar; its output alone is not cross-document acceptance.
Baseline path/ID/blob evidence
selects historical bindings for unchanged completed Tasks; a copied or changed
old-form Task has no blanket completed exemption. Existing completed parents
remain historical completion observations rather than backdated approvals.

One quality writer owns Registry/schema/form/reader/status-writer/test/routes;
one document writer owns current governance/README guidance. Root owns current
Task authoring and the selected blocked P01 Task rewrite. Implementation
results and final acceptance are recorded after actual execution.

### AC Review Correction

The first current-record review found that P01's literal local comparison,
approval-route, resource and delivery ACs were being rejected because broader
common adoption and hosted/control outcomes were absent. Reuse the existing
Spec/Plan to name VAL-P01-007/008 for those already-requested remaining lanes;
accept the literal local ACs only from their actual local evidence and preserve
the blocked WORK-008, all adverse results and old criterion memberships.
Independent p01_review confirmed that semantic correction. Its next review
found that "integrity proof or an operator-reviewed transition" could allow
an exact setting approval to stand in for independent workflow-control proof.
Spec VAL-P01-008 now requires actual-input integrity proof, with settings
approval/read-back separately verified. The security reviewer found the old
Task handoff repeated the ambiguous condition; it is clarified and its earlier
wording preserved as a historical observation in the migration note. Actual
final review of these corrected inputs passed in EVD-P03-017-016; the original
required review failure remains EVD-P03-017-005 with that explicit successor.

### Security Review Correction

The draft security review found two enforcement gaps beyond current-row
shape validation: a cancelled/superseded Task's successor validity was checked
only on its terminal status edge, and existing adverse Evidence could disappear
between base and proposed bytes. Require current disposition checks even when
terminal status is unchanged, and preserve recorded evidence observations
through later edits, appending any actual resolving PASS instead of deleting
or changing failures. The real v2-to-modern AC clarification must preserve
original work criteria, new registered Spec/Plan assignment, adverse facts and
source provenance; it is not an arbitrary criterion or Required downgrade.
The assigned quality writer repaired these boundaries with focused negatives.
EVD-P03-017-015 records the independent corrected-source PASS; original
required review failure remains EVD-P03-017-006 with explicit resolution.

The declared entry-state field also needs semantic enforcement: the modern
Spec/Plan and Task edition must start in draft, not an arbitrary nonterminal
approved, ready, in-progress or blocked state. Current Registry values already
say draft; post-handoff security review found that an invalid later declaration
would otherwise bypass the intended entry edge. Require exact draft for this
edition, preserve older actual Registry readers, and reject malformed or
missing modern declarations. EVD-P03-017-007 retains this separate finding,
resolved by EVD-P03-017-015 after source and hash review.

### Tool and Check Boundaries

Intake, design, scope, focused implementation and coupled exact-index checks
are observed and locally accepted. This evidence-state input and the following
completion state each receive their own changed-input index check.
Python3.12.3 task-owned qa-venv installs the existing hash-pinned QA lock with
--only-binary=:all: and --require-hashes; no tool/config/technical limit is
changed. Exact index and message checks precede each normal logical commit.
Compute identity before freezing QA and invoke no Git/index/writer operation
while it runs; P02's snapshot-guard failure is not repeated as a procedure.
No business/session deadline, reserve approval, full/CI sweep or blanket unit
discovery is an acceptance condition.

### Focused Verification

The first integrated focused command was
`python3 -m unittest tests.test_task_acceptance_contract tests.test_task_acceptance_boundaries tests.test_document_scope_selection tests.test_task_execution_contract.CompletionIndexTests -q`.
All 37 tests passed in 18.347 seconds. The existing completion fixtures read
the real earlier Registry, not a locally invented legacy edition. Targeted
formatter execution over nine changed Python files passed without changes.

Before index QA, `_workspace/qa-venv/bin/python _workspace/p03-coverage.py`
traced the same four selected targets and five production sources. Its first
37-test run passed and observed 608/764 changed executable function lines
against da51f933, 79.6 percent. The core task_contract_issues function observed
113/131, 86.3 percent. This current-process measurement excludes spawned
validators and module-level changes; it does not assert repository-wide
coverage. The subsequent independent review found EVD-P03-017-008, so this
first successful test run is not final acceptance of the corrected input.

The two review gaps are corrected as one contract unit. A cancelled Task may
structurally record not-required only with actual same-package cancelled Spec
scope proof checked by the read-only cross-document validator. A successor
handoff alone cannot waive a criterion. Actual PASS and FAIL need concrete
check/input/location; unexecuted NOT_RUN/DEFER retain their distinct meaning.
Focused negatives, current guidance and final independent review must agree
before EVD-P03-017-008 is resolved by a later actual PASS.
Criterion tokens require complete boundaries, including Unicode letters and
digits; an ID embedded in a longer token is not criterion-specific scope
proof. Authored authorization references establish document consistency only;
the approving owner separately verifies the actual trusted approval decision.

The final four-target command above passed 44/44 tests in 27.804 seconds after
all source fixes. RED-to-GREEN observations include fresh authority states,
scope waivers without real cross-document basis, malformed criterion tokens
including Unicode adjacency, placeholder actual FAIL provenance, legacy
accepted Evidence semantics and malformed current terminal bodies. Additional
negative and recovery checks cover duplicate decisions/citations, required
NOT_RUN/DEFER resolution and immutable prior failures. The optional-PASS
resolution defect was found by inspection and fixed before its negative ran;
it is not claimed as an observed RED execution. Contract and boundary tests
were organized into two existing selected files, both below 800 lines, with
all 44 tests retained and no duplicate class discovery. Selected Python Ruff
check and format-check passed after the final changes.

Final production SHA-256:
document_contracts.py 4aee2367026fb9cfb6d076054eaa64ed326a6514ffb5cf9954ac196ace393cc1;
validate-document-lifecycle.py 95fc8268b181af7c03b2f4bd5d0f87702312b0d9732617f32d2058c985cd95f5.
Final selected test SHA-256:
test_task_acceptance_contract.py fd4a97f6bc5e8340663461bb48d58dfba84771f649d8c02a69e382d6659b68e3;
test_task_acceptance_boundaries.py 7228371514b60ebc2c1208659ec7055398ca9c35bfd4a301930a5eadfd9b1e32.
The final coverage artifact records all five source and four target hashes;
the interrupted measurements above remain explicitly nonfinal.

Final stdlib trace passed 44/44 tests in 317.592 seconds and observed 673/806
changed executable function lines, 83.5 percent, against da51f933. Per-file
observations are document_contracts 215/251, document_lifecycle 102/122,
validate-document-lifecycle 262/330, links 49/52 and Markdown 45/51. The
task_contract_issues function observed 112/130, 86.2 percent. Exact command:
`rtk proxy _workspace/qa-venv/bin/python _workspace/p03-coverage.py --source scripts/document_contracts.py --source scripts/document_lifecycle.py --source scripts/validate-document-lifecycle.py --source scripts/validate-links-and-owners.py --source scripts/validate-markdown-profiles.py --test test_task_acceptance_contract.py --test test_task_acceptance_boundaries.py --test test_document_scope_selection.py --test test_task_execution_contract.py:CompletionIndexTests`.
JSON SHA-256 is 0602fc26cc206b568e490248960e1ec735c8042842207e3fffac91aaaa2fc1c8;
test log SHA-256 is 51616f843df6346ad1e507ad69b2e8579c41714fd3f57f1705e8abfabd85c09e.
These artifacts retain all selected input hashes and uncovered line lists.
Neither this metric nor the source reviews certify a whole repository, spawned
validator coverage, native enforcement, trusted approval authentication or live
behavior. Final index QA is the separate acceptance input.

### Changes and Continuing Owners

| Local action | Current owner and reason |
| --- | --- |
| Registry/schema/Task form and common reader coupling | Stage 99 Registry plus scripts/document_contracts.py; one criterion decision, factual check resolution and explicit draft-only entry replace duplicate authored Acceptance |
| Lifecycle, Markdown and link consumers with selected regressions/routes | Document validation owners; preserve actual historical bindings, immutable Evidence, current terminal disposition and source-based approved-package eligibility |
| Current governance/README guidance | Existing .agents and Stage 99 owners; maintain authority versus execution meaning and status-writer boundary, without duplicate progress ledgers or provider projection changes |
| Current P01 Spec/Plan/blocked Task clarification | SPEC-0105 WORK-008; literal local acceptance preserved, new common/PR-control criteria retain actual adverse evidence and owners |
| Operating adoption and historical completion | Existing Stage 05 and completed Task owners; no completed Task rewrite, no Runbook status reset, no Archive movement/deletion or actual Release |

P02 is the available local input. Unreceived P05/P07/P08 and other-repository
adoption remain with their actual owners; no absent output is local PASS. Final
common edition/adoption stays with buenhyden and one Project-Template source
writer. SEC-P01-001 HIGH and the next authorized PR's actual control/style proof
stay in blocked SPEC-0105-TSK-0004. Static documents and exact setting read-back
cannot substitute for independent actual-input workflow-control evidence.
The operating owner retains actual Release/live/native proof. Local rollback is
a forward corrective commit; original evidence and source recovery remain Git.

### Exact-index Failure and Correction

The first coupled index above passed affected-surface-contract,
agent-governance, archive-integrity, document-contract-registry,
document-lifecycle, knowledge-surface, links-and-owners, markdown-profiles,
repository-quality and selected-style. Archive regressions exposed a real
older-generation consumer error: the new Task criterion mapping assumed a
modern Plan Criteria column while the actual generation 9 contract had a
different layout. The exact historical fixture reproduced KeyError Criteria;
keep that fixture and frozen bytes, and build the new mapping only for the
modern Task binding. Its affected historical module subsequently passed
46/46 and focused P03 passed 45/45 after an actual old-Registry regression.

Sanitized reproduction of the failed nonstyle hook reported detect-secrets
only at scripts/document_contracts.py line33. That literal is the public
ae93644e7e1137ed66ac243af4156ecea2d9cee4 Git commit, not a credential. Name the
constant TASK_LEGACY_BASELINE_COMMIT to state its exact meaning under the
existing trusted uppercase Git-identity rule. No scanner configuration,
secret baseline, skip flag or allowlist pragma is changed. Diagnostic output
retains only hook identity, selected path and line, never secret values.

EVD-P03-017-018/019 retain their actual earlier input/results. The repaired
source needs refreshed focused checks, source review, changed-function trace
and exact-index QA before local acceptance; the earlier coverage files are
preserved and are not proof of this later source snapshot.

Independent p01_review and server_security_review both passed the two repaired
source boundaries. Refreshed final-v2 trace passed 45/45 in 325.631 seconds,
with the same scoped 673/806, 83.5 percent observation. The exact five source
hashes, four test hashes and uncovered line lists are in
`_workspace/p03-coverage-final-v2.json`, SHA-256
543faf950af0c2a3d1636d375cae462388315d3d891f6bf41751bc93d9818e98;
its test log SHA-256 is 4ede91a371565a9b8e35056295ebc0b05f2661b4975ab2ef553b38dacd7c5d89.
Source identity now includes document_contracts
6a28896371646e43f7ae908fd53bb71e9ea02c7908bd6de1754cb308134c8db1 and lifecycle
validator cb35ca41afa18df2251071dddb2df92e4e9f81dc0653574c36caeffdf949444a.
The earlier implementation message already passed pinned Commitizen; its exact
file, grammar, pin, mode and trust inputs remain unchanged, so that leaf is
reused. Diff and final index checks use the repaired input.

### Local Acceptance and Finish

Repaired frozen tree fff1efcad28be61faddbb6c5db5f7589325e1974 passed all 12
selected gates, aggregate rc0: affected-surface-contract, agent-governance,
archive-contract-tests, archive-integrity, document-contract-registry,
document-lifecycle, knowledge-surface, links-and-owners, markdown-profiles,
repository-quality, selected-nonstyle and selected-style. Normal implementation
commit 6327c3d395a105fe9ba11aaee48f7e52c1f5c120 retains that exact tree. Active
hooks were preserved; no skip or trust/configuration bypass occurred. Earlier
required failures remain intact with explicit later PASS resolution.

VAL-P03-017 has one accepted criterion row and continuing owners above. This
state update makes ready-to-in-progress explicit; completion follows its own
validated edge. The requested local main fast-forward and owned branch/worktree
cleanup remain authorized, with exact checked-tree comparison before integration.
Actual remote PR style stays NOT_RUN, common approval/joint adoption and live
Release stay DEFER. No completed Task is reopened and no Archive unit is moved.
Task-owned scratch logs/messages/coverage will be copied byte-identically to
main's `_workspace/p03-task-acceptance/` before owned worktree removal; recorded
commands and original scratch locations remain historical invocation facts.
