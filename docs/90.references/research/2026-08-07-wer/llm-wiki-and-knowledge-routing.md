---
title: 'LLM Wiki and Agent Knowledge Routing Reference'
type: content/reference
status: active
owner: platform
updated: 2026-08-07
---

# LLM Wiki and Agent Knowledge Routing Reference

## Overview

This reference records how machine-readable knowledge indexes for LLM agents are
specified externally, how this repository implements one, and where the two
diverge. It covers the `llms.txt` proposal, the Model Context Protocol Resources
and Prompts primitives, the CLAUDE.md and AGENTS.md instruction-file
conventions, and the sitemap protocol, each checked on 2026-08-07. It then
records the exact behavior of `scripts/generate-llm-wiki-index.sh` and the
discoverability of `docs/90.references/llm-wiki/wiki-index.md` to a cold agent.

The central finding is a divergence of purpose. External index conventions
optimize for a consumer that fetches an index and then decides what to read.
This repository's index is a deterministic, byte-reproducible canonical-owner
link map that is not part of the documented just-in-time loading sequence any
agent actually follows.

This is descriptive Stage 90 reference material. It does not change the
generator, the loading sequence, the boundary statements, or any validator.

### Purpose

- Record source-backed definitions of the external index conventions an agent
  may encounter, with their stated limits.
- Record what `scripts/generate-llm-wiki-index.sh` guarantees and what it
  cannot guarantee.
- Separate three distinct drift risks that the repository currently treats as
  one.
- Route each gap to the repository path that owns it.

## Reference Type

- Type: durable-concept / external-standard-snapshot
- Source checked: `2026-08-07`
- Refresh trigger: an `llms.txt` specification change; an MCP specification
  revision; a Claude Code or Codex instruction-file discovery change; a change
  to `scripts/generate-llm-wiki-index.sh`, `docs/90.references/llm-wiki/`, or
  the Stage 00 just-in-time loading sequence.

## Authority Boundary

- **Authoritative for**:
  - Dated external findings and their explicit limits, checked 2026-08-07.
  - The observed behavior of `scripts/generate-llm-wiki-index.sh` and the
    validators that consume it, read on 2026-08-07.
  - The observed discoverability assessment of `wiki-index.md`.
- **Not authoritative for**:
  - The generator's content, the boundary statements enforced by
    `scripts/validate-repo-quality-gates.sh`, or the loading sequence in
    `docs/00.agent-governance/rules/bootstrap.md`.
  - Any claim that a provider runtime reads `wiki-index.md`. No such evidence
    exists; the lane is `DEFER`.
  - Any decision to add a repository-root machine entrypoint. That requires
    explicit human approval under the no-new-files rule.
  - Live cluster, provider runtime, hosted CI, or remote evidence.

## Scope

### In Scope

- `llms.txt`, MCP Resources and Prompts, CLAUDE.md, AGENTS.md, Codex
  instruction discovery, and the sitemap protocol as index conventions.
- The repository's generator, index, boundary enforcement, and consumers.
- Drift classification and gap routing.

### Out of Scope

- Editing `wiki-index.md`, which is generated and hand-edit protected.
- Changing the generator, the loading sequence, or any boundary phrase.
- Introducing MCP exposure, embeddings, vector stores, or a retrieval service.
  The repository excludes all of these by policy.
- Live, provider-runtime, hosted-CI, or remote verification.

## Definitions / Facts

### External Index Conventions

**`llms.txt`** (<https://llmstxt.org/>, checked 2026-08-07). A file served at
the website root that carries "brief background information, guidance, and
links to detailed markdown files", because context windows are too small to
consume whole sites. Mandated structure, in order: a required H1 with the
project name; an optional blockquote summary; optional heading-free sections;
and optional H2-delimited file lists whose entries are "a required markdown
hyperlink `[name](url)`, then optionally a `:` and notes about the file". An
`Optional` section has defined semantics: "if it's included, the URLs provided
there can be skipped if a shorter context is needed". The proposal's stated
rationale for markdown is that it "is human and LLM readable, but is also in a
precise format allowing fixed processing methods".

Two corrections worth recording. The specification's expansion artifacts are
`llms-ctx.txt` and `llms-ctx-full.txt`, produced by the `llms_txt2ctx` tool; the
commonly cited `llms-full.txt` does not appear in the specification text. And
the specification mandates nothing: no crawler is required to fetch the file,
and it defines no freshness field, no size budget, and no validator.

**Model Context Protocol** (<https://modelcontextprotocol.io/>, spec revision
`2026-07-28`, checked 2026-08-07). Resources are "designed to be
**application-driven**, with host applications determining how to incorporate
context based on their needs". Methods are `resources/list` (paginated,
cacheable), `resources/read`, and `resources/templates/list`. Resource
annotations relevant to index design are `audience` (`user` or `assistant`),
`priority` (0.0 to 1.0, where "1 means 'most important' (effectively required)"),
and `lastModified` (ISO 8601); clients "can use these annotations to ...
Prioritize which resources to include in context". Prompts are
"**user-controlled**", and a prompt message may carry a `resource_link` — a URI
reference with no inlined content, which is the protocol's documented way to
hand an agent a pointer instead of a body. MCP defines no documentation-index
file format and no chunking rule.

**Sitemap protocol** (<https://www.sitemaps.org/protocol.html>, checked
2026-08-07). Requires `<urlset>`, `<url>`, `<loc>`; optionally `<lastmod>`,
`<changefreq>` (a hint, "not a command"), and `<priority>` (0.0 to 1.0, default
0.5, meaningful only within one site). Limits are 50,000 URLs and 50 MB
uncompressed per sitemap. A sitemap at `/catalog/sitemap.xml` may only list URLs
under `/catalog/`. The convention that matters here is per-entry `lastmod` and
`priority`: an index that carries neither gives a consumer no basis to choose.

**Instruction-file conventions.** `AGENTS.md` (<https://agents.md/>, checked
2026-08-07) is plain Markdown with no required fields, placed at the repository
root, where "the closest one takes precedence". OpenAI Codex
(<https://learn.chatgpt.com/docs/agent-configuration/agents-md.md>, reached by
HTTP 308 from `developers.openai.com/codex/guides/agents-md`, checked
2026-08-07) reads at most one file per directory, concatenates "from the root
down, joining them with blank lines", and "stops adding files once the combined
size reaches the limit defined by `project_doc_max_bytes` (32 KiB by default)".
Claude Code (<https://code.claude.com/docs/en/memory>, checked 2026-08-07)
concatenates managed policy, user, project, and local files "rather than
overriding each other", supports `@path` imports "with a maximum depth of four
hops", targets "under 200 lines per CLAUDE.md file", and states plainly that
"Claude Code reads `CLAUDE.md`, not `AGENTS.md`".

**Progressive disclosure precedent.** Claude Code skills
(<https://code.claude.com/docs/en/skills>, checked 2026-08-07) state that "a
skill's body loads only when it's used, so long reference material costs almost
nothing until you need it", and that "the combined `description` and
`when_to_use` text is truncated at 1,536 characters in the skill listing to
reduce context usage". That is the clearest external precedent for a
metadata-only discovery layer with a hard budget.

### The Repository Generator

`scripts/generate-llm-wiki-index.sh` is 157 lines. It resolves its root from
`BASH_SOURCE`, so it is working-directory independent, and writes to a
hardcoded `docs/90.references/llm-wiki/wiki-index.md`. It accepts `--check` and
`-h|--help`; any other argument exits 2.

The generator body is a single quoted heredoc. Because the heredoc is quoted,
there is no variable expansion, no command substitution, no date computation, no
globbing, and no repository traversal. The entire index — frontmatter, prose,
the 24-row owner table, sources, freshness, and related documents — is a
literal string inside the script.

In write mode it creates the output directory, writes the heredoc, and prints
`[PASS] generated <path>`. In `--check` mode it renders to a temporary file,
fails with `ERR generated LLM WIKI index is missing` when the output is absent,
`cmp`-compares otherwise, and on mismatch prints `ERR generated LLM WIKI index
is stale` followed by a diff when `diff` is available. Both failure paths exit 1.

What this guarantees is byte-exact reproducibility and detection of any hand
edit. `scripts/reference_information_architecture.py` strengthens that by
executing the check under a closed environment with `HOME=/nonexistent`,
`PATH=/usr/bin:/bin`, `LANG=LC_ALL=C`, and a 10-second timeout.
`scripts/validate-repo-quality-gates.sh` additionally asserts twelve literal
boundary phrases in the collection README, including `reference-only`,
`deterministic`, `link map`, `not a runtime surface`, `not a vector store`, and
`not a retrieval service`, and rejects non-Markdown files and `embeddings/`,
`vector/`, `cache/`, `dist/`, `site/`, `node_modules/`, and `runtime/` path
segments under `llm-wiki/`.

What it does not do is equally important. It never scans the repository, so the
"declared inputs" list is a contract about where content originates, not
something the script reads. It never verifies that a linked path exists: a row
pointing at a deleted file passes `--check` indefinitely. And it never advances
a date — `updated`, `Source checked`, and `Last reviewed` are frozen `2026-05-10`
literals at lines 41, 63, and 87, so regenerating on 2026-08-07 still emits
2026-05-10.

### Three Distinct Drift Risks

The repository currently treats index integrity as one problem. It is three.

| Risk            | What it means                                              | Control                                                                                                       | State                        |
| --------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| Artifact drift  | The committed index no longer matches the generator        | `--check` byte comparison, wired into the repository quality gate                                             | Controlled                   |
| Reference drift | An index row points at a path that no longer exists        | `scripts/validate-links-and-owners.py --mode strict`, a different validator the generator knows nothing about | Partially controlled         |
| Coverage drift  | The repository gains a domain the index never learns about | None                                                                                                          | Uncontrolled                 |
| Date drift      | Freshness fields cannot advance                            | None; the dates are literals                                                                                  | Uncontrolled by construction |

Coverage drift is observable today. `infrastructure/`, `traefik/`, `tests/`,
`.github/`, `_workspace/`, `docs/98.archive/`, and
`docs/00.agent-governance/memory/` are linked from the repository root README
but have no row in the 24-row index, while `gitops/`, `scripts/`, and
`examples/` do.

### Discoverability

There is no `llms.txt`-equivalent at the repository root; a glob for
`llms*.txt` returns nothing. The functional entrypoints are the four shims
`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, and `.claude/CLAUDE.md`.

A cold agent following the documented just-in-time sequence in
`docs/00.agent-governance/rules/bootstrap.md` — bootstrap, preflight, persona,
one scope, provider notes, progress ledger, postflight — never reads
`wiki-index.md`. The sequence does not mention it. The only always-loaded
mention is in `.claude/CLAUDE.md`, and it is a do-not-edit warning rather than a
navigation instruction. Neither `AGENTS.md` nor `GEMINI.md` references it at
all.

The index is therefore well protected from corruption and absent from the load
path it was built to serve.

### Gap Routing

| ID      | Gap                                                                                                                                                                     | Owning path                                                                                                                                                                                  |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| WIKI-G1 | No repository-root machine entrypoint comparable to `llms.txt`; the index sits at Stage 90 and is unreferenced by the Codex and Gemini shims                            | `docs/00.agent-governance/rules/bootstrap.md` (loading sequence). A new root file needs explicit human approval and would also conflict with the Markdown-only rule enforced for `llm-wiki/` |
| WIKI-G2 | The 24 rows are flat; no priority or optional tier exists, unlike `llms.txt` Optional and MCP `priority`                                                                | `scripts/generate-llm-wiki-index.sh`, bounded by `docs/90.references/llm-wiki/README.md`                                                                                                     |
| WIKI-G3 | `updated`, `Source checked`, and `Last reviewed` are frozen literals that regeneration never advances, so freshness metadata is unfalsifiable                           | `scripts/generate-llm-wiki-index.sh` lines 41, 63, 87                                                                                                                                        |
| WIKI-G4 | `--check` proves reproducibility, not correspondence; the generator inspects nothing                                                                                    | `scripts/generate-llm-wiki-index.sh`; existence enforcement belongs to `scripts/validate-links-and-owners.py`                                                                                |
| WIKI-G5 | No structured export of the owner entries exists; the JSON records only the generator relation, so non-Markdown consumers must parse prose tables                       | `docs/90.references/data/reference-information-architecture.json`                                                                                                                            |
| WIKI-G6 | `wiki-index.md` is absent from the canonical just-in-time sequence, so its stated purpose is not wired into any documented load path                                    | `docs/00.agent-governance/rules/bootstrap.md`, `.claude/CLAUDE.md`                                                                                                                           |
| WIKI-G7 | Coverage holes: seven root-linked areas have no index row                                                                                                               | `scripts/generate-llm-wiki-index.sh`, `docs/90.references/llm-wiki/README.md`                                                                                                                |
| WIKI-G8 | Provider context budgets are unrecorded: Codex 32 KiB `project_doc_max_bytes`, Claude four-hop import depth and 200-line target, versus this repository's import chains | `docs/00.agent-governance/providers/claude.md`, `docs/00.agent-governance/providers/codex.md`                                                                                                |
| WIKI-G9 | MCP-style protocol exposure does not exist                                                                                                                              | Excluded by policy at `docs/90.references/llm-wiki/README.md` and enforced by boundary phrases; changing it needs a Spec, not a reference                                                    |

## Sources

- <https://llmstxt.org/> checked 2026-08-07. Adopted: file purpose, mandated
  structure, `Optional` semantics, and the markdown rationale. Rejected: any
  claim of mandatory client support, and the attribution of `llms-full.txt` to
  this specification.
- <https://modelcontextprotocol.io/specification/latest> and
  `/specification/2026-07-28/server/resources` and `/server/prompts`, checked
  2026-08-07. Adopted: Resources and Prompts primitives, the
  application-driven and user-controlled framings, and the `audience`,
  `priority`, and `lastModified` annotations. Rejected: any documentation-index
  format or chunking rule; MCP defines none.
- <https://code.claude.com/docs/en/memory> checked 2026-08-07. Adopted: the
  concatenation model, four-hop import depth, 200-line target, and the
  statement that Claude Code reads `CLAUDE.md`, not `AGENTS.md`. Rejected: any
  guarantee of instruction compliance.
- <https://code.claude.com/docs/en/skills> checked 2026-08-07. Adopted:
  progressive disclosure and the 1,536-character listing budget. Rejected: any
  claim that this repository uses skills for knowledge routing.
- <https://agents.md/> checked 2026-08-07. Adopted: root placement and
  nearest-file precedence. Rejected: any schema or size rule; the format
  defines none.
- <https://learn.chatgpt.com/docs/agent-configuration/agents-md.md> checked
  2026-08-07, reached by HTTP 308 from
  <https://developers.openai.com/codex/guides/agents-md>. Adopted: one file per
  directory, root-down concatenation, and the 32 KiB default budget. Rejected:
  any index or freshness convention.
- <https://www.sitemaps.org/protocol.html> checked 2026-08-07. Adopted:
  `lastmod` and `priority` as per-entry consumer signals, and the scale limits.
  Rejected: applicability to a repository-local Markdown index.
- Repository evidence read 2026-08-07: `scripts/generate-llm-wiki-index.sh`,
  `docs/90.references/llm-wiki/README.md`, `docs/90.references/llm-wiki/wiki-index.md`,
  `scripts/validate-repo-quality-gates.sh`, `scripts/reference_information_architecture.py`,
  `docs/90.references/data/reference-information-architecture.json`,
  `docs/00.agent-governance/rules/bootstrap.md`, `.claude/CLAUDE.md`,
  `docs/00.agent-governance/memory/README.md`.

## Review and Freshness

- Review when the generator, the collection README boundary phrases, or the
  Stage 00 loading sequence changes, and when any external index convention
  publishes a revision.
- The 24-row count, the coverage holes, and the frozen dates are dated
  observations and must be re-observed rather than reused.
- Current truth for the index content stays with the generator; current truth
  for routing stays with `docs/00.agent-governance/`.
- No provider runtime was observed reading this index. That lane is `DEFER`.

## Related Documents

- [Research Pack Index](README.md)
- [Agent Memory Tiers and Management](agent-memory-tiers-and-management.md)
- [Workspace Governance Baseline](../2026-07-07-wer/workspace-governance-baseline.md)
- [LLM Wiki Collection](../../llm-wiki/README.md)
- [LLM Wiki Curation Guide](../../../05.operations/guides/0009-llm-wiki-curation-guide.md)
