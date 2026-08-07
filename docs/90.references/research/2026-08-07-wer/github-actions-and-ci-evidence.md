---
title: 'GitHub Actions and CI Evidence Reference'
type: content/reference
status: active
owner: platform
updated: 2026-08-07
---

# GitHub Actions and CI Evidence Reference

## Overview

This reference records the GitHub Actions and CI/CD rules this repository is
measured against, the workflow and hook inventory observed on 2026-08-07, and
the separation between repository-static evidence and a hosted run. It covers
workflow syntax, least-privilege `GITHUB_TOKEN`, action pinning, script
injection, supply-chain provenance, the deployment-pipeline and continuous-
integration definitions, the GitOps pull model, and the pre-commit framework.

The repository treats GitHub Actions as a provider-agnostic remote QA gate and
not as deployment CD. That boundary is observable: no workflow contains a
`kubectl`, `argocd`, `helm`, registry push, or kubeconfig step. The
corresponding cost is that no current hosted run PASS exists, so the `ci` and
`remote/live` lanes remain `DEFER`.

This is descriptive Stage 90 reference material. It does not change a workflow,
a validator, a pin, or a lane definition.

### Purpose

- Record source-backed Actions and CI/CD rules with their stated limits.
- Record the exact workflow, pin, and pre-commit inventory observed on
  2026-08-07.
- Record how CI jobs are selected from changed paths and which validator owns
  which rule.
- Separate repository-static evidence from hosted-run evidence, and route each
  observed gap to its owning path.

## Reference Type

- Type: durable-concept / external-standard-snapshot
- Source checked: `2026-08-07`
- Refresh trigger: a change under `.github/`, `.pre-commit-config.yaml`,
  `docs/00.agent-governance/contracts/validation-surfaces.json`, or any CI
  validator in `scripts/`; a GitHub Actions security-guidance change; or the
  first recorded hosted-run PASS.

## Authority Boundary

- **Authoritative for**:
  - Dated external findings checked 2026-08-07 and their stated limits.
  - The `.github` file, trigger, permission, and pin inventory observed
    2026-08-07.
  - The pre-commit hook inventory observed 2026-08-07.
  - The observed repository-static failures listed under Current Defects.
- **Not authoritative for**:
  - Workflow content, pin selection, validator rules, or lane definitions.
    Those belong to `.github/`, `scripts/`, and
    `docs/00.agent-governance/rules/quality-standards.md`.
  - Server-side GitHub state: rulesets, required status checks, run history, or
    organization action policies. No repository file evidences them.
  - Any claim of a current hosted-run PASS. That lane is `DEFER`.
  - Any Argo CD statement. The documentation host returned HTTP 429 on every
    attempt on 2026-08-07.

## Scope

### In Scope

- GitHub Actions syntax, permissions, concurrency, reusable workflows, caching,
  and security hardening as external rules.
- SLSA build levels and GitHub artifact attestation as supply-chain context.
- Deployment-pipeline, continuous-integration, trunk-based, and OpenGitOps
  definitions.
- The pre-commit framework's stage and freeze semantics.
- This repository's `.github` inventory, selection contract, validator
  responsibilities, lane vocabulary, and observed defects.

### Out of Scope

- Changing any workflow, pin, requirement lock, validator, or hook.
- Enabling caching, OIDC, attestation, or reusable workflows.
- Any deployment, push, publish, or cluster action.
- Claiming a hosted run, a ruleset, or a branch protection state.

## Definitions / Facts

### External Rules

**Security hardening**
(<https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions>,
checked 2026-08-07). Pinning to a full-length commit SHA "is currently the only
way to use an action as an immutable release", because an attacker "would need
to generate a SHA-1 collision for a valid Git object payload". `pull_request_target`
and `workflow_run` are privileged triggers that "share the same cache of the
main branch with other privileged workflow triggers, and may have repository
write access and access to referenced secrets"; the guidance is to "Avoid using
the `pull_request_target` workflow trigger if it's not necessary." For script
injection, "The preferred approach to handling untrusted input is to set the
value of the expression to an intermediate environment variable." Self-hosted
runners "do not have guarantees around running in ephemeral clean virtual
machines" and "should almost never be used for public repositories." Secret
redaction is "not guaranteed", and structured secrets are discouraged because
storing them that way "significantly reduces the probability the secrets will be
properly redacted". For the token: "It's good security practice to set the
default permission for the `GITHUB_TOKEN` to read access only for repository
contents."

**Workflow syntax**
(<https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax>,
checked 2026-08-07). `permissions` is settable at workflow or job level, job
level overrides workflow level, and `permissions: {}` disables all access.
`concurrency` takes `group`, `cancel-in-progress`, and `queue: max`, and
`queue: max` cannot combine with `cancel-in-progress: true`. Path filters
`paths` and `paths-ignore` cannot both be used for the same event.

**Reusable workflows**
(<https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows>,
checked 2026-08-07). Requires `on: workflow_call`, the file must live directly
in `.github/workflows/`, nesting is limited to 10 levels, loops are not
permitted, and permissions can only be maintained or reduced down the chain. No
primary source comparing reusable workflows to composite actions was obtained;
no such comparison is asserted here.

**Caching**
(<https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching>,
checked 2026-08-07). `key` is capped at 512 characters; the default limit is
10 GB per repository; entries unused for over 7 days are removed. Low-trust
triggers get read-only access to default-branch caches, which is the documented
cache-poisoning boundary.

**Supply chain.** SLSA v1.0 (<https://slsa.dev/spec/v1.0/levels>, checked
2026-08-07) defines Build L0 as "the lack of SLSA", L1 as documented process
plus distributed provenance that "may be incomplete and/or unsigned", L2 as
signed provenance on dedicated infrastructure preventing post-build tampering,
and L3 as build isolation with secret material inaccessible to user-defined
steps. GitHub artifact attestations
(<https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations>,
checked 2026-08-07) require `id-token: write`, `attestations: write`, and
`contents: read`; the page states no SLSA level, so none is attributed to it
here.

**Pipeline definitions.** A deployment pipeline is "a way to deal with [the
tension between fast builds and comprehensive testing] by breaking up your build
into stages", where the same compiled artifact progresses through each stage
(<https://martinfowler.com/bliki/DeploymentPipeline.html>, checked 2026-08-07).
Continuous integration's practices include a self-testing build, daily mainline
commits, automated verification per mainline commit, immediate build fixes, and
"a ten minute build"
(<https://martinfowler.com/articles/continuousIntegration.html>, checked
2026-08-07). Trunk-based development is collaboration "in a single branch called
'trunk'" with short-lived branches (<https://trunkbaseddevelopment.com/>,
checked 2026-08-07); no specific branch lifetime in days was found on the page,
so none is quoted.

**GitOps.** OpenGitOps v1.0.0 (<https://opengitops.dev/>, checked 2026-08-07)
states four principles: declarative desired state; storage that "enforces
immutability, versioning and retains a complete version history"; "Software
agents automatically pull the desired state declarations from the source"; and
continuous reconciliation. The rule that CI must not push to the cluster is an
inference from principle three plus this repository's own policy, not a quoted
prohibition. Argo CD documentation was unreachable (HTTP 429 on four attempts
across three URLs on 2026-08-07), so no Argo CD statement is cited.

**pre-commit** (<https://pre-commit.com/>, checked 2026-08-07). `manual` is "a
special stage which will not be automatically triggered by any git hook".
`pre-commit run --all-files` runs every hook against every file and is the
recommended CI form. `pre-commit autoupdate --freeze` stores frozen hashes for
reproducible builds. `files` and `exclude` are Python regexes matched with
`re.search()`.

### Workflow Inventory Observed 2026-08-07

`.github/` contains `CODEOWNERS`, `README.md`, `SECURITY.md`,
`PULL_REQUEST_TEMPLATE.md`, `dependabot.yml`, `labeler.yml`, three
`ISSUE_TEMPLATE/` files, two `requirements/` files, and five workflows. There is
no `.github/actions/` directory and no `.github/zizmor.yml`.

| Workflow                 | Triggers                                              | Workflow permissions | Concurrency                              | Jobs (timeout, minutes)                                                                                                                                                     | Job write permissions                   |
| ------------------------ | ----------------------------------------------------- | -------------------- | ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| `ci.yml`                 | `push` main, `pull_request` main, `workflow_dispatch` | `contents: read`     | `ci-${{ github.ref }}`, cancel           | `branch-policy` (5), `changes` (5), `pre-commit` (20), `repo-quality-static` (10), `agent-governance-static` (10), `manifest-static` (10), `ci-summary` (5, `if: always()`) | none                                    |
| `generate-changelog.yml` | `push` tags `v*.*.*`                                  | `contents: read`     | `changelog-${{ github.ref }}`, no cancel | `changelog` (10)                                                                                                                                                            | none                                    |
| `labeler.yml`            | `pull_request` opened, synchronize                    | `contents: read`     | per PR, cancel                           | `label` (5)                                                                                                                                                                 | `pull-requests: write`                  |
| `greetings.yml`          | `pull_request` opened, `issues` opened                | `contents: read`     | per PR or issue, cancel                  | `greeting` (5)                                                                                                                                                              | `issues: write`, `pull-requests: write` |
| `stale.yml`              | `schedule` daily                                      | `contents: read`     | `stale-maintenance`, cancel              | `stale` (10)                                                                                                                                                                | `issues: write`, `pull-requests: write` |

Every remote `uses:` is a full 40-character commit SHA with a trailing version
comment. `pull_request_target` is not used anywhere. No job runs on a
self-hosted runner. Every `actions/checkout` step sets
`persist-credentials: false`. Every `run:` block that consumes event context
routes it through an `env:` variable, matching the script-injection guidance.

Python dependencies install from a fully hashed lock with
`--only-binary :all: --require-hashes`. Gitleaks 8.30.0 is downloaded and
verified with `sha256sum --check --strict` before installation.

### Selection Contract

`docs/00.agent-governance/contracts/validation-surfaces.json` (schemaVersion 2)
declares 21 validators, 24 path surfaces, and 4 CI jobs mapped to workflow
outputs: `agent-governance-static` to `agent_governance`, `manifest-static` to
`manifests`, `pre-commit` to `precommit`, and `repo-quality-static` to
`repo_quality`. Matching is exact or anchored regex with `precedence: none`, so
routes must be unambiguous, and every surface carries a fail-closed fallback.

The `ci.yml` `changes` job computes a NUL-delimited changed-path set per event
and passes it to `scripts/select-affected-surfaces.py`, which emits
`<output>=true|false` per declared CI job. A path that matches no surface emits
`SURFACE-PATH-UNMATCHED` and exits 1, so an unrouted new file breaks CI by
design. Git ranges use `--no-renames` so both the old and the new path retain
their gates.

`scripts/run-validation-lane.py` executes contract-approved validators under one
reviewed envelope: 1,200 seconds per child, 4 MiB retained stdout and 1 MiB
stderr, a 2-second cleanup deadline, and 64 KiB read chunks with concurrent
draining. Each child runs in its own session and process group; timeout, pipe
overflow, or pipes held by descendants is `FAIL`. Evidence lines expose only
byte counts, digests, completion flags, boundary status, and return code.

Validator ownership is split. `validate-github-actions-security.py` owns pin
form, permission shape, and artifact retention.
`validate-agent-governance-ci.py` owns CI topology, the summary truth table, and
the governance-lane checkout identity. `validate-ci-python-contract.py` owns the
Python lock, the exact install command, gitleaks provenance, the pre-commit
command string, `fetch-depth: 0` on the `pre-commit` and `repo-quality-static`
checkouts, and the frozen pre-commit revisions.
`validate-affected-surfaces.py` owns the contract itself and reconciles it
against `ci.yml`.

### Lane Vocabulary

`docs/00.agent-governance/rules/quality-standards.md` is the sole owner. The
lanes are `affected`, `staged`, `all-files`, `message/manual`, `ci`, and
`remote/live`. Only `pre-commit run --all-files` counts as all-files evidence,
and it does not prove `commit-msg` or `manual` stages. Results are `PASS`,
`SKIP`, `FAIL`, and `DEFER`, where "`DEFER` is a visible limitation, never a
pass". The completion sequence is `targeted`, `affected`, `staged`, `tests`,
`all-files`, `formatter-review`, `rerun`, `diff-checks`.

### Hosted-Run and CD Posture

No workflow performs deployment. A grep of `.github/` for `kubectl`, `argocd`,
`helm`, `docker push`, `kubeconfig`, or `registry` matches only prose in
`README.md`, `SECURITY.md`, `PULL_REQUEST_TEMPLATE.md`, and an issue template —
never a `run:` or `uses:`.

No current hosted-run PASS is recorded anywhere in the repository. The only
concrete run identifier in tracked files is hosted run `29982910320`, recorded
as a historical FAIL for an older commit. `.github/PULL_REQUEST_TEMPLATE.md`
requires a run identity per PR, but no run URL is stored. Branch protection and
ruleset state have no repository-file evidence and remain `DEFER`.

### Current Defects Observed 2026-08-07

`bash scripts/validate-repo-quality-gates.sh .` fails on a clean checkout. The
observed errors, none of which is caused by this reference, are:

| Error                   | Detail                                                                                                                                                                                         |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Stale absolute path     | An absolute host path appears in `docs/04.execution/plans/2026-08-02-repository-assurance-integration-and-closure.md`                                                                          |
| Checkout step count     | `ci.yml` `changes` and `manifest-static` jobs each report "must have exactly one pinned checkout step"                                                                                         |
| Action version conflict | `actions/checkout` is pinned to two different SHAs within `ci.yml`, as is `actions/setup-python`                                                                                               |
| Inventory drift         | `docs/90.references/data/tech-stack-version-inventory.md` records different SHAs than the workflows use for `actions/checkout`, `actions/setup-python`, `actions/labeler`, and `actions/stale` |

Two further errors, `CI-PRECOMMIT-HISTORY` and `CI-REPOSITORY-HISTORY`, were
present on a clean checkout and were resolved by adding `fetch-depth: 0` to the
`pre-commit` and `repo-quality-static` checkout steps, which
`validate-ci-python-contract.py` requires because gitleaks needs full history.

### Gap Routing

| ID    | Gap                                                                                                                                                                                                                             | Owning path                                                                                                                                           |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| CI-G1 | Action pin conflicts and inventory drift block the repository quality gate                                                                                                                                                      | `.github/workflows/ci.yml`, `.github/workflows/labeler.yml`, `.github/workflows/stale.yml`, `docs/90.references/data/tech-stack-version-inventory.md` |
| CI-G2 | Dependabot covers only `github-actions`; the hashed Python lock has no ecosystem entry, so refreshes are manual                                                                                                                 | `.github/dependabot.yml`                                                                                                                              |
| CI-G3 | The pip-install block is duplicated four times and the gitleaks install twice; no reusable workflow or composite action exists. Any refactor must update the exact command strings asserted by `validate-ci-python-contract.py` | `.github/workflows/ci.yml`, `scripts/validate-ci-python-contract.py`                                                                                  |
| CI-G4 | No dependency caching. The trade-off is real: caching would reintroduce the documented poisoning surface, so the decision should be explicit rather than by omission                                                            | `.github/workflows/ci.yml`                                                                                                                            |
| CI-G5 | No provenance or attestation. Currently `DEFER` because nothing is published; it becomes binding if container or artifact publishing is added                                                                                   | `.github/workflows/generate-changelog.yml`                                                                                                            |
| CI-G6 | Branch protection and ruleset intent is unverifiable from the repository and is not recorded anywhere as intended state                                                                                                         | `.github/README.md`                                                                                                                                   |
| CI-G7 | No Argo CD primary source was obtainable; the no-push-from-CI rule rests on OpenGitOps principle three plus local policy                                                                                                        | This reference; re-attempt the fetch before promoting the claim                                                                                       |
| CI-G8 | `language: system` may be renamed upstream to `language: unsupported`; a single fetch did not establish whether this is a rename with back-compatibility or a break                                                             | `.pre-commit-config.yaml`; verify against the pre-commit changelog first                                                                              |

## Sources

- <https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions>
  checked 2026-08-07. Adopted: SHA pinning, privileged-trigger risk, script
  injection mitigation, self-hosted runner risk, secret handling, and token
  least privilege. Rejected: any statement about this repository.
- <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax>
  checked 2026-08-07. Adopted: permission scopes and precedence, concurrency,
  and path-filter constraints. Rejected: any security requirement; it is a
  syntax reference.
- <https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows>
  checked 2026-08-07. Adopted: `workflow_call` requirements, the 10-level
  nesting limit, and permission narrowing. Rejected: any comparison to
  composite actions, which the page does not make.
- <https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching>
  checked 2026-08-07. Adopted: key and size limits, eviction, and the
  cache-poisoning trust boundary.
- <https://docs.github.com/en/actions/concepts/security/github_token> checked
  2026-08-07. Adopted: token lifetime and the recursion guard.
- <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets>
  checked 2026-08-07. Adopted: the rule names and the strict-versus-loose
  status-check distinction. Rejected: any claim about this repository's
  configured rulesets.
- <https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations>
  checked 2026-08-07. Adopted: required permissions and the verify command.
  Rejected: any SLSA level; the page states none.
- <https://slsa.dev/spec/v1.0/levels> checked 2026-08-07. Adopted: Build L0
  through L3 definitions. Rejected: source-track claims.
- <https://martinfowler.com/bliki/DeploymentPipeline.html> and
  <https://martinfowler.com/articles/continuousIntegration.html> checked
  2026-08-07. Adopted: the staged-pipeline definition and the CI practice list.
- <https://trunkbaseddevelopment.com/> checked 2026-08-07. Adopted: the trunk
  definition. Rejected: any specific branch lifetime in days; the page states
  none.
- <https://opengitops.dev/> checked 2026-08-07. Adopted: the four principles.
  Rejected: a quoted prohibition on CI pushing to a cluster; that is inference.
- <https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/> returned
  HTTP 429 on four attempts on 2026-08-07. Unreachable; no claim is made from
  it.
- <https://pre-commit.com/> checked 2026-08-07. Adopted: stage semantics,
  `--all-files`, `--freeze`, and regex matching. Flagged: the
  `language: system` naming note, unresolved.
- Repository evidence read 2026-08-07: all files under `.github/`,
  `.pre-commit-config.yaml`,
  `docs/00.agent-governance/contracts/validation-surfaces.json`,
  `docs/00.agent-governance/rules/quality-standards.md`,
  `docs/90.references/data/tech-stack-version-inventory.md`, and the CI
  validators in `scripts/`.

## Review and Freshness

- Review on any change under `.github/`, `.pre-commit-config.yaml`, the
  validation-surface contract, or a CI validator.
- The defect list is a dated observation of a repository-static run. Re-run
  `bash scripts/validate-repo-quality-gates.sh .` rather than reusing it.
- GitHub documentation is a living surface. These findings are observation-time
  evidence for current guidance, not dated snapshots.
- The `ci` lane here is repository-static only. A hosted-run PASS needs its own
  check URL or run identity, and `remote/live` stays `DEFER`.

## Related Documents

- [Research Pack Index](README.md)
- [Automation, Pipeline, Workflow, and QA Reference](../2026-07-07-wer/automation-pipeline-workflow-qa.md)
- [Spec, SDLC, CI, QA, and Formatting Reference](../2026-07-07-wer/spec-sdlc-ci-qa-formatting.md)
- [Kubernetes, Infrastructure, and Security Reference](../2026-07-07-wer/kubernetes-infrastructure-security.md)
- [Agent Quality Standards](../../../00.agent-governance/rules/quality-standards.md)
