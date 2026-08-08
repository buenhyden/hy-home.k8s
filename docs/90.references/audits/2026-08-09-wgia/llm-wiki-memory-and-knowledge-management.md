---
title: 'Audit: LLM-WIKI, Memory, and Knowledge Management'
type: content/reference
status: draft
owner: platform
updated: 2026-08-09
---

# Audit: LLM-WIKI, Memory, and Knowledge Management

## Overview

This report owns the audit of LLM-WIKI, deterministic knowledge routing, the
four memory classes, freshness, promotion, retention, conflict, redaction,
archive/GC, compaction, and handoff. WGIA-001 records current owners and
boundaries; WGIA-006 owns complete analysis and review.

## Reference Type

Dated repository-static knowledge and memory audit. It is not a knowledge
router, generated index, memory policy, checkpoint, or provider-local store.

## Authority Boundary

LLM-WIKI source/index contracts, the generator, Stage 00 memory owners, and
machine schemas retain authority. This report does not hand-edit generated
output, read ignored or provider-local memory, promote temporary context, or
infer provider/runtime delivery from tracked files.

## Scope

Included: LLM-WIKI sources and generated boundary, deterministic routing,
working-short-term, durable-long-term, domain-scoped, provider-local-auxiliary
memory, freshness, promotion, retention, conflict, redaction, compaction, and
handoff. Excluded: private runtime state, credentials, ignored checkpoints,
provider recall, generator modification, and conclusions before WGIA-006.

## Definitions / Facts

### LLM-WIKI

`docs/90.references/llm-wiki/README.md` routes the collection,
`wiki-index.md` is generated output, and `scripts/generate-llm-wiki-index.sh`
is the current producer/check surface. Canonical sources, not a hand edit to
the index, own knowledge changes.

### Memory Tiers and Management

The current contract has exactly four classes:
`working-short-term`, `durable-long-term`, `domain-scoped`, and
`provider-local-auxiliary`. `docs/00.agent-governance/memory/progress.md` is
the durable shared progress ledger, not a fifth class. Repository evidence and
canonical owners win conflicts with temporary or provider-local context.

### Canonical-owner Inventory

| Role | Current evidence surface | Foundation use |
| --- | --- | --- |
| Knowledge human index | `docs/90.references/llm-wiki/README.md` | Collection routing. |
| Generated output | `docs/90.references/llm-wiki/wiki-index.md` | Derived lookup only. |
| Evidence producer | `scripts/generate-llm-wiki-index.sh` | Generation and drift check. |
| Memory policy/index | `docs/00.agent-governance/memory/README.md` | Four-class use and routing. |
| Durable ledger | `docs/00.agent-governance/memory/progress.md` | Shared progress evidence. |
| Machine owner | checkpoint, loop, harness, and closure contracts | Synthetic lifecycle enforcement. |

### Finding Convention

Every material finding uses the complete finding field set and the closed audit
verdict/evidence-depth vocabularies. Source facts must distinguish authored
canonical input, generated output, evidence producer, and advisory runtime
state; unavailable advisory/runtime evidence is `DEFER`.

#### WGA-KNW-001 — Knowledge and memory owner inventory established

- **Request IDs**: LLM-WIKI and memory-tiers/management coverage rows in the pack index.
- **Scope**: pinned source, generated output, generator, memory index, durable ledger, and machine-contract inventory.
- **Expected state**: WGIA-006 can verify routing, lifecycle, freshness, conflict, redaction, retention, promotion, GC, compaction, and handoff against unique owners.
- **Observed state**: current owner families and four-class vocabulary are identified; source coverage and lifecycle completeness remain pending.
- **Evidence**: `docs/90.references/llm-wiki/README.md#item-index`; `docs/90.references/llm-wiki/wiki-index.md#authority-boundary`; `scripts/generate-llm-wiki-index.sh#generate_index`; `docs/00.agent-governance/memory/README.md#four-memory-classes`; `docs/00.agent-governance/memory/progress.md#work-entries`; `docs/00.agent-governance/contracts/agent-checkpoint.schema.json#properties`; `docs/00.agent-governance/contracts/agent-loop-lifecycle.json#checkpointBoundary`; `docs/00.agent-governance/contracts/harness-contract.json#memory`; `docs/00.agent-governance/contracts/agent-governance-closure.json#memoryLayers`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Partial`.
- **Impact**: the later audit has a stable authority map, but current knowledge freshness and memory behavior cannot yet be concluded.
- **Disposition**: `Keep`.
- **Canonical owner**: current LLM-WIKI sources/generator and Stage 00 memory/machine contracts.
- **Verification**: generated-index `--check`, memory-contract checks, strict links, and WGIA-006 review.
- **Uncertainty**: source completeness, freshness triggers, actual compaction/handoff execution, and provider-local behavior are unobserved.
- **Blocker**: none; private and runtime lanes are intentionally `DEFER`.

## Sources

Source roles are closed to `policy owner`, `machine owner`, `human index`,
`evidence producer`, and `historical snapshot`.

| Source ID | Source role | Evidence at the observation commit | Use |
| --- | --- | --- | --- |
| SRC-WGA-KNW-001 | human index | `docs/90.references/llm-wiki/README.md#item-index`; `docs/00.agent-governance/memory/README.md#four-memory-classes`; `docs/00.agent-governance/memory/progress.md#work-entries` | Knowledge and memory routing. |
| SRC-WGA-KNW-002 | evidence producer | `scripts/generate-llm-wiki-index.sh#generate_index`; `docs/90.references/llm-wiki/wiki-index.md#authority-boundary` | Generated-index production and drift check. |
| SRC-WGA-KNW-003 | machine owner | `docs/00.agent-governance/contracts/agent-checkpoint.schema.json#properties`; `docs/00.agent-governance/contracts/agent-loop-lifecycle.json#checkpointBoundary`; `docs/00.agent-governance/contracts/harness-contract.json#memory`; `docs/00.agent-governance/contracts/agent-governance-closure.json#memoryLayers` | Synthetic lifecycle evidence. |
| SRC-WGA-KNW-004 | historical snapshot | `docs/90.references/research/2026-08-08-wer/agent-memory-tiers-and-management.md#lifecycle-rules-and-evidence-limits`; `docs/90.references/audits/2026-07-11-weia/governance-harness-loop-providers.md#residual-risks` | Source-commit-bounded context only. |

## Review and Freshness

- Review status: `Pending` for WGIA-006 independent topic review.
- Review disposition: `DEFER`; no knowledge or memory lifecycle is closed yet.
- Evidence observed: 2026-08-09 at the exact observation commit.
- Current-truth owners: canonical LLM-WIKI sources/generator and Stage 00
  memory/machine-contract surfaces.
- Refresh triggers: source, generated index, generator, memory class, lifecycle,
  freshness, promotion, retention, conflict, redaction, compaction, handoff,
  observation commit, or finding change.
- Provider-runtime, hosted, remote, credential-bearing, private-memory, and live
  evidence remains `DEFER`.

## Related Documents

- [Pack Index](README.md)
- [Spec 054](../../../03.specs/054-workspace-governance-audit-and-remediation/spec.md)
- [Memory README](../../../00.agent-governance/memory/README.md)
- [LLM-WIKI README](../../llm-wiki/README.md)
- [Implementation Task](../../../04.execution/tasks/2026-08-09-workspace-governance-audit-and-remediation.md)
