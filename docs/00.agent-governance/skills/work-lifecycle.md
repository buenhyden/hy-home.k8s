---
title: 'Work Lifecycle'
version: "1.0"
type: governance/reference
layer: "00.agent-governance"
status: active
owner: platform
updated: 2026-08-28
---

# Work Lifecycle

## Overview

Use one intake-to-handoff procedure for substantial repository work rather than
separate bootstrap, preflight, and postflight rule copies.

## Authority Boundary

This procedure applies [agent execution](../policies/agent-execution.md),
[approval and safety](../policies/approval-and-safety.md), and
[quality](../policies/quality.md). It does not grant new scope or override the
active Task, registry permissions, or provider controls.

## Governance Context

Start at the current provider gateway, then load the minimum relevant policy,
role responsibility, provider note, and owning Spec/Plan/Task. Re-observe Git
state on resume; historical progress and provider-local memory are auxiliary.

## Current Contract

### Intake

1. State the outcome, acceptance IDs, in/out scope, material assumptions, and
   protected actions. Resolve contradictions before editing.
2. Inspect branch/worktree, status, relevant diffs, and canonical owners.
   Preserve unrelated changes and identify the exact write boundary.
3. Select the responsibility from [roles](../roles/README.md), resolve any
   delegated role and skills from the agent registry, and load the provider
   note only for native behavior.
4. Resolve the Stage 99 profile and template before authored document changes.
5. Define focused checks, expected evidence lanes, rollback, unavailable tools,
   and the next owner before implementation.

### Implementation

Make the smallest testable change. Demonstrate a focused failing case for a
changed behavior, then its passing result. Keep active Task evidence current
and remove touched duplication only after consumer and recovery disposition.
Use [delegated development](delegated-development.md) for authorized subagents.

### Completion

1. Check acceptance, links, owner boundaries, language, and README navigation.
2. Follow the complete ordered sequence in
   [quality policy](../policies/quality.md#canonical-completion-sequence).
3. Review final diff scope and remove task-owned scratch/debug residue.
4. Record the canonical handoff fields in the active Task; include failures,
   skipped optional tools, unavailable runtime checks, review disposition,
   rollback, residual risk, and next owner.
5. Follow [Git policy](../policies/git.md) for requested logical commits and
   branch finish. Do not infer push, merge, or cleanup approval.

Hooks are supplemental evidence or enforcement only when their intended
runtime actually loads them. Advisory compaction output is not completion
evidence, and no historical progress-ledger append is required for new work.

## Validation and Refresh

Run the selected static checks and preserve exact results. Review this
procedure when intake, delegation, completion, or handoff routing changes;
keep shared lane meanings in quality policy.

## Related Documents

- [SDLC Flow](../sdlc.md)
- [Document Authoring](../policies/document-authoring.md)
- [Context and Memory](../policies/context-and-memory.md)
- [Roles](../roles/README.md)
