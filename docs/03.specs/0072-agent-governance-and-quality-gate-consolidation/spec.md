---
title: "Agent Governance and Quality Gate Consolidation Technical Specification"
version: "2.2.0"
type: "sdlc/spec"
status: "active"
owner: "platform"
updated: "2026-09-09"
layer: "specs"
artifact_id: "SPEC-0072"
---

# Agent Governance and Quality Gate Consolidation Technical Specification (Spec)

## Overview

Common authority and the QA migration are complete. This specification now
owns the approved 2026-09-08 correction of gate coverage, formatter behavior,
commit validation, redundant execution and current guidance, plus the approved
2026-09-09 local repair of evaluation-input containment, QA snapshot integrity,
document identity, live-script temporary files and current ownership prose. The accepted
[ADR-0036](../../02.architecture/decisions/0036-common-knowledge-and-prompt-surfaces.md)
succeeds ADR-0034/0035 for current authority. SPEC-0074 owns provider write-guard
behavior and SPEC-0075 owns knowledge/prompt adoption; neither replaces this QA
follow-up. The [original Task](tasks/tsk-0001-consolidate-governance-and-quality-gates.md)
preserves completed migration and native follow-up evidence. The
[repair Task](tasks/tsk-0002-repair-governance-and-validation-contracts.md)
owns the new local implementation and its evidence without reopening that stream.

## Strategic Boundaries & Non-goals

Authorized scope includes `.github/`, `.agents/`, `.claude/`,
`.codex/`, root gateways, current SDLC owners, QA scripts, tests, fixtures,
templates, and current operations guidance. Historical and in-progress records are reviewed for conflicting current
authority. Preserve historical facts and valid archive isolation; replace or
retire obsolete instructions with their consumers and recovery evidence.

No live infrastructure, provider, credential, release, deployment, or Argo CD
reconciliation operation is authorized. Historical evidence is not rewritten
to simulate a timeless repository state.

The 2026-09-09 repair is local-only and authorizes only the current owners,
implementations, focused tests and synthetic fixtures named below. It authorizes
no file deletion, new document registry/profile/gate, native projection change,
private configuration read, network action, push, PR, merge or branch/worktree
cleanup. Task-owned temporary cleanup is authorized and required. The
existing `WORK-009` native follow-up remains separate and deferred to the
operator; this repair cannot satisfy it.

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
- **C-AGQ-009 — contained evaluation inputs.** Evaluation registry, case,
  response and citation reads accept only contained bounded regular files decoded as strict
  UTF-8. Rejections identify a safe path and reason without payload content.
- **C-AGQ-010 — exact snapshot and review subjects.** A gate that promises an
  unchanged snapshot compares both working-tree bytes and the pre-gate index.
  Change review accepts staged-only and unstaged differences, rejects an empty
  or untracked-only subject, and states which diff forms were reviewed.
- **C-AGQ-011 — path-bound document identity.** Every registered numbered
  authored family binds its artifact ID to the path-derived family and number.
  Current IDs are unique even for partial selected inputs; retired IDs cannot be
  reused unless existing base, sealed-migration or tombstone provenance proves
  the same document lineage.
- **C-AGQ-012 — private live-script temporaries.** Each live verification run
  creates a private per-run temporary directory and removes it on every exit
  while preserving the command status and existing diagnostic meaning.
- **C-AGQ-013 — source-owned current guidance.** Evaluation, formatting, Git and
  PR prose points to its executable or configuration owner and does not copy
  mutable inventories. A dated ADR clarification preserves historical meaning.

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

### Approved governance and validation contract repairs

- `scripts/run-agent-evaluations.py` reuses
  `scripts/validation/repository/bounded_io.py` for case, response and citation
  inputs and applies the same boundary to the agent registry input. Exactly one
  tracked authority-negative case and synthetic response
  demonstrate the fail-closed criterion; test module entry guards remain at EOF.
- `scripts/qa.py` snapshots the index as content before running a gate, so a
  modify-and-stage child cannot pass `require_unchanged_snapshot`. The
  `change-review` prompt and `scripts/prompt-input.py` distinguish staged,
  unstaged, empty and untracked-only inputs. Deleted-path routing fixtures remain.
- Existing Markdown-profile, lifecycle and Archive implementations enforce
  numbered path-to-ID binding, current uniqueness and retired-number provenance.
  They keep existing conforming current IDs, template placeholders, tombstone
  payloads and frozen bytes unchanged. Stage, package and Task numbers remain
  distinct; cross-document references use the parent artifact plus an existing
  local ID without renumbering.
- `infrastructure/tests/verify-gitops.sh`,
  `infrastructure/tests/verify-external-services.sh` and
  `infrastructure/tests/verify-ingress-tls.sh` replace predictable shared `/tmp`
  files with private per-run storage and a trap. Stubbed tests exercise status,
  diagnostics and cleanup without invoking live commands or adding retention.
- `.agents/README.md` routes evaluation assets to `evals/`, execution to the
  script runner and role truth to the registry. ADR-0036 receives only a dated
  ownership clarification. Formatting prose and comments describe editor,
  hook, Git and pinned defaults without behavior changes. The PR template calls
  its entries review categories and points commit syntax to `.cz.toml`; the
  quality assertion checks that pointer instead of copying the 13 types.

## Data Modeling & Storage Strategy

The common role registry keeps stable role IDs, permission classes, supported
providers, capability references, skill references, handoffs, and provider
projection paths. Paths are repository-relative POSIX strings. Provider model
and tool metadata stay in native projection files because they are provider
configuration, not shared policy.

The existing validation registry remains versioned JSON. QA profile records
contain ordered gate IDs only. They never duplicate command arguments,
timeouts, mutable commit SHAs, runtime observations or copied policy prose.

Artifact identity is derived from the selected profile and numbered path, then
compared across the current governed corpus. A selected-path run still loads the
existing current identity base needed to detect collisions. Historical identity
comes only from the existing lifecycle base and sealed migration/tombstone
provenance; no ledger, README, registry or Spec tree is added. Recorded
same-document lineage may retain its identity.

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
An unchanged-snapshot gate also compares the post-gate index with the pre-gate
index content. Prompt assembly treats staged and unstaged diffs as reviewable
subjects and status-only untracked paths as insufficient input.

## Edge Cases & Error Handling

Paths with spaces remain individual argv elements. Commands use validated absolute executable paths and the selected Python
interpreter without shell interpolation or unfiltered environment inheritance. Interruptions terminate
the active child and return failure. A missing required tool or module fails closed. SKIP is reserved for an
inapplicable or explicitly optional check; missing authorization/environment
for required external evidence is DEFER and cannot satisfy overall completion.

A provider projection may remain tracked when the provider supports that native
format, but its common responsibility and skill meaning must resolve to `.agents/`. Historical source paths are retained as evidence
only; they never provide an executable fallback to the removed owner.

Escaping, symlinked, oversized, non-regular or non-UTF-8 evaluation inputs fail
with stable payload-free diagnostics. A duplicated current artifact ID, a valid
but wrong family/number ID, or retired-number reuse without accepted provenance
fails even for partial selected inputs. Same-lineage recovery is accepted only
through existing provenance owners. Live-script cleanup runs after success,
command failure and signal-driven exit and returns the original status.

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
python3 -B -m unittest tests.test_agent_evaluations tests.test_prompt_input
python3 -B -m unittest tests.test_document_artifact_identity
python3 -B -m unittest tests.test_infrastructure_tempfiles
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
| VAL-AGQ-015 | Evaluation registry, case, response and citation inputs are contained, bounded regular strict-UTF-8 files with payload-free diagnostics | Focused path, symlink, size and one tracked authority-negative evaluation case |
| VAL-AGQ-016 | Snapshot mutation through modify-and-stage fails, and review input semantics distinguish staged, unstaged, empty and untracked-only states | QA snapshot regression and prompt-input contract tests |
| VAL-AGQ-017 | Every registered numbered authored family has path-bound unique current identity and retired IDs require existing provenance, including partial selected inputs | Ten-family wrong-valid-ID probes, duplicate/partial-input tests and Archive lineage regressions |
| VAL-AGQ-018 | The three live verification scripts use private per-run temporary storage, preserve exit status and diagnostics, and always clean up | Stubbed no-live-command script tests |
| VAL-AGQ-019 | Current evaluation, formatting, Git and PR guidance points to canonical owners without copied mutable inventories or changed native/tool behavior | Focused governance prose and repository-quality assertions |

## Traceability

[Implementation Plan](plan.md) owns ordered work and
[original Task evidence](tasks/tsk-0001-consolidate-governance-and-quality-gates.md)
owns the completed migration and unresolved native follow-up. The
[repair Task](tasks/tsk-0002-repair-governance-and-validation-contracts.md) owns
`WORK-010` onward and the local repair evidence.

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
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGQ-015 | Bounded-input negative tests and tracked authority-negative evaluation |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGQ-016 | Exact-index snapshot and prompt-input state tests |
| [REQ-0003-FR-0023](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGQ-017 | Path/identity, partial-selection and retained-provenance tests |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGQ-018 | Stubbed private-temporary cleanup and exit-status tests |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGQ-019 | Canonical-owner prose and repository-quality tests |
