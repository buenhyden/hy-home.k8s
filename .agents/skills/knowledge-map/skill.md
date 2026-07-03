---
name: knowledge-map
description: Use when maintaining provider gateway shims, governance docs, and docs/ indexes; detecting stale documents and broken cross-links in hy-home.k8s.
---

# knowledge-map

## Purpose

Maintain the governance knowledge base for `hy-home.k8s`: keep provider
gateway shims, `harness-catalog.md`, stage README files, and cross-links
consistent and up-to-date. Detect stale documents, broken references, and
coverage gaps across `docs/00.agent-governance/` and stage directories.

## Trigger Phrases

- "check for stale documents"
- "audit cross-links"
- "update governance index"
- "find broken links"
- "knowledge base audit"
- "docs coverage audit"
- "which docs are outdated"
- "update harness-catalog"

## When to Use

- Auditing whether all `docs/` stage README files link to their canonical artifacts.
- Verifying that `harness-catalog.md` Skills and Agents tables are consistent with
  `.agents/skills/*/skill.md` plus provider-native agent files on disk.
- Detecting `docs/00.agent-governance/` files that reference artifacts that no longer exist.
- After a large batch of doc changes, checking that `progress.md` is up-to-date.
- Identifying orphaned files not referenced by any index or stage README.

## When NOT to Use

- Authoring new governance policy; make policy changes in the canonical owner file.
- Tracing requirements to design; use `requirements-to-design`.
- Creating runbooks; use `ops-runbook`.
- Generating a Coverage Ledger for a full workspace analysis; use `workspace-harness-audit`.

## Workflow Steps

1. List all files under `.agents/skills/`, `.claude/agents/`,
   `.agents/agents/`, and `.codex/agents/` and compare against the Skills and
   Agents tables in `docs/00.agent-governance/harness-catalog.md`.
   Record missing or extra entries.
2. For each stage directory (`docs/01.requirements/` through `docs/05.operations/`), verify
   the stage README links to at least one artifact in its directory.
3. Scan `docs/00.agent-governance/` for `docs/`, `.claude/`, or `docs/99.templates/` links
   that point to non-existent paths.
4. Check that `docs/00.agent-governance/memory/progress.md` entries reference real files.
5. Run `bash scripts/generate-llm-wiki-index.sh --check` to detect wiki-index drift.
6. Report a gap table: File → Expected Link Target → Status (ok, stale, missing, orphaned).
7. For each gap, recommend the minimal edit to fix it (update link, remove entry, add entry).
   Do not bulk-delete; surface gaps and let the human approve fixes.

## Gap Table Format

| File                                          | Expected Link Target                           | Status  | Recommended Fix               |
| --------------------------------------------- | ---------------------------------------------- | ------- | ----------------------------- |
| `docs/00.agent-governance/harness-catalog.md` | `.agents/skills/new-skill/skill.md`            | missing | Add row to Skills table       |
| `docs/01.requirements/prd-001.md`             | `docs/02.architecture/requirements/ard-001.md` | stale   | Update Related Documents link |
