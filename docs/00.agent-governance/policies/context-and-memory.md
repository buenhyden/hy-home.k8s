---
title: 'Context and Memory Policy'
type: governance/reference
status: draft
owner: platform
updated: 2026-08-28
---

# Context and Memory Policy

## Overview

Retain only the context needed to resume safely. Repository state and the
owning SDLC document, not a memory ledger, determine current truth.

## Authority Boundary

This extracted policy awaits activation in WP-003B. Until then, the active
execution and approval policies and existing checkpoint/loop protections
continue to govern; this draft grants no new authority.

The active Task owns work status, verification, and handoff. Requirements,
ADRs, Specs, Runbooks, and incident records own durable domain knowledge.
Temporary checkpoints and provider-local memory are advisory and confer no
execution authority.

## Governance Context

Compaction and handoff can preserve useful summaries while also carrying stale
assumptions. On resume, re-observe Git state, the active Task, and changed
canonical owners before using remembered paths, results, or approvals.

## Current Contract

- Keep working context bounded, factual, redacted, and scoped to one task.
  Record remaining acceptance criteria and next owner rather than raw sessions.
- Promote recurring knowledge only after review into the appropriate policy,
  skill, operating document, or reference record. Do not create a duplicate
  current-state ledger.
- Provider-local recall never writes canonical truth directly; verify it
  against the repository first. A provider's memory feature does not change
  repository ownership or permission.
- Discard task-local context after its useful evidence reaches the owner.
  Refresh, supersede, or retire durable knowledge through its profile contract.
- Do not read or store credentials, secret values, auth configuration, shell
  history, environment dumps, raw prompts, or complete provider transcripts.
- The retained `memory/progress.md` is transitional historical context, not an
  intake prerequisite or new-work destination. Its later disposition belongs
  to the approved progress-owner retirement work package.
- Ignored checkpoints are optional recovery aids. Static validation of a
  synthetic checkpoint proves neither actual checkpoint execution nor provider
  memory, hook, or compaction behavior.

## Validation and Refresh

Check summaries for stale owner links, duplicated task state, and sensitive
data. Report conflicting memory rather than rewriting the repository to match
it. Use [quality policy](quality.md) for evidence and handoff classification.

## Related Documents

- [Work Lifecycle](../skills/work-lifecycle.md)
- [Document Lifecycle](document-lifecycle.md)
- [Memory Transition Router](../memory/README.md)
- [Approval and Safety](approval-and-safety.md)
