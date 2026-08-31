---
title: 'SDLC Document and AI Agent Governance Consolidation Implementation Plan'
type: sdlc/plan
status: active
owner: platform
updated: 2026-08-31
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
  recovery are independently proven. Keep MIG-0006 through MIG-0009
  byte-for-byte and defer their deletion until authorized remote or full-clone
  ancestry proof is available.
- Preserve source provenance while Stage 90 content moves to its semantic
  owner. Point-in-time dispositions belong to the Task/diff, not a permanent
  corpus ledger or digest.
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
- Do not restore the retired Stage 02 requirements or Stage 04 execution
  routes; Requirement Packages, Architecture Descriptions, and Stage 03
  siblings are their current replacement owners.
- Limit Stage 90 to `research/`, `audits/`, and `data/` numbered packages;
  route `learning/` content to a Stage 05 Guide or Research.
- Limit Stage 98 to README, prefix-free numbered Migrations, and only the
  minimal Tombstones genuinely required for immutable historical lookup; Git
  history is the default full-body archive.
- Make `docs/99.templates/registry.json` the only document-profile machine
  authority, with normalized top-level `lifecycleDomains` and one human router
  in Stage 99 README. Do not gate schema, profile, or template counts.
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
- Keep only bounded fixtures needed to prove semantic rule families; generate
  combinations as mutations instead of permanent fixture matrices or fixed
  case-count gates.
- Remove branch-HEAD, current-document, current-validator, line-number, and
  snapshot-count SHA policies. Retain a digest only for external supply-chain
  identity, explicitly sealed evidence bytes, or a Git-reachable Archive
  recovery object, and record that purpose explicitly.
- Delete a legacy, deprecated, duplicate, or one-time asset only after every
  current consumer is migrated and Git recovery is proven. Add Stage 98
  evidence only for a genuinely necessary immutable historical lookup.
- Treat repository-static, provider-runtime, hosted-CI, remote-live, and
  actual-evaluation evidence as distinct classes.
- Apply simplification in every WP: when a touched rule, gate, fixture, SHA
  pin, compatibility path, or script duplicates an accepted owner, remove or
  merge it in that same logical unit. WP-010 closes the repository-wide
  ownership graph and WP-014 closes the final fixed point; neither defers an
  already-safe local cleanup.
- After ADR-0031 is accepted with the reciprocal ADR-0030 scoped-amendment
  evidence, organize `scripts/` by responsibility under `docs/`, `setup/`, `qa/`,
  `validation/{documents,agents,archive,repository}`, and `lib/`. Keep focused
  validator tests and fixtures independent under top-level `tests/` and
  `tests/fixtures/`; production modules must not import or read them. Split
  modules by responsibility, duplication, and change risk rather than a fixed
  line ceiling. Use thin temporary compatibility wrappers only with an
  explicit consumer-zero retirement gate.
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

Spec 0054 remains the integration and acceptance owner. Draft Spec 0066 at
`../0066-validation-tooling-ownership/spec.md` is the delegated execution
package for WP-010 and WP-011; its queued execution record is
`TSK-0066-0001`. Cross-package navigation is owned by the
[Current Spec Index](../README.md#current-spec-index). The relation is governed by
[proposed ADR-0031](../../02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md).
It is not a standalone program. This design checkpoint does not activate Spec
0066 or change any Task lifecycle state.

After written-design approval and completion of WP-009 and its owning Task, the
active owner hands off to TSK-0054-0010 as the sole `in-progress` parent Task in
a separate lifecycle-valid change. That handoff also moves the existing Spec
0054 `standaloneExecutions` task pointer to TSK-0054-0010; the compatibility
row remains parent-only and creates no Spec 0066 authority. TSK-0054-0010 then
owns one activation transaction before delegated execution starts. That
transaction accepts ADR-0031; moves ADR-0016/0017/0020/0021/0022 from
`accepted` to `superseded` with reciprocal ADR-0031 relations; adds the
two-clause ADR-0030 amendment evidence without changing ADR-0030 status;
updates the Decisions README and every current `Proposed ADR-0031` label plus
the Stage 03 validator-test placement rule; updates the thin Spec 0066 README's
current-state prose and the Current Spec Index row from `Draft` to `Active`;
adds the narrow delegated-component ownership gate and focused tests; verifies
the updated router and index; activates Spec/Plan/Task 0066; completes
TSK-0054-0010; moves the existing Spec 0054 row
to TSK-0054-0011; and moves that Task from `queued` to `in-progress` as the sole
parent acceptance owner. TSK-0066-0001 does not execute or partially own the
transaction that activates it, and no standalone Spec 0066 row is created.

The predecessor worktree contained a reviewed but uncommitted WP-003 candidate.
WP-004 has since completed the document, lifecycle, and recovery authority
activation, and WP-003 is now `in-progress` on those owners. The candidate's
valid AI-agent governance, provider evidence, and thin-adapter semantics remain
recoverable input. Its Gemini/Antigravity surfaces, Stage 98 full-document
pinning, Stage 99 support-registry coupling, or other conflicts with ADR-0030
are discarded rather than ported. No edit is accepted solely because it was
staged in a predecessor worktree.

Execution continues in the linked worktree created from the approved design
authority. Completed WP-004 established the document registry, generic
recovery contract, lifecycle vocabulary, and Spec Task layout; WP-003 now uses
those owners. Old transition exceptions, branch/current-document SHA pins,
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
- Stage 98 contains full-body Tombstones and redirect chains that duplicate Git
  recovery. Sealed records cannot be compacted in place; consumer-zero and the
  applicable recovery proof determine whether each can be deleted.
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
- Reduce Stage 98 to bounded lookup evidence that Git cannot supply; do not
  require a record for every removal or consolidation.
- Reduce Stage 99 to profile definitions, normalized top-level lifecycle
  domains, one human router, and only the schemas/templates required by active
  profiles.
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
| WP-005 | Review Stage 05 semantic owners | WP-003 | Governance and template contracts stable | Reviewed Guide/Policy/Runbook/Incident/Postmortem target and Task-local cutover decisions |
| WP-006 | Reconcile Stage 05 ownership and remove Release family | WP-005 | Operations owner review complete | Canonical operations owners, strengthened incident contracts, Release consumer-zero, and Git recovery GREEN |
| WP-007 | Review Stage 90 semantic destinations | WP-006 | Active owners stable | Research/Audit/Data/Guide destinations reviewed in the Task/diff; permanent RIA census contract rejected |
| WP-008 | Reconcile Stage 90 semantic owners | WP-007 | Stage 90 destination review complete | Current package ownership/freshness GREEN; obsolete wiki, generator, gate, redirect, audit, and data overlap removed |
| WP-009 | Minimize Stage 98 and close recovery | WP-008 | Current consumers and Git recovery mapped | Sealed records unchanged; redundant full-body/redirect records removed; remote-dependent records explicitly deferred |
| WP-010 | Close the script, gate, fixture, and SHA ownership graph through delegated Spec 0066 | WP-009 and approved written design | Existing validation-surface contract and consumers mapped | Delegated Task evidence proves one routing owner, removes safe duplicates, and reports acceptance to Spec 0054 |
| WP-011 | Cut over compatibility wrappers and scripts topology through delegated Spec 0066 | WP-010 within Spec 0066 | Wrapper and path consumers mapped | Responsibility directories active; wrappers deleted only at consumer-zero; TSK-0054-0011 records parent acceptance; no fixed census policy |
| WP-012 | Rotate progress and remove stale generated-current residue | WP-011 | Earlier program evidence stable | Spec Task/Git evidence and generated-current ownership GREEN |
| WP-013 | Cut over the remaining current corpus and close transition references | WP-012; accepted and completed Spec 0066 result; completed TSK-0054-0011 parent handoff | ADR-0031 accepted; TSK-0066-0001, Plan 0066, and Spec 0066 are `done`; TSK-0054-0011 is `done`; the existing Spec 0054 compatibility pointer names queued TSK-0054-0013 | Stage 01/02/03/99 disposition, residual transition consumer-zero, and Git-first recovery GREEN |
| WP-014 | Final convergence and branch completion | WP-013 and accepted Spec 0066 result | All logical commits present | Ownership/fixed-point/focused/affected/staged/aggregate/all-files/review GREEN |

WP-012 is a closed historical scheduling exception, not a reusable dependency
rule. Its terminal Task keeps the originally declared WP-011 dependency and is
not rewritten. It executed before WP-011 under direct human approval on
2026-08-30, after Spec 0052 `WORK-113` had transferred and Spec 0064 had
recorded the `VAL-AGS-002` blocker. This record explains existing Git evidence;
it grants no current or future Task authority to bypass a declared dependency.

Work follows the dependency table, not one global closed order. Each Spec
Package may have at most one `in-progress` Task. After the reviewed activation
checkpoint, Spec 0066 may execute its own WP-001 through WP-012 plan for the
delegated parent WP-010/WP-011 scope while TSK-0054-0011 remains Spec 0054's
sole parent acceptance Task. No unrelated Spec 0054 Task runs in that window;
parent WP-014 later joins both results. Parent WP-001 and WP-002 remain
completed evidence and are not re-entered.

WP-004 migrates the transitional `tasks.md` ledger without renumbering its
work packages. The lossless identity map is:

| Plan label | Terminal Task ID | Initial terminal status |
| --- | --- | --- |
| WP-001 | TSK-0054-0001 | done |
| WP-002 | TSK-0054-0002 | done |
| WP-003 | TSK-0054-0003 | in-progress |
| WP-004 | TSK-0054-0004 | done |
| WP-005 | TSK-0054-0005 | queued |
| WP-006 | TSK-0054-0006 | queued |
| WP-007 | TSK-0054-0007 | queued |
| WP-008 | TSK-0054-0008 | queued |
| WP-009 | TSK-0054-0009 | queued |
| WP-010 | TSK-0054-0010 | queued; transfer to Spec 0066 is not effective until its activation checkpoint |
| WP-011 | TSK-0054-0011 | queued; becomes the parent acceptance owner at the Spec 0066 activation checkpoint |
| WP-012 | TSK-0054-0012 | done |
| WP-013 | TSK-0054-0013 | queued |
| WP-014 | TSK-0054-0014 | queued |

TSK-0054-0011 has an earlier lifecycle activation dependency than the
delegated WP-011 implementation: it starts only as the parent acceptance owner
after WP-009 and the TSK-0054-0010 activation transaction. Spec 0066 WP-011
still depends on Spec 0066 WP-010 and cannot execute early.

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

- Historical WP-002 activated Spec/Plan/Task 0054 and its then-current
  direct-approval projection. That evidence is not authority to recreate the
  `standaloneExecutions` roster; proposed ADR-0031 replaces it with
  package-local relationships.
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
  python3 scripts/validate-document-contract-registry.py --mode strict
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

WP-003 is `in-progress`. Completed WP-004 supplied the Stage 99 document
registry, profile lifecycle, Spec Task topology, and generic recovery contract
that unblocked this package. Its accepted Task record is the current execution
state owner.

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
- [ ] Split touched agent validators by contract responsibility and remove
  production `--self-test`. Relocate their tests/fixtures to top-level `tests/`
  only after ADR-0031 acceptance; until then preserve ADR-0030's current layout
  without adding duplication. Make the aggregate call only the three terminal
  agent gates: registry/schema integrity, provider projection/config integrity,
  and semantic/permission integrity. Affected-surface selection remains
  repository orchestration.
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

WP-004 is completed historical execution. It established the owners required
by later work and superseded the conflicting terminal assumptions of completed
WP-002 without rewriting that evidence. Its accepted Task and commits are the
execution record; sealed MIG-0004 is not regenerated. Terminal corpus
reductions introduced by proposed ADR-0031 are prospective WP-013 work, not a
reason to reopen WP-004.

**Accepted historical boundary:**

- Converged `docs/00.agent-governance/{README.md,sdlc.md,policies/**}`
  for human SDLC and lifecycle policy; provider-specific content remained with
  WP-003.
- Converted the eight Stage 01 records to flat
  `docs/01.requirements/####-<slug>.md` Requirement Packages without reusing
  any issued ID.
- Renamed `docs/02.architecture/descriptions/ad-####-<slug>.md` to
  prefix-free routes, preserved AD frontmatter IDs, retained the already
  prefix-free Decision routes, kept superseded ADRs in Stage 02, and activated
  reciprocal supersession links for ADR-0030 and its predecessors.
- Converted active Spec Packages to
  `{README.md,spec.md,plan.md,tasks/tsk-####-<slug>.md}`, migrated unique
  `design.md` and `tests.md` content to its semantic owner, and migrated the
  transitional `tasks.md` ledger last.
- Created `docs/99.templates/{README.md,registry.json,contracts/**,templates/**}`
  with exactly the approved document template groups and no Release profile.
- Created and sealed
  `docs/98.archive/migrations/0004-document-authority-convergence.md` for the
  authority/path cutover; this Plan does not recreate or edit it.
- Split touched document-validator internals by responsibility and extracted
  bounded readers behind stable interfaces, while preserving current root CLI
  and `tests/` paths as compatibility surfaces through WP-011.

**Interfaces:**

- `docs/99.templates/registry.json` owns document path, profile, required
  sections, lifecycle, ID pattern, and normalized lifecycle domains. It does
  not own current program, execution-instance, approval-sentence, or reference
  pack rosters; package-local Spec/Plan/Task relationships own execution
  delegation and approval traceability.
- Every authored profile has `id`, `pathPattern`, `artifactIdPattern`,
  `template`, `requiredFrontmatter`, `requiredSections`, `lifecycle`, and
  `relationships`; README router profiles have no artifact ID or lifecycle.
- Templates reference a registry profile ID and never hardcode a target path.
- Stage 99 contains no agent roster, role, permission, provider, or skill
  fields; WP-003 creates the separate `.agents` registry and schema.
- Lifecycle transitions exactly match C-SDLC-007; global IDs and per-package
  member/Task numbers are append-only and never reused.

- [x] **RED — topology and identity:** reject directory Requirement Packages,
  PRD/SRS/IFC profiles, abbreviated member IDs, reused IDs, `ad-`/`adr-` path
  prefixes, missing reciprocal ADR links, Stage 03 `design.md`/`tests.md`/
  `tasks.md`, a Release profile/path, and a path/frontmatter sequence mismatch.
- [x] **RED — authority and lifecycle:** reject a Stage 99 support owner, agent
  roster fields in Stage 99, an illegal
  profile transition, mutable supersession without reciprocal links, a
  hardcoded template destination, and a production `--self-test` switch.
- [x] Ran focused tests and recorded the exact diagnostics before each move.
- [x] Created the Stage 99 registry/two schemas and moved existing document
  validators to this authority with bounded strict reads and staged-index/
  worktree drift detection.
- [x] Converted Stage 01 to flat Requirement Packages. Assigned normative source
  statements in source order to `REQ-####-FR-####`, `REQ-####-NFR-####`, and
  `REQ-####-IF-####`; preserved acceptance text and full-ID trace links.
- [x] Moved the prefixed AD routes, kept the already prefix-free ADR routes, and
  reconciled ADR-0015, ADR-0018, ADR-0019, ADR-0023, ADR-0024, ADR-0025, and
  ADR-0030 according to the ADR-0030 supersession table without archiving
  superseded ADR bodies.
- [x] Converted Spec Packages and migrated unique design/test content to its
  owner. Each logical unit received a `TSK-<SPEC>-####` Task with focused
  RED/GREEN evidence, rollback, review result, and intended commit boundary;
  package READMEs remained thin routers.
- [x] Reorganized Stage 99 templates, merged PRD/SRS/Interface into Requirement,
  renamed `changes/` to `specs/`, deleted design/tests/Release templates, and
  consolidated unique support prose into the Stage 99 README.
- [x] Removed duplicate aggregate rules, embedded self-test matrices,
  exhaustive permanent fixture combinations, and unjustified current-state
  SHA pins in every touched document validator. Kept representative positives
  and independent mutation negatives under top-level `tests/`.
- [x] Added the exact migration/recovery mapping atomically with moves and proved
  full commit OID, durable-ref reachability, regular legacy blob resolution,
  bounded strict reads, and sealed digest match where applicable.
- [x] Recorded GREEN execution for:

  ```bash
  python3 -m unittest tests.test_document_strict_cutover tests.test_document_lifecycle_archive_cutover tests.test_archive_recovery
  python3 scripts/validate-document-contract-registry.py --mode strict
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

- [x] Obtained documentation-contract, architecture, Python, and security review.
- [x] Committed document authority and lifecycle as
  `refactor(governance): activate document lifecycle authority`.
- [x] Committed Requirement/Architecture/Spec route cutover and recovery evidence
  as `refactor(docs): converge SDLC packages`.
- [x] Committed templates, validator tests, fixtures, and support-prose removal as
  `refactor(validation): simplify document contracts`.

### WP-005 — Stage 05 semantic-owner review

**Files:**

- Review Stage 05 READMEs, Guides, Policies, Runbooks, Incident/Postmortem
  contracts, and Release surfaces. Record point-in-time decisions only in
  TSK-0054-0005 and its reviewed diff; do not create a Stage 90 disposition
  package, schema, or permanent corpus census.

- [ ] Confirm Guide `0010` as the retained/rewrite Guide owner and plan the
  merge/removal of Guides `0001`, `0002`, `0003`, `0006`, `0007`, `0008`, and
  `0009` after consumer cutover.
- [ ] Confirm Policies `0001`, `0003`, `0004`, `0005`, and `0007` as retained
  owners; merge `0002` into `0001` and `0006` into `0005`.
- [ ] Keep and rewrite all nine existing Runbooks as procedure owners, removing
  duplicated policy, unsafe live execution, and secret-bearing examples.
- [ ] Strengthen Incident/Postmortem role, timeline, evidence, cause,
  action-owner, due-state, and closure contracts. Route Release evidence to
  Spec Task, Git/CI/deployment evidence, or Incident/Postmortem.
- [ ] Add semantic duplicate-owner and contract tests without an exact document
  count, exhaustive fixture matrix, or permanent disposition ledger.
- [ ] Run:

  ```bash
  python3 -m unittest discover -s tests -p 'test_*document*.py'
  python3 scripts/validate-document-contract-registry.py --mode strict
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
- Create at most one bounded operations Migration only if an immutable
  historical lookup cannot be resolved through Git. Do not create per-file
  Tombstones.

- [ ] Start from the reviewed WP-005 semantic targets and re-check consumers in
  the candidate diff before mutation.
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
  python3 -m unittest discover -s tests -p 'test_*document*.py'
  python3 -m unittest tests.test_archive_recovery
  python3 scripts/validate-document-contract-registry.py --mode strict
  python3 scripts/validate-document-contract-registry.py --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-document-lifecycle.py --root . --mode staged
  bash scripts/check-secret-handling.sh
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

  Run the recovery validator only when this cutover adds a bounded Migration
  or minimal Tombstone.
- [ ] Obtain operations and security review.
- [ ] Commit: `refactor(ops): clarify operations document ownership`.

### WP-007 — Stage 90 semantic-destination review

**Files:**

- Review Stage 90 packages and their consumers by semantic family. Record the
  point-in-time destination in TSK-0054-0007 and its reviewed diff; do not
  create a permanent disposition Data package or schema.
- Retire the large reference-information-architecture SHA/FSM/current-pack
  contract and its exclusive fixtures/gates rather than porting it as the new
  owner.

- [ ] Route `cloud-examples` and relevant maintained snapshots to numbered
  Research packages, and route the learning roadmap to Stage 05 Guide `0010`.
- [ ] Mark `llm-wiki`, its generator and gates for consumer-zero deletion.
  Merge or remove older Audit packages and overlapping Data assets by semantic
  owner.
- [ ] Define terminal Stage 90 checks only for numbered date-free package
  identity, owner, lifecycle, freshness, consumers, and bounded supporting
  assets. Do not add file-count, corpus-digest, or disposition completeness
  gates.
- [ ] Run:

  ```bash
  python3 -m unittest discover -s tests -p 'test_*reference*.py'
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

- [ ] Obtain documentation and architecture review.
- [ ] Commit: `docs(references): record Stage 90 dispositions`.

### WP-008 — Stage 90 ownership cutover

The remaining Stage 90 cutover starts from WP-007's Task-local semantic review;
it does not recreate the retired RIA or a permanent disposition ledger.

**Files:**

- Modify Stage 90 indexes, current semantic packages, consumers, and focused
  semantic tests selected by WP-007.
- Remove the obsolete RIA and llm-wiki generator/gate surfaces with their
  exclusive fixtures after consumer-zero. Add one bounded Stage 98 Migration
  only if an immutable historical lookup cannot be resolved through Git.

- [ ] Reject a stale Stage 04 link, an unauthorized dated-current path, and a
  maintained generated output without safe check mode before cutover.
- [ ] Convert maintained current references to semantic undated filenames and
  move observation dates into frontmatter/source metadata.
- [ ] Merge duplicate research findings, older Audit packages, and overlapping
  Data assets into one semantic owner while preserving useful provenance.
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
  python3 -m unittest discover -s tests -p 'test_*reference*.py'
  python3 -m unittest discover -s tests -p 'test_*archive*.py'
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

  Verify a newly admitted bounded Migration or minimal Tombstone only when the
  cutover actually requires one.
- [ ] Obtain documentation, architecture, and Python review.
- [ ] Commit: `refactor(references): reconcile Stage 90 ownership`.

### WP-009 — global Stage 98 parity and recovery closure

**Files:**

- Reduce `docs/98.archive/` to README, prefix-free numbered Migrations, and
  only the minimal Tombstones required for immutable historical lookup. Git is
  the default full-body archive. Never preserve secret-bearing history through
  ordinary Stage 98; route it to incident, rotation, and explicitly approved
  history-removal handling.
- Modify archive validation/recovery and focused tests only to close global
  parity across evidence committed in WP-002, WP-004, WP-003, WP-006, and
  WP-008.

- [ ] Add semantic RED cases for an in-place sealed-record edit, a remaining
  consumer of a proposed removal, an unresolved immutable historical link,
  unsafe recovery, and an active direct Tombstone link.
- [ ] Never compact or rewrite a sealed record in place. Delete full-body
  Tombstones and redirect chains only after consumer-zero and Git recovery are
  proven; keep point-in-time decisions in the Task/diff rather than an Archive
  census.
- [ ] Retain MIG-0006 through MIG-0009 byte-for-byte in this cutover. Mark
  deletion `DEFER` until an authorized remote operation or full clone proves
  the required `origin/main` ancestry; local `main` evidence is insufficient.
- [ ] Require the minimal Migration/Tombstone fields from C-SDLC-009 and reject
  line-number hashes, full-corpus digests, current-document pins, and copied
  completed Spec/Plan/Task bodies without an approved exception.
- [ ] Create a new Migration or minimal Tombstone only when an actual immutable
  lookup cannot be resolved through Git and maintained mappings. Do not create
  one record per deletion or a meta-Migration solely to delete Migrations.
- [ ] Apply bounded object/path/decoding and sealed-byte checks only to the
  recovery lookup that remains. Route secret-bearing history through
  incident/rotation/removal rules.
- [ ] Remove direct active-document links to individual Tombstones; route human
  recovery lookup through Archive README or the relevant Migration.
- [ ] Run:

  ```bash
  python3 -m unittest tests.test_archive_validation tests.test_archive_cutover tests.test_archive_recovery tests.test_document_lifecycle_archive_cutover
  python3 scripts/archive_cutover.py --root .
  python3 scripts/validate-document-lifecycle.py --root . --mode staged
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

- [ ] Obtain archive, security, and Python review.
- [ ] Commit: `refactor(archive): minimize recovery evidence`.

### WP-010 — script, gate, fixture, and SHA ownership fixed point

**Delegation boundary:**

- Spec 0054 owns the WP-010 acceptance criteria and integration decision.
  Draft Spec 0066 at `../0066-validation-tooling-ownership/spec.md`, through
  `TSK-0066-0001`, owns execution, detailed file batches, focused tests, review
  evidence, and rollback after its activation checkpoint. The
  [Current Spec Index](../README.md#current-spec-index) owns cross-package
  navigation while the legacy standalone boundary remains current.
- Atomically move, rather than copy,
  `docs/00.agent-governance/contracts/validation-surfaces.json` and its schema
  to `scripts/validation/registry.json` and its schema. The moved contract owns
  validation responsibility, lane selection, executable entrypoints, and
  supported consumers; it is not a second registry or a per-file inventory.
- Keep point-in-time disposition in the Spec 0066 Task and reviewed diff. Do
  not create a Stage 90 census package, fixed file count, inventory digest, or
  permanent field-complete ledger for scripts, tests, fixtures, hooks, and
  pins.
- After ADR-0031 acceptance, preserve top-level `tests/` and
  `tests/fixtures/` as independent test surfaces. Production code must not
  import or read them.
- The activation owner changes `scripts/validate-links-and-owners.py` and adds
  focused coverage under top-level `tests/` before Spec 0066 becomes active.
  A delegated component is admitted only when its Spec/Plan/Task links are
  closed and package-local, the parent and delegate Specs link reciprocally,
  accepted ADR-0031 authorizes both, exactly one registry-owned parent package
  is found, lifecycle states agree, and no child standalone row exists. Tests
  reject missing reciprocity, proposed ADR authority, multiple parents,
  foreign Plan/Task links, and duplicate child authority. Existing roster
  consumers continue for unrelated rows until WP-013; this is not a broad
  bypass.

**Parent acceptance:**

- [ ] TSK-0054-0011 owns this checklist after activation while
  TSK-0066-0001 remains the sole delegated execution owner. It reviews
  committed, review-ready evidence and does not edit or claim the delegated
  implementation.
- [ ] Reject duplicate rule owners, aggregate reimplementation, production
  `--self-test`, orphan fixtures, unjustified current-state SHA pins,
  unbounded reads, missing timeouts, and staged-index/worktree ambiguity.
- [ ] Preserve SHA identity only for external immutable dependencies, sealed
  evidence bytes, or explicitly verified Git recovery.
- [ ] Require one routing owner and deterministic diagnostics without fixing
  the number of entrypoints, files, negative cases, or module lines.
- [ ] Accept Spec 0066's focused and broad validation, independent review,
  rollback evidence, and logical commits in TSK-0054-0011 before Spec 0066
  closes and WP-013 starts.

### WP-011 — responsibility topology and compatibility cutover

**Delegation boundary:**

- Spec 0066 owns the responsibility-batch implementation under `scripts/docs/`,
  `scripts/setup/`, `scripts/qa/`, `scripts/validation/`, and `scripts/lib/`.
  These responsibility domains guide placement but do not impose exactly four
  validator entrypoints.
- Preserve required CI check names until remote branch-protection evidence is
  available. Internal job commands, local lanes, and aggregate orchestration
  may simplify while retaining their observable selection and diagnostics.
- Delete a compatibility wrapper only after consumer-zero and unique-diagnostic
  checks pass. Git history is the default recovery owner; use a bounded sealed
  Migration only for a required immutable lookup that Git alone cannot
  resolve, and a minimal Tombstone only when both are insufficient.
- The retired `route_state` option is not reintroduced. Spec 0066 owns current
  executable commands and negative behaviors rather than inheriting stale
  command lines from this parent Plan.

**Activation and transfer checkpoint:**

- [ ] Only after the written design and implementation plan are reviewed and
  WP-009 and its owning Task are complete, hand off to TSK-0054-0010 as the sole
  `in-progress` Task in a separate lifecycle-valid change. TSK-0054-0010 owns
  the activation index and its evidence; TSK-0054-0011 remains `queued`. Move
  the existing Spec 0054 `standaloneExecutions` task pointer from the prior
  current parent Task to TSK-0054-0010 in that same handoff.
- [ ] While TSK-0054-0010 is the active owner, prepare one activation index that
  transitions ADR-0031 from `proposed` to `accepted`; adds its `supersedes`
  relation; changes ADR-0016, ADR-0017, ADR-0020, ADR-0021, and ADR-0022 from
  `accepted` to `superseded` with reciprocal `superseded_by: ADR-0031`; adds
  ADR-0030's two-clause scoped-amendment Traceability note without lifecycle
  supersession or status change; updates the Decisions README state and
  explanation, every current Stage 02/03 and Spec-package `Proposed ADR-0031`
  label, and the Stage 03 validator-test placement rule; updates the thin Spec
  0066 README from design-checkpoint `draft`/`queued` prose to the active
  execution projection and changes its Current Spec Index row from `Draft` to
  `Active`; adds the package-local delegated ownership rule in
  `scripts/validate-links-and-owners.py` plus focused positive and negative
  tests; verifies that Spec 0066 Plan/Task have no rendered parent Plan/Task
  link and that the router/index projections agree; changes Spec
  0066 Spec/Plan to `active` and TSK-0066-0001 to `in-progress`; changes
  TSK-0054-0010 to `done`; moves the existing Spec 0054 compatibility pointer
  from TSK-0054-0010 to TSK-0054-0011; and changes TSK-0054-0011 from `queued`
  to `in-progress` as the sole parent acceptance owner. Do not create a Spec
  0066 standalone row. All Task transitions already exist in the Stage 99
  lifecycle domain; do not edit the lifecycle registry, schema, or its code
  projection in this activation transaction.
- [ ] Validate and commit that exact index as one logical transaction. Do not
  expose an intermediate accepted-ADR, illegal Task edge, ownerless change, or
  dual-`in-progress` state inside either package. The intended concurrent pair
  is one parent Task and one delegated child Task. Until that transaction
  commits, TSK-0066-0001 remains `queued` and carries no accepted execution
  evidence.
- [ ] WP-011 completes only when Spec 0066 reports consumer-zero wrapper
  retirement, current registry/path parity, focused and broad validation,
  independent review, rollback evidence, and logical commits to
  TSK-0054-0011. All implementation, independent review, and
  acceptance-bearing focused and broad gates are committed before that Task
  records integrated acceptance. It remains `in-progress` while Spec 0066
  performs only the state closure: TSK-0066-0001 moves `in-progress → done`,
  and its Plan and Spec move `active → done`, followed by post-state lifecycle
  and diff confirmation. In the next parent handoff, move TSK-0054-0011 to
  `done` and the existing Spec 0054 compatibility pointer to queued
  TSK-0054-0013 atomically. TSK-0054-0013 may activate only in a later
  lifecycle-valid change.

### WP-012 — progress and generated-current cleanup

**Files:**

- Transfer active execution state from
  `docs/00.agent-governance/memory/progress.md` to the owning Spec Task records
  and Git history. Remove the Stage 00 memory surface after consumer-zero and
  reachable recovery proof; do not create a new global progress ledger.
- Verify the four graphify retirements advanced to WP-003 under C-SDLC-009;
  do not recreate their outputs or repeat their recovery record. Other
  generated-current cleanup still requires its own current-consumer and
  reproducibility proof plus Git recovery. Add Stage 98 evidence only when an
  immutable historical lookup cannot otherwise be resolved.
- Modify only the indexes, ignores, contracts, tests, and current links needed
  for that recovery boundary.

- [x] Restored the transferred intent of Spec 0052 WORK-113 without leaving a
  competing queued item, as recorded by terminal TSK-0054-0012.
- [x] Proved the old progress path recoverable, assigned current Task owners,
  and retired the progress-prefix and whole-file SHA validators. The terminal
  Task records three bounded residuals rather than claiming forced completion.
- [x] Ran the closing validation recorded by TSK-0054-0012 and its commits:

  ```bash
  python3 -m unittest discover -s tests -p 'test_*archive*.py'
  python3 -m unittest discover -s tests -p 'test_*document*.py'
  python3 scripts/validate-document-contract-registry.py --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-document-lifecycle.py --root . --mode staged
  python3 scripts/validate-affected-surfaces.py --root .
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```
- [x] Recorded the review limitation: the historical execution was
  self-reviewed and had no second reviewer. This is evidence about that closed
  exception, not a precedent that relaxes current review requirements.
- [x] Closed the Task through `aeb22636` and `eb68a4fe`; its logical
  implementation commits remain listed in TSK-0054-0012. Do not rerun WP-012.

### WP-013 — current corpus and transition-control cutover

**Files:**

- Enter only after ADR-0031 is accepted with its reciprocal evidence and Spec
  0054 has accepted the completed Spec 0066 result. That result is an immutable
  dependency boundary: Spec 0066 no longer mutates registry, runner, wrapper,
  pin, test, or fixture surfaces while WP-013 owns the remaining transition
  closure.
- Re-check the named Stage 01, 02, 03, and 99 dispositions against current
  consumers immediately before mutation. These names are the reviewed cutover
  candidate, not a permanent corpus-count invariant.
- Retain and rewrite Requirement Packages `0001` through `0004`. Transfer any
  unique current requirement or trace link from `0005` through `0008` to those
  owners, then remove `0005` through `0008` only at consumer-zero.
- Retain and update Architecture Descriptions `0004` through `0007`. Transfer
  current traceability from Descriptions `0008` through `0011`, then retire
  those four descriptions. Keep every ADR body in the Stage 02 decision log
  with accurate lifecycle and reciprocal supersession relations.
- Retain Spec Packages `0004`, `0005`, `0008`, `0054`, and delegated `0066` as
  the reviewed current-owner set. For every other Stage 03 package, first
  transfer unfinished work and unique current authority or prove it obsolete,
  completed, duplicated, or conflicting; then remove it from the current tree
  with Git-first recovery.
- Reduce Stage 99 to the human router, authored profiles, normalized top-level
  `lifecycleDomains`, required schemas, and templates used by retained
  profiles. Remove `programLineage.programs`, `referenceCurrentPacks`,
  `standaloneExecutions`, the data-model and full-body archive templates, and
  stale progress/memory forms after their current consumers move. The Spec
  0054 pointer rotations above are a bounded compatibility bridge, not a new
  authority; remove that row and its consumers rather than adding a Spec 0066
  row.
- Re-evaluate the taxonomy transition manifest, migration tool, and
  transition-only tests against the accepted Spec 0066 routing and consumer
  graph. Migrate remaining consumers to their current semantic owners and
  delete those assets only after consumer-zero; do not preserve the retired
  RIA as an intermediary.

- [ ] Add RED cases that reject a removed current owner,
  unresolved trace or template consumer, duplicate-purpose retained document,
  execution-instance roster, full-body archive template, and document reference
  or executable consumer of a retired transition asset.
- [ ] Move terminal invariants and unfinished work to the current semantic
  document, registry, production module, Spec Task, or focused behavioral test
  before removing a source.
- [ ] Prove current consumers zero and recovery from reachable Git history.
  Add one bounded Migration only when an immutable lookup cannot be resolved
  through Git, and one minimal Tombstone only when both are insufficient.
- [ ] Delete the transition manifest/tool and transition-only tests after
  consumer-zero against the accepted Spec 0066 result. Assert current
  document/registry parity and absence of transition authority without a fixed
  script or document count.
- [ ] Reject retired Stage 01/02/03/99 owners, the transition profile,
  manifest, tool, and every live three-digit/Stage 04 residue without
  recreating a `route_state` field or a permanent corpus census.
- [ ] Run:

  ```bash
  python3 -m unittest discover -s tests -p 'test_*.py'
  python3 scripts/validate-document-contract-registry.py --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-document-lifecycle.py --root . --mode staged
  python3 scripts/validate-affected-surfaces.py --root .
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  TMPDIR=/tmp pre-commit run
  ```
- [ ] Obtain architecture, documentation, Python, archive, and code-quality
  review.
- [ ] Commit the Stage 01/02 owner and traceability cutover as
  `refactor(docs): converge requirements and architecture corpus`.
- [ ] Commit the Stage 03 unfinished-work transfer and current-owner cutover as
  `refactor(specs): converge current execution packages`.
- [ ] Commit the Stage 99 profile/lifecycle/template reduction as
  `refactor(templates): reduce document control plane`.
- [ ] Commit taxonomy transition consumer-zero retirement as
  `refactor(validation): retire taxonomy transition controls`.

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
convergence. The retired `route_state` interface is never reintroduced; the
current registry and executable paths define the validated state.

The owner creates NUL-delimited, normalized path files for the exact affected
and staged scopes and invokes the lanes without shell reconstruction. These
temporary path files are execution inputs, not durable SHA-pinned evidence:

```bash
python3 scripts/run-validation-lane.py --root . --lane affected --paths-file /tmp/spec-0054-affected.nul --delimiter nul
python3 scripts/run-validation-lane.py --root . --lane staged --paths-file /tmp/spec-0054-staged.nul --delimiter nul
TMPDIR=/tmp pre-commit run
```

The terminal minimum is:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/validate-document-contract-registry.py --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-document-lifecycle.py --root . --mode staged
python3 scripts/validate-affected-surfaces.py --root .
TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
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
| Stage 90 cleanup destroys provenance | Task-local semantic disposition, current-consumer cutover, and Git recovery precede removal; add Stage 98 only for an unresolved immutable lookup and never rewrite sealed bytes |
| Governance adapters drift from canonical semantics | `.agents` owns neutral semantics; adapters carry provider-native metadata only; parity tests cover Codex and Claude |
| Script deletion breaks hidden consumers | Tracked consumer sweep plus consumer-zero and unique-diagnostic checks precede each deletion |
| Guide/Runbook consolidation removes necessary audiences | Purpose and trigger matrix reviewed by operations and documentation reviewers |
| Large validator files become harder to maintain | Split touched modules when responsibility, duplication, or change risk warrants it, and centralize bounded I/O in `scripts/lib/`; line counts remain review signals rather than policy gates |
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
  has reachable Git recovery; Stage 98 exists only for a required immutable
  lookup that Git alone cannot resolve.
- Every validation-registry command and route resolves, and dynamic discovery
  proves every production validator is reachable without turning the
  routing-only registry into a tracked-path census. There are no duplicate rule
  owners, production self-tests, orphan fixtures, unexplained current-state SHA
  pins, or expired compatibility wrappers.
- All required validation and independent review gates pass without mutation.
- Each logical work package is represented by its own commit.

## Traceability

### Lifecycle Traceability

For VAL-SDLC-010 through VAL-SDLC-012, TSK-0054-0010 and
TSK-0054-0011 own the pending transfer and parent acceptance relation;
TSK-0066-0001 owns delegated execution evidence after activation. The parent
Tasks do not claim delegated implementation evidence: TSK-0054-0010 closes the
activation transfer, and TSK-0054-0011 records only the integrated acceptance
before it transitions to `done`.

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-SDLC-001](spec.md#success-criteria--verification-plan) | WP-001, WP-002, WP-004, WP-003, WP-006, WP-008, WP-009, WP-011, WP-013, WP-014 | [TSK-0054-0001](tasks/tsk-0001-approved-design-authority.md), [TSK-0054-0002](tasks/tsk-0002-terminal-topology-and-four-digit-identity.md), [TSK-0054-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [TSK-0054-0003](tasks/tsk-0003-codex-claude-only-ai-agent-governance.md), [TSK-0054-0006](tasks/tsk-0006-stage-05-ownership-cutover.md), [TSK-0054-0008](tasks/tsk-0008-stage-90-ownership-cutover.md), [TSK-0054-0009](tasks/tsk-0009-global-stage-98-parity-and-recovery-closure.md), [TSK-0054-0011](tasks/tsk-0011-responsibility-topology-and-compatibility-cutover.md), [TSK-0054-0013](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-002](spec.md#success-criteria--verification-plan) | WP-002, WP-004, WP-006, WP-008, WP-009, WP-013, WP-014 | [TSK-0054-0002](tasks/tsk-0002-terminal-topology-and-four-digit-identity.md), [TSK-0054-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [TSK-0054-0006](tasks/tsk-0006-stage-05-ownership-cutover.md), [TSK-0054-0008](tasks/tsk-0008-stage-90-ownership-cutover.md), [TSK-0054-0009](tasks/tsk-0009-global-stage-98-parity-and-recovery-closure.md), [TSK-0054-0013](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-003](spec.md#success-criteria--verification-plan) | WP-002, WP-004, WP-005, WP-006, WP-014 | [TSK-0054-0002](tasks/tsk-0002-terminal-topology-and-four-digit-identity.md), [TSK-0054-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [TSK-0054-0005](tasks/tsk-0005-stage-05-responsibility-ledger.md), [TSK-0054-0006](tasks/tsk-0006-stage-05-ownership-cutover.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-004](spec.md#success-criteria--verification-plan) | WP-002, WP-004, WP-013, WP-014 | [TSK-0054-0002](tasks/tsk-0002-terminal-topology-and-four-digit-identity.md), [TSK-0054-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [TSK-0054-0013](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-005](spec.md#success-criteria--verification-plan) | WP-003, WP-014 | [TSK-0054-0003](tasks/tsk-0003-codex-claude-only-ai-agent-governance.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-006](spec.md#success-criteria--verification-plan) | WP-004, WP-013, WP-014 | [TSK-0054-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [TSK-0054-0013](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-007](spec.md#success-criteria--verification-plan) | WP-005, WP-006, WP-014 | [TSK-0054-0005](tasks/tsk-0005-stage-05-responsibility-ledger.md), [TSK-0054-0006](tasks/tsk-0006-stage-05-ownership-cutover.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-008](spec.md#success-criteria--verification-plan) | WP-007, WP-008, WP-014 | [TSK-0054-0007](tasks/tsk-0007-stage-90-disposition-ledger.md), [TSK-0054-0008](tasks/tsk-0008-stage-90-ownership-cutover.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-009](spec.md#success-criteria--verification-plan) | WP-002, WP-004, WP-003, WP-006, WP-008, WP-009, WP-011, WP-012, WP-013, WP-014 | [TSK-0054-0002](tasks/tsk-0002-terminal-topology-and-four-digit-identity.md), [TSK-0054-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [TSK-0054-0003](tasks/tsk-0003-codex-claude-only-ai-agent-governance.md), [TSK-0054-0006](tasks/tsk-0006-stage-05-ownership-cutover.md), [TSK-0054-0008](tasks/tsk-0008-stage-90-ownership-cutover.md), [TSK-0054-0009](tasks/tsk-0009-global-stage-98-parity-and-recovery-closure.md), [TSK-0054-0011](tasks/tsk-0011-responsibility-topology-and-compatibility-cutover.md), [TSK-0054-0012](tasks/tsk-0012-progress-and-generated-current-cleanup.md), [TSK-0054-0013](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-010](spec.md#success-criteria--verification-plan) | WP-010, WP-011, WP-012, WP-013, WP-014 | `TSK-0066-0001` (delegated execution), [TSK-0054-0010](tasks/tsk-0010-script-gate-fixture-and-sha-ownership-fixed-point.md), [TSK-0054-0011](tasks/tsk-0011-responsibility-topology-and-compatibility-cutover.md), [TSK-0054-0012](tasks/tsk-0012-progress-and-generated-current-cleanup.md), [TSK-0054-0013](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-011](spec.md#success-criteria--verification-plan) | WP-004, WP-003, WP-005, WP-006, WP-007, WP-008, WP-009, WP-010, WP-011, WP-012, WP-013, WP-014 | `TSK-0066-0001` (delegated execution), [TSK-0054-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [TSK-0054-0003](tasks/tsk-0003-codex-claude-only-ai-agent-governance.md), [TSK-0054-0005](tasks/tsk-0005-stage-05-responsibility-ledger.md), [TSK-0054-0006](tasks/tsk-0006-stage-05-ownership-cutover.md), [TSK-0054-0007](tasks/tsk-0007-stage-90-disposition-ledger.md), [TSK-0054-0008](tasks/tsk-0008-stage-90-ownership-cutover.md), [TSK-0054-0009](tasks/tsk-0009-global-stage-98-parity-and-recovery-closure.md), [TSK-0054-0010](tasks/tsk-0010-script-gate-fixture-and-sha-ownership-fixed-point.md), [TSK-0054-0011](tasks/tsk-0011-responsibility-topology-and-compatibility-cutover.md), [TSK-0054-0012](tasks/tsk-0012-progress-and-generated-current-cleanup.md), [TSK-0054-0013](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-012](spec.md#success-criteria--verification-plan) | WP-001, WP-002, WP-004, WP-003, WP-005, WP-006, WP-007, WP-008, WP-009, WP-010, WP-011, WP-012, WP-013, WP-014 | `TSK-0066-0001` (delegated execution), [TSK-0054-0001](tasks/tsk-0001-approved-design-authority.md), [TSK-0054-0002](tasks/tsk-0002-terminal-topology-and-four-digit-identity.md), [TSK-0054-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [TSK-0054-0003](tasks/tsk-0003-codex-claude-only-ai-agent-governance.md), [TSK-0054-0005](tasks/tsk-0005-stage-05-responsibility-ledger.md), [TSK-0054-0006](tasks/tsk-0006-stage-05-ownership-cutover.md), [TSK-0054-0007](tasks/tsk-0007-stage-90-disposition-ledger.md), [TSK-0054-0008](tasks/tsk-0008-stage-90-ownership-cutover.md), [TSK-0054-0009](tasks/tsk-0009-global-stage-98-parity-and-recovery-closure.md), [TSK-0054-0010](tasks/tsk-0010-script-gate-fixture-and-sha-ownership-fixed-point.md), [TSK-0054-0011](tasks/tsk-0011-responsibility-topology-and-compatibility-cutover.md), [TSK-0054-0012](tasks/tsk-0012-progress-and-generated-current-cleanup.md), [TSK-0054-0013](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md), [TSK-0054-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
