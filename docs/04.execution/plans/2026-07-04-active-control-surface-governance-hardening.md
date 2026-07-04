---
title: 'Active Control Surface Governance Hardening Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-04
---

# Active Control Surface Governance Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Harden active GitHub, CI/CD, QA, GitOps, infrastructure, policy,
test, Traefik, and sample-app control surfaces while keeping AWS/Azure cloud
examples as dated snapshots.

**Architecture:** This plan follows a contract-first sequence. First create
task evidence and baseline inventory, then normalize canonical support and
governance contracts, then align GitHub/CI/QA surfaces, then align GitOps and
repo-static validation surfaces, and finally close evidence with full harness
validation.

**Tech Stack:** Markdown governance and README files, GitHub Actions YAML,
Kubernetes and Argo CD manifests, Bash/Python validation scripts, Rego policy,
and repo-static harness validation.

---

## Overview

This document defines the implementation plan for
`docs/03.specs/016-active-control-surface-governance-hardening/spec.md`. The
plan intentionally does not promote `examples/aws/docs` or
`examples/azure/docs` into active SDLC documents. It strengthens the active
control surfaces that route to, validate, or protect those snapshot examples.

The implementation must keep README files as frontmatter-free entrypoints and
must keep GitHub-native Markdown files frontmatter-free. Durable policy belongs
in Stage 00 governance, Stage 99 support contracts, Stage 05 operations
documents, workflow files, or validators according to ownership.

## Context

Current validation already passes:

- `git diff --check`
- `bash scripts/validate-repo-quality-gates.sh .`
- `bash scripts/validate-harness.sh`

The current repository contract has several strong foundations:

- `scripts/validate-repo-quality-gates.sh` enforces README section profiles,
  frontmatter bans, GitHub control-surface boundaries, script inventory,
  GitOps matrices, policy fallback, and provider adapter rules.
- `scripts/validate-harness.sh` wraps the repo-static quality, GitOps,
  manifest, secret, policy, infrastructure, and diff hygiene gates.
- `examples/README.md` already classifies `aws/` and `azure/` as Cloud Example
  Snapshot material, not live provider-latest guidance.
- GitHub Actions, GitOps, Kubernetes, Argo CD, Argo Rollouts, ESO,
  OPA/Conftest, and KubeLinter official documentation provide the external
  basis for active CI/CD and QA claims.

## Goals & In-Scope

- **Goals**:
  - Capture baseline evidence for active control surfaces and snapshot
    boundaries.
  - Normalize support and governance contracts around active control surfaces,
    README routing, GitHub-native Markdown, and Cloud Example Snapshot rules.
  - Align `.github` control files, CI workflow, PR template, security policy,
    Dependabot, and QA wording with the canonical contracts.
  - Align `scripts`, `gitops`, `infrastructure`, `policy`, `tests`,
    `traefik`, and `examples/sample-app` README/validation surfaces with
    official-source-backed boundaries.
  - Add deterministic validator checks only where the repository can enforce a
    rule without live cluster, cloud, Vault, or GitHub mutation.
- **In Scope**:
  - `.github/**`
  - `examples/README.md`
  - `examples/sample-app/**`
  - `gitops/**`
  - `infrastructure/**`
  - `policy/**`
  - `scripts/**`
  - `tests/**`
  - `traefik/**`
  - `docs/00.agent-governance/**` when active-control rules need canonical
    governance wording.
  - `docs/99.templates/support/**` when README, GitHub-native Markdown, or
    common/SDLC boundary rules need template contract wording.
  - `docs/04.execution/plans/**`, `docs/04.execution/tasks/**`, and
    `docs/00.agent-governance/memory/progress.md` for evidence.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Rewrite all AWS/Azure cloud example SDLC documents to active
    frontmatter/section contracts.
  - Change live Kubernetes, Argo CD, Vault, ESO, cloud, DNS, certificate, or
    GitHub settings.
  - Replace the current Stage 00 through Stage 99 docs taxonomy.
  - Replace the current CI workflow architecture.
- **Out of Scope**:
  - Secret value inspection or certificate regeneration.
  - Remote push, PR creation, merge, publish, or third-party mutation.
  - Live cluster validation beyond documenting operator-owned commands.
  - Provider-latest AWS/Azure guidance refresh.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| ACS-001 | Create task record and baseline active/snapshot inventory | `docs/04.execution/tasks/2026-07-04-active-control-surface-governance-hardening.md`, `docs/04.execution/tasks/README.md`, `docs/00.agent-governance/memory/progress.md` | VAL-SPC-001, VAL-SPC-002 | Baseline scans captured; repo-quality gate passes |
| ACS-002 | Normalize Stage 99 and Stage 00 active-control contracts | `docs/99.templates/support/*.md`, `docs/00.agent-governance/rules/*.md`, `docs/00.agent-governance/scopes/*.md` as needed | VAL-SPC-001, VAL-SPC-003 | README/GitHub-native/snapshot ownership rules are canonical and non-duplicative |
| ACS-003 | Align GitHub, CI/CD, QA, and protected-surface control files | `.github/**`, `scripts/validate-repo-quality-gates.sh`, `docs/00.agent-governance/rules/quality-standards.md`, `docs/00.agent-governance/rules/git-workflow.md` as needed | VAL-SPC-001, VAL-SPC-003, VAL-SPC-004 | GitHub Markdown remains frontmatter-free; workflow YAML parses; repo-quality gate passes |
| ACS-004 | Align GitOps, infrastructure, policy, scripts, tests, Traefik, and sample-app surfaces | `scripts/README.md`, `gitops/README.md`, `gitops/workloads/README.md`, `infrastructure/README.md`, `policy/**`, `tests/README.md`, `traefik/README.md`, `examples/README.md`, `examples/sample-app/README.md`, validators as needed | VAL-SPC-001, VAL-SPC-002, VAL-SPC-004 | Harness validation passes; optional tool skips remain explicit |
| ACS-005 | Close evidence, review, and branch readiness | Plan, task record, task README, progress ledger | VAL-SPC-005 | Full validation bundle passes; plan/task status updated; no unresolved drift |

## Detailed Tasks

### Task 1: Baseline Inventory and Task Record

**Files:**

- Create: `docs/04.execution/tasks/2026-07-04-active-control-surface-governance-hardening.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/00.agent-governance/memory/progress.md`
- Read: `docs/99.templates/templates/sdlc/execution/task.template.md`
- Read: `docs/03.specs/016-active-control-surface-governance-hardening/spec.md`

- [x] **Step 1: Confirm branch and clean state**

Run:

```bash
git status --short --branch
```

Expected: current branch is
`codex/active-control-surface-governance-hardening` and the worktree is clean
after the plan commit.

- [x] **Step 2: Read the task template**

Run:

```bash
sed -n '1,260p' docs/99.templates/templates/sdlc/execution/task.template.md
```

Expected: output includes `type: sdlc/task`, `## Overview`,
`## Validation Evidence`, and `## Related Documents`.

- [x] **Step 3: Capture active control-surface inventory**

Run:

```bash
rg --files .github examples/sample-app gitops infrastructure policy scripts tests traefik | sort
```

Expected: output lists GitHub control files, sample-app manifests, GitOps
desired state, infrastructure contracts, policy files, validation scripts,
tests README, and Traefik manifests.

- [x] **Step 4: Capture snapshot example document inventory**

Run:

```bash
rg --files examples/aws/docs examples/azure/docs | rg '\.md$' | sort
```

Expected: output lists the AWS/Azure cloud example Markdown documents that
remain snapshot-bounded and are not promoted into active SDLC frontmatter
enforcement.

- [x] **Step 5: Capture active README and GitHub control headings**

Run:

```bash
rg -n "^# |^## " .github examples/README.md examples/sample-app/README.md gitops infrastructure scripts tests traefik -g '*.md'
```

Expected: output shows `.github` control file headings and active README
sections. Classify each file as `GitHub-native control`, `common README`,
`sample onboarding template`, or `snapshot boundary index` in the task record.

- [x] **Step 6: Capture external-source-backed contract candidates**

Run:

```bash
rg -n "GitHub Actions|workflow|CI|QA|GitOps|Argo CD|Argo Rollouts|ExternalSecret|Secret|Kustomize|conftest|kube-linter|Cloud Example Snapshot|provider-latest|live provider" .github examples gitops infrastructure policy scripts tests traefik docs/99.templates/support docs/00.agent-governance/rules
```

Expected: output identifies active claims and snapshot boundary statements
that may need canonical ownership or validator reinforcement.

- [x] **Step 7: Create the task record**

Create `docs/04.execution/tasks/2026-07-04-active-control-surface-governance-hardening.md`
from the task template with these values:

```yaml
title: 'Active Control Surface Governance Hardening Task Record'
type: sdlc/task
status: draft
owner: platform
updated: 2026-07-04
```

The task record must include:

- Parent Plan:
  `../plans/2026-07-04-active-control-surface-governance-hardening.md`
- Parent Spec:
  `../../03.specs/016-active-control-surface-governance-hardening/spec.md`
- Task IDs `ACS-001` through `ACS-005`.
- Initial `ACS-001` status: `in-progress`.
- Baseline inventory evidence from Steps 3 through 6.
- The approved boundary: AWS/Azure cloud example docs remain dated snapshots.

- [x] **Step 8: Update the Stage 04 tasks README**

Add the new task record to `docs/04.execution/tasks/README.md` with:

- Status: `Draft`
- Final updated date: `2026-07-04`
- Description:
  `Active control surface governance hardening evidence for GitHub, CI/CD, QA, GitOps, infrastructure, policy, scripts, tests, Traefik, and sample-app snapshot boundaries.`

- [x] **Step 9: Update progress ledger**

Append an entry to `docs/00.agent-governance/memory/progress.md` with:

- Date: `2026-07-04`
- Title: `Active control surface hardening baseline`
- Tags: `#governance #ci #qa #gitops #validation`
- Evidence commands from Steps 3 through 6.
- Result: task record created and baseline scope locked.

- [x] **Step 10: Validate and commit ACS-001**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/04.execution/tasks/2026-07-04-active-control-surface-governance-hardening.md docs/04.execution/tasks/README.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(task): Track active control surface hardening evidence"
```

Expected: `git diff --check` prints no output,
`scripts/validate-repo-quality-gates.sh` prints
`[PASS] repository quality gates passed`, and the commit contains only the task
record, tasks README, and progress ledger changes.

### Task 2: Canonical Support and Governance Contracts

**Files:**

- Modify: `docs/99.templates/support/documentation-contract.md`
- Modify: `docs/99.templates/support/template-routing.md`
- Modify: `docs/99.templates/support/frontmatter-schema.md`
- Modify: `docs/99.templates/support/common-documentation-governance.md`
- Modify: `docs/99.templates/support/legacy-cleanup-rules.md`
- Modify: `docs/00.agent-governance/rules/documentation-protocol.md`
- Modify: `docs/00.agent-governance/rules/document-stage-routing.md`
- Modify: `docs/00.agent-governance/rules/quality-standards.md`
- Modify: `docs/00.agent-governance/rules/approval-boundaries.md`
- Modify: `docs/04.execution/tasks/2026-07-04-active-control-surface-governance-hardening.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [x] **Step 1: Inspect current canonical wording**

Run:

```bash
rg -n "README|GitHub-native|frontmatter-free|Cloud Example Snapshot|provider-latest|active control|workflow|CI/CD|QA|protected surface|secret value|live mutation" docs/99.templates/support docs/00.agent-governance/rules
```

Expected: output shows where README, GitHub-native Markdown, snapshot, QA,
CI/CD, and protected-surface rules currently live.

- [x] **Step 2: Normalize template support contract wording**

Edit the support files so they state these contract sentences in the owning
documents without duplicating long bodies:

- `documentation-contract.md`: Active control surfaces include GitHub-native
  Markdown, workflows, validators, GitOps desired state, policy-as-code, and
  route manifests; README files route to canonical owners.
- `template-routing.md`: `.github` control Markdown remains an explicit
  non-routed exception; AWS/Azure cloud example docs remain snapshot material
  unless a future spec promotes them.
- `frontmatter-schema.md`: README and GitHub-native Markdown remain
  frontmatter-free; cloud snapshot docs are not active SDLC frontmatter targets
  unless routed by a future support contract.
- `common-documentation-governance.md`: README files may summarize active
  control boundaries through matrices and links, but detailed rules belong to
  support/governance/operations/validator owners.
- `legacy-cleanup-rules.md`: Provider-latest claims in active cloud example
  indexes are legacy unless backed by a current approved provider refresh.

- [x] **Step 3: Normalize Stage 00 governance wording**

Edit Stage 00 rule files so they state these active-control rules:

- `documentation-protocol.md`: README files are entrypoints and must not hold
  duplicated policy bodies.
- `document-stage-routing.md`: Cloud example snapshot material is not an
  active SDLC route target for wholesale frontmatter migration.
- `quality-standards.md`: CI/CD and QA evidence must distinguish optional-tool
  skips from successful full coverage.
- `approval-boundaries.md`: Live cluster, Vault, cloud, GitHub publish/merge,
  and secret value work require explicit approval.

- [x] **Step 4: Validate canonical ownership scan**

Run:

```bash
rg -n "Cloud Example Snapshot|provider-latest|frontmatter-free|GitHub-native|README files are entrypoints|optional-tool skips|secret value" docs/99.templates/support docs/00.agent-governance/rules
```

Expected: output shows canonical support/governance owners for each phrase.
No README file is the only owner of a durable policy rule.

- [x] **Step 5: Update task evidence**

In `docs/04.execution/tasks/2026-07-04-active-control-surface-governance-hardening.md`,
mark `ACS-002` as `done` and add the Step 4 scan as validation evidence.

- [x] **Step 6: Update progress ledger**

Append a progress entry stating that support and Stage 00 canonical ownership
were normalized for active control surfaces and snapshot boundaries.

- [x] **Step 7: Validate and commit ACS-002**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/99.templates/support/documentation-contract.md docs/99.templates/support/template-routing.md docs/99.templates/support/frontmatter-schema.md docs/99.templates/support/common-documentation-governance.md docs/99.templates/support/legacy-cleanup-rules.md docs/00.agent-governance/rules/documentation-protocol.md docs/00.agent-governance/rules/document-stage-routing.md docs/00.agent-governance/rules/quality-standards.md docs/00.agent-governance/rules/approval-boundaries.md docs/04.execution/tasks/2026-07-04-active-control-surface-governance-hardening.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(governance): Define active control surface boundaries"
```

Expected: repository quality gate passes and the commit contains only
canonical contract, task, and progress evidence changes.

### Task 3: GitHub, CI/CD, QA, and Protected-Surface Alignment

**Files:**

- Modify: `.github/ABOUT.md`
- Modify: `.github/PULL_REQUEST_TEMPLATE.md`
- Modify: `.github/SECURITY.md`
- Modify: `.github/workflows/ci.yml` when workflow metadata or gate wording
  needs alignment.
- Modify: `.github/dependabot.yml` only if the config contradicts documented
  ownership.
- Modify: `.github/zizmor.yml` only if rule ownership wording is stale.
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `docs/04.execution/tasks/2026-07-04-active-control-surface-governance-hardening.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [x] **Step 1: Inspect GitHub control and workflow surfaces**

Run:

```bash
rg -n "frontmatter|policy source of truth|branch-policy|repo-quality|manifest-static|secret|workflow_dispatch|pull_request_target|Dependabot|zizmor|publish|push|merge|Cloud Example Snapshot" .github scripts/validate-repo-quality-gates.sh
```

Expected: output identifies GitHub-native Markdown, workflow gates, protected
actions, and validator checks.

- [x] **Step 2: Keep GitHub-native Markdown frontmatter-free**

Run:

```bash
rg -n "^---$" .github/ABOUT.md .github/PULL_REQUEST_TEMPLATE.md .github/SECURITY.md
```

Expected: no matches. If matches appear, remove YAML frontmatter from those
GitHub-native Markdown files and route metadata to the owning governance file.

- [x] **Step 3: Align `.github/ABOUT.md` routing language**

Edit `.github/ABOUT.md` so it remains a routing hub and includes these
boundaries without adding a new ad hoc section:

- `.github/workflows/ci.yml` owns CI gate execution.
- Stage 00 and Stage 99 own durable governance and template contracts.
- `scripts/validate-repo-quality-gates.sh` owns deterministic repo-static
  drift checks.
- It does not duplicate branch policy, protected surface, or provider-latest
  policy bodies.

- [x] **Step 4: Align PR template checks**

Edit `.github/PULL_REQUEST_TEMPLATE.md` so checklist text routes durable
policy to canonical owners and keeps these review prompts:

- CI and branch-policy checks cannot be bypassed for `main`.
- GitOps, workflow, secrets, and protected surfaces require review evidence.
- Cloud example changes must preserve Cloud Example Snapshot boundaries unless
  an approved provider refresh spec exists.

- [x] **Step 5: Align security policy surface**

Edit `.github/SECURITY.md` only if needed so it stays GitHub-renderable and
frontmatter-free. It should report vulnerability handling boundaries without
duplicating secret-handling or live-mutation governance from Stage 00.

- [x] **Step 6: Add deterministic GitHub validation if missing**

Update `scripts/validate-repo-quality-gates.sh` only for deterministic checks.
The acceptable additions are:

- `.github` Markdown frontmatter ban remains enforced.
- `.github/ABOUT.md` workflow matrix row order matches tracked workflows.
- PR template contains the Cloud Example Snapshot preservation prompt when
  `examples/aws` or `examples/azure` can be touched.
- Workflow files do not contain live publish, push, or mutation commands
  outside approved workflow roles.

- [x] **Step 7: Validate GitHub and CI/CD surfaces**

Run:

```bash
git diff --check
python3 - <<'PY'
import pathlib, yaml
for path in sorted(pathlib.Path('.github/workflows').glob('*.yml')):
    with path.open(encoding='utf-8') as handle:
        yaml.safe_load(handle)
print('workflow yaml parse ok')
PY
bash scripts/validate-repo-quality-gates.sh .
```

Expected:

```text
workflow yaml parse ok
[PASS] repository quality gates passed
```

- [x] **Step 8: Update task and progress evidence**

Mark `ACS-003` as `done` in the task record and append progress evidence with
the commands from Step 7.

- [x] **Step 9: Commit ACS-003**

Run:

```bash
git add .github/ABOUT.md .github/PULL_REQUEST_TEMPLATE.md .github/SECURITY.md .github/workflows/ci.yml .github/dependabot.yml .github/zizmor.yml scripts/validate-repo-quality-gates.sh docs/04.execution/tasks/2026-07-04-active-control-surface-governance-hardening.md docs/00.agent-governance/memory/progress.md
git diff --cached --name-only
git commit -m "docs(ci): Align active GitHub control surfaces"
```

Expected: staged files include only touched GitHub, validator, task, and
progress files. If optional `.github` files were not changed, omit them from
the final `git add` command before committing.

### Task 4: GitOps, Infrastructure, Policy, Scripts, Tests, Traefik, and Sample-App Alignment

**Files:**

- Modify: `scripts/README.md`
- Modify: `gitops/README.md`
- Modify: `gitops/workloads/README.md`
- Modify: `infrastructure/README.md`
- Modify: `tests/README.md`
- Modify: `traefik/README.md`
- Modify: `examples/README.md`
- Modify: `examples/sample-app/README.md`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `scripts/validate-harness.sh` only if wrapper evidence wording is
  stale.
- Modify: `scripts/check-secret-handling.sh` only if active path or fixture
  coverage wording is stale.
- Modify: `scripts/validate-policy-gates.sh` only if policy fallback wording
  is stale.
- Modify: `scripts/validate-k8s-manifests.sh` only if optional
  `kube-linter` wording is stale.
- Modify: `scripts/validate-gitops-structure.sh` only if GitOps hierarchy
  wording is stale.
- Modify: `infrastructure/tests/verify-contracts-static.sh` only if static
  contract wording is stale.
- Modify: `docs/04.execution/tasks/2026-07-04-active-control-surface-governance-hardening.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [x] **Step 1: Inspect active README matrices and validation references**

Run:

```bash
rg -n "## |Validation|validate-|check-secret-handling|repo-quality|GitOps|Secret|ExternalSecret|Argo CD|Argo Rollouts|Kustomize|conftest|kube-linter|Cloud Example Snapshot|not live provider-latest|live mutation|secret values" scripts/README.md gitops/README.md gitops/workloads/README.md infrastructure/README.md tests/README.md traefik/README.md examples/README.md examples/sample-app/README.md
```

Expected: output shows active README sections, validation commands, secret
boundaries, and snapshot boundary wording.

- [x] **Step 2: Keep README profile unchanged**

Run:

```bash
deprecated_related='^## Related '
rg -n "^---$|${deprecated_related}(References|Folders)" scripts/README.md gitops/README.md gitops/workloads/README.md infrastructure/README.md tests/README.md traefik/README.md examples/README.md examples/sample-app/README.md
```

Expected: no YAML frontmatter and no deprecated README related-link headings.
If matches appear, remove frontmatter and replace deprecated headings with the
current `## Related Documents` section.

- [x] **Step 3: Align README routing and boundaries**

Edit active README files with these exact ownership outcomes:

- `scripts/README.md`: script inventory distinguishes Tier A direct CI/hook
  gates, Tier B focused validators, and Tier C manual/documentation surfaces;
  optional-tool skips are named as skips, not full coverage.
- `gitops/README.md`: GitOps desired state remains declarative and
  versioned; active image/kind policy and secret responsibility matrices route
  to validators and operations policy.
- `gitops/workloads/README.md`: new workload onboarding starts from
  `examples/sample-app`, then becomes active only after copied under
  `gitops/workloads/<appname>` and validated.
- `infrastructure/README.md`: bootstrap and live runtime checks stay
  operator-owned; repo-static checks do not create, delete, or repair clusters.
- `tests/README.md`: QA evidence separates repo-static, optional tool, and
  live/operator-owned checks.
- `traefik/README.md`: local route manifests are repo-static route contracts;
  live port availability is operator-owned.
- `examples/README.md`: `sample-app/` is the active onboarding template;
  `aws/` and `azure/` are Cloud Example Snapshot material and not live
  provider-latest guidance.
- `examples/sample-app/README.md`: placeholders must be replaced before
  copying into active GitOps desired state; sample secrets use ESO remoteRef
  key conventions without exposing secret values.

- [x] **Step 4: Add deterministic validator checks for active README drift**

Update `scripts/validate-repo-quality-gates.sh` only for deterministic checks
that can be enforced locally. Acceptable checks are:

- Active README files keep common README sections and no frontmatter.
- `examples/README.md` role matrix still classifies `sample-app/`, `aws/`,
  and `azure/` correctly.
- `examples/sample-app/README.md` still names placeholder replacement,
  `gitops/workloads/adminer/` as fuller active reference, and feature branch +
  PR flow.
- `gitops/README.md` matrices keep explicit non-latest image policy, AppProject
  allow-list rationale, external service contract, and secret management
  responsibility.
- `infrastructure/README.md`, `tests/README.md`, and `traefik/README.md`
  distinguish repo-static checks from live/operator-owned checks.

- [x] **Step 5: Validate active control surfaces**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
bash scripts/validate-gitops-structure.sh
bash scripts/validate-k8s-manifests.sh .
bash scripts/check-secret-handling.sh .
bash scripts/validate-policy-gates.sh .
bash infrastructure/tests/verify-contracts-static.sh
```

Expected:

- Repository quality gate prints `[PASS] repository quality gates passed`.
- GitOps structure check exits `0`.
- Kubernetes manifest check exits `0`; optional `kube-linter` absence is
  reported as `SKIP`.
- Secret handling prints no plaintext secret patterns.
- Policy gates exit `0`; optional `conftest` absence is reported as `SKIP`
  with built-in fallback passing.
- Static infrastructure contracts pass.

- [x] **Step 6: Update task and progress evidence**

Mark `ACS-004` as `done` in the task record and append progress evidence with
the commands from Step 5.

- [x] **Step 7: Commit ACS-004**

Run:

```bash
git add scripts/README.md gitops/README.md gitops/workloads/README.md infrastructure/README.md tests/README.md traefik/README.md examples/README.md examples/sample-app/README.md scripts/validate-repo-quality-gates.sh scripts/validate-harness.sh scripts/check-secret-handling.sh scripts/validate-policy-gates.sh scripts/validate-k8s-manifests.sh scripts/validate-gitops-structure.sh infrastructure/tests/verify-contracts-static.sh docs/04.execution/tasks/2026-07-04-active-control-surface-governance-hardening.md docs/00.agent-governance/memory/progress.md
git diff --cached --name-only
git commit -m "docs(validation): Align active control surface checks"
```

Expected: staged files include only touched active README, validator, task, and
progress files. If optional scripts were not changed, omit them from the final
`git add` command before committing.

### Task 5: Final Evidence Closure and Branch Readiness

**Files:**

- Modify: `docs/04.execution/plans/2026-07-04-active-control-surface-governance-hardening.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/2026-07-04-active-control-surface-governance-hardening.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [x] **Step 1: Run final validation bundle**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
bash scripts/validate-harness.sh
```

Expected:

- `git diff --check` prints no output.
- Repository quality gate prints `[PASS] repository quality gates passed`.
- Harness validation ends with `PASS harness repo-static validation`.

- [x] **Step 2: Run focused final scans**

Run:

```bash
rg -n "^---$" .github/ABOUT.md .github/PULL_REQUEST_TEMPLATE.md .github/SECURITY.md scripts/README.md gitops/README.md gitops/workloads/README.md infrastructure/README.md tests/README.md traefik/README.md examples/README.md examples/sample-app/README.md
rg -n "Cloud Example Snapshot|not live provider-latest guidance|provider-latest" examples/README.md docs/99.templates/support docs/00.agent-governance/rules scripts/validate-repo-quality-gates.sh
rg -n "secret values|live mutation|operator-owned|optional.*SKIP|repo-static" scripts/README.md gitops/README.md infrastructure/README.md tests/README.md traefik/README.md scripts/validate-repo-quality-gates.sh
```

Expected:

- First scan returns no frontmatter delimiters in README/GitHub-native
  Markdown files.
- Second scan shows snapshot boundary wording in canonical owners and active
  routing surfaces.
- Third scan shows protected-surface, optional-tool, and repo-static wording in
  active owners.

- [x] **Step 3: Update plan and task statuses**

Update:

- This plan frontmatter `status: done`.
- `docs/04.execution/plans/README.md` row for this plan to `Done`.
- Task record frontmatter `status: done`.
- `docs/04.execution/tasks/README.md` row for this task record to `Done`.
- Task record `ACS-005` status to `done` with final validation evidence.

- [x] **Step 4: Update progress ledger**

Append a final progress entry with:

- Full validation commands and pass results.
- Optional-tool skip notes for `kube-linter` or `conftest` if they remain
  unavailable.
- Final boundary summary: active control surfaces hardened, AWS/Azure examples
  remain snapshot-bounded, no live mutation performed.

- [x] **Step 5: Commit ACS-005**

Run:

```bash
git add docs/04.execution/plans/2026-07-04-active-control-surface-governance-hardening.md docs/04.execution/plans/README.md docs/04.execution/tasks/2026-07-04-active-control-surface-governance-hardening.md docs/04.execution/tasks/README.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(validation): Close active control surface hardening"
```

Expected: one closure commit with plan/task/status/progress evidence only.

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-ACS-001 | Structural | Diff hygiene | `git diff --check` | No output |
| VAL-ACS-002 | Repository | Canonical repo quality gate | `bash scripts/validate-repo-quality-gates.sh .` | Prints `[PASS] repository quality gates passed` |
| VAL-ACS-003 | Harness | Full repo-static harness | `bash scripts/validate-harness.sh` | Ends with `PASS harness repo-static validation` |
| VAL-ACS-004 | GitOps | GitOps structure | `bash scripts/validate-gitops-structure.sh` | Exits `0` and reports hierarchy/kustomization checks as OK |
| VAL-ACS-005 | Manifests | Kubernetes manifest syntax and optional lint | `bash scripts/validate-k8s-manifests.sh .` | Exits `0`; optional `kube-linter` absence may be reported as `SKIP` |
| VAL-ACS-006 | Secrets | Secret-handling static scan | `bash scripts/check-secret-handling.sh .` | Exits `0` and reports no plaintext secret patterns |
| VAL-ACS-007 | Policy | Rego or fallback policy gate | `bash scripts/validate-policy-gates.sh .` | Exits `0`; optional `conftest` absence may be reported as `SKIP` when fallback passes |
| VAL-ACS-008 | Infrastructure | Static infrastructure contract verification | `bash infrastructure/tests/verify-contracts-static.sh` | Ends with `[PASS] static contract verification passed` |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| README files become policy bodies again | Medium | Keep README edits concise and route durable wording to Stage 00, Stage 99, Stage 05, workflows, or validators |
| Validator overfits snapshot cloud docs | High | Scope deterministic checks to active surfaces or approved snapshot boundary phrases |
| Optional tool absence is mislabeled as full coverage | Medium | Preserve explicit `SKIP` wording for missing `kube-linter` and `conftest` and require fallback success |
| Secret fixtures are exposed while auditing | High | Use path and static scanner evidence only; do not display, edit, or regenerate `secrets/certs/*.pem` |
| Live mutation sneaks into validation | High | Keep validation repo-static; document operator-owned live commands instead of running them |
| Cloud provider latestness is implied | Medium | Keep `aws/` and `azure/` examples as Cloud Example Snapshot material unless a separate refresh spec is approved |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Run repository quality, harness, GitOps, manifest,
  secret, policy, and static infrastructure gates before closure.
- **Sandbox / Canary Rollout**: Not applicable. This is repo-static
  governance and validation work.
- **Human Approval Gate**: Required for live runtime validation, cloud
  mutation, GitHub push/merge/publish, credential changes, certificate
  regeneration, or changing the approved AWS/Azure snapshot boundary.
- **Rollback Trigger**: Any deterministic validator failure that cannot be
  fixed by aligning the changed contract surface.
- **Prompt / Model Promotion Criteria**: Not applicable. No model or prompt
  runtime promotion is included.

## Completion Criteria

- [x] Scoped active control-surface work completed.
- [x] AWS/Azure cloud examples remain snapshot-bounded.
- [x] README and GitHub-native Markdown files remain frontmatter-free.
- [x] Deterministic validator additions are aligned with canonical
  support/governance owners.
- [x] Required validation bundle passes.
- [x] Plan, task record, task README, and progress memory are updated.
- [x] Logical-unit commits exist for each completed task.

## Related Documents

- **Spec**: [Active Control Surface Governance Hardening Spec](../../03.specs/016-active-control-surface-governance-hardening/spec.md)
- **Prior Spec**: [Workspace Document Governance Hardening](../../03.specs/013-workspace-document-governance-hardening/spec.md)
- **Prior Spec**: [Workspace Document Contract Normalization](../../03.specs/014-workspace-document-contract-normalization/spec.md)
- **Prior Spec**: [Agent Governance Contract Normalization](../../03.specs/015-agent-governance-contract-normalization/spec.md)
- **Task Record**: `../tasks/2026-07-04-active-control-surface-governance-hardening.md`
  will be created by ACS-001.
- **Template Documentation Contract**: [documentation-contract.md](../../99.templates/support/documentation-contract.md)
- **Template Routing Contract**: [template-routing.md](../../99.templates/support/template-routing.md)
- **Frontmatter Schema**: [frontmatter-schema.md](../../99.templates/support/frontmatter-schema.md)
- **Common Documentation Governance**: [common-documentation-governance.md](../../99.templates/support/common-documentation-governance.md)
- **Documentation Protocol**: [documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Quality Standards**: [quality-standards.md](../../00.agent-governance/rules/quality-standards.md)
- **Approval Boundaries**: [approval-boundaries.md](../../00.agent-governance/rules/approval-boundaries.md)
