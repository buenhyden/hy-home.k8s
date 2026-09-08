---
title: "Agent Governance and Quality Gate Consolidation Technical Specification"
version: "2.1.0"
type: "sdlc/spec"
status: "active"
owner: "platform"
updated: "2026-09-08"
layer: "specs"
artifact_id: "SPEC-0072"
---

# Agent Governance and Quality Gate Consolidation Technical Specification (Spec)

## Overview

Common authority and the QA migration are complete. This specification now
owns the approved 2026-09-08 correction of gate coverage, formatter behavior,
commit validation, redundant execution and current guidance. The accepted
[ADR-0036](../../02.architecture/decisions/0036-common-knowledge-and-prompt-surfaces.md)
succeeds ADR-0034/0035 for current authority. SPEC-0074 owns provider write-guard
behavior and SPEC-0075 owns knowledge/prompt adoption; neither replaces this QA
follow-up. The [Task](tasks/tsk-0001-consolidate-governance-and-quality-gates.md)
preserves completed migration evidence and the current approval boundary.

## Strategic Boundaries & Non-goals

Authorized scope includes `.github/`, `.agents/`, `.claude/`,
`.codex/`, root gateways, current SDLC owners, QA scripts, tests, fixtures,
templates, and current operations guidance. Historical and in-progress records are reviewed for conflicting current
authority. Preserve historical facts and valid archive isolation; replace or
retire obsolete instructions with their consumers and recovery evidence.

No live infrastructure, provider, credential, release, deployment, or Argo CD
reconciliation operation is authorized. Historical evidence is not rewritten
to simulate a timeless repository state.

## Contracts

- **C-AGQ-001 — one governance root.** Shared policy,
  roles, skills, permissions, handoffs, and projection references are owned below
  `.agents/`; the former documentation governance root must not exist.
- **C-AGQ-002 — thin provider adapters.** `.claude/` and `.codex/` contain only
  native configuration and projections and link to `.agents/` for shared meaning.
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

The common registry/schema and neutral role bodies live in `.agents/roles/`.
Normative policy and SDLC live in `.agents/governance/`. Registered
callable packages live at `.agents/skills/<id>/SKILL.md`; the registry, not a
fixed count, determines the required set. Plain lifecycle and delegation
procedures live in `.agents/workflows/`. Provider-only support notes live at
`.claude/provider.md` and `.codex/provider.md`.

Codex discovers repository skills at `.agents/skills/`; Claude exposes one
relative link per skill below `.claude/skills/`. Set explicit-only invocation
metadata for these packages and retain role/user approval preconditions. No
skill grants tools or credentials. Root AGENTS uses explicit read instructions;
Claude imports only common and Claude instructions. Native role bodies remain
thin references with unchanged model, tools and responsibility metadata.
The whole `.agents/` directory is not an automatic instruction loader.

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
| `quick` | Affected working-tree gates during implementation; focused tests run separately |
| `staged` | Changed-path validation of the exact Git index before a local commit |
| `full` | Complete local repository-static evidence before handoff |
| `ci` | The same blocking set as `full`, executed by GitHub Actions |

GitHub Actions uses one setup and one `qa` job. The job installs the hashed
Python requirements, installs Gitleaks with the existing checksum, and invokes
`python3 scripts/qa.py ci`. `ci-summary` remains the protected check and fails
unless branch policy and QA have valid results.

### Approved gate corrections

- Keep the existing registry and pre-commit gate. Full/ci invoke pre-commit's
  explicit manual stage once. Pinned Gitleaks scans the isolated snapshot tree;
  its native pre-commit stage scans the index. Exclude Git metadata before
  directory traversal and retain separate historical and domain secret checks.
- Commitizen in `.cz.toml` owns new-message syntax. Commit-msg validation uses
  the actual UTF-8 candidate message and is independent of file QA. Preserve
  active hooks and separate manual validation from observed native execution.
  Keep optional scope, supported types and BREAKING CHANGE footer; `!` remains
  unsupported. Subject length and capitalization guidance are recommendations.
- ShellCheck/shfmt select both providers' shell adapters. Shfmt explicitly
  writes formatted bytes; QA rejects snapshot changes without changing the
  source tree/index. Explicit fixes use existing hooks on selected files.
  Frozen bodies remain outside mutating hooks under the lifecycle contract.
- Remove redundant harness calls and move embedded synthetic probes into
  independent tests while retaining every unique production rule. Remove
  unused Docker lint configuration only after confirming no Dockerfile target.
- Preserve trusted tool resolution, closed environment, bounds and cleanup.
  Escaped-process diagnostics use process name/state, never command arguments.
  Tool/cache identities and platform limits belong to measured Task evidence.

## Data Modeling & Storage Strategy

The common role registry keeps stable role IDs, permission classes, supported
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
python3 scripts/qa.py staged
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
format, but its common responsibility and skill meaning must resolve to `.agents/`. Historical source paths are retained as evidence
only; they never provide an executable fallback to the removed owner.

## Failure Modes & Fallback / Human Escalation

Invalid registries and missing commands fail before implementation or merge.
A failing gate is fixed at its smallest current owner; it is not bypassed by
running a narrower profile. Rollback reverses only the reviewed migration as a
new change after checking for later user edits and dependent commits against
the recorded baseline; no blanket restore or history rewrite is authorized.

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
| VAL-AGQ-001 | The old governance root is absent and every source has a disposition; current consumers resolve solely to `.agents/` or native provider owners | Governance validator and current-reference sweep |
| VAL-AGQ-002 | Every registered role, skill, handoff, permission class, and provider projection resolves from `.agents/` without expanded permissions | Focused governance tests and validator |
| VAL-AGQ-003 | `quick`, `full`, and `ci` are valid profiles with no duplicate gate execution | QA runner unit tests and `--list` output |
| VAL-AGQ-004 | Local `full` and hosted `ci` execute the same blocking gate IDs | Registry assertion and workflow contract test |
| VAL-AGQ-005 | Obsolete agent contracts, validators, hooks, tests, and fixtures have no current consumers | Current executable-reference check and reviewed deletion set |
| VAL-AGQ-006 | GitHub Actions has one QA execution path and a fail-closed `ci-summary` | actionlint, zizmor, workflow contract test, hosted run |
| VAL-AGQ-007 | QA and CI/CD guidance distinguishes GitHub validation from Argo CD reconciliation | Current governance and operations guide review |
| VAL-AGQ-008 | Remaining fixtures are test-only and production scripts do not import `tests` | Fixture-boundary test |
| VAL-AGQ-009 | Commit-msg validation is separate from file QA and commit/changelog guidance matches supported syntax | Pinned valid/invalid messages and stage-selection tests |
| VAL-AGQ-010 | Both provider shell adapters receive the same common shell checks | Actual-path selectors and malformed shell regression |
| VAL-AGQ-011 | Formatter mismatches fail without source/index mutation or frozen-body edits | Snapshot isolation and lifecycle-aware selector tests |
| VAL-AGQ-012 | Full/ci secret scanning covers unchanged eligible snapshot files | Clean-tree canary, hidden file and stage-mode checks |
| VAL-AGQ-013 | Environment identity and process diagnostics preserve the security boundary | Trusted resolver, bounded process state and no-cmdline tests |
| VAL-AGQ-014 | Removed duplication preserves unique rules, failure meanings and base inputs | Independent probe tests and consumer-zero review |

## Traceability

[Implementation Plan](plan.md) owns ordered work and
[Task evidence](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) owns
execution outcomes and remaining verification limits.

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
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGQ-009 | Pinned valid/invalid messages and stage-selection tests |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGQ-010 | Actual-path selectors and malformed shell regression |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGQ-011 | Snapshot isolation and lifecycle-aware selector tests |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGQ-012 | Clean-tree canary, hidden file and stage-mode checks |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGQ-013 | Trusted resolver, bounded process state and no-cmdline tests |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGQ-014 | Independent probe tests and consumer-zero review |
