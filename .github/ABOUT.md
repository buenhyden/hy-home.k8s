# GitHub Configuration Hub

This directory contains repository-specific GitHub automation for the `hy-home.k8s` main-branch PR flow.

## Content Mapping

- `workflows/` - CI, release evidence, and repository maintenance automations.
- `ISSUE_TEMPLATE/` - Structured bug and feature intake forms.
- `PULL_REQUEST_TEMPLATE.md` - PR verification checklist aligned with `docs/01.prd/`, `docs/02.ard/`, `docs/04.specs/`, and GitOps QA.
- `CODEOWNERS` - Review ownership for repository paths and GitHub configuration.
- `dependabot.yml`, `labeler.yml`, `zizmor.yml` - GitHub-native dependency, labeling, and workflow hardening configuration.
- `SECURITY.md` - Vulnerability reporting instructions.

## Workflow Roles

- `ci.yml` is the required quality gate for pushes and pull requests targeting `main`. `pre-commit` owns broad lint, formatting, and security hooks; `repo-quality-static` owns repository structure, workflow duplication, script references, and version inventory drift; `manifest-static` owns k3d/GitOps contract checks; `shell-static` performs Bash syntax checks only.
- `generate-changelog.yml` runs on `v*.*.*` tags and stores changelog evidence as a workflow artifact. It does not commit or push to `main`.
- `labeler.yml`, `greetings.yml`, and `stale.yml` are repository maintenance automations, not QA gates.

## Branch and Release Rules

- Default PR target is `main`; long-lived `dev` or `develop` branches are not assumed.
- Tracked changelog updates must be merged by PR before tagging.
- GitHub Actions use version tags plus `docs/90.references/tech-stack-version-inventory.md` drift checks. Full SHA pinning is not the current repository policy.
- Workflows in this directory must not deploy to a live cluster, run `kubectl apply`, or mutate external Vault resources.
