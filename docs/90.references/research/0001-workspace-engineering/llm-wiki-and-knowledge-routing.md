---
title: 'Reference: LLM-WIKI and Knowledge Routing'
type: content/reference
status: active
owner: platform
updated: 2026-08-31
---

# Reference: LLM-WIKI and Knowledge Routing

## Overview

At the recorded observation dates, LLM-WIKI was a repository-local generated
canonical-owner link map. It made the correct document easier to find; it was
neither a knowledge store nor a retrieval system and could not make its targets
authoritative, fresh, or safe.

> **Current implementation disposition (2026-08-31):** the local generated
> LLM-WIKI README, index, generator, dedicated guide, and freshness gate were
> retired as a duplicate navigation control plane. The external-source analysis
> and observation-dated workspace evidence below are preserved as research;
> they no longer describe a maintained current surface.

## Reference Type

Source-backed routing and freshness analysis. It neither publishes a web file
nor operates an MCP server, search system, RAG pipeline, or provider runtime.

## Authority Boundary

Canonical documents own their facts, policy, lifecycle, and evidence. At the
observation date, the retired LLM-WIKI README declared the link-map boundary,
its generator owned deterministic output, and the index was generated output
only. This reference must not be used to infer current implementation, model
ingestion, retrieval quality, access control, or external exposure.

## Scope

It covers REQ-WERPC-021: generated owner routing, schema/generator/drift and
freshness rules, and the boundary from llms.txt, MCP Resources, search, and RAG.

## Definitions / Facts

### LLM-WIKI baseline

At the observation date, the now-retired generator emitted a fixed Markdown
canonical-owner map to the then-tracked `docs/90.references/llm-wiki/wiki-index.md`
and its `--check` mode compared generated output with that index. The retired
README declared its inputs and prohibited copied
policy/procedure content, vector data, embeddings, runtime configuration, and
static-site output. This was a deterministic **link-map contract**, not a
document-discovery experiment; Git history preserves the former implementation.

| Surface       | What it is                                                                                                        | What it is not                                                                                         | Evidence boundary                                                                                           |
| ------------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| LLM-WIKI      | Historical generated Markdown pointers to canonical repository owners; the local generator and output are retired. | A current policy, active index, search engine, semantic index, RAG corpus, or runtime context provider. | Historical drift evidence proved only the declared static inputs observed at that time.                     |
| `llms.txt`    | A proposal for a Markdown file at a website root that helps an LLM use that website.                              | A local repository index specification or proof any LLM fetches/uses it.                               | No workspace publication or consumer is observed; a separate web/publication review would be required.      |
| MCP Resources | URI-addressed data exposed by an MCP server through the Resources capability; hosts/clients decide incorporation. | A Markdown index, a local file merely because it has links, or proof of an MCP server/client session.  | Requires a separately configured server, capability negotiation, access policy, and runtime evidence.       |
| Search        | Keyword/metadata lookup over an indexed corpus.                                                                   | A canonical-authority decision or source-freshness guarantee.                                          | Requires index ownership, update policy, access and quality evaluation.                                     |
| RAG           | Retrieval plus model-context assembly over selected content.                                                      | A deterministic owner map or proof retrieved content is current/correct.                               | Requires corpus boundaries, ingestion/deletion, permissions, provenance, evaluation, and incident handling. |

### Historical owner, drift, and freshness rules

1. **Canonical-owner-first.** Each index entry is a pointer to the owner that
   controls the claim. The index must not copy mutable policy, procedure,
   secrets, credentials, operational commands, or release approval.
2. **Generator-only output.** While the surface existed, declared owner links
   or the generator changed first and a fixed generated-index check detected
   byte drift. The generator and output are now retired and must not be
   recreated as a parallel current index.
3. **Schema and input rule.** At the observation date, the generator's fixed
   table was its generation schema and the README's declared inputs and relative
   links formed its input contract. Those local surfaces are now retired. Any
   future discovery-based generator needs an approved schema,
   collision/absence behavior, fixture tests, and migration plan first.
4. **Freshness rule.** While the surface existed, a source-owner path,
   documentation taxonomy, governance routing, scripts inventory, GitOps owner,
   examples taxonomy, generator, or version-inventory path change triggered
   review and check. As checked on
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

The generator/readme/check contract described here was later retired. A future
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

**Workspace result at the time:** `confirmed`. The then-current LLM-WIKI README
declared one generator, README, generated index, and fixed check contract.
The generated index frontmatter recorded `updated: 2026-08-09` with matching
source-checked and last-reviewed dates. The entire local LLM-WIKI surface was
later retired; Git history preserves that historical implementation evidence.

**Status effect at the observation date:** `no-change`
(`CLM-WERPC-011-21`). `REQ-WERPC-021` remained `Verified` on the then-current
deterministic canonical-owner map, with publication, MCP, search, RAG, and
retrieval `DEFER`. The two external version facts were new evidence about cited
sources and did not change that cycle's local boundary.

**Current local disposition (2026-09-01):** `Contradicted`. The generated owner
map and generator were intentionally retired, so the earlier local
implementation result is no longer current. The external llms.txt, MCP,
search, and RAG comparison remains preserved as descriptive research.

**Blocking class:** `repo-static`, reachable — with a bounded limitation. The
then-current generated-index drift check was **not executed this cycle**,
because the package that owned this row ran without a shell tool.
Index freshness is therefore inferred from unchanged frontmatter dates and is
explicitly not proven by running the check. That local generated-index trigger
closed when the surface was retired; the external research reopens if llms.txt
is adopted by a formal standards body or the cited MCP capability changes.

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

### 2026-08-20 full-corpus reverification

This increment consumes the reviewed `REQ-WERPC-021` row and its empty
source/claim allocation slice. It preserves the distinction among canonical
source ownership, deterministic routing output, publication, ingestion,
retrieval, and provider runtime.

#### REQ-WERPC-021 LLM-WIKI routing and retrieval boundary

- **Sources and result:** `unchanged` / `confirmed`, using existing
  `SRC-WERPC-021`, `SRC-WERPC-086`, and `SRC-WERPC-087` boundaries and selector
  `llm-wiki-and-knowledge-routing.md#llm-wiki-baseline`. `llms.txt` remains a
  community proposal, and MCP Resources remain URI-addressed server data whose
  incorporation is application-driven.
- **Observed As-Was:** LLM-WIKI was a deterministic Markdown canonical-owner
  link map. Its README owned declared inputs, the generator owned output, and
  its index was generated state. The research report did not run the generator;
  the recorded integration task ran the then-existing `--check` lane without
  changing the immutable baseline observation. That lane is now retired.
- **Gap / Target:** no web publication, llms.txt consumer, MCP server/session,
  capability negotiation, access policy, search index, RAG corpus, ingestion,
  deletion, retrieval, or retrieval-quality evaluation was observed. Retain
  canonical-owner-first routing and generator-only updates; design any future
  discovery, publication, or retrieval surface under a separate authority.
- **Evidence / rejected inference:** repository-static plus official/public
  specification evidence. A Markdown map, current proposal, MCP specification,
  or generator PASS cannot prove authority, source currency, publication,
  ingestion, retrieval, access control, or model use.
- **Disposition / retained boundary:** historical `Verified`; blocking class
  `repo-static`. No current generator check remains. Provider/runtime and
  hosted/user effects remain `DEFER`.
- **Owner / safe follow-up / trigger:** this preserved research pack and current
  canonical content owners. Reopen on a newly approved discovery surface,
  llms.txt status, or MCP Resources revision change; require a separately
  approved security and evaluation design before publication or retrieval.

## Related Documents

- [Documentation architecture and Diátaxis](documentation-architecture-and-diataxis.md)
- [Source coverage and migration ledger](source-coverage.md)
