---
title: 'Validation Tooling Ownership Technical Specification'
type: sdlc/spec
status: draft
owner: platform
updated: 2026-08-31
artifact_id: "SPEC-0066"
---

# Validation Tooling Ownership Technical Specification (Spec)

## Overview

Spec 0066 is the delegated execution owner for Spec 0054 WP-010 and WP-011.
It does not create a standalone program, replace Spec 0054, or weaken the
parent package's acceptance authority. Spec 0054 owns the integrated governance
outcome; this package owns the bounded validation-tooling transition and its
evidence under proposed [ADR-0031](../../02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md).

The current validators can report green while executable references, routing,
fixtures, and rule ownership remain inconsistent. The main causes are a script
reference check that does not cover every executable shape, broad selection
that makes affected validation effectively global, duplicated runner and hook
paths, production self-tests, and fixtures consumed from production code.
Measured counts are audit evidence only. They are not permanent governance
invariants.

This document is a design checkpoint. The Spec and Plan remain `draft`, and the
Task remains `queued`, until the design is reviewed and the package is
explicitly activated. Its thin README already exists as the lifecycle-free
navigation projection required by accepted ADR-0030; creating that router does
not activate the Spec, Plan, or Task and requires no Stage 98 record.

## Strategic Boundaries & Non-goals

In scope are the tracked validation implementation under `scripts/`, independent
tests and fixtures under `tests/`, validator runners, hooks, CI consumers,
validation documentation, and the existing validation-surface contract.

Before this Spec executes, Spec 0054 owns one atomic activation transaction:
ADR-0031 `proposed → accepted` plus its `supersedes` relation; all five
predecessor `accepted → superseded` transitions and reciprocal
`superseded_by: ADR-0031` relations; ADR-0030's two-clause scoped amendment
Traceability note without changing its accepted status; the Decisions and
Stage 03 READMEs; all current `Proposed ADR-0031` label updates; this package
README's active-execution prose and the Current Spec Index `Draft → Active`
projection; the Spec 0054 delegation Tasks; and verification of the unchanged
Stage 99 Task lifecycle rules. After TSK-0054-0010 becomes the sole active
parent Task, that Task owns the exact activation index and evidence. The
transaction establishes the
reviewed authority and legal transfer, adds a narrow package-local delegated
ownership rule with focused positive and negative tests, activates this Spec,
Plan, and Task, moves the existing Spec 0054 compatibility pointer from
TSK-0054-0010 to TSK-0054-0011, completes TSK-0054-0010, and activates
TSK-0054-0011 as the sole parent acceptance Task. It creates no Spec 0066
standalone row.
It is an external precondition, not work executed by the queued
TSK-0066-0001. No lifecycle-domain, schema, or code-projection edit is part of
that activation.

The contract currently located at
`docs/00.agent-governance/contracts/validation-surfaces.json` and its schema are
reused by moving them atomically to `scripts/validation/registry.json` and
`scripts/validation/registry.schema.json`. The move does not create a second
registry. The target registry owns only the routing graph: validation surfaces,
lanes, executable arguments, CI routing, and their consumers. Rule semantics
remain in validator modules, and point-in-time disposition evidence remains in
the active Task and Git diff.

Out of scope are live cluster changes, provider-runtime claims, hosted-CI
claims, branch protection mutation, push, merge, and deployment. This design
does not require a fixed validator count, a fixed entrypoint count, a line-count
ceiling, or a permanent inventory ledger.

Existing required CI check names are retained until the remote protection rules
are verified through an authorized remote operation. Internal jobs, commands,
and routing may be simplified without renaming those external checks.

### Authority and Ownership

| Concern | Single owner |
| --- | --- |
| Integrated SDLC acceptance for WP-010 and WP-011 | Spec 0054 through TSK-0054-0011 |
| Validation-tooling transition and execution evidence | Spec 0066 |
| Surface, lane, executable, and CI routing graph | `scripts/validation/registry.json` |
| Rule semantics and diagnostics | The responsible validator module |
| Independent behavior verification | Tests under `tests/` |
| Current execution history and rollback | Git and the active Task |
| Historical path recovery | Reachable Git history by default; a sealed Stage 98 Migration only for a required immutable lookup Git alone cannot resolve |

One permanent rule has one semantic owner. Aggregates and runners dispatch to
that owner; they do not reimplement the rule. The registry declares routing but
does not become an executable rule engine.

## Contracts

1. Spec 0066 executes only the delegated Spec 0054 WP-010/WP-011 scope and
   reports acceptance evidence back to Spec 0054. The thin package README is a
   lifecycle-free navigation projection and exists before activation. Its Plan
   and Task form one closed package-local execution component with their own
   Spec; they do not render links to a parent Plan or Task. Parent/delegate
   ownership is instead proved by reciprocal Spec links, accepted ADR-0031,
   one unambiguous registry-owned parent during transition, lifecycle parity,
   and absence of a child standalone row.
2. The existing validation-surface JSON and schema move to the scripts-owned
   location in one logical change. Source and target may not coexist as current
   authorities.
3. During that atomic move, the selected validators and unmatched-path result
   are equivalent before and after. Later routing changes may intentionally
   alter selection when their reason and focused evidence are recorded.
4. A current reference to an executable resolves to an executable in the
   current tree. Reachable Git history is the default historical recovery
   owner. An explicit sealed Migration is added only for a required immutable
   lookup that Git alone cannot resolve, and a minimal Tombstone only when both
   are insufficient. An active Spec that merely proposes a future path does
   not make a missing current executable valid.
5. A rule has one semantic owner and one diagnostic contract. A thin aggregate,
   dispatcher, or compatibility runner contains no duplicate rule meaning.
6. Production validators do not embed `--self-test`. Independent tests exercise
   their importable contracts.
7. Validator tests and fixtures remain under top-level `tests/` and
   `tests/fixtures/`. Production code does not import from or read those paths.
8. A wrapper is removed only after all current consumers are absent and it has
   no unique diagnostic or recovery behavior. Otherwise it remains explicit.
9. Repository reads and subprocesses are bounded, text decoding is explicit
   UTF-8, and subprocesses have timeouts with actionable diagnostics.
10. Staged validation uses the Git index as its subject and fails closed when
    index/worktree ambiguity would make the result unreliable.
11. Branch-tip SHAs and generated digests do not track current repository
    state. Full SHAs are limited to immutable external dependencies and sealed
    recovery coordinates with an owner and update or recovery path.
12. Each package has at most one `in-progress` Task. This package has none while
    its only Task is `queued`.

## Core Design

The target separates declaration, semantics, dispatch, and verification:

```text
scripts/
├── validation/
│   ├── registry.json
│   ├── registry.schema.json
│   └── <responsibility-owned validator modules>
├── qa/
│   └── <thin aggregate and operational runners>
└── lib/
    └── <shared bounded Git, path, UTF-8, and subprocess primitives>
tests/
├── <independent validator tests>
└── fixtures/
    └── <test-only case data>
```

Responsibility boundaries, not an exact file count, determine whether a
validator is split or combined. Dead code is removed before decomposition.
Large modules are split when they combine independent rule ownership, duplicate
logic, or materially increase review and failure risk; size alone is supporting
evidence, not a gate.

The aggregate selects and invokes responsible validators from the registry. It
may normalize results and exit status, but it cannot contain rule predicates or
authoritative diagnostic text. Domain runners follow the same rule.

## Data Modeling & Storage Strategy

The registry cutover is one reviewable logical change:

1. Move the existing JSON and schema without forking their authority.
2. Update every current consumer to the target paths in the same change.
3. Verify schema validity and routing-selection equivalence across the move.
4. Remove the source paths before the change is considered complete.

After cutover, the registry may be simplified intentionally. Such a change
records the affected paths, the old and new selected lanes, the reason for the
change, and focused verification. Permanent rows for every script, fixture,
hook, pin, and audit decision are prohibited; those facts belong to code,
tests, current consumers, or Task evidence.

## Interfaces & Data Structures

Independent tests cover the behaviors that previously depended on embedded
`--self-test` branches. Behavior cases include missing executable references,
duplicate rule owners, aggregate rule reimplementation, orphan fixtures,
unbounded I/O, subprocesses without timeouts, unexplained pins, and staged
index/worktree ambiguity. The list may evolve with the implementation; its
cardinality is not a contract.

Fixtures remain test-only. If production needs the same data, the data is moved
to a production-owned authority under `scripts/` and tests consume that owner or
maintain clearly scoped test input. Tests do not become a runtime dependency.

## Edge Cases & Error Handling

Before removing a compatibility wrapper, the Task records a current-consumer
sweep covering scripts, tests, hooks, workflows, pre-commit, and current docs.
It also compares diagnostic and recovery behavior. A wrapper with either a
consumer or unique behavior stays until a later cutover proves both conditions
false.

Historical references inside sealed Stage 98 records remain historical. They
do not require the old executable to exist in the current tree, and they do not
justify a current redirect copy. A new Migration is created only when an
immutable historical link needs an explicit recovery mapping that reachable
Git history alone cannot provide.

Spec 0065 retired `route_state`. No command, schema, test, or compatibility path
in this work may reintroduce that option.

## Failure Modes & Fallback / Human Escalation

- If the reference validator cannot distinguish current references from sealed
  historical references, restructuring stops until that distinction is tested.
- If the registry move changes selection, the atomic move stops. Intentional
  selection changes occur only after the move as separately evidenced work.
- If remote branch-protection state cannot be verified, required CI check names
  remain unchanged and the limitation is recorded.
- If a wrapper's current consumers or unique diagnostics are uncertain, the
  wrapper remains.
- If staged validation cannot bind to the index deterministically, it fails
  closed rather than silently falling back to worktree state.

Rollback is per logical commit. No rollback edits a sealed Stage 98 record or
restores a body-copy redirect.

## Verification Commands

Each logical change runs focused independent tests plus these currently
resolvable control-plane checks:

```bash
python3 -B scripts/validate-document-contract-registry.py --mode strict
python3 -B scripts/validate-markdown-profiles.py --root . --mode strict
python3 -B scripts/validate-links-and-owners.py --root . --mode strict
python3 -B scripts/validate-document-lifecycle.py --root . --mode staged
python3 -B scripts/validate-affected-surfaces.py --root .
git diff --check
git diff --cached --check
```

The active Task records additional focused commands only after their executable
paths exist. The registry move updates those commands atomically and compares
routing selection before and after using the same path cases; a planned path is
never treated as an executable command merely because this Spec names it.

All evidence is repository-static. It does not prove native agent discovery,
hook delivery, authenticated provider runtime, hosted CI, or live cluster
readiness.

## Success Criteria & Verification Plan

| ID | Criterion |
| --- | --- |
| VAL-VTO-001 | Spec 0066 remains a delegated execution package for Spec 0054 WP-010/WP-011, with no standalone or replacement authority; its lifecycle-free thin router exists before activation; its Plan/Task component remains package-local; and the TSK-0054-0010-owned activation establishes reciprocal Spec/accepted-ADR ownership, focused fail-closed tests, legal state transfer, and the parent-only compatibility-pointer rotation without a child roster row |
| VAL-VTO-002 | The existing validation-surface JSON and schema are moved atomically to `scripts/validation/registry.*`, every consumer is updated, and no second current registry remains |
| VAL-VTO-003 | Selection is equivalent across the registry move; later intentional routing changes carry an explicit before/after explanation and focused evidence |
| VAL-VTO-004 | Every current executable reference resolves to a current executable; historical recovery uses reachable Git by default and adds sealed Stage 98 evidence only for a required immutable lookup Git alone cannot resolve |
| VAL-VTO-005 | Each permanent rule has one semantic owner, and aggregates, dispatchers, runners, and compatibility paths contain no duplicate rule meaning |
| VAL-VTO-006 | Production `--self-test` branches are removed only after independent top-level tests cover their behavior; production code has no dependency on `tests/` or `tests/fixtures/` |
| VAL-VTO-007 | Each removed wrapper has recorded consumer-zero and unique-diagnostic-zero evidence; retained wrappers name their current consumer or unique behavior |
| VAL-VTO-008 | Validation I/O is bounded and UTF-8 explicit, subprocesses time out, and staged validation fails closed on unreliable index/worktree state |
| VAL-VTO-009 | Current-state branch SHAs and generated digests are absent; retained SHAs are limited to owned external immutable dependencies or sealed recovery coordinates |
| VAL-VTO-010 | Existing required CI check names remain stable until authorized remote branch-protection verification permits a separate rename decision |
| VAL-VTO-011 | Focused tests, affected and staged gates, diff checks, and the integrated Spec 0054 acceptance lane pass at completion |

## Traceability

Spec 0054 remains the upstream acceptance authority. Proposed ADR-0031 defines
the current-corpus and validation-routing ownership used here; ADR-0022's
standalone execution model is not an authority for this delegated package and
is intended to be superseded only when ADR-0031 is accepted.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — Spec 0054 integrated acceptance | VAL-VTO-001 | ADR/README reciprocity, package-local delegation, and lifecycle traceability |
| N/A — delegated Spec 0054 WP-010 | VAL-VTO-002 | Atomic registry cutover and consumer sweep |
| N/A — delegated Spec 0054 WP-011 | VAL-VTO-003 | Routing before/after evidence |
| N/A — delegated Spec 0054 WP-010 | VAL-VTO-004 | Current-reference and Git-first bounded-recovery cases |
| N/A — delegated Spec 0054 WP-011 | VAL-VTO-005 | Rule-owner and thin-runner audit |
| N/A — delegated Spec 0054 WP-010 | VAL-VTO-006 | Independent test and production fixture-dependency audit |
| N/A — delegated Spec 0054 WP-011 | VAL-VTO-007 | Wrapper consumer and diagnostic evidence |
| N/A — delegated Spec 0054 WP-010 | VAL-VTO-008 | Bounded-I/O, timeout, and staged-index cases |
| N/A — delegated Spec 0054 WP-010 | VAL-VTO-009 | Pin owner and recovery classification |
| N/A — delegated Spec 0054 WP-011 | VAL-VTO-010 | Required CI check-name compatibility evidence |
| N/A — Spec 0054 integrated acceptance | VAL-VTO-011 | Focused suites, staged gates, diff checks, and parent acceptance evidence |

### Related Documents

- [Proposed ADR-0031 — current corpus retention and validation ownership](../../02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md)
- [ADR-0030 — authority-first SDLC and agent governance convergence](../../02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md)
- [Spec 0054](../0054-sdlc-document-and-agent-governance-consolidation/spec.md)
- [Plan 0066](plan.md)
- [TSK-0066-0001](tasks/tsk-0001-vto-000.md)
