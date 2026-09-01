---
title: 'Contract Cutover and Program Closure Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-28
artifact_id: "SPEC-0040-PLAN-0001"
---

# Contract Cutover and Program Closure Implementation Plan

## Overview

This completed Plan executes [Spec 040](spec.md)
as the final PRD-0006 repository-static tranche. It activated a reciprocal
[Task](README.md#task-records), removes
active compatibility-reader behavior, proves the final repository contract,
and closes PRD-0006, AD-0009, ADR-0020, the Spec, Plan, Task, indexes, and
program relation in exact terminal closure commit
`c5adc27b13893d7cbd1266c9225372cfb7df79e9`. Deterministic precommit validation
passes, and independent terminal reviewers approved staged diff SHA-256
`e146fb13fb3a62db014e6317992a4f519b79ba330253c4c5fe89834dc67e1888` with no
findings. Explicit-ref lifecycle from parent
`35d8552ba423e3e2d92294ddeb81674392b8f333` to the closure commit and
clean-tree repository-static aggregate passed. This evidence-update commit is
unidentified and unclaimed.

## Context

Spec 039 closed in commit `e1d1e910840337327a557ab4b84e86f8fced11d6`.
Its activation-to-closure
explicit-ref lifecycle and clean-tree repository-static postflight passed.
Commit `11a020d9b299ae91b7af9278c22ed89ffccb5cfc` records that observed result
without claiming its own identity in the earlier evidence proposal. Hosted run
`29982910320` remains a historical FAIL for its older SHA, while current
hosted, provider, and live evidence remains `DEFER`.

The active production gates already invoke strict document validation, but
the validator CLIs and current support/inventory prose still expose
compatibility-era behavior and wording. Finite fixtures that prove a closed
historical transition remain necessary regression evidence; they are not
active compatibility readers. The final cutover must preserve that distinction
and must not rewrite completed historical execution records merely to make
their terminology current.

This Plan, its Task, the Spec backlink, both Stage 04 indexes, and the shared
progress handoff formed the exact six-path activation package committed as
`5c7bb820d9b424577eda3eb3a5c368f0c7cfc656`. No registry or
migration-ledger change belonged to activation. Explicit-ref lifecycle from
`11a020d9b299ae91b7af9278c22ed89ffccb5cfc` to that observed activation
commit and the clean-tree repository-static aggregate passed.

### Legacy Task ledger inputs

This Task is the evidence owner for the
[Spec 040 Plan](plan.md).
It records completed reciprocal activation, strict-only active-reader cutover,
closure-matrix and Current-audit reconciliation, whole-branch QA and reviews,
the exact staged PRD-0006 terminal proposal with observed independent terminal
review, and exact terminal closure commit
`c5adc27b13893d7cbd1266c9225372cfb7df79e9` with parent-to-closure postflight
evidence. Work is repository-local unless a separately approved action
explicitly changes that boundary. This evidence-update commit is unidentified
and unclaimed.

The predecessor closure commit
`e1d1e910840337327a557ab4b84e86f8fced11d6` passed explicit-ref lifecycle and
clean-tree repository-static postflight. Evidence update
`11a020d9b299ae91b7af9278c22ed89ffccb5cfc` hands the active frontier to Spec
040. Hosted run `29982910320` remains historical FAIL for its older SHA, and
current hosted, provider, remote, and live evidence remains `DEFER`. The
activation package was committed as
`5c7bb820d9b424577eda3eb3a5c368f0c7cfc656`; explicit-ref lifecycle from the
evidence-update commit and the clean-tree repository-static aggregate passed.

- [Contract Cutover and Program Closure Implementation Plan](plan.md)
- [Spec 040](spec.md)
- [PRD-0006](../../01.requirements/0006-workspace-document-lifecycle-and-evidence-consolidation.md)
- [AD-0009](../../02.architecture/descriptions/0009-document-lifecycle-evidence-operating-model.md)
- [ADR-0017](../../02.architecture/decisions/0017-program-follow-up-lineage-semantics.md)
- [ADR-0018](../../02.architecture/decisions/0018-full-body-archive-record-and-retention.md)
- [ADR-0020](../../02.architecture/decisions/0020-document-lifecycle-program-closure-evidence.md)
- [Document profile registry](../../99.templates/registry.json)
- [Stage 90 reference router](../../90.references/README.md)
- `docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md`; [current lookup](../../90.references/research/0001-workspace-engineering/source-coverage.md)
- Spec 039 closure `e1d1e910840337327a557ab4b84e86f8fced11d6`
  and evidence update `11a020d9b299ae91b7af9278c22ed89ffccb5cfc`
- [Document quality standards](../../00.agent-governance/rules/quality-standards.md)
- [Git workflow](../../00.agent-governance/rules/git-workflow.md)
## Goals & In-Scope

- Activate the reciprocal Spec 040 Plan/Task pair and direct backlinks as one
  lifecycle-valid package.
- Make the active registry, Markdown-profile, and owner/link readers
  strict-only while retaining bounded historical-transition proof fixtures.
- Remove stale current compatibility and registry-version claims from active
  support, script, test, and audit surfaces.
- Produce a criterion-level closure matrix and update the Current audit with
  repository-static results, explicit limitations, owners, and rollback.
- Run focused, affected, strict, lifecycle, aggregate, all-files, and
  whole-branch review lanes.
- Close PRD-0006, AD-0009, Spec 040, this Plan, its Task, and the final program
  relation atomically, then run explicit-ref and clean-tree postflight checks.

## Non-Goals & Out-of-Scope

- Rewriting immutable or completed historical evidence solely to replace
  accurate compatibility-era terminology.
- Removing finite archive-cutover, registry-version, or transition fixtures
  that fail closed and prove a bounded historical event.
- Implementing Specs 041-046, provider adapters, model routing, roster changes,
  shared provider memory, or unrelated `.github/README.md` changes.
- Pushing, merging, dispatching GitHub Actions, modifying repository settings,
  publishing, installing dependencies, or mutating provider, Kubernetes,
  GitOps, Vault, ESO, Argo CD, cloud, credential, or secret state.
- Promoting a repository-static PASS to hosted, provider, remote, or live PASS.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| CCPC-000 | Activate reciprocal Spec 040 planning | Spec 039 closure and evidence update | Closure `e1d1e910…` and evidence update `11a020d9…` are observed | Intentional Plan-only `LIFECYCLE-CREATE` RED; exact six-path lifecycle GREEN; one observed logical activation commit; no registry or migration-ledger drift |
| CCPC-001 | Cut active document readers over to strict-only operation | CCPC-000 | Reciprocal Plan/Task pair is active | Tests prove strict default/no-mode PASS and retired compatibility invocation rejection; active current prose and retirement guard are consistent; finite historical proof fixtures remain bounded |
| CCPC-002 | Build the final closure matrix and Current audit overlay | CCPC-001 | Strict-only active reader contract is green | Every Spec 040 criterion and PRD-0006 requirement has repository evidence, result class, owner, limitation, rollback, and final disposition; no unowned current finding remains |
| CCPC-003 | Run whole-branch QA and independent reviews | CCPC-002 | Closure matrix is complete and the proposal is stable | Focused, affected, strict, lifecycle, aggregate, all-files, formatter, and diff gates pass; independent requirements and quality/security reviews approve the exact proposal |
| CCPC-004 | Close the program lifecycle atomically and record postflight | CCPC-003 | Observed validator compatibility prerequisite commit `35d8552` is the closure parent | Exact 14-path terminal closure commit `c5adc27b13893d7cbd1266c9225372cfb7df79e9` transitions PRD-0006, AD-0009, ADR-0020, Spec/Plan/Task, six indexes, progress, and registry relation together; required precommit gates pass and final frontier is `0/0·6/3·3`; independent terminal reviewers approved staged diff SHA-256 `e146fb13fb3a62db014e6317992a4f519b79ba330253c4c5fe89834dc67e1888` with no findings; parent-to-closure explicit-ref lifecycle and clean-tree aggregate passed; this evidence-update commit remains unclaimed |

### CCPC-000 — Reciprocal activation

1. Preserve the settled migration ledger as a read-only input.
2. Prepare the Spec backlink, this Plan, its reciprocal Task, both Stage 04
   indexes, and shared progress entry as exactly six changed paths.
3. Stage the Plan alone and require exit `1` with `LIFECYCLE-CREATE`, Plan
   count `1`, and Task count `0`.
4. Stage exactly all six activation paths and require lifecycle, registry,
   strict document, link/owner, aggregate, and diff gates to pass.
5. Obtain independent requirements and quality review before creating one
   logical activation commit. Record its identity only after Git returns it.

### CCPC-001 — Strict-only active readers

1. Add or update focused tests first so no-mode validation exercises strict
   behavior and a compatibility-mode request fails at the CLI boundary.
2. Remove compatibility execution branches from current registry,
   Markdown-profile, and owner/link validators without weakening strict
   diagnostics.
3. Retain `template-compatibility.json` as the bounded no-growth retirement
   guard it already is; do not delete or rename that finite historical proof,
   and do not recreate the retired semantic-debt fixture.
4. Update current Stage 99 support, script inventory, test inventory, and
   Current audit wording to the current registry and strict-only contract.
5. Preserve private finite historical conversion/read fixtures only when they
   are pinned, fail closed outside the exact transition, and are not reachable
   as an active production fallback.

### CCPC-002 — Closure matrix and Current audit

1. Map VAL-CCPC-001 through VAL-CCPC-006 and every PRD-0006 requirement to
   commands, result class, changed path or commit, reviewer, limitation,
   rollback, and follow-up owner.
2. Re-run archive integrity, historical-link, execution-disposition,
   reference, generated-output, workflow, selector, and residue checks.
3. Update the Current audit overlay with observed repository-static facts.
   Preserve current hosted/provider/live `DEFER` rows and their triggers.
4. Confirm every migration row has a terminal disposition and rollback
   reference without modifying the settled ledger during activation.

### CCPC-003 — Whole-branch QA and review

1. Run focused tests and all affected-surface validators for the cumulative
   branch diff.
2. Run lifecycle self-tests and staged validation, strict registry/profile/link
   validation, the repository aggregate, and `pre-commit run --all-files`.
3. Review formatter changes, rerun any mutated lane, and require both staged
   and unstaged diff checks to pass.
4. Give independent reviewers the exact proposal digest, merge-base range,
   criteria, limitations, and rollback chain. Remediate every blocking finding
   and obtain fresh verdicts.

### CCPC-004 — Atomic closure and postflight

1. Committed one terminal lifecycle closure that changes PRD-0006 from `active`
   to `done`, AD-0009 from `active` to `accepted`, and Spec 040, this Plan,
   its Task, their indexes, and the final registry relation from `active` to
   `done`. Updated the accepted decision evidence required by the lifecycle
   contract in the same proposal.
2. Passed terminal lifecycle, strict document, residue, reference, aggregate,
   unqualified all-files, formatter, and diff gates for the exact staged
   proposal.
3. Recorded independent terminal review for staged diff SHA-256
   `e146fb13fb3a62db014e6317992a4f519b79ba330253c4c5fe89834dc67e1888`:
   `/root/ccpc004_terminal_requirements_review` returned `REQUIREMENTS
   COMPLIANT`, `/root/ccpc004_terminal_quality_review` returned `QUALITY
   APPROVED`, and `/root/ccpc004_terminal_security_review` returned `SECURITY
   APPROVED`; all reported no findings.
4. Observed exact terminal closure commit
   `c5adc27b13893d7cbd1266c9225372cfb7df79e9` with parent
   `35d8552ba423e3e2d92294ddeb81674392b8f333`.
5. Recorded explicit-ref lifecycle and clean-tree repository-static aggregate
   PASS for the parent-to-closure interval. An initial over-wide
   activation-to-closure comparison
   `5c7bb820d9b424577eda3eb3a5c368f0c7cfc656..c5adc27b13893d7cbd1266c9225372cfb7df79e9`
   failed because it combined ADR/AD creation with terminal transition; the
   correct atomic terminal interval passed. Remote/live lanes remain `DEFER`
   until separately authorized and executed. This evidence-update commit is
   unidentified and unclaimed.

## Verification Plan

| Lane | Commands or method | Required result |
| --- | --- | --- |
| Focused strict cutover | Focused unit tests for the three active readers and retirement guard | No-mode strict behavior passes; compatibility invocation is rejected; finite pinned history remains fail closed |
| Lifecycle | `python3 scripts/validate-document-lifecycle.py --root . --self-test`; staged mode during proposals; explicit-ref mode after closure | Self-test, reciprocal activation, atomic closure, and observed-ref postflight pass |
| Registry and document contracts | `python3 scripts/validate-document-contract-registry.py --self-test`; strict registry, Markdown-profile, and owner/link commands | Zero uncovered/ambiguous routes, profile violations, duplicate current owners, or broken current links |
| Archive and migration | Archive integrity, historical-link, active-corpus residue, and final-disposition suites | Every governed archive and baseline execution record passes; settled evidence remains protected |
| Reference and generated surfaces | Reference IA, generated-output, workflow, and selector self-tests and production checks | Every current owned surface passes with stable ownership |
| Repository QA | `bash scripts/validate-repo-quality-gates.sh .`; `pre-commit run --all-files`; formatter/status review; `git diff --check`; `git diff --cached --check` | Aggregate final marker and every applicable hook pass; optional no-file lanes are explicit SKIP; no unreviewed formatter mutation |
| Independent review | Requirements and quality/security reviewers inspect the exact cumulative and terminal proposals | No unresolved Critical or Important finding |
| External evidence | Hosted CI, provider, remote, and live systems | `DEFER` unless separately authorized and observed; no inference from repository-static PASS |

### Legacy Task verification evidence

The current input state is observed: Spec 039 closure
`e1d1e910840337327a557ab4b84e86f8fced11d6` and its clean-tree
repository-static postflight are PASS, and evidence update
`11a020d9b299ae91b7af9278c22ed89ffccb5cfc` is the base for this activation.
Current hosted, provider, remote, and live lanes remain `DEFER`; historical
hosted run `29982910320` remains FAIL for its older SHA.

The Spec 040 activation is observed in
`5c7bb820d9b424577eda3eb3a5c368f0c7cfc656`. Plan-only lifecycle exited `1`
with `LIFECYCLE-CREATE`, Plan count `1`, and Task count `0`. Exact-six staging
then passed lifecycle; registry self-test `119` and strict registry
`450` with zero uncovered/ambiguous routes; strict Markdown with zero
findings; strict links/owners; residue closure at active controls `2/1`,
terminal controls `4/2`, terminal Specs `2`, and findings `0`; diff-check; and
the repository aggregate final marker. `pre-commit run --all-files` passed
every applicable hook, Dockerfile lint was a no-file `SKIP`, and no formatter
mutation remained. Reviewer `/root/spec040_activation_requirements` returned
`REQUIREMENTS COMPLIANT`; `/root/spec040_activation_quality` returned
`QUALITY APPROVED` after its sole stale-fallback finding was fixed. The
activation commit then passed explicit-ref lifecycle from
`11a020d9b299ae91b7af9278c22ed89ffccb5cfc` and the clean-tree aggregate.

CCPC-001 began with 6 focused tests and 14 intentional RED failures. The
strict-only implementation now passes all 6 tests, registry self-test `119`,
Markdown and cross-document self-tests, and all three validators in both
no-mode and explicit strict production. Each retired compatibility invocation
is rejected by argparse with exit `2`; strict registry reports `450` paths,
strict Markdown reports zero findings, strict links/owners passes, and
diff-check passes. The finite Spec 033 retirement guard remains closed and the
retired semantic-debt fixture remains absent. Reviewer
`/root/spec040_ccpc001_requirements` returned `REQUIREMENTS COMPLIANT`, and
`/root/spec040_ccpc001_quality` returned `QUALITY APPROVED`. The CCPC-001
regression initially failed the staged aggregate with
`ROLE-AUDIT-HELPER-ADMISSION`; its identity-bound post-closure admission now
passes role-audit tests `36`, self-test `28`, and production with helpers
`44/33/11`, formats `16/21/6/1`, and findings `0`. The CCPC-001 logical commit
proposal then passed staged lifecycle, the repository aggregate final marker,
and every applicable all-files hook; Dockerfile lint was a no-file `SKIP`,
neither formatter nor unstaged drift changed the proposal, and both diff
checks passed. Reviewers `/root/spec040_ccpc001_final_requirements` and
`/root/spec040_ccpc001_final_quality` returned `REQUIREMENTS COMPLIANT` and
`QUALITY APPROVED` for pre-evidence digest
`f83ec5afb90b6c2cb7d35e9c5259d5c8358697e6d7304bfa9cde39ddf9c1b360`.
The logical implementation commit is
`0ae1fcd300d43914901d0eb2f0fd929bfe65cb1d`. Explicit-ref lifecycle from
activation `5c7bb820d9b424577eda3eb3a5c368f0c7cfc656` to that commit passed, as
did the clean-tree focused regression, role-audit production, status/diff
checks, and repository aggregate final marker. This postflight evidence update
does not identify or claim its own commit. CCPC-001 and CCPC-002 are done.
CCPC-003 whole-branch QA and independent review are recorded below, and
CCPC-004 completes the exact staged terminal proposal, observes terminal
closure commit `c5adc27b13893d7cbd1266c9225372cfb7df79e9`, and records
parent-to-closure explicit-ref lifecycle plus clean-tree repository aggregate
PASS. This evidence-update commit does not identify or claim its own commit.

The exact CCPC-002 evidence proposal with staged digest
`4f3e372d6842547c9ded7e098bb3c434b7e76230a23d137307c3c7ada8c6d8e8`
was independently reviewed across every criterion, requirement, quality
attribute, limitation, rollback/follow-up owner, and retained result class.
Reviewer `/root/spec040_ccpc002_evidence_requirements` returned
`REQUIREMENTS COMPLIANT`, and
`/root/spec040_ccpc002_evidence_quality` returned `QUALITY APPROVED`. This
evidence-only addition does not identify its own commit or claim CCPC-003,
CCPC-004, hosted, provider, remote, credential, or live completion.

CCPC-003 whole-branch QA observed the original effective-identity portability
blocker and remediated it in `9cc36e81d26e7b52cb00d9381cdc1a56db57afa6`. The
final cumulative range is
`32ffb7fce2147e485c94443479e82bba261b3d9c..9cc36e81d26e7b52cb00d9381cdc1a56db57afa6`
(30 commits, 68 changed paths) with binary diff SHA-256
`f8e4641a91a7d4c4f08f7d03fdf14422a85b4be9b9df133a6dd011e57a3cf241`.
Focused cumulative modules passed `253` tests, portability passed `16`
including the simulated non-root effective-identity fixture, lifecycle
self-test passed `668` cases with clean staged lifecycle, and the final
affected lane selected 10 validators for 68 paths and every validator passed.
`pre-commit run --all-files` exited `0` with every applicable hook passing and
Dockerfile lint a no-file `SKIP`; formatter/status inspection and both cached
and unstaged diff checks were clean. Final reviewers
`/root/spec040_ccpc003_whole_branch_requirements`,
`/root/spec040_ccpc003_whole_branch_quality`, and
`/root/spec040_ccpc003_whole_branch_security` returned `REQUIREMENTS
COMPLIANT`, `QUALITY APPROVED`, and `SECURITY APPROVED`. This evidence-only
addition does not claim its own commit, CCPC-004 terminal closure, hosted,
provider, remote, credential, or live completion.

CCPC-004 closes exactly the 14 paths named in its Task row in terminal closure
commit `c5adc27b13893d7cbd1266c9225372cfb7df79e9` from parent/prerequisite
`35d8552ba423e3e2d92294ddeb81674392b8f333`. CCPC-003 evidence commit
`a65a2e838a54a405e20da65197de2828cf05bcd5` remains the earlier
whole-branch QA/review evidence point.
Lifecycle self-test `668` and staged lifecycle pass; strict registry,
Markdown, and links/owners pass; the residue focused module, self-test, and
production pass at final frontier `active_controls=0/0`,
`terminal_controls=6/3`, and `terminal_specs=3`; reference IA, the repository
aggregate, unqualified all-files pre-commit, formatter review, and both diff
checks pass. Independent terminal reviewers inspected staged diff SHA-256
`e146fb13fb3a62db014e6317992a4f519b79ba330253c4c5fe89834dc67e1888`:
`/root/ccpc004_terminal_requirements_review` returned `REQUIREMENTS
COMPLIANT`, `/root/ccpc004_terminal_quality_review` returned `QUALITY
APPROVED`, and `/root/ccpc004_terminal_security_review` returned `SECURITY
APPROVED`; all reported no findings. Explicit-ref lifecycle for
`35d8552ba423e3e2d92294ddeb81674392b8f333..c5adc27b13893d7cbd1266c9225372cfb7df79e9`
passed, and clean-tree repository aggregate, status, and diff inspection
passed. An initial over-wide activation-to-closure comparison
`5c7bb820d9b424577eda3eb3a5c368f0c7cfc656..c5adc27b13893d7cbd1266c9225372cfb7df79e9`
failed because it combined ADR/AD creation and terminal transition; the
correct atomic terminal parent-to-closure interval passed. This evidence-update
commit is unidentified and unclaimed. Hosted, provider, remote, credential, and
live PASS remains unclaimed.

### Closure Matrix

This matrix is the CCPC result ledger. `PASS` means repository-static evidence
has been observed and recorded in this Task. `Pending` means future observed
commit/postflight evidence still has to be recorded. `DEFER` means an external,
hosted, provider, remote, live, or credential-bearing lane is intentionally not
claimed by this local Task.

#### Spec 040 Criteria

| Criterion | Owner | Command / evidence | Result class | Limitation | Rollback / follow-up owner |
| --- | --- | --- | --- | --- | --- |
| VAL-CCPC-001 — active compatibility, retired Stage 99 archive profile/form claims, and stale wording are zero | CCPC-001 | `python3 -m unittest tests/test_document_strict_cutover.py`; registry, Markdown, and links/owners no-mode and explicit strict production PASS; retired `--mode compatibility` exits `2`; implementation `0ae1fcd300d43914901d0eb2f0fd929bfe65cb1d`; postflight `98ed9c6`; wording remediation `d99b183` | PASS | Repository-static only; provider/runtime/native behavior is not inferred. | Revert the wording remediation and CCPC-001 logical unit newest-first; do not restore an active compatibility reader. |
| VAL-CCPC-002 — uncovered routes, ambiguous routes, duplicate current owners, invalid transitions, and broken current links are zero | CCPC-001 / CCPC-002 | Registry self-test `119`, strict registry `451` with uncovered/ambiguous `0/0`, strict Markdown zero, links/owners self/production PASS, lifecycle self-test `668`, and residue advanced frontier `2/1·4/2·2` with findings `0` | PASS | Repository-static current frontier only; CCPC-004 owns the terminal transition and provider/remote/live behavior is not inferred. | Revert the newest responsible strict/frontier unit, rerun this exact group, and preserve the external `DEFER` owners. |
| VAL-CCPC-003 — archive provenance and historical links pass for every archived record | CCPC-002 | `python3 -m unittest tests/test_archive_recovery.py`; `python3 -m unittest tests/test_archive_validation.py`; `python3 -m unittest tests/test_archive_cutover.py`; `python3 -m unittest tests/test_document_lifecycle_archive_cutover.py`; `python3 scripts/archive_cutover.py --root .` | PASS | Repository-static only: tests pass `15/22/27/17`, and production reports records `43`, historical links `362`, secret-clean records `43`. | Revert the newest archive-affecting logical unit and rerun the same five commands; no live or secret-value evidence is inferred. |
| VAL-CCPC-004 — every baseline Plan/Task has a final migration disposition | CCPC-002 | Retention self/production `27` and `110/2/24/29→30`; eligibility `54` and `110/12/98/2`; migration `32` and trusted-Gitleaks production `6/12/43/362/12/15`; role audit `36/28/44/33/11`; residue `85/23` with `100` owned `DEFER`, `0` retain, and findings `0` | PASS | The settled migration ledger remains read-only; retained rows are explicitly owned `DEFER`, and Spec 040 active controls remain until CCPC-004. | Revert the newest lineage-scoped unit, use the recorded rollback-parent chain, and rerun retention through residue without rewriting settled evidence. |
| VAL-CCPC-005 — references, generated outputs, workflows, selectors, and result classes pass their complete contract | CCPC-002 / CCPC-003 | RIA tests `85`, self/root PASS; generated LLM Wiki current; GitHub Actions security self/production PASS; CI Python `9/13` and `3/3`; affected surfaces `739`, `21/21`, validators `12`, CI jobs `3`, uncovered/ambiguous `0/0`; workspace, agent semantics `480/30`, and repository aggregate PASS | PASS | Repository-static result only; hosted workflow run `29982910320` remains a historical older-SHA FAIL, while current hosted/provider/remote/live lanes remain `DEFER`. | CCPC-003 reruns the cumulative whole-branch group; any remote retry requires separate approval and evidence. |
| VAL-CCPC-006 — all-files pre-commit and independent whole-branch review pass with remote/live limitations preserved | CCPC-003 / CCPC-004 | CCPC-003 cumulative range `32ffb7fce2147e485c94443479e82bba261b3d9c..9cc36e81d26e7b52cb00d9381cdc1a56db57afa6` and independent whole-branch approvals; exact CCPC-004 14-path staged proposal passes lifecycle `668`, staged/strict/residue/reference/aggregate, unqualified all-files pre-commit, formatter review, and both diff checks at `0/0·6/3·3`; staged diff SHA-256 `e146fb13fb3a62db014e6317992a4f519b79ba330253c4c5fe89834dc67e1888` is approved by terminal requirements, quality, and security reviewers with no findings; terminal closure commit `c5adc27b13893d7cbd1266c9225372cfb7df79e9` and explicit-ref lifecycle from parent `35d8552ba423e3e2d92294ddeb81674392b8f333` are observed | PASS | Repository-static PASS covers whole-branch review, exact terminal precommit validation, observed terminal review, terminal closure commit, and parent-to-closure postflight. This evidence-update commit is unidentified and unclaimed; hosted/provider/remote/live lanes remain `DEFER`. | The future evidence-update committer records only the commit it actually creates while preserving `DEFER` lanes. |

#### PRD-0006 Requirements and Acceptance

| PRD item | Acceptance item | Owner | Command / evidence | Result class | Limitation | Rollback / follow-up owner |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-0006-FR-0001 — `document-profiles.json` remains the sole machine owner | ACC-WDLEC-001 | Spec 034 / CCPC-002 | Registry self-test `119`; strict registry `451`, programs `2`, uncovered `0`, ambiguous `0`; strict Markdown and links/owners PASS | PASS | Repository-static registry/current-owner authority only; provider-native discovery is not inferred. | Revert the newest registry-affecting unit and rerun registry, Markdown, and links/owners as one group. |
| REQ-0006-FR-0002 — Spec 033 is a follow-up, not an eighth original tranche | ACC-WDLEC-002 | ADR-0017 / Spec 034 / CCPC-004 | Registry `programLineage` keeps PRD-0005 Specs 026-032 as original tranches and Spec 033 as a follow-up; PRD-0006 Specs 034-040 are terminal tranches with Spec 040 `done` in exact closure commit `c5adc27b13893d7cbd1266c9225372cfb7df79e9` | PASS | Repository-static lineage only; no provider/runtime/native behavior is inferred. | Revert the terminal closure commit newest-first without changing accepted ADR-0017 history. |
| REQ-0006-FR-0003 — closed metadata and state-transition contracts | ACC-WDLEC-003 | Spec 035 / CCPC-002 / CCPC-004 | Strict registry/Markdown/links PASS; lifecycle self-test `668`; exact current advanced frontier validator and aggregate PASS; terminal closure commit `c5adc27b13893d7cbd1266c9225372cfb7df79e9` records the PRD/AD/Spec/Plan/Task/ADR transition comparison | PASS | Repository-static closed contract is proved; this evidence-update commit is unidentified and unclaimed. | Revert the newest contract unit and rerun strict plus lifecycle gates; CCPC-004 owns terminal rollback. |
| REQ-0006-FR-0004 — retired metadata-only archive stubs replaced by full-body archives | ACC-WDLEC-004 | Spec 036 / ADR-0018 | Archive recovery, validation, cutover, lifecycle-archive tests `15/22/27/17`; production archive cutover `43/362/43` | PASS | Repository-static archive corpus and historical-link proof only. | Revert the newest archive-affecting logical unit and rerun the exact archive group. |
| REQ-0006-FR-0005 — current owners stay separate from archive records | ACC-WDLEC-005 | Spec 036 / CCPC-002 | Archive validation and lifecycle archive cutover pass; production historical links `362` | PASS | Current/source-tree separation is proved locally; remote object retention or live publication is not inferred. | Preserve full-body records and revert only the newest responsible current-link change. |
| REQ-0006-FR-0006 — eligible completed Plans and Tasks move or retain with evidence | ACC-WDLEC-006 | Spec 037 / CCPC-002 | Retention/eligibility/migration/role/residue group passes with `12` migrated records, `100` owned `DEFER`, exact rollback parents, archive `43/362`, and findings `0` | PASS | Settled ledgers remain read-only and retained `DEFER` is not promoted to migration eligibility. | Revert newest-first by lineage using recorded rollback parents, then rerun the complete active-corpus group. |
| REQ-0006-FR-0007 — active-stage cardinality is lifecycle-based | ACC-WDLEC-006 | Spec 037 / CCPC-002 / CCPC-004 | Exact terminal frontier passes at active controls `0/0`, terminal controls `6/3`, and terminal Specs `3` | PASS | Repository-static lifecycle cardinality only; it is not a numeric file-count quota or live/provider evidence. | Revert the exact terminal closure commit and rerun the same residue validator. |
| REQ-0006-FR-0008 — reference, audit, data, generated, learning, archive, and scratch boundaries are clear | ACC-WDLEC-007 | Spec 038 / CCPC-002 | RIA tests `85`, self/root PASS; generated LLM Wiki current; Current overlay updated without changing source rows, scores, or protected frontmatter | PASS | Repository-static taxonomy/currentness proof only; external knowledge/provider freshness is not inferred. | Revert only the mutable roadmap overlay, regenerate derived output, and rerun RIA plus generator checks. |
| REQ-0006-FR-0009 — `_workspace` stays ignored, temporary, non-secret support scratch | ACC-WDLEC-001 | Spec 036 / CCPC-002 | Workspace-boundary self/production and repository aggregate PASS | PASS | Ignored children, auth files, tokens, kubeconfigs, shell history, and secret values are deliberately unread and out of scope. | Revert the newest boundary-policy unit and rerun workspace plus aggregate checks without inspecting ignored children. |
| REQ-0006-FR-0010 — GitHub CI aligns affected lanes, aggregate verdict, retention, and least privilege | ACC-WDLEC-008 | Spec 039 / CCPC-002 | GitHub Actions security self/production PASS; CI Python `9` rules/`13` cases and `3` jobs/`3` pins; affected surfaces `739/21/12/3/0/0`; aggregate PASS | PASS | Static workflow contract only; no current hosted Actions run is claimed and historical run `29982910320` remains older-SHA FAIL. | Revert the newest workflow-contract unit and rerun static checks; remote retry remains separately approved. |
| REQ-0006-FR-0011 — logical commits, independent review, full QA, and revertable migration boundaries | ACC-WDLEC-008 | Spec 040 / CCPC-003 / CCPC-004 | CCPC-003 whole-branch QA/review is approved; exact CCPC-004 14-path terminal proposal passes lifecycle `668`, staged/strict/residue/reference/aggregate/all-files/formatter/diff gates and terminal requirements/quality/security review for staged diff SHA-256 `e146fb13fb3a62db014e6317992a4f519b79ba330253c4c5fe89834dc67e1888`; terminal closure commit `c5adc27b13893d7cbd1266c9225372cfb7df79e9` and parent-to-closure explicit-ref/aggregate postflight are observed | PASS | This evidence-update commit is unidentified and unclaimed. | The future evidence-update committer records only the commit it actually creates and uses the newest-first rollback chain. |
| REQ-0006-NFR-0001 — protected surfaces, secrets, and live approval boundaries are preserved | ACC-WDLEC-009 | Spec 040 / CCPC-004 | Task safety boundaries forbid live/provider/credential mutation without approval | DEFER | Remote Actions, branch protection, Kubernetes, Vault, ESO, Argo CD, provider, credential, and secret-value evidence are not local repository-static facts. | Human-approved future live/provider Tasks own any non-static evidence. |
| REQ-0006-NFR-0002 — operations and helper Tests roles have one role-specific contract | ACC-WDLEC-010 | Spec 035 / Spec 037 / CCPC-002 | Role-audit tests `36`, self-test `28`, production helpers `44/33/11`, formats `16/21/6/1`, findings `0`; agent semantics `480` cases and `30` adapters | PASS | Proves repository-static helper and role contracts only; no provider/runtime behavior is claimed. | Revert the newest helper-admission or role-contract unit and rerun both validators. |

#### AD-0009 Quality Attributes

| Quality attribute | Owner | Command / evidence | Result class | Limitation | Rollback / follow-up owner |
| --- | --- | --- | --- | --- | --- |
| Integrity — archive bytes and current owners are verified by source commit, blob, and digest | Spec 036 / CCPC-002 | Archive tests `15/22/27/17`; production archive cutover records `43`, historical links `362`, secret-clean records `43` | PASS | Repository-static corpus proof only; no secret value is opened or reported. | Revert the newest archive-affecting logical unit and rerun the complete archive group. |
| Traceability — tranches, follow-ups, transitions, execution closure, replacements, and `DEFER` outcomes have owners | Spec 034 / Spec 037 / CCPC-002 / CCPC-004 | Registry, lifecycle `668`, links/owners, exact 14-path transition, reciprocal accepted ADR-0020, and terminal frontier `0/0·6/3·3` PASS | PASS | Repository-static traceability only; external owners remain `DEFER`. | Revert the exact terminal closure commit atomically and preserve accepted ADR-0017/0018 history. |
| Reliability — migration is fail-closed and lineage-scoped | Spec 037 / CCPC-002 | Retention/eligibility/migration/role/residue group passes with exact six-pair migration, rollback-parent chain, `100` owned `DEFER`, and findings `0` | PASS | Repository-static settled evidence only; ledgers remain read-only and no new eligibility is inferred. | Revert the newest lineage unit using its recorded rollback parent and rerun the full group. |
| Security — ignored local state, secrets, workflows, and live surfaces remain bounded | Spec 039 / Spec 040 | Workspace boundary, GitHub Actions security, CI Python, affected surfaces, secrets hooks, and repository aggregate PASS locally | DEFER | Static checks pass, but provider, remote, branch protection, Kubernetes, Vault, ESO, Argo CD, and secret-value evidence are not inferred. | Human-approved follow-up owner per live/provider lane. |
| Operability — each tranche has isolated Plan, Task, review, commit, validation, and revert boundary | Spec 040 / CCPC-003 / CCPC-004 | CCPC-003 whole-branch QA/review is approved; exact CCPC-004 proposal has a 14-path boundary, passing precommit matrix, observed terminal review, closure commit, explicit-ref lifecycle, clean-tree postflight, and newest-first rollback handoff | PASS | This evidence-update commit is unidentified and unclaimed. | The future evidence-update committer owns the remaining observed evidence. |
| Scalability — active stages are bounded by lifecycle/current-owner cardinality rather than file-count quotas | Spec 037 / CCPC-002 / CCPC-004 | Exact terminal frontier `0/0·6/3·3`, active-corpus `100` owned `DEFER`, and aggregate PASS | PASS | Repository-static lifecycle cardinality only; external systems remain `DEFER`. | Revert the exact terminal closure commit without introducing a numeric file-count quota. |

## Risks & Mitigations

| Risk | Mitigation | Owner |
| --- | --- | --- |
| Removing a historical proof reader breaks the bounded transition regression | Separate active fallback behavior from pinned, private, fail-closed historical fixtures; test both boundaries before deletion | platform |
| Strict default changes silently alter diagnostics | Start with focused RED tests; preserve stable rule IDs and exit semantics; review exact output contracts | platform |
| Final status changes are split across commits | Use the lifecycle validator's complete-product, accept-architecture, complete-specification, and execution-pair predicates in one terminal proposal | platform |
| Closure prose overstates remote evidence | Keep local PASS, historical hosted FAIL, and current hosted/provider/live DEFER in separate result rows | platform |
| Completed historical bodies are rewritten | Limit currentness edits to active contracts, indexes, inventories, and Current audit surfaces; retain immutable historical evidence | platform |
| Formatter or generated output mutates the proposal after review | Reinspect status and diffs, rerun affected and all-files gates, and refresh reviews for the final digest | platform |
| Rollback would overwrite unrelated work | Revert newest logical units only; never reset, clean, or rewrite shared history | platform |

### Legacy Task approval and rollback boundaries

- **Allowed Paths**: Spec 040 and its reciprocal Plan/Task/index/progress
  lineage; current document validators and their focused tests/fixtures;
  current Stage 99 support, script/test inventories, Current audit overlay,
  closure-matrix evidence, PRD-0006/AD-0009 and ADR-0017/0018/0020 lifecycle
  and decision evidence,
  document registry final relation, and directly affected repository-static
  QA surfaces authorized by the Plan.
- **Forbidden Paths**: Specs 041-046 implementation; provider adapters, models,
  roster, and shared-provider memory; `.gemini/**`; Kubernetes/GitOps desired
  state; infrastructure, Vault, ESO, Argo CD, deployment, release, credentials,
  secret values, ignored `_workspace` children, auth files, tokens,
  kubeconfigs, and shell history.
- **Approval Required**: Push, merge, workflow dispatch, GitHub setting
  mutation, publication, dependency installation, live command, credential or
  secret access, and any expansion outside the Plan require separate explicit
  human approval.
- **Static Validation**: Focused tests; affected-surface checks; lifecycle
  self-test, staged, and explicit-ref modes; strict registry/profile/link
  checks; archive, migration, reference, generated-output, workflow and
  selector gates; repository aggregate; unqualified all-files pre-commit;
  formatter/status inspection; cached and unstaged diff checks.
- **Live Validation**: `DEFER`. No current hosted GitHub Actions, provider,
  remote, Kubernetes, Vault, ESO, Argo CD, cloud, deployment, or credential
  result is authorized by this Task.
- **Secret / Vault Handling**: Do not open, print, copy, hash, or report secret
  values. Evidence is limited to stable rule IDs, repository-relative paths,
  bounded counts, public run identifiers, and observed Git identities.
- **Rollback Plan**: Revert the newest observed logical unit first, rerun its
  focused and aggregate gates, and continue through the recorded chain only as
  needed. Revert activation last. Never reset, clean, rewrite shared history,
  or overwrite unrelated work.
- **Evidence Location**: This Task is the result ledger. The reciprocal Plan
  owns execution order; the Spec owns criteria; reviewed logical commits,
  exact tests/fixtures, the Current audit overlay, closure matrix, and progress
  ledger retain supporting evidence.
## Completion Criteria

- CCPC-000 through CCPC-004 each have an observed result and durable Task
  evidence.
- Active document readers have one strict contract; compatibility requests do
  not select a fallback path.
- Finite historical-transition fixtures remain only where pinned, bounded,
  private, and fail closed outside their exact event.
- VAL-CCPC-001 through VAL-CCPC-006 and every PRD-0006 requirement have
  traceable repository-static evidence, review disposition, rollback, and
  honest limitation.
- The full branch passes focused, affected, lifecycle, strict document,
  archive, migration, reference, generated-output, workflow, aggregate,
  all-files, formatter, and diff gates.
- CCPC-003 independent requirements and quality/security reviews approve the
  whole-branch implementation; CCPC-004 independent terminal requirements,
  quality, and security reviews approve the exact staged terminal proposal
  without findings.
- PRD-0006, AD-0009, ADR-0020, Spec 040, Plan, Task, indexes, progress, and the
  final registry relation transition atomically in exact 14-path closure commit
  `c5adc27b13893d7cbd1266c9225372cfb7df79e9`.
- Parent-to-closure explicit-ref lifecycle and clean-tree repository-static
  postflight are observed. This evidence-update commit itself remains
  unidentified and unclaimed. Current hosted, provider, remote, and live lanes
  remain `DEFER` unless separately authorized and observed.

## Traceability

- **Spec**: Contract Cutover and Program Closure Technical Specification
- **Task**: Contract Cutover and Program Closure Task
- **Program PRD**:
  [PRD-0006](../../01.requirements/0006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **Program AD**:
  [AD-0009](../../02.architecture/descriptions/0009-document-lifecycle-evidence-operating-model.md)
- **Decisions**:
  [ADR-0017](../../02.architecture/decisions/0017-program-follow-up-lineage-semantics.md),
  [ADR-0018](../../02.architecture/decisions/0018-full-body-archive-record-and-retention.md),
  and
  [ADR-0020](../../02.architecture/decisions/0020-document-lifecycle-program-closure-evidence.md)
- **Predecessor evidence**: Spec 039 closure
  `e1d1e910840337327a557ab4b84e86f8fced11d6` and evidence update
  `11a020d9b299ae91b7af9278c22ed89ffccb5cfc`

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-CCPC-001](spec.md#success-criteria--verification-plan) | CCPC-001 | [Strict-only reader and bounded historical-proof evidence](tasks/tsk-0002-ccpc-001.md) |
| N/A — VAL-CCPC-002 shares the Spec 040 source linked in VAL-CCPC-001 | CCPC-001, CCPC-002 | N/A — the paired Task is linked in VAL-CCPC-001 |
| N/A — VAL-CCPC-003 shares the Spec 040 source linked in VAL-CCPC-001 | CCPC-002 | N/A — the paired Task is linked in VAL-CCPC-001 |
| N/A — VAL-CCPC-004 shares the Spec 040 source linked in VAL-CCPC-001 | CCPC-002 | N/A — the paired Task is linked in VAL-CCPC-001 |
| N/A — VAL-CCPC-005 shares the Spec 040 source linked in VAL-CCPC-001 | CCPC-002, CCPC-003 | N/A — the paired Task is linked in VAL-CCPC-001 |
| N/A — VAL-CCPC-006 shares the Spec 040 source linked in VAL-CCPC-001 | CCPC-003, CCPC-004 | N/A — the paired Task is linked in VAL-CCPC-001 |

### Legacy Task traceability

- **Plan**: Contract Cutover and Program Closure Implementation Plan
- **Spec**: Contract Cutover and Program Closure Technical Specification
- **Predecessor evidence**: Spec 039 closure
  `e1d1e910840337327a557ab4b84e86f8fced11d6` and evidence update
  `11a020d9b299ae91b7af9278c22ed89ffccb5cfc`
- **Program**:
  [PRD-0006](../../01.requirements/0006-workspace-document-lifecycle-and-evidence-consolidation.md)
  and
  [AD-0009](../../02.architecture/descriptions/0009-document-lifecycle-evidence-operating-model.md)

#### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [CCPC-000](plan.md#ccpc-000--reciprocal-activation) | Done — Plan-only RED, exact-six lifecycle/strict/aggregate/all-files GREEN, both independent approvals, activation commit, explicit-ref lifecycle, and clean-tree aggregate observed. | `LIFECYCLE-CREATE` Plan `1` / Task `0`; lifecycle, registry `119/450`, Markdown, links/owners, residue active `2/1`, diff-check, aggregate, and applicable all-files PASS; requirements/quality approved; activation `5c7bb820d9b424577eda3eb3a5c368f0c7cfc656`. |
| [VAL-CCPC-001](spec.md#success-criteria--verification-plan) | Done — strict-only implementation, staged QA, final reviews, implementation commit, and postflight pass. | RED `6/14` plus helper-admission aggregate RED; GREEN focused `6/6`, role audit `36/28/44`, registry self-test `119`, three no-mode and strict production PASS, three compatibility exit `2`, strict registry `450`, Markdown zero, links/owners, lifecycle, aggregate, all-files, and diff checks PASS; final requirements/quality approved; implementation `0ae1fcd300d43914901d0eb2f0fd929bfe65cb1d`; explicit-ref and clean-tree aggregate PASS. |
| N/A — VAL-CCPC-002 shares the Spec 040 source linked in VAL-CCPC-001 | Done — exact current route, owner, transition, link, and advanced-frontier evidence passes. | Registry `119/451/0/0`, Markdown zero, links/owners, lifecycle `668`, residue `2/1·4/2·2` and findings `0`. |
| N/A — VAL-CCPC-003 shares the Spec 040 source linked in VAL-CCPC-001 | Done — archive provenance and historical links pass. | Archive tests `15/22/27/17`; production `43/362/43`. |
| N/A — VAL-CCPC-004 shares the Spec 040 source linked in VAL-CCPC-001 | Done — every baseline execution row has a migrated or owned `DEFER` disposition and rollback evidence. | Retention/eligibility/migration/role/residue PASS; migration `6/12/43/362/12/15`, current `100` owned `DEFER`, findings `0`. |
| N/A — VAL-CCPC-005 shares the Spec 040 source linked in VAL-CCPC-001 | Done for CCPC-002 repository-static scope. | RIA `85` plus self/root, generated index, workflow security, CI Python, affected surfaces `739/21/12/3/0/0`, workspace, agent semantics, and aggregate PASS; hosted/provider/live remain `DEFER`. |
| N/A — VAL-CCPC-006 shares the Spec 040 source linked in VAL-CCPC-001 | Done — CCPC-003 whole-branch QA/review and the exact CCPC-004 terminal closure are repository-static complete with observed terminal review and postflight. | Exact 14 paths; closure commit `c5adc27b13893d7cbd1266c9225372cfb7df79e9`; parent `35d8552ba423e3e2d92294ddeb81674392b8f333`; lifecycle `668`, staged/strict/residue/reference/aggregate/all-files/formatter/diff PASS; frontier `0/0·6/3·3`; reviewed digest `e146fb13fb3a62db014e6317992a4f519b79ba330253c4c5fe89834dc67e1888`; terminal requirements, quality, and security verdicts approved with no findings; parent-to-closure explicit-ref and clean-tree aggregate PASS. This evidence-update commit remains unclaimed. |
