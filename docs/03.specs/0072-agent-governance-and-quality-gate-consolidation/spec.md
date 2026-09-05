---
title: "Agent Governance and Quality Gate Consolidation Technical Specification"
version: "1.0.0"
type: "sdlc/spec"
status: "active"
owner: "platform"
updated: "2026-09-04"
layer: "specs"
artifact_id: "SPEC-0072"
---

# Agent Governance and Quality Gate Consolidation Technical Specification (Spec)

## Overview

This specification implements ADR-0034. It consolidates shared agent assets in
Stage 00, removes `.agents/`, retires duplicate and stale agent validation
surfaces, and makes one QA command the executable contract for local and GitHub
Actions environments.

## Strategic Boundaries & Non-goals

Authorized scope includes `.github/`, `docs/00.agent-governance/`, `.claude/`,
`.codex/`, root gateways, current SDLC owners, QA scripts, tests, fixtures,
templates, and current operations guidance. Historical and in-progress records are reviewed for conflicting current
authority. Preserve historical facts and valid archive isolation; replace or
retire obsolete instructions with their consumers and recovery evidence.

No live infrastructure, provider, credential, release, deployment, or Argo CD
reconciliation operation is authorized. Historical evidence is not rewritten
to simulate a timeless repository state.

## Contracts

- **C-AGQ-001 — one governance root.** Shared policy, provider definitions,
  roles, skills, permissions, handoffs, and projection paths are owned below
  `docs/00.agent-governance/`; `.agents/` does not exist.
- **C-AGQ-002 — thin provider adapters.** `.claude/` and `.codex/` contain only
  native configuration and projections and link to Stage 00 for shared meaning.
- **C-AGQ-003 — one QA entrypoint.** `python3 scripts/qa.py <profile>` is the
  supported local and hosted orchestration interface. A gate is current only
  when declared in the QA registry and reachable from a supported profile.
- **C-AGQ-004 — no duplicate execution.** One CI run invokes each blocking gate
  at most once. Unit discovery is not repeated by an aggregate and a workflow
  job.
- **C-AGQ-005 — bounded fixtures.** Test fixtures stay under `tests/fixtures/`,
  are read only by tests, and represent one failure boundary each. Stale
  provider-runtime, checkpoint, and self-only gate fixtures are removed.
- **C-AGQ-006 — explicit evidence classes.** Repository-static QA, hosted CI,
  provider runtime, and live infrastructure evidence are not interchangeable.
- **C-AGQ-007 — GitOps CD boundary.** GitHub Actions validates repository state;
  Argo CD performs operator-controlled reconciliation from merged desired state.
- **C-AGQ-008 — fail-closed summary.** Missing commands, timeouts, invalid gate
  definitions, and non-zero child results fail the selected profile and the
  required `ci-summary` check.

## Core Design

Stage 00 roles owns the shared `roles/registry.json`, its schema and concrete
role bodies. Stage 00 skills owns shared native skill packages with `SKILL.md`
metadata and assets. Claude may expose these through its supported skill
adapter. Codex uses explicit reads from root AGENTS and role instructions;
this is not automatic native skill registration. Native role bodies reference
canonical responsibilities directly, so no projection framework is introduced.

`scripts/qa.py` selects gate IDs from the existing validation registry. The
existing registry remains the sole argv and execution-configuration owner;
profiles introduce no second gate definitions. The bounded runner retains its
time, stdout/stderr and descendant/pipe cleanup guarantees. QA validates
selection before running children, rejects duplicate IDs and nested aggregate
recursion, and emits bounded redacted error summaries plus non-zero status.
The invoking Python environment is preserved without inheriting arbitrary
startup variables or caller-controlled search paths.

The supported profiles are:

| Profile | Purpose |
| --- | --- |
| `quick` | Fast governance, document, workflow, and focused QA tests during implementation |
| `full` | Complete local repository-static evidence before handoff |
| `ci` | The same blocking set as `full`, executed by GitHub Actions |

GitHub Actions uses one setup and one `qa` job. The job installs the hashed
Python requirements, installs Gitleaks with the existing checksum, and invokes
`python3 scripts/qa.py ci`. `ci-summary` remains the protected check and fails
unless branch policy and QA have valid results.

## Data Modeling & Storage Strategy

The Stage 00 registry keeps stable role IDs, permission classes, supported
providers, capability references, skill references, handoffs, and provider
projection paths. Paths are repository-relative POSIX strings. Provider model
and tool metadata stay in native projection files because they are provider
configuration, not shared policy.

The existing validation registry remains versioned JSON. QA profile records
contain ordered gate IDs only. They never duplicate command arguments,
timeouts, mutable commit SHAs, runtime observations or copied policy prose.

## Interfaces & Data Structures

```text
python3 scripts/qa.py quick
python3 scripts/qa.py full
python3 scripts/qa.py ci
python3 scripts/qa.py --list
```

Gate definitions retain the existing validation schema and one owner for
commands and execution limits. QA rejects unknown profiles/gates, duplicate
IDs, empty command arrays, invalid limits and inadmissible evidence lanes.
`quick` selects changed working-tree paths; staged validation reads the actual
index in a separate snapshot without hiding staged errors behind unstaged
repairs. NUL-delimited paths preserve deletions, renames and whitespace.

## Edge Cases & Error Handling

Paths with spaces remain individual argv elements. Commands use validated absolute executable paths and the selected Python
interpreter without shell interpolation or unfiltered environment inheritance. Interruptions terminate
the active child and return failure. A missing required tool or module fails closed. SKIP is reserved for an
inapplicable or explicitly optional check; missing authorization/environment
for required external evidence is DEFER and cannot satisfy overall completion.

A provider projection may remain tracked when the provider supports that native
format, but its common responsibility and skill meaning must resolve to Stage
00. A historical `.agents/` mention is allowed only outside current executable
or active guidance surfaces.

## Failure Modes & Fallback / Human Escalation

Invalid registries and missing commands fail before implementation or merge.
A failing gate is fixed at its smallest current owner; it is not bypassed by
running a narrower profile. Rollback is a Git revert of the logical commit that
owns the failed migration or orchestration change.

Provider-runtime and live-environment checks may be recorded as `DEFER` only in
the owning Task with a reason and next owner. They never satisfy repository
static acceptance.

## Verification Commands

```bash
python3 -m unittest tests.test_qa_runner tests.test_agent_governance
python3 scripts/qa.py --list
python3 scripts/qa.py quick
python3 scripts/qa.py full
# ci is membership-equivalent to full; do not repeat the same suite locally.
# pre-commit is owned by full and is not invoked a second time on unchanged bytes.
```

GitHub Actions provides hosted evidence for the same `ci` profile. No command in
this section proves provider runtime or live cluster behavior.

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-AGQ-001 | `.agents/` is absent and no current gateway, provider adapter, policy, role, skill, QA registry, workflow, or active guidance depends on it | Governance validator and current-reference sweep |
| VAL-AGQ-002 | Every registered role, skill, handoff, permission class, and provider projection resolves from Stage 00 | Focused governance tests and validator |
| VAL-AGQ-003 | `quick`, `full`, and `ci` are valid profiles with no duplicate gate execution | QA runner unit tests and `--list` output |
| VAL-AGQ-004 | Local `full` and hosted `ci` execute the same blocking gate IDs | Registry assertion and workflow contract test |
| VAL-AGQ-005 | Obsolete agent contracts, validators, hooks, tests, and fixtures have no current consumers | Current executable-reference check and reviewed deletion set |
| VAL-AGQ-006 | GitHub Actions has one QA execution path and a fail-closed `ci-summary` | actionlint, zizmor, workflow contract test, hosted run |
| VAL-AGQ-007 | QA and CI/CD guidance distinguishes GitHub validation from Argo CD reconciliation | Current governance and operations guide review |
| VAL-AGQ-008 | Remaining fixtures are test-only and production scripts do not import `tests` | Fixture-boundary test |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGQ-001 | Governance path and current-reference validation |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGQ-002 | Registry and projection validation |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGQ-003 | QA registry tests |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGQ-004 | Local/CI profile parity test |
| [REQ-0003-IF-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGQ-005 | Consumer-zero and deletion review |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGQ-006 | Workflow static and hosted validation |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGQ-007 | Governance and operations review |
| [REQ-0003-IF-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGQ-008 | Fixture ownership test |
