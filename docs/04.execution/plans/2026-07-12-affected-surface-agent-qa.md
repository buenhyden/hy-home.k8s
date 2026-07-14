---
title: 'Affected Surface and Agent QA Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-14
---

# Affected Surface and Agent QA Implementation Plan

## Overview

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish one affected-path-to-validator contract and one
provider-neutral agent-role evidence contract consumed consistently by local
hooks, pre-commit, CI job selection, shared roles, and provider gateways.

**Architecture:** Stage 00 JSON contracts own path selection and role semantics;
small Python programs validate, select, and execute local lanes. Hooks and CI
consume selector output rather than copying path globs, while provider adapters
retain native syntax and share only responsibility, output, prohibition, stop,
handoff, capability-tier, and evidence meaning.

**Tech Stack:** JSON Schema 2020-12, Python 3.11 standard library, Bash,
pre-commit, GitHub Actions YAML, Markdown/TOML provider adapters, and existing
repository-static validators.

### Global Constraints

- Work only in the isolated worktree for branch `codex/workspace-document-assurance-modernization`.
- Use normalized repository-relative POSIX exact or anchored-regex routes with no first-match precedence.
- Local and CI selection must derive from `docs/00.agent-governance/contracts/validation-surfaces.json`.
- A changed tracked path that matches zero or multiple surfaces is a failure.
- Validation results are exactly `PASS`, `SKIP`, `FAIL`, or `DEFER`; no matching files is `SKIP`, not `PASS`.
- `pre-commit run --all-files` does not prove `commit-msg` or `manual` stages; record them separately.
- Ignored `_workspace/**` children are not changed-path inputs; only `_workspace/README.md` and ignore contracts are tracked surfaces.
- Provider-native syntax and metadata remain distinct; common role semantics must not duplicate provider model IDs, Claude tools, or Codex effort values.
- This Plan owns workflow path detection and job routing only. Spec 032 owns Action identity, permissions, and protected-domain behavior.
- Post-Spec-030 program-created authored documents add an exact fourteen-column
  durable migration-ledger row in their creation commit; never weaken strict
  ledger inventory equality to admit a new path.
- Remote/provider/live availability remains `DEFER` without separately approved evidence.
- Do not inspect secret values or ignored authentication/local-state files.
- Use `apply_patch`, run fixture-first TDD, obtain independent review for protected changes, and commit each Task separately.

---

This Plan implements Spec 031 through execution startup, affected-surface
contracts, local lane integration, CI selector integration, role-semantic
contracts, and provider/gateway closure.

## Context

The current workflow and hooks duplicate path conditions. CI does not fully
cover `_workspace/README.md`, `.gitignore`, `.env.example`, all GitOps and
infrastructure paths, policy, secrets, or Traefik. Current agent validation
checks stems and selected Claude/Codex phrases but does not enforce complete
role semantics across Gemini, Claude, and Codex for all ten roles.

## Goals & In-Scope

- Map every protected or validator-consumed tracked path to local validators,
  CI jobs, protected level, fallback, and evidence lane.
- Drive pre/post-edit and completion validation from the canonical mapping.
- Replace copied GitHub path filters with deterministic selector outputs.
- Enforce shared role semantics across thirty provider adapters.
- Align provider gateways and handoff evidence without overstating runtime use.

## Non-Goals & Out-of-Scope

- Updating Action SHA references, workflow permissions, dependency policy,
  GitOps/Vault/ESO behavior, model assignments, or live state.
- Requiring identical provider metadata or claiming adapter files are consumed
  by a provider runtime.
- Adding new AI-agent roles or changing task-specific behavioral evaluation.

### File and Interface Map

| Unit | Files | Responsibility |
| --- | --- | --- |
| Surface contract | `docs/00.agent-governance/contracts/validation-surfaces.json` and schema | Path routes, validator argv, lanes, jobs, protection, fallback, evidence. |
| Selector and runner | `scripts/validate-affected-surfaces.py`, `scripts/select-affected-surfaces.py`, `scripts/run-validation-lane.py` | Validate mapping, select deterministic IDs/jobs, run approved local argv. |
| Local consumers | shared hooks, three hook configs, `.pre-commit-config.yaml`, QA workflow | Pass changed paths to selector/runner and report exact results. |
| CI consumer | `.github/workflows/ci.yml` | Collect changed paths and expose canonical job-selection outputs. |
| Role contract | `agent-role-semantics.json` and schema | Ten-role provider-neutral semantic owner. |
| Role validator | `scripts/validate-agent-role-semantics.py`, fixture JSON | Validate thirty adapters without redefining native metadata. |
| Gateways/governance | root shims, runtime baselines, provider notes, Stage 00 QA docs | Link canonical contracts and define evidence lanes/handoffs. |

### Affected-Surface Interfaces

```json
{
  "id": "repository-document-contract",
  "routes": [{"kind": "regex", "value": "^docs/.*$"}],
  "validators": ["document-contract", "repository-quality"],
  "ciJobs": ["repo-quality-static"],
  "protectedLevel": "none",
  "evidenceLane": "repo-static"
}
```

```text
select-affected-surfaces.py --root PATH --lane affected|staged|all-files|ci --paths-file FILE --delimiter nul --format json|github-output
run-validation-lane.py --root PATH --lane affected|all-files --paths-file FILE --delimiter nul
```

All machine-produced path transport is NUL-delimited from producer through
selector and runner. Newline-delimited temporary files are not a supported
machine interface; a newline inside a valid tracked filename remains data.

### Role Contract Interface

```text
role id -> responsibilities, outputs, prohibitedActions, stopConditions,
handoffs, capabilityTier, requiredEvidence
```

## Work Breakdown

| Task | Deliverable | Primary validation | Commit |
| --- | --- | --- | --- |
| ASQA-001 | Reciprocal execution chain | Lineage assertion | `docs(execution): start affected surface agent qa` |
| ASQA-002 | Surface contract, selector, fixtures | Selector self-test and coverage check | `feat(qa): define affected-surface validation contract` |
| ASQA-003 | Local runner, hooks, pre-commit | Hook simulations and shell/JSON validation | `refactor(hooks): drive local validation from affected surfaces` |
| ASQA-004 | CI job selector | Local/CI parity fixtures and actionlint | `ci(qa): select jobs from affected-surface registry` |
| ASQA-005 | Ten-role semantic contract | Thirty-adapter semantic self-test | `feat(agents): enforce cross-provider role semantics` |
| ASQA-006 | Gateways, governance, closure | Full QA and independent review | `docs(agents): align provider qa evidence contracts` |

## Verification Plan

| ID | Level | Command | Pass criteria |
| --- | --- | --- | --- |
| VAL-031-001 | Contract | `validate-affected-surfaces.py --self-test` | Positive and negative path/local/CI cases match exact expected IDs. |
| VAL-031-002 | Local | hook simulations and lane runner | Required validators run; no-file and optional-tool semantics are honest. |
| VAL-031-003 | CI | selector fixture and actionlint | CI job set equals registry result for every fixture path set. |
| VAL-031-004 | Agents | `validate-agent-role-semantics.py --self-test` | All semantic-category mutations fail across provider forms. |
| VAL-031-005 | Repository | quality gate and all-files pre-commit | Required checks pass with separate manual/remote limitations. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Registry executes arbitrary shell | High | Store validated argv arrays, reject shell strings/metacharacter expansion, and run without `shell=True`. |
| Push/PR changed-path calculation differs | High | Fixture both event ranges and use NUL-delimited git output. |
| Semantic checks become phrase-only theater | High | Contract each category separately and mutate each role/provider surface in self-tests. |
| Provider metadata ownership is duplicated | High | Exclude model/tool/effort fields from common role contract and retain native validators. |
| Workflow scope crosses into Spec 032 | High | Do not change `uses:`, permissions, protected commands, or manifest behavior. |

### Agent Rollout & Evaluation Gates

- **Offline Eval Gate:** Surface and role fixture suites pass before consumer changes.
- **Sandbox / Canary Rollout:** Local hooks consume the selector before CI path filters are removed.
- **Human Approval Gate:** Required before workflow merge, protected-role changes, remote push, model policy, or live/provider validation.
- **Rollback Trigger:** Unmatched tracked path, local/CI selection disagreement, missing semantic category, or changed protected behavior.
- **Prompt / Model Promotion Criteria:** No model promotion is performed; current provider mappings stay canonical.

---

### Task 1: Start Reciprocal Execution Lineage

**Files:**

- Modify: `docs/03.specs/031-affected-surface-agent-qa/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/2026-07-12-affected-surface-agent-qa.md`
- Modify: `docs/04.execution/plans/README.md`
- Create: `docs/04.execution/tasks/2026-07-12-affected-surface-agent-qa.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md`

**Interfaces:**

- Consumes: strict Spec 029/030 document validation and this Plan.
- Produces: Task IDs `ASQA-001` through `ASQA-006`, reciprocal execution
  lineage, and the new Task's exact durable-ledger row.

- [ ] **Step 1: Run RED lineage assertion**

```bash
python3 - <<'PY'
from pathlib import Path
paths = [Path('docs/03.specs/031-affected-surface-agent-qa/spec.md'), Path('docs/04.execution/plans/2026-07-12-affected-surface-agent-qa.md'), Path('docs/04.execution/tasks/2026-07-12-affected-surface-agent-qa.md')]
assert all(path.exists() for path in paths), paths
for source in paths:
    text = source.read_text(encoding='utf-8')
    for target in paths:
        if target != source:
            assert target.name in text, (source, target)
PY
```

Expected: FAIL because Task and reciprocal links are absent.

- [ ] **Step 2: Create active Task and six exact rows**

Use the canonical Task profile and rows `ASQA-001` through `ASQA-006` from the
Work Breakdown table, including exact validation commands and commit messages.
In the same change, add the program-created Task's fourteen-column ledger row
with its computed active owner key, self destination, Spec/Plan lineage,
official Spec Kit and NIST SSDF applicability, independent reviewer, and
`execution-lineage-active` result.

- [ ] **Step 3: Add reciprocal links and active index rows**

Update only Spec, Plan, Task, and their Stage indexes. Preserve unrelated rows.

- [ ] **Step 4: Run GREEN lineage, focused QA, and commit**

```bash
python3 - <<'PY'
from pathlib import Path
paths = [Path('docs/03.specs/031-affected-surface-agent-qa/spec.md'), Path('docs/04.execution/plans/2026-07-12-affected-surface-agent-qa.md'), Path('docs/04.execution/tasks/2026-07-12-affected-surface-agent-qa.md')]
for source in paths:
    text = source.read_text(encoding='utf-8')
    assert source.exists()
    for target in paths:
        if target != source:
            assert target.name in text
PY
git diff --check
pre-commit run --files docs/03.specs/031-affected-surface-agent-qa/spec.md docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-12-affected-surface-agent-qa.md docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-12-affected-surface-agent-qa.md docs/04.execution/tasks/README.md \
  docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md
git add docs/03.specs/031-affected-surface-agent-qa/spec.md docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-12-affected-surface-agent-qa.md docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-12-affected-surface-agent-qa.md docs/04.execution/tasks/README.md \
  docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md
python3 - <<'PY'
import subprocess
expected = {
    'docs/03.specs/031-affected-surface-agent-qa/spec.md',
    'docs/03.specs/README.md',
    'docs/04.execution/plans/2026-07-12-affected-surface-agent-qa.md',
    'docs/04.execution/plans/README.md',
    'docs/04.execution/tasks/2026-07-12-affected-surface-agent-qa.md',
    'docs/04.execution/tasks/README.md',
    'docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md',
}
staged = {
    item.decode()
    for item in subprocess.check_output(
        ['git', 'diff', '--cached', '--name-only', '-z']
    ).split(b'\0')
    if item
}
unstaged = subprocess.check_output(['git', 'diff', '--name-only', '-z'])
assert staged == expected, (sorted(staged), sorted(expected))
assert unstaged == b'', unstaged
PY
git commit -m "docs(execution): start affected surface agent qa"
```

Expected: assertion/hooks PASS and commit succeeds.

---

### Task 2: Define the Affected-Surface Contract and Selector

**Files:**

- Create: `docs/00.agent-governance/contracts/validation-surfaces.json`
- Create: `docs/00.agent-governance/contracts/validation-surfaces.schema.json`
- Create: `scripts/validate-affected-surfaces.py`
- Create: `scripts/select-affected-surfaces.py`
- Create: `tests/fixtures/validation-surfaces.json`
- Modify: `docs/00.agent-governance/harness-implementation-map.md`
- Modify: `scripts/README.md`
- Modify: `tests/README.md`

**Interfaces:**

- Consumes: existing validator commands and Spec 026 normalized path semantics.
- Produces: validated surface records and deterministic JSON/GitHub output.

- [ ] **Step 1: Add exact fixture paths and expected selection**

Cover `_workspace/README.md`, `.gitignore`, `.env.example`, root provider shims,
`docs/00.agent-governance/**`, `docs/99.templates/**`, `.agents/**`,
`.claude/**`, `.codex/**`, `.github/**`, `gitops/**`, `infrastructure/**`,
`policy/**`, `scripts/**`, `secrets/**`, `tests/**`, and `traefik/**`.
Add negative cases for `../x`, `./README.md`, case aliases, ambiguous routes,
and unmatched tracked paths.

- [ ] **Step 2: Add schema and validator shell, then run RED**

Initially parse JSON and return an empty selected set.

```bash
python3 scripts/validate-affected-surfaces.py --self-test
```

Expected: exit 1 because required path cases do not select their expected validators/jobs and malformed paths are not rejected.

- [ ] **Step 3: Implement route validation and selection**

```python
def match_route(path: str, route: dict[str, str]) -> bool:
    if route['kind'] == 'exact':
        return path == route['value']
    if route['kind'] == 'regex':
        pattern = route['value']
        if not pattern.startswith('^') or not pattern.endswith('$'):
            raise ContractError('SURFACE-REGEX-ANCHOR', pattern)
        return re.fullmatch(pattern[1:-1], path) is not None
    raise ContractError('SURFACE-ROUTE-KIND', route['kind'])
```

Require exactly one matching surface per tracked input path. Validate validator
IDs, argv arrays, lane names, CI job IDs, protected level, fallback, and evidence lane.

- [ ] **Step 4: Implement output formats**

JSON output contains sorted `validators`, `ciJobs`, maximum `protectedLevel`,
and `unmatchedPaths`. GitHub output emits one lowercase boolean per declared CI
job. The selector splits input only on NUL and never reserializes paths through
newline text, so embedded newline/control bytes cannot change record boundaries.

- [ ] **Step 5: Run GREEN tests and repository coverage**

```bash
python3 scripts/validate-affected-surfaces.py --self-test
python3 scripts/validate-affected-surfaces.py --root .
python3 -m py_compile scripts/validate-affected-surfaces.py scripts/select-affected-surfaces.py
```

Expected: fixture and actual registry validation PASS with zero uncovered validator-consumed paths.

- [ ] **Step 6: Update inventories and commit**

```bash
git diff --check
pre-commit run --files docs/00.agent-governance/contracts/validation-surfaces.json \
  docs/00.agent-governance/contracts/validation-surfaces.schema.json \
  scripts/validate-affected-surfaces.py scripts/select-affected-surfaces.py \
  tests/fixtures/validation-surfaces.json docs/00.agent-governance/harness-implementation-map.md \
  scripts/README.md tests/README.md
git add docs/00.agent-governance/contracts scripts/validate-affected-surfaces.py \
  scripts/select-affected-surfaces.py tests/fixtures/validation-surfaces.json \
  docs/00.agent-governance/harness-implementation-map.md scripts/README.md tests/README.md \
  docs/04.execution/tasks/2026-07-12-affected-surface-agent-qa.md
git commit -m "feat(qa): define affected-surface validation contract"
```

---

### Task 3: Drive Local Hooks and Pre-commit from the Contract

**Files:**

- Create: `scripts/run-validation-lane.py`
- Modify: `docs/00.agent-governance/hooks/k8s-pre-edit.sh`
- Modify: `docs/00.agent-governance/hooks/post-validate.sh`
- Modify: `docs/00.agent-governance/hooks/lifecycle-guard.sh`
- Modify: `.pre-commit-config.yaml`
- Modify: `.claude/settings.json`
- Modify: `.agents/hooks.json`
- Modify: `.codex/hooks.json`
- Modify: `.agents/workflows/qa-cicd-workflow.md`
- Modify: fixture and script/test inventories

**Interfaces:**

- Consumes: selector JSON and validated argv arrays.
- Produces: affected/all-files local runner and honest PASS/SKIP/FAIL/DEFER lines.

- [ ] **Step 1: Add hook simulation cases and run RED**

Add expected selections for `_workspace/README.md`, `.gitignore`,
`policy/conftest/kubernetes.rego`, `.agents/agents/network-reviewer.md`, and a
no-files event.

```bash
python3 scripts/validate-affected-surfaces.py --self-test
```

Expected: exit 1 until hook-consumer cases are represented.

- [ ] **Step 2: Implement safe argv execution**

```python
completed = subprocess.run(
    command_argv,
    cwd=root,
    text=True,
    capture_output=True,
    shell=False,
)
```

Never execute `remote/live`; emit `DEFER`. Emit `SKIP` for no matching files or
missing optional tool and report fallback separately.

- [ ] **Step 3: Replace hook path cases with selector/runner calls**

Retain provider event payload extraction, secret redaction, and existing
protected-domain messages. Write every extracted path as one NUL-terminated
record to a temporary `.nul` file and invoke selector/runner with
`--delimiter nul`. Do not pass the records through shell command substitution,
line iteration, or a newline temporary file.

- [ ] **Step 4: Add local pre-commit contract hooks**

Add local `language: system`, `pass_filenames: false`, `always_run: true` hooks
for affected-surface contract and strict repository-quality entrypoints. Keep
`commit-msg` stage separate from pre-commit/all-files evidence.

- [ ] **Step 5: Run GREEN local checks**

```bash
python3 scripts/validate-affected-surfaces.py --self-test
python3 -m py_compile scripts/run-validation-lane.py
bash -n docs/00.agent-governance/hooks/*.sh
python3 -m json.tool .claude/settings.json >/dev/null
python3 -m json.tool .agents/hooks.json >/dev/null
python3 -m json.tool .codex/hooks.json >/dev/null
pre-commit run validate-affected-surfaces --all-files
```

Expected: all checks PASS and no-file fixture reports SKIP.

- [ ] **Step 6: Commit**

```bash
git add scripts/run-validation-lane.py docs/00.agent-governance/hooks .pre-commit-config.yaml \
  .claude/settings.json .agents/hooks.json .codex/hooks.json \
  .agents/workflows/qa-cicd-workflow.md tests/fixtures/validation-surfaces.json \
  scripts/README.md tests/README.md docs/04.execution/tasks/2026-07-12-affected-surface-agent-qa.md
git commit -m "refactor(hooks): drive local validation from affected surfaces"
```

---

### Task 4: Select CI Jobs from the Canonical Contract

**Files:**

- Modify: `.github/workflows/ci.yml`
- Modify: `tests/fixtures/validation-surfaces.json`
- Modify: `scripts/validate-affected-surfaces.py`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `docs/00.agent-governance/harness-implementation-map.md`
- Modify: `docs/90.references/data/tech-stack-version-inventory.md`
- Modify: same-topic Task
- Modify: this Plan

**Interfaces:**

- Consumes: NUL-delimited `git diff --name-only -z` and selector GitHub output.
- Produces: `precommit`, `repo_quality`, and `manifests` outputs for existing jobs.

- [ ] **Step 1: Add durable push and pull-request range fixtures and workflow
  parity validation, then run RED**

Fixture expected job sets must cover root docs, `_workspace/README.md`, policy,
GitOps, infrastructure, secrets, Traefik, agent, template, and workflow changes.
The fixture and validator must compare both selected job IDs and exact GitHub
boolean outputs. Push coverage includes ordinary `before..head` and initial or
zero-`before` head-tree selection; pull-request coverage uses `base..head`.

```bash
python3 scripts/validate-affected-surfaces.py --self-test
```

Expected: `SURFACE-LOCAL-CI-MISMATCH` until CI selection matches the registry.

- [ ] **Step 2: Replace copied workflow filters**

Keep current jobs and every Action reference except the obsolete copied-filter
owner removed in Step 3. In `changes`, checkout sufficient history, write
`git diff --name-only -z` directly to
`$RUNNER_TEMP/changed-paths.nul`, pass that same file to the selector with
`--delimiter nul`, and append only the selector's boolean job outputs to
`$GITHUB_OUTPUT`. No intermediate command may decode or newline-join paths.

- [ ] **Step 3: Preserve ownership boundary**

Remove only the obsolete `dorny/paths-filter@v4.0.1` copied-filter owner and
its inventory row. Do not add or change any other `uses:` reference, workflow/
job `permissions`, manifest-static command, or protected-domain step. Keep
`ci-summary` aggregation unchanged. Replace legacy quality-gate path-glob
assertions with canonical selector, NUL transport, output-wiring, self-test,
root coverage, and no-dorny assertions.

- [ ] **Step 4: Run GREEN CI-static checks**

```bash
python3 scripts/validate-affected-surfaces.py --self-test
python3 scripts/validate-affected-surfaces.py --root .
bash scripts/validate-repo-quality-gates.sh .
pre-commit run actionlint --files .github/workflows/ci.yml
pre-commit run zizmor --files .github/workflows/ci.yml
```

Expected: selector parity and actionlint PASS; zizmor findings outside selector ownership remain assigned to Spec 032.

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/ci.yml tests/fixtures/validation-surfaces.json \
  scripts/validate-affected-surfaces.py \
  scripts/validate-repo-quality-gates.sh \
  docs/00.agent-governance/harness-implementation-map.md \
  docs/90.references/data/tech-stack-version-inventory.md \
  docs/04.execution/tasks/2026-07-12-affected-surface-agent-qa.md \
  docs/04.execution/plans/2026-07-12-affected-surface-agent-qa.md
git commit -m "ci(qa): select jobs from affected-surface registry"
```

---

### Task 5: Enforce Ten-Role Cross-Provider Semantics

**Files:**

- Create: `docs/00.agent-governance/contracts/agent-role-semantics.json`
- Create: `docs/00.agent-governance/contracts/agent-role-semantics.schema.json`
- Create: `scripts/validate-agent-role-semantics.py`
- Create: `tests/fixtures/agent-role-semantics.json`
- Modify: ten role stems under `.agents/agents/*.md`
- Modify: ten matching role stems under `.claude/agents/*.md`
- Modify: ten matching role stems under `.codex/agents/*.toml`
- Modify: script/test inventories and same-topic Task

**Interfaces:**

- Consumes: provider-native bodies and canonical model policy without copying model metadata.
- Produces: category-specific semantic diagnostics for thirty adapters.

- [ ] **Step 1: Define ten role records and mutation fixtures**

Roles are exactly `supervisor`, `code-reviewer`, `doc-writer`,
`gitops-reviewer`, `incident-responder`, `k8s-implementer`,
`network-reviewer`, `observability-reviewer`, `security-auditor`, and
`wiki-curator`. For every role/provider, fixtures remove or replace one
responsibility, output, prohibition, stop, handoff, capability tier, or evidence
anchor and name the exact expected rule ID.

- [ ] **Step 2: Add validator shell and run RED**

```bash
python3 scripts/validate-agent-role-semantics.py --self-test
```

Expected: exit 1 for unimplemented `ROLE-RESPONSIBILITY`, `ROLE-OUTPUT`,
`ROLE-PROHIBITED`, `ROLE-STOP`, `ROLE-HANDOFF`, `ROLE-CAPABILITY-TIER`,
`ROLE-EVIDENCE`, and `ROLE-PROVIDER-STEM` cases.

- [ ] **Step 3: Parse provider-native bodies**

Use YAML Frontmatter plus Markdown body for `.agents`/`.claude`; use `tomllib`
and `developer_instructions` for Codex. Normalize whitespace only; retain exact
scope import targets and provider metadata validation in existing owners.

- [ ] **Step 4: Align role bodies with the common contract**

Add missing semantic content to the owning section in all provider forms.
Do not change model, reasoning effort, or native tool metadata. Make the
smallest topic-specific edit needed for each failed category.

- [ ] **Step 5: Run GREEN role validation**

```bash
python3 scripts/validate-agent-role-semantics.py --self-test
python3 scripts/validate-agent-role-semantics.py --root .
python3 scripts/validate-agent-roster-currentness.py . --self-test
python3 scripts/validate-agent-roster-currentness.py .
```

Expected: semantic fixtures, thirty adapters, and roster currentness PASS.

- [ ] **Step 6: Commit**

```bash
git add docs/00.agent-governance/contracts/agent-role-semantics.json \
  docs/00.agent-governance/contracts/agent-role-semantics.schema.json \
  scripts/validate-agent-role-semantics.py tests/fixtures/agent-role-semantics.json \
  .agents/agents .claude/agents .codex/agents scripts/README.md tests/README.md \
  docs/04.execution/tasks/2026-07-12-affected-surface-agent-qa.md
git commit -m "feat(agents): enforce cross-provider role semantics"
```

---

### Task 6: Align Gateways, Governance, and Completion Evidence

**Files:**

- Modify: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`
- Modify: `.agents/GEMINI.md`, `.claude/CLAUDE.md`, `.codex/CODEX.md`
- Modify: `docs/00.agent-governance/subagent-protocol.md`
- Modify: `docs/00.agent-governance/rules/postflight-checklist.md`
- Modify: `docs/00.agent-governance/rules/quality-standards.md`
- Modify: four files under `docs/00.agent-governance/providers/`
- Modify: `docs/00.agent-governance/harness-catalog.md`
- Modify: `docs/00.agent-governance/harness-implementation-map.md`
- Modify: `scripts/validate-repo-quality-gates.sh`, script/test READMEs
- Modify: Spec 031, this Plan, same-topic Task, indexes, and `memory/progress.md`

**Interfaces:**

- Consumes: canonical surface and role contracts plus all prior Task evidence.
- Produces: thin gateway pointers, provider-neutral QA handoff semantics, and completed Spec 031 evidence.

- [x] **Step 1: Run RED governance search**

```bash
rg -n 'pre-commit run --all-files|commit-msg|manual|PASS|SKIP|FAIL|DEFER|validation-surfaces|agent-role-semantics' \
  AGENTS.md CLAUDE.md GEMINI.md .agents/GEMINI.md .claude/CLAUDE.md .codex/CODEX.md \
  docs/00.agent-governance
```

Expected: output shows incomplete lane/result/contract coverage and duplicated command wording.

Observed on 2026-07-14: exit `0`, 1,009 matching lines. The broad result showed
lane/result terms and copied command wording distributed across gateways,
provider baselines, Stage 00, and historical progress evidence; it was the RED
inventory, not a completion result.

- [x] **Step 2: Update canonical governance owners**

Define affected, staged, all-files, message/manual, CI, and remote/live lanes in
Stage 00. Define the handoff evidence fields: scope, changed paths, acceptance
IDs, commands, tool/version, PASS/SKIP/FAIL/DEFER, limitations, reviewer,
rollback, residual risk, and next owner.

- [x] **Step 3: Keep root/provider gateways thin**

Add only links to canonical contract/QA owners. Remove copied full command or
path tables from gateways. State that static adapter presence is not native
runtime-consumption evidence.

- [x] **Step 4: Integrate focused validators into repository quality**

Invoke `validate-affected-surfaces.py` and `validate-agent-role-semantics.py`;
remove superseded hardcoded path/semantic checks while retaining provider-native
metadata and roster-currentness validation.

- [x] **Step 5: Run full GREEN bundle**

```bash
python3 scripts/validate-affected-surfaces.py --self-test
python3 scripts/validate-affected-surfaces.py --root .
python3 scripts/validate-agent-role-semantics.py --self-test
python3 scripts/validate-agent-role-semantics.py --root .
python3 scripts/validate-agent-roster-currentness.py . --self-test
python3 scripts/validate-agent-roster-currentness.py .
find infrastructure scripts docs/00.agent-governance/hooks -type f -name '*.sh' -exec bash -n {} +
bash scripts/validate-repo-quality-gates.sh .
git diff --check
pre-commit run --all-files
```

Expected: all required checks PASS; message/manual, remote/provider, and live lanes are reported separately rather than inferred.

- [x] **Step 6: Close evidence and lifecycle**

Record independent reviewer identity, protected-change findings, commands,
results, limitations, rollback commits, and residual risks in the Task. Set
Spec, Plan, and Task to `done`, update indexes, and append the reusable contract
handoff to `memory/progress.md`.

Independent reviewer agent `/root/review_adm006_adm007_conflict` approved
lifecycle closure with disposition `APPROVED FOR LIFECYCLE CLOSURE
(C0/H0/M0/L0)`. The ignored evidence package is
`.superpowers/sdd/asqa006-provisional-review.md`; the tracked Task and progress
ledger record its identity, result, lane boundaries, rollback unit, residual
risk, and Spec 032 handoff.

- [ ] **Step 7: Commit (controller action after this lifecycle staging proof)**

```bash
git add AGENTS.md CLAUDE.md GEMINI.md .agents/GEMINI.md .claude/CLAUDE.md .codex/CODEX.md \
  docs/00.agent-governance scripts/validate-repo-quality-gates.sh scripts/README.md tests/README.md \
  docs/03.specs/031-affected-surface-agent-qa/spec.md docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-12-affected-surface-agent-qa.md docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-12-affected-surface-agent-qa.md docs/04.execution/tasks/README.md
git commit -m "docs(agents): align provider qa evidence contracts"
```

## Completion Criteria

- [x] Every protected and validator-consumed tracked path has deterministic local and CI selection coverage.
- [x] Local hooks, pre-commit, and CI consume the canonical surface contract.
- [x] Thirty provider adapters satisfy all shared semantic categories without common model/tool metadata duplication.
- [x] PASS/SKIP/FAIL/DEFER and all validation lanes are documented and evidenced without overclaim.
- [x] Action identity, permissions, and protected behavior remain assigned to Spec 032.

## Traceability

- [Program PRD](../../01.requirements/005-workspace-document-assurance-modernization.md)
- [Operating Model ARD](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- [Affected Surface and Agent QA Spec](../../03.specs/031-affected-surface-agent-qa/spec.md)
- [Affected Surface and Agent QA Task](../tasks/2026-07-12-affected-surface-agent-qa.md)
- [Authored Migration Plan](./2026-07-12-authored-document-migration.md)
- [Protected Surface Spec](../../03.specs/032-protected-surface-supply-chain-hardening/spec.md)
