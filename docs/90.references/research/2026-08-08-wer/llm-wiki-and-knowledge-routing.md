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

| Surface       | What it is                                                                                                        | What it is not                                                                                         | Evidence boundary                                                                                           |
| ------------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| LLM-WIKI      | Generated local Markdown pointers to canonical repository owners, with a deterministic drift check.               | A policy, a duplicated wiki, a search engine, semantic index, RAG corpus, or runtime context provider. | Generator and `--check` establish output freshness against declared static inputs only.                     |
| `llms.txt`    | A proposal for a Markdown file at a website root that helps an LLM use that website.                              | A local repository index specification or proof any LLM fetches/uses it.                               | No workspace publication or consumer is observed; a separate web/publication review would be required.      |
| MCP Resources | URI-addressed data exposed by an MCP server through the Resources capability; hosts/clients decide incorporation. | A Markdown index, a local file merely because it has links, or proof of an MCP server/client session.  | Requires a separately configured server, capability negotiation, access policy, and runtime evidence.       |
| Search        | Keyword/metadata lookup over an indexed corpus.                                                                   | A canonical-authority decision or source-freshness guarantee.                                          | Requires index ownership, update policy, access and quality evaluation.                                     |
| RAG           | Retrieval plus model-context assembly over selected content.                                                      | A deterministic owner map or proof retrieved content is current/correct.                               | Requires corpus boundaries, ingestion/deletion, permissions, provenance, evaluation, and incident handling. |

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
   version-inventory path change triggers review and check. As checked on
   2026-08-10, the generated file's `updated`, `Source checked`, and
   `Last reviewed` values are all 2026-08-09, so the freshness debt recorded at
   the 2026-08-08 observation is closed. A current review date remains evidence
   of declared-input review only; it is not evidence of current external
   knowledge.
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

### 2026-08-17 full-corpus refresh

This increment is the fifth refresh cycle over this pack, executed under
Spec 058. Unlike the three preceding cycles it re-observed every owner row in
the pack rather than the twelve `Partial` rows, and it assigns each retained
`Partial` or `DEFER` row a blocking class recorded in the
[scope application index](scope-application-index.md). All observations are
dated **2026-08-17**. No live cluster, hosted CI run, provider runtime,
authenticated execution, or secret value was observed.

#### REQ-WERPC-021 re-observation

**External result:** `changed` on two distinct axes (`SRC-WERPC-086`,
`SRC-WERPC-087`).

First, the `llms.txt` proposal is now at **v2**, last modified 2026-08-10, inside
this refresh window. It is still explicitly a community proposal rather than an
official standards-body specification, so this report's core boundary claim
holds; the version it cites, however, has moved.

Second, the Model Context Protocol published revision **2026-07-28** as the
current specification, which supersedes the `2025-06-18` Resources path this
report cites. The core boundary claim — URI-addressed data, application-driven
incorporation, hosts and clients deciding — is unchanged, but the cited version
and URL are stale. Under revision `2026-07-28` the Resources capability gained
`resultType`, pagination, caching through `ttlMs` and `cacheScope`, a
`subscriptions/listen` mechanism replacing simple `subscribe`, and a
multi-round-trip `InputRequiredResult`.

**Workspace result:** `confirmed`. `docs/90.references/llm-wiki/README.md:22-30`
still declares the generator, README, `wiki-index.md`, and `--check` contract
unchanged. `wiki-index.md` frontmatter still records `updated: 2026-08-09` with
matching source-checked and last-reviewed dates, and
`scripts/generate-llm-wiki-index.sh` remains the sole generator.

**Status effect:** `no-change` (`CLM-WERPC-011-21`). `REQ-WERPC-021` keeps
`Verified` on the deterministic canonical-owner map, with publication, MCP,
search, RAG, and retrieval `DEFER`. The two external version facts are new
evidence about cited sources; neither changes the local link map, the generator,
or the boundary.

**Blocking class:** `repo-static`, reachable — with a bounded limitation. The
drift check `bash scripts/generate-llm-wiki-index.sh --check` was **not executed
this cycle**, because the package that owned this row ran without a shell tool.
Index freshness is therefore inferred from unchanged frontmatter dates and is
explicitly not proven by running the check. Reopens when the generator or its
declared inputs change, when `wiki-index.md` frontmatter dates change, when
`--check` is run and reports byte drift, or when `llms.txt` is adopted by a
formal standards body.

#### Supersession note with pack-wide reach

The revision jump to `2026-07-28` is broader than the Resources capability cited
here, spanning a stateless protocol core, multi-round-trip requests, header-based
routing, cacheable list results, authorization hardening, an extensions
framework, and a feature-lifecycle policy. Any other owner in this pack still
citing `2025-06-18` for tools, prompts, or authorization needs the same
supersession note. That correction is not applied here, because each owner row
owns its own citations.

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
