---
title: "Reference: Agent Memory Tiers and Management"
version: "1.2.0"
type: "reference/research"
status: "published"
owner: "platform"
updated: "2026-09-27"
layer: "references"
artifact_id: "RES-0001-m0011"
---

# Reference: Agent Memory Tiers and Management

## Overview

This reference distinguishes task context, reviewed durable project knowledge, domain knowledge and provider-local recall. Storage, eligibility, retrieval, context inclusion and correct application are separate stages. The current external research describes lifecycle choices and risks without inspecting memory stores.

## Reference Type

External primary-source research directly read on 2026-09-27, with conditional investigation design and preserved historical evidence.

## Authority Boundary

Official documentation establishes only bounded external product facts. This reference defines no local permission, model promotion, memory retention rule or provider configuration change. Current workspace availability, parsing, entitlement, effective settings, execution, cost, retrieval and correct application are `not observed in this cycle`. Candidate selectors are unobserved. Private settings, account records, memory stores, credentials and conversations are excluded. External claim judgment is separate from source refresh result and repository-static document QA.

## Scope

Primary owner of U30 and existing REQ-WERPC-029 through REQ-WERPC-032. Includes authority/lifetime/readers, storage choices, promotion/review/provenance, TTL/expiry/deletion/correction, conflicts, poisoning, sensitive-data exclusion, compaction and portable handoff. Excludes private memories, conversations, ignored checkpoints, connected-resource contents and runtime recall/deletion experiments.

## Definitions / Facts

### Memory authority and lifecycle

`CLM-WERPC-017-141` proposes tiers by authority, audience and lifetime rather than one generic memory folder. These names are analytical choices, not a universal vendor standard or a new local retention policy.

| Tier / audience | Purpose and storage choice | Lifecycle and trade-off |
| --- | --- | --- |
| Task/session context / active executor | Current goal, acceptance and short-lived observations in a bounded session or checkpoint. | Fast and relevant, but context truncation/compaction and stale approval can lose meaning. Re-observe on resume and expire temporary work through its authorized owner. |
| Durable reviewed project knowledge / team | Canonical versioned Task, decision, guide or other existing owner plus Git evidence. | Reviewable and portable, but duplicate ledgers create conflicting truth. Promote only reusable redacted facts; correct with provenance. |
| Domain-scoped knowledge / authorized domain readers | Owning domain records or a controlled retrieval backend. | Better relevance and access boundaries; cross-domain promotion requires reviewed links and explicit readership. |
| Provider-local recall / product-user scope | Generated notes or product/session backend convenience. | Low maintenance for recall, with product-specific defaults, lifecycle and portability. It does not become shared authority merely by being stored. |

`CLM-WERPC-017-142` records Claude Code's documented default auto memory: machine/repository scope shared across worktrees, with separate subagent memory; startup reads only the first 200 lines or 25KB of `MEMORY.md`, while topic files load on demand. Memory files persist until edited/deleted and are outside the session-transcript `cleanupPeriodDays` sweep. Authored required instructions remain separate. File edit/delete is not secure backup erasure or proof of use. Source: SRC-WERPC-004 in [current source observations](m0012-source-coverage.md#current-source-observations).

`CLM-WERPC-017-143` records Codex local memories as off by default, enabled through `features.memories`, generated below Codex home `memories/` and controlled per chat for generation/use. When the feature is enabled, documented generate/use defaults are true; `disable_on_external_context` defaults false and can exclude MCP/web/tool-search threads from generation when enabled. `max_rollout_age_days` defaults 30 with 0–90 clamp; `max_unused_days` defaults 30 with 0–365 clamp. These are consolidation eligibility bounds, **not a secure deletion TTL**. Other generation defaults include six-hour idle eligibility and 25% rate-limit headroom. Required team rules belong in instruction files/checked-in documents; recall is not guaranteed. Sources: SRC-WERPC-068 and 049. No store, generation or effective setting was observed.

`CLM-WERPC-017-144` separates SDK session backends from knowledge stores. OpenAI Agents SDK sessions expose get/add/pop/clear with SQL, Redis, hosted and custom choices; host namespace, access and storage security remain host responsibilities. `clear_session` is an interface operation, not backup destruction. Serialized compaction may attempt restoration and still fail at the backend, leaving history unrestored. Session history is neither Codex local memories nor a fact registry. Source: SRC-WERPC-050. Prefer existing versioned records for reviewed project facts; add a retrieval store only when scale/access requirements justify its maintenance and deletion burden.

`CLM-WERPC-017-145` proposes provenance fields: claim/source URL or Git revision, creation and last-review date, canonical owner, scope/readership, trust/confidence, sensitivity, expiry and correction/successor relationship. MCP revision 2026-07-28 requires URI validation/sanitization and recommends access checks; transport/tool authentication and authorization scopes remain separate. A resource read supplies untrusted data, not instruction authority or permission. Provider external-context exclusion is not a complete poisoning defense. Quarantine untrusted candidates, review/redact before promotion and restrict readership to the least necessary scope. Source: SRC-WERPC-087; the protocol revision is externally reverified through SRC-WERPC-066, not locally negotiated.

`CLM-WERPC-017-146` proposes capture → review/redact/deduplicate → promote to an existing canonical owner → refresh/expire → correct/delete with retained successor provenance. Keep fact, inference and preference distinct. Resolve duplicates and conflicts through source/date/evidence and accountable owner; neither a newer timestamp nor repeated retrieval can overrule current configuration or approval. Define TTL separately for temporary context, stale cached evidence, retained decisions and legal/security holds. Correction must affect the index/cache and future retrieval as well as the source body. Deletion must state its scope, backup/retention limits and authorized owner; do not promise secure erasure from a file removal. Anthropic structured-note/relevant-retrieval guidance supports these mechanisms, not this proposed full TTL workflow. Sources: SRC-WERPC-125, 004, 049, 050 and 087.

### Retrieval poisoning and handoff

`CLM-WERPC-017-147` bounds compaction and recovery. Summaries and tool-output clearing can lose qualifiers, exact source support, failed attempts and approval limits. Claude resume/fork can retain old history while current files differ; a file checkpoint is not Git history or external-database rollback. Re-read goal, current Git identity, owned paths, canonical Task/evidence and approval unknowns after compaction or handoff. Durable records need enough provenance to recover the source rather than preserve every transcript. Sources: SRC-WERPC-125 and 096.

`CLM-WERPC-017-148` treats provider transfer as a one-time reviewed operation. Codex import can include Claude project memory and recent chats, but does not establish continuous sync, universal formats or semantic parity. Versioned canonical files, Git and Task references are the more portable shared handoff option, with source freshness and recipient re-observation. The proposed handoff fields and cross-provider cost/security comparisons are owned by [workspace governance](m0001-workspace-governance-and-common-agent-environment.md#cross-provider-governance). Private memory/chat import is excluded in this cycle. Source: SRC-WERPC-137.

`CLM-WERPC-017-149` distinguishes **stored → indexed/eligible → retrieved → included in context → correctly applied**. Startup bounds, topic retrieval, exclusion settings, authorization and lossy compaction can fail at different stages. A file count demonstrates none of relevance, freshness or safe application. A later authorized synthetic evaluation should check cited source support, relevant recall, exclusion of expired/retracted facts, correction propagation, deleted-item cache invalidation, permission separation and task accuracy. Keep storage/deletion metadata and behavioral retrieval evidence distinct; the current result of every workspace stage is `not observed in this cycle`.

Memory poisoning and prompt injection can persist a malicious instruction as an apparently useful remembered fact. Treat retrieved/ingested text as data, keep executable/system instructions at their authorized owner, block sensitive content before persistence, preserve provenance and independent review, and test with synthetic conflicting and revoked notes. Domain namespaces and access checks reduce accidental leakage but do not certify resistance to adversarial context. Recovery must identify affected facts/readers and correction/deletion scope without collecting raw private memory. These are conditional controls, not observed filtering effectiveness.

### Memory verification questions

`CLM-WERPC-017-150` points to the [central evidence-contract ledger](m0013-scope-application-index.md#follow-up-question-ledger). Current results are `not observed in this cycle`; candidate file types are canonical Tasks/domain records, memory policy/schema, synthetic backend fixtures, retrieval indexes and non-secret provider feature declarations. Private memories, transcripts and credential-bearing stores remain excluded.

- Q-WERPC-176: which tier, owner, lifetime, authorized readers and backend holds each kind of context, and how does one-time provider import affect portability/scope?
- Q-WERPC-177: what source/date/trust/sensitivity fields and review/redaction gate permit promotion into a canonical owner?
- Q-WERPC-178: do TTL, consolidation eligibility, correction/deletion, cache invalidation and backup retention have distinct contracts and demonstrable boundaries?
- Q-WERPC-179: how do deduplication, stale-source withdrawal and conflicts avoid shadow policy and ensure stored knowledge is actually retrieved and correctly applied?
- Q-WERPC-180: do synthetic poisoning/injection and cross-domain access cases remain quarantined and unable to change authority or expose sensitive data?
- Q-WERPC-181: what compaction losses occur, and can a recipient recover goal, Git/Task identity, evidence and approval by re-observing canonical records?

### Historical observations and corrections — 2026-08-08 to 2026-09-05

The following preserves original observation dates, identities, statuses, evidence limits and correction relationships. Retired owners and product assumptions are dated provenance, not current instructions or workspace findings. Current workspace result: `not observed in this cycle`.

#### Historical Overview

This reference records the workspace's four memory classes and the lifecycle
controls that prevent transient or provider-local context from becoming
authority without review.

#### Historical Reference Type

Repository-static research baseline.

#### Historical Authority Boundary

The Stage 00 memory contract owns class definitions and canonical authority.
Provider-local stores and externally retrieved resources are advisory. They
never override observed repository state or a canonical domain owner.

#### Historical Scope

It covers working short-term, durable long-term, domain-scoped, and
provider-local auxiliary memory, plus their retention, promotion, compaction,
conflict, staleness, and deletion rules.

#### Historical Definitions / Facts

#### Short-term-memory baseline

> [!NOTE]
> The rows below are observations at the dates their cycles record, not the
> current owner graph. `docs/00.agent-governance/` and its `memory/`, `rules/`,
> `contracts/` and `harness-catalog.md` were retired, `.agents/agents/` and
> `.gemini/` are not part of the current two-provider surface, and common
> authority now lives under `.agents/` with progress owned by the Stage 03 Task.

`.agent-work/checkpoint.json` is ignored, advisory, and must use the closed
atomic/redacted checkpoint contract. It may contain bounded task identity,
next action, redacted evidence references, and review state, never raw
prompts/transcripts, stdout/stderr, shell history, environment dumps,
credentials, tokens, account identifiers, or secret-bearing data. On resume,
re-observe the repository and recompute; the checkpoint cannot establish
current state. Its runtime existence/use is `DEFER` and was not inspected.

#### Long-term-memory baseline

At the 2026-08-14 observation the durable shared progress ledger was
`docs/00.agent-governance/memory/progress.md`. That ledger and the whole
governance memory tree were retired afterwards; the current owners are the
Stage 03 Task for progress and verification, and
`.agents/governance/context-and-memory.md` for the retention contract. The
shape recorded then still describes what a reusable lesson must name: its task,
canonical owner, evidence path/URL/commit, observation date, sensitivity,
reviewer, retention/expiry, and handoff, as a concise fact/decision/evidence
summary rather than an operational trace or a second policy owner.

#### Domain-scoped-memory baseline

The owning Spec, Runbook, Incident, or Postmortem is the domain-scoped owner
for domain constraints, decisions, recovery knowledge, and invalidation. A
cross-domain promotion requires review plus links between the prior and new
canonical owners. On supersession, archive with original/replacement provenance
instead of overwriting the historical decision.

#### Memory-management baseline

| Tier                       | Authority and typical payload                                                        | Promotion / retention                                                                                                     | Compaction, conflict, and deletion                                                                                                                                                                                        |
| -------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `working-short-term`       | Active executor; redacted checkpoint and bounded pending work.                       | Review/redact recurring evidence before durable promotion; discard at terminal task state.                                | Atomic summary only; repository re-observation wins every resume.                                                                                                                                                         |
| `durable-long-term`        | `progress.md` or another canonical owner; reusable lesson/progress/evidence/handoff. | Retain until the owner replaces it with provenance.                                                                       | Concise indexed summary; canonical owner wins conflicts.                                                                                                                                                                  |
| `domain-scoped`            | Owning Spec/Runbook/Incident/Postmortem; domain decision and operating knowledge.    | Promote across domains only after review and reciprocal owner links.                                                      | A compacted domain record retains the reviewed conclusion, its evidence references, and the archive/replacement provenance link; domain owner resolves conflicts; archive superseded records with replacement provenance. |
| `provider-local-auxiliary` | Provider/user-local recall, auto memory, or sandbox context.                         | Re-observe before use; never promotes directly to canonical memory. Provider/user retention applies after re-observation. | It is lowest authority and follows provider/user deletion controls; content must pass the same never-list as the checkpoint contract before it enters `working-short-term`.                                               |

#### Lifecycle rules and evidence limits

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

#### 2026-08-10 freshness re-check

All four external sources were re-read on 2026-08-10 and none changed inside
the 2026-08-08 to 2026-08-10 window. The re-check did surface one material fact
that the original observation missed: the pinned Model Context Protocol revision
this report cites is superseded.

| Observation                      | Finding                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Effect on this report                                                                                                                                                           |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MCP revision currency            | `2025-11-25` remains published and reachable, but the MCP versioning page states the current protocol revision is `2026-07-28` ([SRC-WERPC-066](m0012-source-coverage.md#source-register)). That revision pre-dates the 2026-08-08 check, so this is a missed-currency correction, not a two-day change.                                                                                                                                                        | The connected-resource statements here describe the `2025-11-25` semantics only. They remain accurate for that revision and must not be read as current-protocol claims.        |
| MCP resource semantics delta     | At `2026-07-28`, `resources/subscribe` is replaced by `subscriptions/listen` with a `resourceSubscriptions` filter and a subscription id in `_meta`; `resources/list`, `resources/read`, and `resources/templates/list` gain `resultType`, `ttlMs`, and `cacheScope`; resource-not-found moves from `-32002` to `-32602` with `-32002` retained for compatibility; every request must carry `io.modelcontextprotocol/protocolVersion`, `clientInfo`, and `clientCapabilities`. | Any future domain-scoped memory design that assumes the cited retrieval and subscription shape must re-derive it from `2026-07-28`. This report does not adopt those semantics. |
| Codex and Claude memory surfaces | `config-reference`, the Agents SDK sessions page, and the Claude Code memory page were reachable and consistent with the claims already recorded. None publishes a last-modified date, so "unchanged" here is content identity, not a publisher freshness signal.                                                                                                                                                                                                              | No claim changes. The absence of a publisher timestamp is itself a recorded limit.                                                                                              |

No status in this report is promoted by this re-check. `REQ-WERPC-032` stays
`Partial` because provider retention, deletion, compaction, and
connected-resource behavior still require runtime evidence that is `DEFER`.

#### 2026-08-17 full-corpus refresh

This increment is the fifth refresh cycle over this pack, executed under
Spec 058. Unlike the three preceding cycles it re-observed every owner row in
the pack rather than the twelve `Partial` rows, and it assigns each retained
`Partial` or `DEFER` row a blocking class recorded in the
[scope application index](m0013-scope-application-index.md). All observations are
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

**Workspace result:** the checkpoint contract remains, while the tracked memory
ledger was retired after the original observation. The current
[`context-and-memory` policy](../../../../.agents/governance/context-and-memory.md)
owns the repository-versus-provider-memory boundary.
`contracts/agent-checkpoint.schema.json` still requires `synthetic`,
`atomicWrite` with the `same-directory-temp-fsync-replace` strategy, `redaction`
with the `[REDACTED-SYNTHETIC]` marker, `resume.repositoryStateWins` and its
conflict order, `compaction`, and `handoff`. Durable progress now belongs to the
owning Spec Task and Git evidence; no Stage 00 `memory/` directory or parallel
tracked progress ledger remains. `docs/03.specs/` continues to host
domain-scoped owners.

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

#### Historical Review and Freshness

Refresh after a memory/checkpoint contract, canonical owner, provider memory,
MCP Resource, retention/privacy, or lifecycle-validator change. Static PASS
does not prove provider-local memory, checkpoint use, authentication, or actual
compaction execution.

External sources were re-checked on 2026-08-10; no cited claim changed inside
that window. The re-check recorded that the pinned `2025-11-25` MCP revision is
superseded by `2026-07-28`, so treat every MCP statement here as revision-scoped
rather than current-protocol. None of the four sources publishes a last-modified
date, so an unchanged result is content identity rather than a publisher signal.

#### 2026-08-11 Partial/DEFER incremental refresh

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

**Current implementation:** the
[`context-and-memory` policy](../../../../.agents/governance/context-and-memory.md)
defines repository state and the owning Spec Task as current authority, while
provider-local memory and ignored checkpoints remain advisory.
`contracts/agent-checkpoint.schema.json` is the repository-static schema for an
ignored, advisory, atomic/redacted checkpoint with repository-wins recovery,
compaction, lifecycle, and handoff fields. The retired `memory/` directory is
recoverable from Git and is not a current owner.

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

#### 2026-08-14 consistency and Partial re-observation

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

#### 2026-08-20 full-corpus reverification

This increment re-observed the four memory rows at workspace baseline
`8d8c8e5634fe939f8daaf041fbf5dfb444ed4a9c`. The allocation slice assigns no
new source or claim ID. Provider-local memory and MCP resources remain
auxiliary evidence and never replace a canonical repository owner.

#### REQ-WERPC-029 short-term memory and checkpoint re-observation

- **Sources and external result:** `unchanged`; `SRC-WERPC-068`,
  `SRC-WERPC-050`, and `SRC-WERPC-051` were re-observed on 2026-08-20 as
  public provider-memory and SDK-session context only.
- **Workspace selector and result:** `confirmed` at
  `m0011-agent-memory-tiers-and-management.md#short-term-memory-baseline`. The
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
  `m0011-agent-memory-tiers-and-management.md#long-term-memory-baseline`. The durable
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
  `m0011-agent-memory-tiers-and-management.md#domain-scoped-memory-baseline`. Specs,
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
  `m0011-agent-memory-tiers-and-management.md#memory-management-baseline`. The four
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

#### 2026-08-23 provider-memory gap increment

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

#### 2026-09-05 external-source reverification

This increment re-observed the four memory owners under the approved 2026-09-05
follow-on cycle. Workspace re-observation was excluded by direct user decision.
New sources are `SRC-WERPC-125` and `SRC-WERPC-138`; the cycle claim is
`CLM-WERPC-016-09`.

#### REQ-WERPC-029, REQ-WERPC-030, REQ-WERPC-031, REQ-WERPC-032 memory re-observation

- **Sources and external result:** `changed` by evidence depth, not by
  contradiction. The first provider's memory reference was re-observed on
  2026-09-05 and registered as
  [SRC-WERPC-138](m0012-source-coverage.md#2026-09-05-external-source-reverification).
  It now documents an automatic-memory note taxonomy, an index file with a
  stated line and byte loading bound, an instruction-file size cap above which a
  file is skipped entirely, ancestor-exclusion settings for nested projects, and
  a separate memory directory for subagents. The corpus previously described
  this page only as documenting provider-local automatic memory. A vendor
  context-engineering publication naming compaction, structured note-taking, and
  sub-agent summarisation was registered as
  [SRC-WERPC-125](m0012-source-coverage.md#2026-09-05-external-source-reverification).
  The second provider's memory surface was re-observed as `unchanged` and
  remains off by default, with its own documentation directing required team
  guidance to checked-in instruction files rather than to recalled memory.
- **Workspace selector and result:** `not observed in this cycle`. The
  short-term, long-term, domain-scoped, and memory-management baselines retain
  their earlier repository-static observation dates.
- **As-Is, gap, and target:** no status changes. The three tier rows stay
  `Verified` for their local contracts and the management row stays `Partial`.
  The external record is now detailed enough to state precisely what a
  provider-local memory does and does not guarantee, which sharpens rather than
  moves the existing boundary between provider-local recall and the local
  durable-memory contract.
- **Evidence boundary:** blocking class and retained boundary remain
  `provider-runtime` / `DEFER`. Documented note classes and loading bounds do
  not prove enablement, generation, retention, deletion, secure erasure, or
  redaction in this environment.
- **Owner, safe follow-up, and trigger:** owner is this reference and the Stage
  00 memory contracts. The safe follow-up is to keep provider-local recall
  outside the durable-memory authority and to re-state, without changing policy,
  which documented bound corresponds to which local tier. Refresh when memory
  classes, storage locations, loading bounds, or default enablement change.

## Sources

Current [source observations](m0012-source-coverage.md#current-source-observations) own exact URLs/claim support for SRC-WERPC-004, 049, 050, 066, 068, 087, 096, 123, 125 and 137. Direct external reads: 2026-09-27. MCP current revision is externally confirmed as 2026-07-28; this says nothing about a connected client. Anthropic context-engineering article is published 2025-09-29; long-running harness 2025-11-26. Other read pages exposed no publication/modification date. Product storage/default/eligibility controls are not a local privacy, retention or secure-erasure guarantee.

### Historical source provenance

- [OpenAI Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) and [OpenAI Agents SDK sessions](https://openai.github.io/openai-agents-python/sessions/), checked 2026-08-08, re-checked 2026-08-10 (`SRC-WERPC-049`–`050`).
- [Anthropic Claude Code memory](https://code.claude.com/docs/en/memory), checked 2026-08-08, re-checked 2026-08-10 (`SRC-WERPC-051`).
- [Model Context Protocol Resources specification](https://modelcontextprotocol.io/specification/2025-11-25/server/resources), checked 2026-08-08, re-checked 2026-08-10 and confirmed superseded (`SRC-WERPC-052`).
- [Model Context Protocol versioning](https://modelcontextprotocol.io/specification/versioning) and the [2026-07-28 Resources specification](https://modelcontextprotocol.io/specification/2026-07-28/server/resources), checked 2026-08-10 (`SRC-WERPC-066`).
- [Context and memory policy](../../../../.agents/governance/context-and-memory.md) and `contracts/agent-checkpoint.schema.json` are local static owners.

## Review and Freshness

Refresh on provider memory defaults, storage/loading limits, SDK session/compaction recovery, MCP Resources/version/access/cache, instruction import or canonical memory/correction/deletion contracts. Reverify expired and retracted sources before promotion. Future tests need exact product/backend and authorized synthetic data, separate evidence for each retrieval stage and a responsible retention/access owner; this cycle neither reads private stores nor advances historical lifecycle observations.

## Related Documents

- [Pack coverage matrix](m0012-source-coverage.md#requirement-coverage-matrix)
- [Source ledger](m0012-source-coverage.md)
- [Context and memory policy](../../../../.agents/governance/context-and-memory.md)
