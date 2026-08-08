---
title: 'Reference: LLM-WIKI and Knowledge Routing'
type: content/reference
status: active
owner: platform
updated: 2026-08-08
---

# Reference: LLM-WIKI and Knowledge Routing

## Overview

LLM-WIKI is a repository-local, generated canonical-owner link map. It makes
the correct document easier to find; it is neither a knowledge store nor a
retrieval system and cannot make its targets authoritative, fresh, or safe.

## Reference Type

Source-backed routing and freshness analysis. It neither publishes a web file
nor operates an MCP server, search system, RAG pipeline, or provider runtime.

## Authority Boundary

Canonical documents own their facts, policy, lifecycle, and evidence.
`docs/90.references/llm-wiki/README.md` declares the link-map boundary;
`scripts/generate-llm-wiki-index.sh` owns deterministic output generation; and
`wiki-index.md` is generated output only. This reference must not be used to
infer model ingestion, retrieval quality, access control, or external exposure.

## Scope

It covers REQ-WERPC-021: generated owner routing, schema/generator/drift and
freshness rules, and the boundary from llms.txt, MCP Resources, search, and RAG.

## Definitions / Facts

### LLM-WIKI baseline

The current generator emits a fixed Markdown canonical-owner map to
`docs/90.references/llm-wiki/wiki-index.md`; `--check` compares that output to
the tracked file. Its README declares the current inputs and prohibits copied
policy/procedure content, vector data, embeddings, runtime configuration, and
static-site output. This is a deterministic **link-map contract**, not a
document-discovery experiment.

| Surface | What it is | What it is not | Evidence boundary |
| --- | --- | --- | --- |
| LLM-WIKI | Generated local Markdown pointers to canonical repository owners, with a deterministic drift check. | A policy, a duplicated wiki, a search engine, semantic index, RAG corpus, or runtime context provider. | Generator and `--check` establish output freshness against declared static inputs only. |
| `llms.txt` | A proposal for a Markdown file at a website root that helps an LLM use that website. | A local repository index specification or proof any LLM fetches/uses it. | No workspace publication or consumer is observed; a separate web/publication review would be required. |
| MCP Resources | URI-addressed data exposed by an MCP server through the Resources capability; hosts/clients decide incorporation. | A Markdown index, a local file merely because it has links, or proof of an MCP server/client session. | Requires a separately configured server, capability negotiation, access policy, and runtime evidence. |
| Search | Keyword/metadata lookup over an indexed corpus. | A canonical-authority decision or source-freshness guarantee. | Requires index ownership, update policy, access and quality evaluation. |
| RAG | Retrieval plus model-context assembly over selected content. | A deterministic owner map or proof retrieved content is current/correct. | Requires corpus boundaries, ingestion/deletion, permissions, provenance, evaluation, and incident handling. |

### Owner, drift, and freshness rules

1. **Canonical-owner-first.** Each index entry is a pointer to the owner that
   controls the claim. The index must not copy mutable policy, procedure,
   secrets, credentials, operational commands, or release approval.
2. **Generator-only output.** Change declared owner links or the generator,
   then regenerate. Do not hand-edit `wiki-index.md`; run
   `bash scripts/generate-llm-wiki-index.sh --check` to detect byte drift.
3. **Schema and input rule.** The generator's fixed table is its present
   generation schema; the README's declared inputs and relative links are the
   current input contract. A profile/schema change does not automatically
   discover a new owner. Any discovery-based generator needs an approved schema,
   collision/absence behavior, fixture tests, and migration plan first.
4. **Freshness rule.** A source-owner path, documentation taxonomy, governance
   routing, scripts inventory, GitOps owner, examples taxonomy, generator, or
   version-inventory path change triggers review and check. The generated file's
   own `updated`/last-reviewed date remains 2026-05-10; that is a visible
   freshness debt, not evidence of current external knowledge.
5. **Security rule.** An owner map is intentionally reference-only. Do not add
   secrets, ignored configuration, embeddings, runtime cache, package manifest,
   or copied runbook text. Any future retrieval endpoint requires separately
   designed authorization, data classification, retention/deletion, provenance,
   audit, and incident boundaries.

### Implementation proposal boundary

The smallest safe improvement is to retain the current generator/readme/check
contract and review its static owners when a declared trigger occurs. A future
proposal may add a structured owner manifest only if it preserves one owner per
domain, validates missing/duplicate targets, has deterministic ordering,
updates the generated metadata, and supplies stale-output and broken-link tests.
It must remain a repository-navigation change until a separate authority
approves web publication, MCP Resources, search, or RAG.

## Sources

- [llms.txt proposal](https://llmstxt.org/), checked 2026-08-08: website-root Markdown proposal and its intentionally unspecified application processing boundary.
- [MCP server primitives](https://modelcontextprotocol.io/specification/2025-06-18/server/index) and [MCP Resources](https://modelcontextprotocol.io/specification/2024-11-05/server/resources), checked 2026-08-08: server-exposed URI resources and capability/incorporation boundary.
- Workspace observation, 2026-08-08: LLM-WIKI README, generated index, curation guide, generator, and scripts inventory. No MCP server, llms.txt publication, search index, RAG corpus, or retrieval-quality test was evaluated.

## Review and Freshness

Refresh when the generator, declared inputs, canonical owner paths, taxonomy,
stage routing, script inventory, GitOps/examples/version ownership, or generated
output changes; recheck the external proposal/spec when a web/MCP/retrieval
design is proposed. Run the generator check after every owner-map change.

## Related Documents

- [LLM-WIKI README](../../llm-wiki/README.md)
- [Generated LLM-WIKI index](../../llm-wiki/wiki-index.md)
- [LLM-WIKI curation guide](../../../05.operations/guides/0009-llm-wiki-curation-guide.md)
- [Documentation architecture and Diátaxis](documentation-architecture-and-diataxis.md)
- [Source coverage and migration ledger](source-coverage-and-migration-ledger.md)
