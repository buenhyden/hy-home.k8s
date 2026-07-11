---
title: 'Agent Governance Contract Normalization Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-04
---

# Agent Governance Contract Normalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Normalize the repository's AI-agent governance, provider adapter, and
QA/CI enforcement surfaces so Claude, Codex, and Gemini use one canonical
Stage 00 contract with provider-native projections.

**Architecture:** This plan follows a contract-first sequence. First capture
baseline evidence and task tracking, then normalize Stage 00 owner language,
then align provider adapters, then close GitHub/CI/QA validation drift, and
finally run full repo-static validation and review.

**Tech Stack:** Markdown governance files, TOML Codex agent mirrors, JSON hook
wiring, GitHub Actions YAML, shell/Python repository validators, and
repo-static validation scripts.

---

## Overview

This document defines the implementation plan for
`docs/03.specs/015-agent-governance-contract-normalization/spec.md`. It turns
the approved spec into small commit-sized work units with explicit files,
checks, and handoff evidence.

The work is documentation and validation-contract heavy. It still uses the
repository's TDD spirit by making every contract change measurable through
focused scans, parser checks, repository quality gates, and final harness
validation.

## Context

The repository already has a strong Stage 00 governance model:

- Root provider shims route to canonical governance and runtime baselines.
- `.agents/` owns shared provider-neutral assets.
- `.claude/**`, `.codex/**`, and `.agents/**` expose provider-native runtime
  adapters.
- `.github/workflows/ci.yml`, shared hooks, and
  `scripts/validate-repo-quality-gates.sh` provide repo-static feedback loops.

The approved spec identifies the remaining cleanup direction: role parity
should be expressed in provider-native syntax, not by forcing the same metadata
keys onto every provider. The plan must also keep `.github` Markdown files
frontmatter-free, root shims thin, and validation evidence explicit.

## Goals & In-Scope

- **Goals**:
  - Establish a current drift inventory for the target agent-governance
    surfaces.
  - Normalize Stage 00 contracts for provider-aware parity, harness engineering,
    loop engineering, subagents, QA, CI/CD, protected surfaces, and memory.
  - Align Claude, Codex, and Gemini adapters with the canonical Stage 00
    contract while preserving native syntax and runtime boundaries.
  - Align `.github` control surfaces and validators with the normalized
    contract.
  - Record task evidence and reusable memory.
- **In Scope**:
  - `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`
  - `.agents/**`, `.claude/**`, `.codex/**`
  - `.github/**`
  - `docs/00.agent-governance/**`
  - `docs/04.execution/plans/**`, `docs/04.execution/tasks/**`
  - `docs/00.agent-governance/memory/progress.md`
  - `scripts/validate-repo-quality-gates.sh` when deterministic enforcement is
    warranted

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Add a new provider family.
  - Change live cluster state.
  - Replace the docs taxonomy or template-routing contract.
  - Replace the current CI workflow architecture.
- **Out of Scope**:
  - Live k3d, ArgoCD, Vault, ESO, or Kubernetes mutation.
  - Secret value inspection.
  - Remote push, publishing, PR creation, or third-party resource mutation.
  - Broad rewrites outside the target surfaces unless a direct link or index
    must be updated for validation.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Create execution task record and baseline drift inventory | `docs/04.execution/tasks/2026-07-04-agent-governance-contract-normalization.md`, `docs/04.execution/tasks/README.md`, `docs/00.agent-governance/memory/progress.md` | VAL-AGC-001, VAL-AGC-006 | Baseline scans saved in task evidence; repo-quality gate passes |
| PLN-002 | Normalize Stage 00 canonical contract wording | `docs/00.agent-governance/common-governance.md`, `docs/00.agent-governance/subagent-protocol.md`, `docs/00.agent-governance/harness-catalog.md`, `docs/00.agent-governance/harness-implementation-map.md`, `docs/00.agent-governance/rules/*.md`, `docs/00.agent-governance/providers/*.md` | VAL-AGC-001, VAL-AGC-003 | Focused scans show one canonical owner per contract area; repo-quality gate passes |
| PLN-003 | Align provider adapter surfaces | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/CLAUDE.md`, `.codex/CODEX.md`, `.agents/GEMINI.md`, `.claude/agents/*.md`, `.agents/agents/*.md`, `.codex/agents/*.toml`, `.claude/settings.json`, `.codex/hooks.json`, `.agents/hooks.json` | VAL-AGC-002, VAL-AGC-003 | JSON/TOML parse checks pass; provider mirror scans pass; repo-quality gate passes |
| PLN-004 | Align GitHub, QA, CI/CD, and protected-surface enforcement | `.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/SECURITY.md`, `.github/workflows/ci.yml`, `docs/00.agent-governance/rules/quality-standards.md`, `docs/00.agent-governance/rules/approval-boundaries.md`, `scripts/validate-repo-quality-gates.sh` | VAL-AGC-004, VAL-AGC-005 | GitHub Markdown remains frontmatter-free; workflow YAML parses; gate/harness validation passes |
| PLN-005 | Final review, evidence closure, and branch-readiness handoff | `docs/04.execution/plans/2026-07-04-agent-governance-contract-normalization.md`, `docs/04.execution/tasks/2026-07-04-agent-governance-contract-normalization.md`, `docs/04.execution/plans/README.md`, `docs/04.execution/tasks/README.md`, `docs/00.agent-governance/memory/progress.md` | VAL-AGC-005, VAL-AGC-006 | Full validation bundle passes; final reviewer finds no blocking issue |

## Detailed Tasks

> [!NOTE]
> The unchecked items below preserve the approved historical execution
> instructions. The linked `status: done` Task is the completion-state and
> evidence owner; these boxes are not a current work queue.

### Task 1: Baseline Drift Inventory and Task Record

**Files:**

- Create: `docs/04.execution/tasks/2026-07-04-agent-governance-contract-normalization.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/00.agent-governance/memory/progress.md`
- Read: `docs/99.templates/templates/sdlc/execution/task.template.md`
- Read: `docs/03.specs/015-agent-governance-contract-normalization/spec.md`

- [ ] **Step 1: Confirm branch and clean state**

Run:

```bash
git status --short --branch
```

Expected: current branch is `codex/agent-governance-contract-normalization`
with only intentional plan-task work after this plan commit.

- [ ] **Step 2: Read the task template before authoring evidence**

Run:

```bash
sed -n '1,260p' docs/99.templates/templates/sdlc/execution/task.template.md
```

Expected: output includes `type: sdlc/task`, `## Overview`, `## Validation
Evidence`, and `## Related Documents`.

- [ ] **Step 3: Capture target inventory**

Run:

```bash
rg --files AGENTS.md CLAUDE.md GEMINI.md .agents .claude .codex .github docs/00.agent-governance | sort
```

Expected: output lists root shims, provider adapters, GitHub control surfaces,
and Stage 00 governance files.

- [ ] **Step 4: Capture provider metadata inventory**

Run:

```bash
rg -n "^---$|^name:|^description:|^model:|^tools:|^model_reasoning_effort|^description =|^developer_instructions =|^name =" .claude/agents .agents/agents .codex/agents
```

Expected: Claude agent files show `tools:` frontmatter, Gemini agent files show
Gemini model frontmatter, and Codex TOML files show `model` plus
`model_reasoning_effort`.

- [ ] **Step 5: Capture contract-drift candidates**

Run:

```bash
rg -n "tools:|permission gate|hook wiring|provider-native|mirror|parity|Subagent|subagent|AGENTS.md|CLAUDE.md|GEMINI.md|QA|CI/CD|protected surface|frontmatter" docs/00.agent-governance AGENTS.md CLAUDE.md GEMINI.md .agents .claude .codex .github
```

Expected: output identifies the active surfaces that discuss provider parity,
hook behavior, QA, CI/CD, and protected-surface rules. Classify results in the
task record as `canonical owner`, `adapter summary`, `enforcement`, or
`historical evidence`.

- [ ] **Step 6: Create the task record**

Add `docs/04.execution/tasks/2026-07-04-agent-governance-contract-normalization.md`
from the task template with:

- `title: 'Agent Governance Contract Normalization Task Record'`
- `type: sdlc/task`
- `status: draft`
- `owner: platform`
- `updated: 2026-07-04`
- Parent plan:
  `../plans/2026-07-04-agent-governance-contract-normalization.md`
- Parent spec:
  `../../03.specs/015-agent-governance-contract-normalization/spec.md`
- Task IDs: `T-001` through `T-005`, matching this plan.
- Initial T-001 status: `in-progress`.

- [ ] **Step 7: Update the Stage 04 tasks README**

Add the new task record to `docs/04.execution/tasks/README.md` with status
`Draft`, date `2026-07-04`, and a description that states it tracks agent
governance contract normalization evidence.

- [ ] **Step 8: Update progress ledger**

Append a progress entry to `docs/00.agent-governance/memory/progress.md`
stating that T-001 created the task record and captured the baseline drift
inventory. Record the commands from Steps 3 through 5 as evidence.

- [ ] **Step 9: Validate T-001**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected:

```text
[PASS] repository quality gates passed
```

- [ ] **Step 10: Commit T-001**

Run:

```bash
git add docs/04.execution/tasks/2026-07-04-agent-governance-contract-normalization.md docs/04.execution/tasks/README.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(task): Track agent governance normalization evidence"
```

Expected: one commit containing only the task record, tasks README update, and
progress ledger update.

### Task 2: Stage 00 Canonical Contract Normalization

**Files:**

- Modify: `docs/00.agent-governance/common-governance.md`
- Modify: `docs/00.agent-governance/subagent-protocol.md`
- Modify: `docs/00.agent-governance/harness-catalog.md`
- Modify: `docs/00.agent-governance/harness-implementation-map.md`
- Modify: `docs/00.agent-governance/rules/bootstrap.md`
- Modify: `docs/00.agent-governance/rules/agentic.md`
- Modify: `docs/00.agent-governance/rules/standards.md`
- Modify: `docs/00.agent-governance/rules/quality-standards.md`
- Modify: `docs/00.agent-governance/rules/approval-boundaries.md`
- Modify: `docs/00.agent-governance/providers/claude.md`
- Modify: `docs/00.agent-governance/providers/codex.md`
- Modify: `docs/00.agent-governance/providers/gemini.md`
- Modify: `docs/04.execution/tasks/2026-07-04-agent-governance-contract-normalization.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [ ] **Step 1: Recheck official capability basis**

Open or search the official sources listed in the spec for the current
Claude settings/hooks/subagents, Codex `AGENTS.md`/subagents/config, Gemini CLI
hierarchical memory and agents command, and GitHub Actions behavior.

Expected: task evidence records source URLs and the checked date
`2026-07-04`.

- [ ] **Step 2: Normalize `subagent-protocol.md` provider metadata wording**

Replace the current generic Markdown-agent requirement with provider-aware
language:

```markdown
Claude Markdown agent files must contain frontmatter with `name`,
`description`, `model`, and least-privilege `tools`. Gemini Markdown agent
files under `.agents/agents/*.md` must contain `name`, `description`, and
`model`, and must preserve the same role, scope imports, guardrails, handoff,
and postflight contract as the Claude source. They do not require Claude-style
`tools:` frontmatter unless a future approved Gemini adapter change adds a
verified native tool-scoping field. Codex agent files use TOML and must declare
`name`, `description`, `developer_instructions`, `model`, and
`model_reasoning_effort`.
```

Expected: the document still states that role parity is required across
providers, while native metadata keys differ.

- [ ] **Step 3: Normalize subagent dispatch language**

Update `subagent-protocol.md` so dispatch rules say:

```markdown
Use the provider-native delegated-agent mechanism for the current runtime:
Claude uses the Task tool or explicit agent invocation, Codex uses explicit
subagent orchestration when requested by the user, and Gemini uses its
available agent registry or project-local adapter workflow where supported.
Do not embed full role definitions inline when a provider-local agent file
exists.
```

Expected: the protocol no longer claims that every provider dispatches through
Claude's Task tool only.

- [ ] **Step 4: Normalize `common-governance.md` ownership mapping**

Revise the `Platform Mapping` and `Canonical Adapter Ownership` text so it
states:

- `.agents/` is the provider-neutral shared asset owner for skills,
  workflows, and output styles.
- `.agents/agents/*.md`, `.claude/agents/*.md`, and `.codex/agents/*.toml`
  are provider-native role adapters.
- Tool and permission syntax is provider-specific.
- Hook JSON for Codex and Gemini is context/validation wiring, not a native
  permission gate equivalent to Claude settings.

Expected: no table row implies that all providers share identical frontmatter
keys.

- [ ] **Step 5: Normalize `harness-catalog.md` matrices**

Update the `Harness Four-Element Control Model`, `Provider Capability Parity
Matrix`, `QA and CI/CD Dimensions`, and `Consistency Rules` so they state:

- Provider parity is role parity plus validation evidence.
- Claude has native settings/hooks/subagent/tool-scoping surfaces.
- Codex has official `AGENTS.md`, config, and explicit subagent orchestration,
  with `.codex/hooks.json` as repo-local context/validation wiring.
- Gemini has `GEMINI.md` hierarchical memory and agents command support, while
  this repository's `.agents/**` remains the tracked Antigravity/Gemini
  adapter baseline.
- CI/CD remains provider-agnostic and owned by GitHub Actions plus local
  validators.

Expected: readiness rows remain `Ready` only where `Gap=None` is accurate.

- [ ] **Step 6: Normalize provider notes**

Update `providers/claude.md`, `providers/codex.md`, and `providers/gemini.md`
to include short official-source basis bullets and provider-specific boundary
phrases:

- Claude: settings, hooks, subagents, native permissions, and `tools:`.
- Codex: `AGENTS.md`, config, explicit subagents, and sandbox/approval
  boundaries.
- Gemini: `GEMINI.md` hierarchical memory, agents command, and repo-local
  `.agents/**` adapter distinction.

Expected: provider notes remain concise and do not duplicate the harness
catalog's full matrices.

- [ ] **Step 7: Normalize rule documents**

Review and update `bootstrap.md`, `agentic.md`, `standards.md`,
`quality-standards.md`, and `approval-boundaries.md` so their statements match
the provider-aware contract. Preserve these exact rules:

- Root shims stay thin.
- Governance docs stay English.
- Human-facing responses stay Korean.
- Live cluster mutation is forbidden by default.
- Repo-static validation does not prove live runtime readiness.
- Repo-changing work updates `memory/progress.md`.

Expected: no rule file introduces a second provider matrix that competes with
`harness-catalog.md`.

- [ ] **Step 8: Update task and progress evidence**

Mark T-002 as completed in the task record, summarize Stage 00 files changed,
and append a progress ledger entry with the official-source basis and
validator commands.

- [ ] **Step 9: Validate T-002**

Run:

```bash
git diff --check
jq empty .agents/hooks.json .claude/settings.json .codex/hooks.json
python3 - <<'PY'
from pathlib import Path
import tomllib
for path in sorted(Path('.codex/agents').glob('*.toml')):
    tomllib.loads(path.read_text())
PY
bash scripts/validate-repo-quality-gates.sh .
```

Expected:

```text
[PASS] repository quality gates passed
```

- [ ] **Step 10: Commit T-002**

Run:

```bash
git add docs/00.agent-governance docs/04.execution/tasks/2026-07-04-agent-governance-contract-normalization.md
git commit -m "docs(governance): Normalize agent provider contracts"
```

Expected: one commit containing Stage 00 contract normalization and related
evidence only.

### Task 3: Provider Adapter Parity Alignment

**Files:**

- Modify: `AGENTS.md`
- Modify: `CLAUDE.md`
- Modify: `GEMINI.md`
- Modify: `.claude/CLAUDE.md`
- Modify: `.codex/CODEX.md`
- Modify: `.agents/GEMINI.md`
- Modify: `.claude/agents/*.md`
- Modify: `.agents/agents/*.md`
- Modify: `.codex/agents/*.toml`
- Modify: `.claude/settings.json`
- Modify: `.codex/hooks.json`
- Modify: `.agents/hooks.json`
- Modify: `docs/04.execution/tasks/2026-07-04-agent-governance-contract-normalization.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [ ] **Step 1: Verify root shims are thin**

Run:

```bash
wc -l AGENTS.md CLAUDE.md GEMINI.md
sed -n '1,80p' AGENTS.md
sed -n '1,80p' CLAUDE.md
sed -n '1,80p' GEMINI.md
```

Expected: each root shim is concise, imports or points to Stage 00 and the
provider runtime baseline, and does not embed long policy bodies.

- [ ] **Step 2: Align root shim wording**

Ensure the root shims use equivalent shape:

- `AGENTS.md`: Codex/GPT provider shim; routes to `providers/codex.md` and
  `.codex/CODEX.md`.
- `CLAUDE.md`: Claude provider shim; routes to `providers/claude.md` and
  `.claude/CLAUDE.md`.
- `GEMINI.md`: Gemini provider shim; routes to `providers/gemini.md` and
  `.agents/GEMINI.md`.

Expected: no root shim imports another provider's root shim.

- [ ] **Step 3: Align runtime baseline wording**

Update `.claude/CLAUDE.md`, `.codex/CODEX.md`, and `.agents/GEMINI.md` so each
contains the same conceptual sections:

- Purpose
- Loading Order
- Workspace Contract
- Harness Four-Element Runtime Contract
- Capabilities & Constraints
- Model Hierarchy
- Validation and Tooling
- Relationship to Gateway Files

Expected: provider-specific sections describe native behavior only; full
policy remains in Stage 00.

- [ ] **Step 4: Align agent role files**

For every agent stem in `.claude/agents/*.md`, verify matching files exist in
`.agents/agents/*.md` and `.codex/agents/*.toml`.

Run:

```bash
python3 - <<'PY'
from pathlib import Path
claude = {p.stem for p in Path('.claude/agents').glob('*.md')}
gemini = {p.stem for p in Path('.agents/agents').glob('*.md')}
codex = {p.stem for p in Path('.codex/agents').glob('*.toml')}
print('claude_only=', sorted(claude - gemini - codex))
print('gemini_only=', sorted(gemini - claude - codex))
print('codex_only=', sorted(codex - claude - gemini))
PY
```

Expected:

```text
claude_only= []
gemini_only= []
codex_only= []
```

- [ ] **Step 5: Align provider-native metadata**

Run:

```bash
rg -n "^model:|^tools:|model_reasoning_effort" .claude/agents .agents/agents .codex/agents
```

Expected:

- Claude worker agents use `model: sonnet 4.6`; supervisor uses
  `model: opus 4.8`.
- Claude agent files contain the expected `tools:` line.
- Gemini worker agents use `model: Gemini 3.5 Flash`; supervisor uses
  `model: Gemini 3.1 Pro`.
- Codex worker agents use `model = "gpt-5.3-codex"`; supervisor uses
  `model = "gpt-5.5"`.
- Codex `model_reasoning_effort` is `xhigh`, `high`, or `medium` according to
  the model policy.

- [ ] **Step 6: Align hook wiring descriptions**

Review `.claude/settings.json`, `.codex/hooks.json`, and `.agents/hooks.json`.
Keep these properties:

- All three point to shared scripts under
  `docs/00.agent-governance/hooks/*.sh`.
- Claude settings retain `permissions.allow` and `permissions.deny`.
- Codex and Gemini hook JSON files do not gain Claude-style permissions.
- Hook commands use provider project-dir fallbacks already present in the JSON.

Expected: `jq empty` succeeds and the repo-quality gate hook simulation passes.

- [ ] **Step 7: Update task and progress evidence**

Mark T-003 as completed in the task record. Record agent parity command output,
JSON/TOML parsing, and root shim checks in the task evidence and progress
ledger.

- [ ] **Step 8: Validate T-003**

Run:

```bash
git diff --check
jq empty .agents/hooks.json .claude/settings.json .codex/hooks.json
python3 - <<'PY'
from pathlib import Path
import tomllib
for path in sorted(Path('.codex/agents').glob('*.toml')):
    tomllib.loads(path.read_text())
PY
bash scripts/validate-repo-quality-gates.sh .
```

Expected:

```text
[PASS] repository quality gates passed
```

- [ ] **Step 9: Commit T-003**

Run:

```bash
git add AGENTS.md CLAUDE.md GEMINI.md .agents .claude .codex docs/04.execution/tasks/2026-07-04-agent-governance-contract-normalization.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(adapters): Align provider agent surfaces"
```

Expected: one commit containing provider adapter alignment and evidence only.

### Task 4: GitHub, QA, CI/CD, and Protected-Surface Enforcement

**Files:**

- Modify: `.github/ABOUT.md`
- Modify: `.github/PULL_REQUEST_TEMPLATE.md`
- Modify: `.github/SECURITY.md`
- Modify: `.github/workflows/ci.yml`
- Modify: `docs/00.agent-governance/rules/quality-standards.md`
- Modify: `docs/00.agent-governance/rules/approval-boundaries.md`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `docs/04.execution/tasks/2026-07-04-agent-governance-contract-normalization.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [ ] **Step 1: Reconfirm GitHub-native Markdown boundary**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
for path in [Path('.github/ABOUT.md'), Path('.github/PULL_REQUEST_TEMPLATE.md'), Path('.github/SECURITY.md')]:
    text = path.read_text()
    print(path, text.startswith('---\\n'))
PY
```

Expected:

```text
.github/ABOUT.md False
.github/PULL_REQUEST_TEMPLATE.md False
.github/SECURITY.md False
```

- [ ] **Step 2: Align `.github/ABOUT.md`**

Ensure `.github/ABOUT.md` says:

- `.github` is a map and routing surface, not the policy source of truth.
- `ci.yml` owns branch-policy, repo-quality-static, manifest-static, and
  ci-summary gates.
- GitHub automation does not deploy, mutate Kubernetes, mutate Vault, publish
  containers, or push commits.
- Durable agent-governance policy routes to `docs/00.agent-governance/**`.

Expected: no workflow row claims deployment CD.

- [ ] **Step 3: Align PR template**

Ensure `.github/PULL_REQUEST_TEMPLATE.md` keeps:

- The approved branch prefix list matching `.github/workflows/ci.yml`.
- The exact coverage phrase `90% target for future testable application code`.
- Harness impact options for `.github/workflows/**`, `docs/00.agent-governance/**`,
  scripts, secrets, and live runtime evidence.
- The static validation command block with `bash scripts/validate-harness.sh`
  and `bash infrastructure/tests/verify-contracts-static.sh`.

Expected: the repository quality gate accepts the PR template.

- [ ] **Step 4: Align security policy**

Review `.github/SECURITY.md` against the protected-surface contract. Keep it
GitHub-renderable and frontmatter-free. Add concise routing to
`docs/00.agent-governance/rules/approval-boundaries.md` if the file does not
already direct secret-handling and vulnerability reporting away from public
issues.

Expected: security policy remains short and does not duplicate the approval
matrix.

- [ ] **Step 5: Align workflow and quality-standard wording**

Review `.github/workflows/ci.yml`,
`docs/00.agent-governance/rules/quality-standards.md`, and
`docs/00.agent-governance/rules/approval-boundaries.md` for these invariants:

- CI is provider-agnostic.
- GitHub Actions is the remote QA gate, not live deployment CD.
- Repo-static, CI/toolchain, and live runtime evidence stay separate.
- Permission expansion, live mutation, and secret value access remain protected
  surfaces.

Expected: branch-policy and path filters remain unchanged unless a drift is
found and documented in the task evidence.

- [ ] **Step 6: Add deterministic validator coverage for recurring drift**

Edit `scripts/validate-repo-quality-gates.sh` only for deterministic checks
that can be expressed without network, live cluster, or secret access. Approved
check classes for this task are:

- GitHub-native Markdown remains frontmatter-free.
- Provider role files remain provider-native.
- Hook JSON files parse and include shared hook script paths.
- Root shims retain required canonical links.
- PR template retains branch-prefix and coverage wording.

Expected: no heavyweight dependency or network-dependent CI gate is added.

- [ ] **Step 7: Smoke test validator changes when the validator changed**

If `scripts/validate-repo-quality-gates.sh` changed in Step 6, run:

```bash
bash -n scripts/validate-repo-quality-gates.sh
bash scripts/validate-repo-quality-gates.sh .
```

Expected:

```text
[PASS] repository quality gates passed
```

If the validator did not change, record in the task evidence:

```text
Validator logic unchanged; existing repository quality gate coverage used.
```

- [ ] **Step 8: Validate GitHub workflow YAML**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
import yaml
for path in sorted(Path('.github/workflows').glob('*.yml')):
    yaml.safe_load(path.read_text())
print('workflow-yaml-ok')
PY
```

Expected:

```text
workflow-yaml-ok
```

- [ ] **Step 9: Update task and progress evidence**

Mark T-004 as completed in the task record. Record frontmatter-free GitHub
Markdown check, workflow YAML parse, validator status, and repo-quality gate
evidence in the progress ledger.

- [ ] **Step 10: Validate T-004**

Run:

```bash
git diff --check
jq empty .agents/hooks.json .claude/settings.json .codex/hooks.json
bash scripts/validate-repo-quality-gates.sh .
```

Expected:

```text
[PASS] repository quality gates passed
```

- [ ] **Step 11: Commit T-004**

Run:

```bash
git add .github docs/00.agent-governance/rules/quality-standards.md docs/00.agent-governance/rules/approval-boundaries.md scripts/validate-repo-quality-gates.sh docs/04.execution/tasks/2026-07-04-agent-governance-contract-normalization.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(ci): Align agent governance validation gates"
```

Expected: one commit containing GitHub/QA/CI/protected-surface alignment and
evidence only.

### Task 5: Final Validation and Handoff Closure

**Files:**

- Modify: `docs/04.execution/plans/2026-07-04-agent-governance-contract-normalization.md`
- Modify: `docs/04.execution/tasks/2026-07-04-agent-governance-contract-normalization.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [ ] **Step 1: Run final validation bundle**

Run:

```bash
git diff --check
jq empty .agents/hooks.json .claude/settings.json .codex/hooks.json
bash -n scripts/validate-repo-quality-gates.sh
bash scripts/validate-repo-quality-gates.sh .
bash scripts/validate-harness.sh
```

Expected:

```text
[PASS] repository quality gates passed
PASS harness repo-static validation
```

- [ ] **Step 2: Run focused final scans**

Run:

```bash
rg -n "docs/superpowers|deprecated owner value|permission gate equivalent|Task tool only|must contain.*tools" AGENTS.md CLAUDE.md GEMINI.md .agents .claude .codex .github docs/00.agent-governance docs/04.execution/plans/2026-07-04-agent-governance-contract-normalization.md docs/04.execution/tasks/2026-07-04-agent-governance-contract-normalization.md
```

Expected: matches are either absent or intentionally classified in historical
progress/task evidence. Active policy text must not claim that Codex/Gemini
hook JSON is a Claude permission gate equivalent or that every provider must
use Claude-style `tools:` frontmatter.

- [ ] **Step 3: Request final review**

Use a reviewer subagent or local review pass to inspect:

- Spec compliance against
  `docs/03.specs/015-agent-governance-contract-normalization/spec.md`.
- Stage 00 canonical owner consistency.
- Provider adapter parity.
- GitHub/QA/CI protected-surface consistency.
- Validation evidence completeness.

Expected: no blocking correctness, scope, safety, or contract issue remains.

- [ ] **Step 4: Close task and plan statuses**

Update:

- Task record status to `done`.
- T-005 status to completed.
- Plan status to `done`.
- `docs/04.execution/plans/README.md` row status to `Done`.
- `docs/04.execution/tasks/README.md` row status to `Done`.
- Progress ledger final entry with final validation commands and review result.

- [ ] **Step 5: Commit T-005**

Run:

```bash
git add docs/04.execution/plans/2026-07-04-agent-governance-contract-normalization.md docs/04.execution/tasks/2026-07-04-agent-governance-contract-normalization.md docs/04.execution/plans/README.md docs/04.execution/tasks/README.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(validation): Close agent governance normalization"
```

Expected: one final evidence/closure commit.

- [ ] **Step 6: Prepare branch completion**

Run:

```bash
git status --short --branch
git log --oneline --decorate --max-count=8
```

Expected: working tree is clean on
`codex/agent-governance-contract-normalization`, with logical commits for spec,
plan, task evidence, governance, adapters, CI/QA, and final validation.

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Diff hygiene | `git diff --check` | No output and exit code 0 |
| VAL-PLN-002 | Parser | Hook JSON parse | `jq empty .agents/hooks.json .claude/settings.json .codex/hooks.json` | Exit code 0 |
| VAL-PLN-003 | Parser | Codex agent TOML parse | `python3 - <<'PY'` block from Task 2 Step 9 | Exit code 0 |
| VAL-PLN-004 | Parser | GitHub workflow YAML parse | `python3 - <<'PY'` block from Task 4 Step 8 | `workflow-yaml-ok` |
| VAL-PLN-005 | Repository | Quality gate | `bash scripts/validate-repo-quality-gates.sh .` | `[PASS] repository quality gates passed` |
| VAL-PLN-006 | Harness | Full repo-static harness bundle | `bash scripts/validate-harness.sh` | `PASS harness repo-static validation` |
| VAL-PLN-007 | Review | Spec and quality review | Reviewer pass after T-004 | No blocking issue |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Provider capability docs changed after prior repository baseline | Medium | Recheck official sources before Stage 00/provider edits and record checked date in task evidence |
| Over-normalizing provider files erases native differences | High | Treat parity as role/scope/guardrail parity and preserve provider-native metadata syntax |
| Validator changes become too broad | Medium | Add only deterministic no-network checks and run `bash -n` plus repo-quality gate |
| Historical progress entries create noisy scans | Low | Classify `docs/00.agent-governance/memory/progress.md` as historical evidence in scan results |
| GitHub Markdown receives frontmatter by mistake | Medium | Keep `.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md`, and `.github/SECURITY.md` frontmatter-free and validate with the existing gate |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Repository static gates in this plan are mandatory
  before handoff.
- **Sandbox / Canary Rollout**: No live rollout is required; this is a
  governance and validation-contract change.
- **Human Approval Gate**: Human approval is required before push, PR creation,
  branch finishing, live runtime checks, direct cluster mutation, secret value
  inspection, or third-party resource mutation.
- **Rollback Trigger**: Any failing repo-quality or harness validation gate
  after a task commit must be fixed in a follow-up commit before proceeding to
  the next task.
- **Prompt / Model Promotion Criteria**: No prompt or model promotion is in
  scope. Model identifiers may be documented only when supported by the
  existing model policy and provider sources.

## Completion Criteria

- [x] T-001 baseline task record and drift inventory completed
- [x] T-002 Stage 00 canonical contract normalization completed
- [x] T-003 provider adapter parity alignment completed
- [x] T-004 GitHub/QA/CI/protected-surface alignment completed
- [x] T-005 final validation and review closure completed
- [x] `git diff --check` passed
- [x] `jq empty .agents/hooks.json .claude/settings.json .codex/hooks.json`
  passed
- [x] `bash scripts/validate-repo-quality-gates.sh .` passed
- [x] `bash scripts/validate-harness.sh` passed or recorded a concrete
  environment limitation
- [x] Progress ledger updated
- [x] Logical commits created for each task unit

## Related Documents

- **Spec**: [../../03.specs/015-agent-governance-contract-normalization/spec.md](../../03.specs/015-agent-governance-contract-normalization/spec.md)
- **Task**: [../tasks/2026-07-04-agent-governance-contract-normalization.md](../tasks/2026-07-04-agent-governance-contract-normalization.md)
- **Governance Hub**: [../../00.agent-governance/README.md](../../00.agent-governance/README.md)
- **Common Governance**: [../../00.agent-governance/common-governance.md](../../00.agent-governance/common-governance.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Subagent Protocol**: [../../00.agent-governance/subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)
- **Approval Boundaries**: [../../00.agent-governance/rules/approval-boundaries.md](../../00.agent-governance/rules/approval-boundaries.md)
- **Plan Template**: [../../99.templates/templates/sdlc/execution/plan.template.md](../../99.templates/templates/sdlc/execution/plan.template.md)
