---
title: 'Active Control Surface Governance Hardening Implementation Plan'
version: "1.0"
type: sdlc/plan
layer: "03.specs"
status: done
owner: platform
updated: 2026-07-13
artifact_id: "SPEC-0016-PLAN-0001"
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
`docs/03.specs/0016-active-control-surface-governance-hardening/spec.md`. The
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

### Legacy Task ledger inputs

This document tracks implementation and verification work for Active Control
Surface Governance Hardening. It keeps GitHub, CI/CD, QA, GitOps,
infrastructure, policy, scripts, tests, Traefik, and sample-app control-surface
work traceable to the parent Spec and Plan while preserving AWS/Azure cloud
examples as dated snapshots.

- **Parent Plan**:
  [../plans/2026-07-04-active-control-surface-governance-hardening.md](plan.md)
- **Parent Spec**:
  [../../03.specs/0016-active-control-surface-governance-hardening/spec.md](spec.md)
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
  - `docs/03.specs/**`, `docs/03.specs/**`, and
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
| ACS-001 | Create task record and baseline active/snapshot inventory | `docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records`, `docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records`, `docs/00.agent-governance/memory/progress.md` | VAL-SPC-001, VAL-SPC-002 | Baseline scans captured; repo-quality gate passes |
| ACS-002 | Normalize Stage 99 and Stage 00 active-control contracts | `docs/99.templates/support/*.md`, `docs/00.agent-governance/rules/*.md`, `docs/00.agent-governance/scopes/*.md` as needed | VAL-SPC-001, VAL-SPC-003 | README/GitHub-native/snapshot ownership rules are canonical and non-duplicative |
| ACS-003 | Align GitHub, CI/CD, QA, and protected-surface control files | `.github/**`, `scripts/validate-repo-quality-gates.sh`, `docs/00.agent-governance/rules/quality-standards.md`, `docs/00.agent-governance/rules/git-workflow.md` as needed | VAL-SPC-001, VAL-SPC-003, VAL-SPC-004 | GitHub Markdown remains frontmatter-free; workflow YAML parses; repo-quality gate passes |
| ACS-004 | Align GitOps, infrastructure, policy, scripts, tests, Traefik, and sample-app surfaces | `scripts/README.md`, `gitops/README.md`, `gitops/workloads/README.md`, `infrastructure/README.md`, `policy/**`, `tests/README.md`, `traefik/README.md`, `examples/README.md`, `examples/sample-app/README.md`, validators as needed | VAL-SPC-001, VAL-SPC-002, VAL-SPC-004 | Harness validation passes; optional tool skips remain explicit |
| ACS-005 | Close evidence, review, and branch readiness | Plan, task record, task README, progress ledger | VAL-SPC-005 | Full validation bundle passes; plan/task status updated; no unresolved drift |

### Detailed Tasks

### Task 1: Baseline Inventory and Task Record

**Files:**

- Create: `docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records`
- Modify: `docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records`
- Modify: `docs/00.agent-governance/memory/progress.md`
- Read: `docs/99.templates/templates/specs/task.template.md`
- Read: `docs/03.specs/0016-active-control-surface-governance-hardening/spec.md`

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
sed -n '1,260p' docs/99.templates/templates/specs/task.template.md
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

Create `docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records`
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
  `../../03.specs/0016-active-control-surface-governance-hardening/spec.md`
- Task IDs `ACS-001` through `ACS-005`.
- Initial `ACS-001` status: `in-progress`.
- Baseline inventory evidence from Steps 3 through 6.
- The approved boundary: AWS/Azure cloud example docs remain dated snapshots.

- [x] **Step 8: Update the Stage 04 tasks README**

Add the new task record to `docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records` with:

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
git add docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records docs/00.agent-governance/memory/progress.md
git commit -m "docs(task): Track active control surface hardening evidence"
```

Expected: `git diff --check` prints no output,
`scripts/validate-repo-quality-gates.sh` prints
`[PASS] repository quality gates passed`, and the commit contains only the task
record, tasks README, and progress ledger changes.

### Task 2: Canonical Support and Governance Contracts

**Files:**

- Modify: `docs/99.templates/support/documentation-contract.md`
- Modify: `docs/99.templates/README.md`
- Modify: `docs/99.templates/contracts/frontmatter.schema.json`
- Modify: `docs/99.templates/support/common-documentation-governance.md`
- Modify: `docs/99.templates/support/legacy-cleanup-rules.md`
- Modify: `docs/00.agent-governance/rules/documentation-protocol.md`
- Modify: `docs/00.agent-governance/rules/document-stage-routing.md`
- Modify: `docs/00.agent-governance/rules/quality-standards.md`
- Modify: `docs/00.agent-governance/rules/approval-boundaries.md`
- Modify: `docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records`
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

In `docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records`,
mark `ACS-002` as `done` and add the Step 4 scan as validation evidence.

- [x] **Step 6: Update progress ledger**

Append a progress entry stating that support and Stage 00 canonical ownership
were normalized for active control surfaces and snapshot boundaries.

- [x] **Step 7: Validate and commit ACS-002**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/99.templates/support/documentation-contract.md docs/99.templates/README.md docs/99.templates/contracts/frontmatter.schema.json docs/99.templates/support/common-documentation-governance.md docs/99.templates/support/legacy-cleanup-rules.md docs/00.agent-governance/rules/documentation-protocol.md docs/00.agent-governance/rules/document-stage-routing.md docs/00.agent-governance/rules/quality-standards.md docs/00.agent-governance/rules/approval-boundaries.md docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records docs/00.agent-governance/memory/progress.md
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
- Modify: `docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records`
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
git add .github/ABOUT.md .github/PULL_REQUEST_TEMPLATE.md .github/SECURITY.md .github/workflows/ci.yml .github/dependabot.yml .github/zizmor.yml scripts/validate-repo-quality-gates.sh docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records docs/00.agent-governance/memory/progress.md
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
- Modify: `docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records`
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
git add scripts/README.md gitops/README.md gitops/workloads/README.md infrastructure/README.md tests/README.md traefik/README.md examples/README.md examples/sample-app/README.md scripts/validate-repo-quality-gates.sh scripts/validate-harness.sh scripts/check-secret-handling.sh scripts/validate-policy-gates.sh scripts/validate-k8s-manifests.sh scripts/validate-gitops-structure.sh infrastructure/tests/verify-contracts-static.sh docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records docs/00.agent-governance/memory/progress.md
git diff --cached --name-only
git commit -m "docs(validation): Align active control surface checks"
```

Expected: staged files include only touched active README, validator, task, and
progress files. If optional scripts were not changed, omit them from the final
`git add` command before committing.

### Task 5: Final Evidence Closure and Branch Readiness

**Files:**

- Modify: `docs/03.specs/0016-active-control-surface-governance-hardening/plan.md`
- Modify: `docs/03.specs/0016-active-control-surface-governance-hardening/plan.md`
- Modify: `docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records`
- Modify: `docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records`
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
- `docs/03.specs/0016-active-control-surface-governance-hardening/plan.md` row for this plan to `Done`.
- Task record frontmatter `status: done`.
- `docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records` row for this task record to `Done`.
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
git add docs/03.specs/0016-active-control-surface-governance-hardening/plan.md docs/03.specs/0016-active-control-surface-governance-hardening/plan.md docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records docs/00.agent-governance/memory/progress.md
git commit -m "docs(validation): Close active control surface hardening"
```

Expected: one closure commit with plan/task/status/progress evidence only.

### Legacy Task supplemental evidence

### Phase View

### Task 1: Baseline Inventory and Task Record

- [x] ACS-001 Create task record and baseline active/snapshot inventory.

### Task 2: Canonical Support and Governance Contracts

- [x] ACS-002 Normalize Stage 99 and Stage 00 active-control contracts.

### Task 3: GitHub, CI/CD, QA, and Protected Surfaces

- [x] ACS-003 Align GitHub, CI/CD, QA, and protected-surface control files.

### Task 4: GitOps and Repo-static Validation Surfaces

- [x] ACS-004 Align GitOps, infrastructure, policy, scripts, tests, Traefik,
  and sample-app surfaces.

### Task 5: Evidence Closure

- [x] ACS-005 Close evidence, review, and branch readiness.

### Baseline Inventory Evidence

### Commands

- `git status --short --branch`
- `rg --files .github examples/sample-app gitops infrastructure policy scripts tests traefik | sort`
- `rg --files examples/aws/docs examples/azure/docs | rg '\.md$' | sort`
- `rg -n "^# |^## " .github examples/README.md examples/sample-app/README.md gitops infrastructure scripts tests traefik -g '*.md'`
- `rg -n "GitHub Actions|workflow|CI|QA|GitOps|Argo CD|Argo Rollouts|ExternalSecret|Secret|Kustomize|conftest|kube-linter|Cloud Example Snapshot|provider-latest|live provider" .github examples gitops infrastructure policy scripts tests traefik docs/99.templates/support docs/00.agent-governance/rules`

### Findings

- Branch baseline was clean on
  `codex/active-control-surface-governance-hardening`.
- Active control-surface inventory returned 135 files across GitHub controls,
  sample-app manifests, GitOps desired state, infrastructure contracts, policy
  files, validation scripts, tests README, and Traefik route manifests.
- Snapshot example document inventory returned 59 Markdown files:
  26 under `examples/aws/docs` and 33 under `examples/azure/docs`.
- Active README and GitHub control heading scan returned 118 heading-pattern
  matches across 11 Markdown files.
- External-source-backed contract candidate scan returned 523 matches across
  active surfaces, governance/support owners, and AWS/Azure snapshot examples.

### Active Inventory Counts

| Area | Files |
| ---- | ----- |
| `.github` | 15 |
| `examples/sample-app` | 8 |
| `gitops` | 81 |
| `infrastructure` | 15 |
| `policy` | 1 |
| `scripts` | 9 |
| `tests` | 1 |
| `traefik` | 5 |

### README and GitHub Control Classification

| File | Class | Heading-pattern Matches | Notes |
| ---- | ----- | ----------------------- | ----- |
| `.github/ABOUT.md` | GitHub-native control | 7 | GitHub configuration hub, workflow roles, source basis, and boundaries. |
| `.github/PULL_REQUEST_TEMPLATE.md` | GitHub-native control | 9 | GitHub PR template consumed directly by GitHub. |
| `.github/SECURITY.md` | GitHub-native control | 3 | GitHub security policy surface consumed directly by GitHub. |
| `examples/README.md` | snapshot boundary index | 12 | Routes `sample-app` as active template and AWS/Azure as Cloud Example Snapshot material. |
| `examples/sample-app/README.md` | sample onboarding template | 11 | Minimal local k3d GitOps onboarding template with placeholder replacement notes. |
| `gitops/README.md` | common README | 16 | Desired-state GitOps entrypoint and matrix owner. |
| `gitops/workloads/README.md` | common README | 9 | Workload onboarding and coverage matrix owner. |
| `infrastructure/README.md` | common README | 14 | Bootstrap, infrastructure tests, and live/static boundary owner. |
| `scripts/README.md` | common README | 17 | Validation script inventory and command contract owner. |
| `tests/README.md` | common README | 10 | Repository validation model and evidence boundary owner. |
| `traefik/README.md` | common README | 10 | Local Traefik dynamic-config route contract owner. |

### Contract Candidate Counts

| Area | Matches |
| ---- | ------- |
| `.github` | 38 |
| `docs/00.agent-governance/rules` | 33 |
| `docs/99.templates/support` | 6 |
| `examples/README.md` | 10 |
| `examples/aws` snapshot | 51 |
| `examples/azure` snapshot | 44 |
| `examples/sample-app` active | 19 |
| `gitops` | 54 |
| `infrastructure` | 33 |
| `policy` | 2 |
| `scripts` | 216 |
| `tests` | 8 |
| `traefik` | 9 |

### Approved Snapshot Boundary

AWS and Azure cloud example docs under `examples/aws/docs` and
`examples/azure/docs` remain dated Cloud Example Snapshot material. They are
not active provider-latest guidance, not live deployment evidence, and not
promoted into active SDLC frontmatter or section enforcement by this task.
Future cloud provider refresh work must create separate scoped evidence and
validation.

### ACS-002 Canonical Ownership Evidence

### Commands

- `rg -n "Cloud Example Snapshot|provider-latest|frontmatter-free|GitHub-native|README files are entrypoints|optional-tool skips|secret value" docs/99.templates/support docs/00.agent-governance/rules`

### Findings

- Stage 99 support contracts now own active control-surface boundaries for
  README routing, GitHub-native Markdown, Cloud Example Snapshot material,
  provider-latest cleanup, and frontmatter-free exceptions.
- Stage 00 rules now own README entrypoint policy, Cloud Example Snapshot
  routing exclusions, CI/CD and QA optional-tool skip evidence, and explicit
  approval boundaries for live cluster, Vault, cloud, GitHub publish/merge,
  and secret value work.
- The scan returned canonical support/governance matches; no README file is
  the only owner of a durable policy rule.
- `git diff --check` passed with no output.
- `bash scripts/validate-repo-quality-gates.sh .` passed with
  `[PASS] repository quality gates passed`.

### ACS-003 GitHub Control Evidence

### Commands

- `rg -n "frontmatter|policy source of truth|branch-policy|repo-quality|manifest-static|secret|workflow_dispatch|pull_request_target|Dependabot|zizmor|publish|push|merge|Cloud Example Snapshot" .github scripts/validate-repo-quality-gates.sh`
- `rg -n "^---$" .github/ABOUT.md .github/PULL_REQUEST_TEMPLATE.md .github/SECURITY.md`
- `git diff --check`
- GitHub workflow YAML parse:

```bash
python3 - <<'PY'
import pathlib, yaml
for path in sorted(pathlib.Path('.github/workflows').glob('*.yml')):
    with path.open(encoding='utf-8') as handle:
        yaml.safe_load(handle)
print('workflow yaml parse ok')
PY
```

- `bash scripts/validate-repo-quality-gates.sh .`

### Findings

- `.github/ABOUT.md` and `.github/SECURITY.md` already matched the
  frontmatter-free routing contract and did not need edits.
- `.github/PULL_REQUEST_TEMPLATE.md` now prompts reviewers to preserve Cloud
  Example Snapshot boundaries for `examples/aws` or `examples/azure` changes
  unless an approved provider refresh spec exists.
- `scripts/validate-repo-quality-gates.sh` now deterministically rejects PR
  template drift if no PR-template line keeps the Cloud Example Snapshot paths,
  boundary-preservation intent, and approved provider refresh spec terms
  together.
- GitHub workflow YAML parsed successfully with `workflow yaml parse ok`.
- `git diff --check` passed with no output.
- `bash scripts/validate-repo-quality-gates.sh .` passed with
  `[PASS] repository quality gates passed`.

### ACS-004 GitOps and Repo-static Validation Evidence

### Commands

- `rg -n "## |Validation|validate-|check-secret-handling|repo-quality|GitOps|Secret|ExternalSecret|Argo CD|Argo Rollouts|Kustomize|conftest|kube-linter|Cloud Example Snapshot|not live provider-latest|live mutation|secret values" scripts/README.md gitops/README.md gitops/workloads/README.md infrastructure/README.md tests/README.md traefik/README.md examples/README.md examples/sample-app/README.md`
- `rg -n "^---$|^## Related (References|Folders)" scripts/README.md gitops/README.md gitops/workloads/README.md infrastructure/README.md tests/README.md traefik/README.md examples/README.md examples/sample-app/README.md`
- `git diff --check`
- `bash scripts/validate-repo-quality-gates.sh .`
- `bash scripts/validate-gitops-structure.sh`
- `bash scripts/validate-k8s-manifests.sh .`
- `bash scripts/check-secret-handling.sh .`
- `bash scripts/validate-policy-gates.sh .`
- `bash infrastructure/tests/verify-contracts-static.sh`

### Findings

- Active README profile stayed unchanged: no README YAML frontmatter and no
  deprecated related-heading variants.
- `scripts/README.md` now states optional `kube-linter` and `conftest` skips
  as SKIP/fallback evidence, not full optional-tool coverage.
- `gitops/README.md`, `gitops/workloads/README.md`, `examples/README.md`, and
  `examples/sample-app/README.md` now make the sample-app activation boundary
  explicit: placeholders must be replaced and repo-static validation must pass
  before copied manifests are treated as active GitOps desired state.
- `tests/README.md` separates repo-static, optional-tool, and
  live/operator-owned evidence, and `traefik/README.md` separates route
  manifest contracts from live port availability.
- `scripts/validate-repo-quality-gates.sh` now deterministically checks the
  sample-app activation, workload onboarding, Traefik live-port boundary, and
  tests README evidence-boundary phrases.
- Optional wrapper and focused validator scripts were reviewed and left
  untouched because their existing wording already documents repo-static,
  SKIP/fallback, no-live-check, GitOps hierarchy, secret redaction, and static
  contract boundaries.
- `git diff --check` passed with no output.
- `bash scripts/validate-repo-quality-gates.sh .` passed with
  `[PASS] repository quality gates passed`.
- `bash scripts/validate-gitops-structure.sh` passed with
  `=== done (exit: 0) ===`.
- `bash scripts/validate-k8s-manifests.sh .` passed with 104 YAML files; local
  `kube-linter` was not installed and was reported as
  `SKIP optional kube-linter not installed — YAML syntax validation only`.
- `bash scripts/check-secret-handling.sh .` passed with 100 files and
  `OK  no plaintext secret patterns found`.
- `bash scripts/validate-policy-gates.sh .` passed; local `conftest` was not
  installed and the built-in policy fallback reported
  `[PASS] built-in policy fallback passed`.
- `bash infrastructure/tests/verify-contracts-static.sh` passed with
  `[PASS] static contract verification passed`.
- RTK limitation repeated: `rtk` is not on PATH; `/home/hy/.local/bin/rtk
  --version` works, but `/home/hy/.local/bin/rtk gain` cannot initialize its
  tracking database, so required validation commands were run directly.
- No live Kubernetes, Argo CD, Vault, cloud, external Traefik, provider,
  publish, push, merge, or secret-value action was performed.

### ACS-005 Final Closure Evidence

### Commands

- `git diff --check`
- `bash scripts/validate-repo-quality-gates.sh .`
- `bash scripts/validate-harness.sh`
- `rg -n "^---$" .github/ABOUT.md .github/PULL_REQUEST_TEMPLATE.md .github/SECURITY.md scripts/README.md gitops/README.md gitops/workloads/README.md infrastructure/README.md tests/README.md traefik/README.md examples/README.md examples/sample-app/README.md`
- `rg -n "Cloud Example Snapshot|not live provider-latest guidance|provider-latest" examples/README.md docs/99.templates/support docs/00.agent-governance/rules scripts/validate-repo-quality-gates.sh`
- `rg -n "secret values|live mutation|operator-owned|optional.*SKIP|repo-static" scripts/README.md gitops/README.md infrastructure/README.md tests/README.md traefik/README.md scripts/validate-repo-quality-gates.sh`

### Findings

- `git diff --check` passed with no output.
- `bash scripts/validate-repo-quality-gates.sh .` passed with
  `[PASS] repository quality gates passed`.
- `bash scripts/validate-harness.sh` passed and ended with
  `PASS harness repo-static validation`.
- Harness validation also confirmed GitOps structure, Kubernetes manifest
  syntax across 104 files, static secret handling, policy gates, and static
  infrastructure contracts.
- Optional `kube-linter` was unavailable and remained explicit SKIP evidence;
  optional `conftest` was unavailable and the built-in policy fallback passed.
- README and GitHub-native Markdown frontmatter delimiter scan returned no
  matches.
- Cloud Example Snapshot and provider-latest scans showed the boundary in
  canonical owners and active routing surfaces: `examples/README.md`, Stage 99
  support contracts, Stage 00 governance rules, and the repo quality gate.
- Protected-surface scans showed secret-value, live-mutation, operator-owned,
  optional-tool, and repo-static wording in active owners.
- Plan and task indexes are marked `Done`, and this task record is closed.
- No live Kubernetes, Argo CD, Vault, cloud, external Traefik, provider,
  publish, push, merge, or secret-value action was performed.
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

### Legacy Task verification evidence

- **Test Commands**:
  - `git status --short --branch` - PASS, clean branch
    `codex/active-control-surface-governance-hardening`.
  - `git diff --check` - PASS.
  - `bash scripts/validate-repo-quality-gates.sh .` - PASS, including
    `[PASS] repository quality gates passed`.
  - `bash scripts/validate-harness.sh` - PASS, ended with
    `PASS harness repo-static validation`.
  - GitHub workflow YAML parse - PASS, `workflow yaml parse ok`.
  - `bash scripts/validate-gitops-structure.sh` - PASS.
  - `bash scripts/validate-k8s-manifests.sh .` - PASS with optional
    `kube-linter` SKIP.
  - `bash scripts/check-secret-handling.sh .` - PASS.
  - `bash scripts/validate-policy-gates.sh .` - PASS with optional `conftest`
    SKIP and built-in fallback pass.
  - `bash infrastructure/tests/verify-contracts-static.sh` - PASS.
- **Eval Commands**:
  - Baseline inventory and contract-candidate scans listed in
    `Baseline Inventory Evidence`.
  - ACS-002 canonical ownership scan listed in
    `ACS-002 Canonical Ownership Evidence`.
  - ACS-003 GitHub control scan and frontmatter scan listed in
    `ACS-003 GitHub Control Evidence`.
  - ACS-004 active README matrix scan, README profile scan, and repo-static
    validation bundle listed in
    `ACS-004 GitOps and Repo-static Validation Evidence`.
  - ACS-005 final frontmatter, snapshot-boundary, protected-surface, and
    repo-static scans listed in `ACS-005 Final Closure Evidence`.
- **Logs / Evidence Location**:
  - This task record.
  - [../../00.agent-governance/memory/progress.md](../../00.agent-governance/memory/progress.md)
## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| README files become policy bodies again | Medium | Keep README edits concise and route durable wording to Stage 00, Stage 99, Stage 05, workflows, or validators |
| Validator overfits snapshot cloud docs | High | Scope deterministic checks to active surfaces or approved snapshot boundary phrases |
| Optional tool absence is mislabeled as full coverage | Medium | Preserve explicit `SKIP` wording for missing `kube-linter` and `conftest` and require fallback success |
| Secret fixtures are exposed while auditing | High | Use path and static scanner evidence only; do not display, edit, or regenerate `secrets/certs/*.pem` |
| Live mutation sneaks into validation | High | Keep validation repo-static; document operator-owned live commands instead of running them |
| Cloud provider latestness is implied | Medium | Keep `aws/` and `azure/` examples as Cloud Example Snapshot material unless a separate refresh spec is approved |

### Agent Rollout & Evaluation Gates

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

### Legacy Task approval and rollback boundaries

- **Allowed Paths**: `ACS-001 through ACS-005` is limited to these Active Control Surface Governance Hardening owners and Task-Table surfaces:
  - `docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records`
  - `docs/03.specs/0016-active-control-surface-governance-hardening/plan.md`
  - `docs/03.specs/0016-active-control-surface-governance-hardening/spec.md`
  - `examples/aws/docs`
  - `examples/azure/docs`
  - `examples/sample-app`
  - `.github/ABOUT.md`
- **Forbidden Paths**: runtime manifests, provider or CI settings, secret values, generated/local state, and paths outside the Active Control Surface Governance Hardening work items and linked evidence owners.
- **Approval Required**: Human approval is required before Active Control Surface Governance Hardening protected-file expansion, deletion/relocation, runtime/CI/provider mutation, credential access, publication, push, or merge beyond the parent Plan.
- **Static Validation**: Preserve the Active Control Surface Governance Hardening outcomes and limitations recorded in Verification Summary; use these recorded checks:
  - `git status --short --branch`
  - `git diff --check`
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `bash scripts/validate-harness.sh`
- **Live Validation**: DEFER — Active Control Surface Governance Hardening is closed by repository-static/documentation evidence; historical live commands, if any, are not authority for a new cluster, provider, external-service, or deployment claim.
- **Secret / Vault Handling**: No secret value is required for Active Control Surface Governance Hardening; do not read or print tokens, credentials, Vault/Kubernetes Secret data, kubeconfigs, auth files, private logs, or shell history.
- **Rollback Plan**: Revert the logical Active Control Surface Governance Hardening change set for `ACS-001 through ACS-005` and restore its allowed implementation/evidence paths with this Task and parent Plan; documentation rollback does not authorize live mutation.
- **Evidence Location**: Durable Active Control Surface Governance Hardening evidence remains in:
  - `docs/03.specs/0016-active-control-surface-governance-hardening/README.md#task-records`
  - `docs/03.specs/0016-active-control-surface-governance-hardening/plan.md`
  - `docs/03.specs/0016-active-control-surface-governance-hardening/spec.md`
## Completion Criteria

- [x] Scoped active control-surface work completed.
- [x] AWS/Azure cloud examples remain snapshot-bounded.
- [x] README and GitHub-native Markdown files remain frontmatter-free.
- [x] Deterministic validator additions are aligned with canonical
  support/governance owners.
- [x] Required validation bundle passes.
- [x] Plan, task record, task README, and progress memory are updated.
- [x] Logical-unit commits exist for each completed task.

## Traceability

- **Spec**: [Active Control Surface Governance Hardening Spec](spec.md)
- **Prior Spec**: [Workspace Document Governance Hardening](../0013-workspace-document-governance-hardening/spec.md)
- **Prior Spec**: [Workspace Document Contract Normalization](../0014-workspace-document-contract-normalization/spec.md)
- **Prior Spec**: [Agent Governance Contract Normalization](../0015-agent-governance-contract-normalization/spec.md)
- **Task**: [../tasks/2026-07-04-active-control-surface-governance-hardening.md](README.md#task-records)
- **Template Documentation Contract**: [documentation-contract.md](../../99.templates/README.md)
- **Template Routing Contract**: [template-routing.md](../../99.templates/README.md)
- **Frontmatter Schema**: [frontmatter-schema.md](../../99.templates/README.md)
- **Common Documentation Governance**: [common-documentation-governance.md](../../99.templates/README.md)
- **Documentation Protocol**: [documentation-protocol.md](../../00.agent-governance/rules/document-authoring.md)
- **Quality Standards**: [quality-standards.md](../../00.agent-governance/rules/quality-standards.md)
- **Approval Boundaries**: [approval-boundaries.md](../../00.agent-governance/rules/approval-boundaries.md)

### Legacy Task traceability

- **Spec**:
  [../../03.specs/0016-active-control-surface-governance-hardening/spec.md](spec.md)
- **Plan**:
  [../plans/2026-07-04-active-control-surface-governance-hardening.md](plan.md)
- **Task Template**:
  [../../99.templates/templates/specs/task.template.md](../../99.templates/templates/specs/task.template.md)
