---
title: 'SDLC Document and AI Agent Governance Consolidation Implementation Plan'
version: "1.0.0"
type: sdlc/plan
layer: "specs"
status: active
owner: platform
updated: 2026-09-01
artifact_id: "SPEC-0054-PLAN-0001"
---

# SDLC Document and AI Agent Governance Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:executing-plans` for inline execution. Use
> `superpowers:subagent-driven-development` only when the human explicitly
> requests delegated agent work. Each task requires specification review,
> code-quality review, and focused RED/GREEN evidence. Each independently
> testable logical unit gets one scoped commit; a WP may own ordered commits.
> Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Converge the repository on flat four-digit Requirement Packages,
prefix-free Architecture and Operations paths, work-unit-local Spec-driven
execution, Codex/Claude-only AI-agent governance, a bounded Stage 90 reference
library, an isolated historical Stage 98 archive, a minimal Stage 99 document
control surface, and responsibility-oriented validation modules.

**Architecture:** Stage 00 owns human agent policy, while `.agents/registry.json`
owns the provider-neutral agent roster and Stage 99 owns only document
profiles. Stage 01 Requirement Packages, Stage 02 Architecture, and Stage 03
Spec Packages form the active delivery chain; Stage 05 owns Guides, Policies,
Runbooks, and Incident packages but no Release family. Stage 90 retains the
latest externally researched pack as its durable evidence collection and
removes obsolete Audit/Data control-plane copies without banning those
reference roles; Stage 98 is an isolated historical archive with no inbound
current-document links. Focused validators consume these owners, aggregates
only orchestrate, and every cutover is staged-index-aware, fail-closed, and
committed as an independently testable logical unit.

**Tech Stack:** Markdown, JSON/JSON Schema, Python 3 standard library, shell,
Git index/object APIs, unittest, pre-commit, and repository quality gates.

**Spec:**
`docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md`

## Global Constraints

- Preserve Git history and unrelated user changes.
- Do not edit existing immutable Stage 98 envelopes or source blobs to satisfy
  current validators. Remove redundant records only in WP-009 after WP-013
  removes active citations and Git recovery is confirmed. Do not require
  remote or mutable-branch ancestry as current policy.
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
- Use Stage 90 for Audit, external Research, Data, and other bounded
  non-authoritative workspace references. Remove the existing Audit/Data
  bodies only because their reviewed current purpose is obsolete or
  duplicated. Remove the existing `cloud-examples`, `learning`, and `llm-wiki`
  bodies after consumer cutover; do not misclassify the learning roadmap as an
  operational Guide or create a replacement package without a distinct
  current owner.
- Treat Stage 98 as an isolated historical archive. Stages 00, 01, 02, 03, 05,
  and 90 must neither cite nor cross-link a Stage 98 document or file. Keep
  validation minimal, treat `migrations/` as temporary historical material,
  and use Git history as the default full-body recovery source.
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
  current consumer is migrated and Git recovery is proven. Do not create a
  Stage 98 record as a routine deletion dependency.
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

Spec 0054 remains the integration and acceptance owner. Active `SPEC-0066` is
the delegated execution package for WP-010 and WP-011; its current execution
record is `SPEC-0066-TSK-0001`. Cross-package navigation is owned by the
[Current Spec Index](../README.md#current-spec-index). The relation is governed by
[accepted ADR-0031](../../02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md).
It is not a standalone program.

After written-design approval and completion of WP-006 and WP-008,
SPEC-0054-TSK-0010 became the sole `in-progress` parent activation owner in a
separate lifecycle-valid handoff. It then completed one atomic activation
transaction before delegated execution began. That transaction accepted
ADR-0031; moved ADR-0016/0017/0020/0021/0022 from `accepted` to `superseded`
with reciprocal ADR-0031 relations; added the two-clause ADR-0030 amendment
evidence without changing ADR-0030 status; aligned the Decisions README,
current ADR-0031 labels, Stage 03 test-placement rule, Spec 0066 router, and
Current Spec Index; added the narrow delegated-component ownership gate and
focused tests; activated Spec/Plan/Task 0066; completed SPEC-0054-TSK-0010; moved
the existing Spec 0054 row to SPEC-0054-TSK-0011; and moved that Task from `queued`
to `in-progress` as the sole parent acceptance owner. SPEC-0066-TSK-0001 did not
execute or partially own the transaction that activated it, and no standalone
Spec 0066 row was created.

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
- Isolate and minimize Stage 98 as historical material with only bounded
  safety/readability checks; do not make a record a current-document or
  deletion dependency.
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
| WP-007 | Review Stage 90 semantic destinations | WP-003 | Agent governance closure complete and direct user preservation boundary recorded | Latest external-research owner and Audit/Data removals reviewed in the Task/diff; permanent RIA census contract rejected |
| WP-008 | Reconcile Stage 90 semantic owners | WP-007 | Stage 90 destination review complete | Latest external-research content preserved; obsolete audit, data, RIA, and dependent gate overlap removed |
| WP-009 | Isolate and minimize Stage 98 | WP-013 | Active Archive citations and cross-links are zero; Git recovery is confirmed | Historical records receive only minimal validation; redundant full-body/redirect records and empty historical families are removed |
| WP-010 | Close the script, gate, fixture, and SHA ownership graph through delegated Spec 0066 | WP-006, WP-008, and approved written design | Stage 05 and Stage 90 cutovers complete; existing validation-surface contract and consumers mapped | Delegated Task evidence proves one routing owner, removes safe duplicates, and reports acceptance to Spec 0054 |
| WP-011 | Cut over compatibility wrappers and scripts topology through delegated Spec 0066 | WP-010 within Spec 0066 | Wrapper and path consumers mapped | Responsibility directories active; wrappers deleted only at consumer-zero; SPEC-0054-TSK-0011 records parent acceptance; no fixed census policy |
| WP-012 | Rotate progress and remove stale generated-current residue | WP-011 | Earlier program evidence stable | Spec Task/Git evidence and generated-current ownership GREEN |
| WP-013 | Cut over the remaining current corpus and close transition references | WP-012; WP-006; WP-008; accepted and completed Spec 0066 result; completed SPEC-0054-TSK-0011 parent handoff | ADR-0031 accepted; SPEC-0066-TSK-0001, Plan 0066, and Spec 0066 are `done`; SPEC-0054-TSK-0011 is `done`; the existing Spec 0054 compatibility pointer names queued SPEC-0054-TSK-0013 | Stage 01/02/03/99 disposition, zero active Archive citations/cross-links, residual transition consumer-zero, and Git-first recovery GREEN |
| WP-014 | Final convergence and branch completion | WP-009, WP-013, and accepted Spec 0066 result | All logical commits present | Ownership/fixed-point/focused/affected/staged/aggregate/all-files/review GREEN |

WP-012 is a closed historical scheduling exception, not a reusable dependency
rule. Its terminal Task keeps the originally declared WP-011 dependency and is
not rewritten. It executed before WP-011 under direct human approval on
2026-08-30, after Spec 0052 `WORK-113` had transferred and Spec 0064 had
recorded the `VAL-AGS-002` blocker. This record explains existing Git evidence;
it grants no current or future Task authority to bypass a declared dependency.

On 2026-08-31 the user directly prioritized Stage 90 cleanup after WP-003 and
required preservation of the latest externally researched material under
`docs/90.references/research/0001-workspace-engineering/`. WP-007 and WP-008 therefore run
before queued WP-005 and WP-006. After WP-008, the active pointer returns to
WP-005. After WP-006, WP-010 activates delegated Spec 0066. WP-013 removes the
remaining current-corpus conflicts and every active citation or cross-link to
Stage 98 before WP-009 minimizes that isolated historical archive. This order
prevents Archive cleanup from preserving the very inbound dependencies that
the approved terminal contract rejects.

Work follows the dependency table, not one global closed order. Each Spec
Package may have at most one `in-progress` Task. After the reviewed activation
checkpoint, Spec 0066 may execute its own WP-001 through WP-012 plan for the
delegated parent WP-010/WP-011 scope while SPEC-0054-TSK-0011 remains Spec 0054's
sole parent acceptance Task. No unrelated Spec 0054 Task runs in that window;
parent WP-014 later joins both results. Parent WP-001 and WP-002 remain
completed evidence and are not re-entered.

WP-004 migrates the transitional `tasks.md` ledger without renumbering its
work packages. The lossless identity map is:

| Plan label | Terminal Task ID | Initial terminal status |
| --- | --- | --- |
| WP-001 | SPEC-0054-TSK-0001 | done |
| WP-002 | SPEC-0054-TSK-0002 | done |
| WP-003 | SPEC-0054-TSK-0003 | in-progress |
| WP-004 | SPEC-0054-TSK-0004 | done |
| WP-005 | SPEC-0054-TSK-0005 | queued |
| WP-006 | SPEC-0054-TSK-0006 | queued |
| WP-007 | SPEC-0054-TSK-0007 | queued |
| WP-008 | SPEC-0054-TSK-0008 | queued |
| WP-009 | SPEC-0054-TSK-0009 | queued |
| WP-010 | SPEC-0054-TSK-0010 | done; completed the Spec 0066 activation transaction |
| WP-011 | SPEC-0054-TSK-0011 | in-progress; current parent acceptance owner for delegated Spec 0066 execution |
| WP-012 | SPEC-0054-TSK-0012 | done |
| WP-013 | SPEC-0054-TSK-0013 | queued |
| WP-014 | SPEC-0054-TSK-0014 | queued |

SPEC-0054-TSK-0011 has an earlier lifecycle activation dependency than the
delegated WP-011 implementation: it starts only as the parent acceptance owner
after the SPEC-0054-TSK-0010 activation transaction. Spec 0066 WP-011
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
  `standaloneExecutions` roster; accepted ADR-0031 replaces it with
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
- The completed historical cutover paired moves and deletions with its
  then-current recovery evidence. Current work relies on reachable Git history
  and does not reuse that historical mapping as a dependency.

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

WP-003 remains `in-progress`. WP-004 supplied the document registry,
lifecycle, Task, and generic recovery prerequisites at
`bb55a1ae93c9fc3017f64b5f2246af11442265d3`. This section is the current
execution contract; the long candidate/index checkpoint narrative in the Task
is historical Git evidence, not pending work.

**Landed baseline:**

- Commit `74817983629850a6e5a22a78285083342c01e37d` established the initial
  agent-governance control-plane cutover. Commit
  `e8bb831926b28c90639aed267d0c538857cffafc` completed the current
  `.agents/registry.json` and schema authority, thin Codex/Claude projections,
  Stage 00 policy/role/provider routing, Gemini/Antigravity consumer removal,
  and its then-required recovery evidence. Later current-tree commits closed
  the memory/progress and document-contract residue without reopening a third
  provider.
- The current tracked tree has no root `GEMINI.md`, `.gemini/**`,
  `.agents/GEMINI.md`, or Gemini provider document. The registry names only
  Codex and Claude, and the focused registry, provider-evidence, semantic, and
  governance-CI production gates pass. These are repository-static facts, not
  provider-runtime or hosted-CI claims.
- The authority/projection cutover is therefore not re-executed and no
  predecessor candidate is restaged. Historical path and byte recovery remains
  in reachable Git history.

**Deferred to ADR-0031-activated Spec 0066:**

- moving the validation-surface registry and schema to their responsibility
  path;
- separating production `--self-test` branches and production fixture reads
  into independent top-level tests and fixtures;
- reducing aggregates to thin routing, including the former three-terminal-
  agent-gate target; and
- retiring current-state SHA/digest pins and compatibility wrappers.

WP-003 must not duplicate those WP-010/WP-011 responsibilities before
ADR-0031 and Spec 0066 activate. Generic cumulative lifecycle behavior is
implemented and reviewed; the remaining WP-003 work is the context/memory
policy activation, closure validation, and state-only handoff.

**Completed cumulative implementation:**

- The reviewed implementation spans
  `332f0ad10cd8e8fe3f5df2f4b42dd954d2c27396` through
  `ab524c37613423555e881a0f3195ca71a89d8304`. These object IDs are execution
  evidence, not a validator allowlist or current-state pin.
- Disposable real Git fixtures prove generic cumulative creation and legal
  transition behavior in both `ci` and `explicit-ref` modes. Focused tests
  passed 14 cases; the final Archive/Migration regression run passed 74 cases
  in 167.533 seconds.
- Focused specification, Python, and static security reviews are clean after
  four fix rounds. Static security review makes no provider-runtime claim.
- Git records snapshots, not rename identity. A first-appearance commit that
  also contains a deletion is ambiguous and cannot receive cumulative
  admission. No path/SHA exception, real-path override, or new provenance
  ledger is permitted.

**Remaining files:**

- Activate
  `docs/00.agent-governance/policies/context-and-memory.md`, update its
  activation boundary, add it to the current Stage 00 policy index in
  `docs/00.agent-governance/README.md`, and replace the draft statement in
  `scripts/README.md` with the active owner relation.
- Update this Plan and SPEC-0054-TSK-0003 only with observed evidence. The final
  state-only handoff also updates SPEC-0054-TSK-0007 and the existing Spec 0054
  `standaloneExecutions` pointer in `docs/99.templates/registry.json`.

**TDD and diagnostic contract:**

- [x] **RED — actual intermediate history:** create a temporary repository in
  which the target is absent at the supplied base, created in the profile's
  zero-indegree state, and promoted through every declared edge in later
  commits. The current net comparison must expose `LIFECYCLE-CREATE`; GREEN
  must accept both `ci` and `explicit-ref` only after validating each actual
  intermediate transition.
- [x] **RED — provenance boundary:** prove in disposable real Git repositories
  that both comparison modes use committed blobs rather than checkout bytes
  and reject an ambiguous first appearance whose commit also deletes a path.
  Preserve `--include-path` as the additive selector documented by
  `scripts/README.md`; it is not a focus filter and this WP does not change its
  meaning.
- [x] **RED — fail closed:** direct active creation, an illegal intermediate
  transition, missing history, a non-ancestral range, ambiguous history, and
  malformed or bounds-exceeding Git output must remain unadmitted. Retain the
  exact existing `LIFECYCLE-CREATE` for an unproved net creation, or the
  validator's existing invocation diagnostic where resolution cannot proceed;
  do not require a new diagnostic ID or exit code. No checkout bytes,
  branch-name rule, fixed commit list, or target-path exception may substitute
  for commit evidence.
- [x] **GREEN — bounded proof:** resolve commit objects with the existing
  strict ref/object checks; require an ancestral supplied range; enumerate a
  bounded, uniquely ordered chain of target-affecting commits; load the target
  blob from each commit; prove `absent → initial` and then every consecutive
  declared transition; and consume only the exact `LIFECYCLE-CREATE`
  diagnostic proved by that chain. Preserve every other diagnostic and the
  existing additive include-path behavior. Ambiguous first appearances remain
  unadmitted without a waiver or separate gate.
- [x] Run focused GREEN and Archive/Migration lifecycle regressions:

  ```bash
  python3 -m unittest tests.test_document_lifecycle_cumulative_history
  python3 -m unittest tests.test_document_lifecycle_archive_cutover tests.test_document_lifecycle_migration
  ```

  The focused run passed 14 tests. The final Archive/Migration run passed 74
  tests in 167.533 seconds.
- [x] Complete focused specification, Python, and static security review over
  commits `332f0ad10cd8e8fe3f5df2f4b42dd954d2c27396` through
  `ab524c37613423555e881a0f3195ca71a89d8304`; all four fix rounds are clean.

**Activation and cumulative proof:**

- [x] Commit the generic lifecycle behavior and four reviewed correction rounds
  from `332f0ad10cd8e8fe3f5df2f4b42dd954d2c27396` through
  `ab524c37613423555e881a0f3195ca71a89d8304`.
- [x] In a second logical unit, change the context/memory policy from `draft`
  to `active`, remove its waiting language, and update the Stage 00 and scripts
  routers. Pass staged lifecycle and strict document checks, then commit this
  activation without changing either Task state.
- [x] Resolve the activation and its clean committed draft parent to full
  object IDs, record them in SPEC-0054-TSK-0003 as execution evidence rather than a
  code/config allowlist, and run both modes over the actual adjacent ranges:

  ```bash
  ACTIVATION_COMMIT="$(git rev-parse HEAD)"
  DRAFT_BASE_COMMIT="$(git rev-parse "${ACTIVATION_COMMIT}^")"
  git cat-file -e "${ACTIVATION_COMMIT}^{commit}"
  git cat-file -e "${DRAFT_BASE_COMMIT}^{commit}"
  git merge-base --is-ancestor "${DRAFT_BASE_COMMIT}" "${ACTIVATION_COMMIT}"
  python3 scripts/validate-document-lifecycle.py --root . --mode ci --base-ref "${DRAFT_BASE_COMMIT}" --to-ref "${ACTIVATION_COMMIT}" --include-path docs/00.agent-governance/policies/context-and-memory.md
  python3 scripts/validate-document-lifecycle.py --root . --mode explicit-ref --from-ref "${DRAFT_BASE_COMMIT}" --to-ref "${ACTIVATION_COMMIT}" --include-path docs/00.agent-governance/policies/context-and-memory.md
  ```

  The CLI pair proves only the clean committed `draft → active` edge.
  Disposable real-Git fixtures already prove generic cumulative behavior in
  both modes. The whole approved-base-to-activation comparison, including any
  real-path `absent → draft → active` claim, remains unclaimed and deferred
  until WP-009 removes archive/legacy cutover overreach. It is neither waived
  nor a PASS.

**Closure checks, reviews, and handoff:**

- [x] Re-run the current agent authority gates and document checks:

  ```bash
  python3 -m unittest discover -s tests -p 'test_validate_agent_*.py'
  python3 scripts/validate-agent-harness-contract.py --root .
  python3 scripts/validate-agent-provider-evidence.py --root .
  python3 scripts/validate-agent-harness-semantics.py --root .
  python3 scripts/validate-agent-governance-ci.py --root .
  python3 scripts/validate-document-contract-registry.py --root . --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-document-lifecycle.py --root . --mode staged
  python3 scripts/validate-affected-surfaces.py --root .
  bash scripts/check-secret-handling.sh
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  git diff --cached --name-only -z > /tmp/spec-0054-wp003-staged.nul
  python3 scripts/run-validation-lane.py --root . --lane staged --paths-file /tmp/spec-0054-wp003-staged.nul --delimiter nul
  TMPDIR=/tmp pre-commit run
  TMPDIR=/tmp pre-commit run --all-files
  git diff --check
  git diff --cached --check
  ```

- [x] Obtain independent specification, code-quality, Python, and static
  security review for the policy activation, closure evidence, and state-only
  handoff. Resolve every Critical or Important finding and rerun the checks
  affected by corrections. Record that static security review makes no
  provider-runtime claim.
- [x] After every acceptance-bearing check and review passes, make one final
  state-only logical commit: set SPEC-0054-TSK-0003 to `done`, set SPEC-0054-TSK-0007 to
  `in-progress`, and move the existing Spec 0054 `standaloneExecutions` task
  pointer from SPEC-0054-TSK-0003 to SPEC-0054-TSK-0007. Do not activate Spec 0066 or
  modify another Spec 0054 Task in this handoff.

**Rollback:** stop before the state-only handoff on any failed proof. With
authorization, revert only the failing logical unit: router/policy activation
first, then cumulative-history behavior if necessary. After handoff, revert
the state-only commit before reverting activation. Do not reset shared history,
edit retained historical records, or restore Gemini/Antigravity surfaces.

### WP-004 — document, lifecycle, Task, and registry authority activation

WP-004 is completed historical execution. It established the owners required
by later work and superseded the conflicting terminal assumptions of completed
WP-002 without rewriting that evidence. Its accepted Task and commits are the
execution record; no historical Archive record is regenerated. Terminal corpus
reductions introduced by accepted ADR-0031 are prospective WP-013 work, not a
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
- Recorded the then-required authority/path recovery evidence. Current work
  uses reachable Git history and neither recreates nor cites that historical
  record as a dependency.
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
- [x] Added the then-required recovery mapping atomically with moves and proved
  full commit OID, durable-ref reachability, regular legacy blob resolution,
  bounded strict reads, and sealed digest match where applicable. The current
  rule retains only the reachable Git recovery principle.
- [x] Recorded GREEN execution for:

  ```bash
  python3 -m unittest tests.test_document_strict_cutover tests.test_document_lifecycle_archive_cutover tests.test_archive_recovery
  python3 scripts/validate-document-contract-registry.py --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-document-lifecycle.py --root . --mode staged
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
  SPEC-0054-TSK-0005 and its reviewed diff; do not create a Stage 90 disposition
  package, schema, or permanent corpus census.

- [x] Confirm Guide `0010` as the retained/rewrite Guide owner and plan the
  merge/removal of Guides `0001`, `0002`, `0003`, `0006`, `0007`, `0008`, and
  `0009` after consumer cutover. Guide `0009` was already removed by WP-008;
  the remaining six procedural Guides route to their reviewed Runbook/Policy
  owners in WP-006.
- [x] Confirm Policies `0001`, `0003`, `0004`, `0005`, and `0007` as retained
  owners; merge `0002` into `0001` and `0006` into `0005`.
- [x] Keep and rewrite all nine existing Runbooks as procedure owners, removing
  duplicated policy, unsafe live execution, and secret-bearing examples.
- [x] Strengthen Incident/Postmortem role, timeline, evidence, cause,
  action-owner, due-state, and closure contracts. Route Release evidence to
  Spec Task, Git/CI/deployment evidence, or Incident/Postmortem.
- [x] Define bounded WP-006 semantic duplicate-owner and contract negatives
  without an exact document count, exhaustive fixture matrix, permanent
  disposition ledger, or one gate per retired document.
- [x] Run:

  ```bash
  python3 -m unittest discover -s tests -p 'test_*document*.py'
  python3 scripts/validate-document-contract-registry.py --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-affected-surfaces.py --root .
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

- [x] Obtain execution-owner operations and documentation diff review. No
  delegated review was requested for this point-in-time disposition.
- [x] Commit: `docs(ops): record operations document dispositions`.

### WP-006 — Stage 05 ownership cutover

**Files:**

- Modify the Stage 05 READMEs and only the Guide, Policy, Runbook, Incident,
  Postmortem, and Release records authorized by WP-005.
- Modify affected Stage 05 templates, registry body contracts, hooks, fixtures,
  indexes, and current links. Preserve only WP-002's lowercase Incident
  grammar; supersede its prefixed Guide/Policy/Runbook routes.
- Do not create an Archive record, redirect, or body copy for the operations
  cutover. Reachable Git history owns full-content recovery.

- [x] Start from the reviewed WP-005 semantic targets and re-check consumers in
  the candidate diff before mutation.
- [x] Resolve the reviewed bootstrap, platform-expansion, observability,
  metrics, and GitOps-onboarding Guide/Runbook overlaps.
- [x] Strengthen Incident role/timeline/severity/evidence fields and Postmortem
  cause/action-owner/due-state/closure fields.
- [x] Rename Guide/Policy/Runbook files to prefix-free four-digit routes while
  preserving `GDE-####`, `POL-####`, and `RUN-####` frontmatter IDs.
- [x] Migrate every Release consumer to its approved evidence owner, delete the
  Release documents/directory/profile/template/fixtures/gates, and prove zero
  current consumers. Do not create a Release tombstone or redirect.
- [x] Run:

  ```bash
  python3 -m unittest discover -s tests -p 'test_*document*.py'
  python3 -m unittest tests.test_archive_recovery
  python3 scripts/validate-document-contract-registry.py --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-document-lifecycle.py --root . --mode staged
  bash scripts/check-secret-handling.sh
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

- [x] Obtain execution-owner operations and static security review backed by
  focused semantic tests, secret handling, staged validation, aggregate quality,
  and pre-commit. No live-runtime claim is accepted.
- [x] Commit: `refactor(ops): clarify operations document ownership`
  (`b8d35ff`).

### WP-007 — Stage 90 semantic-destination review

**Files:**

- Review Stage 90 packages and their consumers by semantic family. Record the
  point-in-time destination in SPEC-0054-TSK-0007 and its reviewed diff; do not
  create a permanent disposition Data package or schema.
- Retire the large reference-information-architecture SHA/FSM/current-pack
  contract and its exclusive fixtures/gates rather than porting it as the new
  owner.
- Record that Audit, external Research, Data, and other bounded reference
  material are valid Stage 90 roles. Removal decisions apply to the reviewed
  existing bodies, not to the category names themselves.

The approved preservation boundary is the current
`research/0001-workspace-engineering/` pack plus its collection and Stage 90 routers. The
34 Audit files and seven Data files are removal candidates after consumer
cutover. Later mechanical governance edits do not outrank the latest external
research commits when determining recency.

- [x] Mark `cloud-examples`, `learning`, `llm-wiki`, its generator, and its
  gates for consumer-zero deletion. Do not route the learning roadmap to Guide
  `0010`, which already owns CI/CD QA reference operations; no reviewed body in
  these families has a distinct current owner that warrants a replacement
  Research package.
- [x] Merge or remove existing Audit packages and overlapping Data assets by
  semantic owner while preserving Audit and Data as valid future Stage 90
  roles.
- [x] Define terminal Stage 90 checks only for semantic category, stable
  identity, owner, lifecycle, freshness, consumers, and bounded supporting
  assets. Preserve the current external-research path while Spec 0062 consumes
  it; do not add file-count, corpus-digest, or disposition completeness gates.
- [x] Run:

  ```bash
  python3 -m unittest discover -s tests -p 'test_*reference*.py'
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

- [x] Obtain direct human boundary review plus execution-owner documentation
  and architecture diff review. No delegated review was requested for this
  state transition.
- [x] Commit: `docs(references): record Stage 90 dispositions` (`16a8038`).

### WP-008 — Stage 90 ownership cutover

The remaining Stage 90 cutover starts from WP-007's Task-local semantic review;
it does not recreate the retired RIA or a permanent disposition ledger.

**Files:**

- Modify Stage 90 indexes, current semantic packages, consumers, and focused
  semantic tests selected by WP-007.
- Remove the obsolete RIA and llm-wiki generator/gate surfaces with their
  exclusive fixtures after consumer-zero. Do not create an Archive record or
  redirect; reachable Git history owns removed full bodies.

- [x] Reject a stale Stage 04 link, an unauthorized dated-current path, and a
  maintained generated output without safe check mode before cutover.
- [x] Convert any newly retained current reference to a semantic undated
  filename and move observation dates into frontmatter/source metadata. Keep
  the approved `research/0001-workspace-engineering/` path stable while Spec 0062 consumes
  it.
- [x] Preserve the current `research/0001-workspace-engineering/` external-research pack's
  external sources, observations, and claims through the Audit/Data cutover.
  Permit only the numbering cutover, frontmatter normalization, link repair,
  and current local-implementation corrections required by the approved
  governance model. Remove Audit and Data bodies
  from the reviewed existing corpus only after their live consumers route to
  canonical Stage 00-05 owners or direct repository sources; Git remains their
  full-body recovery owner. Do not encode a ban on future valid Audit or Data
  references.
- [x] Remove `cloud-examples`, `learning`, and `llm-wiki` after routing every
  live consumer to a current semantic owner or direct source. Remove obsolete
  `res-`/`aud-` paths and redirects after consumer-zero; do not create a
  replacement document solely to preserve old content.
- [x] Ensure retained generated indexes use canonical inputs, bounded reads, check mode,
  and no write during check. A generated-output digest is allowed only when the
  output is explicitly sealed evidence, not as a current-state freshness pin.
  Remove the obsolete LLM Wiki generator and generated index instead of
  preserving a second reference control plane.
- [x] Run:

  ```bash
  python3 -m unittest discover -s tests -p 'test_*reference*.py'
  python3 -m unittest discover -s tests -p 'test_*archive*.py'
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
  ```

- [x] Obtain execution-owner documentation, architecture, and Python diff
  review backed by strict profile/link validation, 93 lifecycle tests, 223
  Archive tests, focused reference tests, and the repository quality aggregate.
- [x] Commit: `refactor(references): reconcile Stage 90 ownership`.

### WP-009 — global Stage 98 parity and recovery closure

Stage 98 is an isolated historical archive, not a current governance or
recovery control plane. Its `migrations/` directory is temporary historical
material. WP-009 starts only after WP-013 has removed every citation and
cross-link from Stages 00, 01, 02, 03, 05, and 90. Validation is limited to
retained-record safety, readability, and declared sealed-byte integrity; it
does not require a current consumer, permanent census, or remote-ancestry gate.

**Files:**

- Reduce Stage 98 to a small historical index and only the records with unique
  historical value. Git is the default full-body recovery source. Never
  preserve secret-bearing history through ordinary Stage 98; route it to
  incident, rotation, and explicitly approved history-removal handling.
- Modify archive validation/recovery and focused tests only to close global
  parity across evidence committed in WP-002, WP-004, WP-003, WP-006, and
  WP-008.

- [ ] Add semantic RED cases for an in-place sealed-record edit, an inbound
  active-stage Archive link, unsafe or unbounded reads, and a malformed
  retained record.
- [ ] Never compact or rewrite a sealed record in place. Delete full-body
  Tombstones and redirect chains after Git recovery is confirmed; keep
  point-in-time decisions in the Task/diff rather than an Archive census.
- [ ] Retain a Migration only while it supplies unique archive-internal
  historical context. Remove obsolete Migration records and empty families
  without creating a meta-Migration; do not require a mutable branch-head or
  remote-ancestry pin as current policy.
- [ ] Require the minimal Migration/Tombstone fields from C-SDLC-009 and reject
  line-number hashes, full-corpus digests, current-document pins, and copied
  completed Spec/Plan/Task bodies without an approved exception.
- [ ] Do not create a new Migration, Tombstone, redirect, or body copy during
  this cleanup. Retain or remove existing records only by archive-internal
  historical value and reachable Git recovery; never to satisfy a current
  consumer.
- [ ] Apply bounded path/decoding and sealed-byte checks only where each
  retained record declares that contract. Do not run a full Archive census,
  compare unrelated current files with historical SHAs, require an inbound
  consumer, or validate branch ancestry. Route secret-bearing history through
  incident/rotation/removal rules.
- [ ] Verify that Stages 00, 01, 02, 03, 05, and 90 contain no Archive citation
  or cross-link. Do not replace removed direct links with an Archive README or
  Migration link.
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
  Active `SPEC-0066`, through `SPEC-0066-TSK-0001`, owns execution, detailed file
  batches, focused tests, review evidence, and rollback. The
  [Current Spec Index](../README.md#current-spec-index) owns cross-package
  navigation while the legacy standalone boundary remains current.
- Atomically move, rather than copy, the validation-surface contract formerly
  under Stage 00 to `scripts/validation/registry.json` and its schema. The moved contract owns
  validation responsibility, lane selection, executable entrypoints, and
  supported consumers; it is not a second registry or a per-file inventory.
- Keep point-in-time disposition in the Spec 0066 Task and reviewed diff. Do
  not create a Stage 90 census package, fixed file count, inventory digest, or
  permanent field-complete ledger for scripts, tests, fixtures, hooks, and
  pins.
- Under accepted ADR-0031, preserve top-level `tests/` and
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

- [x] SPEC-0054-TSK-0011 owns this checklist after activation while
  SPEC-0066-TSK-0001 remains the sole delegated execution owner. It reviews
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
  rollback evidence, and logical commits in SPEC-0054-TSK-0011 before Spec 0066
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
  checks pass. Reachable Git history is the default recovery owner; do not
  create an Archive record, redirect, or body copy for wrapper retirement.
- The retired `route_state` option is not reintroduced. Spec 0066 owns current
  executable commands and negative behaviors rather than inheriting stale
  command lines from this parent Plan.

**Activation and transfer checkpoint:**

- [x] After the written design and implementation plan were reviewed and
  WP-006 and WP-008 completed, a separate lifecycle-valid handoff made
  SPEC-0054-TSK-0010 the sole `in-progress` activation owner and moved the parent
  compatibility pointer to it.
- [x] SPEC-0054-TSK-0010 prepared one activation index that moves ADR-0031 from
  `proposed` to `accepted` with its `supersedes` relation; moves ADR-0016,
  ADR-0017, ADR-0020, ADR-0021, and ADR-0022 to `superseded` with reciprocal
  `superseded_by: ADR-0031`; adds ADR-0030's two-clause scoped-amendment trace
  without changing its accepted status; aligns the Decisions README, current
  Stage 02/03 ADR labels, Stage 03 validator-test placement rule, Spec 0066
  router, and Current Spec Index; adds the delegated-ownership rule and focused
  cases; activates Spec/Plan/Task 0066; completes SPEC-0054-TSK-0010; moves the
  compatibility pointer to SPEC-0054-TSK-0011; and activates SPEC-0054-TSK-0011 as the
  sole parent acceptance owner. The index creates no Spec 0066 standalone row
  and makes no Stage 99 lifecycle-domain, schema, or projection change.
- [x] Validate and commit that exact index as one logical transaction without
  exposing an intermediate accepted-ADR, illegal Task edge, ownerless change,
  or dual-`in-progress` state inside either package. Focused delegated cases,
  strict cross-document validation, staged lifecycle validation,
  Archive/Recovery regression, and aggregate repository quality gates pass for
  the intended pair of one parent Task and one delegated child Task.
- [ ] WP-011 completes only when Spec 0066 reports consumer-zero wrapper
  retirement, current registry/path parity, focused and broad validation,
  independent review, rollback evidence, and logical commits to
  SPEC-0054-TSK-0011. All implementation, independent review, and
  acceptance-bearing focused and broad gates are committed before that Task
  records integrated acceptance. It remains `in-progress` while Spec 0066
  performs only the state closure: SPEC-0066-TSK-0001 moves `in-progress → done`,
  and its Plan and Spec move `active → done`, followed by post-state lifecycle
  and diff confirmation. In the next parent handoff, move SPEC-0054-TSK-0011 to
  `done` and the existing Spec 0054 compatibility pointer to queued
  SPEC-0054-TSK-0013 atomically. SPEC-0054-TSK-0013 may activate only in a later
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
  reproducibility proof plus reachable Git recovery; it does not add an
  Archive dependency.
- Modify only the indexes, ignores, contracts, tests, and current links needed
  for that recovery boundary.

- [x] Restored the transferred intent of Spec 0052 WORK-113 without leaving a
  competing queued item, as recorded by terminal SPEC-0054-TSK-0012.
- [x] Proved the old progress path recoverable, assigned current Task owners,
  and retired the progress-prefix and whole-file SHA validators. The terminal
  Task records three bounded residuals rather than claiming forced completion.
- [x] Ran the closing validation recorded by SPEC-0054-TSK-0012 and its commits:

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
  implementation commits remain listed in SPEC-0054-TSK-0012. Do not rerun WP-012.

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
  owners, then remove `0005` through `0008` only at consumer-zero. Compare the
  retained requirements with current manifests, configuration, code,
  validators, and supported operational interfaces so durable implemented
  behavior has a solution-independent Requirement owner.
- Retain and update Architecture Descriptions `0004` through `0007`. Transfer
  current traceability from Descriptions `0008` through `0011`, then retire
  those four descriptions. Reconcile every retained description with the
  actual current structure, boundaries, components, data/control/deployment
  flows, and implementation evidence. Keep every ADR body in the Stage 02
  decision log with accurate lifecycle and reciprocal supersession relations.
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
- Remove every citation and cross-link from Stages 00, 01, 02, 03, 05, and 90
  to a Stage 98 document or file. Replace current navigation with the current
  semantic owner; retain only a path-free Git-history recovery statement where
  historical recovery is relevant.

- [ ] Add RED cases that reject a removed current owner,
  unresolved trace or template consumer, duplicate-purpose retained document,
  execution-instance roster, full-body archive template, and document reference
  or executable consumer of a retired transition asset. Also reject durable
  implemented behavior with no appropriate Requirement/Architecture owner and
  a retained current Architecture claim with no repository implementation
  evidence.
- [ ] Move terminal invariants and unfinished work to the current semantic
  document, registry, production module, Spec Task, or focused behavioral test
  before removing a source.
- [ ] Prove current consumers zero and recovery from reachable Git history.
  Do not create an Archive record or redirect as part of the current-corpus
  cutover.
- [ ] Record the implementation evidence used for each retained Requirement
  Package and Architecture Description, transfer unique current facts from
  removal candidates, and correct or retire claims that conflict with the
  repository. Keep raw inventories in direct repository evidence rather than
  duplicating them in Stage 01/02 prose.
- [ ] Delete the transition manifest/tool and transition-only tests after
  consumer-zero against the accepted Spec 0066 result. Assert current
  document/registry parity and absence of transition authority without a fixed
  script or document count.
- [ ] Assert zero active Archive citations and cross-links without enumerating
  a permanent allowed-path list. Complete the state-only handoff from
  SPEC-0054-TSK-0013 to SPEC-0054-TSK-0009 only after this invariant is green.
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
- [ ] Commit active Archive-link isolation as
  `refactor(docs): isolate historical archive`.

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
| Stage 90 cleanup destroys provenance | Task-local semantic disposition, current-consumer cutover, and Git recovery precede removal; do not create an active Archive dependency or rewrite sealed bytes |
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
  has reachable Git recovery; Stage 98 is isolated historical material with
  no inbound current-document dependency and only minimal validation.
- Every retained Stage 01 Requirement Package and Stage 02 Architecture
  Description reflects the current implementation at the appropriate
  abstraction level, with no durable implemented behavior lacking an owner and
  no current architectural claim lacking implementation evidence.
- Every validation-registry command and route resolves, and dynamic discovery
  proves every production validator is reachable without turning the
  routing-only registry into a tracked-path census. There are no duplicate rule
  owners, production self-tests, orphan fixtures, unexplained current-state SHA
  pins, or expired compatibility wrappers.
- All required validation and independent review gates pass without mutation.
- Each logical work package is represented by its own commit.

## Traceability

### Lifecycle Traceability

For VAL-SDLC-010 through VAL-SDLC-012, SPEC-0054-TSK-0010 and
SPEC-0054-TSK-0011 own the pending transfer and parent acceptance relation;
SPEC-0066-TSK-0001 owns delegated execution evidence after activation. The parent
Tasks do not claim delegated implementation evidence: SPEC-0054-TSK-0010 closes the
activation transfer, and SPEC-0054-TSK-0011 records only the integrated acceptance
before it transitions to `done`.

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-SDLC-001](spec.md#success-criteria--verification-plan) | WP-001, WP-002, WP-004, WP-003, WP-006, WP-008, WP-009, WP-011, WP-013, WP-014 | [SPEC-0054-TSK-0001](tasks/tsk-0001-approved-design-authority.md), [SPEC-0054-TSK-0002](tasks/tsk-0002-terminal-topology-and-four-digit-identity.md), [SPEC-0054-TSK-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [SPEC-0054-TSK-0003](tasks/tsk-0003-codex-claude-only-ai-agent-governance.md), [SPEC-0054-TSK-0006](tasks/tsk-0006-stage-05-ownership-cutover.md), [SPEC-0054-TSK-0008](tasks/tsk-0008-stage-90-ownership-cutover.md), [SPEC-0054-TSK-0009](tasks/tsk-0009-global-stage-98-parity-and-recovery-closure.md), [SPEC-0054-TSK-0011](tasks/tsk-0011-responsibility-topology-and-compatibility-cutover.md), [SPEC-0054-TSK-0013](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md), [SPEC-0054-TSK-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-002](spec.md#success-criteria--verification-plan) | WP-002, WP-004, WP-006, WP-008, WP-009, WP-013, WP-014 | [SPEC-0054-TSK-0002](tasks/tsk-0002-terminal-topology-and-four-digit-identity.md), [SPEC-0054-TSK-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [SPEC-0054-TSK-0006](tasks/tsk-0006-stage-05-ownership-cutover.md), [SPEC-0054-TSK-0008](tasks/tsk-0008-stage-90-ownership-cutover.md), [SPEC-0054-TSK-0009](tasks/tsk-0009-global-stage-98-parity-and-recovery-closure.md), [SPEC-0054-TSK-0013](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md), [SPEC-0054-TSK-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-003](spec.md#success-criteria--verification-plan) | WP-002, WP-004, WP-005, WP-006, WP-014 | [SPEC-0054-TSK-0002](tasks/tsk-0002-terminal-topology-and-four-digit-identity.md), [SPEC-0054-TSK-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [SPEC-0054-TSK-0005](tasks/tsk-0005-stage-05-responsibility-ledger.md), [SPEC-0054-TSK-0006](tasks/tsk-0006-stage-05-ownership-cutover.md), [SPEC-0054-TSK-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-004](spec.md#success-criteria--verification-plan) | WP-002, WP-004, WP-013, WP-014 | [SPEC-0054-TSK-0002](tasks/tsk-0002-terminal-topology-and-four-digit-identity.md), [SPEC-0054-TSK-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [SPEC-0054-TSK-0013](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md), [SPEC-0054-TSK-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-005](spec.md#success-criteria--verification-plan) | WP-003, WP-014 | [SPEC-0054-TSK-0003](tasks/tsk-0003-codex-claude-only-ai-agent-governance.md), [SPEC-0054-TSK-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-006](spec.md#success-criteria--verification-plan) | WP-004, WP-013, WP-014 | [SPEC-0054-TSK-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [SPEC-0054-TSK-0013](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md), [SPEC-0054-TSK-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-007](spec.md#success-criteria--verification-plan) | WP-005, WP-006, WP-014 | [SPEC-0054-TSK-0005](tasks/tsk-0005-stage-05-responsibility-ledger.md), [SPEC-0054-TSK-0006](tasks/tsk-0006-stage-05-ownership-cutover.md), [SPEC-0054-TSK-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-008](spec.md#success-criteria--verification-plan) | WP-007, WP-008, WP-014 | [SPEC-0054-TSK-0007](tasks/tsk-0007-stage-90-disposition-ledger.md), [SPEC-0054-TSK-0008](tasks/tsk-0008-stage-90-ownership-cutover.md), [SPEC-0054-TSK-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-009](spec.md#success-criteria--verification-plan) | WP-002, WP-004, WP-003, WP-006, WP-008, WP-009, WP-011, WP-012, WP-013, WP-014 | [SPEC-0054-TSK-0002](tasks/tsk-0002-terminal-topology-and-four-digit-identity.md), [SPEC-0054-TSK-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [SPEC-0054-TSK-0003](tasks/tsk-0003-codex-claude-only-ai-agent-governance.md), [SPEC-0054-TSK-0006](tasks/tsk-0006-stage-05-ownership-cutover.md), [SPEC-0054-TSK-0008](tasks/tsk-0008-stage-90-ownership-cutover.md), [SPEC-0054-TSK-0009](tasks/tsk-0009-global-stage-98-parity-and-recovery-closure.md), [SPEC-0054-TSK-0011](tasks/tsk-0011-responsibility-topology-and-compatibility-cutover.md), [SPEC-0054-TSK-0012](tasks/tsk-0012-progress-and-generated-current-cleanup.md), [SPEC-0054-TSK-0013](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md), [SPEC-0054-TSK-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-010](spec.md#success-criteria--verification-plan) | WP-010, WP-011, WP-012, WP-013, WP-014 | `SPEC-0066-TSK-0001` (delegated execution), [SPEC-0054-TSK-0010](tasks/tsk-0010-script-gate-fixture-and-sha-ownership-fixed-point.md), [SPEC-0054-TSK-0011](tasks/tsk-0011-responsibility-topology-and-compatibility-cutover.md), [SPEC-0054-TSK-0012](tasks/tsk-0012-progress-and-generated-current-cleanup.md), [SPEC-0054-TSK-0013](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md), [SPEC-0054-TSK-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-011](spec.md#success-criteria--verification-plan) | WP-004, WP-003, WP-005, WP-006, WP-007, WP-008, WP-009, WP-010, WP-011, WP-012, WP-013, WP-014 | `SPEC-0066-TSK-0001` (delegated execution), [SPEC-0054-TSK-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [SPEC-0054-TSK-0003](tasks/tsk-0003-codex-claude-only-ai-agent-governance.md), [SPEC-0054-TSK-0005](tasks/tsk-0005-stage-05-responsibility-ledger.md), [SPEC-0054-TSK-0006](tasks/tsk-0006-stage-05-ownership-cutover.md), [SPEC-0054-TSK-0007](tasks/tsk-0007-stage-90-disposition-ledger.md), [SPEC-0054-TSK-0008](tasks/tsk-0008-stage-90-ownership-cutover.md), [SPEC-0054-TSK-0009](tasks/tsk-0009-global-stage-98-parity-and-recovery-closure.md), [SPEC-0054-TSK-0010](tasks/tsk-0010-script-gate-fixture-and-sha-ownership-fixed-point.md), [SPEC-0054-TSK-0011](tasks/tsk-0011-responsibility-topology-and-compatibility-cutover.md), [SPEC-0054-TSK-0012](tasks/tsk-0012-progress-and-generated-current-cleanup.md), [SPEC-0054-TSK-0013](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md), [SPEC-0054-TSK-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
| [VAL-SDLC-012](spec.md#success-criteria--verification-plan) | WP-001, WP-002, WP-004, WP-003, WP-005, WP-006, WP-007, WP-008, WP-009, WP-010, WP-011, WP-012, WP-013, WP-014 | `SPEC-0066-TSK-0001` (delegated execution), [SPEC-0054-TSK-0001](tasks/tsk-0001-approved-design-authority.md), [SPEC-0054-TSK-0002](tasks/tsk-0002-terminal-topology-and-four-digit-identity.md), [SPEC-0054-TSK-0004](tasks/tsk-0004-document-lifecycle-task-and-registry-authority-activation.md), [SPEC-0054-TSK-0003](tasks/tsk-0003-codex-claude-only-ai-agent-governance.md), [SPEC-0054-TSK-0005](tasks/tsk-0005-stage-05-responsibility-ledger.md), [SPEC-0054-TSK-0006](tasks/tsk-0006-stage-05-ownership-cutover.md), [SPEC-0054-TSK-0007](tasks/tsk-0007-stage-90-disposition-ledger.md), [SPEC-0054-TSK-0008](tasks/tsk-0008-stage-90-ownership-cutover.md), [SPEC-0054-TSK-0009](tasks/tsk-0009-global-stage-98-parity-and-recovery-closure.md), [SPEC-0054-TSK-0010](tasks/tsk-0010-script-gate-fixture-and-sha-ownership-fixed-point.md), [SPEC-0054-TSK-0011](tasks/tsk-0011-responsibility-topology-and-compatibility-cutover.md), [SPEC-0054-TSK-0012](tasks/tsk-0012-progress-and-generated-current-cleanup.md), [SPEC-0054-TSK-0013](tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md), [SPEC-0054-TSK-0014](tasks/tsk-0014-convergence-and-branch-completion.md) |
