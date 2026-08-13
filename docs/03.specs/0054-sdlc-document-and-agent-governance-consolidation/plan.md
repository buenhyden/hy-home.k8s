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
- Do not restore retired `docs/02.architecture/requirements/` or
  `docs/04.execution/` routes; Stage 01/AD and Stage 03 siblings are their
  current replacement owners.
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
instructions in predecessor Spec 0052
only where Spec 0054 explicitly owns the outcome. It starts from the Git parent
of the WP-001 design-authority commit and an inherited, mixed WORK-109 candidate
containing staged and unstaged edits. The exact object identities are execution
evidence, not durable plan constants. No inherited edit is accepted solely
because it is already staged.

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
| WP-001 | Freeze approved design authority | None | Human-approved Spec 0054 | Reviewed Spec/Plan/Task commit |
| WP-002 | Complete four-digit topology, Stage 04 retirement, route-sensitive Stage 00/99 contracts, and Incident route | WP-001 | Inherited candidate classification starts fail-closed | Registry/Markdown/links/lifecycle GREEN; exact path map; atomic migration evidence |
| WP-003 | Consolidate Stage 00 common governance and provider adapters | WP-002 | Active document routes stable | Canonical-owner and provider evidence validators GREEN |
| WP-004 | Reconcile remaining Stage 99 duplication and validator ownership | WP-003 | Governance owners stable | One profile/template/lifecycle/negative-fixture contract per family |
| WP-005 | Record Stage 05 responsibility ledger | WP-004 | Template contract stable | Exact Guide/Policy/Runbook/Incident disposition with no deletion |
| WP-006 | Reconcile Stage 05 ownership with atomic Stage 98 evidence | WP-005 | Operations dispositions approved | Operations, duplicate-owner, and recovery tests GREEN |
| WP-007 | Record complete Stage 90 disposition ledger | WP-006 | Active owners stable | Every Stage 90 file classified exactly once without mutation |
| WP-008 | Reconcile Stage 90 with atomic Stage 98 evidence | WP-007 | Stage 90 dispositions approved | Freshness, generator, link, migration, and recovery GREEN |
| WP-009 | Close global Stage 98 parity and recovery | WP-008 | All current moves/deletions recorded atomically | Archive parity and recovery tests GREEN |
| WP-010 | Complete exact fifty-row script ledger | WP-009 | Exact fifty-script census | Complete disposition/consumer graph with no deletion |
| WP-011 | Retire `validate-harness.sh` | WP-010 | Wrapper consumers migrated | Consumer-zero proof and exact forty-nine-script census |
| WP-012 | Rotate progress and remove stale generated-current residue | WP-011 | Earlier program evidence stable | Append-only memory and generated-current ownership GREEN |
| WP-013 | Retire taxonomy transition assets and activate terminal route state | WP-012 | Terminal consumers moved to permanent contracts | Exact forty-seven-script census, terminal registry, and recovery GREEN |
| WP-014 | Final convergence and branch completion | WP-013 | All logical commits present | Focused/affected/staged/aggregate/all-files/review GREEN |

### WP-001 — approved design authority

**Files:**

- Create: `docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md`
- Create: `docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/plan.md`
- Create: `docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/tasks.md`

- [x] Record the approved topology, scope, protected boundaries, work-package
  sequence, validation lanes, and logical commit policy.
- [x] Keep Spec, Plan, and Task in `draft` until WP-002 atomically registers the
  four-digit path and direct-approval lineage.
- [x] Review the Spec for placeholders, contradictory topology, scope leakage,
  and ambiguous deletion authority.
- [x] Commit only Spec 0054, Plan 0054, and Tasks 0054:
  `docs: define SDLC governance consolidation`.

### WP-002 — terminal topology and four-digit identity

**Files:**

- Activate the direct-approval lineage and change Spec/Plan/Task 0054 from
  `draft` to `active` atomically in
  `docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/`, the
  Stage 03 index, and the registry `standaloneExecutions` projection.
- Reconcile the inherited WORK-109 candidate in
  `docs/03.specs/0052-document-taxonomy-consolidation/{spec.md,plan.md,tasks.md}`
  so WORK-109 through WORK-115 have one explicit `superseded`, `transferred`,
  or retained disposition and no competing active queue.
- Modify the exact eight PRD records, all forty-nine Stage 03 work-unit paths,
  their current mutable consumers, and the relevant Stage 01/02/03 indexes.
- Delete `docs/04.execution/{README.md,plans/README.md,tasks/README.md}` only in
  this atomic route cutover.
- Consolidate the route-sensitive authoring owner at
  `docs/00.agent-governance/rules/document-authoring.md` and repair every root,
  provider, scope, skill, hook, and README link that selects an SDLC route.
- Reconcile the route-sensitive Stage 99 owners:
  `docs/99.templates/support/{document-contract.md,document-lifecycle.md,document-profiles.json,document-profiles.schema.json}`,
  the exact path-bearing templates, and route/identity fixtures.
- Modify `scripts/document_contracts.py`,
  `scripts/validate-document-contract-registry.py`,
  `scripts/validate-document-lifecycle.py`,
  `scripts/validate-links-and-owners.py`,
  `scripts/validate-markdown-profiles.py`, and their focused fixtures/tests.
- Create or extend the current-path rows in
  `docs/98.archive/migrations/mig-0002-sdlc-document-and-governance-consolidation.md`
  in the same commit as every move or deletion; do not defer evidence to
  WP-009.

- [x] Inventory the inherited staged and unstaged paths against the exact
  WP-002/003/004 disposition. Reject unknown paths and correct the inherited
  five-digit-positive/four-digit-negative test before accepting any candidate.
- [x] Add RED tests for three-digit PRD/Spec paths, five-digit paths,
  uppercase Incident paths, date-bearing active filenames, Stage 04 active
  owners, path/frontmatter ID mismatch, missing 0054 direct-approval lineage,
  and a missing migration row.
- [x] Run the focused strict-cutover, registry, lifecycle, and link tests and
  preserve their deterministic diagnostics.
- [x] Apply the exact eight-PRD and forty-nine-work-unit path map; do not infer
  targets from mutable prose.
- [x] Recompute every current cross-link from the path map and reject unknown
  source or target paths.
- [x] Make the Incident route exactly
  `incidents/<year>/inc-####-<slug>/{incident.md,postmortem.md}` and derive
  `INC-<YYYY>-<DDDD>` and `POSTMORTEM-<YYYY>-<DDDD>`.
- [x] Migrate Stage 04 current consumers to Stage 03 siblings while keeping
  immutable historical evidence resolvable through reviewed aliases.
- [x] Run:

  ```bash
  python3 -m unittest tests.test_document_strict_cutover
  python3 scripts/validate-document-contract-registry.py --self-test
  python3 scripts/validate-document-contract-registry.py --mode strict --route-state transition
  python3 scripts/validate-markdown-profiles.py --root . --self-test
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --self-test
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-document-lifecycle.py --root . --self-test
  python3 scripts/validate-document-lifecycle.py --root . --mode staged
  python3 scripts/archive_cutover.py --root .
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  git diff --check
  git diff --cached --check
  ```

- [x] Obtain Python and architecture review.
- [x] Commit: `refactor(docs): normalize terminal SDLC routes`.

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
  consumers reach zero, and commit its Stage 98 disposition/recovery evidence
  atomically with the removal.
- [ ] Run every `scripts/validate-agent-*.py` with `--self-test` and its
  production invocation, plus:

  ```bash
  python3 -m unittest tests.test_document_lifecycle_agent_roster_cutover
  python3 scripts/validate-agent-harness-semantics.py --root . --self-test
  python3 scripts/validate-agent-harness-semantics.py --root .
  python3 scripts/validate-agent-roster-currentness.py --self-test .
  python3 scripts/validate-agent-roster-currentness.py .
  python3 scripts/validate-affected-surfaces.py --root . --self-test
  python3 scripts/validate-affected-surfaces.py --root .
  bash scripts/check-secret-handling.sh
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

- [ ] Obtain architecture, security, and code-quality review.
- [ ] Commit: `refactor(governance): consolidate agent control plane`.

### WP-004 — non-route Stage 99 template deduplication

**Files:**

- Modify: `docs/99.templates/{README.md,templates/README.md,support/README.md}`.
- Modify canonical support prose and authored templates under
  `templates/sdlc/**` and common templates only where their already-active
  profile contracts require it.
- Remove replaced support prose only after current links and hooks point to the
  canonical owners, with matching Stage 98 disposition evidence in the same
  commit.

- [ ] Do not change active route state, path regexes, path-derived identity, or
  direct-approval lineage here; those are atomic WP-002 responsibilities.
- [ ] Add RED tests proving every authored profile has exactly one canonical
  template, frontmatter/body form, lifecycle rationale, and negative fixture
  set without duplicating the registry's machine values in prose.
- [ ] Add template-instance tests for PRD, SRS, IFC, AD, ADR, Spec, Plan, Task,
  Guide, Policy, Runbook, Incident, and Postmortem.
- [ ] Make templates include every required `artifact_id` and Incident metadata
  field; keep dates out of filenames.
- [ ] Remove ARD, RFC, authored API-Spec, Stage 04, legacy routing, and duplicate
  support forms from active lookup surfaces while preserving native OpenAPI,
  GraphQL, and Protobuf contracts.
- [ ] Run:

  ```bash
  python3 -m unittest tests.test_document_strict_cutover
  python3 scripts/validate-document-contract-registry.py --self-test
  python3 scripts/validate-document-contract-registry.py --mode strict --route-state transition
  python3 scripts/validate-markdown-profiles.py --root . --self-test
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-document-lifecycle.py --root . --mode staged
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

  The strict-cutover suite consumes the template compatibility and source-
  parity fixtures under `tests/fixtures/document-contracts/`.
- [ ] Obtain documentation-contract and Python review.
- [ ] Commit: `refactor(templates): converge SDLC document contracts`.

### WP-005 — Stage 05 responsibility ledger

**Files:**

- Create `docs/90.references/data/operations-document-disposition.json` and
  its schema with one row for every Stage 05 README and authored record.
- Extend the existing `scripts/validate-active-corpus-role-audit.py`, its
  ledger, fixtures, and `tests/test_active_corpus_role_audit.py`; do not add a
  duplicate validator executable.
- Review all eight Guides, seven Policies, nine Runbooks, the empty Incident
  collection, and all five collection/index READMEs without changing or
  deleting their bodies in this package.

- [ ] Add RED tests for an operation document with two canonical owners, a
  Guide containing privileged mutation ownership, a Runbook lacking trigger
  or recovery, malformed Incident/Postmortem metadata, and a missing or
  duplicate disposition row.
- [ ] Record owner, purpose, audience, trigger, procedure ownership, consumers,
  overlap group, disposition, successor, source object, and retirement gate.
- [ ] Prove the ledger covers the exact current corpus and makes no content
  mutation or deletion.
- [ ] Run:

  ```bash
  python3 -m unittest tests.test_active_corpus_role_audit
  python3 scripts/validate-active-corpus-role-audit.py --root . --self-test
  python3 scripts/validate-active-corpus-role-audit.py --root .
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

- [ ] Obtain operations and documentation review.
- [ ] Commit: `docs(ops): record operations document dispositions`.

### WP-006 — Stage 05 ownership cutover

**Files:**

- Modify the Stage 05 READMEs and only the Guide, Policy, Runbook, Incident,
  and Postmortem records authorized by WP-005.
- Modify affected Stage 05 templates, registry body contracts, hooks, fixtures,
  indexes, and current links without changing their WP-002 route grammar.
- Add the matching migration/tombstone row and recoverable source evidence to
  Stage 98 in this same commit for every merge, replacement, or deletion.

- [ ] Start from the accepted WP-005 ledger; reject any path or disposition
  absent from it.
- [ ] Resolve the reviewed bootstrap, platform-expansion, observability,
  metrics, and GitOps-onboarding Guide/Runbook overlaps.
- [ ] Strengthen Incident role/timeline/severity/evidence fields and Postmortem
  cause/action-owner/due-state/closure fields.
- [ ] Prove that no Release family or placeholder release directory is added.
- [ ] Run:

  ```bash
  python3 -m unittest tests.test_active_corpus_role_audit tests.test_archive_recovery
  python3 scripts/validate-active-corpus-role-audit.py --root . --self-test
  python3 scripts/validate-active-corpus-role-audit.py --root .
  python3 scripts/validate-document-contract-registry.py --mode strict --route-state transition
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-document-lifecycle.py --root . --mode staged
  python3 scripts/archive_cutover.py --root .
  bash scripts/check-secret-handling.sh
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

  Also run `python3 scripts/archive_recovery.py --root . --record <record>
  --verify` once for each newly admitted Stage 98 record.
- [ ] Obtain operations and security review.
- [ ] Commit: `refactor(ops): clarify operations document ownership`.

### WP-007 — Stage 90 disposition ledger

**Files:**

- Create: `docs/90.references/data/stage90-reference-disposition.json` and
  `docs/90.references/data/stage90-reference-disposition.schema.json`.
- Modify: `scripts/reference_information_architecture.py`,
  `scripts/validate-reference-information-architecture.py`,
  the RIA schema/fixtures, and `tests/test_reference_information_architecture.py`.
- Do not rename, merge, delete, regenerate, or edit a Stage 90 evidence body in
  this package.

- [ ] Enumerate every Stage 90 file with blob OID, profile, current owner,
  freshness trigger, consumers, and one closed disposition.
- [ ] Add RED tests for missing/duplicate disposition, a current reference
  claiming policy authority, and an unowned freshness or generator contract.
- [ ] Require an exact one-to-one census of all tracked Stage 90 files,
  including indexes, data/schema assets, generated outputs, dated evidence
  packs, snapshots, and current semantic references.
- [ ] Run:

  ```bash
  python3 -m unittest tests.test_reference_information_architecture
  python3 scripts/validate-reference-information-architecture.py --root . --self-test
  python3 scripts/validate-reference-information-architecture.py --root . --staged --require-settled-baselines
  bash scripts/generate-llm-wiki-index.sh --check
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

- [ ] Obtain documentation and architecture review.
- [ ] Commit: `docs(references): record Stage 90 dispositions`.

### WP-008 — Stage 90 ownership cutover

**Files:**

- Modify only Stage 90 indexes and current references authorized by WP-007.
- Modify `scripts/reference_information_architecture.py`, the RIA CLI,
  `scripts/generate-llm-wiki-index.sh`, schemas, fixtures, and tests when needed
  to enforce the approved disposition.
- Add Stage 98 migration/tombstone and recovery evidence atomically for every
  Stage 90 move, merge, replacement, or deletion.

- [ ] Reject a stale Stage 04 link, an altered historical source record, an
  unauthorized dated-current path, and a generated output without safe check
  mode before applying the ledger.
- [ ] Convert maintained current references to semantic undated filenames and
  move observation dates into frontmatter/source metadata.
- [ ] Merge duplicate research findings into one current owner; preserve source
  coverage and source commits.
- [ ] Keep audit/snapshot/research-pack dates only where the ledger classifies
  the directory as typed historical evidence.
- [ ] Ensure generated indexes use canonical inputs, bounded reads, check mode,
  protected-output pins where transitional, and no write during check.
- [ ] Run:

  ```bash
  python3 -m unittest tests.test_reference_information_architecture tests.test_archive_recovery
  python3 scripts/validate-reference-information-architecture.py --root . --self-test
  python3 scripts/validate-reference-information-architecture.py --root . --staged --require-settled-baselines
  bash scripts/generate-llm-wiki-index.sh --check
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/archive_cutover.py --root .
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

  Also verify each newly admitted Stage 98 record with `archive_recovery.py`.
- [ ] Obtain documentation, architecture, and Python review.
- [ ] Commit: `refactor(references): reconcile Stage 90 ownership`.

### WP-009 — global Stage 98 parity and recovery closure

**Files:**

- Reconcile program indexes and global parity under `docs/98.archive/` without
  changing sealed predecessor envelopes, source blobs, or embedded payloads.
- Modify archive registry, validation, recovery, cutover, retention, and link
  tests only to close global parity across evidence already committed in
  WP-002, WP-006, and WP-008.

- [ ] Add RED cases for duplicate artifact IDs, malformed stable IDs,
  path/frontmatter mismatch, missing source commits, missing replacement,
  orphan deletion, changed source blob, and active direct Archive-record links.
- [ ] Require the exact seven migration fields from Spec 0054 plus any existing
  stronger archive envelope fields.
- [ ] Join each current deletion/consolidation to exactly one already-atomic
  migration or tombstone record and a recoverable source object; reject late
  evidence created only to mask an earlier unproved deletion.
- [ ] Preserve immutable archive record bytes and resolve current successor
  existence through narrow reviewed aliases only.
- [ ] Run:

  ```bash
  python3 -m unittest tests.test_archive_validation tests.test_archive_cutover tests.test_archive_recovery tests.test_active_corpus_migrations tests.test_active_corpus_retention tests.test_document_lifecycle_archive_cutover
  python3 scripts/archive_cutover.py --root .
  python3 scripts/validate-active-corpus-migrations.py --root . --self-test
  python3 scripts/validate-active-corpus-migrations.py --root .
  python3 scripts/validate-active-corpus-retention.py --root . --self-test
  python3 scripts/validate-active-corpus-retention.py --root .
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

- [ ] Obtain archive, security, and Python review.
- [ ] Commit: `test(archive): close consolidation recovery parity`.

### WP-010 — exact fifty-script disposition ledger

**Files:**

- Create: `docs/90.references/data/script-disposition.json` and
  `docs/90.references/data/script-disposition.schema.json`.
- Modify `scripts/README.md`,
  `docs/00.agent-governance/contracts/validation-surfaces.json`,
  `scripts/validate-affected-surfaces.py`, its schema/fixture, and focused
  tests. This existing validator owns the script inventory; do not add a
  fifty-first executable.
- Do not delete or rename a script in this package.

- [ ] Add RED tests requiring one exact disposition for each of the fifty
  tracked assets and rejecting missing consumers, arguments, diagnostics,
  fixtures, evidence, recovery, or retirement gates.
- [ ] Record all fifty rows and verify the inventory digest.
- [ ] Require owner, purpose, consumers, arguments, diagnostics, fixtures,
  evidence, recovery, decision, replacement, and retirement gate for every
  tracked asset; filename similarity is not a merge reason.
- [ ] Run:

  ```bash
  python3 scripts/validate-affected-surfaces.py --root . --self-test
  python3 scripts/validate-affected-surfaces.py --root .
  python3 -m unittest tests.test_run_validation_lane
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

- [ ] Obtain script and code-quality review.
- [ ] Commit: `docs(scripts): record exact script dispositions`.

### WP-011 — forty-nine-script wrapper cutover

**Files:**

- Modify `scripts/README.md`, validation surfaces, CI/pre-commit contracts,
  root and governance command documentation, fixtures, and current work-unit
  consumers.
- Delete only `scripts/validate-harness.sh` after consumer-zero proof.
- Add its Stage 98 deletion/replacement and recovery evidence in the same
  commit.

- [ ] Add RED cases for each current executable or command consumer of the
  wrapper and for any wrapper-only unique diagnostic or ordering semantic.
- [ ] Migrate README, PR template, approval rule, fixture, CI, hook, and manual
  consumers from `validate-harness.sh` to canonical aggregate/affected lanes.
- [ ] Prove zero current consumers, delete only the wrapper, and assert exact
  forty-nine-file inventory.
- [ ] Run:

  ```bash
  bash -n scripts/*.sh
  python3 scripts/validate-affected-surfaces.py --root . --self-test
  python3 scripts/validate-affected-surfaces.py --root .
  test "$(git ls-files scripts | wc -l)" -eq 49
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  TMPDIR=/tmp pre-commit run
  ```

  Run ShellCheck as an additional `PASS` or explicit optional-tool `SKIP` when
  it is available.
- [ ] Obtain script and code-quality review.
- [ ] Commit: `refactor(scripts): retire harness compatibility wrapper`.

### WP-012 — progress and generated-current cleanup

**Files:**

- Append to `docs/00.agent-governance/memory/progress.md`; preserve its prior
  bytes and history through the approved archive namespace/recovery mechanism.
- Review and remove tracked stale `graphify-out/**` only after current-consumer
  and reproducibility proof; add atomic Stage 98 disposition evidence.
- Modify only the indexes, ignores, contracts, tests, and current links needed
  for that recovery boundary.

- [ ] Restore the transferred intent of Spec 0052 WORK-113 explicitly; do not
  leave it as a competing queued item.
- [ ] Prove the progress snapshot is recoverable, the live ledger is bounded
  and append-only, generated-current ownership is explicit, and stale graph
  residue has zero current consumers.
- [ ] Run:

  ```bash
  python3 scripts/validate-active-corpus-migrations.py --root . --self-test
  python3 scripts/validate-active-corpus-migrations.py --root .
  python3 scripts/validate-active-corpus-retention.py --root . --self-test
  python3 scripts/validate-active-corpus-retention.py --root .
  python3 scripts/archive_cutover.py --root .
  python3 scripts/validate-reference-information-architecture.py --root . --staged --require-settled-baselines
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```
- [ ] Obtain archive and documentation review.
- [ ] Commit: `chore(governance): close progress and generated residue`.

### WP-013 — forty-seven-script terminal cutover

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
- [ ] Change the registry to terminal route state atomically and reject the
  transition profile, manifest, tool, and every live three-digit/Stage 04
  residue.
- [ ] Run:

  ```bash
  python3 scripts/validate-document-contract-registry.py --self-test
  python3 scripts/validate-document-contract-registry.py --mode strict --route-state terminal
  python3 scripts/validate-active-corpus-residue-closure.py --root . --self-test
  python3 scripts/validate-active-corpus-residue-closure.py --root .
  python3 scripts/validate-reference-information-architecture.py --root . --staged --require-settled-baselines
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  test "$(git ls-files 'scripts/*.py' | wc -l)" -eq 39
  test "$(git ls-files 'scripts/*.sh' | wc -l)" -eq 7
  test "$(git ls-files scripts/README.md | wc -l)" -eq 1
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  TMPDIR=/tmp pre-commit run
  ```
- [ ] Obtain Python, archive, and code-quality review.
- [ ] Commit: `refactor(scripts): retire taxonomy transition assets`.

### WP-014 — convergence and branch completion

**Files:**

- Modify only final evidence fields in `tasks.md`, Stage 00 append-only
  progress, and generated indexes whose check-mode contract requires a final
  deterministic refresh.

- [ ] Run exact path, artifact-ID, active-date, direct-archive-link, Stage 04,
  Release-family, legacy/deprecated, and script-inventory audits.
- [ ] Run all focused suites named by WP-002 through WP-013.
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
production validator. WP-002 through WP-014 run affected and staged lanes when
they change a validator-selected surface. Aggregate and pre-commit run at every
route, evidence, generated-output, or deletion boundary and at final
convergence. `transition` is valid only through WP-012; WP-013 and WP-014 must
validate the terminal state.

The owner creates NUL-delimited, normalized path files for the exact affected
and staged scopes, records their SHA-256 digests, and invokes the lanes without
shell reconstruction:

```bash
python3 scripts/run-validation-lane.py --root . --lane affected --paths-file /tmp/spec-0054-affected.nul --delimiter nul
python3 scripts/run-validation-lane.py --root . --lane staged --paths-file /tmp/spec-0054-staged.nul --delimiter nul
TMPDIR=/tmp pre-commit run
```

The terminal minimum is:

```bash
python3 scripts/validate-document-contract-registry.py --self-test
python3 scripts/validate-document-contract-registry.py --mode strict --route-state terminal
python3 scripts/validate-markdown-profiles.py --root . --self-test
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --self-test
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-document-lifecycle.py --root . --self-test
python3 scripts/validate-document-lifecycle.py --root . --mode staged
python3 scripts/validate-reference-information-architecture.py --root . --self-test
python3 scripts/validate-reference-information-architecture.py --root . --staged --require-settled-baselines
bash scripts/generate-llm-wiki-index.sh --check
test "$(git ls-files 'scripts/*.py' | wc -l)" -eq 39
test "$(git ls-files 'scripts/*.sh' | wc -l)" -eq 7
test "$(git ls-files scripts/README.md | wc -l)" -eq 1
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
| [VAL-SDLC-003](spec.md#success-criteria--verification-plan) | WP-002, WP-004, WP-005, WP-006 | [WORK-054-002, WORK-054-004..WORK-054-006](tasks.md#task-table) |
| [VAL-SDLC-004](spec.md#success-criteria--verification-plan) | WP-002, WP-004 | [WORK-054-002, WORK-054-004](tasks.md#task-table) |
| [VAL-SDLC-005](spec.md#success-criteria--verification-plan) | WP-003 | [WORK-054-003](tasks.md#task-table) |
| [VAL-SDLC-006](spec.md#success-criteria--verification-plan) | WP-004 | [WORK-054-004](tasks.md#task-table) |
| [VAL-SDLC-007](spec.md#success-criteria--verification-plan) | WP-005, WP-006 | [WORK-054-005, WORK-054-006](tasks.md#task-table) |
| [VAL-SDLC-008](spec.md#success-criteria--verification-plan) | WP-007, WP-008 | [WORK-054-007, WORK-054-008](tasks.md#task-table) |
| [VAL-SDLC-009](spec.md#success-criteria--verification-plan) | WP-002, WP-006, WP-008, WP-009, WP-012, WP-013 | [WORK-054-002, WORK-054-006, WORK-054-008, WORK-054-009, WORK-054-012, WORK-054-013](tasks.md#task-table) |
| [VAL-SDLC-010](spec.md#success-criteria--verification-plan) | WP-010..WP-013 | [WORK-054-010..WORK-054-013](tasks.md#task-table) |
| [VAL-SDLC-011](spec.md#success-criteria--verification-plan) | WP-002..WP-014 | [WORK-054-002..WORK-054-014](tasks.md#task-table) |
| [VAL-SDLC-012](spec.md#success-criteria--verification-plan) | WP-001..WP-014 | [WORK-054-001..WORK-054-014](tasks.md#task-table) |
