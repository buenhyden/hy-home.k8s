---
title: "Current Registry Fixture Consumers"
version: "1.0.4"
type: "sdlc/task"
status: "completed"
owner: "platform"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0005"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Current Registry Fixture Consumers

## Overview

This bounded follow-up owns [VAL-P02-005](../spec.md#success-criteria--verification-plan)
and [WORK-005](../plan.md#work-breakdown). The existing hosted complement
failed unit tests because three current fixtures still expect retired
profile/domain declarations. This work follows completed Task0004 and
preserves all completed evidence. A later same-pattern comparison proved
that new metadata eligibility also reached non-Task targets; this Task owns
the forward restoration of the explicitly approved Task-only boundary.

## Inputs

- The user's normal unit-commit, push and merge instruction authorizes the
  necessary scoped fixture repair. The explicit narrow Task-template approval
  also authorizes restoring that change to Task targets only. Root assigned
  seven paths to one repo-tooling-engineer writer; quality, code review and
  security review are separate.
- [Plan](../plan.md), [registered Task form](../../../99.templates/templates/specs/task.template.md)
  and [quality policy](../../../../.agents/governance/quality.md).
- Clean Task0004 closing commit `961e6b21277b86f4c9238728e8ca3663d27b0ae1`.
- Existing automatic run `37294064121`, published P01 head `d0f358e8…`,
  complement job `111711030852`; no retry or cancel. Only the observed
  `unit-tests` complement gate failed; pre-commit and other gates passed.
  The clipped output identified five named failures, not a total failure count.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-005 | [VAL-P02-005](../spec.md#success-criteria--verification-plan) | Align current Registry fixture consumers while preserving identity, lifecycle and provenance refusals | repo-tooling-engineer | frontmatter | PASS | accepted | [Terminal candidate and handoff](#terminal-candidate-and-handoff) |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-040 | [VAL-P02-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Existing hosted failure and bounded named reproduction | Unchanged published Registry and three test consumers | FAIL | [Observed intake](#observed-intake) | pending |
| EVD-P02-041 | [VAL-P02-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Changed-input named GREEN and scoped hooks | Final identity/authority fixtures; migration `8bace413…` with guard `a9c4991d…` | PASS | [Fixture acceptance preparation](#fixture-acceptance-preparation) | accepted |
| EVD-P02-042 | [VAL-P02-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Observed draft/ready actual-index staged/message and independent review | Draft `2c433586…`; ready `dc2c3469…` | PASS | [Ready prerequisites](#ready-prerequisites) | accepted |
| EVD-P02-043 | [VAL-P02-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Observed prospective completion and separate review | Isolated proposal tree `3fcef2db…`; fresh actual-index acceptance remains separately required before commit | PASS | [Terminal candidate and handoff](#terminal-candidate-and-handoff) | accepted |
| EVD-P02-044 | [VAL-P02-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Initial changed-input identity check | First identity four-method group | FAIL | [Observed implementation preparation](#observed-implementation-preparation) | pending |
| EVD-P02-045 | [VAL-P02-005](../spec.md#success-criteria--verification-plan) | WORK-005 | First migration prerequisite check | First five changed-input methods | FAIL | [Observed implementation preparation](#observed-implementation-preparation) | pending |
| EVD-P02-046 | [VAL-P02-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Post-Schema migration group and causal diagnosis | Schema-valid fixture; first five-method group | FAIL | [Observed implementation preparation](#observed-implementation-preparation) | pending |
| EVD-P02-047 | [VAL-P02-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Same-pattern parent/current causal RED | Identical malicious proposed route; previous and Task0004 validator | FAIL | [Narrow history-order restoration](#narrow-history-order-restoration) | pending |
| EVD-P02-048 | [VAL-P02-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Changed Task-only guard and related controls | Guard `a9c4991d…`; control test `80816a8…`; migration first-five input `8bace413…` | PASS | [Narrow history-order restoration](#narrow-history-order-restoration) | accepted |
| EVD-P02-049 | [VAL-P02-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Observed guard-index staged/message and independent review | Guard commit `3b94d367…`; index `bdc1c146…` | PASS | [Fixture acceptance preparation](#fixture-acceptance-preparation) | accepted |
| EVD-P02-050 | [VAL-P02-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Observed fixture-index staged/message and independent review | Fixture commit `cff2cf32…`; index `097af6cd…` | PASS | [Terminal candidate and handoff](#terminal-candidate-and-handoff) | accepted |

## Approval and Safety Boundaries

- **Allowed Paths**: This Spec, Plan and Task; `tests/test_document_artifact_identity.py`, `tests/test_document_lifecycle_archive_cutover.py`, `tests/test_document_lifecycle_migration.py` and only the private first-appearance metadata eligibility condition in `scripts/validate-document-lifecycle.py`. One writer owns these seven paths. The registered validation member is explicitly delegated for this narrow restoration.
- **Forbidden Paths**: Other production validator behavior, schemas, Registry, published profiles/domains, validation lanes, hosted configuration, frozen Archive, completed Tasks/evidence, the generic migration fixture, provider/native state, private values and unrelated files.
- **Approval Required**: The existing explicit user commit/push/normal-merge authority and root's bounded necessary fixture delegation apply. The user's conditional terminal-candidate reflection authorization persists: fresh actual checks and separate review must pass before commit. No authentication or native runtime enforcement is claimed.
- **Static Validation**: Existing observed RED is preserved without identical retries. Changed-input named GREEN and meaningful related negatives, scoped pinned hooks, every actual index's canonical staged/message and independent review are required. Prospective completion/review precedes reflected source's fresh staged/completion/message/review. Local full and affected execution remain NOT_RUN under the current exclusion.
- **Live Validation**: DEFER — no cluster or runtime operation requested.
- **Secret / Vault Handling**: Safe path, rule and exception metadata only; no private values or raw sensitive CI output.
- **Rollback Plan**: Reviewed forward correction or revert; no force, rebase, branch deletion, cleanup or local main mutation.
- **Evidence Location**: This Task and external safe receipts; operational absolute argv/cwd stay outside tracked source.

## Verification Summary

### Observed intake

Five exact methods reproduced the observed failures on unchanged inputs,
each under a 60-second bound, without discovery. The identity method
`PathArtifactIdentityTest.test_wrong_but_pattern_valid_ids_fail_for_each_numbered_profile`
raises `KeyError('archive/route-tombstone')`; the published profile is
`archive/route`. Both `DocumentAuthorityLifecycleTests` methods
`test_real_registry_edge_list_accepts_legal_and_rejects_illegal` and
`test_loaded_registry_types_terminal_domains_and_owns_transition_projection`
raise `StopIteration` for retired `requirement-architecture`.
Both `MigrationLifecycleTest` methods
`test_canonical_policy_guard_precedes_pattern_compilation` and
`test_canonical_default_api_and_schema_null_semantics_are_preserved`
raise `StopIteration` in shared setup for retired
`governance-guide-policy-runbook`. That family differs from the authority
failure; the earlier same-family shorthand is corrected here.

Safe reproduction stderr SHA-256 values are
`c6dbb6debfb3f6a9c276a3724fb3fe48b18914e018678a9707998d0c43e2b3a8`
(identity),
`6a9b778a09a98716adeaf873b99f28e0b17c894d17c86856584d745775b505bc`
(authority), and
`7365f561553e9af4e8f5dbf8d9535cf63f721780357b963c08ab799af6587c0b`
(migration). These historical FAIL observations do not revoke completed
Task0003/0004 local acceptance or establish repaired hosted acceptance.

### Planned repair

Use the published `archive/route` key consistently in identity cases and
their exclusion set while preserving wrong-ID refusals. Authority cases
follow current `requirement` review-to-approved and separate
`architecture-description` review-to-active semantics; illegal edges remain
refused. Migration setup already inherits the complete current graph and
declared assets. Adjust its existing governance route for the finite test
paths; retain current membership and remove duplicate declaration additions.
The two migration pattern/route matrices retain `archive/migration`, which
is still a published retained evidence profile. The ready transition's
contrary lookup inference is withdrawn; document type mutations also retain
`archive/migration`. The existing
unmapped-state negative must render its quoted header's actual requested
active or retired state; otherwise its retired case does not mutate bytes.
Preserve policy-before-pattern, default/null, source Git/digest, disposition,
consumer, recovery and negative proof checks. No retired declaration returns.

### Validation boundaries

At draft authoring, implementation, named GREEN, scoped hooks and all current
index outcomes remain unobserved. Quality owns explicitly named identity and
authority controls plus all 25 affected migration setup methods. Independent
review reads each full candidate and actual receipts. Canonical staged runs
retain the existing runner limits and every actually selected gate; manual
named tests use separate bounded invocations. Existing Conftest preparation
and pinned tools are reused without configuration changes.

### Ready prerequisites

Draft commit `9d6fc142227bcc4659c7aae878edc866bdff178c` has tree
`2c4335864b7ae7e67f399bc21bd53419910b99ce`. Its six actual canonical staged
gates, configured message and separate candidate/evidence review passed.
Safe staged stdout SHA-256 is
`9e6d1541834095bbf0cd260709e759d1e92a2a21f0a23706a415337e881891bb`;
outer stderr was empty and all children reported complete output/cleanup.
The actual message fixture SHA-256 is
`032ff0e200d39e52b5b5975cde3c9e9e4c818b7f8eaf5bfd5acfe692ec2c99b2`.
This accepts only that prior draft; the ready index receives fresh checks.

Selection-only canonical preflight of the exact six allowed paths reported
no unmatched path and seven validators: agent-governance,
archive-contract-tests, document-contract-registry, document-lifecycle,
links-and-owners, markdown-profiles and repository-quality. No affected
execution occurred. Existing tools/configuration and runner limits are
unchanged; the selected gates retain their existing prerequisites.
The explicit focused manifest under `.worktrees/proposal/` names four
identity methods, two authority methods and all 25 shared migration setup
methods. These changed-input checks retain the five observed failure cases
and directly affected positive/negative contracts; they are not discovery.
Each named invocation is separately bounded. At this ready transition,
implementation, focused GREEN and required hosted outcomes remain pending.

Ready commit `6db05bc0c89a4975631a3c178fe5573cd824611d` has tree
`dc2c346964cf622967d76d8cb735f0815c2bbdc3`. Its six actual staged gates,
configured message and separate review passed; staged stdout SHA-256 is
`cec57cf1c8e0094bc57d19ab536f3027592e66ed3e5e48efadc1581a5a479497`,
with empty stderr and complete output/cleanup. The message fixture SHA-256 is
`390299e83e7fde73c63a8741b96ceea6d18f01bf68944259ff9c3087229dcc88`.
This accepts only that prior ready index, not implementation acceptance.

### Observed implementation preparation

The first changed identity group ran four methods: two passed and two failed.
The authored case inventory omitted three current reference pack profiles;
`archive/route` also has a declared identity pattern rather than an identity
derived by the existing path helper. Safe stderr SHA-256 is
`4df7008ae3c932fa942be4a4b990cf9e8be8b77c40178e67340fe1e080975ef3`.
The queued authority and migration methods had not run at that observation.
The corrected identity inventory includes all three packs. A renamed method
tests current declared identity contracts; normal text validation checks
pattern-valid controls and malformed-ID refusal for pack/route owners.
Every owner that derives an ID retains pattern-valid wrong-path-ID refusal.
This is pattern-focused validation, not a full document acceptance claim.

Independent review corrected the ready-stage inference about migration
profile lookup IDs: the published `archive/migration` profile still owns
the retained numbered records and the inherited fixture's bounded extension.
Its two original negative controls are restored. Current schemas and Registry
are unchanged; the later narrow order restoration is described below. New focused outcomes and this
implementation index's required checks remain pending until observed.

The corrected identity four-method group and both authority methods passed.
The first five migration methods then failed before their intended checks;
the remaining twenty were held. Exact schema diagnosis identified
`profiles[18].path_pattern`, keyword `pattern`: the test-only route union
did not have the required outer `^` and `$` anchors. Failure stderr SHA-256
is `67d0ab7053a0f1d7dde7afc89f1c4bd55f4c8c0178b999962c8a6efc4b97762c`;
the schema-path receipt has SHA-256
`f8948858419020072a923e27ba85553ee0b246ad03b7b6a0b40cf6b78f29a1ce`.
The minimal fixture correction wraps the unchanged published route body
and finite synthetic alternatives in that anchored envelope. Schema and
production behavior remain unchanged; new migration results are pending.

The anchored fixture passed Schema preflight, but the next five-method group
still failed, with eight subtest failures and one error; twenty methods
remained held. Safe stderr SHA-256 is
`2f8757af8bf868c5b97f14cc8f5db13918bc90379373a6a071ac945199fe2e0b`.
The default-API positive had removed the required Stage98 Spec alternative,
causing `REGISTRY_RETENTION_MODE`. Its finite added route now preserves the
entire published alternative. The intentionally aliased proposed graph
returns exact `LIFECYCLE-BASE` / `history registry is malformed` with both
the pre-Task0004 and current validator on identical inputs. Comparative
receipt SHA-256 `967ee6e1c53e1e864b7bbc16f8299d1326074ed9402d10b96bd48e2ffb0c7958`
disconfirms the suspected Task0004 causal regression for that case.
The identity-negative test proves its initial trusted model compiles, then
expects that precise malformed proposed-history refusal, nonzero outcome,
no traceback and no evaluated-pattern marker. Direct trusted policy checks
still assert that pattern compilation is never called. Executable-pattern
timeouts retain their existing bound. These alias observations do not
authorize production or deadline changes.

The revised malformed-proposal and default-API methods both passed on
migration source SHA-256
`17e2606f93c03febb33a57c324109cef34d7810a888dba5f67b3dcd745191394`;
safe stderr SHA-256 is
`b4b534024d1432d6e0cb95c551f173da137e9afb69a9a4ad7d2e4e3c6db6a26e`.
A separate unchanged-policy explicit-ref control returned zero in 1.349
seconds, below the existing five-second executable-pattern bound; safe
receipt SHA-256 is
`0aa8c485270706228619af35a193046452740182a5a54e5937e5625a30d6d2b6`.
This excludes baseline startup as the timeout explanation, without proving
its evaluation cause. Remaining named methods and a separate read-only
security diagnosis were pending at this observation; no complete GREEN
acceptance is claimed.

### Narrow history-order restoration

The separate same-malicious-pattern comparison used identical explicit-ref
fixture inputs: pre-Task0004 validator returned `ARCHIVE-MIGRATION-PROFILE`
in 1.421 seconds; the current validator exceeded the unchanged five-second
bound at 5.008 seconds. Its stack reached untrusted route matching through
the newly eager first-appearance `_history_document` call. Safe comparison
receipt SHA-256 is
`742a5c9bda6759b270ce42803581ff497554f6efa1f1fa1309d7a0aea3d77a6b`.
This proves the non-Task metadata regression for this pattern, separately
from the alias comparison that disproved that hypothesis for its own input.

The authorized correction preserves prior `allow_distinct_artifact_copy`
eligibility and adds all-mode metadata only when the already trusted Registry
classifies the target as `sdlc/task`. Ordinary-copy permission, all later
Task checks, history bounds and non-Task refusal order remain unchanged.
Fresh bounded Task-template controls and the existing malicious-pattern
method provide regression evidence; no mirrored cumulative test is added.
Independent code and security reviewers must accept the correction and
actual receipts before the separate guard commit. The earlier completed
Task0004 evidence is historical and remains untouched.

Five forward commits now separate draft and ready (already observed), guard
restoration, three fixture repairs while this Task remains in-progress, and
terminal completion. The guard index includes only this Spec/Plan/Task and
validator; the controlled fixture edits remain unstaged. Named focused
checks use their recorded working-tree bytes; actual staged checks consume
the distinct Git index. Fresh staged/message and review are pending until
observed. The fixture slice receives its own actual-index checks, and the
closing candidate retains the user's fresh actual-check/review condition.

The previously held twenty migration methods ran next: nineteen passed and
the final retained-record control raised `REGISTRY_ROUTE_AMBIGUOUS`.
Safe stderr SHA-256 is
`445d692e9e76228737875e5eed61cb3e05635a1232934624271c9fe74d0d6ee8`.
Typed route metadata shows each published retained migration 0001–0003
matching two regex routes in the same profile; the inherited broad synthetic
extension overlaps the published branch. This subclass now retains the
published route and adds only its actual synthetic `self.path` record.
The shared generic helper and its separate 0006/future-profile tests remain
unchanged. Final fixture and restored-validator bytes require fresh explicit
selection of all25 migration methods; earlier partial outputs are history.

The restored guard's focused controls passed on validator SHA-256
`a9c4991dcea16d695a11ce212022f653355cb77d5361115e45397e8cc0d149c4`
and unchanged cumulative test SHA-256
`80816a8b9cfde307db5b97476d28b9e749cc0b3b41fe7f1179d5aaf11f024249`.
The three registered-template positives cover real first draft, CI/explicit
refs and staged merge; safe stderr SHA-256 is
`6870f3f004e729b84d322c5144511755d45e03e658ba5fd0d1b2e2ba134212a5`.
The ten-condition boundary, ordinary canonical-copy CI refusal and later
Task checks passed; stderr SHA-256 is
`59b848828dd01de50d332ce04957c5a7c57d9dd69768fc0185b1886f10effe6c`.
The explicitly selected existing22 cumulative methods also passed, stderr
SHA-256 `cff91f6d72c39d3501b9f8b99d2f4d3456376882a7662c3781b58ae483c7c228`.
These named groups used separate 60-second bounded unittest invocations;
the six exact names are corroborated by actual tool-call provenance, not
claimed as a separately persisted argv file.

The final migration first-five group, including all four existing malicious
pattern variants, passed on fixture SHA-256
`8bace4130b766a3a38b5821a4b17eb4116f899b98a2490ac9bb6330889097a40`.
Safe stderr SHA-256 is
`27070641465228167c4ef11121052f0d9096da2dcbd2a7476733a2b3d4ddbe85`.
The internal five-second rejection bound and marker/refusal assertions are
unchanged. Final migration twenty methods, scoped hooks and guard index's
required staged/message and independent evidence disposition remain pending
at this observation; focused PASS is not complete implementation acceptance.

Separate independent code and security readers accepted this focused input
and its actual receipts. The security disposition covers the restored
non-Task rejection order and unchanged Task-template/copy checks; it does
not claim general combined hostile Task/Registry safety, actual staged/full
or hosted acceptance. The C3 index, configured message and scoped hooks still
receive their own required checks before its normal commit.

### Fixture acceptance preparation

The final named migration selection passed all25 methods, with each exact
five-method selection persisted alongside its raw unittest summary. Group
stderr SHA-256 values are
`27070641465228167c4ef11121052f0d9096da2dcbd2a7476733a2b3d4ddbe85`,
`36b131143d2c62939a9ee3d8b4cd246e3c9269bb129e71381e4278cc26d5730b`,
`7a3b7055c3ca07fbc5f69a926a103466ac2b2c4cbc987286799b6cf97fd28bbc`,
`736fac945c04b5ad71d39fa4c8b2bd12be94cb07b6c102ae42a135a9e38c9fc1`,
and `ac21ade787cde4d5d9fcb7d8951e80135faa9f9651eeb0b7dda782ffa8d7994f`.
This includes the retained-record control that previously found overlapping
routes. The unchanged pure-contract identity4 and authority2 results remain
PASS; their test, Registry and public contract dependencies are unchanged by
the isolated private history-condition repair. Their raw stderr SHA-256
values are `aee96418849d49e0f7081794b33d0578dbd6313d4ba672762229f414348f3091`
and `cb836db6d9201aa851c9e43fb920a1a4b82ae7ea8b917e0272186e2f3b890d9b`.
Independent review directly audited the final selections and receipts.

Pinned Ruff check/format, detect-secrets and markdownlint passed on exact
disposable copies of the four changed Python files and three scope documents,
with identical source/copy bytes after formatting. Safe structured hook
receipt SHA-256 is
`9a9a19404d0b24d3de21e6c6cd144891376e46e29725c690373a84b60a623631`.
The current Task-only evidence update needs fresh document/input checks.

Normal guard commit `3b94d3673f3db3ad88925fb8671c85d0c5b3405d` has reviewed
index tree `bdc1c146749d7992b5fff9c30e7854e856b27e2e`. Its actual12 canonical
staged gates and configured message passed, with complete output/cleanup,
unchanged source/index/refs and separate final review. Staged stdout SHA-256
is `8713424e3799cdd06d4388eca78a849064188f8ff2efdc4a0fac82c26801d6d1`;
outer stderr was empty. Actual message SHA-256 is
`976d911fbc2a291260be4894f5d576d67c6170ee61dc7226ef7f7738ac76baa5`.
The previous quality actor's model-capacity dispatch produced no observed
canonical outcome; a fresh neutral quality actor reconciled no active run
before executing these actual checks. No previous focused result was rerun
to recover that dispatch. These facts accept the prior guard index, whose
snapshot excluded the then-unstaged fixtures. At fixture-slice authoring,
that index still required its own staged/message and independent review;
whole Work acceptance and terminal checks remained pending at that transition.

Normal required exact-head hosted checks precede merge, and automatic
integrated-main checks precede integration acceptance. Remote push waits for
both local follow-ups to finish. The later known-path real-Git cumulative
probe is a private history-proof lane, not full CI or explicit-ref acceptance.

### Terminal candidate and handoff

The user's explicit conditional permission authorizes this source closing
candidate after observed implementation and prospective completion/review.
The prior fixture commit `cff2cf32a2d09d5443341db930d098fea1ffb9f9` has reviewed
index `097af6cdc3d3f5e8361eb0c9c2fe8bb3b8b95533`. Its actual7 canonical staged
gates, fresh Task Markdown, configured message and separate final review
passed, with complete output/cleanup and empty outer stderr. Staged stdout
SHA-256 is `b5f312b454ef438571def668ccb858401a318f70a10de96a05cdd9922f48a3b9`;
actual message SHA-256 is
`4a8adf2a2d888b0e95b52c2c8a8f3b85f640fe12fd25b16959e762f24fc73e70`.

The nonauthoritative isolated proposal at that clean implementation base,
under `.worktrees/proposal/p01-task5-c5-terminal`, retained the same tracked
configuration and durable branch reference. Exact proposal tree
`3fcef2dbe9a5069c8666c652941f0a45403c6dc8` passed SPEC0106-only completion and
separate semantic/evidence review. Actual INDEX-SNAPSHOT is
`b730088569ae73e1cf26f05abb8b27e632a50485cd31a6f8905cf52945f54966`;
completion stdout SHA-256 is
`6a3c97817ecf3e92f5565f5394a9abb908631ddc11389f17ac41d34cd8dba5f7`.
The original source remained clean/in-progress during that observation.
No proposal staged run was required by the current owner policy.

EVD-P02-043 accepts only those observed prospective results. This reflected
actual index is a new input: fresh canonical staged, SPEC0106 completion,
actual configured message and separate final evidence review must all pass
before its normal commit. Those actual closing receipts stay external;
no self-OID or unobserved actual result is written here. Local full/affected,
the later known-path private history probe, hosted exact-head checks and
integrated-main acceptance remain separate pending lanes. Rollback uses a
reviewed forward correction or revert under the existing normal delivery
authority; all branches, worktrees and completed historical evidence remain
preserved. No native/runtime or remote success is inferred.
