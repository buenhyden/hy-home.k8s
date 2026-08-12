---
title: 'Reference: Agent Memory Tiers and Management'
type: content/reference
status: active
owner: platform
updated: 2026-08-10
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

| Tier                       | Authority and typical payload                                                        | Promotion / retention                                                                                                     | Compaction, conflict, and deletion                                                                                                                                                                                        |
| -------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `working-short-term`       | Active executor; redacted checkpoint and bounded pending work.                       | Review/redact recurring evidence before durable promotion; discard at terminal task state.                                | Atomic summary only; repository re-observation wins every resume.                                                                                                                                                         |
| `durable-long-term`        | `progress.md` or another canonical owner; reusable lesson/progress/evidence/handoff. | Retain until the owner replaces it with provenance.                                                                       | Concise indexed summary; canonical owner wins conflicts.                                                                                                                                                                  |
| `domain-scoped`            | Owning Spec/Runbook/Incident/Postmortem; domain decision and operating knowledge.    | Promote across domains only after review and reciprocal owner links.                                                      | A compacted domain record retains the reviewed conclusion, its evidence references, and the archive/replacement provenance link; domain owner resolves conflicts; archive superseded records with replacement provenance. |
| `provider-local-auxiliary` | Provider/user-local recall, auto memory, or sandbox context.                         | Re-observe before use; never promotes directly to canonical memory. Provider/user retention applies after re-observation. | It is lowest authority and follows provider/user deletion controls; content must pass the same never-list as the checkpoint contract before it enters `working-short-term`.                                               |

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

### 2026-08-10 freshness re-check

All four external sources were re-read on 2026-08-10 and none changed inside
the 2026-08-08 to 2026-08-10 window. The re-check did surface one material fact
that the original observation missed: the pinned Model Context Protocol revision
this report cites is superseded.

| Observation                      | Finding                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Effect on this report                                                                                                                                                           |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MCP revision currency            | `2025-11-25` remains published and reachable, but the MCP versioning page states the current protocol revision is `2026-07-28` ([SRC-WERPC-066](source-coverage-and-migration-ledger.md#source-register)). That revision pre-dates the 2026-08-08 check, so this is a missed-currency correction, not a two-day change.                                                                                                                                                        | The connected-resource statements here describe the `2025-11-25` semantics only. They remain accurate for that revision and must not be read as current-protocol claims.        |
| MCP resource semantics delta     | At `2026-07-28`, `resources/subscribe` is replaced by `subscriptions/listen` with a `resourceSubscriptions` filter and a subscription id in `_meta`; `resources/list`, `resources/read`, and `resources/templates/list` gain `resultType`, `ttlMs`, and `cacheScope`; resource-not-found moves from `-32002` to `-32602` with `-32002` retained for compatibility; every request must carry `io.modelcontextprotocol/protocolVersion`, `clientInfo`, and `clientCapabilities`. | Any future domain-scoped memory design that assumes the cited retrieval and subscription shape must re-derive it from `2026-07-28`. This report does not adopt those semantics. |
| Codex and Claude memory surfaces | `config-reference`, the Agents SDK sessions page, and the Claude Code memory page were reachable and consistent with the claims already recorded. None publishes a last-modified date, so "unchanged" here is content identity, not a publisher freshness signal.                                                                                                                                                                                                              | No claim changes. The absence of a publisher timestamp is itself a recorded limit.                                                                                              |

No status in this report is promoted by this re-check. `REQ-WERPC-032` stays
`Partial` because provider retention, deletion, compaction, and
connected-resource behavior still require runtime evidence that is `DEFER`.

## Sources

- [OpenAI Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) and [OpenAI Agents SDK sessions](https://openai.github.io/openai-agents-python/sessions/), checked 2026-08-08, re-checked 2026-08-10 (`SRC-WERPC-049`–`050`).
- [Anthropic Claude Code memory](https://code.claude.com/docs/en/memory), checked 2026-08-08, re-checked 2026-08-10 (`SRC-WERPC-051`).
- [Model Context Protocol Resources specification](https://modelcontextprotocol.io/specification/2025-11-25/server/resources), checked 2026-08-08, re-checked 2026-08-10 and confirmed superseded (`SRC-WERPC-052`).
- [Model Context Protocol versioning](https://modelcontextprotocol.io/specification/versioning) and the [2026-07-28 Resources specification](https://modelcontextprotocol.io/specification/2026-07-28/server/resources), checked 2026-08-10 (`SRC-WERPC-066`).
- [Memory README](../../../00.agent-governance/memory/README.md) and `contracts/agent-checkpoint.schema.json` are local static owners.

## Review and Freshness

Refresh after a memory/checkpoint contract, canonical owner, provider memory,
MCP Resource, retention/privacy, or lifecycle-validator change. Static PASS
does not prove provider-local memory, checkpoint use, authentication, or actual
compaction execution.

External sources were re-checked on 2026-08-10; no cited claim changed inside
that window. The re-check recorded that the pinned `2025-11-25` MCP revision is
superseded by `2026-07-28`, so treat every MCP statement here as revision-scoped
rather than current-protocol. None of the four sources publishes a last-modified
date, so an unchanged result is content identity rather than a publisher signal.

### 2026-08-11 Partial/DEFER incremental refresh

This bounded increment was executed and checked on **2026-08-12**. The heading
identifies the approved package date rather than the check date. The ignored
`.agent-work/checkpoint.json` was treated only as the named forbidden/unread
boundary; its contents were not inspected. No provider-local memory,
connected-resource content, credentials, retention/deletion result, compaction
run, or retrieval was accessed.

#### REQ-WERPC-032 provider and MCP lifecycle delta

| Official source | Publication / revision and adopted scope | Rejected inference, uncertainty, and refresh trigger |
| --- | --- | --- |
| [OpenAI Codex memories](https://learn.chatgpt.com/docs/customization/memories) | Current page with no publisher date, checked 2026-08-12. Local memories are separate from ChatGPT web memory, off by default, generated under the Codex home directory, and controlled per chat for use and future generation; required guidance belongs in `AGENTS.md` or checked-in docs. | The page states no complete retention or deletion guarantee. It does not prove enablement, generation, use, redaction, or storage in this environment. Recheck when memory controls, location, lifecycle, or privacy language changes. |
| [OpenAI Agents SDK sessions](https://openai.github.io/openai-agents-python/sessions/) | Current SDK documentation with no publisher date, checked 2026-08-12. Sessions retrieve and store conversation items around runs; backends have distinct persistence, `clear_session` is an interface operation, and `OpenAIResponsesCompactionSession` can rewrite an underlying session after compaction. | SDK session and compaction semantics do not transfer to Codex local memory or this repository. No backend, deletion result, or compaction was invoked. Recheck when session interfaces, storage, compaction, or deletion semantics change. |
| [Anthropic Claude Code memory](https://code.claude.com/docs/en/memory) | Current page with no publisher date, checked 2026-08-12. Auto memory is on by default, machine-local, repository-scoped and shared across worktrees; only the first 200 lines or 25KB of its index load initially, and users can inspect, edit, or delete the Markdown files. | File-level edit/delete controls are not a provider retention guarantee, secure erasure result, or proof of use. Recheck when scope, load limit, storage, compaction, or deletion changes. |
| [MCP versioning](https://modelcontextprotocol.io/specification/versioning) and [MCP 2026-07-28 Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources) | Current revision `2026-07-28`, checked 2026-08-12. Each request declares a protocol version; resources are application-driven, authorization-sensitive, list/read/cache capable, and optionally updated through `subscriptions/listen`. | The protocol does not make retrieved data authoritative or prove a connected server, negotiated version, access control, cache behavior, notification, or retrieval. Recheck when the current revision or Resources/caching/subscription contract changes. |

**As-Is:** `memory/README.md` and `contracts/harness-contract.json` retain four
authority classes. `memory/progress.md` is the durable shared ledger;
`contracts/agent-checkpoint.schema.json` is the repository-static schema for an
ignored, advisory, atomic/redacted checkpoint with repository-wins recovery,
compaction, lifecycle, and handoff fields. Only the schema and ignore rule were
read for this refresh.

**Gap and bounded target:** Current provider and MCP documentation describes
local-store, deletion-control, compaction, caching, and subscription surfaces,
but none supplies this repository's authority or proves actual behavior. Keep
provider memory and MCP results `provider-local-auxiliary`,
re-observe repository truth before use, and promote only reviewed/redacted
facts. Any retention, deletion, compaction, or retrieval claim needs a
separately authorized, non-secret test against the exact provider/version and
store; the ignored checkpoint remains unread unless a future task explicitly
authorizes recovery inspection.

**Final disposition:** `Partial`. Evidence depth is current official public
contract plus exact repo-static memory, progress, ignore, and schema selectors.
Owner: Stage 00 memory lifecycle and checkpoint schema. Refresh when a cited
provider/MCP memory contract or a named local memory selector materially
changes.

## Related Documents

- [Pack coverage matrix](README.md#requirement-coverage-matrix)
- [Source ledger](source-coverage-and-migration-ledger.md)
- [Memory README](../../../00.agent-governance/memory/README.md)
