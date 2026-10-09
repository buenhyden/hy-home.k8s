# PULL REQUEST TEMPLATE

## 1. Description

A clear and concise description of the changes being proposed.

## 2. Related Issue

Fixes # (link to issue if applicable)

## 3. Branch Target

- [ ] This PR targets `main`; any exception must update CI `ci-summary` and governance in the same change.
- [ ] No PR targeting `main` bypasses the CI metadata check.
- [ ] Draft/WIP status is intentional; this PR is not ready for review or merge until required checks pass and verification evidence is complete.
- [ ] The source branch uses an approved prefix: `feat/`, `fix/`, `docs/`, `refactor/`, `test/`, `chore/`, `ci/`, `release/`, `hotfix/`, `codex/`, or `dependabot/`.
- [ ] CI `ci-summary` validates pull request branch metadata; check the dated main protection read-back for required checks and administrator bypass.

## 4. Change Review Categories

Select every category that applies to this PR. These categories route review;
they do not define commit-message types. [`.cz.toml`](../.cz.toml) owns the
supported commit types and message syntax, and
[Git policy](../.agents/governance/git.md) explains their validation.

- [ ] `feat`: New feature or enhancement
- [ ] `fix`: Bug fix
- [ ] `refactor`: Code reorganization
- [ ] `docs`: Documentation updates
- [ ] `test`: Tests or validation updates
- [ ] `chore`: Maintenance updates
- [ ] `infra`: Changes to Kubernetes manifests or GitOps assets
- [ ] `ci`: Changes to GitHub Actions, hooks, or automation

Note: `infra` is a PR review category, not an approved branch prefix or a
Commitizen type. Use an approved source branch prefix above.

## 5. Breaking Changes

- [ ] Yes
- [ ] No

If yes, please describe the impact and migration path.

## 6. How Has This Been Tested?

Describe the manual verification or automated tests conducted.

Follow the [Quality Policy](../.agents/governance/quality.md#canonical-completion-sequence)
for the delivery route and evidence required for this PR. Link the owning Task's
selected local purpose checks and exact-index staged result on their actual
inputs. Link both hosted `ci-summary` and `style-pr` results with each PR SHA
and run identity when observed. This workflow does not run local purpose or
document-content QA. Live evidence remains `DEFER` without direct observation
and a named next owner.
Link the owning Task for execution status, acceptance, and check evidence;
do not copy its progress or outcomes into this PR description.

- [ ] ArgoCD/GitOps impact reviewed (if applicable)
- [ ] Workflow triggers and job ownership reviewed (if `.github` automation changed)
- [ ] Documentation changes preserve current implementation contracts; obsolete or conflicting numbered stage docs are routed through `docs/98.archive/README.md` only.
- [ ] Cloud example changes under `examples/aws` or `examples/azure` preserve each provider README and adjacent executable assets as one boundary; they are not live provider-latest guidance unless an approved provider refresh spec exists.
- [ ] Coverage policy reviewed: apply the approved target where testable application code exists; Bash/YAML/Markdown infrastructure changes use applicable purpose and contract checks instead of application coverage claims
- [ ] Every validation lane is explicitly classified as `PASS`, `NOT_RUN`, `FAIL`, `DEFER`, or `NOT_APPLICABLE`.
- [ ] No live cluster mutation or external Vault mutation was introduced
- [ ] Tracked changelog updates were merged by PR before tagging (if release-facing)

## 7. Checklist

- [ ] My change follows the governance and workflow rules in `AGENTS.md` and `.agents/`.
- [ ] I have updated the documentation accordingly.
- [ ] My commit messages follow Conventional Commits.
- [ ] I did not introduce plaintext secrets. Secret-related changes use GitOps-approved patterns only.

## 8. Harness Impact

- [ ] No harness surface changed
- [ ] `gitops/**` changed
- [ ] `infrastructure/**` changed
- [ ] `scripts/**` validation, hook, or policy gate changed
- [ ] `.github/workflows/**` changed
- [ ] `.agents/**` changed
- [ ] `docs/05.operations/**` changed
- [ ] Secret, Vault, ExternalSecret, SecretStore, or ClusterSecretStore contract changed
- [ ] Bootstrap-only behavior changed
- [ ] Live runtime evidence is required

For harness changes, record the applicable local checks and hosted result under
[Quality Policy](../.agents/governance/quality.md). Live checks require explicit
operator approval.

Secret handling:

- [ ] No secret values, Vault tokens, private keys, or credential material are included
- [ ] Secret-related changes record only path, key, property, mount, and redacted evidence

See [Approval Boundaries](../.agents/governance/approval-and-safety.md) and the [Local Harness Catalog](../.agents/roles/README.md).
