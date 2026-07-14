---
title: 'Postflight Checklist (March 2026)'
type: governance/reference
status: draft
owner: platform
updated: 2026-07-14
---

# Postflight Checklist (March 2026)

## Overview

Run this checklist before finalizing a response.

## Authority Boundary

### 2. Language and Audience

- [ ] All `docs/00.agent-governance/*` changes are English.
- [ ] Human-facing README files remain Korean.
- [ ] Final user response is Korean.

### 7. Branch Completion Boundary

- [ ] Relevant local verification passed before offering merge/PR/keep/discard options.
- [ ] Workspace state was identified as normal checkout, linked worktree, or detached HEAD.
- [ ] Base branch was determined from repository evidence; default is `main`.
- [ ] Finish options were presented explicitly instead of assumed.
- [ ] No merge, push, branch deletion, reset, clean, or worktree removal was performed without human selection.
- [ ] Any destructive discard required exact typed confirmation and recorded affected branch, commits, and worktree path.
- [ ] PR handoff preserves the branch/worktree for review iteration.

## Governance Context

### 1. Policy Consistency

- [ ] JIT order is still consistent: bootstrap -> preflight -> persona -> scope -> provider -> progress -> postflight.
- [ ] No contradictory statements were introduced across rules/scopes/providers.
- [ ] Gateway files remain thin and non-duplicative.

### 3. Reference Integrity

- [ ] All newly added links resolve correctly.
- [ ] Relative paths in templates resolve from template location.
- [ ] Optional placeholder paths are not emitted as broken Markdown links.
- [ ] README files satisfy their registry-selected required/allowed H2 contract; no deprecated related-document heading remains.

### 4. Stage Compliance

- [ ] Any stage-specific guidance is consistent with `stage-authoring-matrix.md`.
- [ ] Inputs/outputs/templates/DoD are aligned for affected stages.

## Current Contract

### 6. Docs 3 Rules Compliance

- [ ] R1: Template read before document creation; `status: draft` set; k8s triggers respected (namespace→ARD, RBAC→ADR, prod→OPER first).
- [ ] R2: Folder-level changes **and content modifications to existing documents** include a README review and update (if stale) in the same PR, with the selected README profile intact.
- [ ] R3: Every new authored document includes `## Related Documents` section.
- [ ] R4: Memory ledger coupling is satisfied for repo-changing work and standalone memory files.
- [ ] No HALT condition is unresolved before PR submission.

## Validation and Refresh

### 5. Verification Evidence

- [ ] The owning Task or evidence record identifies scope, changed paths, and acceptance IDs.
- [ ] Validation commands and tool/version were recorded (or limitations were stated).
- [ ] Relevant outputs were reviewed.
- [ ] `affected`, `staged`, `all-files`, `message/manual`, `ci`, and `remote/live` lanes are each reported as `PASS`, `SKIP`, `FAIL`, or `DEFER` without inference across lanes.
- [ ] No-file and unavailable optional-tool outcomes are `SKIP`; any fallback result is recorded separately.
- [ ] Lifecycle hook guard ran or equivalent validation commands were executed; PreCompact advisory output is not treated as completion evidence.
- [ ] Unresolved risks are explicitly documented.
- [ ] Reviewer identity/disposition, rollback, residual risk, and next owner are recorded.
- [ ] No direct cluster mutation or plaintext Kubernetes secret was introduced.
- [ ] `.claude/*.local.md` files remain ignored and untracked; Hookify local rules keep required frontmatter when present.
- [ ] Staged and unstaged changes were reviewed for scope.
- [ ] Unavailable tools, skipped live validation, or CI-only checks were stated.
- [ ] `memory/progress.md` was updated with progress, reusable memory, evidence, and handoff for repo-changing work.
- [ ] Standalone memory files, if any, used `docs/99.templates/templates/common/memory.template.md` and link back to a related `progress.md` entry.

The canonical lane, result, and handoff field definitions are in
[`quality-standards.md`](quality-standards.md). Static adapter presence is
repo-static evidence only and must not be reported as native provider runtime
consumption.

## Related Documents
