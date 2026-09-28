---
title: "Standardize Archive Lifecycle"
version: "0.1.1"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-28"
layer: "specs"
artifact_id: "SPEC-0100-TSK-0001"
---

# Task: Standardize Archive Lifecycle

## Overview

Record execution of [SPEC-0100](../spec.md) on the `d2296de9ea66ea80c27fcc965c21d552febb057d` baseline in the managed detached worktree. The approved scoped implementation and repository-static verification are complete. The published package retains its legal initial `draft`/`draft`/`queued` frontmatter until actual lifecycle transitions; Archive disposition remains pending. Past Task or CI results are not this run's test results.

## Inputs

The [Plan](../plan.md), [ADR-0040](../../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md), [REQ-0003](../../../01.requirements/0003-workspace-agent-governance-platform.md), [AD-0006](../../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), [document lifecycle policy](../../../../.agents/governance/document-lifecycle.md), [Stage 99 registry](../../../99.templates/registry.json), [Archive index](../../../98.archive/README.md), and the user's 2026-09-28 common 3.0.0 proposal are inputs. ADR-0040 is accepted. The user approved only the common proposal's Spec/Plan/Task `done` → `completed` spelling on 2026-09-28, with the same terminal meaning; its other state and field proposals are not accepted.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-ARC-001, VAL-ARC-003 | Recheck accepted policy, machine contract, callers and baseline | supervisor/quality | Verified | Policy/registry/caller map and catalog inventory reviewed; final full QA PASS | S/V binding, inventory and final 22-gate result below |
| WORK-002 | VAL-ARC-001, VAL-ARC-003 | Reproduce and repair confirmed shared-validator and QA defects | repo-tooling/quality | Verified | V12/V27 RED/GREEN; three initial unit failures repaired; independent review found no remaining finding; final unit suite PASS | Focused regressions and full QA chronology below |
| WORK-003 | VAL-ARC-002 | Reconcile current template, policy, REQ/AD and README guidance | doc-writer/wiki-curator | Verified | Current documents and four READMEs authored; links/profiles and final full QA PASS | 17-path repair recheck, 45-path quick and 1,228-path full below |
| WORK-004 | VAL-ARC-004, VAL-ARC-006 | Integrate research and migrate approved Spec/Plan/Task terminal spelling | docs-researcher/architect/doc-writer | Verified | Dated source addendum and spelling migration complete: 11 live `completed`, 492 frozen `done` unchanged; focused state tests and full QA PASS | Research m0001, Spec contract, consumer inventory and migration checks below |
| WORK-005 | VAL-ARC-005 | Targeted, quick, full QA, review and final handoff | quality/supervisor | Verified; follow-up reviewed | Prior FAIL attempts preserved; original quick 13/13 and full 22/22 PASS; current follow-up full 22/22 PASS | Original and dated follow-up evidence below; Task-only refresh pending |

## Approval and Safety Boundaries

- **Allowed Paths**: this SPEC-0100 package; current `.agents/governance/document-lifecycle.md`; current REQ-0003 and AD-0006 wording; existing Archive research member; Incident template; relevant `docs/01.requirements/README.md`, `docs/02.architecture/decisions/README.md`, `docs/02.architecture/descriptions/README.md`, `docs/03.specs/README.md`; existing Archive validators and focused tests for reproduced defects; `.secrets.baseline` metadata-only correction for existing line numbers and timestamp; formatter-only changes to the two affected Archive test files; current Spec/Plan/Task registry and validation consumers, eleven live frontmatter values, current lifecycle policy and Stage 03 README for the approved spelling migration; tests for language state, agent governance content restore, Archive budget and bounded runner cleanup plus their shared implementation owners.
- **Forbidden Paths**: frozen Stage 98 bodies, sealed capture rows, provider settings, cluster manifests, private config/credentials and unrelated work.
- **Approval Required**: in the original implementation phase, the user approved the current Spec/Plan/Task `done`→`completed` spelling migration on 2026-09-28, preserving terminal meaning and leaving frozen history intact. New metadata/state semantics, Incident changes, actual retained-unit removal, secret/security handling, live or remote state changes and push/merge required their own scoped authority; later publication is recorded below. The user authorized publication and cleanup for this continuing follow-up; this document edit performs neither action.
- **Static Validation**: focused archive/profile tests, affected `quick`, exact-index `staged` if a commit is authorized, final `full`, `git diff --check`, frozen-path diff and independent review. Record results only after execution.
- **Live Validation**: DEFER — no cluster, service or provider-runtime observation was made in this document task. The later hosted CI result for PR #108 is recorded separately below.
- **Secret / Vault Handling**: do not read or record secret values, credentials, private logs or Vault resources; refer any real exposure to the security/incident owner.
- **Rollback Plan**: use reviewed forward correction on only changed mutable current files. Preserve other work, Git history and frozen records; no reset, rebase, force cleanup or Archive restoration experiment.
- **Evidence Location**: this Task for actual commands and decisions; Git for recovery; existing research member for dated external findings.

## Verification Summary

### Current snapshot and scope

The observation baseline is `d2296de9ea66ea80c27fcc965c21d552febb057d`; the delegated worktree began as `HEAD (no branch)` with an empty short status. The final reviewed change spans 47 working-tree paths (43 tracked changes, the three new SPEC-0100 files and one new test). At that original local verification snapshot, the original checkout was clean and the worktree index and Stage 98 diff were empty. The approved migration leaves 11 current Spec/Plan/Task frontmatter values at `completed` and all 492 frozen Stage 98 `done` values unchanged. Final repository-static full QA passed at that snapshot; no commit, hosted CI, staged/message or live result was claimed for the original local verification phase. Publication evidence is recorded below; live behavior remains unobserved.

A direct working-tree links/owners diagnostic returned FAIL at `ARCHIVE-MIGRATION-STAGED-DRIFT`: the migration recovery proof differs between target/consumer index and worktree (`scripts/archive_validation.py` near line 1734). This is a mixed-snapshot diagnostic, not a successful source check. The canonical isolated quick/full QA profiles must supply separate evidence; no index is staged to silence the direct failure.

The first canonical `python3 scripts/qa.py quick --root . --base-ref HEAD` ended FAIL (exit 1) on a 17-path working-tree snapshot: 12 of 13 selected gates PASS and `links-and-owners` FAIL with four `BODY-LINK-RECIPROCAL` findings from the new Spec to REQ-0003. The current REQ Traceability now links back to SPEC-0100. A post-fix isolated bounded recheck of `links-and-owners` and `markdown-profiles` over 17 affected paths passed (exit 0); this repairs the link finding without relabeling the original quick run. The other twelve original gate PASS results apply only to their earlier bytes. A later canonical quick over 18 changed paths passed all 13 selected gates (exit 0), including the final guard and prior Task evidence bytes. After the approved migration and QA repairs, a new canonical quick over 45 paths also passed 13/13 gates (exit 0). The final full-profile result is recorded below.

The QA owner reported six focused V12/V27 regression tests and the bounded `archive-contract-tests` gate PASS after the shared ancestor-scan repair. The repair spans `scripts/archive_dispositions.py`, `scripts/archive_cutover.py`, `scripts/validate-document-lifecycle.py`, `tests/test_archive_disposition_lifecycle.py` and `tests/test_archive_catalog_reverification.py`. The focused tests cover merge ancestry, unrelated branch exclusion and valid `git-history-only` removal. Final full QA separately passed below.

The temporary tracked-document inventory at the baseline classified 850 Markdown paths and 44 README routers, with zero unclassified routes. It separately observed this package's three untracked draft files; its regex-extracted inbound/outbound references are navigation evidence, not an authority validator. The four edited READMEs received semantic review by the wiki curator. A direct Registry/working-tree measurement found 53 Archive catalog rows and retained units, 183 payload files, zero Assessment rows and zero catalog parse errors: sixteen legacy rebased units/files, two current single-document units/files, and 35 current package/bundle units containing 165 files. The 53 class rows are superseded 20, completed 28 and retired 5. The same measurement classified 25 frozen tombstone Markdown records, 23 frozen migration records, and 608 Stage 98 Markdown paths with zero unclassified. These are this run's measured inventory, separate from README historical counts.

### Publication and current follow-up (2026-09-28)

The original implementation was subsequently committed as `5bc55bbbaba61001a532b57ae3b44a1b0fab95c0` and published in PR #108. Hosted CI run [36374095637](https://github.com/buenhyden/hy-home.k8s/actions/runs/36374095637) completed successfully for that PR head; merge commit `3d2ad80643cc5701ebd0ed42c8baf875b33ea959` is the current follow-up baseline. These are later hosted/Git facts, distinct from the preceding local QA chronology. The current user request delegates this follow-up to the doc-writer under the supervisor, scoped to this SPEC-0100 package, REQ-0004, its stage README and the directly duplicated AD-0007 text (six current documents total). HEAD/base is merge `3d2ad806`; independent semantic review approved the six-document correction. The earlier affected quick passed 6/6 gates on pre-final wording and is not evidence for the final bytes. The revised frozen six-document snapshot passed `rtk proxy python3 -u scripts/qa.py full --root .`: exit 0, 1,228 paths, all 22 gates PASS, including discovered unit tests and pre-commit, with no selected-gate SKIP, FAIL or DEFER. Python 3.12.3, pre-commit 4.6.1, Git 2.43.0 and RTK 0.49.0 were used; the full output is in tool session 21484, with no persistent log artifact. `rtk git diff --check` and `rtk git diff --cached --check` also passed; the index was empty. This Task-only evidence edit follows that full snapshot. Its first quick refresh exited 1 before any gate ran because source files changed while the snapshot was being created; the reviewer corrections were completed and the final Task bytes frozen for a focused document/pre-commit retry. That failed attempt is not a gate result. The published `draft`/`draft`/`queued` states remain legal initial states; no `completed` transition or Archive disposition is inferred from publication. This follow-up rechecks V25/V28/V37 and REQ-0004 obligations against current implementation under WP-006. The resulting dispositions are recorded below; no new validator or lifecycle transition follows from an unproved proposal.

A bounded disposable-repository audit ran seven named Archive reappraisal, disposition, catalog and recovery `unittest` cases: 7/7 PASS in 2.979 seconds. Its first combined child still returned FAIL because the CRLF probe did not rematerialize the checkout; that failure is not a suite PASS. In the V28 probe, removing then restoring an assessment between commits, and changing `invalidated` to `usable` with the same structural Decision, each returned no diagnostics. Those are observed limits, not approved transitions or a genuine-approval proof. A corrected V37 probe deleted and rechecked out a catalog record under `text eol=crlf`, observed CRLF bytes and no catalog diagnostics, then completed with cleanup; this proves that one object/index case, not custom filters or the full checkout pipeline.

### Ordered QA and repair evidence

| Attempt / scope | Result | Practical limit and disposition |
| --- | --- | --- |
| First canonical quick, 17 affected paths | FAIL exit 1; 12 of 13 gates PASS, links/owners FAIL on four reciprocal links | REQ-0003 backlink added; exact original failure preserved |
| Corrected canonical quick, 18 changed paths | PASS exit 0; all 13 selected gates PASS | Includes final ancestor guard and preceding Task evidence; later Task-only edits require focused recheck |
| Isolated repaired document recheck, 17 paths | PASS exit 0 for links/owners and Markdown profiles | Repairs the link finding; no claim of a second 13-gate quick |
| First full, 1,227 discovered paths | Interrupted exit 130: 18 PASS, Archive cutover FAIL, unit tests in progress, two gates not run | Not a full PASS; interrupt occurred during bounded runner work |
| Required tool preparation | Gitleaks 8.30.0 installed in user-local executable path and accepted by trusted resolver; existing pre-commit 4.6.1 venv kept with a regular-file entrypoint and non-group/other-writable permissions | Explicitly authorized local tool readiness, not a repository rule change or secret scan result |
| Focused prerequisite gate repair | Archive cutover PASS and agent evaluation cases PASS; pre-commit first FAIL because detect-secrets updated baseline metadata and Ruff formatting touched tests | No gate was weakened; exact formatter and metadata proposals reviewed |
| Formatter correction | Two Archive test modules formatted; before/after Python AST identical; focused two-module suite PASS, 60 tests in 25.183 seconds | Formatting only; aggregate unit result reported below |
| Detect-secrets baseline correction | Existing nine findings remain nine with unchanged detection values; seven old research line numbers (m0012 four, m0007 three) plus `generated_at` corrected | Metadata-only `.secrets.baseline` change; no research body or secret value changed |
| Unit repair diagnostic | One legacy Registry fixture initially errored because Assessment was absent; helper now fails closed for a missing current catalog contract. Lifecycle 54 tests PASS in 22.5 seconds, history six PASS in 4.4 seconds, format/diff PASS | Repaired fixture compatibility, not a new Assessment default |
| Repository Archive performance fixture | FAIL at 268 > 267 in both baseline isolated clone (11.693 seconds) and current QA snapshot (12.743 seconds) | New ancestor helper is outside this fixture's call path; budget not relaxed; baseline failure reproduced |
| Four affected full-profile gates, 1,227 paths | PASS exit 0 for Archive cutover, document lifecycle, secret handling and pre-commit after baseline/formatter repair | Run before final ancestor guard; later targeted history gates check that delta |
| Final ancestor-guard review and focused delta | Reviewer raised one medium concern: current catalog plus registry contract could disappear together. Guard now inspects target-reachable history even if Assessment is absent; real-commit negative and legacy positive fixtures PASS, lifecycle 54 PASS, Archive two modules 62 PASS, format/diff PASS. Reviewer found no further issue. | Final two history gates, Archive cutover and document lifecycle, PASS exit 0 over 1,227 paths after guard repair |
| Final whole-unit rerun on pre-final-guard isolated snapshot | FAIL exit 1: 1,223 tests in 1,073.248 seconds, three failures, zero errors and four skips | Followed by final-guard focused lifecycle 54 PASS, Archive two modules 62 PASS, and two full-scope history gates PASS; this older failure is preserved |
| Approved state migration, focused verification | 87 state-contract tests PASS; Ruff PASS; 11 focused initial-QA repair checks PASS | Current Registry and historical generation boundaries checked; 11 live `completed`, 492 frozen `done` values preserved; independent review no finding |
| Approved migration quick, 45 affected paths | PASS exit 0; 13 of 13 gates PASS | Checked before two later test-only fixture corrections; final full covers those final source bytes |
| First approved full, 1,228 discovered paths | FAIL exit 1; 21 of 22 gates PASS; unit suite 1,232 tests in 1,011.066 seconds, one failure and four skips | `test_terminal_document_is_not_checked` still used obsolete live `done`; corrected the fixture to `completed`, then its module passed 27 tests |
| Second approved full, 1,228 discovered paths | FAIL exit 1; 21 of 22 gates PASS; unit suite 1,232 tests in 1,021.302 seconds, one failure and four skips | `test_equal_size_same_inode_content_restore_fails_closed` exposed a timestamp-collision test race; fixture now sets an observable mtime with `os.utime`; focused class passed 36 tests, without changing production semantics |
| Final canonical full, 1,228 discovered paths | PASS exit 0; all 22 gates PASS, including pre-commit and agent evaluation; unit suite 1,232 tests in 1,021.720 seconds, OK with four skips | `python3 scripts/qa.py full --root . --base-ref HEAD` over the final code/document bytes before this Task-only evidence edit; post-Task focused refresh belongs to the supervisor |

The older interrupted and failed attempts above remain failures at their recorded snapshots. The final reviewer found no remaining actionable finding, and the approved migration received a separate independent review with no finding. The last canonical full QA passed all 22 gates on the 1,228-path working-tree snapshot. That original Task-only evidence update followed the QA snapshot; its affected document checks required separate refresh. At that point, the original checkout and worktree index were untouched; no commit, push, PR, merge or Archive removal was claimed. Later publication is recorded in the dated section above.

The three failing tests were `tests.test_archive_validation.ArchiveValidationTest.test_repository_archive_git_snapshot_is_bounded_and_under_sixty_seconds` (268 Git calls versus budget 267), `tests.test_run_validation_lane.BoundedValidationCommandTest.test_escaped_descendant_is_failed_without_post_reap_group_signal` (expected `ProcessLookupError` not raised), and `tests.test_validation_bounded_io.ValidationBoundedIoTests.test_file_reader_rejects_changes_during_read` (expected `BoundedInputError` not raised). The first two failed once in an isolated `d2296de9` baseline as well as current execution. The bounded-IO test passed in that one baseline comparison but failed in current execution; the test and implementation Git blobs were unchanged then. Equal-length overwrite with unchanged metadata was initially a hypothesis; a later same-metadata reproduction confirmed the observation gap. All three initial failures were repaired and the final full unit suite passed. The Archive budget counted nine detached points-at Git calls, not eight, while retaining its 259-call branch budget and 60-second limit; the escaped-descendant test reused the existing process-reap helper without relaxing FAIL or cleanup semantics; and the bounded reader gained a same-descriptor, size-bounded second read to catch an equal-length overwrite with unchanged metadata. Focused repair checks passed 11/11. The new same-metadata security regression closes that test gap, and independent security review found no weakening. The reader cannot observe an ABA content change that leaves no difference at either read, which remains a known observability ceiling rather than an atomic-read claim. The runner did not preserve the identities or reasons for four skips, so they are not inferred or relabeled. A separate equivalent isolated-clone probe skipped four linked-worktree hook tests because the clone had no linked worktree; the canonical log itself records only the skip count. No separate shared-worktree mutation was used to investigate them.

### Common proposal binding (S01–S16)

| Standard | Current owner and disposition for this run | Verification or decision boundary |
| --- | --- | --- |
| S01 | `.agents` policy and Stage 99 registry retain separate semantic/machine authority | Registry/profile review; no second authority |
| S02 | User approved current Spec/Plan/Task `done`→`completed` spelling on 2026-09-28; 11 live instances and current consumers migrated, 492 frozen values preserved | Same terminal meaning; 87 focused state tests and final full QA PASS; no new disposition authority |
| S03 | ADR-0040 owns four retention and two route dispositions | Existing Archive lifecycle regression |
| S04 | ADR-0040 owns terminal unit, approval wait and no new execution | Policy wording correction and unit tests |
| S05 | Archive index Assessment and registry own judgment, availability and Hold | Reappraisal regression |
| S06 | Catalog envelope and default-branch source reachability remain accepted | Git object/reachability fixture; incomplete history fails |
| S07 | Sealed capture rows remain immutable; current assessment is separate | Frozen diff and catalog gate |
| S08 | Registry ordered citation decision governs all callers | Citation regression including Incident exception priority |
| S09 | Existing validation of conditional evidence is retained; proposed new fields are not adopted | No demonstrated need for schema expansion |
| S10 | Current READMEs guide navigation through existing owners | Wiki-curator current-link review |
| S11 | REQ-0003/AD-0006/ADR-0040 retain durable meaning; SPEC-0100 owns execution | Source trace and no duplicate package |
| S12 | Incident `closed` remains legal; form Current state derives from frontmatter; proposed `resolved`→`closed` mapping is not adopted | Template/profile check; distinct lifecycle meanings preserved |
| S13 | Existing registry language contract retained | Applicable language gate |
| S14 | Existing validation registry and quality policy select/check lanes | Quick/full results and exact limitations |
| S15 | Frozen and sealed generations remain byte-for-byte | Git diff and Archive cutover |
| S16 | Common 3.0.0 is assessed per criterion, with deferrals owned here | This binding, V matrix and decision proposal |

S02's approved spelling change is implemented and verified; any new S09 state/field semantics are **not adopted**. S01/S03–S08/S10–S15 are existing local contracts or scoped conformance work, not fresh acceptance of the whole external proposal. The existing `0002-archive-retention-and-provenance` research pack owns external-source findings; SPEC-0099 is workspace-engineering research and SPEC-0095–0098 do not grant this task provider or state-migration authority.

### Regression scenario disposition

The V01–V40 matrix below distinguishes inspected test existence from executed results. V25 approval authenticity is a human review obligation under ADR-0040, not an automation gap; existing path/profile checks remain. Existing V28 endpoint/ancestor row-loss and history-only transition checks and V37 object/index checks remain in force. Transient deletion and restoration between checked commits is unproved; ADR-0040’s no-row-loss obligation remains. The observed CRLF checkout probe passed, while other filter/encoding variants remain untested. The V27 bounded repair uses a target-reachable ancestor (including merge ancestry), excludes unrelated branches and preserves valid approved `git-history-only` removals. It neither restores old payloads nor edits frozen rows.

### V01–V40 test binding at the observed baseline

The QA investigator classified test existence at `d2296de9` on 2026-09-28. `covered` means a named regression exists, `partial` means its requested variant is unproved, and `gap` means no dedicated regression was found. The bounded `archive-contract-tests` gate ran PASS (exit 0) over six modules at the baseline; tests named outside it were initially inspected and later executed by the final full unit suite where discovered. The new V12/V27 fixture ran RED on the old implementation (`test_prior_commit_cannot_erase_unit_and_catalog_together`, observed empty diagnostics), then GREEN within six focused tests after repair. Final canonical full QA has since passed, as recorded above.

| ID | Applicability / current coverage | Existing or needed check and result limit |
| --- | --- | --- |
| V01 | covered | `test_document_strict_cutover`, `test_archive_registry_contract`; inspected |
| V02 | partial | `test_package_with_an_open_task_is_not_retained`; issued Task inventory remains to review |
| V03 | partial | `test_completed_package_may_retain_a_cancelled_task`; cancellation authority fixture not found |
| V04 | partial | `test_package_with_an_open_task_is_not_retained`; approval wait and no new execution need review |
| V05 | covered | `test_package_cannot_drop_a_member`, `test_resolved_bundle_needs_its_postmortem`, `test_partial_removal_is_not_admitted`; archive gate PASS |
| V06 | partial | `test_document_strict_cutover`, `test_json_schema_validation`; closure timestamp variants unproved |
| V07 | partial | `test_resolved_bundle_needs_a_published_postmortem`; corrective owner semantics need review |
| V08 | covered | `test_archive_catalog_reverification` tree/blob/mode and `test_archive_dispositions` envelope; archive gate PASS |
| V09 | covered | `test_archive_disposition_lifecycle` member bytes/membership/mode and symlink fixture; archive gate PASS |
| V10 | covered | `test_archive_reappraisal` row and frozen-unit fixtures; archive gate PASS |
| V11 | partial | whole/hold/partial removal fixtures; actual decision authority remains a human review obligation |
| V12 | repaired, focused PASS | `test_prior_commit_cannot_erase_unit_and_catalog_together` RED on baseline, then GREEN within six focused tests |
| V13 | covered | `test_withdrawn_invalidated_and_removed_units_are_not_cited`, `test_archive_citation_decision`; archive gate PASS |
| V14 | partial | `test_archive_historical_proof`, `test_documentation_link_boundary`; removed payload links need review |
| V15 | partial | rendered CommonMark historical link fixture exists; encoding/HTML/wiki variants unproved |
| V16 | partial | tombstone identity and disposition route fixtures; quoted-frontmatter move unproved |
| V17 | partial | `test_a_form_enforces_only_statuses_its_source_admits`; proposed new conditional meaning not adopted |
| V18 | covered | `test_readme_navigation` and common agents/archive router fixtures; inspected |
| V19 | covered | `test_qa_runner` required tool and `test_validation_profiles`; inspected |
| V20 | covered | `test_ci_qa_workflow` aggregate and `test_validation_profiles`; hosted run not observed |
| V21 | partial | formatter mutation fixture; generator idempotency unproved |
| V22 | partial | lifecycle graph and historical proof fixtures; semantic successor requires review |
| V23 | covered | quality lane policy and validation profile test; live evidence DEFER |
| V24 | covered | frozen body and existing archive mutation fixtures; archive gate PASS |
| V25 | existing contract; automation proposal declined | `assessment_diagnostics` checks current Decision path/profile; ADR-0040 assigns genuine approval to human review, so no validator can claim to prove authority or timing |
| V26 | covered | final tree/index distinction and index-deleted Task fixtures; inspected |
| V27 | repaired, focused PASS | Same ancestor-loss RED as V12; six focused tests and archive gate PASS after repair |
| V28 | partial; transient edge unproved | Existing endpoint/ancestor row-loss and `git-history-only` reversal checks remain. A delete/restore between checked commits is not detected by those checks; ADR-0040’s no-row-loss obligation remains. No new graph validator is adopted in this follow-up |
| V29 | partial | removed-unit citation fixture and catalog link exception; generated site links unproved |
| V30 | partial | deep citation and code-span README fixtures; catalog exception review pending |
| V31 | covered | `test_document_language` profile/terminal/English fixtures; inspected |
| V32 | partial | Registry/template fixture exists; necessity of each form needs owner review |
| V33 | partial | QA snapshot fixture exists; automated ID/date issuance absent here |
| V34 | covered | bounded inventory and reader fixtures; inspected |
| V35 | covered | off-default, shallow and unreachable commit fixtures; archive gate PASS |
| V36 | partial | terminal index and root README routing fixtures; historical command drift review pending |
| V37 | Git object/index checks present; extra engine proposal declined | Git object/index checks remain; a disposable CRLF checkout catalog probe passed. Custom filters, encoding variants and the full checkout pipeline were not exercised |
| V38 | partial | form status-domain tests exist; Incident template now points to frontmatter |
| V39 | partial | frozen payload immutability exists; original Commit Ledger item fixture unconfirmed |
| V40 | partial | stale-owner and terminal progress fixtures exist; current obligation review pending |

The focused V12/V27 suite and bounded Archive gate passed. V25 keeps path/profile checks and human approval review; approval-authenticity automation is not a backlog item. Existing V28 endpoint/ancestor behavior remains checked; transient deletion/restoration is an unproved observation limit under ADR-0040’s no-row-loss obligation. This follow-up does not add a graph validator. V37 keeps Git object/index verification, with CRLF checkout probed and other filter/encoding variants untested; a new attributes engine is not adopted. REQ-0004-FR-0008 and FR-0010 remain open after SPEC-0049 withdrawal. Observed residuals include render/schema, per-target evidence and ingress cross-reference/resource-kind coverage; existing structure, YAML, policy, secret, Vault/ESO, manifest image-version and product checks remain implemented; image provenance is not established by the version check. The request owner should scope a concrete residual before assigning work. SPEC-0100 does not close those requirements. The approved Spec/Plan/Task `completed` spelling satisfies VAL-ARC-006. Incident `resolved`→`closed` mapping and new conditional metadata are not adopted without a demonstrated need.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Policy/registry/caller map and catalog inventory reviewed; final full QA PASS | [VAL-ARC-001](../spec.md#success-criteria--verification-plan), VAL-ARC-003 |
| [WORK-002](../plan.md#work-breakdown) | Focused RED/GREEN and final guard regression PASS; independent review has no remaining finding | [VAL-ARC-001](../spec.md#success-criteria--verification-plan), VAL-ARC-003 |
| [WORK-003](../plan.md#work-breakdown) | Current documents authored; links/profiles and final quick/full PASS; Task-only refresh handled at handoff | [VAL-ARC-002](../spec.md#success-criteria--verification-plan) |
| [WORK-004](../plan.md#work-breakdown) | User-approved spelling migration complete; 11 live frontmatter values and all consumers aligned, 492 frozen values preserved; 87 focused state tests and full QA PASS | [VAL-ARC-004](../spec.md#success-criteria--verification-plan), VAL-ARC-006 |
| [WORK-005](../plan.md#work-breakdown) | Prior failures preserved; original quick 13/13 PASS and full 22/22 PASS with 1,232 tests (four skipped); publication followed in PR #108; current follow-up semantic review approved and full QA 22/22 PASS before Task-only refresh | [VAL-ARC-005](../spec.md#success-criteria--verification-plan) |
