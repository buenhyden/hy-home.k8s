---
name: "workspace-harness-audit"
description: "Use when auditing workspace-wide SDLC, agent governance, GitOps, scripts, and QA ownership against an approved request."
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# workspace-harness-audit

## Purpose

Keep broad workspace analysis complete, evidence-backed, and bounded to the
authorized repository work. Narrow document drift belongs to
`docs-stage-conformance` instead.

## Workflow Phases

### Coverage map

Take the reading and the write boundary from
[work lifecycle](../../workflows/work-lifecycle.md) intake. What this audit adds
is the map: every area the request names gets an owner, an acceptance condition,
and an evidence source, recorded before any of them is inspected. An area with
no evidence source is recorded as uninspected rather than as clean, because a
broad audit fails by leaving a silent gap far more often than by reporting a
wrong finding.

### Authority review

Resolve each instruction, safety constraint, validation signal, and durable
knowledge claim to its current owner: `.agents/roles/registry.json` for roles
and skills, Stage 99 for document contracts, `scripts/` for executable checks.
An external catalog, benchmark, or third-party agent definition is evidence or
a strategy lens. It never authorizes expanding the roster or standing up
governance beside an existing owner.

### Disposition

For each gap, separate what the audit may settle from what it must route.
Remove a duplicate owner only when both tests pass: no consumer remains, and
Git-backed recovery covers the removal. Execute approved gaps only, change
behavior in the owning Spec, and record priority, dependencies, file ownership,
rollback, and deferred external work in the owning Plan/Task under its existing
package IDs.

### Verification and handoff

Follow [quality policy](../../governance/quality.md) and the work-lifecycle
completion sequence. Check every acceptance item against current files and
actual command results rather than against the intake map, and carry each
unresolved item into the handoff by name.

## Boundaries

- An audit request implies no live cluster, Vault, cloud, paid, credential, or
  remote action.
- A finding about native provider behavior needs runtime evidence. Tracked
  configuration shows intent, never discovery or execution.
- Registry inventories, exact gate limits, branch pins, and dated model-fitness
  snapshots stay with their owners. A skill that copies one is itself a finding.
- Durable results belong to canonical documents and Task records. An audit does
  not leave behind a progress, closure, or current-state ledger of its own.

## Outputs

A requirement-to-owner coverage map, bounded disposition decisions, approved
implementation evidence, validation limitations, and a concrete next owner.
