---
name: "workspace-harness-audit"
description: "Use when auditing workspace-wide SDLC, agent governance, GitOps, scripts, and QA ownership against an approved request."
---

# workspace-harness-audit

## Purpose

Keep broad workspace analysis complete, evidence-backed, and bounded to the
authorized repository work. For narrow document drift use docs-stage-conformance.

## Workflow Phases

### Intake

Read the provider gateway, relevant Stage 00 policies, active Spec/Plan/Task,
and current diff. Map every requested area to an owner, acceptance condition,
and evidence source. Record unknowns and named-skill availability without
claiming uninspected areas complete.

### Authority and dependency review

Map instructions, safety constraints, validation feedback, and durable
knowledge to their current owners. Use `docs/00.agent-governance/roles/registry.json` for roles and
skills, Stage 99 for document contracts, and scripts for executable checks.
External catalogs are evidence or strategy lenses, not automatic permission
to expand the roster or create parallel governance.

### Plan and implementation

Record gaps, priority, dependencies, file ownership, rollback, and deferred
external work in the owning Plan/Task. Reuse approved package IDs and preserve
user changes. Execute only approved gaps; remove touched duplicate owners
after consumer-zero and applicable Git-backed recovery. Keep UI design-system
authority at root `DESIGN.md` and change behavior in its Spec.

### Verification and handoff

Use the ordered sequence and result meanings in
`docs/00.agent-governance/policies/quality.md`. Audit every acceptance item
against current files and actual command results. Keep unresolved items
visible, record review and next owner, and remove task-owned temporary output.

## Boundaries

- No live cluster, Vault, cloud, paid, credential, or remote action follows
  implicitly from an audit request.
- Native provider settings differ; explicit repository validation remains
  necessary. Static projection presence does not prove discovery or execution.
- Skills must not duplicate registry inventories, exact gate limits, branch
  pins, or dated model-fitness snapshots.
- Durable results belong to canonical documents and Task records, not a
  parallel progress, closure, or current-state ledger.

## Outputs

A requirement-to-owner coverage map, bounded disposition decisions, approved
implementation evidence, validation limitations, and a concrete next owner.
