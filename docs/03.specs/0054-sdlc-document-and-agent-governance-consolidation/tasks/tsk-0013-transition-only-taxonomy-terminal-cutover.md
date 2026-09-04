---
title: "Task: Current corpus and transition-control cutover"
version: "1.3.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-04"
layer: "specs"
artifact_id: "SPEC-0054-TSK-0013"
---

# Task: Current corpus and transition-control cutover

## Overview

This is the queued Task record for the remaining Stage 01, 02, 03, and 99
current-corpus convergence and transition-control retirement in WP-013. Named
dispositions are execution candidates, not permanent corpus-count policy.

Re-observation on 2026-09-03 refreshed those candidates. Two entry steps now
precede the cutover: Spec 0052 closes, which releases the suspension recorded
against REQ-0007 and REQ-0008, and Spec Packages `0047` through `0051` each
receive a resume-or-remove disposition. The Stage 03 removal set is the fifty-two
packages that will be `done`. The fifty-one measured today partition into
twenty-five already consumer-zero, thirteen released by rewriting REQ-0003,
AD-0006, AD-0008, and AD-0009, and thirteen held by owners disposed of
individually, including four accepted ADRs whose citations convert rather than
disappear. Fourteen packages are retained on unfinished scope rather than on a
fixed list, two of them conditionally: `0062` holds three `blocked` Tasks, and
`0006` is an `active` Spec with no Plan and no Tasks.

## Inputs

- [Common execution contract](../plan.md#common-execution-contract)
- [Spec 0054](../spec.md)
- [Plan 0054](../plan.md)
- [WP-013 execution boundary](../plan.md#wp-013--current-corpus-and-transition-control-cutover)

## Task Table

**Plan label:** WP-013

**Depends on:** WP-006; WP-008; WP-012; accepted ADR-0031; accepted and completed Spec 0066
result with SPEC-0066-TSK-0001, Plan 0066, and Spec 0066 all `done`; completed
SPEC-0054-TSK-0011 parent handoff; and the existing Spec 0054 compatibility pointer,
which named this Task while it was still `queued`

**Current state:** `in-progress`; the entry blocker in the link validator is
released, document-contract v9 has a proposal commit, ADR-0032 and ADR-0033
have human acceptance, and the remaining WP-013 dispositions are not complete

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-054-013 | VAL-SDLC-001..VAL-SDLC-004, VAL-SDLC-006, VAL-SDLC-009..VAL-SDLC-012 | After the completed child and parent handoffs, reconcile retained Stage 01 Requirements and Stage 02 Architecture bidirectionally with the current implementation, converge the reviewed Stage 01/02/03/99 current-owner set, retain terminal governed documents under ADR-0032, remove current-authority dependencies on sealed Archive records, transfer unfinished work and unique authority, then retire residual transition assets against the accepted and completed Spec 0066 routing result without a fixed corpus census. | platform | In progress | Document-contract v9 proposed in commit `41f8144e`; ADR-0032/0033 acceptance and Plan amendment prepared; remaining WP-013 disposition is open. | Terminal Spec 0066 states, completed SPEC-0054-TSK-0011, compatibility pointer to this Task, manifest/configuration/code/validator/operational-interface evidence mapped to retained Requirement Packages and Architecture Descriptions, completed-retention provenance, zero current-authority dependencies on sealed Archive records, consumer/trace/lifecycle parity, Git exact-byte recovery, registry/template parity, delegated routing evidence, and ordered logical commits |

## Approval and Safety Boundaries

The [common execution contract](../plan.md#common-execution-contract) applies
with the explicit human-approved Git/CI/read-only runtime evidence exception
recorded below. WP-013 may disposition a current document or template only
after its unique authority and unfinished work are transferred or proven
absent, current consumers are zero, and Git exact-byte recovery succeeds.
Terminal governed documents follow ADR-0032 retention rather than deletion. The linked Plan
owns the exact candidate dispositions, reviews, rollback, and four ordered
logical commits: Stage 01/02, Stage 03, Stage 99, then transition controls. The
accepted and completed Spec 0066 result plus the completed SPEC-0054-TSK-0011
parent handoff are fixed dependencies; their execution does not overlap the
final WP-013 validation-side transition-control unit. The existing Spec 0054 compatibility pointer named this
Task while it was still `queued`, which satisfied the activation condition.
Each unit is independently validated and can stop before the next unit without
rolling back an already accepted predecessor unit.

The Stage 01/02 unit is not a prose-only consolidation. It compares retained
Requirement Packages `0001` through `0004` and Architecture Descriptions
`0004` through `0007` with current manifests, configuration, executable code,
validators, and supported operational interfaces. Unique current facts move
from removal candidates before deletion. Durable implemented behavior without
an appropriate current Requirement/Architecture owner and retained current
claims without implementation evidence are both blocking findings; raw
inventories remain direct repository evidence rather than duplicated document
authority.

## Verification Summary

No additional Stage 01, 02, 03, or 99 document has been removed in this
follow-up. One entry blocker is released, the document-contract v9 proposal is
committed, and the human acceptance/Plan-amendment boundary is now explicit.

Removing a package that a sealed migration row names as its endpoint raised
`configuration error: WORK-054 WP-004B migration target differs` and exited 2,
naming no holder. Three owners in `scripts/validate-links-and-owners.py`
required a sealed endpoint to be tracked today, and they chained: releasing
`_work054_wp004b_targets` surfaced `_work109_migration_projection`, and
releasing that surfaced `_document_taxonomy_transition_manifest`. With all
three released, the same removal reports eleven findings that each name their
holder -- seven `LINK-BROKEN` from Specs `0011` through `0023`, and
`INDEX-STALE`, `INDEX-TREE`, and `LINK-BROKEN` on `docs/03.specs/README.md`.
The intact tree still returns `PASS CROSS-DOCUMENT`.

The release is a proof rather than a waiver. Ledger coverage is now counted
from the sealed rows, so MIG-0002 still asserts its 141 rows and the transition
manifest still asserts its 82 move-current entries; a manifest target the
ledger never sealed is still rejected. Four regression cases in
`tests/test_archive_validation.py` hold each half.

Two measurements in the Plan were corrected by executing them: consumer-zero
must count terminal documents, and the first removal tier splits into twenty
MIG-0004 row targets, three named only by other ledgers, and two in no ledger.

The validator-release proof created no Archive record, redirect, or Migration
row. Future completed-package retention follows ADR-0032 and therefore requires
a reviewed sealed migration row while still forbidding redirect and body-copy
records.

### Document Contract v9 Gap Matrix

| Current state | Target state | Impact files | Migration | Validator | Test |
| --- | --- | --- | --- | --- | --- |
| Registry v8 camelCase shape plus private projection | Public v9 snake_case model with six families and six modes | Stage 99 Registry/schema; document loaders; hooks | One-shot active-corpus cutover; current readers reject v8 | document authority and strict Registry | exact top/profile key, ambiguity, orphan, trusted-pattern tests |
| Governed READMEs lacked metadata and were separately classified | Identity-free six-key README envelope, optional stage layer, no lifecycle binding | Root, provider, stage, collection, example, and implementation READMEs | Add Registry-selected envelope; never add "artifact_id: README" | strict Markdown and Registry route coverage | README prefix, forbidden identity, router null lifecycle tests |
| Template keys, dates, IDs, and placeholders differed | Ordered profile projection; Markdown and native placeholder grammars are disjoint | All registered Stage 99 forms and catalog | Replace authored-looking values with registered markers; preserve "version: 0.1.0" | template parity, residue, orphan and duplicate checks | positive generation plus invalid placeholder/date/identity cases |
| Public program and standalone instance rosters duplicated package-local ownership | Registry top-level contains profiles and lifecycle domains only | Registry/schema, typed loader, lifecycle/link tests | Remove public rosters and unused conversion path; keep only commit-bounded historical readers | schema exact-key and lifecycle comparison validation | public absence, typed empty compatibility, migration snapshot tests |
| Frontmatter schema name had unclear responsibility | Existing filename retained solely for authored scalar/array grammar | Stage 00/99 guidance and schema consumers | No path rename; document responsibility and keep profile policy in Registry | JSON Schema evaluation plus semantic validator | schema mutation and null/required boundary tests |
| README prose and templates repeated machine facts | Stage README routes people; Registry is the only machine catalog | Stage 00/01/02/03/05/90/99 README and template catalog | Remove camelCase/status/ID allocation restatements; keep human roles and workflow | Markdown sections and links/owners | strict current corpus and stale index tests |
| Release terminology could imply a missing local artifact | External-release-evidence mode remains authoritative | Stage 00 SDLC/authoring, Stage 05, ADR-0033 | Add no release profile or form; require a new ADR and consumer proof to change | profile/template absence checks | no local release profile/template assertion |
| Current formatting could rewrite historical bytes | Frozen Stage 98 payloads stay generation-specific | formatting policy, Markdown/archive readers | Exempt frozen body; validate envelope, commit/blob, digest, and links | Archive/recovery and zero-diff review | bounded historical generation and immutable payload tests |

### Migration and Reference-framework Disposition

- Common key order is "title", "version", "type", "status", "owner",
  "updated", then profile-owned structural and provenance keys. All scalar
  strings use double quotes.
- Active Markdown and registered templates move atomically to Registry v9.
  Stage 98 frozen payloads, source commits/blobs, digests, and historical links
  are byte-preserved.
- Requirement Package continues to integrate PRD, SRS, and interface
  requirement perspectives. Spec, Plan, and Task retain behavior, ordering,
  and execution-evidence ownership.
- GitHub Spec Kit is applied to the Stage 03 flow; Diátaxis to Operations reader
  intent; C4 and arc42 proportionally to Architecture Descriptions; ADR to
  successor history; Google SRE to factual incidents and blameless,
  owner-tracked postmortems. None replaces repository taxonomy.
- Release remains external evidence. No "operation/release" profile, template,
  lifecycle, path, or local record is introduced.

### Baseline and Execution Evidence

- The staged lifecycle gate rejected the attempted direct ADR-0033
  "absent -> accepted" creation. Commit `41f8144e` now establishes the required
  `proposed` state, and the user's 2026-09-04 acceptance authorizes the later
  `proposed -> accepted` transition without weakening the lifecycle contract.
- Current-main re-observation found fifteen Stage 03 packages in the active
  tree and completed packages already retained under Stage 98 by recent
  migration commits. The user's 2026-09-04 acceptance resolves ADR-0032's
  authority mismatch; Spec 0054 and Plan 0054 now distinguish retained
  `completed/` documents from sealed records and replace their older
  deletion/zero-all-links clauses.
- Initial-slice safety identity: repository root ".",
  "https://github.com/buenhyden/hy-home.k8s.git", branch "main", initial HEAD
  "24fe45af". The initial worktree was clean; that initial slice performed no fetch,
  pull, checkout, reset,
  clean, stash, commit, push, PR, tag, release, deployment, or live mutation
  was performed.
- Follow-up authority on 2026-09-04 explicitly approves local logical commits,
  branch `codex/document-contract-v9`, push and PR creation with Hosted CI, and
  secret-safe read-only checks of the configured Kubernetes, Argo CD, Vault,
  ESO, and provider runtime targets. It does not authorize secret-value reads,
  live mutation, forced reconciliation, merge, or destructive Git operations.
- During continuation, the shared checkout reflog recorded an external
  "pull --tags origin main" fast-forward at "2026-09-04 16:42:16 +0900",
  moving "main" from "24fe45af" to "1632ce28". The initial commit remains
  an ancestor of the final HEAD. This work did not execute that pull, did not
  rewind it, and ran the final staged validation against the descendant
  "1632ce28" state.
- Baseline aggregate: repository quality gates passed 22 gates over 1,014
  paths. Baseline strict Registry covered 715 paths, strict Markdown reported
  zero violations, and strict links/owners passed. Baseline pre-commit failed
  only on known detect-secrets false positives; formatter side effects on four
  unrelated Python files were reversed by applying the exact baseline diff.
- Final staged evidence: document authority passed; strict Registry covered 716
  paths with zero uncovered or ambiguous paths; strict Markdown reported zero
  violations; strict links/owners and staged lifecycle passed. Generic
  migration recovery proved 536 targets.
- Regression evidence: strict-cutover passed 53 tests, generic migration
  recovery passed 41 tests, and lifecycle migration passed 22 tests. The
  "FM-QUOTE" negative and retired public execution-roster tests passed.
- Aggregate evidence: "validate-repo-quality-gates.sh" passed all 22
  repository-static gates over 1,015 paths, including archive, GitOps,
  Kubernetes manifest, secret-handling, Registry, Markdown, links, lifecycle,
  and repository-quality owners.
- Recovery-grade Git readers intentionally remove external "GIT_*" variables.
  The final staged lane therefore used a byte-exact backup/install/restore of
  the prepared temporary index. A premature postcondition check ran while the
  long-running links validator was still active and therefore observed the
  temporary index. After the process completed, the exit trap restored the
  exact backup; "cmp" confirmed that the real index matched its original bytes
  and the real cached diff remained empty.
- Follow-up on 2026-09-04 refreshed the seven existing detect-secrets
  fingerprints from their pre-rename research paths and line numbers to the
  current "m0007" and "m0012" paths, without recording secret values. Ruff
  formatted the two long Archive owner constants in the agent checkpoint and
  loop validators. With the prepared staged snapshot installed, the complete
  "pre-commit run --all-files" then passed every applicable repository,
  parser, formatting, secret, shell, security, and infrastructure hook; the
  Dockerfile hook correctly skipped because no Dockerfile was selected.
- ADR acceptance validation used the exact six-file staged set. Direct strict
  Registry, Markdown, links/owners, and staged lifecycle checks passed; the
  affected and staged routing lanes each selected and passed seven validators.
  The lifecycle result proves ADR-0033's committed `proposed` predecessor and
  this change's legal `proposed -> accepted` transition.
- The first affected-lane attempt used shell process substitution and failed
  closed with `SURFACE-PATH-TRANSPORT`; the validator requires a regular bounded
  NUL file. Repeating both lanes with `/tmp/spec-0054-acceptance.nul` produced
  the passing six-path results above. The temporary file contains paths only.
- Plain staged pre-commit first failed before hook execution because the
  sandbox could not create `.git/index.lock`. The approved elevated rerun
  passed every applicable hook. The 22-gate repository aggregate then passed
  over 1,015 paths, and `pre-commit run --all-files` passed every applicable
  hook; Dockerfile lint alone skipped because the repository has no selected
  Dockerfile. Neither invocation produced a formatter mutation.
- "git diff --check" passed and "git diff -- docs/98.archive" remained empty.
- Local static success is not hosted CI, Argo CD reconciliation, cluster
  readiness, Vault/ESO behavior, provider runtime, or release evidence.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-054-013](../plan.md#wp-013--current-corpus-and-transition-control-cutover) | In progress. | Sealed-endpoint pin released across three owners with four regression cases; intact tree `PASS CROSS-DOCUMENT`; no corpus removal made. |
