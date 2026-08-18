---
title: 'SDLC Document and AI Agent Governance Consolidation Implementation Plan'
type: sdlc/plan
status: active
owner: platform
updated: 2026-08-14
artifact_id: "PLAN-0054"
---

# SDLC Document and AI Agent Governance Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` to implement this plan task by
> task. Each task requires a fresh implementer, specification review,
> code-quality review, focused RED/GREEN evidence, and one logical commit.
> Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Converge the repository on package-oriented four-digit requirements,
prefix-free architecture paths, work-unit-local Spec-driven execution,
integrated AI-agent governance, minimal Stage 90/98/99 control surfaces, and a
consumer-safe 47-file terminal script inventory.

**Architecture:** Stage 00 owns agent governance; Stage 99 has one registry,
two schemas, and directly copyable templates; focused validators consume those
owners without duplicating rules in aggregate shell. Stage 01 Requirement
Packages, Stage 02 Architecture, and Stage 03 Spec Packages form the active
delivery chain. Stage 90 is a three-family reference library and Stage 98 is a
minimal Git-backed migration/tombstone index. Every cutover is
staged-index-aware, fail-closed, and committed as an independently testable
logical unit.

**Tech Stack:** Markdown, JSON/JSON Schema, Python 3 standard library, shell,
Git index/object APIs, unittest, pre-commit, and repository quality gates.

## Global Constraints

- Preserve Git history and unrelated user changes.
- Do not edit existing immutable Stage 98 envelopes or source blobs to satisfy
  current validators. Remove one only in WP-009 after consumer-zero and Git
  recovery are independently proven.
- Preserve Stage 90 audit/source evidence byte-for-byte unless its reviewed
  disposition authorizes a migration with recoverable provenance.
- Use four digits for every active numeric SDLC identity.
- Use `docs/01.requirements/####-<slug>/README.md` with package ID `REQ-####`.
  Member IDs are exactly `REQ-####-(FR|NFR|IF)-####`, use the containing
  package namespace, and are never reused.
- Use prefix-free `docs/02.architecture/descriptions/####-<slug>.md` and
  `decisions/####-<slug>.md` routes while retaining `AD-####` and `ADR-####`
  frontmatter IDs. Keep superseded ADRs in Stage 02 with reciprocal links.
- Use `docs/05.operations/incidents/<year>/inc-####-<slug>/` exactly.
- Keep ordinary active filenames free of dates; retain dates in frontmatter or
  typed evidence metadata.
- Do not restore retired `docs/02.architecture/requirements/` or
  `docs/04.execution/` routes; Requirement Packages, Architecture
  Descriptions, and Stage 03 siblings are their current replacement owners.
- Limit Stage 90 to `research/`, `audits/`, and `data/` numbered packages;
  route `learning/` content to a Stage 05 Guide or Research.
- Limit Stage 98 to README, prefix-free numbered Migrations, and numbered
  Tombstones grouped by original stage; Git history is the default full-body
  archive.
- Make `docs/99.templates/registry.json` the only document-profile machine
  authority, with exactly two schemas under `contracts/` and one human router
  in Stage 99 README.
- Keep root `DESIGN.md` as the UI/design-system owner, not a Stage 03 artifact.
- Do not create `docs/05.operations/releases/` without a separately approved
  release-record contract.
- Resolve prose, template, registry, validator, fixture, README, hook, and
  aggregate rules in the same logical cutover.
- Give each permanent rule one machine owner and one validator. Aggregate
  scripts orchestrate canonical validators and do not reimplement rules.
- Keep one representative positive fixture per profile/contract and one
  independent negative per rule family; generate bounded combinations as
  mutations instead of permanent fixture matrices.
- Remove branch-HEAD, current-document, current-validator, line-number, and
  snapshot-count SHA policies. Retain a digest only for immutable recovery,
  external supply-chain integrity, or a sealed evidence payload, and record
  that purpose explicitly.
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
instructions in predecessor Spec 0052 only where Spec 0054 explicitly owns the
outcome. WP-001 and WP-002 remain completed historical evidence: their commits
proved the former design and four-digit/Stage 04 boundary, but their PRD/SRS/
Interface split, prefixed Architecture paths, expanded Stage 90/98 contracts,
and Stage 99 support layout are not terminal authority after the approved
2026-08-14 design amendments.

The active worktree contains a reviewed but uncommitted WP-003 candidate. Its
AI-agent governance, provider evidence, and thin-adapter semantics are retained
only after exact staged/worktree review. Its Stage 98 filename, full-document
pinning, Stage 99 support-registry coupling, or other conflicts with the amended
Spec are reworked or discarded before the WP-003 commit. No edit is accepted
solely because it is already staged.

Execution begins in a new linked worktree and branch created from the approved
Spec/Plan/Task HEAD. The current dirty worktree is preserved read-only as the
candidate source until WP-003 is complete. Valid governance hunks are ported
only after WP-004 establishes the new registry and generic recovery contracts;
the old index, transition exceptions, and SHA/count controls are never copied
as a unit.

The execution sequence first records a lossless candidate disposition, then
closes the active taxonomy before simplifying governance, operations,
references, archive evidence, and scripts. Deletions are deliberately late.

## Context

- Eight flat PRD paths remain where Requirement Packages are now terminal; the
  document-governance packages `0005`, `0006`, and `0008` overlap.
- Stage 04 is retired and forty-nine Stage 03 work units already use four-digit
  package paths; those completed results remain valid.
- Eight Architecture Descriptions still use `ad-` filename prefixes, while
  Decisions already rely on their parent directory and stable ADR IDs.
- The Incident registry candidate uses the approved lowercase four-digit
  route, while Stage 00, Stage 05, aggregate shell, and fixtures still contain
  uppercase three-digit variants.
- Stage 00 already approximates a canonical-core/provider-adapter model, but
  human projections, machine evidence, and native provider claims conflict.
- Stage 90 has `learning/`, cloud snapshots, generated projections, loose data
  ledgers, dated packs, and stale links outside the terminal three-family
  package model.
- Stage 98 has 185 historical files across expanded changes, migrations, and
  tombstones; each requires an explicit retain or minimal Git-backed
  compaction decision.
- Stage 99 still splits human rules and machine values across `support/`,
  `templates/sdlc/`, profile JSON/schema, and duplicate template forms.
- `scripts/` contains exactly fifty tracked assets. One compatibility wrapper
  and two taxonomy-transition assets have approved retirement gates, but none
  is safe to delete immediately.

## Goals & In-Scope

- Produce one exact active topology and one terminology map.
- Convert Stage 01 to Requirement Packages with globally unique member IDs and
  preserve requirement-to-Architecture-to-Spec traceability.
- Remove route prefixes whose parent folder already owns the type without
  changing stable frontmatter identities.
- Make Stage 00, Stage 99, validators, and provider adapters agree.
- Make Stage 05 families purpose-disjoint and Incident-ready.
- Classify and reconcile every Stage 90 file.
- Reduce Stage 98 to the minimum lookup and Git-recovery evidence required for
  every removal or consolidation.
- Reduce Stage 99 to one registry, two schemas, one human README, and one
  directly copyable template per active profile.
- Remove duplicate gate logic, fixture matrices, and unjustified mutable SHA
  pins as each work package touches them.
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
| WP-001 | Freeze and amend approved design authority | None | Human-approved Spec 0054 | Reviewed Spec/Plan/Task design commits; historical authority labeled |
| WP-002 | Preserve completed four-digit and Stage 04 intermediate boundary | WP-001 | Historical execution evidence | Prior GREEN evidence retained; superseded endpoints no longer treated as terminal |
| WP-003 | Reconcile and complete integrated AI-agent governance | WP-004 | New registry and generic recovery authority committed | Canonical-owner/provider/thin-adapter GREEN; minimal prefix-free migration evidence |
| WP-004 | Converge Requirement Packages, prefix-free Architecture, and Stage 99 | WP-002 | New clean worktree from approved design HEAD | Requirement identity, route, registry, template, lifecycle, and link GREEN in two logical commits |
| WP-005 | Record Stage 05 responsibility ledger | WP-003 | Governance and template contracts stable | Exact Guide/Policy/Runbook/Incident disposition with no deletion |
| WP-006 | Reconcile Stage 05 ownership with atomic Stage 98 evidence | WP-005 | Operations dispositions approved | Operations, duplicate-owner, and recovery tests GREEN |
| WP-007 | Record complete Stage 90 disposition ledger | WP-006 | Active owners stable | Every Stage 90 file classified exactly once without mutation |
| WP-008 | Reconcile Stage 90 with atomic Stage 98 evidence | WP-007 | Stage 90 dispositions approved | Freshness, generator, link, migration, and recovery GREEN |
| WP-009 | Minimize Stage 98 and close Git recovery | WP-008 | All current moves/deletions recorded atomically | Existing 185-file disposition, minimal topology, and recovery tests GREEN |
| WP-010 | Complete exact fifty-row script and control-complexity ledger | WP-009 | Exact fifty-script census | Complete owner/consumer graph; duplicate gates, fixture residue, and mutable SHA classified |
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

The approved 2026-08-14 amendments are additional WP-001 design authority.
They preserve this completed evidence while superseding its former terminal
form, path-prefix, Stage 90/98, Stage 99, fixture, gate, and SHA assumptions.

### WP-002 — terminal topology and four-digit identity

WP-002 is complete historical intermediate evidence. Do not rewrite its
reported commands, counts, or commit. Its four-digit Stage 03, Stage 04
retirement, Incident, direct-approval, and Git-recovery results remain inputs.
Its flat PRD paths, split requirement forms, `ad-` paths, expanded Archive
model, and Stage 99 support layout are explicitly superseded by WP-004 and
cannot satisfy the terminal completion criteria.

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
- Rename the staged transition record to
  `docs/98.archive/migrations/0003-agent-governance-control-plane-consolidation.md`
  and reduce it to three `merged` mappings with replacement,
  `recovery_commit`, and reason. Do not retain a mutable full-document,
  validator-blob, or branch-HEAD pin.
- Modify archive, migration, lifecycle, link, and aggregate validators only as
  needed to consume that semantic three-row record and prove Git recovery.

- [ ] Freeze the current candidate inventory before restaging: 105 staged
  paths plus the two unstaged active-migration validator/test paths. Classify
  each path as `retain-governance`, `rework-evidence`, or `discard-conflict`;
  reject an unknown path rather than expanding WP-003.
- [ ] Preserve the existing RED/GREEN coverage for duplicate common policy,
  unsupported provider runtime claims, repository-static evidence promoted to
  runtime, missing canonical owners, divergent role semantics, arbitrary
  adapter payloads, hook-command injection, CRLF graph drift, and unbounded
  adapter instructions.
- [ ] Correct factual provider capability and hook claims against official
  provider documentation and observed evidence.
- [ ] Reduce root/provider files to thin native gateways; move shared semantics
  to one Stage 00 owner.
- [ ] Collapse repeated human matrices into one contract-derived catalog and
  route variable state to machine contracts.
- [ ] Delete only `common-governance.md`, `harness-implementation-map.md`, and
  `providers/agents-md.md`; require zero current consumers and the exact
  three-row prefix-free Migration in the same commit.
- [ ] Remove or replace every WP-003 current-state SHA pin. Keep raw-byte
  digests only for the two provider hook graphs because their executable
  bytes are the reviewed supply-chain surface; keep recovery commits for the
  three removed owners.
- [ ] Stage the two active-migration files only after the exact MIG-0003
  inventory regression is GREEN, then require no index/worktree drift.
- [ ] Run every `scripts/validate-agent-*.py` with `--self-test` and its
  production invocation, plus:

  ```bash
  python3 -m unittest tests.test_document_lifecycle_agent_roster_cutover
  python3 scripts/validate-agent-harness-semantics.py --root . --self-test
  python3 scripts/validate-agent-harness-semantics.py --root .
  python3 scripts/validate-agent-roster-currentness.py --self-test .
  python3 scripts/validate-agent-roster-currentness.py .
  python3 -m unittest tests.test_active_corpus_migrations
  python3 scripts/validate-active-corpus-migrations.py --root . --self-test
  python3 scripts/validate-active-corpus-migrations.py --root .
  python3 -m unittest tests.test_archive_validation tests.test_document_lifecycle_archive_cutover
  python3 scripts/validate-document-lifecycle.py --root . --self-test
  python3 scripts/validate-document-lifecycle.py --root . --mode staged
  python3 scripts/validate-links-and-owners.py --root . --self-test
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-affected-surfaces.py --root . --self-test
  python3 scripts/validate-affected-surfaces.py --root .
  bash scripts/check-secret-handling.sh
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

- [ ] Obtain architecture, security, and code-quality review.
- [ ] Commit: `refactor(governance): consolidate agent control plane`.

### WP-004 — Requirement Package, Architecture, and Stage 99 convergence

**Files:**

- Replace eight flat Stage 01 records with these six packages:
  `0001-argo-rollouts-progressive-delivery/`,
  `0002-argo-notifications-slack/`,
  `0003-workspace-agent-governance-platform/`,
  `0004-current-local-gitops-platform/`,
  `0005-workspace-document-governance/` (merge former `0005`, `0006`, and
  `0008`), and `0007-repository-delivery-and-platform-assurance/`.
- Rename all eight `docs/02.architecture/descriptions/ad-####-<slug>.md`
  files to prefix-free `####-<slug>.md`; keep their `AD-####` identities.
  Keep every Decision in Stage 02 and preserve reciprocal supersession links.
- Create `docs/99.templates/registry.json`,
  `contracts/frontmatter.schema.json`, and
  `contracts/document-profile.schema.json`.
- Reorganize `docs/99.templates/templates/` into exactly `governance/`,
  `requirements/`, `architecture/`, `specs/`, `operations/`, `references/`,
  `archive/`, and `common/`.
- Delete `docs/99.templates/support/` and the old split profile JSON/schema
  only after every current consumer reads the root registry and two schemas.
- Create `docs/98.archive/migrations/0004-requirement-and-architecture-package-convergence.md`
  in the route cutover commit; it maps the eight Stage 01 sources to six
  packages and the eight prefixed AD sources to prefix-free successors.

**Interfaces:**

- `registry.json` has only `$schema`, `$id`, `schemaVersion`, `profiles`,
  `programLineage`, and `standaloneExecutions` at top level.
- Each authored profile has `id`, `pathPattern`, `artifactIdPattern`,
  `template`, `requiredFrontmatter`, `requiredSections`, `lifecycle`, and
  `relationships`. Archive inventories, transition baselines, governance
  owners, and Stage 90 pack inventories are not profile-registry fields.
- Templates declare a registry `profile` ID and never hardcode a destination
  path.

- [ ] Write focused RED cases for a loose Stage 01 file, repeated PRD/SRS/IFC
  owners, wrong `REQ-####` package namespace, invalid member family, reused
  member number, stale member link, `ad-`/`adr-` route prefix, missing reciprocal
  ADR supersession, support-prose authority, duplicate template, hardcoded
  template path, and extra registry top-level field.
- [ ] Run those focused tests and record the exact intended diagnostics before
  moving a document.
- [ ] In each Package README, assign normative statements in source order to
  independent append-only `FR`, `NFR`, and `IF` sequences. Preserve acceptance
  text and link every criterion to one or more full member IDs.
- [ ] Merge former Requirement records `0005`, `0006`, and `0008` without
  losing unique statements; add explicit supersession mappings for their old
  artifact IDs and current links.
- [ ] Move the eight AD files, update current links and indexes, and leave
  accepted/superseded ADR bodies in place.
- [ ] Create the root registry and schemas, then update `document_contracts.py`
  and the registry, Markdown, lifecycle, and link validators to consume them.
- [ ] Add directly copyable templates for Requirement Package, AD, ADR, Spec,
  Plan, Task, Guide, Policy, Runbook, Incident, Postmortem, Research, Audit,
  Data, Migration, and Tombstone. Keep executable OpenAPI/GraphQL/Proto
  contracts in the implementing Spec Package rather than Stage 01 templates.
- [ ] Delete separate PRD/SRS/Interface, `design.template.md`, and
  `tests.template.md` forms; route any change-template consumer to `specs/`.
- [ ] Merge the unique human guidance from Stage 99 support prose into the
  Stage 99 README, delete the support directory, and assert zero consumer.
- [ ] For each touched validator, remove duplicated aggregate logic, collapse
  exhaustive fixtures to one representative positive plus independent
  mutation negatives, and remove unjustified current-state SHA pins.
- [ ] Run:

  ```bash
  python3 -m unittest tests.test_document_strict_cutover
  python3 scripts/validate-document-contract-registry.py --self-test
  python3 scripts/validate-document-contract-registry.py --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --self-test
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --self-test
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-document-lifecycle.py --root . --self-test
  python3 scripts/validate-document-lifecycle.py --root . --mode staged
  python3 -m unittest tests.test_archive_validation tests.test_archive_recovery
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```
- [ ] Obtain documentation-contract and Python review.
- [ ] Commit the route-sensitive package, Architecture, registry, schema, core
  template, validator, link, and Migration change as
  `refactor(docs): adopt package-oriented document contracts`.
- [ ] Commit the remaining support-prose/template/fixture deduplication as
  `refactor(templates): converge Stage 99 contracts`.

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
