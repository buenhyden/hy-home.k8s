---
title: 'LLM Wiki Curation Guide'
type: sdlc/guide
status: active
owner: platform
updated: 2026-05-10
---

# LLM Wiki Curation Guide

## Overview

이 문서는 `hy-home.k8s`의 repo-local LLM Wiki를 관리하는 방법을 설명한다. LLM Wiki는 vector store, retrieval service, static wiki site가 아니라 canonical owner를 찾기 위한 deterministic Markdown link map이다.

`wiki-curator` agent는 이 링크맵을 갱신하고 stale link를 찾는 worker다. 정책, 절차, 배포 승인, runtime 권한은 이 guide나 LLM Wiki가 아니라 각 canonical owner가 소유한다.

## Guide Type

`how-to`

## Target Audience

- Platform maintainer
- Documentation writer
- AI agent operator
- Agent-tuner

## Purpose

LLM Wiki entrypoint, generated index, `wiki-curator` agent 사용 시점을 일관되게 관리하고, source SSoT를 복제하지 않도록 한다.

## Prerequisites

- Repository checkout at `hy-home.k8s`.
- `python3` and `bash` available for repo quality gates.
- Current governance routing reviewed in [Harness Catalog](../../00.agent-governance/harness-catalog.md) and [Document Stage Routing Rules](../../00.agent-governance/rules/document-stage-routing.md).

## Step-by-step Instructions

1. Identify the canonical owner first. Policy, procedure, runtime roster, and command boundary changes must start in their owner files.
2. Use `wiki-curator` when the change affects LLM Wiki entrypoints, generated owner links, stale-link detection, or README/index routing.
3. Update the generator only when a canonical owner link or indexed domain changes.
4. Regenerate the Markdown index.

   ```bash
   bash scripts/generate-llm-wiki-index.sh
   ```

5. Check that generated output is current.

   ```bash
   bash scripts/generate-llm-wiki-index.sh --check
   ```

6. Run the repo quality gate before handoff.

   ```bash
   bash scripts/validate-repo-quality-gates.sh .
   ```

## Common Pitfalls

- Treating `docs/90.references/llm-wiki/wiki-index.md` as the source of policy instead of a generated pointer.
- Editing `wiki-index.md` by hand instead of updating `scripts/generate-llm-wiki-index.sh` and regenerating.
- Adding embeddings, vector files, package manifests, lockfiles, runtime caches, or static-site output under `docs/90.references/llm-wiki/`.
- Letting `wiki-curator` invent policy instead of escalating ownership to `doc-writer`, `supervisor`, or the canonical owner file.

## Related Documents

- **Operation**: [Agentic Execution Rules](../../00.agent-governance/rules/agentic.md)
- **Operation**: [Harness Catalog](../../00.agent-governance/harness-catalog.md)
- **Operation**: [Document Stage Routing Rules](../../00.agent-governance/rules/document-stage-routing.md)
- **Reference**: [LLM WIKI README](../../90.references/llm-wiki/README.md)
- **Reference**: [Generated LLM WIKI Index](../../90.references/llm-wiki/wiki-index.md)
