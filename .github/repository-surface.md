---
title: "GitHub Configuration Hub"
version: "0.1.0"
type: "common/readme-runtime-governance"
status: "active"
owner: "platform"
updated: "2026-09-04"
---
# GitHub Configuration Hub

This document maps the repository-specific GitHub automation surface for the
`hy-home.k8s` main-branch PR flow. It is a routing surface, not the policy
source of truth. It is named `repository-surface.md` rather than `README.md`
because it describes the repository's automation surface rather than the
`.github` directory's own contents, and because GitHub resolves a
`.github/README.md` as a repository profile page.

## Content Mapping

- `workflows/` - CI, release evidence, and repository maintenance automations.
- `ISSUE_TEMPLATE/` - Structured bug and feature intake forms.
- `PULL_REQUEST_TEMPLATE.md` - PR verification checklist aligned with `docs/01.requirements/`, `docs/`, `docs/03.specs/`, and GitOps QA.
- `CODEOWNERS` - Review ownership for repository paths and GitHub configuration.
- `dependabot.yml` and `labeler.yml` - GitHub-native dependency and labeling configuration.
- `SECURITY.md` - Vulnerability reporting instructions.

## Policy Routing

- Branch strategy policy lives in `docs/00.agent-governance/policies/git.md`.
- CI enforcement lives in `workflows/ci.yml`, `scripts/validate-repo-quality-gates.sh`, and the `manifest-static` script bundle.
- The four validation jobs select Python 3.12, resolve the three direct pins
  owned by `requirements/ci-validation.in` through the fully hashed
  `requirements/ci-validation.txt` lock, and install it with hash checking and
  binary-only enforcement; `pre-commit` and
  `repo-quality-static` separately install the official Gitleaks `8.30.0`
  Linux x64 asset after verifying its recorded SHA-256. `pre-commit`,
  `repo-quality-static`, and `agent-governance-static` use full checkout
  history, and `pre-commit` runs the explicit all-files/show-diff command. The
  network-free contract validator reconciles those workflow settings with the
  executable input/lock owners, frozen pre-commit revisions, and technology
  inventory.
- The sole canonical local completion-order, lane, result, formatter, and
  handoff owner is
  [`quality-standards.md`](../docs/00.agent-governance/policies/quality.md);
  this hub and the PR template only route GitHub-specific consumers there.
- Current validator command and fixture inventories live in
  [`scripts/README.md`](../scripts/README.md) and
  [`tests/README.md`](../tests/README.md); this hub does not duplicate their
  counts.
- ARWB-003 records its 31-record/202-link full cutover proof as explicit local/manual evidence, so `repo-quality-static` does not invoke that separate proof. The blocking ACER migration validator does classify its additive archive payloads with the exact security-validated Gitleaks executable supplied to the closed lane.
- `ci.yml` validates pull request shape; GitHub branch protection/rulesets enforce direct-push restrictions outside repo-local files.
- PR author and reviewer prompts live in `PULL_REQUEST_TEMPLATE.md`.
- CI Python dependency identity lives in `.github/requirements/ci-validation.txt`;
  pre-commit repository revisions and source-tag provenance live in
  `.pre-commit-config.yaml`.
- Full-SHA Action pinning is enforced by the repository quality gate; no zizmor suppression file is required.

## Workflow Roles

- `ci.yml` is the required QA gate for pushes and pull requests targeting the repository's canonical integration branch, with manual reruns through `workflow_dispatch`; its single dedicated agent-governance lane enforces the closed CI, harness-semantics, legacy-cutover, and Spec 046 program-closure contracts without treating a tracked workflow as hosted-run evidence.
- `generate-changelog.yml` creates transient seven-day release-evidence artifacts for version tags. It does not commit, push, or publish.
- `labeler.yml`, `greetings.yml`, and `stale.yml` are repository maintenance automations, not QA gates.
- Clear separation of concerns is maintained: local pre-commit handles fast linting and formatting, local repo-static scripts reproduce CI/debug evidence when needed, and GitHub CI performs the required remote gate verdict. Helm chart rendering remains a manual review helper for platform AppProject allow-list changes.

## Source Basis

- Parent Spec: [Workspace Document Governance Hardening Spec](../docs/98.archive/completed/03.specs/0013-workspace-document-governance-hardening/spec.md) records the official-source basis for GitHub Actions documentation, release evidence, supply-chain concepts, and Markdown/YAML formatting claims.
- Workflow role claims in this hub are reconciled against the tracked `.github/workflows/*.yml` files; external-tool currentness changes must update the Spec or a Stage 90 reference before this hub changes behavior.

## Workflow Responsibility Matrix

| Workflow | Role | Trigger / scope | Required evidence | Boundary |
| --- | --- | --- | --- | --- |
| `ci.yml` | Required QA gate for branch policy, repo-quality, agent-governance, manifest, secret, and policy checks. | Runs on `push`, `pull_request`, and `workflow_dispatch` for `main`-centered integration. | `ci-summary` aggregates `branch-policy`, `changes`, `pre-commit`, `repo-quality-static`, `agent-governance-static`, and `manifest-static`; all validation jobs use the shared fully hashed Linux/CPython 3.12 lock with binary-only/hash-required installation, the two repository-quality consumers verify and install Gitleaks `8.30.0`, the three history-dependent jobs use full history, pre-commit performs explicit all-files/show-diff execution from frozen hook commits, the agent lane validates harness semantics and legacy cutover, and manifest-static runs GitOps, manifest, secret, and policy scripts. | No deploy CD, direct Kubernetes mutation, external Vault mutation, container publish, or commit push. |
| `generate-changelog.yml` | Release-evidence artifact generator. | Runs for release tag evidence and manual release support. | Produces a `CHANGELOG.md` artifact retained for exactly seven days for review. | Does not commit, push, publish, or mutate repository history. |
| `greetings.yml` | Repository maintenance greeting automation. | Runs on issue or PR intake events. | Posts onboarding guidance only. | Not a QA gate, not a reviewer approval, and not deployment automation. |
| `labeler.yml` | Repository maintenance labeling automation. | Runs on pull request path changes. | Applies labels from `.github/labeler.yml`. | Not a QA gate and must not replace CODEOWNERS or human review. |
| `stale.yml` | Repository maintenance stale-item automation. | Runs on scheduled issue or PR maintenance. | Marks or closes stale work according to workflow configuration. | Not a QA gate, not release evidence, and not deployment automation. |

## Boundaries

- `.github` automation provides QA gates and release-evidence automation, not deploy CD.
- Workflows in this directory must not deploy to a live cluster, run direct Kubernetes mutations, mutate external Vault resources, publish containers, or push commits.
