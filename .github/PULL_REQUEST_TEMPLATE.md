# PULL REQUEST TEMPLATE

## 1. Description

A clear and concise description of the changes being proposed.

## 2. Related Issue

Fixes # (link to issue if applicable)

## 3. Branch Target

- [ ] This PR targets `main`; any exception must update CI `branch-policy` and governance in the same change.
- [ ] No PR targeting `main` bypasses CI or branch-policy checks.
- [ ] Draft/WIP status is intentional; this PR is not ready for review or merge until required checks pass and verification evidence is complete.
- [ ] The source branch uses an approved prefix: `feat/`, `fix/`, `docs/`, `refactor/`, `test/`, `chore/`, `ci/`, `release/`, `hotfix/`, `codex/`, or `dependabot/`.
- [ ] CI `branch-policy` validates pull request shape; GitHub branch protection/rulesets enforce direct-push restrictions.

## 4. Type of Change

- [ ] `feat`: New feature or enhancement
- [ ] `fix`: Bug fix
- [ ] `refactor`: Code reorganization
- [ ] `docs`: Documentation updates
- [ ] `test`: Tests or validation updates
- [ ] `chore`: Maintenance updates
- [ ] `infra`: Changes to Kubernetes manifests or GitOps assets
- [ ] `ci`: Changes to GitHub Actions, hooks, or automation

Note: `infra` is a change type, not an approved branch prefix. Use an approved source branch prefix above.

## 5. Breaking Changes

- [ ] Yes
- [ ] No

If yes, please describe the impact and migration path.

## 6. How Has This Been Tested?

Describe the manual verification or automated tests conducted.

- [ ] Relevant `pre-commit` hooks passed locally
- [ ] GitHub CI quality gates (`branch-policy`, `repo-quality-static`, `manifest-static`) passed
- [ ] ArgoCD/GitOps impact reviewed (if applicable)
- [ ] Workflow path filters and job ownership reviewed (if `.github` automation changed)
- [ ] Documentation changes preserve current implementation contracts; obsolete or conflicting 01-04 docs are routed through `docs/98.archive/README.md` only.
- [ ] Cloud example changes under `examples/aws` or `examples/azure` preserve Cloud Example Snapshot boundaries unless an approved provider refresh spec exists.
- [ ] Coverage policy reviewed: 90% target for future testable application code where applicable; source-code test surfaces own coverage evidence, while Bash/YAML/Markdown infrastructure changes use validation-matrix evidence instead of application coverage claims
- [ ] No live cluster mutation, `kubectl apply`, or external Vault mutation was introduced
- [ ] Tracked changelog updates were merged by PR before tagging (if release-facing)

## 7. Checklist

- [ ] My change follows the governance and workflow rules in `AGENTS.md` and `docs/00.agent-governance/`.
- [ ] I have updated the documentation accordingly.
- [ ] My commit messages follow Conventional Commits.
- [ ] I did not introduce plaintext secrets. Secret-related changes use GitOps-approved patterns only.

## 8. Harness Impact

- [ ] No harness surface changed
- [ ] `gitops/**` changed
- [ ] `infrastructure/**` changed
- [ ] `scripts/**` validation, hook, or policy gate changed
- [ ] `.github/workflows/**` changed
- [ ] `docs/00.agent-governance/**` changed
- [ ] `docs/05.operations/**` changed
- [ ] Secret, Vault, ExternalSecret, SecretStore, or ClusterSecretStore contract changed
- [ ] Bootstrap-only behavior changed
- [ ] Live runtime evidence is required

If any harness surface changed, record exact static validation evidence:

```bash
bash scripts/validate-harness.sh
bash infrastructure/tests/verify-contracts-static.sh
```

Live checks, only when explicitly approved:

```bash
bash infrastructure/tests/run-all.sh
```

Secret handling:

- [ ] No secret values, Vault tokens, private keys, or credential material are included
- [ ] Secret-related changes record only path, key, property, mount, and redacted evidence

See [Approval Boundaries](../docs/00.agent-governance/rules/approval-boundaries.md) and the [Harness Implementation Map](../docs/00.agent-governance/harness-implementation-map.md).
