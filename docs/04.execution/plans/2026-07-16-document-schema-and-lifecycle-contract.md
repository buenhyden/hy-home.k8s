---
title: 'Document Schema and Lifecycle Contract Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-17
---

# Document Schema and Lifecycle Contract Implementation Plan

## Overview

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Use
> test-first RED/GREEN work, independent requirements and quality review, and
> one logical commit per work package.

**Goal:** Close [Spec 035](../../03.specs/035-document-schema-and-lifecycle-contract/spec.md)
with one closed registry-owned value, lifecycle, evidence, role, template, and
native-surface compatibility contract plus deterministic base-to-proposed
validation.

**Architecture:** Registry v7 adds closed value constraints, role decisions,
transition graphs, and edge-specific evidence predicates to the existing route
and body contracts. The typed loader exposes immutable projections. A separate
lifecycle comparison interface reads the Git index or named refs without
confusing the worktree with the proposed snapshot. Existing validators consume
that interface and preserve their current diagnostics; lifecycle failures use
a dedicated stable diagnostic tuple.

**Tech Stack:** Markdown, YAML frontmatter, JSON Schema 2020-12, JSON, Python 3,
Git plumbing, repository Markdown parsers, pre-commit, and Git.

## Context

Registry v6 classifies 430 governed paths through 64 profiles and 30 canonical
templates with zero uncovered or ambiguous paths. It owns frontmatter keysets,
key order, status domains, headings, body contracts, sources, current owners,
and program lineage. The current Markdown validator checks key presence, order,
basic scalar type, status membership, title, owner, date, and placeholders, but
it cannot express per-key enum, constant, pattern, null, or conditional rules.
It validates only a current snapshot and cannot distinguish an allowed status
from an allowed state change.

The design audit also found these bounded drifts:

- registry schema/data and the typed loader have no lifecycle graph, evidence
  predicate, admission policy, or machine-readable role decision;
- new Tombstones are still admitted even though the 31 existing records are
  only a migration compatibility surface for Spec 036;
- normal template parity compares the derived contract tuple, but mutation
  coverage does not independently prove every tuple field and source
  cardinality;
- native routes are classified, but fixtures do not prove that valid native
  forms remain frontmatter-free or reject a leading SDLC frontmatter block;
- Stage 99 support documents still describe registry v5, Stage 00 universally
  demands `## Related Documents` instead of the selected profile relationship
  section, `tests/README.md` publishes stale counts, and the Incident README
  assigns postmortem analysis to the live-fact document;
- the repository has no GraphQL or protobuf syntax toolchain. Spec 035 proves
  the frontmatter-free routing boundary and uses already available native
  validators; Spec 039 owns CI/toolchain expansion and FIFO portability.

### Approved lifecycle model

A missing status change is not an edge. The v7 registry declares only forward
current-document edges; terminal reopening and every transition into or out of
`archived` are absent and therefore rejected. Spec 036 must add its archive
edge and evidence predicate atomically with the full-body archive route.

| Family | Profiles | Declared edges | Terminal state |
| --- | --- | --- | --- |
| Product | `sdlc/prd` | `draft -> active`, `active -> done` | `done` |
| Architecture and decision | `sdlc/ard`, `sdlc/adr` | `draft -> active`, `active -> accepted` | `accepted` |
| Specification and helper | `sdlc/spec`, `sdlc/api-spec`, `sdlc/agent-design`, `sdlc/data-model`, `sdlc/tests` | `draft -> active`, `active -> done` | `done` |
| Execution | `sdlc/plan`, `sdlc/task` | `draft -> active`, `active -> done` | `done` |
| Operations | `sdlc/guide`, `sdlc/policy`, `sdlc/runbook`, `sdlc/incident`, `sdlc/postmortem` | `draft -> active`, `active -> accepted` | `accepted` |
| Reference and governance | `content/reference`, `governance/reference`, `governance/memory`, `governance/template-support` | `draft -> active`, `active -> accepted`, `active -> done` | edge-selected `accepted` or `done` |
| Tombstone compatibility | `content/archive-tombstone` | none | snapshot-only `archived` |

### Creation and movement admission

The loader exposes a closed `admission` object for every profile. Omitted
operations deny; a future route cannot inherit permissive defaults.

| Profile mode or family | Create states | Delete | Rename | Same-path profile change |
| --- | --- | --- | --- | --- |
| Authored except execution and Tombstone | `draft` only | Deny | Deny | Deny |
| `sdlc/plan` plus `sdlc/task` | Both files `draft`, or both files `active`, in one reciprocal direct-Spec pair | Deny | Deny | Deny |
| Existing `content/archive-tombstone` | None; exact 31-path baseline is read-only | Deny | Deny, including copies | Deny |
| Template, frontmatter-free, classification-only, generated, and non-target | Route/profile snapshot validation; no lifecycle status admission | Deny by lifecycle engine | Deny by lifecycle engine | Deny |

Exact-blob renames use Git's 100-percent rename detection. A rename with any
content change is deterministically a delete plus create, and therefore also
fails. Spec 036 must add its destination route, archive creation predicate,
source deletion predicate, and index evidence atomically. Spec 037 may consume
that interface for eligible execution movement but cannot weaken the default.

### Closed transition evidence predicates

The production graph contains the following predicate IDs. `$self` means the
proposed document selected by the edge. `$relationship` is a closed field of
the profile's role decision: it resolves to `bodyContract.section` when a body
contract exists, otherwise to exactly one named required heading. The four
null-body profiles resolve respectively to `Related Documents` for
`content/reference`, `governance/reference`, and
`governance/template-support`, and `Related Progress` for
`governance/memory`. `pair` means exactly one reciprocal Plan and one
reciprocal Task with direct links to the same governed target. Every listed
state is a proposed-snapshot state.

| Predicate ID | Exact profile edges | Evidence profile and state | Relationship and cardinality | Same-diff and body requirement |
| --- | --- | --- | --- | --- |
| `activate-self-body` | `draft -> active` for PRD, ARD, ADR, Spec/helper, and operations profiles with non-null body contracts | `$self@active` | `$self` exactly one; `$relationship` satisfies the body contract's declared link columns | Self status and body change; selected body contract enforced at `active` |
| `activate-heading-profile` | `draft -> active` for the four reference/governance profiles with null body contracts | `$self@active` | `$self` exactly one; exact role-decision `$relationship` heading contains at least one rendered repository-local link | Self status and body change; required/allowed heading set enforced, with no fabricated body contract |
| `activate-execution-pair` | `draft -> active` for Plan and Task; also active-pair creation | `sdlc/plan@active` plus `sdlc/task@active` | `pair` exactly two documents, reciprocal, both direct to one dependency-ready Spec through `Traceability` | Both created or both status-changed in the diff; both selected body contracts enforced |
| `complete-product-program` | PRD `active -> done` | Exact registry-declared tranche/follow-up Spec set at relation state `done` | PRD `Traceability` resolves every declared Spec; no extra current execution component | PRD and the last unfinished relation change in the diff; named `program-lineage-closed` capability plus PRD body contract |
| `accept-architecture` | ARD `active -> accepted` | One or more linked `sdlc/adr@accepted` | Every evidence ADR is linked from ARD `Traceability` and links back; minimum one, no ambiguous duplicate target | ARD and at least one evidence ADR status/body change; ARD and ADR body contracts enforced |
| `accept-decision-self` | ADR `active -> accepted` | `$self@accepted` | Exactly one self; `Decision` heading and `$relationship` links to its ARD or affected Spec | Self status and Decision body change; ADR heading and body contracts enforced |
| `complete-specification` | Spec and helper `active -> done` | `sdlc/plan@done` plus `sdlc/task@done` | `pair` exactly two, reciprocal and direct to `$self` through `Traceability` | Spec, Plan, and Task statuses change together; all three selected body contracts enforced |
| `complete-execution-pair` | Plan and Task `active -> done` | `sdlc/plan@done` plus `sdlc/task@done` | `pair` exactly two, reciprocal and direct to the same Spec | Both statuses change together; Task rows are terminal with non-placeholder result/evidence and both body contracts are enforced |
| `accept-operated-document` | Guide, Policy, Runbook, Incident, and Postmortem `active -> accepted` | One done execution `pair`; its Task links directly to `$self` | Exactly one pair; target document links the Task through its existing `$relationship` body-contract column | Target and pair statuses change in the diff; target and pair body contracts enforced; no Incident/Postmortem reciprocal relation is invented |
| `terminate-reviewed-reference` | Reference/governance `active -> accepted` or `active -> done` | One done execution `pair`; its Task links directly to `$self` | Exactly one pair; target links the Task through the exact role-decision `$relationship` heading | Target and pair statuses change in the diff; target required/allowed heading set and pair body contracts enforced, with target body contract explicitly null |

Predicate data contains only closed enums, profile/state sets, cardinality,
same-diff mode, relationship selector, body-requirement mode (`body-contract`
or `heading-set`), and named validator capabilities.
Arbitrary expressions and executable snippets are forbidden. Registry
self-tests derive the production `edge x {positive, missing, wrong-profile,
wrong-state, wrong-section, unchanged, ambiguous-base}` matrix and fail when
any declared edge lacks a case; grouping only by predicate family is
insufficient.

### Deterministic comparison modes

| Mode | Base | Proposed | Transition result |
| --- | --- | --- | --- |
| `staged` | `HEAD` tree | Git index blobs | Evaluated |
| `ci` | merge base of explicit base ref and proposed head | proposed head tree | Evaluated |
| `explicit-ref` | named `from-ref` tree | named `to-ref` tree | Evaluated |
| `snapshot` | unavailable | current filesystem | `DEFER`, while current-state validation still runs |

The public module is `scripts/document_lifecycle.py`; the CLI is
`scripts/validate-document-lifecycle.py`; isolated cases live in
`tests/fixtures/document-lifecycle.json`.

The CLI accepts `--root`, `--mode {staged,ci,explicit-ref,snapshot}`,
`--from-ref`, `--base-ref`, `--to-ref`, `--include-path`, and `--self-test`.
`staged` forbids ref flags and compares `HEAD:path` with `:path`. `ci` requires
`--base-ref` and `--to-ref`, computes `git merge-base <base-ref> <to-ref>`, and
uses the resulting tree against `<to-ref>`; no implicit environment variable
selects a ref. `explicit-ref` requires only `--from-ref` and `--to-ref`.
`snapshot` forbids refs and validates filesystem state while emitting exactly
one summary DEFER for transition history. Missing, ambiguous, non-commit, or
non-tree refs fail closed as invocation/provenance errors.

Exit `0` means no contract failure; snapshot DEFER is exit `0` but is never
rendered as PASS. Exit `1` means a lifecycle contract violation. Exit `2`
means invalid arguments, inaccessible refs, ambiguous base, or Git provenance
failure. `LifecycleDiagnostic` has severity, rule ID, path, profile, expected
transition, observed transition, base mode, and evidence gap. Stable rule IDs
are `LIFECYCLE-CREATE`, `LIFECYCLE-DELETE`, `LIFECYCLE-RENAME`,
`LIFECYCLE-PROFILE-CHANGE`, `LIFECYCLE-STATE`, `LIFECYCLE-EDGE`,
`LIFECYCLE-EVIDENCE`, `LIFECYCLE-BASE`, and `LIFECYCLE-BASE-DEFER`; an adapter
preserves existing validator diagnostic envelopes.

Staged mode never reads a changed worktree blob as the proposal. Exact
100-percent renames are identified before profile selection; every other
delete/add pair stays separate. Snapshot/all-files reports transition history
as DEFER instead of silently passing or failing all current documents.

### File and interface map

| Unit | Exact owners | Responsibility |
| --- | --- | --- |
| Registry schema/data | `docs/99.templates/support/document-profiles.schema.json`, `docs/99.templates/support/document-profiles.json` | Own v7 value, role, lifecycle, predicate, source, and compatibility declarations. |
| Typed projection | `scripts/document_contracts.py` | Parse closed v7 objects once and expose immutable value/lifecycle/role contracts. |
| Registry proof | `scripts/validate-document-contract-registry.py`, `tests/fixtures/document-contracts/registry-cases.json` | Reject malformed v7 data and prove isolated v6 migration only in self-tests. |
| Metadata and template proof | `scripts/validate-markdown-profiles.py`, document-contract and Markdown fixtures | Enforce value constraints, source parity, compatibility admission, and current corpus shape. |
| Lifecycle comparison | `scripts/document_lifecycle.py`, `scripts/validate-document-lifecycle.py`, `tests/fixtures/document-lifecycle.json` | Resolve Git snapshots, compare statuses, and return stable lifecycle diagnostics. |
| Cross-document evidence | `scripts/validate-links-and-owners.py` plus lifecycle fixtures | Resolve relationship evidence, profiles, states, same-diff changes, and body contracts. |
| Stage 00/99 summaries | named support, routing, hook, README, and research consumers | Remove stale versions and role claims without copying the registry inventory. |
| Execution evidence | This Plan, its paired Task, Stage 04 indexes, Spec 035, and the migration ledger | Preserve authorization, review, results, and rollback boundaries. |

## Goals & In-Scope

- Upgrade production from registry v6 to one closed v7 value/lifecycle/role
  schema; production rejects v6 while a private self-test migration fixture
  proves the explicit version boundary.
- Keep ordinary authored Markdown on exactly five ordered keys and add no
  consumer-free relationship frontmatter.
- Enforce key value kinds, constants/enums, patterns, nullability, conditionals,
  status domains, and template-placeholder exceptions from the selected
  profile.
- Declare creation/movement admission, forward lifecycle edges, and the exact
  closed evidence predicate for every edge listed above; reject undeclared
  create/delete/rename/profile-change, reverse, skip, terminal reopen, and
  archived transitions.
- Add staged, CI, explicit-ref, and snapshot comparison modes with exact blob
  provenance and stable diagnostics.
- Make the 31 Tombstones readable only as pinned baseline compatibility and
  reject any newly added Tombstone before Spec 036.
- Prove canonical source/template parity, one reviewed role/source decision per
  governed family and README profile, and operations/helper overlap rejection.
- Prove native forms stay frontmatter-free without replacing native syntax
  owners or inventing partial GraphQL/protobuf parsers.
- Correct only the directly implicated Stage 00/99 support, hook text, tests
  inventory, research source pointer, Runbook prompt, and Incident README.
- Close Spec 035 and its Plan/Task atomically after full repository-static QA
  and independent requirements and quality review.

## Non-Goals & Out-of-Scope

- Creating `content/archive`, an archive envelope, or archive reason/replacement
  values; converting or deleting 31 Tombstones; moving any source into Stage 98.
- Bulk-rewriting the 24 current operations documents or the completed helper
  agent-design document; Spec 037 owns semantic corpus consolidation and
  completed Plan/Task retention.
- Editing generated, accepted, done, archived, dated-snapshot, or historical
  bodies to manufacture new evidence.
- Adding arbitrary metadata keys, embedded rule code, or a second machine
  registry.
- Implementing full OpenAPI/GraphQL/protobuf lint toolchains, GitHub workflow
  redesign, aggregate CI, artifact retention, or FIFO portability; Spec 039
  owns those changes.
- Live Kubernetes, Vault, ESO, Argo CD, provider runtime, GitHub settings,
  publication, push, or secret access.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| DSLC-001 | Add registry v7 value, role, lifecycle, evidence, and compatibility schema | Approved Spec 035 and reciprocal active Plan/Task | RED registry mutations for every new closed field and v6 production rejection | v7 schema/data, typed projection, exhaustive registry cases, strict load, logical commit, independent review |
| DSLC-002 | Enforce metadata values, template/source parity, and baseline-only Tombstone admission | DSLC-001 | RED value/order/conditional/parity/admission fixtures | Full mutation matrix, current-corpus PASS, no new Tombstone admission, logical commit, independent review |
| DSLC-003 | Implement deterministic base snapshots and transition graph validation | DSLC-002 | RED staged/index, CI merge-base, explicit-ref, snapshot-DEFER, and illegal-edge fixtures | Exact-blob comparison interface, stable lifecycle diagnostics, current snapshot PASS/DEFER, logical commit, independent review |
| DSLC-004 | Enforce edge-specific evidence predicates | DSLC-003 | RED positive/missing/wrong-profile/wrong-state/wrong-section/unchanged/ambiguous fixtures per predicate family | Closed predicate resolution, same-diff evidence, body-contract proof, logical commit, independent review |
| DSLC-005 | Close native, role/source, support, and directly implicated consumer drift | DSLC-004 | RED native-frontmatter and role-overlap fixtures plus exact drift inventory | Native boundary proof, registry-derived relationship wording, v7 support docs, corrected Incident/tests/research consumers, no bulk corpus rewrite, logical commit, independent review |
| DSLC-006 | Run full QA and close the tranche atomically | DSLC-005 | All package reviews approved and no unresolved Spec 035 defect | Done Spec/Plan/Task and registry relation, indexes/ledger aligned, full static command matrix, whole-tranche reviews, rollback boundary |

### DSLC-001: Registry v7 contract

**Files:**

- Modify `docs/99.templates/support/document-profiles.schema.json`
- Modify `docs/99.templates/support/document-profiles.json`
- Modify `scripts/document_contracts.py`
- Modify `scripts/validate-document-contract-registry.py`
- Modify `tests/fixtures/document-contracts/registry-cases.json`
- Modify `scripts/README.md`
- Update the paired Task

- [x] Add RED schema and semantic mutations for unknown fields, missing fields,
  invalid kind/enum/constant/pattern/null/conditional data, duplicate edges,
  invalid states, terminal outgoing edges, archived edges, unknown evidence
  profiles/states, executable predicates, invalid role decisions, creation,
  deletion, rename, same-path profile change, and new Tombstone admission.
- [x] Upgrade the production schema/data to v7 and reject v6 in production.
- [x] Add typed immutable value, role, lifecycle, edge, and evidence projection.
- [x] Keep any v6 converter private to self-test code and assert the exact v7
  production projection rather than comparing production data with itself.
- [x] Run strict registry and current profile validation, request requirements
  and quality review, remediate, and commit DSLC-001.

### DSLC-002: Metadata, template, and compatibility enforcement

**Files:**

- Modify `scripts/validate-markdown-profiles.py`
- Modify relevant document-contract and Markdown fixture files
- Modify canonical forms only where the v7 source tuple requires it
- Update the paired Task

- [x] Add RED fixtures for unsupported keys, order, scalar kind, enum, constant,
  pattern, null, conditional value, owner/title/date, and placeholder policy.
- [x] Add independent template drift fixtures for frontmatter, order, status,
  headings, class, body contract, source cardinality, missing source, duplicate
  source, and unknown source.
- [x] Pin the 31 tracked Tombstone paths as readable compatibility and reject an
  added or renamed Tombstone independently of worktree noise.
- [x] Implement registry-derived validation without hard-coded type inventories.
- [x] Run strict current-corpus validation, review, and commit DSLC-002.

### DSLC-003: Base and transition engine

**Files:**

- Add or modify a focused lifecycle module under `scripts/`
- Modify `scripts/validate-markdown-profiles.py` only for stable integration
- Add `scripts/document_lifecycle.py`
- Add `scripts/validate-document-lifecycle.py`
- Add `tests/fixtures/document-lifecycle.json`
- Modify `scripts/README.md`
- Update the paired Task

- [x] Write RED fixtures proving that staged mode reads `HEAD:path` versus
  `:path`, ignores an unstaged worktree edit, and handles add/delete/rename
  without guessing identity.
- [x] Write RED CI merge-base and explicit-ref fixtures for exact CLI flags,
  resolvable refs, missing/ambiguous/non-commit refs, invalid flag
  combinations, exit `0/1/2`, and snapshot-only DEFER output.
- [x] Write RED lifecycle fixtures for each forward edge, skipped edge, reverse
  edge, terminal reopen, archive reactivation, cross-profile move, and
  snapshot `DEFER`.
- [x] Implement one comparison interface and a lifecycle-specific diagnostic
  result without breaking existing diagnostic consumers.
- [x] Run current snapshot validation, isolated Git fixtures, review, and commit
  DSLC-003.

### DSLC-004: Transition evidence

**Files:**

- Modify the lifecycle module and `scripts/validate-links-and-owners.py`
- Add or modify focused link/lifecycle fixtures
- Update `scripts/README.md` and the paired Task

- [x] Derive and run positive and negative fixtures for every production edge,
  not only every predicate family: missing,
  wrong profile, wrong state, wrong relationship section, unchanged evidence,
  ambiguous base, body-contract mismatch, plain-text path, and opaque Markdown.
- [x] Resolve evidence through selected profiles and rendered links, reuse the
  existing CommonMark-aware extractor, and avoid a second Markdown parser.
- [x] Require same-diff evidence from the proposed snapshot and reject orphan
  or multiply matching evidence deterministically.
- [x] Preserve Plan/Task atomic-pair and program-lineage admission checks from
  Spec 034.
- [x] Run strict link/owner, lifecycle, and current-corpus validation, review,
  and commit DSLC-004.

### DSLC-005: Native, role, and support drift

**Files:**

- Modify Stage 99 support documents that name the registry version
- Modify `docs/00.agent-governance/rules/stage-authoring-matrix.md`,
  `docs/00.agent-governance/rules/postflight-checklist.md`, and
  `docs/00.agent-governance/hooks/k8s-pre-edit.sh`
- Modify the canonical Runbook prompt if the role audit confirms the drift
- Modify `docs/05.operations/incidents/README.md`
- Modify `tests/README.md`, the affected research ledger/pointer, and validators
  or fixtures needed for native and role proof
- Update the paired Task

- [x] Add frontmatter-free native-shaped issue/workflow/OpenAPI/GraphQL/protobuf
  route fixtures and a leading-SDLC-frontmatter negative fixture for each
  governed native family. Run `check-yaml`, the repository GitHub workflow
  validator, `actionlint`, and `zizmor` where they are authoritative and
  available; record OpenAPI, GraphQL, and protobuf syntax validation as Spec
  039 DEFER when no repository tool exists.
- [x] Add role/source overlap mutations for Guide versus Runbook, Policy versus
  Runbook, Incident versus Postmortem, and helper Tests versus execution Task.
- [x] Replace the four active universal `## Related Documents` requirements
  across the Stage 00 authoring matrix, postflight R3 checklist, and pre-edit
  hook with the relationship section selected by the registry profile; do not
  rewrite historical memory entries. Update v5 references to v7, correct
  current test counts from validator output, repair the removed template-source
  pointer, and keep support rationale free of an exact duplicated inventory.
- [x] Remove postmortem hypothesis/root-cause ownership from the Incident README
  and make the Runbook prompt role-based rather than a closed topic list.
- [x] Record the 24-document operations semantic review as a Spec 037 input; do
  not rewrite that corpus in this package.
- [x] Run focused and full static validation, review, and commit DSLC-005.

### DSLC-006: Closure

**Files:**

- Modify Spec 035, this Plan, its Task, Stage 03/04 indexes, the program
  relation state, and migration ledger rows in one closure commit

- [x] Prepare the exact atomic proposal that sets Spec/Plan/Task and the Spec
  035 registry relation to done, updates indexes and ledger rows, and records
  Spec 036 as dependency-ready with zero Plan/Task.
- [x] Stage exactly the eight closure files and pass staged lifecycle, registry
  121, lifecycle 651, strict Markdown/profile, and cross-document validation.
- [x] Complete repository-quality aggregate, YAML, GitHub security, actionlint,
  and zizmor validation with PASS results.
- [x] Run `pre-commit run --all-files`; retain the isolated filesystem's sole
  `os.mkfifo` `Errno 95` failure as Spec 039 portability scope after every
  other hook passes.
- [x] Complete independent requirements review, correct all three stale ledger
  boundaries to `b3fd537`, and obtain `REQUIREMENTS COMPLIANT` on re-review;
  remediate the subsequent evidence, fixture-wording, and successor-set quality
  findings and obtain `QUALITY APPROVED` on re-review.
- [x] Record rollback parent `b3fd537`, the completed package range, and the
  required post-commit strict/snapshot/clean-tree checks without inventing the
  not-yet-created closure commit hash.

## Verification Plan

| Lane | Commands or fixture contract | Required result |
| --- | --- | --- |
| Registry | `python3 scripts/validate-document-contract-registry.py --root . --self-test` and strict mode | All v7 mutations pass; production v6 fails; current registry projection exact |
| Markdown profiles | `python3 scripts/validate-markdown-profiles.py --root . --self-test` and strict mode | Value, order, conditional, template, Tombstone, native, and current corpus checks pass |
| Lifecycle | Focused lifecycle self-test in the selected module | All graph, base-mode, evidence, add/delete/rename, and DEFER fixtures pass |
| Cross-document | `python3 scripts/validate-links-and-owners.py --root . --self-test` and strict mode | Evidence, role, Plan/Task, owner, and program lineage checks pass |
| Native | `check-yaml`, repository workflow validator, `actionlint`, `zizmor`, and isolated native-shaped routing fixtures | GitHub YAML/workflow checks pass; OpenAPI/GraphQL/protobuf syntax remains explicit Spec 039 DEFER where tooling is absent |
| Repository | `bash scripts/validate-repo-quality-gates.sh .` | All repository-static gates pass |
| Pre-commit | `pre-commit run --all-files` | Pass, except the already bounded Spec 039 FIFO portability DEFER if independently reproduced |
| Review | Independent requirements review, then independent quality review for every package and closure | `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED` after remediation |

## Risks & Mitigations

- **False historical PASS:** snapshot mode could imply transitions were checked.
  It emits an explicit transition `DEFER` while retaining current-state PASS.
- **Wrong staged proposal:** a validator could read the worktree instead of the
  index. Isolated fixtures create three different HEAD/index/worktree blobs and
  assert exact provenance.
- **Archive scope collision:** a generic schema capability could accidentally
  create the Spec 036 route. Registry v7 adds no `content/archive` profile or
  archive transition; baseline-only Tombstone admission is separately tested.
- **Corpus rewrite collision:** role findings could trigger bulk operations
  edits. DSLC-005 changes only direct contract consumers and records the rest
  for Spec 037.
- **Parser divergence:** evidence validation could add another Markdown parser.
  DSLC-004 reuses the existing rendered-link/body-contract interfaces.
- **Diagnostic compatibility:** changing the general diagnostic shape could
  break callers. Lifecycle results use a focused typed record and adapter.
- **Tooling overclaim:** OpenAPI/GraphQL/protobuf syntax tools are absent. Only
  native-shaped route and leading-frontmatter fixtures are required; their
  syntax lane is explicit DEFER and toolchain installation remains Spec 039.

Before DSLC-006 closes the lineage, rollback is package-ordered: revert the
newest open package first and never remove v7 schema/data before its consumers.
After DSLC-006, a partial closure revert is forbidden because `done -> active`
is a terminal reopen. The executable full rollback is one atomic uncommitted
reverse patch: apply DSLC-006, DSLC-005, DSLC-004, DSLC-003, DSLC-002, and
DSLC-001 newest-to-oldest with `git revert --no-commit`; do not validate or
commit an intermediate state. Once the lifecycle engine and v7 consumers have
been removed and the v6 schema/data plus active Spec/Plan/Task state are staged
together, run the v6 strict gates and commit that one rollback. If only closure
evidence is wrong, preserve terminal records and create a successor correction
instead of reopening them. Each Task row records its commit and parent.

## Completion Criteria

- VAL-DSLC-001 through VAL-DSLC-008 have deterministic repository evidence.
- Production loads only closed registry v7 and every governed path still
  selects exactly one profile.
- Current metadata, template/source parity, lifecycle, evidence, role, and
  native boundary checks pass without a second registry or copied inventory.
- Existing Tombstones remain readable, new Tombstones fail, and Spec 036 scope
  remains unimplemented.
- Operations/helper bulk consolidation and execution retention remain explicit
  Spec 037 inputs; CI/FIFO work remains an explicit Spec 039 input.
- Spec 035, this Plan, its Task, registry relation, indexes, and migration
  ledger form one atomic closure. The staged change has passed lifecycle and
  independent requirements/quality review; the closure commit remains, while
  post-commit strict/snapshot verification must confirm the committed state.
- Static results make no remote, provider-runtime, Kubernetes, Vault, ESO,
  Argo CD, or secret-readiness claim.

## Traceability

- **Spec**: [Spec 035](../../03.specs/035-document-schema-and-lifecycle-contract/spec.md)
- **Task**: [Execution Task](../tasks/2026-07-16-document-schema-and-lifecycle-contract.md)
- **PRD**: [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **ARD**: [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- **Predecessor**: [Completed Spec 034 Plan](./2026-07-15-authority-and-lineage-foundation.md)
- **Successor boundary**: Specs 036, 037, 038, 039, and 040 are the remaining
  original active tranches in the PRD-006 registry lineage. Spec 036 is the
  dependency-ready successor and has no Plan or Task.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-DSLC-001](../../03.specs/035-document-schema-and-lifecycle-contract/spec.md#success-criteria--verification-plan) | DSLC-001, DSLC-002 | [DSLC-001 and DSLC-002 registry/profile evidence](../tasks/2026-07-16-document-schema-and-lifecycle-contract.md#task-table) |
| N/A — VAL-DSLC-002 shares the Spec 035 source linked in VAL-DSLC-001 | DSLC-001, DSLC-002 | N/A — the paired Task is linked in VAL-DSLC-001 |
| N/A — VAL-DSLC-003 shares the Spec 035 source linked in VAL-DSLC-001 | DSLC-001, DSLC-003 | N/A — the paired Task is linked in VAL-DSLC-001 |
| N/A — VAL-DSLC-004 shares the Spec 035 source linked in VAL-DSLC-001 | DSLC-003, DSLC-004 | N/A — the paired Task is linked in VAL-DSLC-001 |
| N/A — VAL-DSLC-005 shares the Spec 035 source linked in VAL-DSLC-001 | DSLC-002, DSLC-005 | N/A — the paired Task is linked in VAL-DSLC-001 |
| N/A — VAL-DSLC-006 shares the Spec 035 source linked in VAL-DSLC-001 | DSLC-005 | N/A — the paired Task is linked in VAL-DSLC-001 |
| N/A — VAL-DSLC-007 shares the Spec 035 source linked in VAL-DSLC-001 | DSLC-001, DSLC-005 | N/A — the paired Task is linked in VAL-DSLC-001 |
| N/A — VAL-DSLC-008 shares the Spec 035 source linked in VAL-DSLC-001 | DSLC-001, DSLC-003, DSLC-004 | N/A — the paired Task is linked in VAL-DSLC-001 |
