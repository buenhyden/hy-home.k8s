---
title: "Registered Task Template Instantiation"
version: "1.0.3"
type: "sdlc/task"
status: "completed"
owner: "platform"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0004"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Registered Task Template Instantiation

## Overview

This separately approved follow-up owns
[VAL-P02-004](../spec.md#success-criteria--verification-plan) and
[WORK-004](../plan.md#work-breakdown). A real P02 merge candidate failed when
Git identified the newly created Task0003 as a copy from its registered form.
The completed Task0003 remains a historical local acceptance record; its
source and original Task EVD-P02-013/014 are preserved.

## Inputs

- The user's explicit instruction, `좁은 validator 수정·회귀 검증 허용`,
  authorizes only the registered original Task template to new canonical,
  unique first-draft boundary. Other copies, renames, reused identities,
  illegal states and provenance refusals remain required.
- [Plan](../plan.md), [Stage 99 Task form](../../../99.templates/templates/specs/task.template.md)
  and [quality policy](../../../../.agents/governance/quality.md).
- Clean published P01 head `d0f358e8d27d076c5ebbd0badb2c79548296a5ac`.
  The existing hosted run `37294064121` is preserved without retry/cancel.
- P02 merge failure used HEAD `a3bdf5c04f48f27e7f9b882cff0eb58d2a8019e4`,
  MERGE_HEAD `d0f358e8d27d076c5ebbd0badb2c79548296a5ac`, common base
  `df3281d06a931bff6784bcc462800fab23bbb1c9` and index
  `c5582dffb968f43d4a16dc870b35d6e4fab77092`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-004 | [VAL-P02-004](../spec.md#success-criteria--verification-plan) | Correct the registered Task-template first-draft boundary without weakening other provenance controls | repo-tooling-engineer | frontmatter | PASS | accepted | [Observed implementation acceptance](#observed-implementation-acceptance) |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-030 | [VAL-P02-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Existing merge failure | Frozen P02 merge index `c5582dff…` | FAIL | [Observed intake](#observed-intake) | pending |
| EVD-P02-031 | [VAL-P02-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Registered Task template real-Git RED | Ready base; unchanged validator `6c02261c…`, corrected test `db442023…` | FAIL | [Observed RED](#observed-red) | pending |
| EVD-P02-032 | [VAL-P02-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Narrow GREEN and existing refusals | Validator `1ec86e4d…`; final focused test `80816a8b…` and explicitly unchanged prior inputs | PASS | [Focused implementation](#focused-implementation) | accepted |
| EVD-P02-033 | [VAL-P02-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Observed draft/ready/implementation actual-index staged/message and separate review | Three accepted prior logical candidates; implementation tree `c1f932c0…` | PASS | [Observed implementation acceptance](#observed-implementation-acceptance) | accepted |
| EVD-P02-034 | [VAL-P02-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Observed isolated terminal completion and semantic review | Prospective tree `9a29c034…` at accepted C3 base | PASS | [Observed terminal proposal](#observed-terminal-proposal) | accepted |

## Approval and Safety Boundaries

- **Allowed Paths**: This Spec/Plan/Task, `scripts/validate-document-lifecycle.py` private copy guard and `tests/test_document_lifecycle_cumulative_history.py` focused regression fixtures. One writer owns these five paths; preserve the separate P02 worktree.
- **Forbidden Paths**: Public schemas, Registry generation/bindings, validation-lane membership, hosted configuration, frozen Archive, completed Task0003, original Task evidence, provider/native state, secrets and unrelated code.
- **Approval Required**: The explicit narrow user authorization delegates this registered lifecycle validator to the repo-tooling-engineer. The existing user commit/push/normal-merge authority persists. The explicit conditional closing authorization permits applying a tested completed candidate before actual-index checks; no commit occurs until actual checks and separate review pass. No actor authentication or runtime enforcement is claimed.
- **Static Validation**: Real-Git named RED then minimal GREEN; source/binding/identity/state/provenance refusal regressions; exact-index canonical staged and actual message for draft, ready, implementation and closing commits. A same-base/config isolated terminal proposal receives Spec completion and separate semantic review; its uncommitted status does not replace the closing source's fresh actual-index staged, completion, message and separate review. Local full and affected execution NOT_RUN under scope exclusion; required hosted checks precede normal merge and automatic main checks precede integration acceptance.
- **Live Validation**: DEFER — not requested; no cluster or runtime acceptance.
- **Secret / Vault Handling**: No private values or raw sensitive logs; Git metadata and safe check receipts only.
- **Rollback Plan**: Normal forward correction or reviewed forward revert; no force, rebase, cleanup, branch deletion or local main updates.
- **Evidence Location**: This Task and externally captured safe receipts; operational absolute argv/cwd remain outside tracked source.

## Verification Summary

### Observed intake

The frozen P02 merge staged run passed six of seven gates and failed
`document-lifecycle` with `LIFECYCLE-CREATE` for Task0003 absent to completed.
Safe stdout `/tmp/hy-p02-merge-staged.stdout` has SHA-256
`4ea3e6aea513c3bbd37885ff42ae544ee206bd699d1537b7a8263c5644d0fd39`;
stderr was empty. The merge message separately passed. Read-only diagnosis
identified actual Git C006 provenance from the Task's registered template at
its first draft creation. The current guard expects a canonical source
artifact identity, which the template correctly does not have.

### Planned boundary

The only additional admitted C-copy is a first appearance of `sdlc/task`
with valid draft state, a path-derived canonical target ID absent from the
base and unique in the proposed snapshot. The source must equal the current
profile's registered template and the exact parent/event historical binding;
its regular Git blob must exist unchanged across creation. R-copy signals,
ordinary documents, arbitrary forms, modified or nonregular sources, changed
bindings, duplicate/reused IDs and wrong initial states retain refusal.
Normal initial-event comparison and every later lifecycle edge remain in
place, with existing deletion, merge, malformed evidence and budget guards.

The selected neutral role and both required procedures were explicitly read.
This registered-member edit uses the explicit active-Task delegation, not a
filename-based ownership inference. Quality and independent review are
separate actors; tracked provider projections prove no native enforcement.
At both the draft intake and ready transition, implementation, RED/GREEN
and hosted repair outcomes remained pending. The observed implementation
checks below do not promote hosted or current-index acceptance.

### Ready prerequisites

The draft's actual three-document index received six canonical staged gates,
the exact configured commit-message check and independent review, all PASS.
Observed staged stdout has SHA-256
`0a81eb3003a5639bfc8809beb93f6c3c9f5e6589e7e3afe64a0c31af20b2744e`.
The normal draft commit is `e149ffeb6c279f72acb040d966d8a4469c3ac918`.
This records the draft's acceptance only; the ready candidate receives its
own index and message checks before a normal commit.

Selection-only preflight of the five authorized paths selected twelve
canonical implementation gates: agent-governance, archive-contract-tests,
document-contract-registry, document-lifecycle, gitops-structure,
infrastructure-contracts, k8s-manifests, links-and-owners, markdown-profiles,
policy-gates, repository-quality and secret-handling. All selected gates
remain required; no affected execution occurred.

The secure resolver initially found no Conftest candidate. The official
Conftest 0.69.0 release asset matched both its official checksum and the
existing CI pin, SHA-256
`96fc2fbf11f0afde51256647127e6f00a64ce839a4d9a0a1aef2426c0e6f4b3f`.
An absent-only account-owned installation passed the unchanged secure
resolver; observed version was Conftest 0.69.0 with OPA 1.19.0.
Verification and installation receipts are ignored under
`.worktrees/proposal/task4-conftest/`; absolute executable and operational
paths remain there. No existing file, configuration or credential changed.
Named tests use a separate 60-second command bound. Canonical execution
retains the runner's existing timeout, output and cleanup limits.

The original hosted run completed with a unit-tests failure while its
pre-commit and other complement gates passed. Five named cases were diagnosed
as stale current Registry fixture expectations, separately from this copy
guard. This Task claims no hosted repair or integration acceptance and does
not retry that run.

### Observed RED

The first test-only attempt failed during fixture setup because the renderer
used the raw Registry field instead of the typed `.template` accessor.
That setup failure, receipt SHA-256
`60f689a749485e1612cb9752d53a0116b7e556f7aab0e5a4d0647f4c0afa8e71`,
is not the intended RED.
After that correction, the named real-Git test reached its final assertion:
actual C-copy provenance identified the registered Task form, and the parsed
first draft was valid, but the original guard returned True (rejection).
The test exited 1; stderr SHA-256 was
`2a5502bdcebfbb4d4dbffa927e45b6946d0108ca9c8d89494c2d811c641cd449`.
This historical failing input remains FAIL in EVD-P02-031.
Independent inspection also observed actual C007 from the same form at this
Task's own draft introduction; no source-template blob changed there.

### Focused implementation

The final focused validator bytes have SHA-256
`1ec86e4ddd1c994bb18e11275d2c2fc52de1a0606337149c9daf6542eb0cc91c`;
the test file has SHA-256
`80816a8b9cfde307db5b97476d28b9e749cc0b3b41fe7f1179d5aaf11f024249`.

The private C-copy exception verifies the current and exact parent/event
Task template binding, unchanged regular Git source blobs, first valid draft,
path-derived canonical ID absent from the base and unique in the proposed
snapshot. First-appearance metadata is supplied in CI and explicit-ref as
well as staged history. Ordinary canonical-document copy permission is
forwarded separately with its existing staged/generation-admission scope.
Later appearances, R signals, normal event comparisons and bounded evidence
controls retain their existing paths.

Six Task-specific named methods passed across separate 60-second bounded
invocations: real registered-form copy; legal CI/explicit-ref history;
real divergent staged merge; ten invalid source/binding/state/identity
conditions, including proposed-only duplicate ID; ordinary canonical Task
copy refusal in CI; and preserved later Task checks.
The existing 22 explicitly enumerated cumulative methods also passed;
the direct unittest receipt reports 32.706 seconds and SHA-256
`dcc10da5cc6b2eb25a3266a63a654068f9973c18a0b841bf79f99913e850307b`.
Their methods, global helpers, configuration and validator bytes remained
unchanged during the final new-test refinements; AST comparison receipts
under `.worktrees/proposal/` support that reuse.

The first later-result assertion incorrectly required the private history
proof to own final current Task evidence. Actual metadata proved that the
mutation changed a WORK result from PASS/accepted to NOT_RUN/pending and
that the committed Task binding existed. The private proof admits the legal
edges, while normal CI rejects the completed result with
`TASK-TERMINAL-EVIDENCE`; only `LIFECYCLE-CREATE` is removed by cumulative
admission. Diagnostic receipt SHA-256
`54909276d655438f942feb12daca25db6547deee2fcbf8e712856650b5c72532`
withdraws the earlier ineffective-mutation hypothesis.
The corrected test checks a valid normal CI control, illegal-edge private
refusal, a nonempty result mutation and normal terminal-evidence rejection
with no create diagnostic. Its PASS receipt has SHA-256
`10d88e2f55c1d3354bb5b45155b39b1161a48cfcdf64f033ceffa00a296dc4be`;
the ten-condition boundary receipt has SHA-256
`e258d8e199b060fda1e8014601170360f13ae67440e046b40f5bb37a30676e74`.
No production change beyond the approved template-copy boundary was needed.

Pinned Ruff 0.16.5 check/format and detect-secrets 1.5.0 hooks passed on
exact-byte disposable copies of the two changed Python files. Formatting
preserved both source hashes; the hooks did not mutate the sole writer's
worktree. Safe receipt hashes were
`a0b89d57f9b6c3ceb980814836970c036d45058fc93ed1be57acf8b0381352f1`
(Ruff check),
`370442f018ade47bf8c4df3e9a82d9ee38eb53948d2e813c3609b4b23daa2752`
(Ruff format) and
`ee9b110ce682d490c31e03e9c058b478118d877f7ab42ae8bbad2e85e26d6757`
(scanner); outer stderr was empty.

At implementation candidate authoring, Task Markdown hooks, this index's
staged/message checks and whole-index review awaited their own observation.
External actual receipts determine whether that exact candidate may commit;
they are recorded at the next logical transition without self-OID insertion.
At that authoring point the work item remained pending; focused EVD-P02-032
acceptance covered its named checks and observed Python hooks only. Historical failures
and required hosted/integrated-main delivery remain separate from local
source acceptance.

### Observed implementation acceptance

At implementation candidate authoring the work item remained pending.
The subsequent actual C3 index, tree
`c1f932c03bf45785a86b37d9b89d8d4b212e3f5b` at the ready base, received all
twelve selected canonical staged gates, the exact configured message check
and separate full candidate/evidence review, all PASS. Safe staged stdout
has SHA-256
`ca8e673881ecbdfd8f4693b61605e2f9a8efcdbaa6a9b64e8b5f6b64e10dab3c`;
outer stderr was empty and every child reported complete output and cleanup.
The message fixture has SHA-256
`37f5e7f526f08353008aa957917264bd309fb57a9d67cbd0e4b0e4e0d2345757`.
The normally committed implementation is
`fd331cabb5df430bbef57ed092d8ce8389fb5985`.
The preceding draft and ready candidates also received their own six-gate
staged/message and independent review PASS; ready stdout has SHA-256
`40a668aa44f17176972fabc723f860e17e6a44550ee28bf6caaec16e46224383`.
EVD-P02-033 accepts these observed prior candidates only.

### Observed terminal proposal

An isolated, uncommitted terminal proposal at the accepted implementation
base, tree `9a29c034ff8d7836516f19a3a5b9722048f218ef`, received independent
semantic review and SPEC-0106-only completion, both PASS. Completion stdout
has SHA-256
`70acc638fe89de8c3951f35f174873b279457a5a35781c7f3542653266da8196`;
its exact index snapshot has SHA-256
`26fba001b1b3047716e97e6f06bdd602197257f87cc664d0865d4e1ae70940dc`.
Outer stderr was empty. This prospective lane performed no separate staged
run; required actual-index checks are preserved below. EVD-P02-034 accepts
only the observed prospective completion and semantic review.

This source reflects a conditionally authorized completed candidate. At
reflection, its own actual closing index checks remain unobserved; no final
source acceptance or commit is asserted on that basis. A normal closing
commit requires fresh actual-index canonical staged, SPEC-0106 completion,
configured message and separate whole-candidate/evidence review, all PASS.
The actual closing receipts remain external, avoiding self-OID insertion.
Local full/affected execution remains NOT_RUN. Required PR checks, a guarded
normal merge and automatic integrated-main checks remain pending. The old
hosted unit failure and frozen P02 merge failure remain historical receipts;
this local repair does not revoke Task0003 local acceptance or claim remote
success. Current Registry fixture consumers require a separate follow-up.
