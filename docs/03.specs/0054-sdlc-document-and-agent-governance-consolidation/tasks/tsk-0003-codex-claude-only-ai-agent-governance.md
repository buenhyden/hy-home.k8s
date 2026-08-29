---
title: 'Task: Codex Claude-only AI agent governance'
type: sdlc/task
status: in-progress
owner: platform
updated: 2026-08-29
artifact_id: "TSK-0054-0003"
---

# Task: Codex Claude-only AI agent governance

## Overview

This is the single current execution Task. WP-004 completed through `bb55a1ae`;
WP-003 retains its approved two logical units and unchanged WP identity. The
2026-08-29 approval closes the two historical-reference decision holds; their
bounded implementation and actual-index verification are now in progress.

## Inputs

- [Common execution contract](../README.md#common-execution-contract)
- [Spec 0054](../spec.md)
- [Plan 0054](../plan.md)
- [WP-003 execution boundary](../plan.md#wp-003--codexclaude-only-ai-agent-governance)

## Task Table

**Plan label:** WP-003

**Depends on:** WP-004

**Current state:** `in-progress`

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-054-003 | VAL-SDLC-005, VAL-SDLC-011, VAL-SDLC-012 | Create the `.agents` authority, converge Stage 00 on Codex/Claude-only support, and remove Gemini/Antigravity. | platform | In Progress | Reviewed WP-003A candidate is staged; the two approved historical-reference extensions and current-data corrections are in progress. WP-003B remains unstarted. | Source reviews approved; initial actual-index failures remain recorded below; correction, regression review and publication checks are still required |

## Approval and Safety Boundaries

The [common execution contract](../README.md#common-execution-contract) applies
without exception. WP-003's Codex/Claude-only scope, live/provider mutation
boundary, reviews, rollback, and two ordered commits are owned by its linked
Plan section.

## Verification Summary

- WP-004 is complete; no other WP was activated between WP-004 and WP-003.
- The second core fix round passed 88 focused tests and the registry,
  provider-evidence, and semantic production entrypoints. The latest aggregate
  agent run on 2026-08-28 passed 216 tests in 27.950 seconds on the frozen
  historical-fix source. This is a final-byte agent regression result, not an
  index-synchronized publication result; the ordered completion checks remain.
- Independent code, Python, and security re-reviews approve the second core
  fix round with no remaining Critical/Important findings. Reserved declarations
  are unambiguous; schema errors are redacted and external resolution is blocked.
  Mocked transport probes confirm no HTTP/URL/socket/DNS calls. This closes the
  core slice only, not the remaining integration work.
- Stage 00 document consolidation, finite current-link repair, and in-place
  ADR-0013 supersession by ADR-0030 passed focused Markdown/link checks and
  independent review after the README authority residue was removed.
  Completed Spec/Plan bodies remain unchanged.
- CI owner routing now reuses the canonical rendered-link parser. The fix
  passed 37 focused tests, both CLI modes, lint/format/compile and diff checks;
  independent code, Python and security re-reviews approve the slice. Malformed
  Markdown and image examples cannot fabricate owner links; valid reference
  links remain supported.
- Generic recovery's first correction round passed 23 focused recovery and
  retained corruption tests. Review confirms the four original defects are
  resolved: composed move parity, successor-record CLI verification, duplicated
  Stage99 format policy, and blocking FIFO reads. Python/security re-review
  found two additional boundaries, now corrected: malformed action types and
  external schema lookup/resolution errors in the canonical document owner.
  The shared offline helper passed 47 recovery/agent and 39 focused document
  tests. The isolated compatibility loader fix passed five tests and all six
  module orders; code, Python and security reviews are closed for this slice.
  Snapshot-bound Migration lifecycle implementation has handed off for
  independent code, Python and security review: 18 new lifecycle, 19 recovery,
  40 document-contract and eight retained lifecycle tests passed. Controller
  and code reviewer reruns of all 18 lifecycle tests passed after the final
  typed recovery-error correction; code/spec and Python reviews approve.
  Security review found an additional unbounded proposed-registry regex
  evaluation. Its precompile literal-policy correction passed 22 lifecycle,
  19 recovery and 40 strict document tests; code/spec, Python and security
  re-reviews approve. The original public attack now rejects promptly.
  No index-dependent or full Archive result is claimed as passing.
- The retained memory router is not a deleted Migration source. Its extracted
  context policy will first be published as `draft` in WP-003A and activated
  through `draft → active` in WP-003B, with current-owner navigation updated
  at each step. Existing execution and checkpoint/loop safeguards remain.
  Cumulative CI/ref lifecycle comparison still needs separate verification;
  per-commit staged results do not prove that comparison mode. Direct user
  approval on 2026-08-28 authorizes bounded actual-history proof for cumulative
  creation in WP-003B, preserving draft-first and the supplied comparison base
  without a fixed SHA list, path waiver or new gate. It remains second-unit
  work, not part of WP-003A publication or current completion evidence.
- The finite current-reference/generator unit passed 10 generator tests,
  two historical tests, 11 document-profile checks and 229 local-link checks;
  independent code, Python, security and human-document reviews approve the
  slice. The latest combined historical-proof and RIA suite ran 120 tests:
  116 passed and four real-worktree production checks failed before index
  synchronization. Their assertions remain enabled for publication validation.
  Existing transition object identities and dated
  evidence remain unchanged; no current-tree historical-input waiver is claimed.
- The live aggregate consumer repair has completed independent review.
  It removes obsolete catalog/provider/memory snapshots and fixed script counts
  while preserving unique Claude registration, hook behavior and current
  canonical owners. Focused suites and actual branch-policy/PR parity probes
  passed; code/spec, Python and security reviews approve this five-file unit.
  The closure/legacy integration preserves
  actual instruction consumers and verified historical projections while
  removing duplicate control snapshots and occurrence-count rules.
  The closure compatibility slice passed 22 focused tests and both production
  modes. Independent code, Python and security reviews approve after a generic
  exception-message leak was fixed in closure and four sibling compatibility
  CLIs; real malformed-input regressions cover both modes and preserve normal
  typed diagnostics. The affected-owner fixed sibling import also passed seven
  focused tests, repository-root and isolated `-I` loading, and all three reviews.
  The final historical-proof/legacy slice passed 44 tests and the generic
  recovery suite passed 19 tests. Its real-root composition is not proved by
  the temporary Git fixtures.
  Review identified two Important corrections: preserve the legacy held-read
  boundary across shared context loading, and reuse RIA's canonical protected
  commit for audit-settled retired packs. Both corrections are implemented in
  five existing owners and four existing test files. Original-plus-fix Spec
  review passed 13 focused tests in 41.294 seconds, followed by code-quality
  approval. Python and static security review identified a fixture import-path
  leak and RIA's remaining default schema resolver. A second correction reused
  the existing offline evaluator and scoped import restoration in three files.
  Its 11 focused, four historical and five existing helper checks passed;
  independent Spec, code-quality, Python and static security re-reviews approve.
  Static security review makes no runtime/probe claim. The held-input API
  preserves canonical validation,
  default callers, existing bounds and index parity; it adds no global IO layer
  or new authority. The former finding remains static, with no dynamic
  reproduction claimed. Initial RED covered five missing-contract failures;
  focused GREEN runs passed seven, four and four tests. The broader run passed
  184 of 188 tests, with the same four actual-root RIA failures. Two later test
  additions were executed in the final focused run, not as a claimed 190-test
  full pass. Separate lifecycle/strict/recovery checks passed 92 of 93 tests;
  the remaining MIG4 failure is an unchanged current-target index/worktree
  mismatch. Another 30 compatibility/lifecycle tests passed on frozen bytes.
  Both legacy CLI modes still fail on the unindexed new registry, and the public
  historical adapter still stops on removed-but-indexed projections. Reviewed
  index synchronization and real-root reruns remain required.
  Six retiring closure/legacy contract and fixture sources are recorded in
  MIG-0005 with verified Git blob and content identities. Published instructions
  remain scanned; enforcement and negative-test artifacts are classified by
  existing owner contracts, not current-byte pins or filename suffixes.
  Current helper follow-through passed 17 focused tests and 28 self-test cases;
  the controller reran all 17 focused tests on the final shared-proof bytes,
  passing in 93.378 seconds. This does not replace the actual-root checks.
  Independent code/spec, Python and static security reviews approve the
  five-file role/README/route-consumer slice. Historical frozen
  membership remains unchanged, while missing retired fixtures require generic
  Migration source/successor proof. At that review boundary, README entries
  matched the 64 live helper files; this is historical evidence, not a fixed
  count rule. Actual-root role-audit setup and CLI still fail on the
  unsynchronized index.
  Two additional script README descriptions were corrected to remove obsolete
  live counts and retired fixture lists; strict Markdown and independent
  docs-only review passed.
  WP-003B must transfer the remaining unique registration checks before
  reducing the aggregate to its three canonical agent gates.
  MIG-0005 publication, broad validation and both planned commits remain open.
  No provider-runtime or external action is claimed.
- Exact raw-NUL selection preflight over 247 changed paths found fourteen
  removed provider paths without a current surface after Gemini routes were
  correctly retired. This is a selector failure, not an executed affected-lane
  result. The bounded correction reuses complete generic Migration proof only
  for absent unmatched paths and classifies their current terminal targets.
  Existing merged/deleted dispositions supply those targets; no provider route,
  old comparison base, manual map, SHA list or gate is restored. Pure current
  classification and legacy held-owner lookup remain unchanged. The final
  eight-file implementation passed 21 focused tests in 101.112 seconds, 21
  existing runner tests, 17 current/frozen helper tests, and 28 role self-test
  cases. Ruff, compile, both README profiles and current inventory parity
  passed. Independent Spec and code-quality reviews approve, with nine and
  29 additional checks passing; static security review approves without a
  runtime claim. Independent Python review also approves, with 21 focused tests
  in 100.550 seconds, 21 existing runner tests and isolated import checks passing.
  A fresh raw-NUL set contains 250 changed paths, including 29 untracked files;
  the three added paths are the runner, its tests, and the new selection test.
  The actual affected runner was executed over that set and failed before
  selection completion with `SURFACE-MIGRATION-PROOF`. The affected self-test
  also fails before index synchronization. Neither result is waived or counted
  as passing; reviewed index synchronization and both reruns remain required.
- Direct user approval on 2026-08-28 closes the recovery-boundary hold:
  MIG-0005 may interpret links for exact-source historical consumers, and
  immutable Migration recovery is separate from current-template validation.
  Execution has resumed. Terminal bodies and the existing MIG-0004 seal
  remain unchanged; no blanket lifecycle waiver is authorized.

### Actual-index integration and approved correction

The reviewed 250-path candidate was staged after an explicit permission grant
for the isolated worktree index. Raw cached NUL paths exactly matched the
reviewed affected set; cached whitespace and worktree/index parity passed.
The affected surface self-test then passed. The actual affected runner selected
all 250 paths but failed at legacy-cutover, links-and-owners and the aggregate;
the aggregate stops at the same strict-link failure. Other selected commands
passed. These are local repository-static results, not hosted or provider proof.

Direct strict-link validation found a Stage 00 README table-format mismatch,
five missing exact-source historical Plan consumers in MIG-0005, a stale
Spec 0054 execution-Task projection, four historical links to removed symlink
views, and an old authoring-policy link in Archive README. Direct staged
lifecycle validation also requires ADR-0013's successor link in its canonical
Traceability section; an Overview link and frontmatter ID alone do not satisfy
the existing reciprocal relationship check. Those current routing/data repairs
do not require restoring old owners or weakening their validators.

The user explicitly approved both interpretation boundaries on 2026-08-29:

1. PLAN-0009 is byte-identical to its Git source, but its retired harness-map
   path occurs only in a fenced command. Existing historical consumer admission
   deliberately requires a rendered retired-path disposition. Merely adding
   this Plan to MIG-0005 cannot admit it. A bounded literal-reference extension
   must retain exact-source identity and the proved Migration successor chain;
   neither `done` status nor a code fence is a general waiver.
2. The four removed provider symlink views are human evidence in MIG-0005,
   not regular recovery payloads. Historical link interpretation would need
   separate typed source-mode/blob/link-target and consumer proof plus an
   explicit Archive lookup owner. It must not restore symlinks, relax regular
   recovery's symlink rejection, or introduce a fixed alias list.

The new approval is recorded in Spec C-SDLC-009 and the existing WP-003 Plan;
execution resumes without changing WP numbers or the two-commit sequence.
The earlier rendered-link-only hold remains historical evidence, not an open
approval request. New source-backed types must pass focused RED/GREEN tests
and independent review before the affected and exact-index checks are rerun.
MIG-0004, historical progress, the six completed Plan bodies and the protected
Audit body remain unchanged. The index retains the reviewed candidate; this
Task's subsequent handoff update is intentionally unstaged. Staged runner,
plain/all-files pre-commit, complete direct suites and commit checks have not
completed. No commit, WP-003B activation or external action occurred.

### Historical-reference correction verification

The five current routing/data repairs and the MIG-0005/template evidence
update passed independent Spec and document-quality review. The reference
implementation preserves regular recovery separately from consumer-scoped
literal and removed-view interpretation. Spec re-review required three bounded
corrections, including complete token boundaries outside matching quotes;
Python review then removed an unintended one-consumer-per-view restriction.
Identical complete view identities may be shared, while conflicting identities,
duplicate consumer/path pairs and missing occurrences still fail. The controller
reran that view regression with its independent subcases: one test passed in
6.965 seconds. Final Spec, code-quality, Python and static security reviews
approve this slice. The controller also reran the final whole-token,
literal-positive, unregistered-token and regular-symlink rejection tests:
four passed in 29.693 seconds with a captured exit status of zero.

Intermediate test invocations without a captured completion remain
UNCONFIRMED, not PASS. The mocked adapter test proves typed-map forwarding,
not the full generic-to-public path. Real index integration and full direct
suites still have to prove the combined source and Migration data. Ruff 0.15.12
check, format check and Python compilation passed; static security review does
not claim runtime evidence.
The current 250-path raw-NUL scope is unchanged; the index has not yet been
updated with this correction. No historical body, sealed record or main
worktree content changed.

The subsequent index synchronization completed with exact 250-path parity and
no unstaged residue. The actual affected lane then passed all selected owners
except legacy-cutover and the aggregate, which reports the same legacy failure.
Full direct strict-link validation passed. The first remaining legacy consumer
at that checkpoint was unchanged Plan0010. ADR0030's existing reverse relation
was subsequently moved into its canonical Lifecycle Traceability table; after
independent review and exact staging, direct staged lifecycle passed with exit
zero. No first-unit commit or second-unit activation occurred.

The subsequent finite inventory identified four additional unchanged Plans
whose supported literal occurrences can use the approved proof, three Specs
with unsupported inline forms, current Audit/ledger references, original
Archive payloads, and generated graph data. The partial MIG-0005/Audit repair
preserves the four Plans and verified source mappings while deferring those
three Spec admissions. The Audit now distinguishes its observation-commit
evidence from current Migration lookup. No completed body was rewritten.
Independent Spec and quality/architecture reviews approve the two-file
correction; strict Markdown profiles and scoped whitespace checks passed.

The Archive payload bridge reuses the existing record validator and binds
stable records to their MIG-0001 historical envelopes over held bytes. It
excludes only proved payload bytes and continues scanning the header. The
initial five-test run was pre-review evidence. Spec review required candidates
to come from validated profile/path/tracked membership and required proof for
ordinary canonical mirrors, with the additional historical identity binding
limited to MIG-0001 stable paths. These corrections and independent source
identity regressions are implemented; Spec re-review approves. The controller
reran all seven final focused tests in 43.187 seconds with exit zero. Ruff
check/format and Python compilation also passed. Independent general quality,
Python and static security reviews approve the frozen four-file delta. Three
retained public-proof regressions passed in 21.365 seconds; an earlier command
used a nonexistent test method and exited one, so only the corrected run is
the three-test PASS evidence. Actual-index integration remains pending.

Raw-NUL inspection now identifies 251 affected paths, 250 staged paths, seven
unstaged paths and no untracked files. WGIA is the one newly affected path;
the new delta comprises the four Archive source/test files, MIG-0005, WGIA and
this Task. These counts describe the checkpoint, not a fixed corpus rule.

The reviewed seven-path delta was then staged with exact 251-path raw-NUL
scope parity, no unstaged source residue, and a clean cached whitespace check.
On that synchronized index, full strict cross-document validation, MIG-0005
recovery verification and direct staged lifecycle each passed with exit zero.
The normal legacy CLI still exits one at Spec0014's unresolved inline form.
That is the first reported consumer, not a claim that all other consumers are
closed. The broad affected/staged runners, pre-commit and final aggregate have
not been rerun over this new checkpoint. This subsequent evidence-only Task
update is intentionally unstaged; it does not claim final index publication.

### Approved remaining interpretation boundaries

- Spec0014, Spec0022 and Spec0045 contain five comma-adjacent inline path
  forms outside the recorded fenced-command/whole-token boundary. They have
  no independent rendered historical disposition. Their new admission is
  deferred; neither the grammar nor the approval record is silently widened.
- The WER 14-column table is historical inventory, including migration-time
  destination cells. Candidate row rewrites were rolled back to the index.
  Its stated original source does not reproduce the entire later table, which
  includes subsequent projections and RIA evidence. Neither a historical-table
  waiver nor removal of that later evidence is authorized by the existing
  completed-whole-consumer interpretation.
- Tracked graph outputs retain optional Claude/knowledge-map consumers and
  lack a repository-owned deterministic producer check. Git recovery and
  producer reproducibility are distinct. Advancing necessary graph cleanup
  from WP-012 has been put to the user; no answer or cleanup is claimed.

The user subsequently approved all three proposed changes on 2026-08-29:
closed quoted paths followed by a comma and whitespace/EOF; retirement of the
duplicated WER table and its obsolete shape obligation with latest full-content
Git recovery; and retirement of the four graphify outputs after consumer-zero
and Git recovery, advanced only to this WP. Spec C-SDLC-009 and this WP's Plan
now carry these limits. The preceding holds are historical checkpoint facts,
not outstanding approval requests. No new WP, general waiver, external
generator run or early historical-progress removal is authorized.

The first logical commit remains pending implementation and its required
checks. Full suites, staged/plain/all-files pre-commit and final aggregate
are not inferred from focused tests. WP-003B and later WPs remain unactivated.

### Approved retirement implementation

The quoted-comma correction now retains exact source/disposition proof and
rejects unsupported token boundaries. Its focused real-Git tests passed;
the added integration test exercises generic proof, historical adapter and
legacy scanning without a rendered link. Removing the declaration or changing
the consumer bytes fails at the public proof boundary. Final focused three
tests passed in 36.339 seconds; independent Spec/code-quality and Python
review approve the final slice.

The WER terminal parser obligation is removed after the existing protection
and missing-ledger checks, and the redundant later terminal branch is gone.
The actual remaining history table is not parsed as a substitute inventory.
Review identified a false-positive byte-drift negative; the corrected test
first proves a valid settlement, then independently rejects metadata and byte
changes while isolating only unrelated path projection. Final focused seven
tests passed in 0.585 seconds; Spec/code-quality and Python re-review approve.

The WER first inventory table has been removed with a manual MIG-0005 recovery
note, preserving its current path and other tables. A bounded source check
proved the latest full WER and all four graph outputs at the recorded commit.
The controller separately compared the unchanged prefix and retained-table
suffix against the index: both match exactly. The first comparison failed at
a sandboxed child-Git invocation before assertions; the approved read-only
retry passed. This proves body preservation, not generic certification of the
manual partial-content note.

All four approved graph files are deleted. Their current Claude hook,
navigation, ignore exceptions and classification routes are removed; the
privacy ignore file, non-graph hooks/permissions, RTK/.rtk boundaries and
historical WORK105 observations remain. Config/navigation Spec/code-quality
and static-security reviews approve. Graph QA focused tests passed 56 cases in
112.144 seconds; its actual affected-surface fixture self-test still failed
with `SURFACE-MIGRATION-PROOF` against the unsynchronized index. This failure
must be rerun, not waived. Final document wording and graph QA re-review now
approve the frozen changes. Strict Markdown-profile validation passed for the
six changed Spec/Plan/Task, architecture and recovery documents. Index
synchronization, complete publication checks and the first commit remain
pending; no second-unit activation or external action occurred.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-054-003](../plan.md#wp-003--codexclaude-only-ai-agent-governance) | In Progress. | WP-004 dependency and both 2026-08-29 historical-reference decisions are closed. Correction, publication checks and both commits remain; no WP-003 completion evidence is claimed. |
