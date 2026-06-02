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
- `repo-quality-static` also enforces `docs/98.archive` stage-indexed Tombstone structure, `05.operations` archive mirror coverage, and active-doc stale runtime/OIDC/hook/CI currentness rejection.
- `ci.yml` validates pull request shape; GitHub branch protection/rulesets enforce direct-push restrictions outside repo-local files.
- PR author and reviewer prompts live in `PULL_REQUEST_TEMPLATE.md`.
- Version inventory and action tag policy live in `docs/90.references/versions/tech-stack-version-inventory.md`.

## Workflow Roles

- `ci.yml` is the required QA gate for pushes and pull requests targeting the repository's canonical integration branch, with manual reruns through `workflow_dispatch`.
- `generate-changelog.yml` creates release-evidence artifacts for version tags. It does not commit, push, or publish.
- `labeler.yml`, `greetings.yml`, and `stale.yml` are repository maintenance automations, not QA gates.
- Clear separation of concerns is maintained: Local environment handles fast pre-commit linting and formatting, while GitHub CI handles heavy structural validation, template rendering, and policy gates. Redundant execution is avoided where possible.

## Workflow Responsibility Matrix

| Workflow | Role | Trigger / scope | Required evidence | Boundary |
| --- | --- | --- | --- | --- |
| `ci.yml` | Required QA gate for branch policy, repo-quality, manifest, secret checks. | Runs on `push`, `pull_request`, and `workflow_dispatch` for `main`-centered integration. | `ci-summary` aggregates `branch-policy`, `changes`, `pre-commit`, `repo-quality-static`, and `manifest-static`; repo-quality includes `.agents/**` shared asset changes, archive Tombstone/currentness checks, Headlamp OIDC stale-contract rejection, and template enforcement. | No deploy CD, direct Kubernetes mutation, external Vault mutation, container publish, or commit push. |
| `generate-changelog.yml` | Release-evidence artifact generator. | Runs for release tag evidence and manual release support. | Produces `CHANGELOG.md` artifact for review. | Does not commit, push, publish, or mutate repository history. |
| `greetings.yml` | Repository maintenance greeting automation. | Runs on issue or PR intake events. | Posts onboarding guidance only. | Not a QA gate, not a reviewer approval, and not deployment automation. |
| `labeler.yml` | Repository maintenance labeling automation. | Runs on pull request path changes. | Applies labels from `.github/labeler.yml`. | Not a QA gate and must not replace CODEOWNERS or human review. |
| `stale.yml` | Repository maintenance stale-item automation. | Runs on scheduled issue or PR maintenance. | Marks or closes stale work according to workflow configuration. | Not a QA gate, not release evidence, and not deployment automation. |

## Boundaries

- `.github` automation provides QA gates and release-evidence automation, not deploy CD.
- Workflows in this directory must not deploy to a live cluster, run direct Kubernetes mutations, mutate external Vault resources, publish containers, or push commits.
