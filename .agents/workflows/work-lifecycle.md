---
title: "Work Lifecycle"
version: "2.1.0"
type: "governance/skill"
status: "active"
owner: "platform"
updated: "2026-10-08"
---

# Work Lifecycle

## Overview

Use one intake-to-handoff procedure for substantial repository work rather than
separate bootstrap, preflight, and postflight rule copies.

## Authority Boundary

This procedure applies [agent execution](../governance/agent-execution.md),
[approval and safety](../governance/approval-and-safety.md), and
[quality](../governance/quality.md). It does not grant new scope or override the
active Task, registry permissions, or provider controls.

## Governance Context

Start at the current provider gateway, then load the minimum relevant policy,
role responsibility, provider note, and owning Spec/Plan/Task. Re-observe Git
state on resume; historical progress and provider-local memory are auxiliary.

## Current Contract

### Intake

1. State the outcome, acceptance IDs, in/out scope, material assumptions, and
   protected actions. Resolve contradictions before editing.
2. Inspect branch/worktree, status, relevant diffs, and canonical owners. Use
   `.agents/knowledge/` to find which tree and which entry document own the
   affected area, then read that owner; the map routes and never decides.
   Preserve unrelated changes and identify the exact write boundary.
3. Select the responsibility from [roles](../roles/README.md), resolve any
   delegated role and skills from the agent registry, and load the provider
   note only for native behavior.
4. Resolve the Stage 99 profile and template before authored document changes.
   Record the current scoped request in the existing Task Inputs and Approval
   and Safety Boundaries. Keep the Spec acceptance contract, Plan work mapping
   and actual Task execution/evidence separate; no extra progress ledger.
5. Resolve selected required-check tools, environment, actual resource/output
   needs, technical command limits and necessary native execution approval through
   [quality preflight](../governance/quality.md#validation-runner-envelope).
   Define focused checks, expected lanes, rollback, unavailable tools and next
   owner before implementation; protected authority remains separate.
   Quality preflight creates no business deadline, session timebox or
   final-validation reserve approval.

### Resume

Apply the [context policy resume decision](../governance/context-and-memory.md#resume-decision)
before dependent writes. Put worktree identity, relevant file hashes, current
approval/revocation and writer ownership under the existing Task snapshot and
approval fields. Carry command limits, partial output and known budget state
under evidence limitations. On conflict, retain completed work and name the
next owner; refresh the affected evidence before resuming.

### Implementation

Make the smallest testable change. Demonstrate a focused failing case for a
changed executable behavior, then its passing result; use selected profile,
relationship, link and state checks for narrative documents. Keep active Task
evidence current. Before retiring a one-use check, transfer its ongoing
protection, remove its caller and registration, then its dedicated helper,
fixture and test when consumer-zero and Git recovery are established. Preserve
the past result in its existing Task or Archive owner. Use
[delegated development](delegated-development.md) for authorized subagents.

For an ordinary authored document or README router edit, select common diff,
applicable style and commit-message checks plus document content only, as
[quality](../governance/quality.md#ordinary-document-selection) defines. Do
not add a one-use test just to mirror prose. Treat changes to governance,
provider or native contracts, Stage 99 forms, schema or registry, and
implementation as their own contract or behavior changes with necessary
focused regressions. Document writer commands remain explicit, never an
automatic QA side effect.

Bound the attempt. Stop and report instead of continuing when the same check
fails twice with no new information, when two consecutive changes produce no
observable progress, when a repair would require widening the approved scope,
or when the obstacle is an unmet authority, an unavailable environment, or an
external limit. Classify the stop as a repository defect, a missing protected
approval, an unavailable tool or environment, a resource limit, or an authority
conflict, and name the next owner. Stop the dependent action and continue
independent approved safe work. Never weaken a contract, a gate, or a test to
end the loop.

### Completion

1. Check acceptance, links, owner boundaries, language, and README navigation
   through the [semantic review contract](../governance/quality.md#semantic-review):
   applicable automated checks plus an independent read-only reviewer.
2. Follow the delivery route and ordered sequence in
   [quality policy](../governance/quality.md#delivery-ownership). Record local
   selected QA and pre-commit lint/format over their actual snapshots. PR branch
   metadata and selected hosted style have distinct SHA/run evidence. Push and
   merge do not replay an identical leaf.
3. Review final diff scope and remove task-owned scratch/debug residue.
4. Record the canonical handoff fields in the active Task; include failures,
   skipped optional tools, unavailable runtime checks, review disposition,
   rollback, residual risk, and next owner.
5. Follow [Git policy](../governance/git.md) for requested logical commits and
   branch finish. Do not infer push, merge, or cleanup approval.

Hooks are supplemental evidence or enforcement only when their intended
runtime actually loads them. Advisory compaction output is not completion
evidence, and no historical progress-ledger append is required for new work.

## Validation and Refresh

Run the selected static checks and preserve exact results. Review this
procedure when intake, delegation, completion, or handoff routing changes;
keep shared lane meanings in quality policy.

## Related Documents

- [SDLC Flow](../governance/sdlc.md)
- [Document Authoring](../governance/document-authoring.md)
- [Context and Memory](../governance/context-and-memory.md)
- [Roles](../roles/README.md)
