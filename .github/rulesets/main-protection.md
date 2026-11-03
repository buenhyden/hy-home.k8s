# Main Protection and Actions Policy Intended State and Recovery

This file is a local record of intended `main` protection and repository
Actions settings in `buenhyden/hy-home.k8s`. It is not an agent instruction
surface and does not apply remote settings by itself. Nothing here is evidence
that a setting is in force; only a dated authenticated read-back is.

## Observation Boundary

- A read-back belongs in the active Task with its date, the exact fields read,
  and the account that read them.
- Evidence from another repository does not transfer.
- Environment, deployment, release, and unobserved control-plane state remain
  `unverified` unless an approved observation records them.

## Target Main Protection

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
- Require `independent-review` from review App `5341483`, published only
  through RUN-0013, so a PR-edited workflow cannot satisfy every required
  check.
- Do not enforce squash/rebase-only or linear-history settings that would
  discard referenced objects, so delivered history can keep them.
- Keep `enforce_admins` enabled, so the owner also uses a pull request and the
  required checks for `main`. A recovery exception requires its own reviewed
  operator decision and remote read-back; this document grants no bypass.

Branch, merge, finish and recovery rules themselves are owned by
`.agents/governance/git.md`. This file records only the remote settings that
support them.

## Repository Actions Policy Target

Keep Actions enabled, `allowed_actions: all`, default workflow token
permissions at `read`, and PR creation/approval by Actions disabled. Require
`sha_pinning_required: true` at the repository setting while every external
`uses:` reference in tracked workflows remains a full commit SHA. Hosted
compatibility for the next PR still needs that PR's exact SHA and run result.

This server-side requirement protects Action dependency identity across
future workflow edits. When upgrading an Action, review its new full SHA and
the affected workflow checks before delivery. A failed run calls for repairing
the pin and verifying the actual PR run, not silently disabling the setting.
Changing the remote setting back requires a new reviewed before-state,
operator decision and after-state. SHA pinning does not protect the body of a
PR-editable `pull_request` workflow, its shell steps, or required job names.
The repository's default read token is not a hard ceiling on workflow-defined
permissions. Required-check forgery is closed by the `independent-review`
requirement above; the PR-editable workflow body is a separate MEDIUM risk owned
by the CI and security operator. SPEC-0115 Task 0005 first recorded it; that
package left the tree and Git history recovers it.

## Required Status Checks

The target requires three separate checks.
`.github/workflows/ci.yml` owns the two Actions job identities and
`.github/repository-surface.md` explains their roles. The independent review
runbook RUN-0013 in `docs/05.operations/runbooks/` owns the third; SPEC-0116,
which introduced it, left the tree and Git history recovers it.

- `ci-summary` (App `15368`)
- `style-pr` (App `15368`)
- `independent-review` (App `5341483`, no workflow; published locally)

`ci-summary` checks pull-request base and source-prefix
metadata directly, and reports branch policy as `NOT_APPLICABLE` on main
push/manual dispatch. Success establishes only this metadata policy; local QA
has its own input and evidence. `style-pr` checks selected style on the PR
merge candidate using the reviewed base's tool and configuration copies. Its
job result is separately required. A main push or manual dispatch skips the
PR-only job; that skip is not PR style PASS.

The `independent-review` reviewer is an AI agent under the same solo operator,
so the gate is not independent human review; the operator owns that HIGH risk.
A protected publication path requires a new current contract, its own identity
and an authenticated remote read-back. No setting is changed by this guidance.

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

Capture a fresh reading before changing any field, and record it in the active
Task when a package is open. Do not import a before-state from another
repository. Local Git recovery restores tracked definitions only; it never
restores remote settings.

## Application Boundary

Apply changes only after explicit owner approval. Perform remote changes
through the GitHub UI or an audited `gh api` command, then re-check against
this repository:

- `gh api repos/buenhyden/hy-home.k8s/rulesets --paginate`
- `gh api repos/buenhyden/hy-home.k8s/branches/main/protection`
- `gh api repos/buenhyden/hy-home.k8s/actions/permissions`
- `gh api repos/buenhyden/hy-home.k8s/actions/permissions/workflow`

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

The current selected local document contract check classifies an applicable
changed ruleset note against the Stage 99 registry and requires exactly one
profile.
