---
title: 'Agent Memory Tiers and Management Reference'
type: content/reference
status: active
owner: platform
updated: 2026-08-07
---

# Agent Memory Tiers and Management Reference

## Overview

This reference records how agent memory is layered — long-term, short-term or
working, domain-scoped, and provider-local — and how it is managed. It records
provider instruction-file and memory mechanisms checked on 2026-08-07, a
cognitive-architecture grounding for the working, episodic, semantic, and
procedural distinction, and this repository's four-class memory contract with
the exact enforcement its validators apply.

The finding worth stating first is that this repository's memory contract is
materially stricter than any external source surveyed. External sources define
loading, precedence, and size budgets. None of them defines a total conflict
order, a review-gated promotion ceiling, a redaction requirement, an expiry
disposition, or a bounded feedback-routing destination set. This repository
defines all five. The corresponding limit is that every one of those controls is
enforced over a synthetic fixture; no validator reads the real provider-local
store or the ignored checkpoint.

This is descriptive Stage 90 reference material. It does not change a memory
class, an owner, a retention rule, or a validator.

### Purpose

- Record source-backed provider memory mechanisms and their stated limits.
- Record a citable cognitive grounding for the memory-type distinction.
- Record the repository's four classes exactly as declared, with owners.
- Record precisely what the checkpoint and lifecycle validators enforce.
- Separate what is enforced from what is advisory, and route each gap.

## Reference Type

- Type: durable-concept / external-standard-snapshot
- Source checked: `2026-08-07`
- Refresh trigger: a provider memory or instruction-file discovery change; a
  change to `docs/00.agent-governance/memory/README.md`,
  `docs/00.agent-governance/contracts/harness-contract.json`,
  `agent-checkpoint.schema.json`, or `agent-loop-lifecycle.json`; or a change to
  the checkpoint or loop-lifecycle validators.

## Authority Boundary

- **Authoritative for**:
  - Dated provider findings checked 2026-08-07 and their stated limits.
  - The repository's four-class declaration and owners as observed 2026-08-07.
  - The enforcement description of `scripts/validate-agent-checkpoint.py` and
    `scripts/validate-agent-loop-lifecycle.py` as read 2026-08-07.
- **Not authoritative for**:
  - The memory classes, their authority, retention, or conflict rules. Those
    belong to `docs/00.agent-governance/memory/README.md` and
    `docs/00.agent-governance/contracts/harness-contract.json`.
  - Any claim that a repository-static validator PASS proves provider
    discovery, hook delivery, permissions, model resolution, authenticated
    execution, hosted CI, remote, credential-bearing, live, or actual
    checkpoint execution. It proves none of these.
  - Mapping the four operational classes onto cognitive memory types as
    repository policy. That mapping is recorded here as inference.
  - Live cluster, provider runtime, hosted CI, or remote evidence.

## Scope

### In Scope

- Claude Code memory and compaction, the Claude API memory tool and context
  editing, AGENTS.md and Codex discovery, Gemini context files, MCP Resources
  and the memory reference server, and a cognitive-architecture source.
- The repository's four memory classes, owners, and lifecycle rules.
- Checkpoint and loop-lifecycle validator enforcement.
- Drift and staleness assessment, and gap routing.

### Out of Scope

- Changing any memory class, contract, template, or validator.
- Reading or writing `.agent-work/checkpoint.json` or any provider-local store.
- Reorganizing `docs/00.agent-governance/memory/progress.md`.
- Live, provider-runtime, hosted-CI, or remote verification.

## Definitions / Facts

### Cognitive Grounding

CoALA, _Cognitive Architectures for Language Agents_, arXiv:2309.02427, by
Sumers, Yao, Narasimhan, and Griffiths, checked 2026-08-07, describes "a
language agent with modular memory components, a structured action space to
interact with internal memory and external environments, and a generalized
decision-making process". Its memory definitions, quoted from the paper body:
working memory "maintains active and readily available information as symbolic
variables for the current decision cycle"; episodic memory "stores experience
from earlier decision cycles"; semantic memory "stores an agent's knowledge
about the world and itself"; and procedural memory exists in "two forms ...
implicit knowledge stored in the LLM weights, and explicit knowledge written in
the agent's code".

A second survey, arXiv:2404.13501, _A Survey on the Memory Mechanism of Large
Language Model based Agents_, is recorded here only by title and identifier. Its
body was not retrievable on 2026-08-07, so it is deliberately not cited for any
taxonomy claim.

### Provider Mechanisms

**Claude Code memory** (<https://code.claude.com/docs/en/memory>, checked
2026-08-07). Two mechanisms: CLAUDE.md files written by the user, and auto
memory written by Claude. Both "are loaded at the start of every conversation.
Claude treats them as context, not enforced configuration." Four scopes load
broadest to most specific — managed policy, user, project, local — and "All
discovered files are concatenated into context rather than overriding each
other." Imports use `@path`, resolve relative to the importing file, and are
recursive "with a maximum depth of four hops". Size guidance targets "under 200
lines per CLAUDE.md file". Auto memory lives at
`~/.claude/projects/<project>/memory/` with a `MEMORY.md` index; "The first 200
lines of `MEMORY.md`, or the first 25KB, whichever comes first, are loaded at
the start of every conversation", and the store "is machine-local". Subagents do
not inherit the main conversation's auto memory. The enforcement boundary is
explicit: "To block an action regardless of what Claude decides, use a PreToolUse
hook instead."

**Compaction** (<https://code.claude.com/docs/en/context-window>, checked
2026-08-07). Project-root CLAUDE.md, unscoped rules, and auto memory are
"Re-injected from disk". Nested CLAUDE.md files in subdirectories are "Lost
until a file in that subdirectory is read again", and path-scoped rules "load
into message history when their trigger file is read, so compaction summarizes
them away with everything else".

**Claude API memory tool**
(<https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool>,
checked 2026-08-07). It "operates client-side: Claude requests file operations,
and your application executes them." Its injected protocol includes "ASSUME
INTERRUPTION: Your context window might be reset at any moment, so you risk
losing any progress that is not recorded in your memory directory." Security is
the implementer's responsibility, including path-traversal protection, sensitive
data stripping, file-size caps, and expiry: "Periodically delete memory files
that haven't been accessed in a long time."

**Context editing**
(<https://platform.claude.com/docs/en/build-with-claude/context-editing>,
checked 2026-08-07). Applied server-side; "Your client application maintains the
full, unmodified conversation history." The stated rationale is that "context is
a finite resource with diminishing returns, and irrelevant content degrades
model focus." Clearing "Invalidates cached prompt prefixes".

**Compaction risk**
(<https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>,
checked 2026-08-07). "Overly aggressive compaction can result in the loss of
subtle but critical context whose importance only becomes apparent later." It
names "Structured note-taking, or agentic memory" as the mitigation, and
describes just-in-time loading as maintaining "lightweight identifiers" that are
resolved at runtime.

**AGENTS.md and Codex.** AGENTS.md (<https://agents.md/>, checked 2026-08-07)
states "The closest AGENTS.md to the edited file wins; explicit user chat
prompts override everything." Codex
(<https://learn.chatgpt.com/docs/agent-configuration/agents-md.md>, checked
2026-08-07) reads at most one file per directory, concatenates root-down so
closer files override by position, and bounds the total at
`project_doc_max_bytes`, "32 KiB by default".

**Gemini CLI** (<https://geminicli.com/docs/cli/gemini-md/>, checked
2026-08-07). Global context, then workspace context, then just-in-time scanning
when a tool accesses a file. `/memory show` displays the concatenated context
and `/memory reload` rescans. A secondary summary named the command
`/memory refresh`; only the fetched page is treated as authoritative and the
conflict is recorded.

**MCP** (<https://modelcontextprotocol.io/docs/concepts/resources>, spec
revision `2026-07-28`, checked 2026-08-07). Resources are application-driven and
carry `audience`, `priority`, and `lastModified` annotations. The memory
reference server
(<https://github.com/modelcontextprotocol/servers/tree/main/src/memory>, checked
2026-08-07) models a knowledge graph of entities, relations "always stored in
active voice", and observations that "Should be atomic (one fact per
observation)". It is a reference implementation, not a normative spec, and
defines no expiry, review, or authority model.

### The Repository's Four Classes

The readable owner is `docs/00.agent-governance/memory/README.md`; the
machine-readable owner is `harness-contract.json` under `memory.classes`.
Exactly four classes are managed, and `progress.md` is "the durable shared
progress view for `durable-long-term` memory, not a fifth memory class".

| Class                      | Authority mode                              | Canonical owner                                | Refresh basis            | Retention and expiry                                                     | Promotion target                                         | Conflict winner           |
| -------------------------- | ------------------------------------------- | ---------------------------------------------- | ------------------------ | ------------------------------------------------------------------------ | -------------------------------------------------------- | ------------------------- |
| `working-short-term`       | `temporary-context-only`, non-authoritative | active task executor                           | `task-resume`            | discard at task terminal                                                 | `durable-long-term`, reviewed and redacted               | observed repository state |
| `durable-long-term`        | `canonical-repository-record`               | canonical SDLC owner or shared progress ledger | `canonical-owner-review` | retain under canonical owner                                             | none; no implicit onward promotion                       | canonical document owner  |
| `domain-scoped`            | `canonical-domain-record`                   | canonical domain document owner                | `domain-owner-review`    | archive when superseded or invalidated                                   | `durable-long-term` when the lesson becomes cross-domain | canonical domain owner    |
| `provider-local-auxiliary` | `advisory-only`                             | provider runtime or user-local store           | `provider-reobservation` | garbage-collect under provider retention after repository re-observation | `working-short-term` only                                | observed repository state |

The contract's authority sub-flags for repository facts, decisions, task status,
and durable handoff evidence are false across the board for
`working-short-term` and `provider-local-auxiliary`, true across the board for
`durable-long-term`, and true except for task status for `domain-scoped`.

All four classes share one prohibited-content list: credential values, auth
files, tokens, secrets, raw prompts, full provider transcripts, shell history,
private diagnostics, environment dumps, and user configuration.

Two files exist under `docs/00.agent-governance/memory/`: the collection README,
which defers taxonomy authority to the harness contract, and `progress.md`, the
canonical durable shared ledger and the only tracked `progress.md`. Its
structure is newest-first dated entries under `## Work Entries`, followed by
`## Historical Entries`. Entries follow
`docs/99.templates/templates/common/progress.template.md`, which requires
Metadata with Date, Layer, Status, Tags, Owner, Canonical Owner, Provenance,
Sensitivity, Retention or Expiry, and Next Owner, then Progress, Memory,
Evidence, and Handoff.

### Validator Enforcement

`scripts/validate-agent-checkpoint.py` validates a closed synthetic checkpoint
without reading or writing one. Paths must be relative and free of `.` and `..`;
the root and every segment are opened with `O_NOFOLLOW` and re-verified by
device and inode to defeat symlink and time-of-check substitution; duplicate
JSON keys are rejected at every depth.

Atomic write must be exactly same-directory temp, fsync, replace, with partial
writes disallowed. Isolation digests must equal specified SHA-256 compositions
of the identity tuple. Freshness requires created, updated, and observed
timestamps in order with at most 24 hours between updated and observed.

Repository-wins resume is the strongest rule. The conflict order is fixed as
observed repository state, canonical SDLC or domain owner, reviewed durable
memory, working short-term, then provider-local auxiliary. Exactly one active
writer and one active resume are permitted. Terminal states may not be replayed.
Sixteen identity axes must each match observed repository identity, each with a
distinct error code.

Redaction requires a `PASS` status, at least one stored flag with every stored
flag false, and a synthetic marker consistent with the synthetic flag.
Independent scanners reject forbidden key names, key substrings, value
fragments, and secret-shaped regular expressions.

Compaction requires state `compacted`; raw prompt, full transcript, and provider
body retention all false; non-empty validation evidence; a remaining-work count
equal to the actual list length; non-empty source and replacement owners and
evidence; source and replacement digests that differ; and an approved review.

Handoff requires state `ready` with non-empty owner, next owner, result
summary, evidence references, and next action.

Per class, the validator enforces ordering and membership of the four classes,
authority mode, canonical owner, redaction, sensitivity, promotion target,
refresh basis with a 30-day maximum horizon and an observed revision equal to
head, expiry basis and disposition pairing, retention policy, archive or
garbage-collection fields, conflict status with `repositoryWins` true for all
four, and handoff. Provider-local promotion is specifically constrained to
`working-short-term` with repository re-observation and no direct canonical
write; attempting otherwise fails with a dedicated code.

`scripts/validate-agent-loop-lifecycle.py` enforces the checkpoint boundary,
including `actualProviderStateReadAllowed: false`, and the five bounded reviewed
feedback destinations in exact order: regression fixture, instruction
clarification, validator improvement, role evaluation case, and owned external
limitation. Its trigger is `repeated-stable-failure`, exactly one reviewed
destination may be selected, review is required, and promotion of raw traces,
prompts, or transcripts is disallowed.

Neither validator reads or writes `.agent-work/checkpoint.json`, and
`.gitignore` excludes `.agent-work/` entirely.

### Drift and Staleness Assessment

Four mechanisms keep provider-local memory non-authoritative: the declared
advisory-only authority mode with all four authority flags false; the promotion
ceiling at `working-short-term` gated on repository re-observation; the total
conflict order placing it last; and the preflight and postflight requirements to
treat it as advisory and to either discard it or review-promote it to a durable
owner.

The residual risk is that the advisory layer is unobserved. Every control is
enforced over a synthetic fixture. Nothing reads the real auto-memory store or
the ignored checkpoint, so a stale provider-local claim is caught by agent
discipline rather than by a gate. Claude's own documentation compounds this: auto
memory is re-injected from disk after compaction and loaded at the start of every
conversation, yet it is explicitly "context, not enforced configuration".

Three further risks are worth naming. `progress.md` is roughly 13,600 lines with
two heading conventions across its two sections, so full reads are impractical
and partial reads are the norm. Tracked memory documents carry only a manual
`updated:` frontmatter date, with no automated staleness gate; the 30-day
refresh horizon lives only inside the synthetic checkpoint contract. And
compaction loss is a documented provider behavior, while the repository's
PreCompact hook is advisory and does not block.

### Gap Routing

| ID     | Gap                                                                                                                                                                                                              | Owning path                                                                                                                                      |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| MEM-G1 | The memory collection README describes the four classes but never names the external primitives an agent actually meets — CLAUDE.md scopes, auto memory, AGENTS.md nearest-wins, Gemini hierarchy, MCP Resources | `docs/00.agent-governance/memory/README.md`, with the mapping belonging in Stage 90                                                              |
| MEM-G2 | No bridge exists between the four operational classes and the cognitive types, so a reader cannot tell whether `domain-scoped` is closer to semantic or procedural memory                                        | This reference; the mapping must stay labelled inference, not policy                                                                             |
| MEM-G3 | Provider-local memory has no observation, audit, or expiry procedure anywhere in the repository, despite being loaded into every session                                                                         | `docs/00.agent-governance/providers/claude.md`; currently `DEFER`, needing either a provider-runtime lane or an explicit accepted-risk statement |
| MEM-G4 | No tracked staleness gate exists for memory documents; the 30-day refresh rule lives only in the synthetic checkpoint contract                                                                                   | `scripts/validate-repo-quality-gates.sh` or `scripts/validate-links-and-owners.py`                                                               |
| MEM-G5 | `progress.md` has two heading conventions and no partitioning, index, or rotation policy owner at roughly 13,600 lines                                                                                           | `docs/00.agent-governance/memory/progress.md`                                                                                                    |
| MEM-G6 | The Gemini command name conflicts between the fetched page (`/memory reload`) and secondary summaries (`/memory refresh`)                                                                                        | `docs/00.agent-governance/providers/gemini.md`                                                                                                   |
| MEM-G7 | No repository document records that Claude Code reads `CLAUDE.md` and not `AGENTS.md`, although this repository maintains both plus `GEMINI.md` as separate shims                                                | `docs/00.agent-governance/providers/claude.md`                                                                                                   |
| MEM-G8 | Provider context budgets are unrecorded: Codex 32 KiB, Claude four-hop import depth and the 200-line target, and the 200-line or 25 KB auto-memory index cap                                                     | `docs/00.agent-governance/providers/claude.md`, `docs/00.agent-governance/providers/codex.md`                                                    |

## Sources

- <https://code.claude.com/docs/en/memory> checked 2026-08-07. Adopted: the two
  mechanisms, four scopes, concatenation model, import depth, size guidance,
  auto-memory location and load cap, machine-local scope, subagent isolation,
  and the context-not-configuration boundary. Rejected: any compliance
  guarantee.
- <https://code.claude.com/docs/en/context-window> checked 2026-08-07. Adopted:
  the survives-compaction table. Rejected: any fidelity guarantee for the
  summary.
- <https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool>
  checked 2026-08-07 (HTTP 302 from `docs.claude.com`). Adopted: the
  client-side model, the assume-interruption protocol, and the implementer
  security responsibilities including expiry. Rejected: any authority ranking
  against a repository source of truth; the page defines none.
- <https://platform.claude.com/docs/en/build-with-claude/context-editing>
  checked 2026-08-07. Adopted: the server-side clearing model and the
  cache-invalidation caveat.
- <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
  checked 2026-08-07. Adopted: the finite-resource framing, the
  aggressive-compaction risk, and structured note-taking. Noted: this is vendor
  engineering writing, not a specification.
- <https://agents.md/> and
  <https://learn.chatgpt.com/docs/agent-configuration/agents-md.md> checked
  2026-08-07. Adopted: nearest-file precedence, one file per directory,
  root-down concatenation, and the 32 KiB default budget.
- <https://geminicli.com/docs/cli/gemini-md/> checked 2026-08-07. Adopted: the
  three-stage loading sequence and the `/memory reload` command. Flagged: a
  naming conflict with secondary sources; publisher authority not verified from
  the page.
- <https://modelcontextprotocol.io/docs/concepts/resources> checked 2026-08-07,
  spec revision `2026-07-28`. Adopted: the application-driven framing and the
  annotation set.
- <https://github.com/modelcontextprotocol/servers/tree/main/src/memory> checked
  2026-08-07. Adopted: the entity, relation, and atomic-observation model.
  Rejected: any normative status; it is a reference implementation.
- <https://arxiv.org/abs/2309.02427> and its HTML rendering, checked
  2026-08-07. Adopted: the working, episodic, semantic, and procedural memory
  definitions.
- <https://arxiv.org/abs/2404.13501> checked 2026-08-07, title and identifier
  only. The body was not retrievable, so it is not cited for any taxonomy
  claim.
- Repository evidence read 2026-08-07:
  `docs/00.agent-governance/memory/README.md`,
  `docs/00.agent-governance/memory/progress.md`,
  `docs/00.agent-governance/contracts/harness-contract.json`,
  `agent-checkpoint.schema.json`, `agent-loop-lifecycle.json`,
  `docs/00.agent-governance/providers/claude.md`, the preflight, postflight,
  and quality-standards rules, the memory and progress templates,
  `scripts/validate-agent-checkpoint.py`,
  `scripts/validate-agent-loop-lifecycle.py`, and `.gitignore`.

## Review and Freshness

- Review on a provider memory or discovery change, a memory contract or
  validator change, or a change to the progress ledger structure.
- Provider documentation is current-only and is not backdated. Re-observe before
  promoting any dated claim.
- Every enforcement statement here describes validation over a synthetic
  fixture. It is repository-static evidence and proves nothing about provider
  discovery, hook delivery, permissions, model resolution, authenticated
  execution, hosted CI, remote, credential-bearing, live, or actual checkpoint
  execution.
- The cognitive mapping is inference and must not be promoted to policy without
  a canonical owner decision.

## Related Documents

- [Research Pack Index](README.md)
- [Harness and Loop Engineering](../research/2026-07-07-wer/harness-and-loop-engineering.md)
- [LLM Wiki and Agent Knowledge Routing](llm-wiki-and-knowledge-routing.md)
- [Provider Implementation Status](../research/2026-07-07-wer/provider-implementation-status.md)
- [Memory Collection](../../00.agent-governance/memory/README.md)
