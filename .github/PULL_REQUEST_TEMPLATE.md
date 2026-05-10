# PULL REQUEST TEMPLATE

## 1. Description

A clear and concise description of the changes being proposed.

## 2. Related Issue

Fixes # (link to issue if applicable)

## 3. Branch Target

- [ ] This PR targets `main`; any exception must update CI `branch-policy` and governance in the same change.
- [ ] The source branch uses an approved prefix: `feat/`, `fix/`, `docs/`, `refactor/`, `chore/`, `ci/`, `release/`, `hotfix/`, `codex/`, or `dependabot/`.
- [ ] CI `branch-policy` validates pull request shape; GitHub branch protection/rulesets enforce direct-push restrictions.

## 4. Type of Change

- [ ] `feat`: New feature or enhancement
- [ ] `fix`: Bug fix
- [ ] `refactor`: Code reorganization
- [ ] `docs`: Documentation updates
- [ ] `infra`: Changes to Kubernetes manifests or GitOps assets
- [ ] `ci`: Changes to GitHub Actions, hooks, or automation

Note: `infra` is a change type, not an approved branch prefix. Use an approved source branch prefix above.

## 5. Breaking Changes

- [ ] Yes
- [ ] No

If yes, please describe the impact and migration path.

## 6. How Has This Been Tested?

Describe the manual verification or automated tests conducted.

- [ ] Relevant `pre-commit` hooks passed
- [ ] `bash scripts/validate-repo-quality-gates.sh .` successful (if docs, workflows, scripts, or governance changed)
- [ ] `bash infrastructure/tests/verify-contracts-static.sh` successful (if GitOps contracts or manifests changed)
- [ ] `bash scripts/validate-gitops-structure.sh` successful (if GitOps assets changed)
- [ ] `bash scripts/validate-k8s-manifests.sh .` successful (if manifests changed)
- [ ] `bash scripts/check-secret-handling.sh .` successful (if manifests or secret wiring changed)
- [ ] ArgoCD/GitOps impact reviewed (if applicable)
- [ ] Workflow path filters and job ownership reviewed (if `.github` automation changed)
- [ ] No live cluster mutation, `kubectl apply`, or external Vault mutation was introduced
- [ ] Tracked changelog updates were merged by PR before tagging (if release-facing)

## 7. Checklist

- [ ] My change follows the governance and workflow rules in `AGENTS.md` and `docs/00.agent-governance/`.
- [ ] I have updated the documentation accordingly.
- [ ] My commit messages follow Conventional Commits.
- [ ] I did not introduce plaintext secrets. Secret-related changes use GitOps-approved patterns only.
