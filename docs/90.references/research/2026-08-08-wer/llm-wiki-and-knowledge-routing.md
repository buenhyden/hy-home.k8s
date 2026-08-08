---
title: 'Reference: LLM-WIKI and Knowledge Routing'
type: content/reference
status: active
owner: platform
updated: 2026-08-08
---

# Reference: LLM-WIKI and Knowledge Routing

## Overview

Baseline routing for LLM-WIKI, repository knowledge indexes, and freshness.

## Reference Type

Repository-static research baseline.

## Authority Boundary

Index generators and their canonical document owners retain authority. This
reference does not prove retrieval quality or provider consumption.

## Scope

It covers deterministic routing, authority, freshness, and drift questions for
WERPC-003.

## Definitions / Facts

### LLM-WIKI baseline

`docs/90.references/llm-wiki/` is current workspace evidence. External index
conformance and actual retrieval behavior are Unverified.

### Knowledge-routing baseline

Repository links and generated indexes are local evidence; freshness across all
consumers is Unverified.

## Sources

No external knowledge-routing source was checked in WERPC-001. Dated predecessor
sources remain recheck-required evidence in the ledger.

## Review and Freshness

WERPC-003 owns current source review. Refresh after index-generator or
authority-routing changes.

## Related Documents

- [Documentation architecture](documentation-architecture-and-diataxis.md)
- [Source ledger](source-coverage-and-migration-ledger.md)
- [LLM-WIKI index](../../llm-wiki/README.md)
