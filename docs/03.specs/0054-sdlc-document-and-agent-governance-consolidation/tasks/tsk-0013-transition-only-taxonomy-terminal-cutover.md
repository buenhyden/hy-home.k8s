---
title: "Task: Current corpus and transition-control cutover"
version: "1.5.2"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0054-TSK-0013"
---

# Task: Current corpus and transition-control cutover

## Overview

This is the in-progress Task record for the remaining Stage 01, 02, 03, and 99
current-corpus convergence and transition-control retirement in WP-013. Named
dispositions are execution candidates, not permanent corpus-count policy.

Re-observation on 2026-09-03 refreshed those candidates. Two entry steps now
precede the cutover: Spec 0052 closes, which releases the suspension recorded
against REQ-0007 and REQ-0008, and Spec Packages `0047` through `0051` each
receive a resume-or-remove disposition. The Stage 03 removal set is the fifty-two
packages that will be `done`. The fifty-one measured on that date partition into
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
released, document-contract v9 and the ADR-0032/ADR-0033 acceptance transitions
are committed, and the remaining WP-013 dispositions are not complete

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-054-013 | VAL-SDLC-001..VAL-SDLC-004, VAL-SDLC-006, VAL-SDLC-009..VAL-SDLC-012 | After the completed child and parent handoffs, reconcile retained Stage 01 Requirements and Stage 02 Architecture bidirectionally with the current implementation, converge the reviewed Stage 01/02/03/99 current-owner set, retain terminal governed documents under ADR-0032, remove current-authority dependencies on sealed Archive records, transfer unfinished work and unique authority, then retire residual transition assets against the accepted and completed Spec 0066 routing result without a fixed corpus census. | platform | In progress | Document-contract v9 proposed in `41f8144e`; ADR-0032/0033 acceptance and the Spec/Plan amendment committed in `5b7ff61f`; CI contract and regression fixes committed through `ad907cb1`; remaining WP-013 dispositions are open. | Terminal Spec 0066 states, completed SPEC-0054-TSK-0011, compatibility pointer to this Task, manifest/configuration/code/validator/operational-interface evidence mapped to retained Requirement Packages and Architecture Descriptions, completed-retention provenance, zero current-authority dependencies on sealed Archive records, consumer/trace/lifecycle parity, Git exact-byte recovery, Registry/template parity, delegated routing evidence, ordered logical commits, PRs 54 and 55, Hosted CI run 33885291302, and secret-safe read-only runtime observations |

## Approval and Safety Boundaries

The [common execution contract](../plan.md#common-execution-contract) applies
with the explicit human-approved Git/CI/read-only runtime evidence exception
recorded below. WP-013 may disposition a current document or template only
after its unique authority and unfinished work are transferred or proven
absent, current consumers are zero, and Git exact-byte recovery succeeds.
Terminal governed documents follow ADR-0032 retention rather than deletion. The linked Plan
owns the exact candidate dispositions, reviews, rollback, and five ordered
logical commits: Stage 03 prerequisites/current execution packages; Stage
01/02 Requirement and Architecture convergence; Stage 99
profile/lifecycle/template reduction; taxonomy transition-control retirement;
then Archive authority-link reconciliation. The 2026-09-05 human ruling is the
current execution context: this Plan/Task amendment precedes those
implementation commits and does not claim that any implementation commit
exists. The accepted and completed Spec 0066 result plus the completed
SPEC-0054-TSK-0011 parent handoff are fixed dependencies; their execution does
not overlap the final WP-013 validation-side transition-control unit. The
existing Spec 0054 compatibility pointer named this Task while it was still
`queued`, which satisfied the activation condition.
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
follow-up. One entry blocker is released, the document-contract v9 proposal and
separate acceptance commits are durable, and the accepted ADR-0032 retention
authority and ADR-0033 v9 decision are reflected in the Spec and Plan.

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
  `proposed` state. Commit `5b7ff61f` applies the user's 2026-09-04 acceptance
  as the later `proposed -> accepted` transition without weakening the
  lifecycle contract.
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
- Logical commits are `41f8144e` for the v9 proposal, `5b7ff61f` for ADR-0032
  and ADR-0033 acceptance plus Spec/Plan amendment, `aa501cf5` and `8d436c17`
  for PR candidate-ref preservation, and `7bc38f46` plus `ad907cb1` for the
  v9 regression contracts. The branch was pushed without force.
- PR 54 carried the v9 and decision commits and was observed as externally
  merged at head `8d436c17`; this work did not request or perform that merge.
  The later regression commits are isolated in open PR 55. No merge action was
  performed on PR 55.
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
- The regression-fix affected lane first failed closed with
  `SURFACE-PATH-TRANSPORT` because filtered `rtk git diff -z` output was not a
  raw NUL stream. `rtk proxy git diff -z` preserved the required machine path
  transport; the affected and staged lanes then passed over the exact three
  paths. Ruff reformatted one assertion, after which affected, staged, plain
  pre-commit, and all-files pre-commit were rerun and passed on the final bytes.
- Local regression evidence at `7bc38f46` is 143 focused tests passed and 887
  discovered tests passed with four skips. After Hosted CI exposed the
  version-dependent `jsonschema.validators.urlopen` test alias, the stable
  urllib/socket boundary replaced it in `ad907cb1`; the failing subcase and all
  41 generic migration recovery tests then passed locally.
- Hosted CI failures were preserved rather than promoted: run 33863703704
  exposed governance/test contract gaps, run 33866665565 exposed detached-HEAD
  history validation, run 33870903959 exposed six failures and four errors in
  the full regression suite, and run 33881795992 reduced the result to four
  version-dependent jsonschema setup errors. Final run 33885291302 on head
  `ad907cb1` passed branch policy, changes, pre-commit, agent governance,
  repository quality and all 887 regression tests, and CI summary. The
  test-only manifest job correctly skipped. Direct evidence is the run URL
  `https://github.com/buenhyden/hy-home.k8s/actions/runs/33885291302` and jobs
  `101063501929`, `101063501975`, `101063502057`, and `101073181642`.
- Secret-safe read-only runtime evidence used kubectl v1.30.14 against context
  `k3d-hyhome`, Argo CD CLI v3.3.6, Codex CLI 0.140.0, and Claude CLI 2.1.260;
  a Vault CLI was unavailable. Kubernetes `/readyz` returned `ok`, but only
  `k3d-hyhome-server-0` was Ready while three agent nodes were NotReady.
- Argo CD Applications included `Unknown` and `Degraded` health states, and
  `platform-ingress-nginx` reported an operation error despite Synced/Healthy
  resource state. ESO reported `vault-backend` as
  `InvalidProviderConfig`, and the observed ExternalSecrets reported
  `SecretSyncedError`. The `vault` namespace exposed no pods or services.
  These are direct FAIL/DEFER runtime observations, not reconciliation success.
- No Secret objects or values, logs, Vault KV/API data, provider credentials,
  or authenticated provider APIs were read. No apply, patch, sync, rollout,
  forced reconciliation, or other live mutation was performed. Provider CLI
  presence is not promoted to authenticated provider-runtime evidence.
- Release evidence is DEFER: the repository had only local tag
  `pre-consolidation-merge`, the GitHub release list was empty, no exact release
  version was supplied, and PR 55 remains unmerged. No tag or release was
  created.
- "git diff --check" passed and "git diff -- docs/98.archive" remained empty.
- Hosted CI success is scoped to run 33885291302. It is not Argo CD
  reconciliation, cluster readiness, healthy Vault/ESO behavior, authenticated
  provider runtime, release, or WP-013 corpus-removal completion.

### Stage 03 Current-Package Convergence (2026-09-05)

This is WP-013's first implementation unit, not integrated WP-013 completion.
The scoped paths are Specs/Plans 0047–0052, SPEC-0047-TSK-0001, the Stage 03
index, and this evidence record. No validator or test behavior changes.

| Package | Observed evidence and disposition | Next owner / trigger |
| --- | --- | --- |
| 0047 | Spec 0052 semantic closure releases suspension. Spec/Plan use `draft → active`; CSASR-000 uses `in-progress → done`; CSASR-001..005 remain queued. Stash object `6370311e020620cc2743005896cc88db97d15465` remains a reachable commit and was found at `stash@{1}` by metadata only. No tracked-hunk or target disposition work is claimed. | Platform / CSASR-001: re-observe current owners and refresh historical planned commands before implementation. |
| 0048 | Spec/Plan remain draft and all Tasks queued; proposed GitHub surface-routing contract and validator remain absent. | Platform / GRCE-000: activate only after 0047's evidenced package closure. |
| 0049 | Spec/Plan remain draft and all Tasks queued; thirteen Kustomize roots remain tracked, but proposed platform-evidence and Traefik validators remain absent. | Platform / PVSE-000: activate only after 0048's evidenced package closure. |
| 0050 | Spec/Plan remain draft and all Tasks queued; the current validation registry declares no Terraform/Bicep validator. | Platform / EIVQ-000: activate only after 0049's evidenced package closure. |
| 0051 | Spec/Plan remain draft and all Tasks queued; predecessors are unfinished. No integration, merge, stash retirement, or cleanup occurs. | Platform / RAIC-000: activate only after 0050's evidenced package closure and revalidate protected-action authority. |
| 0052 | Seventeen done Tasks preserve completed WORK-100..108/amendment evidence and explicit WORK-109..115 transfers to 0054. ADR-0031 discharges VAL-WDTC-015/016 census predicates; focused Archive/recovery/routing tests verify the semantic contracts. Spec/Plan use `active → done`. | WP-013 units 2 and 5: transfer current REQ/AD consumers, prove consumer-zero and historical-link safety, then retain with migration provenance. Keep the entire package at its current Stage 03 path meanwhile. |
| 0006 | Active Spec, no Plan or Tasks. Its Current Ownership Boundary retains the historical harness-gap baseline and unresolved runtime/operator boundaries; roster/provider normalization has successor ownership. Existing static evidence does not establish completion of the remaining boundary. No execution records are invented and no unfinished work is removed. | Platform: establish bounded execution or completed-scope evidence before another disposition. |
| 0062 | Active Spec/Plan, seven done and three blocked Tasks. The approved 2026-08-29 administrative-closeout addendum supersedes future old WRFR-007 Path B replay and WRFR-008/009 guarded completion. Historical missing/non-PASS evidence and all Task states remain unchanged. This slice does not execute administrative closeout. | Platform: narrowly reconcile current indexes/links/census under that addendum, then obtain fresh canonical local validation and independent review before the approved terminal route. No destructive replay or historical evidence reconstruction. |

Accepted ADR-0031/0033 and package-local v9 records replace superseded
ADR-0021/public execution-roster authority. Successor preplanning is retained;
only 0047 resumes, and each successor needs its predecessor's evidenced
closure before the legal Spec/Plan `draft → active` and activation Task
`queued → in-progress` transitions. Older provider/path/command examples are
historical proposal inputs requiring refresh, not authority to restore retired
controls. No public Registry instance row or decision lifecycle changes.

The first focused run was an invalid interleaved snapshot: document edits
occurred while repository-backed tests were running, before the index was
synchronized. It exited 1 with six failures and fourteen errors reporting
migration-target/index-worktree drift. This is not a product RED/GREEN cycle.
The same 187-test batch was rerun only after exact staging and with no
concurrent edits; no validator was weakened.

The stable rerun passed 187 tests in 743.530 seconds (exit 0). Its exact
command was `rtk python3 -m unittest tests.test_archive_validation tests.test_archive_recovery tests.test_validate_affected_surfaces tests.test_document_strict_cutover`.
The unchanged test/validator behavior makes a new product RED/GREEN cycle
inapplicable. Final strict, affected, staged, plain pre-commit, full-suite,
aggregate, all-files, formatter, and diff-check command results are recorded
in the controller-approved `.superpowers/sdd/plan/task-1-report.md`; this unit
cannot commit if a required gate fails.

Review ownership: implementer self-review is scoped to this unit; independent
requirements and quality/security review remains with the controller after
the implementation handoff, not claimed here. Rollback is a reviewed revert
of this one logical commit before dependent units, restoring only these
Stage 03 lifecycle/projection changes while preserving the stash and all
historical payloads. Do not roll back an accepted dependent unit implicitly.
No push, merge, release/tag, secret-value read, live mutation, forced
reconciliation, sealed Stage 98 edit, or later WP-013 unit occurs in this slice.

### Requirement and Architecture Authority Transfer (2026-09-05)

This is WP-013's second implementation unit, not WP-013 completion. Retained
REQ-0001..0004 and AD-0004..0007 own current requirements and architecture.
Their explicit member/responsibility mappings absorb REQ-0005..0008 and
AD-0008..0011 before the source paths leave current authority. All 24 surviving
canonical-link holders were updated; original decision lineage remains in
terminal ADR bodies and source-identical superseded records. REQ-0005/0006's
original successor was REQ-0008; REQ-0003 is the transitive current semantic
successor, not a rewritten original decision target.

The actual Registry admitted both already-superseded sources and the six
active-to-superseded edges, with current same-family replacements. Each source
Git blob passed private, fully redacted secret classification. New MIG-0019
and eight ADR-0032 superseded records preserve exact source commit/blob/digest
and payload. No pre-existing sealed payload or ADR lifecycle was changed.

Focused tests first exposed legacy-only mirror/creation evidence, v9 metadata
order and missing `tomb-REQ` admission. Further RED fixtures exposed WORK-107's
legacy census blocking independently proved additions and the cutover reader
discarding terminal status. Minimal routing/provenance bridges preserve the
old sealed inventory while requiring legal source edges, a current successor,
exact recovery identity and an independently valid sealed disposition. Active
or accepted record-as-authority, wrong category, unproved or mismatched source,
malformed reason and non-archived envelope remain rejected.

The final focused pre-disposition batch passed 24 tests in 13.769 seconds.
Before corpus edits, expanded lifecycle and Archive batches passed 93 and 192
tests respectively on unchanged snapshots. Final-snapshot strict, affected,
staged, full-suite, aggregate and pre-commit evidence is recorded in the
controller handoff report; these earlier runs alone are not final validation.
The remaining cutover bridge is transition-only compatibility to re-evaluate
with Task 4, not a permanent second source owner.

Specs 0047..0051 retain their unfinished package-local states and sequence.
Spec 0052 stays in Stage 03; no package retention, Stage 99 reduction,
transition-control retirement, final archive reconciliation, push, merge,
release/tag, secret-value read or live mutation occurs in this unit. This Task
remains in-progress. Independent review remains the controller's next step.

### Governance Source Cutover (2026-09-05)

This section initially recorded investigation and a proposed amendment. The
human subsequently replied "승인", approving the Stage 00 cutover and explicit
Codex procedure-read design. That approval is now applied by the
[execution amendment](../plan.md#approved-governance-source-cutover-amendment-2026-09-05);
implementation completion remains separate. The current request requires removal
of the repository-owned `.agents/` after source and consumer migration. The
existing Spec 0054 target tree retains that directory; WP-003's completed
approval therefore does not approve this new design. Spec 0068 is a related
`draft` with no Plan or Tasks and an unimplemented renderer proposal. Reuse
Spec 0054 for integration and reconcile that draft rather than create another
program or reopen a completed Task. This intake preserves WP-013's unfinished
work and all earlier evidence.

#### Starting State and Protected Work

| Observation | Evidence / disposition |
| --- | --- |
| Repository | `/home/hy/projects/hy-home.k8s`; sanitized origin `https://github.com/buenhyden/hy-home.k8s.git` |
| Starting HEAD / branch | `6c5ad33444fdbdbe4fb10e9d652287d89a56fe99`; `codex/document-contract-v9` |
| Local integration baseline | `main` and cached `origin/main` at `1632ce28443b5b5bebf9abdba13543d5731f43bc`; merge-base equals that commit; `main...HEAD` is 0 left / 11 right |
| Upstream | `origin/codex/document-contract-v9`; local branch is four commits ahead of the cached upstream |
| Worktree | One primary worktree at the repository root, attached to the current branch; Git common directory is `.git`; no linked worktree was created |
| Research snapshot | `69ae876221410370f13b190c463d88f02f02932a` is unavailable locally; ancestry command exits 128. No fetch or forced checkout was performed |
| Index / untracked | Initial `git status --porcelain=v1 -z` shows no staged entries and no untracked files; twenty pre-existing unstaged paths are listed below |
| Provider links | `.claude/skills` and `.codex/skills` are tracked symlinks to `../.agents/skills`; `.agents` is a real tracked directory |
| Ignored local work | `.claude/RESUME.md`, `.claude/settings.local.json`, seven `.claude/hookify.*.local.md` files, and Stage 00 hook bytecode were found by filename only and preserved. Local settings contents and hook trust were not inspected |
| Session permission boundary | The active managed profile marks `.agents/`, `.codex/`, and `.git/` read-only. Removal, Codex adapter edits, staging, branching, and commits are deferred; no escalation or write probe was attempted |
| Effective Git hook owner | `git config --show-origin --get core.hooksPath` resolves to `/home/hy/.codex/git-hooks` from the user Git configuration. Its content was not read or modified; tracked pre-commit configuration does not prove Git hook delivery |

Machine path collection used `git status --porcelain=v1 -z`,
`git ls-files --stage -z`, and `git ls-files --others` with `-z` and separate
ignored/exclude-standard selection. Display tables are not runner path input.
The current branch already descends from the local integration baseline and
contains the required ongoing document work; proposed implementation keeps
this branch/worktree rather than dropping those changes into a clean base.

Pre-existing unstaged work, preserved without staging or implicit ownership:

- `docs/03.specs/README.md`.
- `docs/99.templates/README.md`, `registry.json`,
  `contracts/frontmatter.schema.json`, and `templates/README.md`.
- Deleted `docs/99.templates/templates/governance/control.template.md` and
  `templates/specs/contracts/{data-model.template.md,openapi.template.yaml,schema.template.graphql,service.template.proto}`
  under the same Stage 99 root.
- `scripts/archive_recovery.py`, `scripts/document_authority.py`,
  `scripts/document_lifecycle.py`, and `scripts/validation/repository/quality.py`.
- `tests/test_archive_recovery.py`,
  `tests/test_document_lifecycle_archive_cutover.py`,
  `tests/test_document_lifecycle_cumulative_history.py`,
  `tests/test_document_lifecycle_migration.py`,
  `tests/test_document_strict_cutover.py`, and
  `tests/test_generic_migration_recovery.py`.

The initial diff contains 276 additions and 640 deletions. It removes unused
Stage 99 capacity and changes lifecycle/recovery behavior; it is relevant
input, not an approved commit belonging to this intake. Preserve its exact
scope and review its failed consumers before any later integration commit.

#### Initial Inventory and Proposed Disposition

These are reviewed design candidates, not a completed exhaustive disposition.
Implementation must extend this same Task with per-path consumer/recovery and
verification evidence before deletion.

| Current path / role | Conflict or consumer | Proposed disposition and final owner | Required proof |
| --- | --- | --- | --- |
| `.agents/registry.json` and `.agents/contracts/agent-registry.schema.json` | Exact roles, permission classes, skill refs and projections remain outside the requested common owner; harness, lifecycle, provider and routing validators consume them | Move the cohesive machine contract to `docs/00.agent-governance/roles/registry.json` and its schema below `roles/`; role records reference skill owners and provider bindings without duplicating their content | Schema, valid references, permission narrowing, migrated routing and negative legacy-path tests |
| `.agents/agents/*.md` | Twelve neutral bodies and two native copies; `@import` is embedded in ordinary instruction bodies | Move each role body to `docs/00.agent-governance/roles/<role-id>.md`; preserve the existing domain responsibility guides; derive native instructions from the role owner and provider binding | Preserve use conditions, inputs, outputs, permissions and handoffs; renderer drift and fixed point |
| `.agents/skills/*/skill.md` | Sixteen registered procedures; lowercase filenames differ from documented native `SKILL.md` entrypoints | Move to `docs/00.agent-governance/skills/<skill-id>/SKILL.md`, preserving native skill metadata and assets; adapt the Stage 99 profile rather than force a prose envelope onto native skill metadata | Registry completeness, link resolution, correct native shape and directly observed reads/discovery |
| `.agents/README.md` | Routes readers to the old authority | Merge useful routing into the Stage 00 hub, remove after consumer transfer; Git recovery uses the starting HEAD | No active old owner or recreated directory |
| `.claude/agents/`, `.codex/agents/` | Manually repeated bodies, inert import markers and unverified model metadata | Keep native generated bindings with explicit read instructions and original role IDs; provider binding facts belong under `providers/` | Claude metadata and Codex TOML parsing plus separately scoped discovery/execution evidence |
| `.claude/skills`, `.codex/skills` | Both links target the retiring directory; a Codex link does not prove discovery | Reconnect Claude to Stage 00 procedures; preferred Codex fallback is explicit root `AGENTS.md` reads, removing the misleading skill view | Approved support contract; do not report explicit reading as native automatic discovery |
| `.claude/settings.json` | `customInstructions` includes retired `memory/`; registered hooks execute code under Stage 00 | Remove unsupported/inert instruction placement after schema confirmation; keep effective policy in the gateway; move native event adapters to `.claude/hooks/` and reusable validation logic to `scripts/` | Valid settings/event schema, root boundary, allow/deny/error cases and hook trust distinction |
| `.claude/hooks/`, `.codex/hooks/`, `.codex/hooks.json`, `.codex/config.toml` | All absent at intake | Create only necessary Claude adapters when moving its existing registered handlers; Codex hooks remain unadopted unless a concrete missing guarantee needs an approved native binding | No empty symmetry directories, no Claude event replay in Codex |
| `docs/00.agent-governance/hooks/` and `contracts/` | Transitional runtime code and contracts still occupy the human governance root | Move executable core and check configuration to their existing script/validation owners; lifecycle semantics to policies/skills, provider observation contracts to providers | All registrations and consumers follow the move; preserve finite limits and failure propagation |
| `policies/quality.md` | Repeats timeout/output/cleanup constants while prohibiting duplicate numeric owners | Retain guarantee and lane meaning here; `scripts/run-validation-lane.py` owns executable bounds | Timeout, stdout/stderr overflow, invalid paths and descendant/pipe cleanup regressions |
| README, SDLC, terminology, Stage 99 and current/retained Spec consumers | Root README guidance and old authority/topology claims require reconciliation with the current registry | Update their existing semantic owners and governed profiles; preserve native formats, accepted history and sealed records | Profile, link, lifecycle and recovery checks; no blanket translation or new glossary |
| `scripts/`, `tests/`, fixtures, pre-commit and CI | Direct legacy consumers extend beyond the four governance/provider folders | Change ownership paths and independent expectations in the same vertical unit; remove only proven duplicate or consumer-zero surfaces | Invoked guarantees remain covered; old-path regeneration and permission widening fail |

The twelve role mappings observed from the neutral bodies are:

| Role ID | Existing responsibility guide(s) under Stage 00 roles |
| --- | --- |
| `code-reviewer` | `architecture.md` |
| `doc-writer` | `documentation.md` |
| `docs-researcher` | `documentation.md` |
| `gitops-reviewer` | `infrastructure.md` |
| `incident-responder` | `operations.md`, `infrastructure.md` |
| `k8s-implementer` | `infrastructure.md` |
| `network-reviewer` | `infrastructure.md` |
| `observability-reviewer` | `infrastructure.md` |
| `quality-engineer` | `quality.md` |
| `security-auditor` | `security.md` |
| `supervisor` | `supervision.md` |
| `wiki-curator` | `documentation.md` |

Registered skill IDs are `deployment-strategies`, `docs-stage-conformance`,
`docs-stage-routing`, `execution-plan`, `gitops-workflow`,
`incident-postmortem`, `k8s-security-audit`, `k8s-validate`, `knowledge-map`,
`ops-runbook`, `rca-methodology`, `requirements-to-design`, `risk-report`,
`task-breakdown`, `vulnerability-patterns`, and `workspace-harness-audit`.
All sixteen metadata blocks parse with `name` and `description`. All twelve
Claude frontmatter blocks and twelve Codex TOML files parse syntactically;
this is not native schema acceptance, account model availability or execution.

#### Design Alternatives and Proposed Execution Order

1. **Recommended within current configuration scope:** move common sources
   and every consumer together; use a verified Claude skill view and explicit
   Codex `AGENTS.md` read instructions. Codex automatic skill discovery is
   explicitly unadopted for these repository procedures, subject to human
   design approval. A required native-discovery outcome remains DEFER rather
   than being silently replaced by this fallback.
2. **Native skill plugin:** a skills-only package owned below `.codex/` may
   supply native discovery, but requires proof of package/link containment,
   installation, activation/trust and real invocation. Merely creating a
   plugin manifest is insufficient; global installation is outside this
   request. Do not adopt this option without a supported local-only route and
   the necessary activation authority.
3. **Temporary `.agents/` compatibility:** rejected as a terminal design
   because copies, symlinks or regeneration conflict with the direct request.

After one explicit approval of the selected design, amend the existing
Spec/Plan with four dependency-ordered vertical units: (1) shared authority,
SDLC/document contract and relevant unfinished-input reconciliation;
(2) source/registry/native binding/generator/validator cutover and removal;
(3) measured duplicate invocation/fixture reduction with regression checks;
(4) historical/current navigation closure and final evidence. Exact executable
steps belong in the Plan after approval, not a parallel Superpowers tree.
Keep Codex model selections unless a supported correction is demonstrated;
do not inherit Spec 0068's proposed blanket model promotions as new authority.
Invalid Claude model labels need a documented compatible binding decision,
not an assumed latest-generation replacement.

Maintain desired-state ownership in `gitops/`; keep `infrastructure/`,
`traefik/`, `examples/`, and Kubernetes Rego `policy/` in their distinct roles.
External Vault/PostgreSQL/Valkey remain interface dependencies. No live
mutation, remote integration, global configuration edit or secret access is
authorized by this design.

#### Tool, Baseline and Cost Evidence

Installed local tools: Codex CLI `0.140.0`, Claude Code `2.1.260`, RTK
`0.45.0`, pre-commit `4.5.1`, Python `3.12.3`, PyYAML `6.0.1`, and jsonschema
`4.10.3`. Codex `features list` reports hooks, plugins and multi-agent support
enabled. It does not establish project/hook trust. CLI observation emitted a
read-only PATH-alias warning; no permission or global PATH change was made.
Superpowers `6.3.0` using-superpowers, its Codex tool reference, and
brainstorming were read from the installed openai-curated-remote cache.
There is no dedicated Skill invocation tool in this session; filesystem
reading is the actual invocation mechanism. Implementation/finishing skills
remain pending the design checkpoint.

| Command / scope | Exit | Result / observation |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .`, invoked through `rtk proxy` before this Task edit | 1 | FAIL; all-files input reports 1,017 paths. Known failures below reproduce independently; this run is not completion evidence |
| `python3 scripts/validate-affected-surfaces.py --root .` | 1 | FAIL, 0.199 s; `SURFACE-PATH-MISSING` for the pre-existing deletion of `docs/99.templates/templates/governance/control.template.md` |
| `python3 scripts/validate-agent-legacy-cutover.py --root .` | 1 | FAIL, 0.923 s; `AGQC-LEGACY-OWNER`, canonical owner validation failed |
| `python3 scripts/validate-links-and-owners.py --root . --mode strict --include-path docs/99.templates/templates/archive/tombstone.template.md` | 2 | FAIL, 1.200 s; `WORK-054 WP-004B migration recovery proof differs` |
| `python3 scripts/archive_cutover.py --root .` | 1 | FAIL, 5.956 s; incomplete cutover, migration parity/recovery and eight superseded-source ownership diagnostics |
| `git diff --check`, initial unstaged snapshot | 0 | PASS; whitespace only |
| `python3 scripts/validate-document-contract-registry.py --root . --mode strict --include-path` followed by this Task path | 0 | PASS after intake authoring; command reports 715 paths, zero uncovered and zero ambiguous paths; this is its actual broader scan scope |
| `python3 scripts/validate-markdown-profiles.py --root . --mode strict --include-path` followed by this Task path | 0 | PASS after intake authoring; zero profile violations reported |
| `git diff --check` and `git diff --cached --check`, after intake authoring | 0 / 0 | PASS; index remains empty, so cached whitespace success is vacuous and is not staged validation |
| affected/staged runner, plain and all-files pre-commit, message/manual and post-formatter final bytes | Not run | DEFER for implementation completion; no new logical index exists and staged/Git writes are read-only. Do not execute formatters over preserved user work merely to claim a baseline |
| Native skill discovery, model resolution and hook delivery/trust | Not run | DEFER; syntax and feature availability are not runtime evidence |
| Hosted CI and live services | Not run | Outside authorized scope; no dispatch, deployment or cluster creation |

Focused timings above use one `time.monotonic()` observation per subprocess;
they are not benchmarks or aggregate duration. The registry lists 22 all-files
validators. Eight explicit commands in `agent-governance-static` also appear
in the all-files aggregate: affected-surface, CI topology, harness contract,
harness semantics, legacy cutover, loop lifecycle, provider evidence, and CI
Python contract. This is a static overlap candidate when both jobs are
selected, not a measured hosted run or a completed reduction. CI already skips
two local aggregate hooks in its pre-commit job; preserve that existing owner
split. Working-tree, index and post-formatter checks remain distinct.

#### Official Feature Evidence and Remaining Decisions

- [Codex skills](https://learn.chatgpt.com/docs/build-skills) documents
  `.agents/skills` repository discovery and `SKILL.md`; `.codex/skills`
  presence alone does not establish native discovery.
- [Codex plugins](https://learn.chatgpt.com/docs/build-plugins) distinguishes
  package creation, installation and testing in a new conversation.
- [Codex hooks](https://learn.chatgpt.com/docs/hooks) describes project-local
  hooks, additive source loading and trust of the exact hook definition.
  The current provider note's blanket unsupported-hook wording needs correction.
- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents),
  [Claude subagents](https://code.claude.com/docs/en/sub-agents),
  [Claude hooks](https://code.claude.com/docs/en/hooks), and
  [Claude settings](https://code.claude.com/docs/en/settings) are reference
  contracts, not proof of native execution in this workspace.

#### Approved Execution, Concurrent Work and GC-001 Evidence

The human confirmed that the twenty staged paths belong to another Codex task
in the same workspace. Read-only task inspection identifies that active task
as `hy-home.k8s 문서 거버넌스 체계 통합`; it owns Stage 99, document lifecycle and
Archive consumer changes. This controller neither staged those files nor
modified their index entries. At resume, that index already includes further
changes to `tests/test_document_strict_cutover.py`; the intake's earlier
unstaged counts remain historical observations, not a frozen shared index.

`/proc/self/mountinfo` confirms read-only mounts at this checkout's `.agents`,
`.codex` and `.git`, and `os.access(..., os.W_OK)` returns false for each.
The repository root, Stage 00 and scripts remain writable. No failed write,
escalation, alternate-index workaround or shadow checkout was used. The
approved source cutover, Codex adapter changes and local commits are DEFER
until the host supplies the needed scoped write capability. Design approval
is satisfied and must not be requested again for the same boundary.

GC-001 changed only `policies/quality.md` and
`tests/test_run_validation_lane.py`, alongside this Plan/Task evidence. The
policy links to the runner's numeric owner and retains finite time/output,
monotonic cleanup, concurrent draining and failure semantics. The old test's
requirement to repeat numeric prose was removed; all four reviewed numeric
assertions and all runner behavior regressions remain. The production runner
was not modified. No fixture, lane or CI invocation was removed in this unit.

| Command / scope | Exit | Result |
| --- | --- | --- |
| `python3 -m unittest tests.test_run_validation_lane.BoundedValidationCommandTest.test_reviewed_limits_match_the_sole_quality_owner`, after the policy edit and before test migration | 1 | Expected contract mismatch: the old test requires the removed numeric sentence. This demonstrates obsolete prose coupling, not a newly discovered runner defect |
| `python3 -m unittest tests.test_run_validation_lane`, after test migration | 0 | PASS; 52 tests in 2.326 s, including timeout, both pipe limits, process/pipe cleanup and selection behavior |
| `python3 scripts/run-validation-lane.py --root . --lane affected --paths-file <temporary NUL file> --delimiter nul`, containing exactly the four GC-001 paths | 1 | FAIL; 138.360 s elapsed for this invocation, six selected validators PASS and four FAIL: legacy cutover, document lifecycle, links/owners and repository quality |
| `python3 scripts/validate-document-lifecycle.py --root . --mode strict`, diagnostic rerun | 1 | FAIL; MIG-0005 evidence is not proved against the other task's staged snapshot, `ARCHIVE-MIGRATION-STAGED-DRIFT` |
| `python3 scripts/validation/repository/quality.py --root .`, diagnostic rerun | 1 | FAIL; the Task's actual root path and the approved Plan/Task's proposed Claude hook path are rejected by old blanket path rules |
| Strict document registry and Markdown profiles, with explicit includes for the three owned documents | 0 / 0 | PASS; registry reports 715 paths, no uncovered/ambiguous paths; Markdown reports no violations |
| `git diff --check` and `git diff --cached --check` | 0 / 0 | PASS for whitespace only; none of the four task-owned paths occurs in the other task's index |
| Exact logical staged lane, pre-commit and local commit | Not run | DEFER: current index belongs to the concurrent task and Git is read-only |
| Independent reviewer | Not run | DEFER: inline execution has not obtained independent review; no reviewer identity is invented |

The repository-quality failures are newly exposed by this design/evidence
text, not pre-existing baseline failures. That validator includes `str(root)`
in its stale-path set and categorically rejects the proposed Claude hook
directory. Its staged owner is the concurrent task, so this controller did
not modify it, mask the failures, or conceal required paths to pass it. GC-002
must replace those obsolete owner assumptions with current path/evidence
semantics and independent negative cases when consumer ownership transfers.
The legacy and links/owners errors retain the intake's recorded recovery
failure signatures. The direct lifecycle result identifies the additional
shared-index evidence boundary; it is not repaired by including another
task's staged work in this unit.

The next owner is this controller after the host write boundary and concurrent
consumer handoff are resolved. Preserve all other work, this unit's unstaged
diff and the existing branch. GC-001 has focused evidence but is not a completed
commit; GC-002 through GC-004 and final branch completion remain outstanding.

#### GC-002 Independent Input-Boundary Preparation

The subsequent continuation preserved the concurrent task's twenty staged
paths and added two owned unstaged paths: `scripts/validate-agent-harness-contract.py`
and `tests/test_validate_agent_harness_contract.py`. The existing reader checked
`PurePosixPath.parts` after that constructor had collapsed empty and dot
components. Consequently three non-normalized aliases loaded the same JSON;
dot-only and NUL inputs instead escaped as `IndexError` and `ValueError`.
The new test reproduced all five behaviors before the production edit.

The reader now checks raw slash-separated components and rejects NUL before
opening an input file. It retains the existing `AGENT-REGISTRY-INPUT` error
and value-free detail, bounded reads and no-follow descriptor traversal.
Two focused tests use a disposable directory containing one synthetic JSON
file: normal string/path inputs remain readable, while eight invalid input
forms are rejected. No source corpus was copied or moved. The renderer remains
unimplemented pending the atomic source/consumer transition; a second source
authority or an unused generator scaffold was not introduced.

| Command / scope | Exit | Result |
| --- | --- | --- |
| `python3 -m unittest tests.test_validate_agent_harness_contract.AgentHarnessRegistryContractTests.test_non_normalized_json_paths_fail_with_a_registry_error`, before the reader fix | 1 | Expected RED: three accepted aliases and two uncaught exceptions reproduced in 0.055 s; the other invalid forms already failed closed |
| `python3 -m unittest tests.test_validate_agent_harness_contract tests.test_validate_agent_registry`, after the fix | 0 | PASS; 22 tests in 0.357 s |
| `python3 scripts/validate-agent-harness-contract.py --root .` | 0 | PASS; current registry has two providers, twelve roles, three permission classes, sixteen skills, thirty-four handoffs and thirty-six projections; this is static evidence only |
| `ruff check --no-cache scripts/validate-agent-harness-contract.py tests/test_validate_agent_harness_contract.py` | 0 | PASS with installed Ruff 0.15.12; system Python has no Ruff module, so the existing CLI was used without installing anything |
| `ruff format --no-cache --check scripts/validate-agent-harness-contract.py tests/test_validate_agent_harness_contract.py`, before formatting | 1 | One newly added test line required wrapping; formatter subsequently changed only the owned test file, exit 0 |
| `python3 -m unittest tests.test_validate_agent_harness_contract tests.test_validate_agent_registry tests.test_run_validation_lane`, after formatting | 0 | PASS; 74 tests in 2.400 s |
| Ruff check and format-check on the two Python paths, after formatting | 0 / 0 | PASS; no remaining lint or formatting changes |
| `python3 scripts/run-validation-lane.py --root . --lane affected --paths-file <temporary NUL file> --delimiter nul`, exactly the six owned paths | 1 | FAIL; 137.128 s, fifteen selected validators: eleven PASS, legacy cutover / document lifecycle / links and owners / repository quality FAIL with exit codes 1 / 1 / 2 / 1 |

This focused fix is reviewable but uncommitted. The six owned paths remain
separate from the concurrent task's index. During the affected run, additional
unowned unstaged changes appeared in `scripts/archive_cutover.py`,
`scripts/document_authority.py` and `tests/test_archive_cutover.py`; they were
preserved. This execution observed a changing shared working tree, not a frozen
index or commit. Adding the validator script to the affected scope selected
five more static checks than GC-001's four-path run: GitOps structure,
infrastructure contracts, Kubernetes manifests, policy gates and secret
handling. Each passed; the different scope and shared edits prevent a cost
reduction claim from the two timings. No gate or fixture was removed.
At the final status observation, the concurrent index contained twenty-two
paths and only this controller's six paths remained unstaged. HEAD stayed
`6c5ad33444fdbdbe4fb10e9d652287d89a56fe99`; this controller made no commit.
Previously recorded integration
failures and required staged/pre-commit/native evidence remain unresolved;
these focused passes do not close GC-002 or the overall Task.

### Task 3/4 Current-State Handoff (2026-09-05)

Task 3 completed as commit `7e13e2b9d838563343c5182cd8127c3a18944268`
(`refactor(templates): reduce document control plane`). Its final affected and
staged lanes each passed 15 validators; plain pre-commit and all-files
pre-commit passed without formatter mutation. The isolated-clone full suite
passed 929 tests with four expected hook-worktree skips; its 22-validator
aggregate and working-tree/index diff checks also passed.

Task 4 retires the transition manifest, mover, and dedicated test while
preserving sealed-ledger and Git recovery evidence. Its focused GREEN checks
passed 35 tests (2 archive/link, 2 affected-surface, 29 disposition-route, and
2 historical-proof); changed Python and focused tests compiled, and its diff
check passed. Documentation now removes the retired scripts row and treats the
former manifest only as historical sealed/Git recovery evidence.

Task 4 transition retirement is committed as `2b9bf9e`; the document branch
merged to main as `0540a433`, and governance snapshot `f4275f5e` is in merge
finalization. A focused integrated run has 56 passes from 57 tests; its one
failure is a sandbox-created empty `.agents` directory; the isolated Stage 00
owner check passes, distinguishing that environment condition. Archive snapshot
integration currently fails on `ARCHIVE-MIGRATION-LEDGER` for MIG-0002 after the
source move, and its bounded fix verification remains pending.
Final affected/staged/all-files lanes, aggregate/full-suite evidence,
independent review, hosted/runtime/release evidence, and final governance merge
remain pending. No Task 5 or WP-009 expansion was performed. This Task remains
`in-progress`; rollback remains a reviewed revert of the applicable logical
commit, and the parent owner retains ordered integration handoff responsibility.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-054-013](../plan.md#wp-013--current-corpus-and-transition-control-cutover) | In progress. Stage 03 state convergence and Stage 01/02 authority-transfer evidence are recorded above; remaining WP-013 dispositions and integrated closure are not complete. | Earlier acceptance, local/Hosted and read-only runtime evidence remains scoped to its original observations. The two dated implementation sections record the later local corpus work; neither claims live mutation or final WP-013 completion. |
