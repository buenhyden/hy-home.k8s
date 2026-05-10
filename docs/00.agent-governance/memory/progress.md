# Agent Progress and Memory Ledger

This file is the repo-local progress and reusable memory ledger for AI agent
work in `hy-home.k8s`. Use `docs/99.templates/progress.template.md` for new
entries. Memory here supports future task intake, but current runtime truth
stays in `docs/00.agent-governance/harness-catalog.md` and current script
inventory stays in `scripts/README.md`.

## Work Entries

### 2026-05-10 — Docs taxonomy and progress memory contract

- **Date**: 2026-05-10
- **Layer**: meta
- **Status**: complete
- **Tags**: #governance #docs #memory

#### Progress

- Migrated the canonical docs taxonomy from the old stage folders to
  `01.requirements`, `02.architecture`, `03.specs`, `04.execution`, and
  `05.operations`.
- Added `docs/99.templates/progress.template.md` as the template for this
  `progress.md` ledger.
- Updated bootstrap, preflight, postflight, documentation protocol, runtime
  baseline, and memory README guidance so AI agents read and write this ledger
  during repo-changing work.

#### Memory

- `docs/00.agent-governance/memory/progress.md` is the mandatory local ledger
  for repo-changing agent progress, reusable memory, evidence, and handoff.
- Standalone memory notes may still use `docs/99.templates/memory.template.md`,
  but normal agent work should append to this file using
  `docs/99.templates/progress.template.md`.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` PASS.

#### Handoff

- None.

### 2026-05-10 — 90.references role and format contract

- **Date**: 2026-05-10
- **Layer**: docs
- **Status**: complete
- **Tags**: #docs #references #governance

#### Progress

- Audited `docs/90.references/README.md`, `docs/90.references/agents/README.md`,
  current reference documents, `docs/99.templates/reference.template.md`, and
  document routing rules.
- Clarified that `90.references` owns durable lookup facts, dated external
  snapshots, version inventories, and learning references, but not requirements,
  architecture decisions, implementation contracts, plans, policies, runbooks,
  release approval, or live mutation procedures.
- Added required `Reference Type`, `Authority Boundary`, and
  `Review and Freshness` sections to `reference.template.md` and aligned current
  reference documents to that format.

#### Memory

- `90.references` can be authoritative for factual lookup and dated snapshot
  values only when the document states its source checked date and freshness
  trigger.
- `tech-stack-version-inventory.md` remains a version-contract inventory only
  when repo manifests/config/examples are updated with it in the same change.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- Targeted stale taxonomy/reference grep returned no matches.

#### Handoff

- None.

## Historical Entries

### Harness Implementation Progress

- **Date**: 2026-04-13
- **Layer**: meta
- **Tags**: #governance #harness #settings
- **Record type**: historical initial implementation snapshot.

Current runtime truth is maintained in `docs/00.agent-governance/harness-catalog.md`.
Current script inventory is maintained in `scripts/README.md`. This memory entry
preserves the initial remediation history and must not be treated as the current
runtime or script roster when those files disagree.

### Problem

Harness layers L1–L6 were incomplete: no `settings.json`, no agent files, no hooks, no k8s scripts, scopes lacked §File Ownership, and no subagent protocol existed.

### Context

- Affected paths: `.claude/`, `scripts/`, `docs/00.agent-governance/scopes/`, `AGENTS.md`, `CLAUDE.md`
- Environment: k3d local cluster, WSL2, ArgoCD GitOps
- Preconditions: Only `settings.local.json` and empty `.claude/` subdirectories existed.

### Resolution

**P0 (complete):**

- `AGENTS.md` restructured to §1–§8 with Agent Catalog, Settings, Role Separation.
- `CLAUDE.md` and `GEMINI.md` updated to ≤30/25 lines gateway overlays.
- `documentation-protocol.md` updated with §Docs 3 Rules (HALT).
- `bootstrap.md` updated with in-place refactor rule.
- `postflight-checklist.md` updated with §6 Docs 3 Rules Compliance.

**P1 (complete):**

- All `scopes/*.md` updated with §File Ownership and §Subagent Bridge.
- `providers/agents-md.md` created.
- `subagent-protocol.md` created.
- `memory/progress.md` created (this file).

**P2 (complete):**

- `.claude/settings.json` — created; git-tracked with allow/deny permission lists and 3 hooks (SessionStart, PreToolUse, PostToolUse).
- `.claude/hooks/` — 3 scripts created: `session-start.sh`, `k8s-pre-edit.sh`, `post-validate.sh`.
- `.claude/agents/` — 7 agent files created: `supervisor.md`, `k8s-implementer.md`, `gitops-reviewer.md`, `security-auditor.md`, `incident-responder.md`, `code-reviewer.md`, `doc-writer.md`.
- `scripts/` — 3 validation scripts created: `validate-k8s-manifests.sh`, `validate-gitops-structure.sh`, `check-secret-handling.sh`.
  Current script inventory is maintained in `scripts/README.md`; this memory entry records the initial harness implementation state.

**P4 (complete, 2026-04-13):**

- Legacy harness examples were migrated into workspace-specific skills under `.claude/skills/`:
  - `deployment-strategies` — k8s/ArgoCD deployment strategy catalog (cicd-pipeline lineage)
  - `incident-postmortem` — cluster incident post-analysis pipeline (incident-postmortem lineage)
  - `rca-methodology` — 5 Whys / Fishbone / FTA / Change Analysis reference (incident-postmortem lineage)
  - `k8s-security-audit` — structured RBAC/NetworkPolicy/Secret/container/supply-chain audit workflow (security-audit lineage)
  - `vulnerability-patterns` — k8s manifest and Helm chart misconfiguration catalog with CIS 5.x mappings (security-audit, code-reviewer lineage)
- `docs/00.agent-governance/harness-catalog.md` Skills table updated from 3 to 8 entries.
- Legacy source example directory removed after migration.

**P3 (complete):**

- Local harness catalog authored under `docs/00.agent-governance/`.
- Model policy standardized: agents use sonnet; supervisor uses opus.
- Legacy source-directory references removed from gateway and protocol files.

### Prevention

- Run `postflight-checklist.md §6 Docs 3 Rules` before every PR.
- `settings.json` must be git-tracked; `settings.local.json` must stay `.gitignore`d.
- Runtime catalog entries in `docs/00.agent-governance/harness-catalog.md` must
  stay in sync with `.claude/agents/`, `.codex/agents/`, `.claude/skills/`,
  and the hook boundary between `.claude/settings.json` and `.codex/hooks.json`.
