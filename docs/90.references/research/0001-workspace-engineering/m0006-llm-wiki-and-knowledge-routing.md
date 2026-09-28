---
title: "Reference: LLM-WIKI and Knowledge Routing"
version: "1.1.0"
type: "reference/research"
status: "published"
owner: "platform"
updated: "2026-09-27"
layer: "references"
artifact_id: "RES-0001-m0006"
---

# Reference: LLM-WIKI and Knowledge Routing

## Overview

This reference distinguishes external LLM-maintained wiki patterns, website export proposals, MCP resources and search/RAG from the retired local generated owner map.

Current external analysis is based on primary-source bodies checked on 2026-09-27. Conditional design recommendations are explicitly separate from product facts. Every workspace result is `not observed in this cycle`; candidate file paths are selectors, not findings. Historical observations below keep their dates, identifiers, corrections and original anchors.

### Historical overview and observation boundary

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

External primary-source research and conditional follow-up investigation design. It is not a local implementation assessment, installation, policy change, release approval or evidence of provider/hosted/live behavior.

### Historical reference classification

Source-backed routing and freshness analysis. It neither publishes a web file
nor operates an MCP server, search system, RAG pipeline, or provider runtime.

## Authority Boundary

This member establishes bounded external source findings and conditional investigation design. Local profiles, registries, policies and provider notes remain their respective owners; they were read only for this authoring contract. No current implementation audit, adoption decision, provider experiment or live operation is performed. The inherited local statements below retain their historical meaning and are not renewed by current source checks.

### Historical authority statement

Canonical documents own their facts, policy, lifecycle, and evidence. At the
observation date, the retired LLM-WIKI README declared the link-map boundary,
its generator owned deterministic output, and the index was generated output
only. This reference must not be used to infer current implementation, model
ingestion, retrieval quality, access control, or external exposure.

## Scope

Current scope includes external LLM-maintained wiki patterns, llms.txt, MCP Resources, search and RAG (U22).

### Historical scope

It covers REQ-WERPC-021: generated owner routing, schema/generator/drift and
freshness rules, and the boundary from llms.txt, MCP Resources, search, and RAG.

## Definitions / Facts

### Current external analysis

#### Distinct knowledge surfaces

`CLM-WERPC-017-71`–`75` distinguish five external patterns from the historical local map. Karpathy's LLM Wiki gist is an original-author proposal, not a standard or a benchmark (`SRC-WERPC-190`). Its recorded creation timestamp is 2026-04-04 16:25; a fresh immutable revision SHA was not obtained. The historical retired local generated link map below remains a different implementation with its original retirement dates. No wiki, generator or gate is restored here.

| Surface | Components, purpose and implementation choice | Limits and exclusion |
| --- | --- | --- |
| LLM-maintained wiki | Original sources plus derived synthesis, authoring schema, index/cross-links and change log; model-assisted maintenance | Synthesized prose is not source truth; original author's experience around 100 sources is anecdotal, not measured scale/performance |
| `llms.txt` | Community v2 docs-export proposal for root/subpath Markdown guidance; most specific path applies; H1 required and other structures optional (`SRC-WERPC-021`) | Does not imply a maintained wiki, retrieval engine, publication or consumer behavior |
| MCP Resources | Revision 2026-07-28 URI-addressed application-driven server data: list/read, capability negotiation, pagination, optional subscription and cache semantics (`SRC-WERPC-087`) | Resource contract does not prove server authorization, publication, client use or runtime enforcement |
| Search | Keyword/metadata matching with index/update/access ownership | Finds candidates rather than settling provenance or authority; start here when exact names/IDs answer the task |
| RAG | Parametric generation combined with nonparametric retrieval (`SRC-WERPC-213`) | Original research abstract was read; benchmarks/full paper were not verified and no local quality claim follows |

For a small stable corpus, direct links and lexical search may suffice. A derived wiki can explain relationships but adds review/change propagation. RAG can retrieve selected evidence for a question but adds corpus/chunk/access/evaluation complexity. MCP is an interface that may expose data from these systems, not an alternative guarantee of their content quality. qmd functionality/performance was not verified and is not adopted as evidence.

#### Wiki ingest query and lint

`CLM-WERPC-017-72` describes the author's ingest/query/lint pattern. Ingest reads source material and updates derived synthesis/cross-links; query answers using the corpus and may produce a reviewed reusable synthesis; lint checks missing links, inconsistencies and maintenance issues. The raw source, synthesis, schema, index and log have different responsibilities. Implementation needs stable source/claim identity, provenance selectors, explicit uncertainty and review ownership; an index must not become a second policy owner.

Conditional management proposal (`CLM-WERPC-017-77`): retain original evidence with its observation date; record claims and supporting/contradicting sources; separate a changed source from a changed conclusion; send unresolved contradictions to a responsible reviewer. A correction should identify the superseded claim. Source edits/deletion/access withdrawal must invalidate dependent summaries, search entries, chunks and caches as applicable. Preservation for audit and removal from active retrieval are different requirements and need an explicit retention/access decision. No license for the gist was confirmed, so content-copy permission is not inferred.

#### Retrieval risk and maintenance

`CLM-WERPC-017-76` uses OWASP LLM01 guidance (`SRC-WERPC-214`) on direct/indirect prompt injection. Extending it to persistent wiki poisoning is explicitly a research inference: ingesting hostile source instructions into durable synthesis can propagate them into future context. Treat fetched text as data, constrain tools/external writes independently, preserve provenance and review substantive changes. Retrieved content never grants authority.

Sensitive-data and copyright review must happen before ingestion/export, with access filtering applied to queries as well as storage. Review summaries and logs for leakage; embeddings/caches and derived answers can preserve content after the original is removed. Staleness, fabricated citations, unresolved contradictions and deleted sources demand change propagation rather than a cosmetic new review date. Verify provenance and deletion with a known changed/withdrawn source; evaluate search/retrieval with representative questions, relevance, citation correctness, access isolation and stale-source exclusion. Generated answers are hypotheses until checked against evidence. Exclude unapproved sensitive corpora and retrieval systems whose permission/deletion contract cannot be demonstrated.

Follow-up questions `Q-WERPC-081`–`087` cover surface identity, source/derived separation, ingest/query/lint and contradiction handling, llms publication/consumer evidence, MCP capability/authorization, scale-driven search/RAG selection and withdrawal/access propagation. Candidate selectors include source manifests, synthesis metadata, index configurations, `llms.txt`, MCP capability schemas and retrieval evaluation records. They are literals and no runtime check is performed. Full contracts are in the [follow-up ledger](m0013-scope-application-index.md#follow-up-question-ledger); every workspace result is `not observed in this cycle`.

### Historical analysis and dated observations

The following retained sections are historical evidence, including their dated local findings. They do not describe a current workspace observation.

#### LLM-WIKI baseline

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

#### Historical owner, drift, and freshness rules

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

#### Implementation proposal boundary

The generator/readme/check contract described here was later retired. A future
proposal may add a structured owner manifest only if it preserves one owner per
domain, validates missing/duplicate targets, has deterministic ordering,
updates the generated metadata, and supplies stale-output and broken-link tests.
It must remain a repository-navigation change until a separate authority
approves web publication, MCP Resources, search, or RAG.

#### 2026-08-17 full-corpus refresh

This increment is the fifth refresh cycle over this pack, executed under
Spec 058. Unlike the three preceding cycles it re-observed every owner row in
the pack rather than the twelve `Partial` rows, and it assigns each retained
`Partial` or `DEFER` row a blocking class recorded in the
[scope application index](m0013-scope-application-index.md). All observations are
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

### Current primary sources

- `SRC-WERPC-190`: [Karpathy LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), checked 2026-09-27; body lines 62–117 excluding comments, creation 2026-04-04 16:25, fresh immutable revision unavailable after API 502; license unconfirmed.
- `SRC-WERPC-021`: [llms.txt](https://llmstxt.org/), v2 proposal checked 2026-09-27; published 2024-09-03, modified 2026-08-10; Proposal/Format sections, not a formal standards-body specification.
- `SRC-WERPC-087`: [MCP Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources), revision 2026-07-28 checked 2026-09-27; User Interaction Model, Capabilities and Protocol Messages, not runtime evidence.
- `SRC-WERPC-213`: [Lewis et al. RAG paper](https://arxiv.org/abs/2005.11401), 2020, abstract/submission history checked 2026-09-27; full paper and benchmark results not verified.
- `SRC-WERPC-214`: [OWASP LLM01:2025](https://genai.owasp.org/llmrisk/llm01-prompt-injection/), Indirect/Prevention guidance checked 2026-09-27; persistent-wiki poisoning is a labeled inference.

The [current source observations](m0012-source-coverage.md#current-source-observations) own full claim/refresh metadata. The retired local surface's dates remain historical.

### Historical sources

- [llms.txt proposal](https://llmstxt.org/), checked 2026-08-08: website-root Markdown proposal and its intentionally unspecified application processing boundary.
- [MCP server primitives](https://modelcontextprotocol.io/specification/2025-06-18/server/index) and [MCP Resources](https://modelcontextprotocol.io/specification/2024-11-05/server/resources), checked 2026-08-08: server-exposed URI resources and capability/incorporation boundary.
- Workspace observation, 2026-08-08: LLM-WIKI README, generated index, curation guide, generator, and scripts inventory. No MCP server, llms.txt publication, search index, RAG corpus, or retrieval-quality test was evaluated.

## Review and Freshness

### Current review boundary

Recheck when cited methods, product plans/schemas, source revisions, permission/export behavior or an actual adoption proposal changes. Current external claims, source refresh outcomes, workspace observations and document QA are independent axes. Historical statuses are not promoted by a new external check. Document QA results belong to the owning Task; this member claims no provider-runtime or live evidence.

### Historical refresh record

Refresh when the generator, declared inputs, canonical owner paths, taxonomy,
stage routing, script inventory, GitOps/examples/version ownership, or generated
output changes; recheck the external proposal/spec when a web/MCP/retrieval
design is proposed. Run the generator check after every owner-map change.

#### 2026-08-20 full-corpus reverification

This increment consumes the reviewed `REQ-WERPC-021` row and its empty
source/claim allocation slice. It preserves the distinction among canonical
source ownership, deterministic routing output, publication, ingestion,
retrieval, and provider runtime.

#### REQ-WERPC-021 LLM-WIKI routing and retrieval boundary

- **Sources and result:** `unchanged` / `confirmed`, using existing
  `SRC-WERPC-021`, `SRC-WERPC-086`, and `SRC-WERPC-087` boundaries and selector
  `m0006-llm-wiki-and-knowledge-routing.md#llm-wiki-baseline`. `llms.txt` remains a
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

#### 2026-09-05 external-source reverification

This increment re-observed the knowledge-routing owner under the approved
2026-09-05 follow-on cycle. Workspace re-observation was excluded by direct user
decision. The new source is `SRC-WERPC-142`; the cycle claim is
`CLM-WERPC-016-12`.

#### REQ-WERPC-021 LLM-WIKI and knowledge-routing re-observation

- **Sources and external result:** `unchanged`. The community index proposal
  remains an informally governed proposal at the version and modification date
  already recorded, notwithstanding broader adoption. The protocol specification
  was read directly on 2026-09-05 rather than through a search summary: the
  revision recorded here is still the current revision, and its resource
  semantics, including result typing, pagination, caching, subscription, and
  multi-round-trip behaviour, are unchanged. The working draft adds an
  extensions framework but carries no dated revision that would supersede the
  current one. The observation is registered as
  [SRC-WERPC-142](m0012-source-coverage.md#2026-09-05-external-source-reverification).
- **Workspace selector and result:** `not observed in this cycle`. The
  historical baseline in this reference retains its earlier observation date and
  its recorded status.
- **As-Is, gap, and target:** the row keeps its `Contradicted` disposition,
  which records that the prior deterministic canonical-owner map did not hold.
  Nothing observed in this cycle revives or replaces that map, and no new
  routing owner is created.
- **Evidence boundary:** blocking class and retained boundary remain
  `runtime-retrieval` / `DEFER`. A specification read proves the protocol
  contract only: no server, session, negotiation, retrieval, authorisation, or
  retrieval-quality claim follows from it, and the index proposal proves no
  publication or consumer behaviour.
- **Owner, safe follow-up, and trigger:** owner is this reference and the Stage
  00 knowledge-routing owners. Refresh when a dated revision supersedes the
  current one, when resource semantics change, or if a knowledge server is ever
  proposed under a separate authorisation.

## Related Documents

- [Documentation architecture and Diátaxis](m0005-documentation-architecture-and-diataxis.md)
- [Source coverage and migration ledger](m0012-source-coverage.md)
