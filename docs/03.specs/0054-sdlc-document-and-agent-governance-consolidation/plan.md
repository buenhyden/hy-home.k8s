---
title: 'SDLC Document and AI Agent Governance Consolidation Implementation Plan'
type: sdlc/plan
status: active
owner: platform
updated: 2026-08-29
artifact_id: "PLAN-0054"
---

# SDLC Document and AI Agent Governance Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` to implement this plan task by
> task. Each task requires a fresh implementer, specification review,
> code-quality review, and focused RED/GREEN evidence. Each independently
> testable logical unit gets one scoped commit; a WP may own ordered commits.
> Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Converge the repository on flat four-digit Requirement Packages,
prefix-free Architecture and Operations paths, work-unit-local Spec-driven
execution, Codex/Claude-only AI-agent governance, minimal Stage 90/98/99
control surfaces, and responsibility-oriented validation modules.

**Architecture:** Stage 00 owns human agent policy, while `.agents/registry.json`
owns the provider-neutral agent roster and Stage 99 owns only document
profiles. Stage 01 Requirement Packages, Stage 02 Architecture, and Stage 03
Spec Packages form the active delivery chain; Stage 05 owns Guides, Policies,
Runbooks, and Incident packages but no Release family. Stage 90 is a
three-family reference library and Stage 98 is a minimal Git-backed
migration/tombstone index. Focused validators consume these owners, aggregates
only orchestrate, and every cutover is staged-index-aware, fail-closed, and
committed as an independently testable logical unit.

**Tech Stack:** Markdown, JSON/JSON Schema, Python 3 standard library, shell,
Git index/object APIs, unittest, pre-commit, and repository quality gates.

**Spec:**
`docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md`

## Global Constraints

- Preserve Git history and unrelated user changes.
- Do not edit existing immutable Stage 98 envelopes or source blobs to satisfy
  current validators. Remove one only in WP-009 after consumer-zero and Git
  recovery are independently proven.
- Preserve Stage 90 audit/source evidence byte-for-byte unless its reviewed
  disposition authorizes a migration with recoverable provenance.
- Use four digits for every active numeric SDLC identity.
- Use `docs/01.requirements/####-<slug>.md` with package ID `REQ-####`.
  Member IDs are exactly `REQ-####-(FR|NFR|IF)-####`, use the containing
  package namespace, and are never reused.
- Use prefix-free `docs/02.architecture/descriptions/####-<slug>.md` and
  `decisions/####-<slug>.md` routes while retaining `AD-####` and `ADR-####`
  frontmatter IDs. Keep superseded ADRs in Stage 02 with reciprocal links.
- Use `docs/05.operations/incidents/<year>/inc-####-<slug>/` exactly.
- Use prefix-free four-digit files for Stage 05 Guides, Policies, and Runbooks;
  remove the local Release document family and its profiles, templates,
  validators, fixtures, links, and directories.
- Keep ordinary active filenames free of dates; retain dates in frontmatter or
  typed evidence metadata.
- Do not restore retired `docs/02.architecture/requirements/` or
  `docs/03.specs/` routes; Requirement Packages, Architecture
  Descriptions, and Stage 03 siblings are their current replacement owners.
- Limit Stage 90 to `research/`, `audits/`, and `data/` numbered packages;
  route `learning/` content to a Stage 05 Guide or Research.
- Limit Stage 98 to README, prefix-free numbered Migrations, and numbered
  Tombstones grouped by original stage; Git history is the default full-body
  archive.
- Make `docs/99.templates/registry.json` the only document-profile machine
  authority, with exactly two schemas under `contracts/` and one human router
  in Stage 99 README.
- Make `.agents/registry.json` plus its schema the only provider-neutral agent
  roster, role, permission, and skill machine authority. Keep `.agents/agents/`
  and `.agents/skills/` provider-neutral; retain only Claude and Codex provider
  projections under `.claude/` and `.codex/`.
- Remove `.gemini/`, root `GEMINI.md`, Gemini/Antigravity provider prose,
  contracts, fixtures, canaries, validators, hooks, and adapter projections;
  do not translate provider-specific semantics into `.agents/`.
- Use `docs/03.specs/####-<slug>/{README.md,spec.md,plan.md,tasks/}` with
  `tasks/tsk-####-<slug>.md`; remove `design.md`, `tests.md`, `tasks.md`, and
  other parallel design/test artifacts only after their unique content is
  assigned to Spec, Plan, Task, AD, or ADR owners.
- Keep root `DESIGN.md` as the UI/design-system owner, not a Stage 03 artifact.
- Do not create or retain `docs/05.operations/releases/`; delivery outcome
  evidence belongs to the executing Task, Git, CI, deployment evidence, or an
  Incident/Postmortem when failure handling is required.
- Resolve prose, template, registry, validator, fixture, README, hook, and
  aggregate rules in the same logical cutover.
- Give each permanent rule one machine owner and one validator. Aggregate
  scripts orchestrate canonical validators and do not reimplement rules.
- Keep one representative positive fixture per profile/contract and one
  independent negative per rule family; generate bounded combinations as
  mutations instead of permanent fixture matrices.
- Remove branch-HEAD, current-document, current-validator, line-number, and
  snapshot-count SHA policies. Retain a digest only for external supply-chain
  identity, explicitly sealed evidence bytes, or a Git-reachable Archive
  recovery object, and record that purpose explicitly.
- Delete a legacy, deprecated, duplicate, or one-time asset only after every
  current consumer is migrated and Stage 98 recovery evidence is valid.
- Treat repository-static, provider-runtime, hosted-CI, remote-live, and
  actual-evaluation evidence as distinct classes.
- Apply simplification in every WP: when a touched rule, gate, fixture, SHA
  pin, compatibility path, or script duplicates an accepted owner, remove or
  merge it in that same logical unit. WP-010 closes the repository-wide
  ownership graph and WP-014 closes the final fixed point; neither defers an
  already-safe local cleanup.
- Organize `scripts/` by responsibility under `docs/`, `setup/`, `qa/`,
  `validation/{documents,agents,archive,repository}`, and `lib/`. Keep focused
  validator tests and fixtures with their production responsibility under
  `scripts/validation/tests/`; retain
  top-level application/infrastructure tests only where they are not validator
  contract tests. Prefer 200–400-line modules, treat 800 lines as a review
  ceiling, and use thin temporary compatibility wrappers only with an explicit
  consumer-zero retirement gate.
- Production validators expose production checks only; remove embedded
  `--self-test` matrices after equivalent focused test modules exist. All
  governed reads are bounded, timeout-controlled, strict-decoding, and exact
  about staged-index versus worktree authority.
- Use `apply_patch` for edits, TDD for behavior changes, scoped staging, and
  conventional logical-unit commits.
- Do not perform push, merge, publication, live deployment, credential access,
  or provider-runtime mutation.

## Overview

This plan executes [Spec 0054](spec.md), tracks its transitional
[Tasks 0054](README.md#task-records), and supersedes conflicting unfinished instructions in
predecessor Spec 0052 only where Spec 0054 explicitly owns the outcome. WP-001
and WP-002 remain completed historical evidence: their commits
proved the former design and four-digit/Stage 04 boundary, but their PRD/SRS/
Interface split, prefixed Architecture paths, expanded Stage 90/98 contracts,
and Stage 99 support layout are not terminal authority after the approved
2026-08-20 design amendments.

The predecessor worktree contained a reviewed but uncommitted WP-003 candidate.
Its valid AI-agent governance, provider evidence, and thin-adapter semantics
remain recoverable candidate input, but WP-003 is blocked until WP-004 activates
the new document, lifecycle, and recovery authorities. Its Gemini/Antigravity surfaces, Stage
98 full-document pinning, Stage 99 support-registry coupling, or other conflicts
with ADR-0030 are discarded rather than ported. No edit is accepted solely
because it was staged in a predecessor worktree.

Execution continues in the linked worktree created from the approved design
authority. WP-004 establishes the terminal document registry, generic recovery
contract, lifecycle vocabulary, and Spec Task layout first. WP-003 then resumes
on those owners. Old transition exceptions, branch/current-document SHA pins,
fixture matrices, and census controls are not copied as a unit.

The execution sequence first records a lossless candidate disposition, then
closes the active taxonomy before simplifying governance, operations,
references, archive evidence, and scripts. Deletions are deliberately late.

## Context

- Eight flat PRD paths remain where unified Requirement Packages are terminal; the
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
- `scripts/` is a flat mixed-responsibility surface with large validators,
  embedded self-tests, duplicate aggregate rules, fixture matrices, and
  transition-only controls. Inventory counts are observations, not terminal
  policy; ownership and consumer-zero evidence govern movement or deletion.

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
- Reorganize scripts by responsibility, split overgrown validators at touched
  boundaries, remove embedded self-test and duplicate aggregate logic, and use
  consumer-zero/recovery gates rather than a fixed terminal file count.
- Finish every work package with deterministic local evidence and an
  independent review.

## Non-Goals & Out-of-Scope

- Rewriting completed historical prose for current terminology.
- Editing sealed Stage 98 payloads to satisfy current rules.
- Creating or retaining a local Release document family; delivery evidence
  remains with Tasks, Git/CI/deployment evidence, or Incident/Postmortem.
- Claiming provider discovery, authenticated execution, hosted CI, deployment,
  or live platform state from repository-static files.
- Combining validators merely because their filenames are similar.
- Cleaning unrelated application, GitOps, Kubernetes, or secret-management
  code.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Establish and amend approved design authority | None | Human-approved Spec 0054 | ADR-0030 and amended Spec committed; conflicting historical assumptions labeled |
| WP-002 | Preserve completed four-digit and Stage 04 intermediate boundary | WP-001 | Historical execution evidence | Prior GREEN evidence retained as migration input, not terminal topology |
| WP-003 | Reconcile Codex/Claude-only AI-agent governance | WP-004 | Document registry, lifecycle, and generic recovery authority active | `.agents` registry, Gemini/Antigravity consumer-zero, and canonical policy/provider projections GREEN |
| WP-004 | Activate document, lifecycle, Spec Task, and recovery authorities | WP-002 | ADR-0030 and Plan/Task update committed | Flat Requirement, prefix-free Architecture, lifecycle, Stage 99, recovery, and link gates GREEN |
| WP-005 | Record Stage 05 responsibility ledger | WP-003 | Governance and template contracts stable | Exact Guide/Policy/Runbook/Incident/Release disposition with no deletion |
| WP-006 | Reconcile Stage 05 ownership and remove Release family | WP-005 | Operations dispositions approved | Prefix-free operations, Release consumer-zero, and recovery tests GREEN |
| WP-007 | Record complete Stage 90 disposition ledger | WP-006 | Active owners stable | Every Stage 90 file classified exactly once without mutation; main staged RIA candidate disposition recorded |
| WP-008 | Reconcile Stage 90 with atomic Stage 98 evidence | WP-007 | Stage 90 dispositions approved | Research/Audit/Data freshness, generator, link, migration, and recovery GREEN |
| WP-009 | Minimize Stage 98 and close Git recovery | WP-008 | Current moves/deletions have atomic evidence | Existing Archive files reduced by retain/compact/delete disposition and reachable recovery proof |
| WP-010 | Close the script, gate, fixture, and SHA ownership graph | WP-009 | Responsibility inventory complete | Every retained control has one owner; duplicate aggregates/self-tests/fixtures/pins classified and safe local duplicates removed |
| WP-011 | Cut over compatibility wrappers and scripts topology | WP-010 | Wrapper and path consumers mapped | Responsibility directories active; wrappers deleted only at consumer-zero; no fixed census policy |
| WP-012 | Rotate progress and remove stale generated-current residue | WP-011 | Earlier program evidence stable | Spec Task/Git evidence and generated-current ownership GREEN |
| WP-013 | Retire transition-only taxonomy controls | WP-012 | Permanent owners carry terminal invariants | Transition assets and exceptions at consumer-zero; terminal registry and recovery GREEN |
| WP-014 | Final convergence and branch completion | WP-013 | All logical commits present | Ownership/fixed-point/focused/affected/staged/aggregate/all-files/review GREEN |

The closed execution order is exactly
`WP-004 → WP-003 → WP-005 → WP-006 → WP-007 → WP-008 → WP-009 → WP-010 → WP-011 → WP-012 → WP-013 → WP-014`.
WP-001 and WP-002 remain completed evidence and are not re-entered.

WP-004 migrates the transitional `tasks.md` ledger without renumbering its
work packages. The lossless identity map is:

| Plan label | Terminal Task ID | Initial terminal status |
| --- | --- | --- |
| WP-001 | TSK-0054-0001 | done |
| WP-002 | TSK-0054-0002 | done |
| WP-003 | TSK-0054-0003 | blocked |
| WP-004 | TSK-0054-0004 | queued; change to `in-progress` only when execution starts after the Plan/Task commit |
| WP-005 | TSK-0054-0005 | queued |
| WP-006 | TSK-0054-0006 | queued |
| WP-007 | TSK-0054-0007 | queued |
| WP-008 | TSK-0054-0008 | queued |
| WP-009 | TSK-0054-0009 | queued |
| WP-010 | TSK-0054-0010 | queued |
| WP-011 | TSK-0054-0011 | queued |
| WP-012 | TSK-0054-0012 | done |
| WP-013 | TSK-0054-0013 | queued |
| WP-014 | TSK-0054-0014 | queued |

Each terminal Task file preserves its WP label, prior result/evidence, current
status, dependencies, ordered logical commit units, rollback, and review state.
These Task IDs and per-package sequences are append-only and never reused.

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

The approved 2026-08-20 amendments are additional WP-001 design authority.
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
- Delete `docs/03.specs/{README.md,plans/README.md,tasks/README.md}` only in
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

### WP-003 — Codex/Claude-only AI-agent governance

WP-003 is `blocked` until WP-004 commits the Stage 99 document registry,
profile lifecycle, Spec Task topology, and generic recovery contract. It
resumes immediately after that dependency; no other WP may become active in
between.

**Files:**

- Modify `docs/00.agent-governance/{README.md,sdlc.md,policies/**,roles/**,
  providers/claude.md,providers/codex.md,skills/**}`.
- Populate `.agents/{registry.json,contracts/agent-registry.schema.json,
  agents/**,skills/**}` as provider-neutral machine authority and reusable
  projections.
- Keep root `AGENTS.md` and `CLAUDE.md`, `.claude/**`, and `.codex/**` as thin
  provider-native gateways. Delete root `GEMINI.md`, `.gemini/**`, Gemini and
  Antigravity provider documents, contracts, canaries, hooks, fixtures, and
  adapter projections.
- Split touched agent-validator internals by responsibility while preserving
  their current root CLIs as compatibility shims through WP-011. Keep focused
  tests in `tests/test_validate_agent_*.py` until the responsibility-path
  cutover moves them and their finite fixtures together.
- Create
  `docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md`
  only for the large governance authority cutover; use minimal Tombstones for
  deleted stable routes whose recovery cannot be found from that Migration.

**Interfaces:**

- `.agents/registry.json` owns role ID, responsibility, permission class,
  capability tier reference, supported providers, skill references, and
  projection paths. Stage 99 MUST NOT duplicate these fields.
- Stage 00 policy owns approval, security, quality, data, Git, SDLC, handoff,
  and evidence rules. Provider notes own only provider-specific discovery and
  capability differences.
- Tracked provider configuration and evidence are secret-free; hosted CI has
  no provider credentials; authenticated canaries are manual/local with
  redacted results.

- [ ] **RED — unsupported surfaces:** add focused tests that reject a Gemini or
  Antigravity provider, `.gemini` projection, Gemini canary, provider-specific
  meaning under `.agents`, and a third supported provider.
- [ ] **RED — authority and injection:** preserve tests that reject duplicate
  role owners, runtime claims from repository-static evidence, arbitrary or
  hidden adapter instructions, extra metadata keys, command injection, CRLF
  hook drift, permission escalation, unbounded input, and secret-bearing
  evidence.
- [ ] Run the focused tests and require the expected missing-terminal-owner and
  forbidden-provider diagnostics before porting any predecessor candidate.
- [ ] Migrate unique policy prose from `rules/`, `controls/`, scopes, catalogs,
  and duplicate provider guides into the approved policies/roles/providers/
  skills owners; delete a source in the same commit once its consumers reach
  zero.
- [ ] Populate the agent registry, generate or normalize provider-neutral role
  and skill projections, and reduce Claude/Codex gateways to the exact
  provider-native metadata and imports allowed by the registry.
- [ ] Remove Gemini/Antigravity surfaces and every current link, schema branch,
  fixture, validator rule, CI/pre-commit invocation, and aggregate command that
  exists only for them. Preserve historical mention only in Git or minimal
  migration evidence.
- [ ] Split touched agent validators by contract responsibility, move their
  tests/fixtures beside the modules, remove production `--self-test`, and make
  the aggregate call only the three terminal agent gates: registry/schema
  integrity, provider projection/config integrity, and semantic/permission
  integrity. Affected-surface selection remains repository orchestration.
- [ ] Remove current-state/provider-document SHA pins. Retain raw-byte digests
  only when a payload is externally supplied and supply-chain-pinned,
  explicitly sealed evidence, or a reachable Archive recovery object. Remove
  unsupported local hook graphs rather than treating executability alone as a
  digest-retention reason.
- [ ] Apply the approved C-SDLC-009 clarification in the authority/projection
  unit: validate MIG-0005 source-backed historical links without changing
  completed bodies, and separate MIG-0004 historical target recovery from
  current Stage 99 template validation. Preserve the existing sealed record
  and source/target identities; reject source drift, missing targets, cycles,
  and unregistered historical consumers. Do not introduce a status-wide
  exception or a new mutable SHA/census control plane.
- [ ] Apply the 2026-08-29 C-SDLC-009 extension in the same first unit:
  explicitly source-backed historical fenced-command literals and separately
  typed removed-view references may resolve only through their proved
  Migration or Archive lookup owner. Preserve ordinary rendered admission,
  regular recovery's symlink rejection, bounded held-input validation and
  unchanged terminal bodies. Add focused positive and independent negative
  regressions before implementing the two reference types. Synchronize the
  missing historical-consumer data, current Stage 00 index format, execution
  Task pointer, Archive policy link and ADR Traceability in the same reviewed
  correction; do not broaden their validators to hide stale data.
- [ ] Apply the subsequent 2026-08-29 C-SDLC-009 approval in this first unit:
  admit only source-proved closed quoted inline paths followed by a comma and
  whitespace/EOF, retaining all other token and recovery boundaries. Add the
  three deferred Spec consumers and their exact literal declarations only
  after the focused positive and independent negative regressions pass.
- [ ] Retire the WER ledger's duplicated first historical inventory table and
  its obsolete terminal shape obligation together, with latest full-file Git
  recovery and Stage 98 partial-content disposition. Preserve the other
  tables, missing-ledger and settlement checks, predecessor-disposition owner,
  and current ledger path; do not add a table or status waiver.
- [ ] Retire the four graphify outputs named in C-SDLC-009 with their current
  consumers and atomic Stage 98 recovery evidence. This approved exception
  advances only that cleanup from WP-012 and substitutes verified Git recovery
  and consumer-zero for the unavailable reproduction procedure. Do not run an
  external generator, claim regeneration, or move historical progress early.
- [ ] In the second logical unit, activate the context/memory policy from its
  first-unit `draft` through the legal `draft → active` transition. Apply the
  approved C-SDLC-007 cumulative CI/ref proof using bounded actual intermediate
  Git history, without changing the requested base or adding SHA/path waivers.
  Verify both staged and cumulative comparison modes; per-commit staged PASS
  alone does not prove the cumulative mode.
- [ ] Run:

  ```bash
  python3 -m unittest discover -s tests -p 'test_validate_agent_*.py'
  python3 scripts/validate-agent-harness-contract.py --root .
  python3 scripts/validate-agent-provider-evidence.py --root .
  python3 scripts/validate-agent-harness-semantics.py --root .
  python3 scripts/validate-affected-surfaces.py --root .
  python3 scripts/validate-document-lifecycle.py --root . --mode staged
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/archive_recovery.py --root . --record docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md --verify
  bash scripts/check-secret-handling.sh
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  git diff --cached --name-only -z > /tmp/spec-0054-staged.nul
  python3 scripts/run-validation-lane.py --root . --lane staged --paths-file /tmp/spec-0054-staged.nul --delimiter nul
  TMPDIR=/tmp pre-commit run
  ```

- [ ] Obtain architecture, security, and code-quality review and resolve every
  Critical/Important finding.
- [ ] Commit authority/projection cutover as
  `refactor(governance): support Codex and Claude only`.
- [ ] Commit validator/test consolidation as
  `refactor(validation): simplify agent governance gates`.

### WP-004 — document, lifecycle, Task, and registry authority activation

WP-004 is the first implementation package after this Plan/Task update. It
establishes the owners required by every later WP and supersedes the
conflicting terminal assumptions of completed WP-002 without rewriting its
historical evidence. It remains queued until this Plan/Task update commits and
the execution handoff begins.

**Files:**

- Create or converge `docs/00.agent-governance/{README.md,sdlc.md,policies/**}`
  for human SDLC and lifecycle policy; defer provider-specific content to
  WP-003.
- Replace the eight Stage 01 records with flat
  `docs/01.requirements/####-<slug>.md` Requirement Packages. Merge overlapping
  document-governance requirements without reusing any issued ID.
- Rename only `docs/02.architecture/descriptions/ad-####-<slug>.md` to
  prefix-free routes, preserve AD frontmatter IDs, retain the already
  prefix-free Decision routes, keep superseded ADRs in Stage 02, and activate
  reciprocal supersession links for ADR-0030 and its predecessors.
- Convert active Spec Packages to
  `{README.md,spec.md,plan.md,tasks/tsk-####-<slug>.md}`. Merge `design.md` and
  `tests.md` content into Spec/Plan/Task or promote durable decisions to AD/ADR
  before deletion. Migrate this transitional `tasks.md` ledger last in WP-004.
- Create `docs/99.templates/{README.md,registry.json,contracts/**,templates/**}`
  with exactly the approved document template groups and no Release profile.
- Create
  `docs/98.archive/migrations/0004-document-authority-convergence.md` for this
  large authority/path cutover and minimal Tombstones only where stable deleted
  paths are not adequately represented by that Migration.
- Split touched document-validator internals by responsibility and extract
  bounded readers behind stable interfaces, while preserving current root CLI
  and `tests/` paths as compatibility surfaces through WP-011.

**Interfaces:**

- `docs/99.templates/registry.json` owns document path, profile, required
  sections, lifecycle, ID pattern, and relationships. It has only `$schema`,
  `$id`, `schemaVersion`, `profiles`, `programLineage`, and
  `standaloneExecutions` at top level.
- Every authored profile has `id`, `pathPattern`, `artifactIdPattern`,
  `template`, `requiredFrontmatter`, `requiredSections`, `lifecycle`, and
  `relationships`; README router profiles have no artifact ID or lifecycle.
- Templates reference a registry profile ID and never hardcode a target path.
- Stage 99 contains no agent roster, role, permission, provider, or skill
  fields; WP-003 creates the separate `.agents` registry and schema.
- Lifecycle transitions exactly match C-SDLC-007; global IDs and per-package
  member/Task numbers are append-only and never reused.

- [ ] **RED — topology and identity:** reject directory Requirement Packages,
  PRD/SRS/IFC profiles, abbreviated member IDs, reused IDs, `ad-`/`adr-` path
  prefixes, missing reciprocal ADR links, Stage 03 `design.md`/`tests.md`/
  `tasks.md`, a Release profile/path, and a path/frontmatter sequence mismatch.
- [ ] **RED — authority and lifecycle:** reject a Stage 99 support owner, agent
  roster fields in Stage 99, an illegal
  profile transition, mutable supersession without reciprocal links, a
  hardcoded template destination, and a production `--self-test` switch.
- [ ] Run focused tests and record the exact diagnostics before any move.
- [ ] Create the Stage 99 registry/two schemas; move existing document
  validators to this authority with bounded strict reads and staged-index/
  worktree drift detection.
- [ ] Convert Stage 01 to flat Requirement Packages. Assign normative source
  statements in source order to `REQ-####-FR-####`, `REQ-####-NFR-####`, and
  `REQ-####-IF-####`; preserve acceptance text and full-ID trace links.
- [ ] Move the prefixed AD routes, keep the already prefix-free ADR routes, and
  reconcile ADR-0015, ADR-0018, ADR-0019, ADR-0023, ADR-0024, ADR-0025, and
  ADR-0030 according to the ADR-0030 supersession table. Do not archive
  superseded ADR bodies.
- [ ] Convert Spec Packages and migrate unique design/test content to its
  owner. For each logical unit create a Task with `TSK-<SPEC>-####`, focused
  RED/GREEN evidence, rollback, review result, and intended commit boundary;
  record the resulting commit in Git/handoff or a later evidence update rather
  than requiring a Task to predict its own commit ID. Keep package README as a
  thin router.
- [ ] Reorganize Stage 99 templates, merge PRD/SRS/Interface into Requirement,
  rename `changes/` to `specs/`, delete design/tests/Release templates, and
  consolidate unique support prose into the Stage 99 README.
- [ ] Remove duplicate aggregate rules, embedded self-test matrices,
  exhaustive permanent fixture combinations, and unjustified current-state
  SHA pins in every touched document validator. Keep representative positives
  and independent mutation negatives beside the production module.
- [ ] Add the exact migration/recovery mapping atomically with moves and prove
  full commit OID, durable-ref reachability, regular legacy blob resolution,
  bounded strict reads, and sealed digest match where applicable.
- [ ] Run:

  ```bash
  python3 -m unittest tests.test_document_strict_cutover tests.test_document_lifecycle_archive_cutover tests.test_archive_recovery
  python3 scripts/validate-document-contract-registry.py --mode strict --route-state transition
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-document-lifecycle.py --root . --mode staged
  python3 scripts/archive_recovery.py --root . --record docs/98.archive/migrations/0004-document-authority-convergence.md --verify
  python3 scripts/validate-affected-surfaces.py --root .
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  git diff --cached --name-only -z > /tmp/spec-0054-staged.nul
  python3 scripts/run-validation-lane.py --root . --lane staged --paths-file /tmp/spec-0054-staged.nul --delimiter nul
  TMPDIR=/tmp pre-commit run
  ```

- [ ] Obtain documentation-contract, architecture, Python, and security review.
- [ ] Commit document authority and lifecycle as
  `refactor(governance): activate document lifecycle authority`.
- [ ] Commit Requirement/Architecture/Spec route cutover and recovery evidence
  as `refactor(docs): converge SDLC packages`.
- [ ] Commit templates, validator tests, fixtures, and support-prose removal as
  `refactor(validation): simplify document contracts`.

### WP-005 — Stage 05 responsibility ledger

**Files:**

- Create a numbered Stage 90 Data package under
  `docs/90.references/data/####-operations-document-disposition/` with a
  stable `DATA-####` identity, bounded ledger, and schema covering every Stage
  05 README and authored file. The package includes its own thin `README.md`.
- Extend `scripts/validate-active-corpus-role-audit.py` and its focused
  tests/fixtures; do not add a duplicate executable. WP-011 later moves this
  responsibility unit and its tests together.
- Review every Guide, Policy, Runbook, Incident/Postmortem, legacy Release
  surface, and collection README without modifying or deleting bodies in this
  package.

- [ ] Add RED tests for an operation document with two canonical owners, a
  Guide containing privileged mutation ownership, a Runbook lacking trigger
  or recovery, malformed Incident/Postmortem metadata, and a missing or
  duplicate disposition row.
- [ ] Record owner, purpose, audience, trigger, procedure ownership, consumers,
  overlap group, disposition, successor, and retirement gate. Record a source
  commit only where the disposition requires Git recovery; do not pin current
  file bytes or corpus counts.
- [ ] Classify every Release path/profile/template/link as `delete` with its
  replacement evidence owner: Spec Task, Git/CI/deployment evidence, or
  Incident/Postmortem.
- [ ] Prove the ledger covers the exact current corpus and makes no content
  mutation or deletion.
- [ ] Run:

  ```bash
  python3 -m unittest tests.test_active_corpus_role_audit
  python3 scripts/validate-active-corpus-role-audit.py --root .
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-affected-surfaces.py --root .
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

- [ ] Obtain operations and documentation review.
- [ ] Commit: `docs(ops): record operations document dispositions`.

### WP-006 — Stage 05 ownership cutover

**Files:**

- Modify the Stage 05 READMEs and only the Guide, Policy, Runbook, Incident,
  Postmortem, and Release records authorized by WP-005.
- Modify affected Stage 05 templates, registry body contracts, hooks, fixtures,
  indexes, and current links. Preserve only WP-002's lowercase Incident
  grammar; supersede its prefixed Guide/Policy/Runbook routes.
- Create `docs/98.archive/migrations/0006-operations-family-convergence.md` for
  the accepted operations path/profile/Release cutover.
- Add the matching migration/tombstone row and recoverable source evidence to
  Stage 98 in this same commit for every merge, replacement, or deletion.

- [ ] Start from the accepted WP-005 ledger; reject any path or disposition
  absent from it.
- [ ] Resolve the reviewed bootstrap, platform-expansion, observability,
  metrics, and GitOps-onboarding Guide/Runbook overlaps.
- [ ] Strengthen Incident role/timeline/severity/evidence fields and Postmortem
  cause/action-owner/due-state/closure fields.
- [ ] Rename Guide/Policy/Runbook files to prefix-free four-digit routes while
  preserving `GDE-####`, `POL-####`, and `RUN-####` frontmatter IDs.
- [ ] Migrate every Release consumer to its approved evidence owner, delete the
  Release documents/directory/profile/template/fixtures/gates, and prove zero
  current consumers. Do not create Release tombstones when the Migration and
  reachable Git history already identify the removed stable paths.
- [ ] Run:

  ```bash
  python3 -m unittest tests.test_active_corpus_role_audit tests.test_archive_recovery
  python3 scripts/validate-active-corpus-role-audit.py --root .
  python3 scripts/validate-document-contract-registry.py --mode strict --route-state transition
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-document-lifecycle.py --root . --mode staged
  python3 scripts/archive_recovery.py --root . --record docs/98.archive/migrations/0006-operations-family-convergence.md --verify
  bash scripts/check-secret-handling.sh
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

  Also run the recovery validator once for every newly admitted Migration or
  Tombstone path and require durable-ref reachability plus legacy blob proof.
- [ ] Obtain operations and security review.
- [ ] Commit: `refactor(ops): clarify operations document ownership`.

### WP-007 — Stage 90 disposition ledger

**Files:**

- Create a numbered Data package under
  `docs/90.references/data/####-reference-disposition/` with the disposition
  ledger, schema, thin `README.md`, and stable `DATA-####` identity.
- Modify `scripts/reference_information_architecture.py`, its CLI, schema,
  finite fixtures, and `tests/test_reference_information_architecture.py`;
  WP-011 later moves this responsibility unit together.
- Do not rename, merge, delete, regenerate, or edit a Stage 90 evidence body in
  this package.

- [ ] Inspect exactly these preserved main-worktree candidate paths by semantic
  diff: `docs/90.references/data/reference-information-architecture.json`,
  `scripts/reference_information_architecture.py`,
  `tests/fixtures/reference-information-architecture/minimal-valid.json`, and
  `tests/test_reference_information_architecture.py`. Record each hunk as
  `port`, `rework`, or `discard`; do not stage or modify the main worktree and
  do not use its index as authority for this branch.
- [ ] Enumerate every Stage 90 file with path, profile, current owner,
  `reviewed_at`, `source_as_of`, `review_due`, consumers, recovery requirement,
  and one closed disposition. Do not add current-file blob or corpus-digest
  pins.
- [ ] Add RED tests for missing/duplicate disposition, a current reference
  claiming policy authority, and an unowned freshness or generator contract.
- [ ] Require an exact one-to-one census of all tracked Stage 90 files,
  including indexes, data/schema assets, generated outputs, dated evidence
  packs, snapshots, and current semantic references.
- [ ] Run:

  ```bash
  python3 -m unittest tests.test_reference_information_architecture
  python3 scripts/validate-reference-information-architecture.py --root . --staged --require-settled-baselines
  bash scripts/generate-llm-wiki-index.sh --check
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

- [ ] Obtain documentation and architecture review.
- [ ] Commit: `docs(references): record Stage 90 dispositions`.

### WP-008 — Stage 90 ownership cutover

The narrowly approved WER historical-table retirement occurs in WP-003 under
C-SDLC-009. Reuse that disposition; the remaining Stage 90 cutover still
requires WP-007 and does not repeat or expand that earlier cleanup.

**Files:**

- Modify only Stage 90 indexes and current references authorized by WP-007.
- Modify the RIA and reference-index generator modules, schemas, finite
  fixtures, and focused tests only as needed to enforce the approved
  disposition.
- Add Stage 98 migration/tombstone and recovery evidence atomically for every
  Stage 90 move, merge, replacement, or deletion.
- Use `docs/98.archive/migrations/0007-reference-library-convergence.md` as the
  single large-cutover mapping when WP-007 dispositions authorize those moves.

- [ ] Reject a stale Stage 04 link, an altered historical source record, an
  unauthorized dated-current path, and a generated output without safe check
  mode before applying the ledger.
- [ ] Convert maintained current references to semantic undated filenames and
  move observation dates into frontmatter/source metadata.
- [ ] Merge duplicate research findings into one current owner; preserve source
  coverage and source commits.
- [ ] Keep all current Research/Audit/Data package paths date-free and store
  observation dates only in `reviewed_at`, `source_as_of`, `review_due`, and
  other profile-approved metadata.
- [ ] Move `learning/` content to a Stage 05 Guide or numbered Research package,
  remove `res-`/`aud-` path prefixes while preserving stable IDs, and delete
  deprecated redirects after consumer-zero.
- [ ] Ensure generated indexes use canonical inputs, bounded reads, check mode,
  and no write during check. A generated-output digest is allowed only when the
  output is explicitly sealed evidence, not as a current-state freshness pin.
- [ ] Run:

  ```bash
  python3 -m unittest tests.test_reference_information_architecture tests.test_archive_recovery
  python3 scripts/validate-reference-information-architecture.py --root . --staged --require-settled-baselines
  bash scripts/generate-llm-wiki-index.sh --check
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/archive_recovery.py --root . --record docs/98.archive/migrations/0007-reference-library-convergence.md --verify
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

  Also verify every newly admitted Migration/Tombstone with the canonical
  recovery validator.
- [ ] Obtain documentation, architecture, and Python review.
- [ ] Commit: `refactor(references): reconcile Stage 90 ownership`.

### WP-009 — global Stage 98 parity and recovery closure

**Files:**

- Reduce `docs/98.archive/` to README, prefix-free numbered Migrations, and
  minimal Tombstones grouped by original stage. Preserve a full historical
  body only for a documented audit/legal exception. Never preserve
  secret-bearing history through ordinary Stage 98; route it to incident,
  rotation, and explicitly approved history-removal handling.
- Modify archive validation/recovery and focused tests only to close global
  parity across evidence committed in WP-002, WP-004, WP-003, WP-006, and
  WP-008.

- [ ] Add RED cases for duplicate artifact IDs, malformed stable IDs,
  path/frontmatter mismatch, missing source commits, missing replacement,
  orphan deletion, changed source blob, and active direct Archive-record links.
- [ ] Classify every existing Archive file as `retain`, `compact`, or `delete`;
  the observed starting count is evidence only and must not become a terminal
  snapshot-count assertion.
- [ ] Require the minimal Migration/Tombstone fields from C-SDLC-009 and reject
  line-number hashes, full-corpus digests, current-document pins, and copied
  completed Spec/Plan/Task bodies without an approved exception.
- [ ] Join each current deletion/consolidation to exactly one already-atomic
  migration or tombstone record and a recoverable source object; reject late
  evidence created only to mask an earlier unproved deletion.
- [ ] For every authorized deletion, require a full commit OID reachable from
  a named durable ref, a regular legacy blob at that path, bounded reads,
  strict UTF-8 for text, and a sealed digest only when the payload is declared
  sealed. Route secret-bearing history through incident/rotation/removal rules.
- [ ] Remove direct active-document links to individual Tombstones; route human
  recovery lookup through Archive README or the relevant Migration.
- [ ] Run:

  ```bash
  python3 -m unittest tests.test_archive_validation tests.test_archive_cutover tests.test_archive_recovery tests.test_active_corpus_migrations tests.test_active_corpus_retention tests.test_document_lifecycle_archive_cutover
  python3 scripts/archive_cutover.py --root .
  python3 scripts/validate-document-lifecycle.py --root . --mode staged
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

- [ ] Obtain archive, security, and Python review.
- [ ] Commit: `refactor(archive): minimize recovery evidence`.

### WP-010 — script, gate, fixture, and SHA ownership fixed point

**Files:**

- Create or converge `scripts/validation/registry.json` and its schema as the
  machine owner for validation responsibilities, lanes, entrypoints,
  consumers, and compatibility retirement gates.
- Modify `scripts/README.md`, affected-surface selection, CI/pre-commit
  consumers, aggregate orchestration, and focused tests under
  `tests/test_run_validation_lane.py` and the existing affected-surface test
  modules. WP-011 moves the complete responsibility unit afterward.
- Use a numbered Stage 90 Data package only for the point-in-time audit that
  justifies the ownership graph; it has a stable `DATA-####` identity and is
  a thin `README.md`, and is not a second executable registry.

- [ ] Add RED tests that reject an unregistered production entrypoint, two
  owners for one rule, aggregate reimplementation, production `--self-test`,
  orphan fixture, matrix fixture without a generator, unexplained SHA pin,
  unbounded read, missing timeout, and index/worktree ambiguity.
- [ ] Record every current script, test, fixture, gate, hook, CI consumer, and
  SHA pin in the ownership graph without a fixed terminal count or inventory
  digest.
- [ ] For every row require responsibility owner, interface, consumers,
  diagnostics, tests, fixtures, evidence class, recovery need, disposition,
  replacement, and retirement gate. Filename similarity is not a merge reason.
- [ ] Remove safe duplicates immediately: aggregate rule copies, embedded
  self-tests already covered by focused modules, redundant fixtures, and
  current-state SHA pins. Leave only blockers with explicit consumer/recovery
  gates for WP-011 or WP-013.
- [ ] Run:

  ```bash
  python3 -m unittest tests.test_run_validation_lane
  python3 scripts/validate-affected-surfaces.py --root .
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  git diff --cached --name-only -z > /tmp/spec-0054-staged.nul
  python3 scripts/run-validation-lane.py --root . --lane staged --paths-file /tmp/spec-0054-staged.nul --delimiter nul
  TMPDIR=/tmp pre-commit run
  ```

- [ ] Obtain script and code-quality review.
- [ ] Commit: `refactor(validation): close control ownership graph`.

### WP-011 — responsibility topology and compatibility cutover

**Files:**

- Modify `scripts/README.md`, validation surfaces, CI/pre-commit contracts,
  root and governance command documentation, fixtures, and current work-unit
  consumers.
- Move scripts into `docs/`, `setup/`, `qa/`, `validation/`, and `lib/` by the
  WP-010 responsibility graph. Delete `validate-harness.sh` and any other
  approved thin compatibility wrapper only after consumer-zero proof; add
  minimal recovery evidence in the same commit when the stable path requires
  it.
- Map document contracts, lifecycle, Markdown, links, RIA, and active-document
  role checks to `scripts/validation/documents/`; agent governance to
  `scripts/validation/agents/`; archive/recovery/retention/migration to
  `scripts/validation/archive/`; affected-surface, lane, workspace, CI, and
  validation-registry controls to `scripts/validation/repository/`.
- Map generators and migration utilities to `scripts/docs/`, bootstrap/render
  helpers to `scripts/setup/`, aggregate/security/GitOps/Kubernetes/Vault
  checks to `scripts/qa/`, and shared bounded Git/path/UTF-8 primitives to
  `scripts/lib/`.
- Expose exactly four canonical validator entrypoints after the move:
  `scripts/validation/documents/validate.py`,
  `scripts/validation/agents/validate.py`,
  `scripts/validation/archive/validate.py`, and
  `scripts/validation/repository/validate.py`. The aggregate entrypoint is the
  thin shell `scripts/qa/validate-repository.sh` and contains no rule logic.

- [ ] Add RED cases for each current executable or command consumer of the
  wrapper and for any wrapper-only unique diagnostic or ordering semantic.
- [ ] Migrate README, PR template, approval rule, fixture, CI, hook, and manual
  consumers from `validate-harness.sh` to canonical aggregate/affected lanes.
- [ ] Move modules and co-located tests in bounded responsibility batches;
  repair imports, CI, pre-commit, docs, affected-surface selection, and shell
  entrypoints atomically in each batch.
- [ ] Prove zero current consumers and zero unique diagnostics before deleting
  each wrapper. Assert registry/path parity rather than an exact file count.
- [ ] Run:

  ```bash
  git ls-files -z 'scripts/**/*.sh' | xargs -0 -r -n1 bash -n
  python3 -m unittest discover -s scripts/validation/tests -p 'test_*.py'
  python3 scripts/validation/documents/validate.py --root . --mode staged --route-state transition
  python3 scripts/validation/agents/validate.py --root .
  python3 scripts/validation/archive/validate.py --root .
  python3 scripts/validation/repository/validate.py --root . --lane affected
  bash scripts/qa/validate-repository.sh .
  TMPDIR=/tmp pre-commit run
  ```

  Run ShellCheck as an additional `PASS` or explicit optional-tool `SKIP` when
  it is available.
- [ ] Obtain script and code-quality review.
- [ ] Commit responsibility batches separately, ending with
  `refactor(scripts): retire compatibility wrappers`.

### WP-012 — progress and generated-current cleanup

**Files:**

- Transfer active execution state from
  `docs/00.agent-governance/memory/progress.md` to the owning Spec Task records
  and Git history. Remove the Stage 00 memory surface after consumer-zero and
  reachable recovery proof; do not create a new global progress ledger.
- Verify the four graphify retirements advanced to WP-003 under C-SDLC-009;
  do not recreate their outputs or repeat their recovery record. Other
  generated-current cleanup still requires its own current-consumer and
  reproducibility proof plus atomic Stage 98 disposition evidence.
- Modify only the indexes, ignores, contracts, tests, and current links needed
  for that recovery boundary.

- [ ] Restore the transferred intent of Spec 0052 WORK-113 explicitly; do not
  leave it as a competing queued item.
- [ ] Prove the old progress path is recoverable, every unfinished item has one
  current Task owner, generated-current ownership is explicit, and stale graph
  residue has zero current consumers. Remove progress-prefix and whole-file
  SHA validators after the transfer.
- [ ] Run:

  ```bash
  python3 -m unittest discover -s scripts/validation/tests/archive -p 'test_*.py'
  python3 -m unittest discover -s scripts/validation/tests/documents -p 'test_*.py'
  python3 scripts/validation/documents/validate.py --root . --mode staged --route-state transition
  python3 scripts/validation/archive/validate.py --root .
  python3 scripts/validation/repository/validate.py --root . --lane affected
  python3 scripts/docs/generate-reference-index.py --root . --check
  bash scripts/qa/validate-repository.sh .
  ```
- [ ] Obtain archive and documentation review.
- [ ] Commit: `chore(governance): close progress and generated residue`.

### WP-013 — transition-only taxonomy terminal cutover

**Files:**

- Migrate permanent consumers of the taxonomy transition manifest and migration
  tool at their WP-011 responsibility paths.
- Modify registry, RIA, generator, residue, links, Markdown fixtures, tests,
  scripts README, and Stage 98 recovery evidence.
- Delete the transition JSON/tool and its transition-only test after closure.

- [ ] Add RED tests that list every remaining transition consumer and prevent
  retirement while one exists.
- [ ] Move terminal invariants to permanent registry, migration ledger, archive
  envelope, or frozen regression fixtures according to ownership.
- [ ] Prove current consumers zero and historical recovery from the source
  commit succeeds.
- [ ] Delete the transition manifest/tool and transition-only tests after
  consumer-zero. Assert validation-registry parity and absence of transition
  authority rather than a fixed script count.
- [ ] Change the registry to terminal route state atomically and reject the
  transition profile, manifest, tool, and every live three-digit/Stage 04
  residue.
- [ ] Run:

  ```bash
  python3 -m unittest discover -s scripts/validation/tests -p 'test_*.py'
  python3 scripts/validation/documents/validate.py --root . --mode strict --route-state terminal
  python3 scripts/validation/agents/validate.py --root . --mode strict
  python3 scripts/validation/archive/validate.py --root . --mode strict
  python3 scripts/validation/repository/validate.py --root . --mode staged
  TMPDIR=/tmp bash scripts/qa/validate-repository.sh .
  TMPDIR=/tmp pre-commit run
  ```
- [ ] Obtain Python, archive, and code-quality review.
- [ ] Commit: `refactor(scripts): retire taxonomy transition assets`.

### WP-014 — convergence and branch completion

**Files:**

- Modify only final evidence fields in the active
  `tasks/tsk-####-<slug>.md` records and generated indexes whose check-mode
  contract requires a deterministic refresh. Do not recreate a Stage 00
  progress ledger.

- [ ] Run exact path, artifact-ID, active-date, direct-archive-link, Stage 04,
  Release-family, Gemini/Antigravity, legacy/deprecated, production-self-test,
  duplicate-owner, orphan-fixture, and validation-registry parity audits.
- [ ] Run the terminal independent test modules that cover the behaviors of
  WP-002 through WP-013; do not rerun retired production `--self-test` paths.
- [ ] Run affected and staged validation with identical path input.
- [ ] Run aggregate quality, exact-index pre-commit, and all-files pre-commit to
  a byte-stable fixed point.
- [ ] Run secret-handling checks without printing candidate values.
- [ ] Obtain final architecture, operations, security, documentation, Python,
  and whole-branch code review; resolve all findings before proceeding.
- [ ] Update append-only Task evidence without recreating Stage 00 progress.
- [ ] Commit: `docs: close SDLC governance consolidation`.
- [ ] Invoke `superpowers:finishing-a-development-branch` and present merge,
  PR, keep, or discard options without pushing or merging automatically.

## Verification Plan

Each work package runs its focused tests first, then the smallest relevant
production validator. WP-004, WP-003, and WP-005 through WP-014 run affected
and staged lanes when
they change a validator-selected surface. Aggregate and pre-commit run at every
route, evidence, generated-output, or deletion boundary and at final
convergence. `transition` is valid only through WP-012; WP-013 and WP-014 must
validate the terminal state.

The owner creates NUL-delimited, normalized path files for the exact affected
and staged scopes and invokes the lanes without shell reconstruction. These
temporary path files are execution inputs, not durable SHA-pinned evidence:

```bash
python3 scripts/validation/repository/validate.py --root . --mode affected --paths-file /tmp/spec-0054-affected.nul --delimiter nul
python3 scripts/validation/repository/validate.py --root . --mode staged --paths-file /tmp/spec-0054-staged.nul --delimiter nul
TMPDIR=/tmp pre-commit run
```

The terminal minimum is:

```bash
python3 -m unittest discover -s scripts/validation/tests -p 'test_*.py'
python3 scripts/validation/documents/validate.py --root . --mode strict --route-state terminal
python3 scripts/docs/generate-reference-index.py --root . --check
python3 scripts/validation/agents/validate.py --root . --mode strict
python3 scripts/validation/archive/validate.py --root . --mode strict
python3 scripts/validation/repository/validate.py --root . --mode staged
TMPDIR=/tmp bash scripts/qa/validate-repository.sh .
TMPDIR=/tmp pre-commit run
TMPDIR=/tmp pre-commit run --all-files
git diff --check
git diff --cached --check
```

Every PASS report records the Task ID, command, exit code, finding count,
mutation status, reviewer disposition, logical commit, and evidence limitation.
The Git commit is execution traceability, not a validator pin for current
documents, registries, templates, or scripts.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Mixed inherited index/worktree makes a false-green candidate | Candidate disposition plus staged-index readers and exact restaging before every broad gate |
| Broad replacements alter historical or native terms | Exact path maps, profile-aware classification, protected blob checks, and focused negative fixtures |
| Stage 90 cleanup destroys provenance | Complete disposition ledger, reachable source commits, and Stage 98 migration before removal; sealed byte pins only when declared |
| Governance adapters drift from canonical semantics | `.agents` owns neutral semantics; adapters carry provider-native metadata only; parity tests cover Codex and Claude |
| Script deletion breaks hidden consumers | Complete consumer graph and zero-consumer negative gate before each deletion |
| Guide/Runbook consolidation removes necessary audiences | Purpose and trigger matrix reviewed by operations and documentation reviewers |
| Large validator files become harder to maintain | Split touched modules by responsibility, use 200–400-line targets and an 800-line review ceiling, and centralize bounded I/O in `scripts/lib/` |
| Static validation is mistaken for live proof | Preserve separate evidence classes and explicit DEFER states |

## Completion Criteria

- The active topology matches C-SDLC-001 exactly.
- Every active numeric SDLC identity is four digits and path-equal to its
  artifact ID.
- Stage 04 and Stage 02 requirements have zero active owners or consumers.
- Incident/Postmortem routes, templates, identities, and fixtures agree.
- Stage 00 and `.agents` have one canonical owner per concern; Codex/Claude
  projections have no unsupported runtime promotion, and Gemini/Antigravity
  have zero current surfaces or consumers.
- Stage 99 profiles, templates, prose, hooks, validators, and fixtures agree.
- Stage 05 Guide/Policy/Runbook/Incident responsibilities are disjoint,
  reviewed duplicates have one owner, and the Release family is absent.
- Every Stage 90 file has one valid disposition and every authorized removal
  has Stage 98 evidence.
- The script validation registry and tracked responsibility paths are equal;
  there are no duplicate rule owners, production self-tests, orphan fixtures,
  unexplained current-state SHA pins, or expired compatibility wrappers.
- All required validation and independent review gates pass without mutation.
- Each logical work package is represented by its own commit.

## Traceability

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-SDLC-001](spec.md#success-criteria--verification-plan) | WP-001, WP-002, WP-004, WP-003, WP-006, WP-008, WP-009, WP-011, WP-013, WP-014 | [TSK-0054-0001](tasks/tsk-0001-approved-design-authority.md), [TSK-0054-0002](tasks/tsk-0002-terminal-topology-and-four-digit-identity.md), [TSK-0054-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [TSK-0054-0003](tasks/tsk-0003-codex-claude-only-ai-agent-governance.md), [TSK-0054-0006](tasks/tsk-0006-stage-05-ownership-cutover.md), [TSK-0054-0008](tasks/tsk-0008-stage-90-ownership-cutover.md), [TSK-0054-0009](tasks/tsk-0009-global-stage-98-parity-and-recovery-closure.md), [TSK-0054-0011](tasks/tsk-0011-responsibility-topology-and-compatibility-cutover.md), [TSK-0054-0013](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-002](spec.md#success-criteria--verification-plan) | WP-002, WP-004, WP-006, WP-008, WP-009, WP-014 | [TSK-0054-0002](tasks/tsk-0002-terminal-topology-and-four-digit-identity.md), [TSK-0054-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [TSK-0054-0006](tasks/tsk-0006-stage-05-ownership-cutover.md), [TSK-0054-0008](tasks/tsk-0008-stage-90-ownership-cutover.md), [TSK-0054-0009](tasks/tsk-0009-global-stage-98-parity-and-recovery-closure.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-003](spec.md#success-criteria--verification-plan) | WP-002, WP-004, WP-005, WP-006, WP-014 | [TSK-0054-0002](tasks/tsk-0002-terminal-topology-and-four-digit-identity.md), [TSK-0054-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [TSK-0054-0005](tasks/tsk-0005-stage-05-responsibility-ledger.md), [TSK-0054-0006](tasks/tsk-0006-stage-05-ownership-cutover.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-004](spec.md#success-criteria--verification-plan) | WP-002, WP-004, WP-014 | [TSK-0054-0002](tasks/tsk-0002-terminal-topology-and-four-digit-identity.md), [TSK-0054-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-005](spec.md#success-criteria--verification-plan) | WP-003, WP-014 | [TSK-0054-0003](tasks/tsk-0003-codex-claude-only-ai-agent-governance.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-006](spec.md#success-criteria--verification-plan) | WP-004, WP-014 | [TSK-0054-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-007](spec.md#success-criteria--verification-plan) | WP-005, WP-006, WP-014 | [TSK-0054-0005](tasks/tsk-0005-stage-05-responsibility-ledger.md), [TSK-0054-0006](tasks/tsk-0006-stage-05-ownership-cutover.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-008](spec.md#success-criteria--verification-plan) | WP-007, WP-008, WP-014 | [TSK-0054-0007](tasks/tsk-0007-stage-90-disposition-ledger.md), [TSK-0054-0008](tasks/tsk-0008-stage-90-ownership-cutover.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-009](spec.md#success-criteria--verification-plan) | WP-002, WP-004, WP-003, WP-006, WP-008, WP-009, WP-011, WP-012, WP-013, WP-014 | [TSK-0054-0002](tasks/tsk-0002-terminal-topology-and-four-digit-identity.md), [TSK-0054-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [TSK-0054-0003](tasks/tsk-0003-codex-claude-only-ai-agent-governance.md), [TSK-0054-0006](tasks/tsk-0006-stage-05-ownership-cutover.md), [TSK-0054-0008](tasks/tsk-0008-stage-90-ownership-cutover.md), [TSK-0054-0009](tasks/tsk-0009-global-stage-98-parity-and-recovery-closure.md), [TSK-0054-0011](tasks/tsk-0011-responsibility-topology-and-compatibility-cutover.md), [TSK-0054-0012](tasks/tsk-0012-progress-and-generated-current-cleanup.md), [TSK-0054-0013](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-010](spec.md#success-criteria--verification-plan) | WP-010, WP-011, WP-012, WP-013, WP-014 | [TSK-0054-0010](tasks/tsk-0010-script-gate-fixture-and-sha-ownership-fixed-point.md), [TSK-0054-0011](tasks/tsk-0011-responsibility-topology-and-compatibility-cutover.md), [TSK-0054-0012](tasks/tsk-0012-progress-and-generated-current-cleanup.md), [TSK-0054-0013](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-011](spec.md#success-criteria--verification-plan) | WP-004, WP-003, WP-005, WP-006, WP-007, WP-008, WP-009, WP-010, WP-011, WP-012, WP-013, WP-014 | [TSK-0054-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [TSK-0054-0003](tasks/tsk-0003-codex-claude-only-ai-agent-governance.md), [TSK-0054-0005](tasks/tsk-0005-stage-05-responsibility-ledger.md), [TSK-0054-0006](tasks/tsk-0006-stage-05-ownership-cutover.md), [TSK-0054-0007](tasks/tsk-0007-stage-90-disposition-ledger.md), [TSK-0054-0008](tasks/tsk-0008-stage-90-ownership-cutover.md), [TSK-0054-0009](tasks/tsk-0009-global-stage-98-parity-and-recovery-closure.md), [TSK-0054-0010](tasks/tsk-0010-script-gate-fixture-and-sha-ownership-fixed-point.md), [TSK-0054-0011](tasks/tsk-0011-responsibility-topology-and-compatibility-cutover.md), [TSK-0054-0012](tasks/tsk-0012-progress-and-generated-current-cleanup.md), [TSK-0054-0013](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-012](spec.md#success-criteria--verification-plan) | WP-001, WP-002, WP-004, WP-003, WP-005, WP-006, WP-007, WP-008, WP-009, WP-010, WP-011, WP-012, WP-013, WP-014 | [TSK-0054-0001](tasks/tsk-0001-approved-design-authority.md), [TSK-0054-0002](tasks/tsk-0002-terminal-topology-and-four-digit-identity.md), [TSK-0054-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [TSK-0054-0003](tasks/tsk-0003-codex-claude-only-ai-agent-governance.md), [TSK-0054-0005](tasks/tsk-0005-stage-05-responsibility-ledger.md), [TSK-0054-0006](tasks/tsk-0006-stage-05-ownership-cutover.md), [TSK-0054-0007](tasks/tsk-0007-stage-90-disposition-ledger.md), [TSK-0054-0008](tasks/tsk-0008-stage-90-ownership-cutover.md), [TSK-0054-0009](tasks/tsk-0009-global-stage-98-parity-and-recovery-closure.md), [TSK-0054-0010](tasks/tsk-0010-script-gate-fixture-and-sha-ownership-fixed-point.md), [TSK-0054-0011](tasks/tsk-0011-responsibility-topology-and-compatibility-cutover.md), [TSK-0054-0012](tasks/tsk-0012-progress-and-generated-current-cleanup.md), [TSK-0054-0013](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
