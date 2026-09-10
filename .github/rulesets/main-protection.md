# Main Branch Protection Intended State and Recovery

This file is a local record of the intended GitHub settings for `main` in
`buenhyden/hy-home.k8s`. It is not an agent instruction surface and does not
apply remote repository settings by itself. Nothing here is evidence that a
setting is in force; only a dated authenticated read-back is.

## Observation Boundary

- **An authenticated read-back was recorded on 2026-09-10 by the account
  `buenhyden`.** `gh api repos/buenhyden/hy-home.k8s/rulesets` and
  `gh api repos/buenhyden/hy-home.k8s/rules/branches/main` both returned `[]`,
  so no repository ruleset exists and none is in force. What is in force is
  classic branch protection, read from
  `gh api repos/buenhyden/hy-home.k8s/branches/main/protection`. The fields
  observed in that response are listed under Observed State below. Every row
  under Target Ruleset is now either matched or contradicted by that reading
  rather than awaiting verification.
- A read-back belongs in the active Task with its date, the exact fields read,
  and the account that read them, and this file may then carry the claim. The
  2026-09-10 reading was taken with no Stage 03 package open, so its date,
  fields and account are carried here instead; that departure is recorded
  rather than hidden, and the next reading returns to a Task when one is open.
- Evidence from another repository does not transfer. This file previously
  carried required-check names, a workflow-contract path, a governance path, a
  Spec reference and `gh api` targets that belong to the sibling
  `hy-home.docker` workspace; none of them exist here, and none of them
  described this repository's protection.
- Environment, deployment, release, and later control-plane state remain
  `unverified` unless an approved observation records them.

## Observed State

Read on 2026-09-10 from `branches/main/protection` by `buenhyden`, before the
correction recorded below. This is point-in-time evidence for that moment and
for those fields only.

| Field | Observed | Target Ruleset row | Agreement |
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

Also observed and unstated by Target Ruleset: `required_signatures.enabled`
`false`, `block_creations.enabled` `false`, `lock_branch.enabled` `false`,
`allow_fork_syncing.enabled` `false`,
`required_pull_request_reviews.dismiss_stale_reviews` `false`, and
`required_pull_request_reviews.require_last_push_approval` `false`.

`enforce_admins` being `false` is why a direct push to `main` by the repository
owner succeeded on 2026-09-10 while the remote reported bypassed rule
violations for the pull-request requirement and the `ci-summary` check. The
rules are configured and they are not applied to administrators. Target Ruleset
states no expectation for that field, so the difference is a gap in the
intended contract rather than a drift from it.

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

`enforce_admins` was not changed. Target Ruleset now states an expectation for
it, so the field is no longer unstated; what remains is a recorded operating
decision rather than a difference from intent.

Every row above is evidence for 2026-09-10 only. A later claim of enforcement
needs a new authenticated read-back.

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

This repository publishes one aggregate check. `.github/workflows/ci.yml` owns
its exact machine identity and `.github/repository-surface.md` explains the
workflow roles.

- `ci-summary`

`ci-summary` runs with `if: always()` and depends on `branch-policy` and `qa`.
It fails closed: a `skipped`, `cancelled` or `failure` result for `qa` is a
failure, and a `skipped` `branch-policy` is accepted only for the `push` and
`workflow_dispatch` events where that job does not apply. Require `ci-summary`
alone. Requiring `branch-policy` directly would leave a permanently pending
check on those two events, because it declares
`if: github.event_name == 'pull_request'`.

GitHub treats a job skipped by a job-level condition as successful for required
checks, and a whole workflow skipped by a path or branch filter can leave its
expected checks pending. No workflow in this repository declares a `paths`
filter, so that failure mode does not currently apply; it would apply again if
one were added. See the
[official required-check troubleshooting guide](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks).

A past merge blockage cannot be attributed to a skipped job without the actual
check-run, PR head or test-merge SHA, expected source app, and contemporaneous
protection configuration.

## Rollback State

A difference from this intended contract is a prompt to inspect, not permission
to restore old settings. Obtain a fresh authenticated read-back and bind any
approved correction to the exact field, before-state, target and recovery.

The 2026-09-10 reading under Observed State is the first captured
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

The route and this file were added in one change. An untracked ruleset note
would not have escaped validation: `scripts/qa.py full` snapshots
`git ls-files --cached --others --exclude-standard`, so a file that is neither
tracked nor ignored still enters the snapshot and must resolve to exactly one
profile.
