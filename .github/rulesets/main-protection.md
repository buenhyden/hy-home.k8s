# Main Branch Protection Intended State and Recovery

This file is a local record of the intended GitHub settings for `main` in
`buenhyden/hy-home.k8s`. It is not an agent instruction surface and does not
apply remote repository settings by itself. Nothing here is evidence that a
setting is in force; only a dated authenticated read-back is.

## Observation Boundary

- **An authenticated read-back was recorded on 2026-09-10 by the account
  `buenhyden`.** `gh api repos/buenhyden/hy-home.k8s/rulesets` and
  `gh api repos/buenhyden/hy-home.k8s/rules/branches/main` both returned `[]`
  at that time. Classic branch protection was read from
  `gh api repos/buenhyden/hy-home.k8s/branches/main/protection`. The original
  fields and the correction that followed are retained below as dated history.
- **A new authenticated read-back was recorded on 2026-10-09 by `buenhyden`.**
  Classic protection, applied branch rules, inherited rulesets, main HEAD and a
  prior PR's check runs were read separately. The current observation is below;
  the prior PR run does not test a later candidate.
- A read-back belongs in the active Task with its date, the exact fields read,
  and the account that read them, and this file may then carry the claim. The
  2026-09-10 reading was taken with no Stage 03 package open, so its date,
  fields and account are carried here instead. The 2026-10-09 read-back is
  routed through [Stage 03 navigation](../../docs/03.specs/README.md) to the
  current QA execution record `SPEC-0107-TSK-0003`.
- Evidence from another repository does not transfer. This file previously
  carried required-check names, a workflow-contract path, a governance path, a
  Spec reference and `gh api` targets that belong to the sibling
  `hy-home.docker` workspace; none of them exist here, and none of them
  described this repository's protection.
- Environment, deployment, release, and unobserved control-plane state remain
  `unverified` unless an approved observation records them.

## Historical 2026-09-10 State

Read on 2026-09-10 from `branches/main/protection` by `buenhyden`, before the
correction recorded below. This is point-in-time evidence for that moment and
for those fields only.

| Field | Observed | Then-target row | Agreement at the time |
| --- | --- | --- | --- |
| `required_pull_request_reviews` | present | Require pull requests before merge | matches |
| `required_pull_request_reviews.required_approving_review_count` | `0` | Require zero approving reviews | matches |
| `required_pull_request_reviews.require_code_owner_reviews` | `false` | Do not require CODEOWNERS review | matches |
| `required_status_checks.contexts` | `["ci-summary"]`, `app_id` `15368` | Require `ci-summary` alone | matches |
| `allow_force_pushes.enabled` | `false` | Block force pushes | matches |
| `allow_deletions.enabled` | `false` | Block branch deletion | matches |
| `required_linear_history.enabled` | `false` | Do not enforce linear history | matches |
| `required_conversation_resolution.enabled` | `false` | Require conversations to be resolved before merge | **contradicts** |
| `required_status_checks.strict` | `false` | Require the latest branch head to pass required checks | **contradicts** |
| `enforce_admins.enabled` | `false` | no row states an expectation | **unstated** |

Also observed and unstated by the then-target: `required_signatures.enabled`
`false`, `block_creations.enabled` `false`, `lock_branch.enabled` `false`,
`allow_fork_syncing.enabled` `false`,
`required_pull_request_reviews.dismiss_stale_reviews` `false`, and
`required_pull_request_reviews.require_last_push_approval` `false`.

`enforce_admins` being `false` is why a direct push to `main` by the repository
owner succeeded on 2026-09-10 while the remote reported bypassed rule
violations for the pull-request requirement and the `ci-summary` check. The
rules were configured and not applied to administrators. The then-target had
no expectation for that field; the decision added later appears below.

### 2026-09-10 correction and re-read

The two contradictions above were corrected on 2026-09-10 by `buenhyden` with
`gh api -X PUT repos/buenhyden/hy-home.k8s/branches/main/protection`, after the
reading above was captured as the before-state. A re-read of the same endpoint
confirms the result:

| Field | Before | After |
| --- | --- | --- |
| `required_status_checks.strict` | `false` | `true` |
| `required_conversation_resolution.enabled` | `false` | `true` |

Eleven fields were sent at their observed values and re-read unchanged:
`required_status_checks.contexts`, `enforce_admins`,
`required_approving_review_count`, `require_code_owner_reviews`,
`allow_force_pushes`, `allow_deletions`, `required_linear_history`,
`block_creations`, `lock_branch`, `allow_fork_syncing` and
`required_signatures`. The endpoint replaces the whole object, so sending them
explicitly is what preserved them.

`enforce_admins` was not changed. The target now states an expectation for
it, so the field is no longer unstated; what remains is a recorded operating
decision rather than a difference from intent.

Every row above is evidence for 2026-09-10 only. A later claim of enforcement
needs a new authenticated read-back.

## Observed State

### Current 2026-10-09 Observation

The account `buenhyden` read
`repos/buenhyden/hy-home.k8s/branches/main/protection`,
`repos/buenhyden/hy-home.k8s/rules/branches/main`, and
`repos/buenhyden/hy-home.k8s/rulesets?includes_parents=true`. The read-back
also identified main HEAD `5cfd420b723cba7417a0d24c8abb94c4f329caa9`.
These are remote observations at that revision, not validation of later local
commits.

| Field | Observed on 2026-10-09 | Consequence |
| --- | --- | --- |
| `required_status_checks.strict` | `true` | Required checks use the latest branch input. |
| `required_status_checks.checks` | `ci-summary` and `style-pr`, each from GitHub Actions App `15368` | Both named PR results are required separately. `qa-provenance` is no longer required. |
| `required_pull_request_reviews.required_approving_review_count` / `require_code_owner_reviews` | `0` / `false` | A CODEOWNERS entry alone is not a required review. |
| `enforce_admins.enabled` | `false` | Administrator bypass remains possible. |
| Applied branch rules | `[]` | No branch ruleset adds an independent workflow-control gate. |
| Inherited rulesets | Two active tag rulesets, `24341547` and `24342332` | Tag rules do not establish a branch check or PR workflow-control guard. |

For prior PR 136, head `a639120b8548f4835a716a082696f01038870d27`,
GitHub Actions run `37785109216` reported both named jobs successful. That
result belongs to its own SHA and run; it does not prove later hosted execution.
`SEC-P01-001` remains HIGH for a PR that changes its own workflow or control
definition. Required checks from App `15368` do not independently authenticate
PR-editable job definitions. The security/CI operator owns that separate guard.

## Target Ruleset

- Target branch: `main`.
- Require pull requests before merge.
- Require zero approving reviews. The repository has a single collaborator who
  authors every pull request, and GitHub forbids self-approval, so any non-zero
  count names an approver who cannot exist and makes administrator bypass the
  only merge path.
- Do not require CODEOWNERS review, for the same reason. `.github/CODEOWNERS`
  stays as the ownership record it is and does not gate merges.
- Require conversations to be resolved before merge.
- Block force pushes.
- Block branch deletion.
- Require the latest branch head to pass required checks before merge.
- Require both `ci-summary` and PR-only `style-pr` from GitHub Actions App
  `15368` on a pull request; the former checks branch metadata and the latter
  checks selected style. Their separate required results carry the style
  failure to the merge decision.
- Do not enforce squash/rebase-only or linear-history settings that would
  discard referenced objects, so delivered history can keep them.
- Leave `enforce_admins` disabled, and read the consequence rather than the
  wording: the pull-request requirement and the required check do not bind the
  administrator, so a direct push to `main` by the owner succeeds and is
  reported as a bypass. This is deliberate. The repository has one operator and
  `allow_force_pushes` is blocked, so enabling administrator enforcement would
  leave a pull request as the only recovery path for a branch the same operator
  must be able to repair. Enabling it is a separate operating decision, not a
  correction of drift, and every administrator bypass stays visible in the
  remote's push output.

Branch, merge, finish and recovery rules themselves are owned by
`.agents/governance/git.md`. This file records only the remote settings that
support them.

## Required Status Checks

The current dated remote observation requires two separate checks.
`.github/workflows/ci.yml` owns the current tracked job identities and
`.github/repository-surface.md` explains their roles.

- `ci-summary`
- `style-pr`

`ci-summary` checks pull-request base and source-prefix
metadata directly, and reports branch policy as `NOT_APPLICABLE` on main
push/manual dispatch. Its earlier full-QA `NOT_RUN` field is historical
evidence, not a current required check. Success establishes only this metadata
policy; local QA has its own input and evidence. `style-pr` checks selected
style on the PR merge candidate using the reviewed base's tool and configuration
copies. Its job result is separately required by the 2026-10-09 protection
read-back. A main push or manual dispatch skips the PR-only job; that skip is
not PR style PASS.

The 2026-09-10 observation required only `ci-summary` and is historical.
Former hosted full-QA proof and `main-<SHA>` publication were retired from the
current workflows. Their
historical authenticated results remain reachable through the
[Archive index](../../docs/98.archive/README.md). A future protected publication
path requires a new current contract, its own identity and an authenticated
remote read-back. No setting is changed by this guidance.

GitHub treats a whole workflow skipped by a path or branch filter as an
expected check that may remain pending. No CI workflow here declares a `paths`
filter. `ci-summary` runs on each configured event; `style-pr` is conditional
on a main-targeting pull request. See the
[official required-check troubleshooting guide](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks).

A past merge blockage cannot be attributed to a skipped job without the actual
check-run, PR head or test-merge SHA, expected source app, and contemporaneous
protection configuration.

## Rollback State

A difference from this intended contract is a prompt to inspect, not permission
to restore old settings. Obtain a fresh authenticated read-back and bind any
approved correction to the exact field, before-state, target and recovery.

The 2026-09-10 reading under Historical 2026-09-10 State is the first captured
before-state for this repository. It covers `branches/main/protection` and the
absence of any ruleset on that date, and nothing else. Capture a fresh reading
before changing any field rather than relying on that one, and record it in the
active Task when a package is open. Do not import a before-state from another
repository. Local Git recovery restores tracked definitions only; it never
restores remote settings.

## Application Boundary

Apply changes only after explicit owner approval. Perform remote changes
through the GitHub UI or an audited `gh api` command, then re-check against
this repository:

- `gh api repos/buenhyden/hy-home.k8s/rulesets --paginate`
- `gh api repos/buenhyden/hy-home.k8s/branches/main/protection`

Every dated read-back is point-in-time evidence, not a perpetual guarantee.
Any later claim of remote enforcement requires a new authenticated read-back;
tracked workflow or policy files alone prove only repository configuration.

## Document Contract

This file is a native GitHub control surface, so the Stage 99 document
profile registry routes `.github/rulesets/*.md` to
`common/github-native-control` alongside the pull request and security
templates. That profile carries no frontmatter and requires no section
list, which is why this file reads as GitHub's own documentation rather
than an authored Stage document.

The route and this file were added in one change. The current selected local
document contract check classifies an applicable changed ruleset note against
the Stage 99 registry and requires exactly one profile. Historical full-QA
results belong to their original inputs and are not a current admission gate.
