---
title: 'Archive Record and Workspace Boundary Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-18
---

# Archive Record and Workspace Boundary Implementation Plan

## Overview

This Plan executes Spec 036 in five dependency-ordered packages. It replaces
the finite 31-record Tombstone compatibility surface with byte-preserved,
non-current archive records, proves 202 historical links in source context,
cuts current navigation over to the archive index, and enforces `_workspace`
through Git metadata without reading ignored scratch children.

Each implementation package begins with a named RED reproduction, ends with
GREEN repository evidence and two-stage independent review, and receives one
logical commit. Baseline and rollback parent for this activation are
`04cb3a6`; no archive payload, validator, or workspace rule is implemented by
the planning commit itself.

Independent requirements review first rejected split cutover commits, stale
current projections, and missing RED cases. After the Plan combined production
authority and corpus cutover, aligned indexes/ledger, and added deterministic
RED diagnostics, re-review returned `REQUIREMENTS COMPLIANT`. Independent
quality review then required fixture-only ARWB-001 authority, non-disclosing
secret classification, and detailed anchor maps; remediation re-review returned
`QUALITY APPROVED`.

ARWB-001 through ARWB-004 are committed as `6b9b9cd`, `f8a54dd`, `787b28f`,
and `87ff444` after their package reviews. ARWB-005 is complete as an exact
eight-file staged closure proposal and local QA handoff, not as a committed or
post-commit result. Fresh independent whole-tranche reviews returned
`REQUIREMENTS COMPLIANT` and `QUALITY APPROVED` with no findings. The closure
commit remains uncreated and post-commit results remain unclaimed. Planning commit
`04a4d32` and package commits `6b9b9cd`, `f8a54dd`, `787b28f`, and `87ff444`
precede remediation commit `4ccc616`, which binds the historical ARWB-003
registry proof to committed cutover `787b28f` through closed Git-object
resolution. Its reviews returned `REQUIREMENTS COMPLIANT` and
`QUALITY APPROVED`. Rollback parent `4ccc616` and pre-closure range
`04a4d32^..4ccc616` bound the proposal; Spec 037 remains active,
dependency-ready, and unplanned with no Plan or Task.

## Context

ADR-0018 supersedes the metadata-only archive model. Twenty-six source files
are recoverable from `5e0221525450dbdacb585e6c98ade3f060ddc827` and five from
`82f0e1922d9748a88b1487a32a59629ba523f408`. The approved inventory contains
31 Git blobs and 202 historical repository-local links. These counts are
planning inputs, not newly executed recovery results.

Registry v7 keeps the exact 31 Tombstone paths readable through a
baseline-only compatibility profile and denies new Tombstones, deletion,
rename, and profile change. Spec 036 must introduce the full-body archive
route, ArchiveEnvelope.v1 metadata and byte grammar, source removal and archive
creation predicates, and migration evidence atomically before retiring that
compatibility surface.

The `_workspace` contract is deliberately asymmetric. `_workspace/README.md`
is the only tracked member; every child path is ignored local scratch. Repo
checks may inspect Git index and ignore-rule results for explicit path strings,
but must not list, glob, traverse, open, hash, move, or delete ignored children.
Temporary dry-run data may be written there only by an explicitly invoked
operator workflow; this Plan and its validators do not require or inspect it.

### File and interface map

| Boundary | Intended owners | Responsibility |
| --- | --- | --- |
| Recovery and envelope | Archive support/form, registry/schema, focused recovery module and fixtures | Recover exact Git blobs and define ArchiveEnvelope.v1 without worktree byte conversion. |
| Archive validation | Archive validator, lifecycle/link adapters, fixtures, script inventory | Check metadata, marker, payload, Git identity, digest, immutability, and source-context links. |
| Corpus conversion | Exact 31 `docs/98.archive/**` records and durable migration evidence | Replace each Tombstone once while preserving payload bytes and provenance. |
| Current navigation | `docs/98.archive/README.md`, current-link consumers, owner/link fixtures | Route current documents to the archive index and reject individual archive records as current owners. |
| Scratch boundary | `_workspace/README.md`, Git-metadata guard and isolated fixtures | Prove one tracked README and ignored-child non-traversal. |
| Closure | Spec/Plan/Task, indexes, registry relation, migration ledger | Record repository-static completion, reviews, rollback, and downstream DEFER boundaries atomically. |

## Goals & In-Scope

- Recover the approved source blob for every one of the 31 original paths and
  produce deterministic path, commit, blob, size, SHA-256, and link evidence.
- Define the closed `content/archive` route, ArchiveEnvelope.v1 form/support
  contract, reason/replacement dependency, and source-tree-aware validation.
- Replace all 31 Tombstones with one mirrored full-body archive record each,
  remove the duplicate Tombstone form/profile, and preserve source bytes
  through EOF without newline normalization.
- Validate all 202 historical links against their source commit and original
  path while keeping current link validation separate.
- Make the archive index the sole current navigation boundary and reject
  active direct links to individual archive records.
- Enforce `_workspace` through tracked-index and ignore metadata only, with no
  read of ignored local content.
- Prepare Spec 036's exact atomic lifecycle proposal only after focused/full
  static QA. Require fresh independent whole-tranche requirements and quality
  review before the closure commit; those reviews are now approved with no
  findings. Do not pre-claim post-commit results.

## Non-Goals & Out-of-Scope

- Moving completed Plans or Tasks; Spec 037 owns execution-retention migration.
- Reading, enumerating, hashing, preserving, cleaning, or deleting ignored
  `_workspace` children, local diagnostics, auth files, tokens, or shell state.
- Preserving secret-bearing history through the ordinary archive workflow;
  such a record is `BLOCKED` for the separately approved removal path.
- Rewriting payload links to current locations or treating archive records as
  current requirements, design, execution, or operations authority.
- Binary archive support, remote object retention, live GitHub changes,
  Kubernetes/Vault/ESO/Argo CD actions, or provider-runtime evidence.
- Installing CI/toolchain support or repairing FIFO portability; Spec 039 owns
  those concerns.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| ARWB-001 | Define recovery and ArchiveEnvelope.v1 capability | Active Spec/Plan/Task pair | RED envelope, metadata, source-object, reason, and byte-boundary fixtures | Recovery/parser/schema capability with no production route or form, GREEN fixtures, review, logical commit |
| ARWB-002 | Implement archive and historical-link validators | ARWB-001 | RED digest, mutation, source-context, direct-current-link, and ambiguity cases | Deterministic validator interfaces, stable diagnostics, GREEN self-tests, review, logical commit |
| ARWB-003 | Atomically migrate 31 records and cut archive authority | ARWB-002 | RED partial-cutover fixture plus exact approved 31/202 preflight | 31 full-body records, 202/202 links, complete index, zero direct current links, retired Tombstone form/profile, review, one logical commit |
| ARWB-004 | Enforce tracked-metadata-only `_workspace` boundary | ARWB-003 | RED tracked-child, force-add, traversal-attempt, and ignore-rule cases | Index-only guard, isolated fixtures, one tracked README, no ignored-child read, review, logical commit |
| ARWB-005 | Run full gates and close the tranche atomically | ARWB-004 | RED incomplete-closure transition plus all prior package approvals | Done Spec/Plan/Task and relation, aligned indexes/ledger, full QA, whole-tranche review, rollback boundary |

### ARWB-001: Recovery and envelope contract

- [x] Add RED fixtures for missing/ambiguous Git objects, wrong original path,
  malformed or misplaced v1 marker, payload collision text, final-newline
  changes, non-UTF-8 input, invalid reason/replacement pairs, and worktree-byte
  substitution.
- [x] Define one recovery result containing original path, source commit, full
  blob ID, byte count, SHA-256, historical-link count, and proposed mirrored
  archive path. Git blob bytes, never a converted worktree read, are canonical.
- [x] Define the ArchiveEnvelope.v1 metadata schema, recovery/parser interfaces,
  and private fixture capabilities without activating a production archive
  route, canonical form, admission rule, evidence predicate, or Tombstone
  retirement.
- [x] Run the focused RED/GREEN suite, strict registry/Markdown checks, request
  requirements review then quality review, remediate, and commit ARWB-001.

### ARWB-002: Archive validators

- [x] Add RED cases for metadata/order/type errors, blob or digest mismatch,
  payload mutation, wrong mirror, source-tree miss, current-tree confusion,
  archive reactivation, active direct link, and duplicate archive authority.
- [x] Implement a fail-closed archive parser and validator with stable
  diagnostics for envelope, provenance, integrity, historical-link, current
  authority, and immutability failures.
- [x] Reuse the canonical rendered-link interface for current Markdown and a
  source-commit/original-path resolver for payload links; do not rewrite
  historical destinations or create a second Markdown authority.
- [x] Run focused fixtures and strict current-corpus checks, obtain independent
  requirements and quality approval, and commit ARWB-002.

### ARWB-003: Atomic corpus and authority cutover

- [x] Add a RED proposed-snapshot fixture that admits a full-body record while
  retaining the Tombstone route/form or incomplete index/current-link state;
  require a stable `ARCHIVE-CUTOVER-INCOMPLETE` diagnostic before migration.
- [x] Run a read-only recovery preflight directly from Git objects and require
  exactly 31 unique source records with no missing, duplicate, ambiguous, or
  secret-bearing ordinary-workflow admission. A validator may stream tracked
  blob bytes in memory only through a secret classifier with redacted
  diagnostics; it must never print a payload, match, or value, and a detection
  blocks envelope creation.
- [x] Produce one archive envelope plus exact source payload at every mirrored
  path. Verify blob bytes, byte count, final-newline behavior, and SHA-256 for
  each proposed record before replacing any compatibility form.
- [x] Prove 31/31 archive records and 202/202 historical local links against
  their source trees. Any mismatch blocks the entire migration package.
- [x] Add RED inventory checks for incomplete archive-index membership, stale
  Tombstone language/form/profile, active direct links to individual records,
  duplicate original-path ownership, and missing current replacement targets.
- [x] Activate the production `content/archive` profile, canonical form,
  value/admission/evidence predicates, and source-removal/archive-creation
  rules only in this complete proposed cutover snapshot.
- [x] Update the archive index and only directly implicated current consumers
  so current navigation targets the index. Preserve payload text unchanged.
- [x] Remove the retired Tombstone form/profile and prove the full-body archive
  route is the only archival role after all 31 records are admitted.
- [x] Record a durable tracked manifest in the owning Task/index evidence. Run
  registry, Markdown, link/owner, archive, and stale-route checks against the
  complete proposed snapshot, obtain independent requirements and quality
  approval, and commit the records, index, current links, predicates, and
  Tombstone retirement together as ARWB-003.

### ARWB-004: `_workspace` Git-metadata guard

- [x] Add isolated RED fixtures for an extra tracked child, force-added ignored
  child, symlink or non-regular tracked member, absent README, and a validator
  attempt to enumerate or open ignored children.
- [x] Implement the production check using tracked Git index entries plus
  explicit ignore-rule queries only. The validator must not use filesystem
  walking, directory listing, globs, recursive hashing, or content reads below
  `_workspace/`.
- [x] Prove `git ls-files _workspace` yields only `_workspace/README.md` and an
  explicit scratch probe path is ignored without creating or opening it.
- [x] Run isolated and production metadata checks, obtain independent
  requirements and quality approval, and commit ARWB-004.

### ARWB-005: Validation and lifecycle closure

- [x] Reproduce the RED staged proposal that marks only Spec 036 done while its
  Plan, Task,
  registry relation, indexes, or ledger remain active/missing; require the
  exact lifecycle evidence/cardinality failure before closure.
- [x] Prepare the atomic closure proposal for Spec 036, this Plan/Task, the
  program relation, three indexes, and three migration-ledger rows; leave Spec
  037 with no Plan/Task.
- [x] Run recovery/archive/workspace self-tests, 31/202 corpus verification,
  strict registry/Markdown/link/lifecycle lanes, and the repository aggregate.
- [x] Run the applicable all-files pre-commit boundary and record its actual
  result. A FIFO `Errno 95` may remain Spec 039 `DEFER`
  only if independently reproduced and every other hook passes.
- [x] Obtain fresh whole-tranche requirements and quality approval. The
  independent closure reviews returned `REQUIREMENTS COMPLIANT` and
  `QUALITY APPROVED` with no findings.
- [x] Record the local command matrix, package history, rollback parent
  `4ccc616`, and exact staged proposal. The closure commit and post-commit
  strict/snapshot/clean-tree results remain pending and unclaimed.

## Verification Plan

| Lane | Focused evidence | Required result |
| --- | --- | --- |
| Recovery/envelope | Recovery and ArchiveEnvelope.v1 self-tests | Exact byte boundaries, Git identity, digest, UTF-8 admission, reason dependency, and round-trip controls pass. |
| Archive corpus | Read-only preflight then proposed-record validation | 31/31 unique records, exact source bytes, zero provenance mismatch. |
| Historical links | Source-commit/original-path link validation | 202/202 links resolve in source context; obsolete-but-historical links are not rewritten. |
| Current authority | Registry, Markdown, cross-document, and active-link scans | Zero uncovered/ambiguous route, no active direct archive-record authority, index is complete. |
| Workspace | Isolated Git-index fixtures and production metadata check | Only tracked README; explicit probe ignored; zero ignored-child traversal/read. |
| Repository | Repository aggregate and all-files pre-commit | All repository-static gates pass, except only the bounded Spec 039 FIFO portability DEFER when its conditions hold. |
| Review | Requirements review followed by fresh quality review per package and closure | Exact verdicts `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED` after remediation. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Worktree conversion changes historical bytes | Irreversible evidence corruption | Read and compare Git blobs; hash payload-to-EOF and preserve final-newline state. |
| Historical links are judged against current paths | False failures or silent rewrites | Resolve against source commit plus original path in a separate lane. |
| Production archive authority lands before its corpus | Strict classification failure or two archive roles | Keep ARWB-001 fixture-only; activate route/form/admission/predicates and retire Tombstones only with the complete ARWB-003 records/index/current-link cutover. |
| A secret-bearing blob is copied for completeness | Credential exposure | Block ordinary migration and route to approved secret-removal handling without printing payload. |
| Workspace validation reads private scratch | Local-state disclosure | Use Git index/ignore metadata only and test non-traversal in isolated fixtures. |
| Closure admits Spec 037 concurrently | Program-order violation | Require Spec 036 done before any Spec 037 Plan/Task pair exists. |

Rollback is newest-first before closure: revert ARWB-004 through ARWB-001 and
never remove the archive contract while migrated records consume it. After
ARWB-005, terminal records are not reopened individually. Build one atomic
reverse patch from closure through ARWB-001, validate the complete restored
Tombstone-compatible state, and create one rollback commit. If only historical
metadata is wrong, preserve payload and terminal state and use an explicitly
reviewed provenance correction instead of hiding the mismatch.

## Completion Criteria

- VAL-ARWB-001 through VAL-ARWB-007 have deterministic automated and reviewed
  repository evidence.
- Exactly 31 mirrored full-body archive records preserve their source blobs and
  all 202 historical links resolve in source context.
- The retired Tombstone profile/form is absent, archive routing is exact-one,
  and current navigation uses only the archive index.
- Payload mutation, reactivation, invalid reason dependency, provenance drift,
  and active direct archive links fail closed.
- `_workspace/README.md` is the only tracked workspace member and no validator
  reads ignored child content.
- Spec/Plan/Task, registry relation, indexes, and ledger form one exact staged
  closure proposal after full local QA. Fresh independent whole-tranche review
  returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED` with no findings;
  the closure commit remains uncreated and post-commit validation unclaimed.
  Spec 037 remains active, dependency-ready, and unplanned
  with no Plan or Task created or linked.
- Remote, provider, Kubernetes, Vault, ESO, Argo CD, secret, and ignored local
  state remain outside the evidence claim.

## Traceability

- **Spec**: [Archive Record and Workspace Boundary](../../03.specs/036-archive-record-and-workspace-boundary/spec.md)
- **Task**: [Archive Record and Workspace Boundary Task](../tasks/2026-07-17-archive-record-and-workspace-boundary.md)
- **PRD**: [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **ARD**: [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- **Decision**: [ADR-0018](../../02.architecture/decisions/0018-full-body-archive-record-and-retention.md)

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-ARWB-001](../../03.specs/036-archive-record-and-workspace-boundary/spec.md#success-criteria--verification-plan) | ARWB-001, ARWB-003 | [Recovery manifest and 31/31 source proof](../tasks/2026-07-17-archive-record-and-workspace-boundary.md#task-table) |
| N/A — VAL-ARWB-002 shares the Spec 036 source linked in VAL-ARWB-001 | ARWB-001, ARWB-002, ARWB-003 | N/A — the paired Task is linked in VAL-ARWB-001 |
| N/A — VAL-ARWB-003 shares the Spec 036 source linked in VAL-ARWB-001 | ARWB-002, ARWB-003 | N/A — the paired Task is linked in VAL-ARWB-001 |
| N/A — VAL-ARWB-004 shares the Spec 036 source linked in VAL-ARWB-001 | ARWB-001, ARWB-003 | N/A — the paired Task is linked in VAL-ARWB-001 |
| N/A — VAL-ARWB-005 shares the Spec 036 source linked in VAL-ARWB-001 | ARWB-002, ARWB-003 | N/A — the paired Task is linked in VAL-ARWB-001 |
| N/A — VAL-ARWB-006 shares the Spec 036 source linked in VAL-ARWB-001 | ARWB-004 | N/A — the paired Task is linked in VAL-ARWB-001 |
| N/A — VAL-ARWB-007 shares the Spec 036 source linked in VAL-ARWB-001 | ARWB-001, ARWB-002 | N/A — the paired Task is linked in VAL-ARWB-001 |

The canonical lifecycle table intentionally renders each reciprocal document
target once so the relationship evidence cardinality remains exact. The
criterion-level anchors below provide the complete navigation map without
turning repeated links into additional lifecycle evidence.

### Detailed Criterion Map

| Criterion anchor | Work packages |
| --- | --- |
| [VAL-ARWB-001](../../03.specs/036-archive-record-and-workspace-boundary/spec.md#success-criteria--verification-plan) | ARWB-001, ARWB-003 |
| [VAL-ARWB-002](../../03.specs/036-archive-record-and-workspace-boundary/spec.md#success-criteria--verification-plan) | ARWB-001, ARWB-002, ARWB-003 |
| [VAL-ARWB-003](../../03.specs/036-archive-record-and-workspace-boundary/spec.md#success-criteria--verification-plan) | ARWB-002, ARWB-003 |
| [VAL-ARWB-004](../../03.specs/036-archive-record-and-workspace-boundary/spec.md#success-criteria--verification-plan) | ARWB-001, ARWB-003 |
| [VAL-ARWB-005](../../03.specs/036-archive-record-and-workspace-boundary/spec.md#success-criteria--verification-plan) | ARWB-002, ARWB-003 |
| [VAL-ARWB-006](../../03.specs/036-archive-record-and-workspace-boundary/spec.md#success-criteria--verification-plan) | ARWB-004 |
| [VAL-ARWB-007](../../03.specs/036-archive-record-and-workspace-boundary/spec.md#success-criteria--verification-plan) | ARWB-001, ARWB-002 |
