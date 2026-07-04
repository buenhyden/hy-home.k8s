---
title: 'Active Control Surface Governance Hardening Task Record'
type: sdlc/task
status: draft
owner: platform
updated: 2026-07-04
---

# Task: Active Control Surface Governance Hardening

## Overview

This document tracks implementation and verification work for Active Control
Surface Governance Hardening. It keeps GitHub, CI/CD, QA, GitOps,
infrastructure, policy, scripts, tests, Traefik, and sample-app control-surface
work traceable to the parent Spec and Plan while preserving AWS/Azure cloud
examples as dated snapshots.

## Inputs

- **Parent Plan**:
  [../plans/2026-07-04-active-control-surface-governance-hardening.md](../plans/2026-07-04-active-control-surface-governance-hardening.md)
- **Parent Spec**:
  [../../03.specs/016-active-control-surface-governance-hardening/spec.md](../../03.specs/016-active-control-surface-governance-hardening/spec.md)

## Working Rules

- Work only repo-static control surfaces unless a separate human approval
  grants a live mutation path.
- Do not inspect secret values, regenerate credentials, mutate live clusters,
  or change third-party resources.
- Keep README files and GitHub-native Markdown frontmatter-free.
- Keep durable policy in Stage 00 governance, Stage 99 support contracts,
  Stage 05 operations documents, workflow files, or validators according to
  the owning surface.
- Repo-static validation must not be reported as live k3d, Argo CD, Vault,
  ESO, cloud, or deployment readiness unless the matching live check was
  approved and run.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| ------- | ----------- | ---- | --------------------- | ------------------- | --------------------- | ----- | ------ |
| ACS-001 | Create task record and baseline active/snapshot inventory | doc | VAL-SPC-001, VAL-SPC-002 | Task 1 | Baseline scans, task record, tasks README, progress ledger, `git diff --check`, repo quality gate | platform | Done |
| ACS-002 | Normalize Stage 99 and Stage 00 active-control contracts | doc | VAL-SPC-001, VAL-SPC-003 | Task 2 | README/GitHub-native/snapshot ownership scan, support/governance owner updates, progress ledger | platform | Done |
| ACS-003 | Align GitHub, CI/CD, QA, and protected-surface control files | doc | VAL-SPC-001, VAL-SPC-003, VAL-SPC-004 | Task 3 | GitHub Markdown remains frontmatter-free, workflow YAML parses, repo quality gate | platform | Todo |
| ACS-004 | Align GitOps, infrastructure, policy, scripts, tests, Traefik, and sample-app surfaces | doc | VAL-SPC-001, VAL-SPC-002, VAL-SPC-004 | Task 4 | Harness validation passes and optional tool skips remain explicit | platform | Todo |
| ACS-005 | Close evidence, review, and branch readiness | doc | VAL-SPC-005 | Task 5 | Full validation bundle, updated plan/task evidence, final drift review | platform | Todo |

## Suggested Types

- `doc`
- `test`
- `eval`
- `guardrail`
- `ops`

## Phase View

### Task 1: Baseline Inventory and Task Record

- [x] ACS-001 Create task record and baseline active/snapshot inventory.

### Task 2: Canonical Support and Governance Contracts

- [x] ACS-002 Normalize Stage 99 and Stage 00 active-control contracts.

### Task 3: GitHub, CI/CD, QA, and Protected Surfaces

- [ ] ACS-003 Align GitHub, CI/CD, QA, and protected-surface control files.

### Task 4: GitOps and Repo-static Validation Surfaces

- [ ] ACS-004 Align GitOps, infrastructure, policy, scripts, tests, Traefik,
  and sample-app surfaces.

### Task 5: Evidence Closure

- [ ] ACS-005 Close evidence, review, and branch readiness.

## Baseline Inventory Evidence

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

## Approved Snapshot Boundary

AWS and Azure cloud example docs under `examples/aws/docs` and
`examples/azure/docs` remain dated Cloud Example Snapshot material. They are
not active provider-latest guidance, not live deployment evidence, and not
promoted into active SDLC frontmatter or section enforcement by this task.
Future cloud provider refresh work must create separate scoped evidence and
validation.

## ACS-002 Canonical Ownership Evidence

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

## Verification Summary

- **Test Commands**:
  - `git status --short --branch` - PASS, clean branch
    `codex/active-control-surface-governance-hardening`.
  - `git diff --check` - PASS.
  - `bash scripts/validate-repo-quality-gates.sh .` - PASS, including
    `[PASS] repository quality gates passed`.
- **Eval Commands**:
  - Baseline inventory and contract-candidate scans listed in
    `Baseline Inventory Evidence`.
  - ACS-002 canonical ownership scan listed in
    `ACS-002 Canonical Ownership Evidence`.
- **Logs / Evidence Location**:
  - This task record.
  - [../../00.agent-governance/memory/progress.md](../../00.agent-governance/memory/progress.md)

## Related Documents

- **Spec**:
  [../../03.specs/016-active-control-surface-governance-hardening/spec.md](../../03.specs/016-active-control-surface-governance-hardening/spec.md)
- **Plan**:
  [../plans/2026-07-04-active-control-surface-governance-hardening.md](../plans/2026-07-04-active-control-surface-governance-hardening.md)
- **Task Template**:
  [../../99.templates/templates/sdlc/execution/task.template.md](../../99.templates/templates/sdlc/execution/task.template.md)
