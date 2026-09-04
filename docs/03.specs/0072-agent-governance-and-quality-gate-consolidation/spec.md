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
templates, and current operations guidance. Closed or archived records are
changed only when they are incorrectly consumed as current authority.

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

Stage 00 gains `registry.json`, an adjacent schema, concrete role documents,
and the shared skill directories formerly stored under `.agents/`. Provider
skill symlinks target Stage 00. Root and provider gateways load the Stage 00
registry and relevant responsibility directly.

`scripts/qa.py` reads `scripts/qa/registry.json`. Profiles are ordered lists of
gate IDs; gates own an argv, timeout, execution environments, and optional
working directory. The runner validates the registry, rejects duplicate gate
execution in one profile, executes without a shell, streams child output, and
returns non-zero on the first blocking failure while still printing a summary.

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

The QA registry is versioned JSON. It contains `schemaVersion`, `profiles`, and
`gates`. No corpus counts, mutable commit SHAs, runtime observations, or copied
policy prose are stored in either registry.

## Interfaces & Data Structures

```text
python3 scripts/qa.py quick
python3 scripts/qa.py full
python3 scripts/qa.py ci
python3 scripts/qa.py --list
```

A gate object has `id`, `argv`, `timeoutSeconds`, and `environments`. A profile
contains an ordered `gates` array. The runner accepts only known profiles and
rejects duplicate IDs, empty argv arrays, non-positive timeouts, unknown gate
references, and a gate not admitted to the selected environment.

## Edge Cases & Error Handling

Paths with spaces remain individual argv elements. Commands are resolved from
the current environment without shell interpolation. Interruptions terminate
the active child and return failure. An unavailable optional external tool is
handled inside its owning pre-commit hook or focused validator; the QA runner
does not convert a required command into a pass.

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
python3 scripts/qa.py ci
pre-commit run --all-files --show-diff-on-failure
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
