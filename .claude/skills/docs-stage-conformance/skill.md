---
name: docs-stage-conformance
description: Use when improving hy-home.k8s authored docs, README indexes, template conformance, duplicate-H1 cleanup, Related Documents links, or docs validation evidence under docs/99.templates.
---

# docs-stage-conformance

## Purpose

Keep `hy-home.k8s` authored documentation aligned with the repository's SDD
stage templates and validation gates while avoiding broad semantic rewrites.

## When to Use

- Docs cleanup, template conformance, or stage README/index drift work.
- Duplicate H1, missing `Related Documents`, target-relative link, or README
  repository-map fixes.
- Narrow documentation validation tasks that should not trigger a full
  workspace harness audit.

## When NOT to Use

- Full workspace Gap analysis across GitOps, scripts, QA, CI/CD, and agent
  governance; use `workspace-harness-audit`.
- New feature design or execution planning; use `docs-stage-routing` first to
  choose the canonical SDD artifact.
- Live k3d, ArgoCD, Vault, ESO, or secret/runtime validation.
- Broad content rewrites that change historical or architectural meaning unless
  a human explicitly asks for that semantic change.

## Evidence to Gather First

1. Read `AGENTS.md`, `.claude/CLAUDE.md`, `docs/00.agent-governance/rules/documentation-protocol.md`, and `docs/00.agent-governance/rules/document-stage-routing.md`.
2. Read the relevant template in `docs/99.templates/` and the owning folder
   `README.md` before editing.
3. Check current repo state with `git status --short` and identify whether the
   task is an in-place cleanup or an explicitly requested new authored artifact.
4. Prefer repo-native validators before custom scans.

## Workflow Steps

1. Audit first; do not edit until the concrete contract drift is identified.
2. Classify each finding as template drift, README/index drift, link drift,
   heading drift, validation drift, historical-doc alignment, or intentional
   template/example content.
3. Apply the smallest in-place fix that satisfies the contract.
4. Do not create new spec/task/plan artifacts for narrow docs cleanup unless
   the human explicitly asks or the owning repo rule requires them.
5. Keep historical docs historical; structural alignment must not imply new
   runtime or architecture decisions.
6. If a validator needs adjustment, scope the check to the intended document
   family and avoid broad whole-tree heuristics unless already repo policy.
7. Update the owning README only when files are added, moved, removed, or an
   index entry is demonstrably stale.
8. Append a concise `docs/00.agent-governance/memory/progress.md` entry for
   repo-changing docs cleanup when the repo rules require progress evidence.

## Verification

- Run `bash scripts/validate-repo-quality-gates.sh .`.
- Run `bash scripts/generate-llm-wiki-index.sh --check` when README/index or
  reference-map changes are involved.
- Run `git diff --check` before staging.
- For heading work, run a targeted duplicate-H1 scan that excludes fenced code,
  comments, and intentional template examples.
- For link work, run the repo validator plus a targeted `rg` check for the
  exact drift that was fixed.

## Common Mistakes

- Rewriting content because the structure is stale.
- Treating templates under `docs/99.templates/` as authored docs that must match
  their own examples.
- Creating a new Plan or Task for a narrow docs cleanup when an in-place fix and
  progress entry are enough.
- Using a broad custom scan as proof without checking whether repo-native gates
  already cover the contract.
