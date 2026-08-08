---
title: 'Reference: Agent Memory Tiers and Management'
type: content/reference
status: active
owner: platform
updated: 2026-08-08
---

# Reference: Agent Memory Tiers and Management

## Overview

This reference records the workspace's four memory classes and the lifecycle
controls that prevent transient or provider-local context from becoming
authority without review.

## Reference Type

Repository-static research baseline.

## Authority Boundary

The Stage 00 memory contract owns class definitions and canonical authority.
Provider-local stores and externally retrieved resources are advisory. They
never override observed repository state or a canonical domain owner.

## Scope

It covers working short-term, durable long-term, domain-scoped, and
provider-local auxiliary memory, plus their retention, promotion, compaction,
conflict, staleness, and deletion rules.

## Definitions / Facts

### Short-term-memory baseline

`.agent-work/checkpoint.json` is ignored, advisory, and must use the closed
atomic/redacted checkpoint contract. It may contain bounded task identity,
next action, redacted evidence references, and review state, never raw
prompts/transcripts, stdout/stderr, shell history, environment dumps,
credentials, tokens, account identifiers, or secret-bearing data. On resume,
re-observe the repository and recompute; the checkpoint cannot establish
current state. Its runtime existence/use is `DEFER` and was not inspected.

### Long-term-memory baseline

`docs/00.agent-governance/memory/progress.md` is the durable shared progress
ledger. A reusable lesson must name its task, canonical owner, evidence
path/URL/commit, observation date, sensitivity, reviewer, retention/expiry,
and handoff. It remains a concise fact/decision/evidence summary, not an
operational trace or a second policy owner.

### Domain-scoped-memory baseline

The owning Spec, Runbook, Incident, or Postmortem is the domain-scoped owner
for domain constraints, decisions, recovery knowledge, and invalidation. A
cross-domain promotion requires review plus links between the prior and new
canonical owners. On supersession, archive with original/replacement provenance
instead of overwriting the historical decision.

### Memory-management baseline

| Tier | Authority and typical payload | Promotion / retention | Compaction, conflict, and deletion |
| --- | --- | --- | --- |
| `working-short-term` | Active executor; redacted checkpoint and bounded pending work. | Review/redact recurring evidence before durable promotion; discard at terminal task state. | Atomic summary only; repository re-observation wins every resume. |
| `durable-long-term` | `progress.md` or another canonical owner; reusable lesson/progress/evidence/handoff. | Retain until the owner replaces it with provenance. | Concise indexed summary; canonical owner wins conflicts. |
| `domain-scoped` | Owning Spec/Runbook/Incident/Postmortem; domain decision and operating knowledge. | Promote across domains only after review and reciprocal owner links. | Domain owner resolves conflicts; archive superseded records with replacement provenance. |
| `provider-local-auxiliary` | Provider/user-local recall, auto memory, or sandbox context. | Re-observe before use; never promotes directly to canonical memory. Provider/user retention applies after re-observation. | It is lowest authority and follows provider/user deletion controls. |

### Lifecycle rules and evidence limits

1. **Provenance and sensitivity:** capture a source identity, observation time,
   authority, fact/decision/inference/limitation label, reviewer, and a
   non-sensitive evidence reference for every promotion.
2. **Retention and staleness:** use explicit task expiry for checkpoints;
   refresh durable/domain material on the owning contract, source, or decision
   trigger. Recency alone does not resolve a conflict.
3. **Promotion and demotion:** working or domain content requires reviewed,
   redacted promotion; provider-local content first requires repository
   re-observation. Demote/discard stale task context at terminal state; archive
   superseded domain records rather than silently deleting authority.
4. **Compaction:** retain a bounded reviewed conclusion, evidence references,
   remaining-work count, and named next owner. Provider compaction mechanisms
   do not replace the local redaction/lifecycle contract.
5. **Conflict and deletion:** order is observed repository state, canonical
   domain owner, reviewed durable memory, working memory, then provider-local
   auxiliary context. A deletion request identifies exact target, authority,
   sensitivity, retention hold, and replacement/rollback disposition.

OpenAI documents configurable Codex memory/compaction and Agents SDK sessions;
Anthropic distinguishes authored instructions from machine-local auto memory;
MCP Resources describes retrieval and optional change notifications. These
surfaces do not define this repository's retention, authorization, truth, or
deletion policy, and no local provider-memory state was inspected.

## Sources

- [OpenAI Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) and [OpenAI Agents SDK sessions](https://openai.github.io/openai-agents-python/sessions/), checked 2026-08-08 (`SRC-WERPC-049`–`050`).
- [Anthropic Claude Code memory](https://code.claude.com/docs/en/memory), checked 2026-08-08 (`SRC-WERPC-051`).
- [Model Context Protocol Resources specification](https://modelcontextprotocol.io/specification/2025-11-25/server/resources), checked 2026-08-08 (`SRC-WERPC-052`).
- [Memory README](../../../00.agent-governance/memory/README.md) and `contracts/agent-checkpoint.schema.json` are local static owners.

## Review and Freshness

Refresh after a memory/checkpoint contract, canonical owner, provider memory,
MCP Resource, retention/privacy, or lifecycle-validator change. Static PASS
does not prove provider-local memory, checkpoint use, authentication, or actual
compaction execution.

## Related Documents

- [Pack coverage matrix](README.md#requirement-coverage-matrix)
- [Source ledger](source-coverage-and-migration-ledger.md)
- [Memory README](../../../00.agent-governance/memory/README.md)
