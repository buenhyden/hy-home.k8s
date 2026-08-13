---
title: 'SDLC Document and AI Agent Governance Consolidation Implementation Plan'
type: sdlc/plan
status: active
owner: platform
updated: 2026-08-13
artifact_id: "PLAN-0054"
---

# SDLC Document and AI Agent Governance Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` to implement this plan task by
> task. Each task requires a fresh implementer, specification review,
> code-quality review, focused RED/GREEN evidence, and one logical commit.
> Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Converge the repository on the approved four-digit, work-unit-local
SDLC taxonomy, integrated AI-agent governance, reconciled operations and Stage
90 references, evidence-backed Stage 98 disposition, and consumer-safe 47-file
terminal script inventory.

**Architecture:** Active contracts are owned by Stage 00 rules and contracts,
the Stage 99 registry/schema/templates, and focused validators. Stage 03 keeps
Spec, Plan, and Tasks together. Stage 90 remains descriptive and
freshness-bounded; Stage 98 preserves historical disposition and recovery.
Every cutover is staged-index-aware, fail-closed, and committed as an
independently testable logical unit.

**Tech Stack:** Markdown, JSON/JSON Schema, Python 3 standard library, shell,
Git index/object APIs, unittest, pre-commit, and repository quality gates.

## Global Constraints

- Preserve Git history and unrelated user changes.
- Do not edit existing immutable Stage 98 envelopes or source blobs.
- Preserve Stage 90 audit/source evidence byte-for-byte unless its reviewed
  disposition authorizes a migration with recoverable provenance.
- Use four digits for every active numeric SDLC identity.
- Use `docs/05.operations/incidents/<year>/inc-####-<slug>/` exactly.
- Keep ordinary active filenames free of dates; retain dates in frontmatter or
  typed evidence metadata.
- Do not restore `docs/02.architecture/requirements/` or
  `docs/04.execution/` as active owners.
- Do not create `docs/05.operations/releases/` without a separately approved
  release-record contract.
- Resolve prose, template, registry, validator, fixture, README, hook, and
  aggregate rules in the same logical cutover.
- Delete a legacy, deprecated, duplicate, or one-time asset only after every
  current consumer is migrated and Stage 98 recovery evidence is valid.
- Treat repository-static, provider-runtime, hosted-CI, remote-live, and
  actual-evaluation evidence as distinct classes.
- Use `apply_patch` for edits, TDD for behavior changes, scoped staging, and
  conventional logical-unit commits.
- Do not perform push, merge, publication, live deployment, credential access,
  or provider-runtime mutation.

## Overview

This plan executes [Spec 0054](spec.md) and supersedes conflicting unfinished
instructions in [Spec 0052](../0052-document-taxonomy-consolidation/spec.md)
only where Spec 0054 explicitly owns the outcome. It starts from HEAD
`160ce006969ddb49965c8af193f3e9ee290e18a8` and an inherited, mixed WORK-109
candidate containing staged and unstaged edits. No inherited edit is accepted
solely because it is already staged.

The execution sequence first records a lossless candidate disposition, then
closes the active taxonomy before simplifying governance, operations,
references, archive evidence, and scripts. Deletions are deliberately late.

## Context

- Eight PRD paths and forty-nine Stage 03 work-unit paths are currently in a
  partial three-to-four-digit migration.
- Stage 04 paths are deleted in the candidate, while registry, fixtures,
  history validators, and reference prose still contain mixed Stage 04 rules.
- Architecture Description is already the intended Stage 02 form; current
  requirements vocabulary survives in historical and conflicting surfaces.
- The Incident registry candidate uses the approved lowercase four-digit
  route, while Stage 00, Stage 05, aggregate shell, and fixtures still contain
  uppercase three-digit variants.
- Stage 00 already approximates a canonical-core/provider-adapter model, but
  human projections, machine evidence, and native provider claims conflict.
- Stage 90 has dated audits, snapshots, one active dated research pack,
  generated projections, machine ledgers, and stale Stage 04 links.
- `scripts/` contains exactly fifty tracked assets. One compatibility wrapper
  and two taxonomy-transition assets have approved retirement gates, but none
  is safe to delete immediately.

## Goals & In-Scope

- Produce one exact active topology and one terminology map.
- Complete the current four-digit migration without losing path identity,
  cross-links, or recovery evidence.
- Make Stage 00, Stage 99, validators, and provider adapters agree.
- Make Stage 05 families purpose-disjoint and Incident-ready.
- Classify and reconcile every Stage 90 file.
- Record every removal or consolidation in Stage 98.
- Reduce the scripts inventory from fifty to forty-nine and finally
  forty-seven only when consumer-zero gates prove safety.
- Finish every work package with deterministic local evidence and an
  independent review.

## Non-Goals & Out-of-Scope

- Rewriting completed historical prose for current terminology.
- Editing sealed Stage 98 payloads to satisfy current rules.
- Creating a release document family without an actual release-record owner.
- Claiming provider discovery, authenticated execution, hosted CI, deployment,
  or live platform state from repository-static files.
- Combining validators merely because their filenames are similar.
- Cleaning unrelated application, GitOps, Kubernetes, or secret-management
  code.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Freeze approved authority and classify inherited WORK-109 edits | None | Human-approved Spec 0054 | Spec/Plan/Task commit plus exact candidate disposition |
| WP-002 | Complete four-digit topology, Stage 04 retirement, and Incident route | WP-001 | Candidate paths classified | Registry/Markdown/links/lifecycle GREEN; exact path map; migration evidence |
| WP-003 | Consolidate Stage 00 common governance and provider adapters | WP-002 | Active document routes stable | Canonical-owner and provider evidence validators GREEN |
| WP-004 | Reconcile Stage 99 templates and validator ownership | WP-003 | Governance owners stable | One profile/template/lifecycle/negative-fixture contract per family |
| WP-005 | Reconcile Stage 05 Guide/Policy/Runbook/Incident responsibilities | WP-004 | Template contract stable | Duplicate-owner audit and operations profile tests GREEN |
| WP-006 | Classify and reconcile every Stage 90 file | WP-005 | Active owners stable | Complete Stage 90 disposition, freshness, generator, and link evidence |
| WP-007 | Close Stage 98 migration and tombstone evidence | WP-006 | All current moves/deletions known | Migration/tombstone validator and recovery tests GREEN |
| WP-008 | Complete script ledger and retire `validate-harness.sh` | WP-007 | Exact fifty-script census | Consumer-zero proof and exact forty-nine-script census |
| WP-009 | Retire taxonomy transition assets | WP-008 | Terminal consumers moved to permanent contracts | Exact forty-seven-script census and recovery proof |
| WP-010 | Final convergence and branch completion | WP-009 | All logical commits present | Focused/affected/staged/aggregate/all-files/review GREEN |

### WP-001 — authority and inherited candidate disposition

**Files:**

- Create: `docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md`
- Create: `docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/plan.md`
- Create: `docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/tasks.md`
- Test: `tests/test_document_strict_cutover.py`
- Modify later in this package only if required for lineage:
  `docs/03.specs/0052-document-taxonomy-consolidation/{spec.md,plan.md,tasks.md}`

- [ ] Record the exact HEAD, branch, staged paths, unstaged paths, and rename-free
  A/D/M shape without changing the inherited candidate.
- [ ] Build a path disposition table assigning every inherited path to WP-002,
  WP-003, WP-004, or `discard-conflicting-candidate`.
- [ ] Add a focused test that rejects an inherited path absent from that exact
  disposition set.
- [ ] Run the test and confirm RED on the current unclassified candidate.
- [ ] Add the complete set and rerun for GREEN.
- [ ] Review the Spec for placeholders, contradictory topology, scope leakage,
  and ambiguous deletion authority.
- [ ] Commit only Spec 0054, Plan 0054, and Tasks 0054:
  `docs: define SDLC governance consolidation`.

### WP-002 — terminal topology and four-digit identity

**Files:**

- Modify: `docs/01.requirements/README.md` and eight PRD files.
- Modify: `docs/02.architecture/{README.md,decisions/README.md,decisions/0024-terminal-artifact-identity-and-archive-layout.md}`.
- Review and either accept or replace:
  `docs/02.architecture/decisions/0025-four-digit-document-path-identity.md`.
- Modify: `docs/03.specs/README.md` and every active Stage 03 work-unit path.
- Delete active Stage 04 indexes only after consumers are migrated:
  `docs/04.execution/{README.md,plans/README.md,tasks/README.md}`.
- Modify: `docs/99.templates/support/document-profiles.json` and schema.
- Modify: `scripts/document_contracts.py`,
  `scripts/validate-document-contract-registry.py`,
  `scripts/validate-document-lifecycle.py`,
  `scripts/validate-links-and-owners.py`, and affected fixtures/tests.
- Create: `docs/98.archive/migrations/mig-0002-sdlc-document-and-governance-consolidation.md`.

- [ ] Add RED tests for three-digit PRD/Spec paths, uppercase Incident paths,
  date-bearing active filenames, Stage 04 active owners, path/frontmatter ID
  mismatch, and a missing migration row.
- [ ] Run the focused strict-cutover, registry, lifecycle, and link tests and
  preserve their deterministic diagnostics.
- [ ] Apply the exact eight-PRD and forty-nine-work-unit path map; do not infer
  targets from mutable prose.
- [ ] Recompute every current cross-link from the path map and reject unknown
  source or target paths.
- [ ] Make the Incident route exactly
  `incidents/<year>/inc-####-<slug>/{incident.md,postmortem.md}` and derive
  `INC-<YYYY>-<DDDD>` and `POSTMORTEM-<YYYY>-<DDDD>`.
- [ ] Migrate Stage 04 current consumers to Stage 03 siblings while keeping
  immutable historical evidence resolvable through reviewed aliases.
- [ ] Run registry self/strict, Markdown self/strict, links self/strict,
  lifecycle self/staged, focused archive recovery, and `git diff --check`.
- [ ] Obtain Python and architecture review.
- [ ] Commit: `refactor(docs): normalize terminal SDLC routes`.

### WP-003 — integrated AI-agent governance

**Files:**

- Modify: `docs/00.agent-governance/{README.md,harness-catalog.md}`.
- Consolidate or retire:
  `common-governance.md`, `harness-implementation-map.md`, and
  `providers/agents-md.md`.
- Modify canonical rules, scopes, provider notes, contracts, schemas, hooks,
  and memory indexes under `docs/00.agent-governance/`.
- Modify thin gateways/adapters: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
  `.agents/**`, `.claude/**`, `.codex/**`, and `.gemini/**` only where the
  canonical contract requires a provider-native projection.
- Modify agent-governance validators and their exact fixtures/tests.

- [ ] Add RED cases for duplicate common policy, unsupported provider runtime
  claims, repository-static evidence promoted to runtime, missing canonical
  owners, divergent role semantics, and unbounded adapter instructions.
- [ ] Correct factual provider capability and hook claims against official
  provider documentation and observed evidence.
- [ ] Reduce root/provider files to thin native gateways; move shared semantics
  to one Stage 00 owner.
- [ ] Collapse repeated human matrices into one contract-derived catalog and
  route variable state to machine contracts.
- [ ] Archive or tombstone a legacy cutover control only after external
  consumers reach zero.
- [ ] Run every `validate-agent-*` self-test and production check, affected
  surface selection, aggregate governance lanes, and secret handling.
- [ ] Obtain architecture, security, and code-quality review.
- [ ] Commit: `refactor(governance): consolidate agent control plane`.

### WP-004 — Stage 99 template and contract convergence

**Files:**

- Modify: `docs/99.templates/{README.md,templates/README.md,support/README.md}`.
- Modify canonical support owners:
  `support/document-contract.md`, `support/document-lifecycle.md`,
  `support/document-profiles.json`, and its schema.
- Modify authored templates under `templates/sdlc/**` and common templates only
  where their profile contracts require it.
- Remove replaced support prose only after current links and hooks point to the
  canonical owners.

- [ ] Add RED tests proving every authored profile has exactly one template,
  route, frontmatter shape, status domain, heading contract, identity rule,
  lifecycle, and negative fixture set.
- [ ] Add template-instance tests for PRD, SRS, IFC, AD, ADR, Spec, Plan, Task,
  Guide, Policy, Runbook, Incident, and Postmortem.
- [ ] Make templates include every required `artifact_id` and Incident metadata
  field; keep dates out of filenames.
- [ ] Remove ARD, RFC, authored API-Spec, Stage 04, legacy routing, and duplicate
  support forms from active lookup surfaces while preserving native OpenAPI,
  GraphQL, and Protobuf contracts.
- [ ] Run registry self/strict, Markdown self/strict, lifecycle self/staged,
  template compatibility, and cross-link checks.
- [ ] Obtain documentation-contract and Python review.
- [ ] Commit: `refactor(templates): converge SDLC document contracts`.

### WP-005 — operations purpose and Incident readiness

**Files:**

- Modify: `docs/05.operations/{README.md,guides/README.md,policies/README.md,runbooks/README.md,incidents/README.md}`.
- Review all eight Guides, seven Policies, and nine Runbooks.
- Modify: Stage 05 templates, routes, validators, hooks, fixtures, and links.
- Create Stage 98 dispositions for any merged, replaced, or deleted Guide or
  Runbook.

- [ ] Add RED tests for an operation document with two canonical owners, a
  Guide containing privileged mutation ownership, a Runbook lacking trigger
  or recovery, and malformed Incident/Postmortem metadata.
- [ ] Record a complete Guide/Policy/Runbook responsibility ledger.
- [ ] Resolve the reviewed bootstrap, platform-expansion, observability,
  metrics, and GitOps-onboarding Guide/Runbook overlaps.
- [ ] Strengthen Incident role/timeline/severity/evidence fields and Postmortem
  cause/action-owner/due-state/closure fields.
- [ ] Prove that no Release family or placeholder release directory is added.
- [ ] Run operations profile, link, lifecycle, secret, and aggregate checks.
- [ ] Obtain operations and security review.
- [ ] Commit: `refactor(ops): clarify operations document ownership`.

### WP-006 — Stage 90 reference reconciliation

**Files:**

- Create: `docs/90.references/data/stage90-reference-disposition.json` and
  `docs/90.references/data/stage90-reference-disposition.schema.json`.
- Modify: `docs/90.references/**` current indexes and authorized current
  references according to the ledger.
- Modify: `scripts/reference_information_architecture.py`,
  `scripts/validate-reference-information-architecture.py`,
  `scripts/generate-llm-wiki-index.sh`, and focused tests when required by the
  new disposition contract.
- Create Stage 98 migration/tombstone evidence for every Stage 90 move, merge,
  replacement, or deletion.

- [ ] Enumerate every Stage 90 file with blob OID, profile, current owner,
  freshness trigger, consumers, and one closed disposition.
- [ ] Add RED tests for missing/duplicate disposition, a current reference
  claiming policy authority, a generated output without check mode, a stale
  Stage 04 link, and an altered historical source record.
- [ ] Convert maintained current references to semantic undated filenames and
  move observation dates into frontmatter/source metadata.
- [ ] Merge duplicate research findings into one current owner; preserve source
  coverage and source commits.
- [ ] Keep audit/snapshot/research-pack dates only where the ledger classifies
  the directory as typed historical evidence.
- [ ] Ensure generated indexes use canonical inputs, bounded reads, check mode,
  protected-output pins where transitional, and no write during check.
- [ ] Run the full RIA suite, generator check, links/owners, Markdown, archive
  recovery, and aggregate gates.
- [ ] Obtain documentation, architecture, and Python review.
- [ ] Commit: `refactor(references): reconcile Stage 90 ownership`.

### WP-007 — Stage 98 migration and tombstone closure

**Files:**

- Modify or create records under `docs/98.archive/migrations/` and
  `docs/98.archive/tombstones/` without changing sealed predecessor records.
- Modify archive registry, validation, recovery, cutover, and link tests only
  to enforce the approved new evidence contract.

- [ ] Add RED cases for duplicate artifact IDs, malformed stable IDs,
  path/frontmatter mismatch, missing source commits, missing replacement,
  orphan deletion, changed source blob, and active direct Archive-record links.
- [ ] Require the exact seven migration fields from Spec 0054 plus any existing
  stronger archive envelope fields.
- [ ] Join each current deletion/consolidation to exactly one migration or
  tombstone record and a recoverable source object.
- [ ] Preserve immutable archive record bytes and resolve current successor
  existence through narrow reviewed aliases only.
- [ ] Run archive validation, cutover, recovery, active-corpus retention, link,
  and aggregate gates.
- [ ] Obtain archive, security, and Python review.
- [ ] Commit: `feat(archive): record SDLC consolidation dispositions`.

### WP-008 — script ledger and forty-nine-file cutover

**Files:**

- Create: `docs/90.references/data/script-disposition.json` and
  `docs/90.references/data/script-disposition.schema.json`.
- Modify: `scripts/README.md`, validation-surface contracts, CI/pre-commit
  consumers, documentation, and fixtures.
- Delete after consumer-zero proof: `scripts/validate-harness.sh`.

- [ ] Add RED tests requiring one exact disposition for each of the fifty
  tracked assets and rejecting missing consumers, arguments, diagnostics,
  fixtures, evidence, recovery, or retirement gates.
- [ ] Record all fifty rows and verify the inventory digest.
- [ ] Migrate README, PR template, approval rule, fixture, CI, hook, and manual
  consumers from `validate-harness.sh` to canonical aggregate/affected lanes.
- [ ] Prove zero current consumers, delete only the wrapper, and assert exact
  forty-nine-file inventory.
- [ ] Run shell syntax, ShellCheck where configured, affected/staged lanes,
  aggregate, and pre-commit.
- [ ] Obtain script and code-quality review.
- [ ] Commit: `refactor(scripts): retire harness compatibility wrapper`.

### WP-009 — transition asset retirement and forty-seven-file cutover

**Files:**

- Migrate permanent consumers of
  `scripts/document-taxonomy-migration.json` and
  `scripts/migrate-document-work-units.py`.
- Modify registry, RIA, generator, residue, links, Markdown fixtures, tests,
  scripts README, and Stage 98 recovery evidence.
- Delete the transition JSON/tool and its transition-only test after closure.

- [ ] Add RED tests that list every remaining transition consumer and prevent
  retirement while one exists.
- [ ] Move terminal invariants to permanent registry, migration ledger, archive
  envelope, or frozen regression fixtures according to ownership.
- [ ] Prove current consumers zero and historical recovery from the source
  commit succeeds.
- [ ] Delete exactly the JSON and migration tool; remove only transition-only
  tests; assert exact forty-seven-file inventory.
- [ ] Run registry, migration/recovery, RIA, residue, Markdown, links,
  affected/staged, aggregate, and pre-commit gates.
- [ ] Obtain Python, archive, and code-quality review.
- [ ] Commit: `refactor(scripts): retire taxonomy transition assets`.

### WP-010 — convergence and branch completion

**Files:**

- Modify only final evidence fields in `tasks.md`, Stage 00 append-only
  progress, and generated indexes whose check-mode contract requires a final
  deterministic refresh.

- [ ] Run exact path, artifact-ID, active-date, direct-archive-link, Stage 04,
  Release-family, legacy/deprecated, and script-inventory audits.
- [ ] Run all focused suites named by WP-002 through WP-009.
- [ ] Run affected and staged validation with identical path input.
- [ ] Run aggregate quality, exact-index pre-commit, and all-files pre-commit to
  a byte-stable fixed point.
- [ ] Run secret-handling checks without printing candidate values.
- [ ] Obtain final architecture, operations, security, documentation, Python,
  and whole-branch code review; resolve all findings before proceeding.
- [ ] Update Task evidence and append-only progress without rewriting history.
- [ ] Commit: `docs: close SDLC governance consolidation`.
- [ ] Invoke `superpowers:finishing-a-development-branch` and present merge,
  PR, keep, or discard options without pushing or merging automatically.

## Verification Plan

Each work package runs its focused tests first, then the smallest relevant
production validator. WP-002, WP-003, WP-004, WP-006, WP-007, WP-008, and
WP-009 additionally run affected and staged lanes before commit. Aggregate and
pre-commit run at every deletion boundary and at final convergence.

The terminal minimum is:

```bash
python3 scripts/validate-document-contract-registry.py --self-test
python3 scripts/validate-document-contract-registry.py --mode strict --route-state transition
python3 scripts/validate-markdown-profiles.py . --self-test
python3 scripts/validate-markdown-profiles.py . --mode strict
python3 scripts/validate-links-and-owners.py . --self-test
python3 scripts/validate-links-and-owners.py . --mode strict
python3 scripts/validate-document-lifecycle.py --root . --self-test
python3 scripts/validate-document-lifecycle.py --root . --mode staged
TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
TMPDIR=/tmp pre-commit run
TMPDIR=/tmp pre-commit run --all-files
git diff --check
git diff --cached --check
```

Every PASS report records the candidate HEAD, staged-path digest, exit code,
finding count, mutation status, and evidence limitation.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Mixed inherited index/worktree makes a false-green candidate | Candidate disposition plus staged-index readers and exact restaging before every broad gate |
| Broad replacements alter historical or native terms | Exact path maps, profile-aware classification, protected blob checks, and focused negative fixtures |
| Stage 90 cleanup destroys provenance | Complete disposition ledger, source commits, byte pins, and Stage 98 migration before removal |
| Governance adapters drift from canonical semantics | Machine contract owns semantics; adapters carry native metadata only; parity tests cover all providers |
| Script deletion breaks hidden consumers | Complete consumer graph and zero-consumer negative gate before each deletion |
| Guide/Runbook consolidation removes necessary audiences | Purpose and trigger matrix reviewed by operations and documentation reviewers |
| Large validator files become harder to maintain | Limit this program to responsibility-preserving changes; schedule safe-I/O extraction only when required by touched code |
| Static validation is mistaken for live proof | Preserve separate evidence classes and explicit DEFER states |

## Completion Criteria

- The active topology matches C-SDLC-001 exactly.
- Every active numeric SDLC identity is four digits and path-equal to its
  artifact ID.
- Stage 04 and Stage 02 requirements have zero active owners or consumers.
- Incident/Postmortem routes, templates, identities, and fixtures agree.
- Stage 00 and provider adapters have one canonical owner per concern and no
  unsupported runtime promotion.
- Stage 99 profiles, templates, prose, hooks, validators, and fixtures agree.
- Stage 05 family responsibilities are disjoint and reviewed duplicates have
  one owner.
- Every Stage 90 file has one valid disposition and every authorized removal
  has Stage 98 evidence.
- The script inventory is exactly forty-seven after both consumer-zero gates.
- All required validation and independent review gates pass without mutation.
- Each logical work package is represented by its own commit.

## Traceability

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-SDLC-001](spec.md#success-criteria--verification-plan) | WP-001, WP-002 | [WORK-054-001, WORK-054-002](tasks.md#task-table) |
| [VAL-SDLC-002](spec.md#success-criteria--verification-plan) | WP-002 | [WORK-054-002](tasks.md#task-table) |
| [VAL-SDLC-003](spec.md#success-criteria--verification-plan) | WP-002, WP-005 | [WORK-054-002, WORK-054-005](tasks.md#task-table) |
| [VAL-SDLC-004](spec.md#success-criteria--verification-plan) | WP-002, WP-004 | [WORK-054-002, WORK-054-004](tasks.md#task-table) |
| [VAL-SDLC-005](spec.md#success-criteria--verification-plan) | WP-003 | [WORK-054-003](tasks.md#task-table) |
| [VAL-SDLC-006](spec.md#success-criteria--verification-plan) | WP-004 | [WORK-054-004](tasks.md#task-table) |
| [VAL-SDLC-007](spec.md#success-criteria--verification-plan) | WP-005 | [WORK-054-005](tasks.md#task-table) |
| [VAL-SDLC-008](spec.md#success-criteria--verification-plan) | WP-006 | [WORK-054-006](tasks.md#task-table) |
| [VAL-SDLC-009](spec.md#success-criteria--verification-plan) | WP-007 | [WORK-054-007](tasks.md#task-table) |
| [VAL-SDLC-010](spec.md#success-criteria--verification-plan) | WP-008, WP-009 | [WORK-054-008, WORK-054-009](tasks.md#task-table) |
| [VAL-SDLC-011](spec.md#success-criteria--verification-plan) | WP-002..WP-010 | [WORK-054-002..WORK-054-010](tasks.md#task-table) |
| [VAL-SDLC-012](spec.md#success-criteria--verification-plan) | WP-001..WP-010 | [WORK-054-001..WORK-054-010](tasks.md#task-table) |
