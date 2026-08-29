---
title: 'Quality and Evidence Policy'
type: governance/reference
status: active
owner: platform
updated: 2026-08-28
---

# Quality and Evidence Policy

## Overview

Report exactly what was checked, over which bytes and scope, and with which
limitations. Passing a local command is not proof of provider or live behavior.

## Authority Boundary

This policy owns lane, result, completion-order, and handoff meanings.
The validation-surface contract selects executable checks; validators own
their rules and bounded execution limits. Aggregates compose those checks.
Do not duplicate limit constants, fixture matrices, mutable digests, or corpus
counts in prose.

## Governance Context

Current infrastructure work uses coverage of applicable validation contracts,
not fictitious application coverage numbers. Where testable application code
and coverage tooling exist, apply the approved application coverage target.
Reviewers assess acceptance and regression coverage, not merely test counts.
Provider projections preserve role and permission semantics while using native
metadata; static parity never proves discovery, model resolution, or execution.

## Current Contract

### Validation lane contract

- **affected**: selected validators run for the normalized changed paths,
  including applicable untracked Markdown. Record input scope and selection.
- **staged**: the staged runner validates the exact logical index, followed
  separately by plain `pre-commit run` against that index. Working-tree or
  all-files results do not replace either result.
- **all-files**: `pre-commit run --all-files` supplies local completion
  evidence; a supplemental all-files runner does not replace it or staged
  checks. Commit-message and manual hooks are separate.
- **message/manual**: record applicable commit-message or explicit manual-stage
  checks individually.
- **ci**: a hosted check needs its own run identity or URL. Local selection,
  workflow syntax, and Action checks are repository-static evidence only.
- **remote/live**: provider discovery or authenticated operation, remote
  execution, and operator-approved runtime checks need direct authorized
  evidence. Static presence and hosted CI do not imply this lane.

### Validation runner envelope

Every repository-static child selected by the validation-surface contract runs
through `scripts/run-validation-lane.py` with one reviewed finite envelope:

- 1,200 seconds maximum execution time per child;
- 4 MiB maximum retained stdout and 1 MiB maximum retained stderr per child;
- 2 seconds total cleanup time under one monotonic deadline; and
- 64 KiB maximum read chunks with concurrent stdout/stderr draining.

The runner starts each child in its own session/process group. Timeout, either
pipe overflow, pipe failure, or pipes held by descendants after the direct
leader exits is `FAIL`.

### Result vocabulary

- `PASS`: the named check ran over the stated scope and met its acceptance
  condition.
- `SKIP`: no applicable files or an explicitly optional tool was unavailable.
  State the reason and report any fallback separately.
- `FAIL`: execution or input validation did not meet the acceptance condition.
- `DEFER`: required authority, environment, provider, or external evidence is
  unavailable. This is a visible limitation, never a pass.

### Canonical completion sequence

1. **targeted**: run the smallest focused checks while implementing.
2. **affected**: run selected validators for every normalized changed path.
3. **staged**: stage the exact logical set, run the staged runner, then plain
   pre-commit against that index.
4. **tests**: run relevant direct suites and the applicable repository aggregate;
   preserve separate command results.
5. **all-files**: run `pre-commit run --all-files`.
6. **formatter-review**: inspect status, unstaged diff, and cached diff for every
   formatter mutation, including changes outside the original target set.
7. **rerun**: after formatter mutation, review and restage the logical set, then
   rerun affected, staged, and all-files checks. A mutating invocation is not
   completion evidence; record a reasoned `SKIP` when no rerun is needed.
8. **diff-checks**: run `git diff --check` and `git diff --cached --check`
   and confirm final scope.

Use raw NUL-delimited machine paths for changed/staged path transport. Do not
reconstruct them with newline iteration or filtered display output. Preserve
runner boundary failures and optional-tool skips rather than treating them as
successful full coverage.

### Handoff evidence contract

Record in the owning Task or approved evidence record:

- scope, changed paths, and acceptance IDs;
- commands and tool/version, with each ordered completion-step result;
- separate lane results and limitations;
- reviewer identity and disposition;
- rollback commit or bounded rollback procedure;
- residual risk and next owner.

A field may state `none` or `DEFER` with a reason, but must not silently
disappear. Do not copy raw child payload or sensitive diagnostics into evidence.

### Supply-chain identity

Retain immutable identities where byte identity is the security contract:
pinned external Actions/hooks, resolved dependency artifacts, sealed evidence,
or Git-backed recovery objects. Their owning contract records purpose and
refresh/recovery procedure. Branch HEADs, current docs, local validators, and
inventory counts are not policy pins.

## Validation and Refresh

Refresh this policy when evidence semantics change, not when a corpus count or
implementation constant changes. Preserve the distinction between repository,
provider-runtime, hosted CI, and live checks. Formatters or skipped tools
cannot silently advance a task to completion.

## Related Documents

- [Validation Surface Contract](../contracts/validation-surfaces.json)
- [Approval and Safety](approval-and-safety.md)
- [Work Lifecycle](../skills/work-lifecycle.md)
- [Git Policy](git.md)
