# LLM WIKI Reference Index

> LLM-readable navigation을 위한 reference-only canonical owner link map이다.

> [!NOTE]
> All AI agent interactions with this directory must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## Overview

`llm-wiki/` is a repo-local, reference-only, deterministic link map for LLM-readable navigation across `hy-home.k8s`.
It is not a runtime surface, not a static wiki site, not a vector store, and not a retrieval service.
It may contain generated Markdown indexes produced by `scripts/generate-llm-wiki-index.sh`.

This README does not define policy or procedure. It points agents and humans to the canonical owner for each domain and records the freshness trigger for the link map.

### Current Index Role

이 문서는 `hy-home.k8s`의 LLM-readable index다. root `docs/`, Agent governance, examples, GitOps, scripts, version references를 빠르게 찾기 위한 링크맵만 제공한다.

정책, 절차, 실행 명령, runtime roster, 운영 runbook 본문은 이 문서에 복제하지 않는다. 각 항목의 정본은 아래 `Definitions / Facts`와 `Related Documents`에 연결된 canonical 문서가 소유한다.

### Collection Readers

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

### Purpose

LLM과 사람이 저장소의 문서 경계를 빠르게 찾도록 돕는다. 특히 agent-first 작업에서 “어디를 읽어야 하는가”를 줄이되, 정책과 절차의 authoritative content는 원래 stage에 남긴다.

### Reference Type

- Type: durable-concept / faq
- Source checked: 2026-05-10
- Refresh trigger: canonical docs taxonomy, Agent governance routing, examples taxonomy, or version inventory path changes.

### Authority Boundary

- **Authoritative for**:
  - Repo-local LLM WIKI link map entries.
  - Generated Markdown index output under this directory.
  - Canonical ownership pointers for major documentation and runtime domains.
  - Freshness criteria for this index.
- **Not authoritative for**:
  - Requirements, architecture decisions, implementation contracts, execution plans, tasks, policies, runbooks, incidents, release gates, runtime permissions, hooks, model routing, cluster mutation, secret handling, or deployment approval.

### Language Boundary

This directory is LLM-readable by design. Canonical owner links, generated-index
contracts, authority boundaries, and freshness triggers should stay
English-first. Short Korean summaries are allowed only as human-facing context
and must not replace the canonical owner links or generated index contract.

## Scope

### In Scope

- Deterministic link map for canonical repository surfaces.
- Generated Markdown index maintained by `scripts/generate-llm-wiki-index.sh`.
- Ownership boundary summary by domain.
- Freshness trigger for keeping the link map current.

### Out of Scope

- Rendered wiki site generation.
- Vector, embedding, RAG, or search index storage.
- Additional agent, skill, hook, model, or workflow definitions beyond the cataloged `wiki-curator` runtime surface.
- Duplicated policy, procedure, or command runbook content.

## Item Index

```text
docs/90.references/llm-wiki/
├── README.md        # Reference-only LLM WIKI boundary and link map
└── wiki-index.md    # Generated canonical-owner link index
```

### Definitions / Facts

| Domain | Canonical owner | Link map role | Freshness trigger |
| --- | --- | --- | --- |
| Documentation routing | [document-stage-routing.md](../../00.agent-governance/rules/document-stage-routing.md) | Points to stage ownership rules | Stage taxonomy or routing rule changes |
| Agent-first runtime | [harness-catalog.md](../../00.agent-governance/harness-catalog.md), [agentic.md](../../00.agent-governance/rules/agentic.md) | Points to runtime matrix and execution rule owners | Agent, skill, model, hook, or provider routing changes |
| LLM Wiki generated index | [wiki-index.md](./wiki-index.md) | Points to generated canonical-owner links | Generator, taxonomy, or owner path changes |
| LLM Wiki operation | [0009-llm-wiki-curation-guide.md](../../05.operations/guides/0009-llm-wiki-curation-guide.md) | Points to refresh triggers and `wiki-curator` usage | Generator or `wiki-curator` contract changes |
| Workspace documentation hub | [docs README](../../README.md) | Points to human-facing docs map | Docs top-level or README hub changes |
| Reference inventory | [90.references README](../README.md) | Points to reference-only authority boundary | Reference category additions or moves |
| Version snapshots | [tech-stack-version-inventory.md](../data/tech-stack-version-inventory.md) | Points to repo-backed version facts | Manifest/config/example version changes or provider support changes |
| Cloud examples | [examples README](../../../examples/README.md) | Points to reference-only AWS/Azure examples | Example taxonomy, snapshot, or command-boundary changes |
| GitOps state | [gitops README](../../../gitops/README.md) | Points to desired-state ownership | GitOps root app or platform layout changes |
| Script inventory | [scripts README](../../../scripts/README.md) | Points to script lifecycle and validation contracts | Script additions, removals, or command contract changes |

### Sources

- [Agent Governance Hub](../../00.agent-governance/README.md)
- [Harness Catalog](../../00.agent-governance/harness-catalog.md)
- [Document Stage Routing Rules](../../00.agent-governance/rules/document-stage-routing.md)
- [Docs README](../../README.md)
- [Examples README](../../../examples/README.md)
- [Scripts README](../../../scripts/README.md)
- [LLM Wiki Curation Guide](../../05.operations/guides/0009-llm-wiki-curation-guide.md)

### Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-05-10
- Next review trigger: any change to `docs/` taxonomy, `examples/` taxonomy, Agent governance routing, script inventory, `wiki-curator`, generator output, or version inventory path.

## Add and Find

1. Update this README only when a canonical owner path or link-map boundary changes.
2. Regenerate `wiki-index.md` with `bash scripts/generate-llm-wiki-index.sh` after generator or owner-link changes.
3. Keep this directory reference-only; do not add embeddings, vector files, lockfiles, runtime config, package manifests, static-site output, or procedure copies.
4. If a policy or runbook needs to change, edit its canonical owner and only update this link map if the owner path changes.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/90.references/llm-wiki/`다.

- 같은 폴더의 generated index는 `./wiki-index.md`로 연결한다.
- reference sibling folder는 `../audits/`, `../data/`, `../learning/`, `../research/`로 연결한다.
- `examples/`, `gitops/`, `scripts/` 같은 root-level owner는 `../../../<path>`로 연결한다.

## Related Documents

- [90.references README](../README.md)
- [Tech Stack Version Inventory](../data/tech-stack-version-inventory.md)
- [Generated LLM WIKI Index](./wiki-index.md)
- [LLM Wiki Curation Guide](../../05.operations/guides/0009-llm-wiki-curation-guide.md)
- [Reference Maintenance Runbook](../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
- [Docs README](../../README.md)
- [Agent Governance Hub](../../00.agent-governance/README.md)
- [Agentic Execution Rule](../../00.agent-governance/rules/agentic.md)
- [Harness Catalog](../../00.agent-governance/harness-catalog.md)
- [Examples README](../../../examples/README.md)
