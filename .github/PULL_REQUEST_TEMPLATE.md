# PULL REQUEST TEMPLATE

## 1. Description

A clear and concise description of the changes being proposed.

## 2. Related Issue

Fixes # (link to issue if applicable)

## 3. Branch Target

- [ ] This PR targets `main`, unless a documented release or hotfix flow requires otherwise.

## 4. Type of Change

- [ ] `feat`: New feature or enhancement
- [ ] `fix`: Bug fix
- [ ] `refactor`: Code reorganization
- [ ] `docs`: Documentation updates
- [ ] `infra`: Changes to Kubernetes manifests or GitOps assets
- [ ] `ci`: Changes to GitHub Actions, hooks, or automation

## 5. Breaking Changes

- [ ] Yes
- [ ] No

If yes, please describe the impact and migration path.

## 6. How Has This Been Tested?

Describe the manual verification or automated tests conducted.

- [ ] Relevant `pre-commit` hooks passed
- [ ] `bash scripts/validate-gitops-structure.sh` successful (if GitOps assets changed)
- [ ] `bash scripts/validate-k8s-manifests.sh .` successful (if manifests changed)
- [ ] `bash scripts/check-secret-handling.sh .` successful (if manifests or secret wiring changed)
- [ ] ArgoCD/GitOps impact reviewed (if applicable)
- [ ] Tracked changelog updates were merged by PR before tagging (if release-facing)

## 7. Checklist

- [ ] My change follows the governance and workflow rules in `AGENTS.md` and `docs/00.agent-governance/`.
- [ ] I have updated the documentation accordingly.
- [ ] My commit messages follow Conventional Commits.
- [ ] I did not introduce plaintext secrets. Secret-related changes use GitOps-approved patterns only.
