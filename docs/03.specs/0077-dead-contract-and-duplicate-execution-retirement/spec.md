---
title: "Dead Contract and Duplicate Execution Retirement Technical Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-09-11"
layer: "specs"
artifact_id: "SPEC-0077"
---

# Dead Contract and Duplicate Execution Retirement Technical Specification (Spec)

## Overview

A repository-wide stocktake of governance, documentation, scripts, tests,
fixtures, gates, QA, CI and skills observed a green baseline with a single
canonical owner for every authority plane, and three defects that a green run
cannot surface: validator and test code that no reachable caller executes,
registered gates re-executed inside the unit-test gate over one snapshot, and
authored procedures that state obligations the corpus never practised.

This Spec owns the retirement of those dead contracts and the removal of that
duplicate execution. It changes no gate meaning, no document route, no profile
and no approval boundary. Its consumers are the validation lane owners, the
test suite, and the skill roster; its verification outcome is an unchanged
`full` gate verdict over a smaller, honest surface.

## Strategic Boundaries & Non-goals

Authorized scope is `scripts/`, `tests/`, `.agents/skills/`,
`.agents/roles/registry.json`, `.agents/governance/document-authoring.md`,
the two provider skill projections, and this package. Deletion of
consumer-zero code, tests and skill packages is authorized, together with the
one skill package this Spec admits.

Explicit non-goals. No validator changes the rule it enforces. No document
route, Stage 99 profile, template, artifact ID or lifecycle edge changes. The
documentation link boundary keeps the behavior `SPEC-0072` criterion
`VAL-AGQ-020` states: a file outside `docs/` reaches the numbered tree only
through the documentation hub, and a stage index is not a second entry point.
This Spec records that rationale and relaxes nothing. No archive payload,
sealed record or issued identifier is edited. No push, PR, merge, branch
cleanup, live cluster, provider runtime or network action is authorized.

`SPEC-0072` remains the owner of its own dated repair; its authorization
excludes file deletion and native projection change, which is why that package
cannot own this work.

## Contracts

A removed symbol has no reachable caller. Reachability is established from the
validator's single diagnostic aggregator and from a repository-wide reference
sweep, not from the absence of failures.

A registered gate executes once per identical input snapshot. A test that
asserts only that a registered validator passes over the repository belongs to
that gate, not to the suite.

A test class that does not subclass the collector's base class is not a test.
A traversal that yields no element is not coverage.

A skill states a procedure its owning role performs. A skill does not restate
governance prose, a Stage 99 path grammar, or a marker the corpus does not use.

## Core Design

Retirement proceeds in dependency order so that each logical unit reverts
alone.

The unreachable cross-document subtree is removed at its dead root, with the
constants it alone consumes and the single test that reaches one of its
private helpers. The rule identifiers it emitted are unreachable, and the only
document naming one is a superseded Architecture Decision Record, so no active
statement becomes false.

Frozen cutover pins are removed with the tests that assert them. Each pin
names a base commit or a path set that no longer exists in the working tree;
the assertions can only be evaluated against history, never against `HEAD`.

Gate re-execution is removed by deleting the pass-through assertions rather
than by weakening the gates. Where a suite needed a real-repository baseline
as setup, the setup is replaced by the synthetic input the surrounding case
already builds.

Duplicate helpers resolve to the existing shared owner. No new abstraction is
introduced; the shared module already exists and is under-adopted.

The skill roster absorbs two packages into their siblings, removes obligations
the corpus never practised, and admits one package for the archive cutover
workflow, which recurs in the corpus and has tooling and Stage 99 profiles but
no owning skill.

## Data Modeling & Storage Strategy

No persistent data shape changes. The role registry gains and loses skill
roster entries only; its schema, permission classes and projection contract
are unchanged. Removed constants held frozen path sets and digests whose
subjects are already absent from the working tree and remain recoverable from
Git history, which is the recovery source this repository designates.

## Interfaces & Data Structures

Validator command-line interfaces, exit codes, diagnostic envelopes and rule
identifier grammar are unchanged. The validation registry keeps its schema and
its profile alias. Removed rule identifiers were never emitted on a reachable
path, so no consumer observes a vocabulary change.

## Edge Cases & Error Handling

Removing a constant that a test imports fails that test at import time rather
than silently; each such pair moves in one logical unit. Removing a pass-through
assertion must not remove the surrounding synthetic coverage; each deletion is
bounded to the named method or class. A skill package removal must update the
role registry and both provider projections atomically, because a dangling
skill reference fails the governance gate.

## Failure Modes & Fallback / Human Escalation

Any logical unit reverts by its own commit. A failing focused check stops that
unit and leaves the rest of the sequence untouched. If a removal turns out to
have a consumer the sweep missed, the gate that consumes it fails closed and
the unit is reverted rather than repaired forward. Unresolved external
authority, hosted results and provider runtime behavior remain operator-owned
and are recorded as DEFER rather than inferred.

## Verification Commands

```bash
python3 -m unittest tests.test_documentation_link_boundary
python3 -B -m unittest tests.test_markdown_render_cache
python3 -B -m unittest tests.test_document_lifecycle_archive_cutover
python3 -B -m unittest tests.test_validation_tooling_ownership
python3 scripts/qa.py quick
python3 scripts/qa.py full
```

`full` owns unit discovery and the pre-commit manual stage; neither is invoked
a second time on unchanged bytes. `ci` is membership-equivalent to `full` and
is not repeated locally. GitHub Actions provides the hosted evidence for the
same profile. No command here proves provider runtime or live cluster behavior.

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-DCR-001 | The unreachable cross-document subtree, its private constants and its single reaching test are absent, and every remaining rule identifier has a reachable emitter | Reference sweep, aggregator read and focused cross-document tests |
| VAL-DCR-002 | Every class the collector treats as a test subclasses its base class, and no traversal in the suite yields an empty sequence where coverage is claimed | Collector-shape assertion and the repaired ledger traversal |
| VAL-DCR-003 | No validator pins a base commit, path set or corpus cardinality whose subject is absent from the working tree | Lifecycle gate read and the paired focused tests |
| VAL-DCR-004 | No registered validator is executed a second time inside the unit-test gate over the same snapshot | Tooling-ownership assertion and the `full` gate result |
| VAL-DCR-005 | Duplicated read, parse and process helpers resolve to the existing shared owner | Focused bounded-input tests and the reference sweep |
| VAL-DCR-006 | Every registered skill has an owning role, states a procedure, and restates no governance prose or Stage 99 path grammar | Governance gate, registry read and skill package review |
| VAL-DCR-007 | The registry routes no absent stage, the evaluation root is inside the document boundary, and no lane, selector or output mode is unreachable | Registry read, contract validator and affected-surface tests |
| VAL-DCR-008 | The documentation link boundary rule owner states why a stage index is not an external entry point, with no change to the diagnostic or its regressions | Rule-owner review and unchanged boundary regressions |

## Traceability

[Implementation Plan](plan.md) owns ordered work and
[retirement Task](tasks/tsk-0001-retire-dead-contracts-and-duplicate-execution.md)
owns execution evidence, approval boundaries and handoff.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DCR-001 | Consumer-zero sweep and cross-document regressions |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DCR-002 | Collector-shape and traversal-coverage checks |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DCR-003 | Absent-subject pin review and paired focused tests |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DCR-004 | Single-execution assertion over one snapshot |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DCR-005 | Shared-owner adoption and bounded-input tests |
| [REQ-0003-FR-0010](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DCR-006 | Registry, projection and skill package validation |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DCR-007 | Routing registry and affected-surface validation |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DCR-008 | Rule-owner review with unchanged boundary evidence |
