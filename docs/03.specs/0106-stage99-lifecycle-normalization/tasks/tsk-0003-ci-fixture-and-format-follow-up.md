---
title: "Hosted Fixture and Formatting Compatibility"
version: "1.0.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0003"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Hosted Fixture and Formatting Compatibility

## Overview

This follow-up owns [VAL-P02-003](../spec.md#success-criteria--verification-plan)
and [WORK-003](../plan.md#work-breakdown). PR 133 exposed historical fixture,
formatting and scanner failures after local P01 acceptance. Completed parent
and original Task evidence retain their historical meaning. Completion here
records local acceptance; remote and integrated-main outcomes need separate
observed evidence.

## Inputs

- The current user's work-unit commit, push and merge instruction authorizes
  necessary bounded forward repairs and normal delivery. The owning workflow
  assigns these paths to one repo-tooling-engineer; preserve other workers.
- Clean starting `codex/p01-authority-evidence` at
  `df3281d06a931bff6784bcc462800fab23bbb1c9`, based on main
  `9067729bf6679a0cd536362113be261056c32dd6`. P02 preserves its own inputs.
- [Stage 99 Task form](../../../99.templates/templates/specs/task.template.md),
  [Registry](../../../99.templates/registry.json) and
  [quality policy](../../../../.agents/governance/quality.md).
- Successful main CI run `36966489221` checked
  `997aa67d4a7ddb5dcdecf7048a68900155178231`. Its comparison to this intake
  selected 221 existing changed tracked paths for bounded diagnosis.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-003 | [VAL-P02-003](../spec.md#success-criteria--verification-plan) | Restore historical fixture and scoped formatting/scanner compatibility | repo-tooling-engineer | frontmatter | NOT_RUN | pending | [Verification Summary](#verification-summary) |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-020 | [VAL-P02-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Hosted required failure | Head `df3281d0…`; checked merge `e972e787…`; run `37278597507` | FAIL | [Observed failure](#observed-failure) | pending |
| EVD-P02-021 | [VAL-P02-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Historical fixture RED and schema diagnosis | Intake head; one named test and synthetic schema comparison | FAIL | [Focused diagnosis](#focused-diagnosis) | pending |
| EVD-P02-022 | [VAL-P02-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Corrected fixture, missing-object refusal and focused hooks | Corrected current proof and cumulative fixtures; unchanged frozen helper tests; final scoped hooks | PASS | [Implementation readiness](#implementation-readiness) | accepted |
| EVD-P02-023 | [VAL-P02-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Exact-index staged/message and semantic checks | Logical indexes pending | NOT_RUN | Pending | pending |
| EVD-P02-024 | [VAL-P02-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Final local completion and remote disposition | Terminal candidate and corrected hosted input pending | NOT_RUN | Pending | pending |
| EVD-P02-025 | [VAL-P02-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Draft exact-index staged/message and independent review | Tree `ad1d97439ff3a183c7bfa2215f1873fa0fccab82` at intake head | PASS | [Draft readiness](#draft-readiness) | accepted |
| EVD-P02-026 | [VAL-P02-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Ready exact-index staged/message and independent review | Tree `54e517917dbb694cf446a471b5efa6d5a35a136a` at `baeb20cb…` | PASS | [Implementation readiness](#implementation-readiness) | accepted |

## Approval and Safety Boundaries

- **Allowed Paths**: `tests/archive_generation_fixture.py`, `tests/test_archive_generation_fixture.py`, `tests/test_generic_migration_recovery.py`, `tests/test_document_lifecycle_cumulative_history.py`, `tests/test_archive_cutover.py`, `tests/test_provider_guard_registry_generation.py`, `tests/README.md`, `docs/02.architecture/decisions/0033-common-document-contract-v9.md`, this Spec/Plan/Task and original `tsk-0001-lifecycle-normalization.md` only for its diagnosed Markdown formatting correction.
- **Forbidden Paths**: Production Registry/schema and validator/gate behavior, scanner baseline/configuration, frozen Archive, old Task facts, native/provider state, secrets, live resources and unrelated changes.
- **Approval Required**: The current user instruction authorizes scoped commits, feature push, PR update and normal merge after required hosted checks. The owning workflow verifies the trusted interaction before protected delivery; this Task claims no actor authentication or revocation result. Force push, rebase, cleanup, branch deletion and worktree removal remain outside scope.
- **Static Validation**: Focused RED/GREEN and historical helper missing-object refusal; focused pinned hooks; exact-index staged and actual message checks for four normal commits; final completion and independent review. Local affected and full execution NOT_RUN under the scoped exclusion. Required hosted PR checks precede merge; integrated-main checks follow merge before integration acceptance.
- **Live Validation**: DEFER — not requested; static and hosted QA establish no runtime activation.
- **Secret / Vault Handling**: No private value reads or output. Only individually verified historical Git commit fixture occurrences receive narrow inline annotations; no baseline/configuration update.
- **Rollback Plan**: Reviewed forward corrective commit or forward revert; preserve both worktrees and history.
- **Evidence Location**: This Task; safe structured receipts may remain in temporary scratch without becoming another progress authority.

## Verification Summary

### Implementation readiness

The ready-only index `54e517917dbb694cf446a471b5efa6d5a35a136a`
passed all six selected canonical staged gates, cached pinned Commitizen and
`git diff --cached --check`. Actual message `/tmp/hy-p01-c2-msg.txt`
has SHA-256 `5d32d236544fb43404d54ceeb03b5948330c506912289b689f8da1e5315d967b`.
Independent reviewer `/root/p02_independent_review` reported PASS on that
exact index. Normal commit `82b4918f17dcdda1b12a0594539f9556eb7d7484`
recorded readiness. The first commit's staged evidence was observed in safe
tool stdout; no persisted raw receipt or native provider transcript is claimed.

Before implementing the asset reader, four new named helper tests were written
in `tests/test_archive_generation_fixture.py` at SHA-256
`871f4a0e534e6e312925f6173d53074ee77272161ba04eac4a939738ba98a114`.
The focused RED command selected only schema equality, template equality,
missing-object refusal and rejected-path cases, with a 60-second bound. It
returned 1: four tests, six subcase errors, all caused by missing
`legacy_asset_bytes`. Safe stderr `/tmp/hy-p01-c3-red.stderr` has SHA-256
`d191496adadda1e3e12ad4025e4d7fa60d48198eaeb0988fbf10cc18937b6a68`;
stdout was empty. This expected RED remains distinct from later GREEN.

The historical asset reader uses one immutable generation, rejects paths
outside normalized Stage 99 and propagates absent Git-object failure. The
first GREEN attempt passed all four new helper tests but failed two existing
proof tests. Matching the old schema removed its schema error, but the current
publisher intentionally rejects generation 9 before schema evaluation. Its
generation-10 admission was neither weakened nor mocked. That failed GREEN
stderr has SHA-256
`6384b7a5ea35f0d892ec52cffac0c85f83491eaa95c5046d98bffdfce86a300e`
at `/tmp/hy-p01-c3-green.stderr`.

The corrected generic fixture uses the complete actual current generation-10
Registry declaration graph, both physical schemas and all declared templates.
Its temporary Registry augments the published migration matcher with the
numbered-name grammar inside its existing 0001–0023 namespace; later numbers
retain the current scope-migration owner. It preserves the published tombstone
matcher and normal compilation,
source Git, digest, disposition, consumer and recovery checks and every
existing negative case. Independent historical asset-reader regressions keep
their separate frozen-generation purpose. The document-profile schema is the
loader's schema boundary; the fixture also copies the published frontmatter
schema as a current physical asset. No missing-frontmatter-schema hypothesis
was promoted to an observed cause.

The second GREEN attempt reached `REGISTRY_LEGACY_RETAINED`. Keeping the full
declaration graph did not resolve it: the third attempt still failed the same
four cases. The earlier dropped-profile explanation was a hypothesis, not a
proven cause. Its
failed stderr `/tmp/hy-p01-c3-green2.stderr` has SHA-256
`ad26f1efa4c5b50ac979a498ec5ba0105d92174dbb4b69917acad0833ff3c983`.
Third-attempt stderr `/tmp/hy-p01-c3-green3.stderr` has SHA-256
`77b8b46a6b47b8a345d0ae719ec41085a9ae352e5c9f4053659e0967e50f3462`.
Exact owner diagnostics showed all sixteen declared retained ADR paths
classify as `sdlc/architecture-decision` in the actual published Registry, but
the fixture's broad tombstone matcher caused `REGISTRY_ROUTE_AMBIGUOUS`.
That violated the required unique `move-frozen-body` binding. Safe tuples are
in `/tmp/hy-p01-retained-classification-safe.json`. The fixture now preserves
the published tombstone matcher entirely; retained declarations and controls
remain unchanged. The complete graph remains a faithful current asset model,
without being claimed as the causal fix for that overlap.
Before the next named test execution, corrected fixture compilation passed;
all sixteen retained paths kept their actual current profile, and the later
0123 path kept `archive/scope-migration`. The structured receipt
`/tmp/hy-p01-corrected-route-safe.json` has SHA-256
`7753a8e9aed8e84de08175863be6ff66a32efe55c108b83ff474e5a57d2ed485`.
The first union syntax failed the published anchored-pattern schema check;
adding the required outer anchors corrected that syntax without schema edits.

The named cumulative-history RED
`CumulativeLifecycleHistoryTest.test_explicit_ref_admits_absent_draft_active_chain`
failed with `LIFECYCLE-CREATE`, not the generic fixture's retained-profile error.
Its header omitted the required version and its intended positive history
skipped the current `in-review` edge. Safe stderr
`/tmp/hy-p01-c3-cumulative-red.stderr` has SHA-256
`367209be5469c4187e21f0d33325805c3090fd473a38e7d9a76541f55c7bc97b`.
The fixture now emits all six quoted/versioned header keys and explicitly
commits review before intended legal activations. Raw commit helpers and
negative assertions remain intact; a direct draft-to-active rejection case
guards against implicit promotion. Its existing selected Registry compiles;
no unrelated profile-graph change was applied to that fixture.

The revised scanner bytes exposed further occurrences of the same verified
Git commit fixture identities. Each annotated occurrence was independently
resolved to an actual Git commit object; approval covers only its inline
disposition. Current schemas, Registry, validators, scanner baseline and
configuration remain unchanged.

After exact retained-route diagnosis, focused GREEN4 ran the prior ten named
helper/proof cases plus the future-profile boundary case, once on changed
inputs: eleven tests passed in 22.645 seconds, exit zero. Safe stderr
`/tmp/hy-p01-c3-green4.stderr` has SHA-256
`c510b043ec8b86139b0995d12834b939f9b3bf6f4e71bc720b022bff6fe2ffff`;
stdout was empty. Separately, the cumulative fixture's shared header and
explicit setup changes selected twenty-two exact named methods, without
discovery: all passed in 31.489 seconds, exit zero. Its explicit argv receipt
`/tmp/hy-p01-c3-cumulative-argv.json` has SHA-256
`6ce3eb7de137921779ca78334847611beff4ae5c0e4b7f6d966e64e2df132bac`;
safe stderr has SHA-256
`536a251a59198765581bab55d86ce45b3a3dfb0183ad83d4d82de81b231dc162`.
Both focused invocations used a 60-second bound, distinct from the canonical
staged runner's 1200-second child bound. Unchanged cumulative inputs reused
their observed PASS after the generic route correction.

Pinned Ruff check passed all six changed Python paths. Its format check found
only the cutover fixture's long annotated argument; the sole writer applied
the pinned formatter and the changed file's check/format passed. The other
five unchanged paths reused their earlier PASS. The exact configured scanner
then reported zero new findings on final cutover bytes, with safe stdout
`/tmp/hy-p01-c3-cutover-secrets.stdout` SHA-256
`2c58a9a75488a66446aa342058a907c2b2d4bcf4050972b5d7b1935d8f51855a`.
Pinned Markdown passed all six changed documents; safe stdout
`/tmp/hy-p01-c3-markdown.stdout` has SHA-256
`a915eea79094503d6ac44258824a67aa9c92e037860bf304b763fd25cfb45416`.
The preservation receipt confirms original Task EVD-P02-013/014 rows are
byte-identical and production/native/schema/Archive paths have zero diff.
Current staged, completion and final index review remain pending until
observed; the staged profile will cover this final evidence text.

### Draft readiness

The draft index `ad1d97439ff3a183c7bfa2215f1873fa0fccab82`
passed all six selected staged gates via
`python3 -B scripts/qa.py staged --base-ref HEAD --root <P01_WORKTREE>`:
agent governance, document Registry, lifecycle, links/owners, Markdown
profiles and repository quality. The bounded runner returned zero with
complete cleanup. `git diff --cached --check` passed. The actual message
`docs(specs): scope hosted fixture compatibility repair` passed cached pinned
Commitizen using `/tmp/hy-p01-c1-msg.txt`. Independent read-only reviewer
`/root/p02_independent_review` verified that tree's three-document diff,
source contracts and safe diagnosis receipts and reported no material finding.
Normal commit `baeb20cb5c809c004e122b72ee7cfc08f71e09b2` recorded that draft
tree. At the subsequent ready-only transition, the Task recorded readiness
for implementation; EVD-P02-022/023/024 were still pending and no hosted
repair result or final acceptance was asserted.

### Observed failure

[PR 133](https://github.com/buenhyden/hy-home.k8s/pull/133) remains open.
[CI run 37278597507](https://github.com/buenhyden/hy-home.k8s/actions/runs/37278597507)
attempt 1 checked merge `e972e7872f8bdd4abf0d6219566381f9c93f1fb3`
for head `df3281d06a931bff6784bcc462800fab23bbb1c9`.
QA job `111661118879` and required summary `111666449249` failed;
required provenance was not observed. Unit tests and pre-commit failed;
the other complement validators, branch policy and isolated QA passed.
No merge, remote rerun, local ref update or gate bypass was performed.
Safe hosted receipt `/tmp/hy-p01-ci-run37278597507-safe-receipt.json`
has SHA-256 `f22b7b9c14aecae73566ef3957cdf1c42a5b8e1e82068720280839b2fc573c60`.
Only bounded redacted diagnostics survived; no artifact was uploaded.

### Focused diagnosis

On the disposable exact-head clone the canonical bounded runner executed
only `python3 -B -m unittest
tests.test_affected_surface_migration.RetiredSurfaceSelectionTest.test_composed_successor_is_classified_once_at_its_terminal -v`.
It returned 1 with `REGISTRY_SCHEMA`, `ARCHIVE-MIGRATION-PROFILE` and
`SURFACE-MIGRATION-PROOF`. The synthetic frozen Registry has one
current-schema `const` error at `schema_version`; its matching historical
schema at `c652331ce1c6bfddf1e670c748ce1a04b3835c33` has zero errors.
Only the generic migration fixture mixes generations. Other inspected legacy
consumers use a typed frozen Registry or matching current Registry/schema.

Focused Markdown found four diagnostics across three paths: ADR-0033 line 180
has two MD050 errors; original P02 Task line 646 has MD037; `tests/README.md`
line 31 has MD001. Python formatting changed only
`tests/test_provider_guard_registry_generation.py` in the disposable clone.
The security reviewer classified scanner findings at
`tests/test_archive_cutover.py` lines 66 and 225 as actual Git commit objects;
only their inline annotations may change.

Safe receipts remain under `/tmp/hy-p01-diagnostic-joka0i9i/`:
`focused-test-safe-receipt.json`, `fixture-schema-safe-receipt.json`,
`post-green-markdownlint-cli2-safe-receipt.json` and
`post-green-ruff-format-safe-receipt.json`. Raw logs and matched scanner values
were neither printed nor retained. Implementation, staged/message, completion
and independent review remain NOT_RUN/pending at draft intake. Local full and
affected execution remain NOT_RUN. Hosted delivery is blocked; next owners
are writer, quality-engineer and independent reviewer, then delivery executor.
