---
title: "Context and Memory Policy"
version: "1.0.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-08-31"
---

# Context and Memory Policy

## Overview

Retain only the context needed to resume safely. Repository state and the
owning SDLC document, not a memory ledger, determine current truth.

## Authority Boundary

This policy owns repository context retention, resume verification, and the
boundary for advisory provider-local memory. It grants no provider/runtime
capability, execution permission, or approval authority; the active execution,
approval, and provider controls continue to own those concerns.

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
- The `memory/progress.md` ledger is retired under Spec 0054 WP-012 and the
  `memory/` directory under Spec 0065; their bytes are recoverable from Git
  through `MIG-0007` and `MIG-0009`. Progress and task status belong to the
  owning Spec Task. No governance memory directory remains, so durable
  knowledge routes to the responsible policy, skill, operating document, or
  reference owner instead.
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
- [Archive Index](../../98.archive/README.md)
- [Approval and Safety](approval-and-safety.md)
