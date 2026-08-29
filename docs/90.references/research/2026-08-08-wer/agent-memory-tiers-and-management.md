---
title: 'Reference: Agent Memory Tiers and Management'
type: content/reference
status: active
owner: platform
updated: 2026-08-23
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

### 2026-08-17 full-corpus refresh

This increment is the fifth refresh cycle over this pack, executed under
Spec 058. Unlike the three preceding cycles it re-observed every owner row in
the pack rather than the twelve `Partial` rows, and it assigns each retained
`Partial` or `DEFER` row a blocking class recorded in the
[scope application index](scope-application-index.md). All observations are
dated **2026-08-17**. No live cluster, hosted CI run, provider runtime,
authenticated execution, or secret value was observed.

#### REQ-WERPC-029 through REQ-WERPC-032 re-observation

**External result:** `unchanged` for all four rows (`SRC-WERPC-078`). The Agents
SDK sessions page still documents the same session backend classes and still
declares no model-selection key. The Codex memories page is unchanged: off by
default, stored under `~/.codex/memories/`, separate from web memory, with no
retention or deletion guarantee, and explicitly described as a recall layer
rather than the only source for rules that must always apply. The Claude Code
memory page is unchanged, including the retention-sweep exclusion for memory
files and the separate-directory statement for subagent memory. The MCP
versioning page confirms the current protocol revision is still `2026-07-28`,
with no newer revision published.

**Workspace result:** `confirmed` for all four rows.
`contracts/agent-checkpoint.schema.json` still requires `synthetic`,
`atomicWrite` with the `same-directory-temp-fsync-replace` strategy, `redaction`
with the `[REDACTED-SYNTHETIC]` marker, `resume.repositoryStateWins` and its
conflict order, `compaction`, and `handoff`. `memory/README.md:45-50` still
defines exactly the four memory classes with the same authority, promotion, and
conflict table, and `memory/README.md:56-58` still forbids credentials, tokens,
secrets, and raw prompts as memory payloads. `memory/progress.md` remains the
single tracked durable ledger. `docs/03.specs/` remains populated and continues
to host domain-scoped owners.

**Status effect:** `no-change` for all four (`CLM-WERPC-011-29` through
`CLM-WERPC-011-32`).

**Blocking class:** `none` for `REQ-WERPC-029`, `030`, and `031`, which are
unblocked and remain `Verified` on contract definition.
`REQ-WERPC-032` is `provider-runtime` and structurally unreachable: provider
retention, deletion, compaction, and connected-resource behavior cannot be
observed from the repository. `REQ-WERPC-029` reopens if the checkpoint
contract version changes or a task is authorized to read ignored checkpoint
contents; `REQ-WERPC-030` reopens if the durable ledger is relocated or a second
tracked `progress.md` appears; `REQ-WERPC-032` reopens if a cited provider or
MCP memory contract changes retention, compaction, or subscription semantics.

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

| Official source                                                                                                                                                                      | Publication / revision and adopted scope                                                                                                                                                                                                                                                                    | Rejected inference, uncertainty, and refresh trigger                                                                                                                                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [OpenAI Codex memories](https://learn.chatgpt.com/docs/customization/memories)                                                                                                       | Current page with no publisher date, checked 2026-08-12. Local memories are separate from ChatGPT web memory, off by default, generated under the Codex home directory, and controlled per chat for use and future generation; required guidance belongs in `AGENTS.md` or checked-in docs.                 | The page states no complete retention or deletion guarantee. It does not prove enablement, generation, use, redaction, or storage in this environment. Recheck when memory controls, location, lifecycle, or privacy language changes.                     |
| [OpenAI Agents SDK sessions](https://openai.github.io/openai-agents-python/sessions/)                                                                                                | Current SDK documentation with no publisher date, checked 2026-08-12. Sessions retrieve and store conversation items around runs; backends have distinct persistence, `clear_session` is an interface operation, and `OpenAIResponsesCompactionSession` can rewrite an underlying session after compaction. | SDK session and compaction semantics do not transfer to Codex local memory or this repository. No backend, deletion result, or compaction was invoked. Recheck when session interfaces, storage, compaction, or deletion semantics change.                 |
| [Anthropic Claude Code memory](https://code.claude.com/docs/en/memory)                                                                                                               | Current page with no publisher date, checked 2026-08-12. Auto memory is on by default, machine-local, repository-scoped and shared across worktrees; only the first 200 lines or 25KB of its index load initially, and users can inspect, edit, or delete the Markdown files.                               | File-level edit/delete controls are not a provider retention guarantee, secure erasure result, or proof of use. Recheck when scope, load limit, storage, compaction, or deletion changes.                                                                  |
| [MCP versioning](https://modelcontextprotocol.io/specification/versioning) and [MCP 2026-07-28 Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources) | Current revision `2026-07-28`, checked 2026-08-12. Each request declares a protocol version; resources are application-driven, authorization-sensitive, list/read/cache capable, and optionally updated through `subscriptions/listen`.                                                                     | The protocol does not make retrieved data authoritative or prove a connected server, negotiated version, access control, cache behavior, notification, or retrieval. Recheck when the current revision or Resources/caching/subscription contract changes. |

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

### 2026-08-14 consistency and Partial re-observation

This bounded increment re-observed the workspace and re-checked external
sources for `REQ-WERPC-032` only, checked on **2026-08-14**. The ignored
`.agent-work/checkpoint.json` remained the named forbidden/unread boundary;
its contents were not inspected. No provider-local memory, connected-resource
content, credentials, retention/deletion result, compaction run, or
retrieval was accessed.

#### REQ-WERPC-032 workspace and source consistency check

**Workspace delta:** `no-change`. `memory/README.md` and
`contracts/harness-contract.json` still retain the same four authority
classes; `memory/progress.md` remains the durable shared ledger;
`contracts/agent-checkpoint.schema.json` remains the repository-static
schema for the ignored, advisory, atomic/redacted checkpoint. Only the
schema and ignore rule were re-read for this refresh.

**External result:** all five sources (four distinct pages) were reachable
and `unchanged` against their 2026-08-12 adopted scope, with one page
disclosing additional, non-contradicting detail.

| Source                                                                                                | Result      | Note                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ----------------------------------------------------------------------------------------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [OpenAI Codex memories](https://learn.chatgpt.com/docs/customization/memories)                        | `unchanged` | Off-by-default, `~/.codex/memories/` storage, per-chat use/generation controls, no retention/deletion guarantee, and the `AGENTS.md`-is-the-required-guidance-owner caution still match. No publisher date.                                                                                                                                                                                                                                                                                                                                                                                                                       |
| [OpenAI Agents SDK sessions](https://openai.github.io/openai-agents-python/sessions/)                 | `unchanged` | `clear_session` is still a plain interface operation; `OpenAIResponsesCompactionSession` still clears and rewrites session history and still names no model-selection key or identifier. The page now enumerates more backends (`SQLiteSession`, `OpenAIConversationsSession`, `RedisSession`, `SQLAlchemySession`, `MongoDBSession`, `DaprSession`, `AdvancedSQLiteSession`, `EncryptedSession`) than previously cited; this is additional detail, not a contradiction of the adopted claim. No publisher date.                                                                                                                  |
| [Anthropic Claude Code memory](https://code.claude.com/docs/en/memory)                                | `unchanged` | On-by-default, machine-local, repository-scoped and shared across worktrees, and the 200-line/25KB `MEMORY.md` load limit still match. The page now additionally states that `MEMORY.md` and topic files are excluded from the session-transcript `cleanupPeriodDays` sweep and "stay until you or Claude edits or deletes them," and that a subagent's own auto memory is a separate directory from the main conversation's. This extends, and does not contradict, the adopted scope; it is recorded as new supporting detail, not a promoted retention guarantee, and does not establish this workspace's effective retention. |
| [MCP versioning](https://modelcontextprotocol.io/specification/versioning)                            | `unchanged` | The current protocol revision is still stated as `2026-07-28`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| [MCP 2026-07-28 Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources) | `unchanged` | `subscriptions/listen` with a `resourceSubscriptions` filter and a subscription id in `_meta` still replaces `resources/subscribe`; `resultType`/`ttlMs`/`cacheScope` still appear on list/read/templates-list results; resource-not-found is still `-32602` with `-32002` retained for backward compatibility; every request still must carry `io.modelcontextprotocol/protocolVersion`, `clientInfo`, and `clientCapabilities` in `_meta`.                                                                                                                                                                                      |

**As-Is:** Unchanged. Four authority classes remain explicit; provider and
MCP documentation still describes local-store, deletion-control, compaction,
caching, and subscription surfaces that do not supply this repository's
authority or prove actual behavior.

**Gap and bounded target:** Unchanged. Keep provider memory and MCP results
`provider-local-auxiliary`, re-observe repository truth before use, and
promote only reviewed/redacted facts. The Claude Code memory page's newly
observed cleanup-sweep exclusion for `MEMORY.md`/topic files is a documented
product design, not an observed local retention fact, and does not change
the `DEFER` boundary.

**Missing evidence:** an authorized, non-secret, provider/version-specific
retention and deletion test against the exact store. **Owning authority:**
Stage 00 memory lifecycle and checkpoint schema. **Safe boundary:** a
separately authorized inspection of the exact provider/version and store
only; the ignored checkpoint stays unread unless a future task explicitly
authorizes recovery inspection. **Refresh trigger:** a cited provider/MCP
memory contract or a named local memory selector materially changes.

**Final disposition:** `Partial`, unchanged from the 2026-08-12 baseline. No
promotion. New source registered: `SRC-WERPC-074`. New claim registered:
`CLM-WERPC-010-04`.

### 2026-08-20 full-corpus reverification

This increment re-observed the four memory rows at workspace baseline
`8d8c8e5634fe939f8daaf041fbf5dfb444ed4a9c`. The allocation slice assigns no
new source or claim ID. Provider-local memory and MCP resources remain
auxiliary evidence and never replace a canonical repository owner.

#### REQ-WERPC-029 short-term memory and checkpoint re-observation

- **Sources and external result:** `unchanged`; `SRC-WERPC-068`,
  `SRC-WERPC-050`, and `SRC-WERPC-051` were re-observed on 2026-08-20 as
  public provider-memory and SDK-session context only.
- **Workspace selector and result:** `confirmed` at
  `agent-memory-tiers-and-management.md#short-term-memory-baseline`. The
  checkpoint contract remains ignored, synthetic, atomic, redacted, advisory,
  compactable, and subordinate to repository re-observation on resume.
- **As-Is, gap, and target:** the short-term contract remains `Verified` at
  repository-static depth. Actual checkpoint creation, compaction, recovery,
  and provider memory use were not observed. Keep task state bounded and
  repository-wins.
- **Evidence boundary:** blocking class is `none`; ignored checkpoint contents
  and provider-local memories remain unread. Provider memory or SDK sessions
  do not prove checkpoint existence, use, or authority.
- **Owner, safe follow-up, and trigger:** owner is this reference and the Stage
  00 checkpoint schema. Review only schema and lifecycle validators unless a
  future task explicitly authorizes secret-safe recovery inspection. Refresh
  when the checkpoint, redaction, resume, compaction, or recovery contract
  changes.

#### REQ-WERPC-030 long-term memory re-observation

- **Sources and external result:** `unchanged`; `SRC-WERPC-068`,
  `SRC-WERPC-050`, and `SRC-WERPC-051` were re-observed on 2026-08-20.
- **Workspace selector and result:** `confirmed` at
  `agent-memory-tiers-and-management.md#long-term-memory-baseline`. The durable
  shared ledger remains the tracked long-term owner with canonical-owner,
  provenance, sensitivity, retention, review, and handoff fields.
- **As-Is, gap, and target:** the durable lifecycle remains `Verified` at
  repository-static depth. Provider persistence, retention, deletion, and
  enforcement are unobserved and non-authoritative. Promote only reviewed,
  redacted facts with provenance into a canonical repository owner.
- **Evidence boundary:** blocking class is `none`. Provider persistence,
  session storage, or auto memory does not create or govern durable repository
  memory.
- **Owner, safe follow-up, and trigger:** owner is this reference and the Stage
  00 memory lifecycle. Use the canonical ledger and re-observe repository truth
  before importing provider-local material. Refresh when the durable ledger,
  provenance/retention lifecycle, or a cited provider memory/session contract
  changes.

#### REQ-WERPC-031 domain memory and MCP resource re-observation

- **Sources and external result:** `unchanged`; `SRC-WERPC-066` was
  re-observed on 2026-08-20. MCP versioning still names `2026-07-28` current,
  and its Resources specification remains protocol context rather than domain
  authority.
- **Workspace selector and result:** `confirmed` at
  `agent-memory-tiers-and-management.md#domain-scoped-memory-baseline`. Specs,
  Runbooks, Incidents, and Postmortems remain the domain owners; archive and
  promotion preserve provenance and review.
- **As-Is, gap, and target:** domain memory remains `Verified` at
  repository-static depth. No MCP server, authorization, version negotiation,
  retrieval, cache, or subscription was observed. Keep retrieved material
  auxiliary until re-observed and reviewed into its canonical owner.
- **Evidence boundary:** blocking class is `none`. A Resources specification
  does not prove connection, access, retrieval behavior, or authority of the
  returned data.
- **Owner, safe follow-up, and trigger:** owner is this reference and the named
  domain document owners. Authorize connector observation separately and do
  not replace domain truth with provider/MCP state. Refresh when MCP
  versioning/Resources or the domain-owner/archive contract changes.

#### REQ-WERPC-032 memory lifecycle re-observation

- **Sources and external result:** `unchanged`; `SRC-WERPC-068`,
  `SRC-WERPC-050`, `SRC-WERPC-051`, and `SRC-WERPC-066` were re-observed on
  2026-08-20.
- **Workspace selector and result:** `confirmed` at
  `agent-memory-tiers-and-management.md#memory-management-baseline`. The four
  local memory classes still require redaction, repository-wins conflict
  resolution, review-gated promotion, compaction, deletion/retention
  boundaries, handoff, and canonical-owner routing.
- **As-Is, gap, and target:** the lifecycle remains `Partial` at
  public-documentation depth. Provider retention and deletion results,
  compaction execution, secure erasure, and connected-resource behavior are
  unobserved. Keep provider-local state auxiliary and promote only reviewed,
  redacted evidence after repository re-observation.
- **Evidence boundary:** blocking class and retained boundary are
  `provider-runtime` / `DEFER`. Public memory, cache, subscription, compaction,
  or deletion controls do not prove this environment's lifecycle behavior.
- **Owner, safe follow-up, and trigger:** owner is this reference and the Stage
  00 memory/checkpoint contracts. After separate approval, perform one
  non-secret lifecycle observation against an exact provider/version/store;
  do not read ignored checkpoint contents. Refresh when a cited provider
  memory, SDK session, MCP lifecycle, or named local selector changes.

### 2026-08-23 provider-memory gap increment

This gap-only increment follows the Spec 0054 Claude/Codex-only terminal
provider boundary and changes no memory owner, checkpoint, adapter, retention
rule, or document topology.

- **Codex:** [Codex
  Memories](https://learn.chatgpt.com/docs/customization/memories) remains off by
  default and is a provider-local recall surface (`SRC-WERPC-068`). A product
  control to use or generate a memory does not prove enablement, retrieval,
  redaction, retention, deletion, or authority in this workspace.
- **Claude:** the current [Claude Code execution and context
  guide](https://code.claude.com/docs/en/how-claude-code-works) documents
  context compaction, while the [memory
  guide](https://code.claude.com/docs/en/memory) documents provider-local auto
  memory (`SRC-WERPC-051`). Compaction preserves provider conversation utility;
  it does not promote a summary or auto-memory entry into durable or
  domain-scoped repository memory.
- **Shared rule:** provider memory, compacted context, session storage, and
  retrieved resources remain `provider-local-auxiliary`. On every resume,
  re-observe repository state. Only reviewed, redacted, provenance-bearing
  facts may enter the durable ledger or the owning domain document; those
  repository owners win every conflict.

**Disposition:** `REQ-WERPC-029` through `031` remain `Verified` on their local
contracts and `REQ-WERPC-032` remains `Partial`. Provider enablement, actual
compaction, retention, deletion, retrieval, and secure-erasure behavior remain
`provider-runtime` / `DEFER`; no provider store or ignored checkpoint was read.

## Related Documents

- [Pack coverage matrix](README.md#requirement-coverage-matrix)
- [Source ledger](source-coverage-and-migration-ledger.md)
- [Memory README](../../../00.agent-governance/memory/README.md)
