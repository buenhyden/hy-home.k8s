# GitHub Configuration Hub

This directory contains repository-specific GitHub automation for the `hy-home.k8s` main-branch PR flow.
It is a map and routing surface, not the policy source of truth.

## Content Mapping

- `workflows/` - CI, release evidence, and repository maintenance automations.
- `ISSUE_TEMPLATE/` - Structured bug and feature intake forms.
- `PULL_REQUEST_TEMPLATE.md` - PR verification checklist aligned with `docs/01.requirements/`, `docs/02.architecture/requirements/`, `docs/03.specs/`, and GitOps QA.
- `CODEOWNERS` - Review ownership for repository paths and GitHub configuration.
- `dependabot.yml`, `labeler.yml`, `zizmor.yml` - GitHub-native dependency, labeling, and workflow hardening configuration.
- `SECURITY.md` - Vulnerability reporting instructions.

## Policy Routing

- Branch strategy policy lives in `docs/00.agent-governance/rules/git-workflow.md`.
- CI enforcement lives in `workflows/ci.yml` and `scripts/validate-repo-quality-gates.sh`.
- `ci.yml` validates pull request shape; GitHub branch protection/rulesets enforce direct-push restrictions outside repo-local files.
- PR author and reviewer prompts live in `PULL_REQUEST_TEMPLATE.md`.
- Version inventory and action tag policy live in `docs/90.references/versions/tech-stack-version-inventory.md`.

## Workflow Roles

- `ci.yml` is the required QA gate for pushes and pull requests targeting the repository's canonical integration branch, with manual reruns through `workflow_dispatch`.
- `generate-changelog.yml` creates release-evidence artifacts for version tags. It does not commit, push, or publish.
- `labeler.yml`, `greetings.yml`, and `stale.yml` are repository maintenance automations, not QA gates.
- Defensive overlap between CI jobs is intentional QA coverage, not prose duplication.

## Boundaries

- `.github` automation provides QA gates and release-evidence automation, not deploy CD.
- Workflows in this directory must not deploy to a live cluster, run direct Kubernetes mutations, mutate external Vault resources, publish containers, or push commits.
