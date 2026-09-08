---
title: "Quality and Evidence Policy"
version: "1.2.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-09-08"
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

- **quick / affected**: selected checks cover normalized working-tree changes,
  including applicable new files and deletion/rename paths. Record selection
  and the snapshot actually checked.
- **staged**: validate the exact logical Git index in an isolated snapshot.
  Unstaged repairs cannot hide invalid staged content. Working-tree full QA
  does not replace this byte-specific evidence; commit-message hooks remain
  separate.
- **full / all-files**: the full QA profile validates the final working tree,
  including one unit discovery and one all-files pre-commit invocation at the
  explicit manual stage. Commit-msg remains separate. Do not
  repeat either command on unchanged bytes outside that profile.
- **message/manual**: record applicable commit-message or explicit manual-stage
  checks individually.
- **ci**: the hosted QA job executes the same static gates and configuration as
  full on its immutable checkout. Branch/event policy and required summary
  are CI-specific. A hosted result needs its exact SHA and run identity;
  locally executing the ci profile is still local evidence.
- **remote/live**: provider discovery or authenticated operation, remote
  execution, and operator-approved runtime checks need direct authorized
  evidence. Static presence and hosted CI do not imply this lane.

A QA profile selects gate IDs; a lane describes routing or an evidence boundary.
The execution registry owns commands and profile membership. A logical gate
runs once per identical input snapshot, configuration, and validation mode.
Different index and working-tree bytes require separate evidence.

### Validation runner envelope

Every repository-static child selected by the validation-surface contract runs
through the [validation runner](../../scripts/run-validation-lane.py), which
owns the reviewed limit constants. The envelope bounds execution time and
retained stdout and stderr independently, uses one monotonic cleanup deadline,
and drains both streams concurrently in bounded read chunks.

The runner starts each child in its own session/process group. Timeout, either
pipe overflow, pipe failure, or pipes held by descendants after the direct
leader exits is `FAIL`.

### Result vocabulary

- `PASS`: the named check ran over the stated scope and met its acceptance
  condition.
- `SKIP`: no applicable files or an explicitly optional tool was unavailable.
  State the reason and report any fallback separately.
- `FAIL`: execution or input validation did not meet the acceptance condition.
  Missing required tools/modules, invalid registry, cancellation, timeout,
  output overflow, and cleanup failure cannot become SKIP or PASS.
- `DEFER`: required authority, environment, provider, or external evidence is
  unavailable. This is a visible limitation, never a pass.

### Canonical completion sequence

1. **targeted**: reproduce changed behavior and run focused checks while implementing.
2. **quick**: validate the affected working-tree snapshot during work.
3. **each logical commit**: inspect status and the unstaged diff, stage only the
   reviewed logical set, inspect the cached diff, run `git diff --check` and
   `git diff --cached --check`, then exact-index staged QA. Validate the actual
   message under Git policy and commit through normal active hooks.
4. **final full**: before handoff run full QA on the final working tree. Its unit
   discovery and pre-commit gate are not repeated on identical inputs under
   another command name. Full/ci equality is checked by contract tests.
5. **repair and refresh**: inspect formatter findings, explicitly fix selected
   files, review/restage changed bytes and refresh affected evidence. QA itself
   never fixes source files. A final full failure keeps the work incomplete.
6. **evidence handoff**: record the checked snapshot and any subsequent Task-only
   changes separately, validating those document changes without a self-SHA or
   elapsed-time rewrite loop. Review final diff scope and remaining acceptance.

For a no-commit request preserve the index and record staged/message evidence
as N/A. Input identity includes bytes, base/history, configuration and mode;
a matching filename set alone never justifies evidence reuse.

Use raw NUL-delimited machine paths for changed/staged path transport. Do not
reconstruct them with newline iteration or filtered display output. Preserve
runner boundary failures and optional-tool skips rather than treating them as
successful full coverage.

### Handoff evidence contract

Record in the owning Task or approved evidence record:

- scope, changed paths, and acceptance IDs;
- the snapshot the work sits on: branch, HEAD, and the base it diverged from;
- commands and tool/version, with each ordered completion-step result;
- separate lane results and limitations;
- the approval boundary in force: what was authorized and what was not;
- reviewer identity and disposition;
- rollback commit or bounded rollback procedure;
- residual risk and next owner.

A field may state `none` or `DEFER` with a reason, but must not silently
disappear. Do not copy raw child payload or sensitive diagnostics into evidence.

These fields carry a handoff between providers as well as between people. The
receiver re-observes Git, the owning Task, and the canonical owner before
acting; a recorded snapshot says which state the evidence described, and a
recorded boundary keeps a past authorization from being read as a standing
one. Neither field grants authority, and a stale record never widens it.

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

- [Validation Routing Registry](../../scripts/validation/registry.json)
- [Approval and Safety](approval-and-safety.md)
- [Work Lifecycle](../workflows/work-lifecycle.md)
- [Git Policy](git.md)
- [Formatting and Linting Policy](formatting-and-linting.md)
