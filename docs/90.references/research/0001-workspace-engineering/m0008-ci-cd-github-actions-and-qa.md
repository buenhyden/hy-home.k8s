---
title: 'Reference: CI/CD, GitHub Actions, and QA'
version: "1.0.0"
type: reference/research
layer: "references"
status: active
owner: platform
updated: 2026-08-31
artifact_id: "RES-0001-m0008"
---

# Reference: CI/CD, GitHub Actions, and QA

## Overview

This dated reference maps the repository's delivery and quality controls to
their evidence depth. The checked tree has static CI and maintenance/release
review automation; it does not contain deploy CD. It is a decision input for
platform, QA, security, and operations owners, not an authorization to change
a workflow, branch rule, environment, cloud identity, release, or cluster.

## Reference Type

Current-primary-source research combined with repository-static workflow,
validation-contract, and predecessor evidence. The dated source and claim
records are in [the pack ledger](m0012-source-coverage.md).

## Authority Boundary

`.github/workflows/` owns tracked workflow declarations; `.github/README.md`
routes their repository purpose; and
[Quality and Evidence Policy](../../../00.agent-governance/policies/quality.md)
owns local completion order, lane names, result vocabulary, formatter handling,
and handoff fields. GitHub repository settings own branch protection, rulesets,
Actions policy, secret availability, environment protection, and retained-run
configuration. GitOps and Stage 05 owners retain promotion, reconciliation,
rollback, and live-operation authority.

A local validator or YAML declaration cannot prove a GitHub-hosted run,
effective token/secret permission, artifact availability, branch-rule
enforcement, OIDC exchange, deployment, Argo CD reconciliation, or runtime
health. Those evidence classes are `DEFER` without separately authorized,
redacted observation.

## Scope

Included: CI/CD control flow, the five tracked Actions workflows, pre-commit
and validator topology, formatting/lint/syntax/test/security lanes, failure
semantics, concurrency, permission and supply-chain declarations, artifact and
release-review boundaries, and adoption recommendations.

Excluded: workflow dispatch, hosted-run/API/UI inspection, branch-rule or
repository-setting inspection, secrets/credentials, artifact download,
deployment/publishing, cloud identity, remote GitOps, and live validation. The
Actions, delivery, and supply-chain sources were checked on 2026-08-08; the
Verification and Validation sources `SRC-WERPC-058` and `SRC-WERPC-059` were
added by the gap-only refresh and checked on 2026-08-10. Their version/product
boundaries and refresh triggers are retained in the ledger.

## Definitions / Facts

### Evidence-depth model

| Evidence level            | What this review can establish                                                                                                          | What it cannot establish                                                                            | Current result                                 |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| Repository static         | A tracked workflow, contract, lock, script, or validator declares the cited behavior.                                                   | GitHub parses it, an event occurs, a job runs, permissions resolve, or an external action succeeds. | Verified where a current path is cited.        |
| Local static QA           | A named local command accepts its stated worktree inputs.                                                                               | Hosted runner/image/network/action bytes, branch rules, artifacts, deployment, or runtime health.   | Verified only for the named command and scope. |
| Hosted CI                 | A specific GitHub run completed with a conclusion and retained evidence.                                                                | Deployment, GitOps reconciliation, or workload health.                                              | DEFER.                                         |
| Repository administration | Rulesets, branch protection, Actions policy, environments, secrets, and retention settings are observed by an authorized administrator. | A workflow run or deployment outcome.                                                               | DEFER.                                         |
| Remote/live delivery      | Artifact, identity, deployment, reconciliation, and health evidence is observed under approved operations.                              | Broader future reliability or security conformance.                                                 | DEFER.                                         |

`Verified` above is evidence-depth wording, not an assertion that every
control is effective. A deeper row is never promoted by inference.

### CI/CD baseline

The repository follows a desired-state/GitOps boundary: workflows check source
and desired-state artifacts; they do not mutate Kubernetes, Vault, a registry,
or the repository. `ci.yml` is a main-branch CI gate, and
`generate-changelog.yml` makes a review artifact for a version tag. Neither
contains an environment, `id-token: write`, cloud login, deployment,
publication, attestation, cache, reusable-workflow invocation, or rollback
automation. The lack is a checked-file observation, not an instruction to add
those surfaces.

For a future deployable artifact, a promotion design needs a separate approved
workflow/owner, protected environment, least privilege, claim-bound identity,
digest-and-signer verification, a Git-revert-first or other bounded rollback
procedure, and independent post-change health evidence. It must not label the
current static QA setup as CD or SLSA conformance.

### GitHub Actions baseline

GitHub defines a workflow as YAML in `.github/workflows/`, with events, jobs,
permissions, conditions, dependencies, and concurrency as distinct controls
([SRC-WERPC-035](m0012-source-coverage.md#source-register)).
The local `ci.yml` uses `push` and `pull_request` limited to `main`, plus
`workflow_dispatch`; it derives paths in a dedicated `changes` job rather than
using broad YAML path filters. GitHub documents that server-side path filtering
has changed-file limits and can leave a required check pending when skipped;
the local explicit selector and the fail-closed summary reduce, but do not
eliminate, the need for hosted evidence.

All five workflows declare default `contents: read`. Only the label, greeting,
and stale maintenance jobs request their narrow issue/pull-request write
permissions. Remote `uses:` entries are full 40-character SHAs accompanied by
version comments; `actions/checkout` uses `persist-credentials: false` and
full history where required. The GitHub secure-use guidance treats full-length
commit pinning and least privilege as important controls, but a SHA pin is not
an upstream-code audit, a provenance claim, or a hosted-run result
([SRC-WERPC-036](m0012-source-coverage.md#source-register)).

### Workflow control inventory

| Trigger / workflow                                                  | Jobs, dependency, and failure behavior                                                                                                                                                                                                                                                                                               | Artifact / state effect                                                                                 | Promotion and rollback boundary                                                                                                                      |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `push` or `pull_request` for `main`, or manual dispatch -> `ci.yml` | PR-only `branch-policy`; `changes` produces no-rename affected-path outputs; selected `pre-commit`, `repo-quality-static`, `agent-governance-static`, and `manifest-static` depend on it. `ci-summary` runs with `always()` and fails when any selected dependency is not `success`; unselected conditional jobs are visible `SKIP`. | Workflow logs and check conclusion only. No cache, upload, publish, deployment, or repository mutation. | No promotion. Correct desired state by governed commit/revert, then obtain separately authorized hosted and, where applicable, remote/live evidence. |
| version tag `v*.*.*` -> `generate-changelog.yml`                    | One changelog job, full-history credentials-disabled checkout, pinned git-cliff action, ten-minute timeout.                                                                                                                                                                                                                          | Uploads `CHANGELOG.md` with exactly seven-day retention and writes a step summary.                      | Review evidence only; no release creation, commit, push, publish, deploy, provenance, or rollback.                                                   |
| PR opened/synchronized -> `labeler.yml`                             | Pinned labeler action with allowlisted `pull-requests: write`.                                                                                                                                                                                                                                                                       | Applies labels.                                                                                         | Maintenance only; not QA, promotion, or rollback.                                                                                                    |
| issue/PR opened -> `greetings.yml`                                  | Pinned first-interaction action with allowlisted issue/PR writes.                                                                                                                                                                                                                                                                    | Posts first-interaction guidance.                                                                       | Maintenance only; not QA, promotion, or rollback.                                                                                                    |
| daily schedule -> `stale.yml`                                       | Pinned stale action with allowlisted issue/PR writes and configured stale/close periods.                                                                                                                                                                                                                                             | Labels, comments on, and can close stale issues/PRs.                                                    | Maintenance only; not release or deployment control.                                                                                                 |
| local hook/manual -> `.pre-commit-config.yaml`                      | Commit message, static-contract, format/lint/syntax/security hooks; frozen remote hooks and local hooks are selected by pre-commit.                                                                                                                                                                                                  | Local feedback and possible formatter mutation.                                                         | Cannot replace exact-index staged, all-files, hosted, or remote/live evidence. Formatter mutation requires review, restage, and rerun.               |

`ci.yml` configures `ci-${{ github.ref }}` concurrency with cancellation of
superseded runs; changelog retains tag runs; maintenance workflows cancel
superseded per-item/scheduled runs. GitHub documents concurrency as deliberate
overlap/cancellation control, but scheduler behavior is `DEFER` until a run is
observed ([SRC-WERPC-037](m0012-source-coverage.md#source-register)).

### QA baseline

The canonical quality system is a validation matrix, not invented numeric code
coverage for this Bash/YAML/Markdown infrastructure repository. The exact
ordered completion evidence is `targeted -> affected -> staged -> tests ->
all-files -> formatter-review -> rerun -> diff-checks`; the detailed definitions
remain in `quality-standards.md`, rather than this snapshot.

| Quality lane                            | Current implementation and evidence scope                                                                                                                                   | Failure/result semantics and limitation                                                                                                                     |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Targeted                                | A direct smallest validator/test selected while editing; pre-commit supplies early local feedback.                                                                          | `PASS` only proves that command and paths. No generic machine `fast` lane exists.                                                                           |
| Affected                                | `scripts/run-validation-lane.py --lane affected` selects from `validation-surfaces.json` for normalized changed paths.                                                      | Empty/no-applicable input is `SKIP`; required failure, timeout, malformed contract, or output-boundary failure is `FAIL`; remote/live selection is `DEFER`. |
| Staged                                  | Exact Git index through the staged runner plus plain `pre-commit run`.                                                                                                      | Both are required. An affected or working-tree pass is not a substitute.                                                                                    |
| All-files                               | `pre-commit run --all-files`; CI `pre-commit` uses the explicit all-files/show-diff command.                                                                                | Only this command is all-files completion evidence. Prettier is deliberately dormant, so it is not coverage.                                                |
| Formatting, linting, and syntax         | Whitespace/end-of-file, YAML/JSON/TOML, Markdown, shell, Dockerfile, Actions, manifest syntax, and static contracts are covered by frozen hooks/scripts when selected.      | Formatter mutation is not semantic proof. Optional local tools such as kube-linter are `SKIP` only with their stated fallback.                              |
| Unit, integration, contract, and render | Python validator self-tests/unittests and repository contracts run where selected; manifest/GitOps/policy/Vault-ESO commands are static/render checks.                      | No application unit/integration/coverage suite or observed report is claimed. A future executable surface needs its own test and coverage contract.         |
| Browser/end-to-end                      | No reviewed workflow invokes browser/end-to-end tests.                                                                                                                      | Missing from this delivery topology; do not call it a skipped passing lane.                                                                                 |
| Security                                | Full-SHA action validation, least-privilege checks, hash-locked CI dependencies, Gitleaks release checksum/scan, and selected policy/secret/GitOps checks.                  | Does not prove GitHub settings/history secrets, runner integrity, dependency provenance, or cloud authorization.                                            |
| Hosted CI / admin                       | `ci-summary` maps selected success to `PASS`, selected non-success to `FAIL`, and unselected jobs to `SKIP`. Branch rules and hosted run identity are outside the worktree. | Hosted run/required-check/ruleset evidence: `DEFER`.                                                                                                        |
| Remote/live                             | No reviewed workflow deploys or mutates a live platform.                                                                                                                    | `DEFER` unless an approved operator procedure captures bounded evidence.                                                                                    |

The local runner gives each selected validator a finite resource envelope: 1,200
seconds, 4 MiB retained stdout, 1 MiB retained stderr, two-second cleanup, and
process-group cleanup. It does not silently waive nonzero results; the reviewed
workflows contain no `continue-on-error`, retry, or flaky-test quarantine rule.
Until one is separately specified, an unstable test is `FAIL`, not `SKIP`.

### Verification and Validation question matrix

The external terms below do not rename the repository's validation lanes or
`VAL-*` acceptance-criterion IDs. They identify the comparison question and
evidence depth that a result can support.

| Term         | Question                                                                                                                                 | Actor                                                                                                                          | Input                                                                                                                                                       | Evidence                                                                                                                                                                                                                                                                                                  | Failure meaning                                                                                                                                                                                                                         | Workspace mapping                                                                                                                                                                                                                                                                                                                                                           |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Verification | Was the artifact realized right: does the identified product or work product conform to its approved specified requirements?             | Implementer/engineer with QA or an independent reviewer proportionate to risk. Full IV&V is not implied.                       | Versioned requirement/specification baseline, acceptance criteria, artifact/commit version, approved method, tools, and environment.                        | Bidirectional requirement-to-result trace plus test, analysis, inspection, or demonstration record; method/tool/environment versions; pass/fail; discrepancies, waivers, corrective action, and closure ([SRC-WERPC-058](m0012-source-coverage.md#source-register)).                       | The artifact is nonconforming, or the method/procedure/environment was invalid. Stop, diagnose, correct and reverify, or process an explicitly controlled waiver.                                                                       | During SDLC implementation/review, targeted/affected/staged/tests and structural validators provide bounded conformance evidence. Release readiness links the approved Spec/Plan/Task/Policy baseline to artifact identity and results; operations use Runbook verification/evidence steps. `VAL-*` names a criterion, and static PASS is not intended-use or live fitness. |
| Validation   | Was the right product realized: does the verified product satisfy stakeholder expectations and intended use in its intended environment? | Product/requirements owner, affected stakeholders, and anticipated users/operators; independent review strength is risk-based. | Verified product version, stakeholder expectation or requirement baseline, intended use/ConOps, scenarios, validation plan, and representative environment. | Expected-versus-observed scenario results under realistic or justified simulated conditions; participating stakeholder/user identities; environment/tool versions; discrepancies, corrective action, and revalidation closure ([SRC-WERPC-059](m0012-source-coverage.md#source-register)). | The setup was not representative, or the product/requirements/design cannot satisfy intended use. Correct the setup and repeat, or rework the expectation, requirement, design, or product with stakeholder involvement and revalidate. | Requirements validation begins during PRD/ARD/Spec review; product/system validation belongs at release readiness and operational scenarios with stakeholders/users. Without separately authorized intended-use, user/operator, hosted, remote, or live evidence, release/operations validation is `DEFER`, never inferred from repository-static PASS.                     |

Testing is a method available to both terms, not a synonym for either one.
Requirements validation is an earlier agreement and quality check on the
requirements themselves; it must not be conflated with later product/system
validation. Traceability must bind stable identities and versions in both
directions so a change can select affected verification and intended-use
scenarios rather than merely link filenames.

### Supply-chain, cache, artifact, environment, and identity boundaries

| Control                 | Repository-static finding                                                                                                                                                            | Evidence and follow-up boundary                                                                                                                                                                                                      |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Dependencies            | Four validation jobs use Python 3.12 and the reviewed fully pinned/all-hash Linux lock with `--only-binary :all:` and `--require-hashes`; direct pins and lock are separately owned. | pip describes hash checking and binary-only resolution as installation constraints ([SRC-WERPC-043](m0012-source-coverage.md#source-register)); this does not prove downloaded bytes, package safety, or portability. |
| Gitleaks bootstrap      | Two CI jobs download a fixed v8.30.0 Linux asset and verify its recorded SHA-256 before installation; a local contract validator reconciles the declaration.                         | Runtime download, publisher identity, GitHub-managed secrets, and history settings are `DEFER`.                                                                                                                                      |
| Artifacts               | One pinned upload action retains a changelog artifact for seven days.                                                                                                                | GitHub artifact retention/deletion behavior is source-backed ([SRC-WERPC-038](m0012-source-coverage.md#source-register)); upload, retrieval, access control, and retention outcome are hosted/admin evidence.         |
| Cache                   | No `actions/cache`, dependency cache, or cache-key policy was found.                                                                                                                 | Do not claim cache isolation or poisoning resistance. Before adding cache, model trusted writers/readers, keys, invalidation, secret exclusion, and release-input boundary.                                                          |
| Environments/deployment | No job `environment`, deployment API/action, registry publish, or cloud login was found.                                                                                             | Protected environment, approval, and deployment state are `DEFER`; a deploy design needs a dedicated owner and evidence plan.                                                                                                        |
| OIDC                    | No `id-token: write` or cloud trust declaration was found.                                                                                                                           | GitHub OIDC uses job-scoped tokens and requires claim-aware trust design ([SRC-WERPC-039](m0012-source-coverage.md#source-register)); no workload is currently evidenced as using it.                                 |
| Attestation/SLSA        | No attestation permission/action, provenance/SBOM, signer verification, reusable build workflow, or admission enforcement was found.                                                 | GitHub attestation and SLSA documents provide a future benchmark ([SRC-WERPC-040](m0012-source-coverage.md#source-register)); no level or conformance is claimed.                                                     |
| Hook supply chain       | Remote pre-commit repositories use unique full commits and frozen tag comments.                                                                                                      | The pre-commit update procedure preserves revision provenance ([SRC-WERPC-042](m0012-source-coverage.md#source-register)); transitive hook environments and cold offline replay remain `DEFER`.                       |

### Workspace As-Is, gap, and target matrix

Recommendations below require a separate approved implementation and do not
alter current controls.

| Priority / trigger                                                 | As-Is or bounded gap                                                                                             | Target acceptance evidence                                                                                                                                                                           | Owner                       |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| High when a distributable artifact/image exists                    | Changelog is review evidence only; no provenance or consumer verification.                                       | Build provenance and digest/signer verification with minimal `attestations: write` and `id-token: write`; named workflow/repository expectations and a version-specific SLSA assessment.             | Delivery + security.        |
| High when cloud/CD is introduced                                   | No OIDC, environment protection, deployment workflow, promotion record, or automated rollback.                   | Separate protected deploy workflow; job-scoped OIDC trust bound to repository/workflow/ref/environment/audience claims; explicit desired-state promotion, rollback, and independent health evidence. | Operations + security.      |
| Medium when repository settings change                             | Rulesets, required checks, Actions policy, fork policy, retention, and bypass roles are not tracked or observed. | Authorized administration snapshot reconciled to the static workflow and recorded with date/run context.                                                                                             | Repository administrator.   |
| Medium when a test framework/browser lane is added or flakes occur | No retained redacted diagnostics artifact or flaky policy.                                                       | Stable test identity, bounded retry/quarantine owner and expiry, artifact data classification/retention, and fail-closed original-attempt evidence.                                                  | QA.                         |
| Medium when caching is proposed                                    | No cache threat model/policy.                                                                                    | Narrow deterministic keys, trust-separated readers/writers, secret exclusion, invalidation, and poison-response procedure.                                                                           | CI + security.              |
| Ongoing for every delivery change                                  | No hosted run identity is preserved by this static reference.                                                    | Command/version/path/job/run URL or ID/attempt/conclusion/artifact digest as applicable; report each lane as `PASS`, `SKIP`, `FAIL`, or `DEFER`.                                                     | Change owner + QA reviewer. |

### 2026-08-17 full-corpus refresh

This increment is the fifth refresh cycle over this pack, executed under
Spec 058. Unlike the three preceding cycles it re-observed every owner row in
the pack rather than the twelve `Partial` rows, and it assigns each retained
`Partial` or `DEFER` row a blocking class recorded in the
[scope application index](m0013-scope-application-index.md). All observations are
dated **2026-08-17**. No live cluster, hosted CI run, provider runtime,
authenticated execution, or secret value was observed.

#### Re-observation of the four delivery rows

All four rows returned `unchanged` externally and `confirmed` in the workspace
(`SRC-WERPC-082`). No status changed
(`CLM-WERPC-011-22` through `CLM-WERPC-011-24`, `CLM-WERPC-011-33`).

| Request ID    | External  | Workspace | Blocking class  | Reachable by static work |
| ------------- | --------- | --------- | --------------- | ------------------------ |
| REQ-WERPC-022 | unchanged | confirmed | hosted-ci       | no                       |
| REQ-WERPC-023 | unchanged | confirmed | hosted-ci       | no                       |
| REQ-WERPC-024 | unchanged | confirmed | repo-static     | yes                      |
| REQ-WERPC-033 | unchanged | confirmed | human-judgement | no                       |

**External detail.** The GitHub Actions workflow-syntax and concurrency pages
still document `on`, `jobs`, `permissions`, `if`, `needs`, and `concurrency` as
distinct workflow-level controls with default cancel-on-supersede. The secure-use
page still states that pinning an action to a full-length commit SHA is currently
the only way to use an action as an immutable release. The pre-commit and pip
pages are unchanged against their adopted scope. Both NASA verification and
validation pages still show unmoved page-revision dates, so the
Verification-and-Validation question matrix rests on the same basis.

**Workspace detail.** All five tracked workflows remain present. Every remote
`uses:` entry in all five files is a full forty-character SHA with a version
comment. Top-level `permissions: contents: read` is present in all five, with
narrow job-level `issues: write` or `pull-requests: write` only in `labeler.yml`,
`greetings.yml`, and `stale.yml`. Concurrency groups are present in all five.
`ci.yml:3-15` still triggers on `push` and `pull_request` against `main` plus
`workflow_dispatch`, and `ci-summary` at `ci.yml:230-352` still fails closed
under `always()`. No `environment`, `id-token: write`, cloud login, deployment,
cache, or reusable-workflow call exists in any of the five files.
`validation-surfaces.json:10-21` and `quality-standards.md:63-87,122-149` still
agree on the lane vocabulary and the ordered completion sequence.

#### Read-only remote observation

Dependabot pull request 50 on the remote proposes bumping `actions/stale` from
`10.4.0` to `11.0.0`, targeting the pin at `.github/workflows/stale.yml:22`. It
was opened 2026-08-09 and is still open. It was observed read-only and was
neither approved, merged, nor dispatched. No other tracked action shows a pending
bump in this pass. This is repository metadata, not a hosted run outcome, and it
promotes nothing.

#### Blocking-class closure for the three unreachable rows

`REQ-WERPC-022` and `REQ-WERPC-023` are blocked by `hosted-ci`: current-revision
hosted run identity, effective per-run token resolution, rulesets, secrets,
environments, OIDC trust, and artifact provenance cannot be obtained from the
repository. The 2026-08-12 read-only administration snapshot remains
carried-forward reference evidence and does not by itself promote any of these.
`REQ-WERPC-033` is blocked by `human-judgement`: stakeholder and intended-use
participation and risk-proportionate independent review require a named reviewer
or stakeholder record, which no file read can supply. These three rows are closed
against further repository-static re-testing.

#### Date-consistency re-check

No new internal date contradiction exists in this report. The apparent mismatch
between the `### 2026-08-11 Partial/DEFER incremental refresh` header and its
body statement that the refresh executed on 2026-08-12 is the pack-wide
convention of naming a package by its gap-identification date while dating
sources and claims by execution, and it is applied identically in the ledger and
every sibling section.

A separate staleness signal is recorded rather than corrected: in several pack
files the frontmatter `updated:` value predates the newest dated body section.
This follows the pack's stated convention that baseline rows are preserved and
lag re-verification, but it means `updated:` cannot be read as the latest
observation date for any pack file without reading the body.

## Sources

Current primary-source rows are `SRC-WERPC-035` through `SRC-WERPC-044` in the
[source register](m0012-source-coverage.md#source-register).
They cover Actions syntax, secure use, concurrency, artifact retention, OIDC,
attestations/SLSA, pre-commit update provenance, and secure pip installs.
The gap-only V&V rows are `SRC-WERPC-058` and `SRC-WERPC-059`, checked
2026-08-10 from NASA's official Systems and Software Engineering Handbooks.
Predecessor documents remain dated provenance until WERPC-008; current claims
were reconciled against workflow, contract, and QA owners rather than copied.

## Review and Freshness

Refresh this reference when workflow triggers/jobs/permissions/concurrency,
Action revisions, CI lock/toolchain, pre-commit hooks, validation surfaces,
artifact/cache/environment/OIDC/attestation settings, branch/ruleset policy,
test topology, release/promotion design, or GitOps recovery boundary changes.
Refresh the Verification and Validation section when the requirement, spec,
artifact, quality-lane, or traceability contract changes, or when the cited NASA
handbooks are revised. Attach a hosted run identity before reporting hosted CI
`PASS`; attach a separately approved bounded procedure before reporting
remote/live `PASS`.

### 2026-08-11 Partial/DEFER incremental refresh

This incremental refresh was executed on 2026-08-12. The exact
`github.com` repository identity, canonical URL, and default branch `main`
passed preflight before one read-only, byte-allowlisted query batch. An
independent security review approved the nine projected commands and checker
boundary with zero findings. No query was retried; no logs, raw response,
secret or variable value, artifact body, dispatch, rerun, approval,
deployment, GraphQL, fallback endpoint, or remote mutation was used. The
guarded mode-`0600` sanitized summary passed local `remote` validation with
nine unique evidence classes: eight `ok` and OIDC `unavailable`.

Official GitHub REST documentation checked on 2026-08-12 defines the admitted
read surfaces for [workflow inventories](https://docs.github.com/en/rest/actions/workflows?apiVersion=2026-03-10),
[workflow runs](https://docs.github.com/en/rest/actions/workflow-runs?apiVersion=2026-03-10),
[Actions permissions](https://docs.github.com/en/rest/actions/permissions?apiVersion=2026-03-10),
[repository rulesets](https://docs.github.com/en/rest/repos/rules?apiVersion=2026-03-10),
[branch protection](https://docs.github.com/en/rest/branches/branch-protection?apiVersion=2026-03-10),
[deployment environments](https://docs.github.com/en/rest/deployments/environments?apiVersion=2026-03-10),
[OIDC subject customization](https://docs.github.com/en/rest/actions/oidc?apiVersion=2026-03-10),
and [Actions artifacts](https://docs.github.com/en/rest/actions/artifacts?apiVersion=2026-03-10).
These current endpoint contracts support interpretation of the projected
fields, not the repository observations themselves. GitHub metadata remains
separate remote evidence and is not an external-source row. Existing
`SRC-WERPC-058`–`059` remain sufficient for the Verification and Validation
definitions; no duplicate general QA research was added.

| Evidence class              | Sanitized observation                                                                                                                                                                                                                         | Bounded interpretation and rejected inference                                                                                                                                                                                                                                                             |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Workflow inventory          | The projected repository list returned seven active workflows. Five paths match the five tracked workflows in this checkout; two projected active paths do not.                                                                               | This proves a dated hosted inventory difference, not the content, safety, trigger, or current-branch provenance of either unmatched workflow. The tracked five remain the only locally reconciled workflow bodies.                                                                                        |
| Run sample                  | The bounded latest-20 projection returned 20 completed runs: 15 `success` and five `failure`, across push, pull-request, schedule, and dynamic events. None used the current local HEAD.                                                      | Hosted execution exists for sampled historical revisions. Conclusion alone does not identify root cause, requirement coverage, current-HEAD status, deployment, promotion, rollback, or live GitOps outcome.                                                                                              |
| Actions policy              | Actions is enabled; the repository policy allows all actions. The default workflow token setting is `read`, and workflow approval of pull-request reviews is disabled.                                                                        | This is a repository-setting snapshot. Local full-SHA pins, read-default workflow declarations, and narrow job writes remain separate static controls; neither layer proves effective per-run token use, upstream integrity, fork behavior, or runner isolation.                                          |
| Rules and branch protection | The projected ruleset list was empty. The `main` branch-protection projection returned one required status check, with strict up-to-date checking disabled; administrator enforcement was false and required approving review count was zero. | This records only projected settings at collection time. It does not prove a merge was blocked, a check mapped to the current local revision, higher-order review quality, bypass history, or policy effectiveness. Null projected fields are not generalized beyond the queried branch-protection shape. |
| Environments and artifacts  | Both projected repository totals were zero.                                                                                                                                                                                                   | No environment or retained artifact was listed at collection time. This does not prove historical absence, deletion/retention correctness, secret absence, release state, deployment absence, or artifact integrity. The tracked changelog upload declaration remains static only.                        |
| OIDC                        | The read executed, but the checker rejected the officially valid nullable projected claim-key shape. A reviewed local-only recovery recorded `unavailable` with empty identities and a fixed non-body limitation.                             | OIDC customization is `UNPROVEN`/`DEFER`. No retry, raw recovery, token request, claim observation, cloud trust, identity exchange, deployment, or absence inference is permitted.                                                                                                                        |

The local reconciliation remains internally consistent. Five tracked workflow
bodies declare default `contents: read`; remote actions are full-commit pinned
with version comments; checkout credentials are disabled where used; `ci.yml`
selects affected surfaces and fails closed through `ci-summary`; four validation
jobs use the fully hashed binary-only Linux/CPython 3.12 lock; pre-commit uses
frozen remote revisions; and the affected/staged/all-files contract keeps
syntax and repository-static evidence distinct. The hosted inventory difference
does not authorize importing or interpreting the two unmatched workflow bodies.

| Request         | Final disposition | Evidence gained                                                                                                                                                       | Remaining boundary and follow-up                                                                                                                                                                                                                                                       |
| --------------- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `REQ-WERPC-022` | `Partial`         | Bounded hosted workflow/run metadata now establishes a dated inventory and historical run sample.                                                                     | No sampled run matches current local HEAD. Current-revision hosted verification, run root cause, deployment, promotion, rollback, reconciliation, and live health remain `DEFER`; refresh on workflow/run topology change or with an approved current-revision run identity.           |
| `REQ-WERPC-023` | `Partial`         | Projected Actions/default-token, ruleset, branch-protection, environment, and artifact settings materially narrow the prior administration gap.                       | OIDC is unavailable; effective per-run permissions, merge enforcement, bypass/fork behavior, secret values, artifact integrity/retention, and any environment or identity use remain `DEFER`; refresh when an allowlisted class or named local workflow/validator changes.             |
| `REQ-WERPC-033` | `Partial`         | The sampled hosted conclusions are bounded verification metadata for identified historical revisions, and local lanes remain reproducible static conformance methods. | No current-HEAD requirements-to-result trace, discrepancy/root-cause record, independence evidence, stakeholder/user participation, intended-use scenario, representative environment, deployment, or live-system result was observed. Product/stakeholder validation remains `DEFER`. |

Syntax/static validation, hosted run metadata, repository administration,
product/stakeholder validation, and deployment/live effects therefore remain
five separate evidence depths. No row is promoted to `Verified`: all three
admitted requests remain `Partial`, with the explicit `DEFER` boundaries above.

### 2026-08-14 consistency and Partial re-observation

This bounded increment re-observed the workspace and re-checked external
sources for `REQ-WERPC-022`, `REQ-WERPC-023`, and `REQ-WERPC-033`, checked on
**2026-08-14**. It did not run `kubectl`, `k3d`, `helm`, `argocd`, `vault`,
`gh`, or `gh api`, and it did not query the GitHub remote for this
repository; the prior 2026-08-12 hosted-metadata batch (`SRC-WERPC-072`,
`CLM-WERPC-009-09`–`010`) is carried forward by reference, not re-fetched.
The objective workspace check was `git diff --stat a5d2dfbb HEAD -- .github/
.pre-commit-config.yaml docs/00.agent-governance/contracts/validation-surfaces.json
docs/00.agent-governance/rules/quality-standards.md`, where `a5d2dfbb` is the
2026-08-12 baseline merge commit; the command returned zero changed files, so
every selector cited below was spot-verified rather than assumed unchanged.

#### REQ-WERPC-022 CI/CD workspace and source consistency check

**Workspace delta:** `no-change`. The five tracked workflow files still exist
unchanged: `ci.yml` still triggers on `push`/`pull_request` limited to `main`
plus `workflow_dispatch`, derives affected paths through its dedicated
`changes` job, and its `ci-summary` job still runs with `always()` and fails
closed on any selected non-`success` dependency; `generate-changelog.yml`
still triggers on `v*.*.*` tags and uploads `CHANGELOG.md` with exactly
seven-day retention; `labeler.yml` still triggers on PR opened/synchronized;
`greetings.yml` still triggers on issue/PR opened; `stale.yml` still runs on
the `30 1 * * *` daily schedule. Concurrency groups are unchanged: `ci.yml`
uses `ci-${{ github.ref }}` with `cancel-in-progress: true`;
`generate-changelog.yml` uses `changelog-${{ github.ref }}` with
`cancel-in-progress: false`; the three maintenance workflows each declare a
per-item/scheduled group with `cancel-in-progress: true`. No `environment`,
`id-token: write`, cloud login, deployment, publication, attestation, cache,
reusable-workflow invocation, or rollback automation was found in any of the
five files.

**External result:** representative URLs for `SRC-WERPC-035`, `037`, `038`,
and `044` were re-fetched; see the [shared source-outcome
table](#re-checked-external-sources-shared-by-req-werpc-022-req-werpc-023-and-req-werpc-033)
below. `SRC-WERPC-044`'s registered URL now returns HTTP 404; the equivalent
content was located at a relocated path and is recorded as `changed`
(URL relocation), not `unreachable`, because reachable equivalent content was
confirmed this cycle.

**As-Is:** Unchanged from the 2026-08-12 baseline: the desired-state/GitOps
boundary, the five-workflow control inventory, and the
[Workspace As-Is, gap, and target matrix](#workspace-as-is-gap-and-target-matrix)
remain repo-static `Verified`.

**Gap and bounded target:** Unchanged. A future deployable artifact still
needs a separately approved promotion design; the current static QA setup is
still not CD or SLSA conformance.

**Missing evidence:** a hosted run identity for the current local HEAD,
required-check/ruleset enforcement, and any environment, OIDC, artifact, or
cache effect. **Owning authority:** platform and delivery owners named in the
[Workspace As-Is, gap, and target matrix](#workspace-as-is-gap-and-target-matrix).
**Safe boundary:** a separately authorized, redacted hosted-run or
administration observation tied to a specific revision/job/run
ID/conclusion; no dispatch, rerun, approval, or mutation. **Refresh trigger:**
a workflow trigger/job/permission/concurrency change, an Action revision
change, or a future approved CD/promotion design.

**Final disposition:** `Partial`, unchanged from the 2026-08-12 baseline. No
promotion. New claim registered: `CLM-WERPC-010-13`.

#### REQ-WERPC-023 GitHub Actions workspace and source consistency check

**Workspace delta:** `no-change`. All five workflows still declare
top-level default `contents: read`; only `labeler.yml`, `greetings.yml`, and
`stale.yml` request their narrow job-level issue/pull-request write
permissions. Every re-read remote `uses:` entry across the five files is
still a full 40-character commit SHA accompanied by a version comment
(for example `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 #
v7.0.1`); `actions/checkout` invocations still use `persist-credentials:
false` where checked out.

**External result:** representative URLs for `SRC-WERPC-036`, `039`, `040`,
and `041` were re-fetched; see the [shared source-outcome
table](#re-checked-external-sources-shared-by-req-werpc-022-req-werpc-023-and-req-werpc-033)
below. All four hold their previously adopted claim.

**As-Is:** Unchanged. Full-SHA action pinning and least-privilege default
permissions remain repo-static `Verified`, matching the current secure-use
guidance.

**Gap and bounded target:** Unchanged. A SHA pin is still not an
upstream-code audit, provenance claim, or hosted-run result; effective
per-run token/secret permission is still not established by a static
declaration.

**Missing evidence:** effective per-run permission resolution, fork/bypass
behavior, and upstream action source integrity. **Owning authority:**
platform and security owners for `.github/workflows/` and
`scripts/validate-github-actions-security.py`. **Safe boundary:** a
separately authorized, redacted hosted-run or Actions-policy observation
tied to a specific revision/job/run; no dispatch, rerun, or token
inspection. **Refresh trigger:** an Action revision, permission, or pinning
change, or a cited GitHub Actions/SLSA source materially changes.

**Final disposition:** `Partial`, unchanged from the 2026-08-12 baseline. No
promotion. New claim registered: `CLM-WERPC-010-14`.

#### REQ-WERPC-033 Verification and Validation workspace and source consistency check

**Workspace delta:** `no-change`. `.pre-commit-config.yaml` still declares
the same frozen remote hook set (`commitizen`, `pre-commit-hooks`,
`gitleaks`, `detect-secrets`, `markdownlint-cli2`, `check-jsonschema`,
`shellcheck-py`, `pre-commit-shfmt`, `zizmor-pre-commit`, `hadolint`,
`actionlint`, and more) alongside the local static-contract/governance
hooks; `docs/00.agent-governance/contracts/validation-surfaces.json` still
declares its `lanes`, `protectedLevels`, `evidenceLanes`, `validators`,
`ciJobs`, and `surfaces` keys; `docs/00.agent-governance/rules/quality-standards.md`
still defines the same `targeted -> affected -> staged -> tests ->
all-files -> formatter-review -> rerun -> diff-checks` canonical completion
sequence, result vocabulary, and handoff-evidence contract.

**External result:** representative URLs for `SRC-WERPC-042`, `043`, `058`,
and `059` were re-fetched; see the [shared source-outcome
table](#re-checked-external-sources-shared-by-req-werpc-022-req-werpc-023-and-req-werpc-033)
below. All four hold their previously adopted claim; `SRC-WERPC-043` newly
surfaces a `--no-require-hashes` flag (pip 26.2), which extends rather than
contradicts the adopted `--require-hashes`/`--only-binary` basis.

**As-Is:** Unchanged. The
[Verification and Validation question matrix](#verification-and-validation-question-matrix)
and the ordered local completion sequence remain repo-static/local-static
`Verified` for the named command and scope; testing remains a shared method,
not a synonym for either term.

**Gap and bounded target:** Unchanged. No current-HEAD requirements-to-result
trace, discrepancy/root-cause record, independence evidence,
stakeholder/user participation, intended-use scenario, representative
environment, or live-system result was observed this cycle.

**Missing evidence:** stakeholder/user intended-use scenarios, an
independent-review record proportionate to risk, and any hosted or
remote/live V&V evidence. **Owning authority:** QA and the product/
requirements owner named in the
[Verification and Validation question matrix](#verification-and-validation-question-matrix).
**Safe boundary:** a separately authorized, non-secret intended-use or
stakeholder-scenario review against the exact cited requirement/spec
baseline; no live or remote action. **Refresh trigger:** the requirement,
spec, artifact, quality-lane, or traceability contract changes, or the cited
NASA handbooks are revised.

**Final disposition:** `Partial`, unchanged from the 2026-08-12 baseline. No
promotion. New claim registered: `CLM-WERPC-010-15`.

#### Re-checked external sources (shared by REQ-WERPC-022, REQ-WERPC-023, and REQ-WERPC-033)

A representative URL from each of the twelve registered rows
`SRC-WERPC-035`–`044` and `SRC-WERPC-058`–`059` was re-fetched on
**2026-08-14**. Eleven held their previously adopted claim; one relocated.

| Source (registered row)                                                                                                                                                                                                                                                                           | Result      | Note                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) (`SRC-WERPC-035`)                                                                                                                                                                           | `unchanged` | Still documents `on`, `jobs`, `permissions`, `if`, `needs`, and `concurrency` as distinct workflow controls; no visible last-modified date.                                                                                                                                                                                                                                                                                               |
| [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) (`SRC-WERPC-036`)                                                                                                                                                                                        | `unchanged` | Still states full-length commit SHA pinning is the only immutable-release option and recommends least-privilege `GITHUB_TOKEN` defaults.                                                                                                                                                                                                                                                                                                  |
| [Concurrency](https://docs.github.com/en/actions/concepts/workflows-and-actions/concurrency) (`SRC-WERPC-037`)                                                                                                                                                                                    | `unchanged` | Still describes concurrency groups as canceling superseded pending runs by default, with an opt-in queuing mode.                                                                                                                                                                                                                                                                                                                          |
| [Store and share data with workflow artifacts](https://docs.github.com/en/actions/tutorials/store-and-share-data) (`SRC-WERPC-038`)                                                                                                                                                               | `unchanged` | Still documents `retention-days` as a configurable per-upload period bounded by the repository/organization/enterprise limit; the paired "Removing workflow artifacts" URL under this row was not individually re-fetched this cycle.                                                                                                                                                                                                     |
| [OpenID Connect](https://docs.github.com/en/actions/concepts/security/openid-connect) (`SRC-WERPC-039`)                                                                                                                                                                                           | `unchanged` | Still describes a per-job auto-generated OIDC token with claims a cloud provider matches against preconfigured trust conditions; the paired OIDC reference URL under this row was not individually re-fetched this cycle.                                                                                                                                                                                                                 |
| [Using artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations) and [reusable workflows for SLSA Build L3](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/increase-security-rating) (`SRC-WERPC-040`) | `unchanged` | Still requires `attestations: write`, `contents: read`, and `id-token: write` (plus `packages: write` for containers) for a reusable-workflow SLSA Build Level 3 path.                                                                                                                                                                                                                                                                    |
| [Specification stages and versioning](https://slsa.dev/spec-stages) (`SRC-WERPC-041`)                                                                                                                                                                                                             | `unchanged` | Still defines Draft/Candidate/Approved/Retired stages and MAJOR.MINOR versioning; no current-version claim is adopted from this page.                                                                                                                                                                                                                                                                                                     |
| [pre-commit autoupdate options](https://pre-commit.com/#pre-commit-autoupdate-options) (`SRC-WERPC-042`)                                                                                                                                                                                          | `unchanged` | Still documents `--bleeding-edge`, `--freeze`, `--repo`, and `-j`/`--jobs`, and that default behavior updates to the latest default-branch tag.                                                                                                                                                                                                                                                                                           |
| [Secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/) (`SRC-WERPC-043`)                                                                                                                                                                                                        | `unchanged` | Still documents hash-checking mode, `--require-hashes`, and `--only-binary :all:`; newly notes a `--no-require-hashes` flag (pip 26.2) not previously recorded, which extends rather than contradicts the adopted basis.                                                                                                                                                                                                                  |
| [Using environments for deployment](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-environments-for-deployment) (`SRC-WERPC-044`)                                                                                                                        | `changed`   | The registered URL now returns HTTP 404. Equivalent content — protection rules, required reviewers, environment-scoped secrets/variables, and deployment-branch restrictions — is now published at `docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments`. Recorded as a relocation, not a content change; the adopted "no environment/deployment found" repository-static claim is unaffected. |
| [NASA Product Verification](https://www.nasa.gov/reference/5-3-product-verification/) (`SRC-WERPC-058`)                                                                                                                                                                                           | `unchanged` | Still defines verification as confirming an end product conforms to its specified requirements, answering "was the end product realized right," through test/analysis/inspection/demonstration with documented objective evidence.                                                                                                                                                                                                        |
| [NASA Product Validation](https://www.nasa.gov/reference/5-4-product-validation/) (`SRC-WERPC-059`)                                                                                                                                                                                               | `unchanged` | Still defines validation as confirming the end product satisfies stakeholder expectations within its intended operational environment, answering "was the right product done."                                                                                                                                                                                                                                                            |

No `kubectl`, `k3d`, `helm`, `argocd`, `vault`, `gh`, or `gh api` command was
run; only public documentation pages were fetched. No row is promoted to
`Verified`; no row is `Contradicted`. New source registered: `SRC-WERPC-077`.
New claims registered: `CLM-WERPC-010-13` through `CLM-WERPC-010-15`.

### 2026-08-20 full-corpus reverification

This closed-corpus increment consumes the immutable delivery/quality report
for `REQ-WERPC-022`, `023`, `024`, and `033`, checked on 2026-08-20. The report
re-opened the already registered GitHub, pre-commit, pip, SLSA, and NASA
primary sources and found no adopted-claim contradiction. It proposes no new
source or claim identity. The workspace baseline is commit
`8d8c8e5634fe939f8daaf041fbf5dfb444ed4a9c`; observations below distinguish
that repository-static baseline, the separately authorized remote metadata,
and outcomes that remain unproven.

#### Evidence boundary and remote metadata

The guarded remote summary, SHA-256
`da137936a4ec5cbb10c06303b96e22cc933188fec7042b8aa0dd774e627d4d21`,
passed its schema, uniqueness, field-allowlist, and nine-class completeness
check. That validation establishes only that the retained projection satisfies
the evidence contract. It does not validate workflow behavior, policy
effectiveness, stakeholder acceptance, deployment, or intended use.

| Evidence class | Sanitized collection-period result (2026-08-21..22 UTC) | Bounded interpretation |
| --- | --- | --- |
| `actions-permissions` | Observed: Actions enabled, allowed-actions mode `all`, selected-actions URL absent. | Dated repository-setting metadata only; it does not override tracked full-SHA pins or prove effective per-run authorization. |
| `workflow-permissions` | Observed: default workflow permission `read`; workflow approval of pull-request reviews disabled. | Default-policy projection, not evidence of a particular job token, fork path, secret, or review outcome. |
| `rulesets` | Observed empty list. | No ruleset was returned at collection time; historical absence, bypass behavior, and enforcement are not inferred. |
| `branch-protection` | Observed on `main`: required `ci-summary` check with app ID `15368`, `strict=false`, administrator enforcement disabled, approving-review count `0`, and stale-review dismissal disabled. | This records projected settings, not that a merge was blocked, a check covered the current local HEAD, or a review was sufficient. |
| `environments` | Observed total `0`. | No environment was listed at collection time; environment history, secrets, approvals, deployment, and their absence are unproven. |
| `artifacts` | Observed total `0`. | No retained artifact was listed at collection time; upload, deletion, retention correctness, historical existence, integrity, and provenance remain unproven. |
| `runs` | Observed 20 retained records, all `completed`: 13 `success`, 7 `failure`, across 8 unique head SHAs. | Historical conclusion metadata only. It supplies no current-local-HEAD hosted result, failure root cause, requirement coverage, promotion, rollback, or live-health evidence. |
| `workflows` | `unavailable`, reason `checker-auth-context-incompatible`. | The remote workflow inventory is unproven. No workflow-list or parity conclusion is adopted. |
| `oidc` | `unavailable`, reason `checker-oidc-schema-incompatible`. | The actual repository OIDC setting, subject format, trust, claims, token exchange, and use remain unproven. |

GitHub's existing OIDC source row (`SRC-WERPC-039`) continues to define the
job-scoped identity design boundary. The current official
[OIDC REST contract](https://docs.github.com/en/rest/actions/oidc) additionally
defines `use_default` as boolean and `include_claim_keys` as optional and
ignored when the default format is used. That API contract explains why a
nullable projection needs checker handling, but the discarded raw response
cannot establish this repository's value. The fixed local recovery therefore
records compatibility unavailability, not an OIDC setting or absence claim.
This diagnostic API contract is not a newly allocated ledger source and adopts
no repository-setting claim.

#### Closed request dispositions

| Request | Workspace As-Is | Gap / retained boundary | Target | Verification / disposition |
| --- | --- | --- | --- | --- |
| `REQ-WERPC-022` | Five tracked workflows implement static CI, changelog review-artifact creation, and maintenance; no tracked deployment, publish, cloud-login, promotion, or rollback workflow was found. | Remote workflow inventory is unavailable, retained runs are historical metadata, and zero listed artifacts/environments do not prove historical or runtime absence. Hosted current-revision execution, promotion, rollback, reconciliation, and live health remain `DEFER` (`hosted-ci`). | If delivery is introduced, bind a protected promotion owner to artifact identity, claim-aware least privilege, bounded rollback, and independent post-change health evidence. | `Partial`. Reverify static declarations with focused validators; require a separately authorized run identity and remote/live record for deeper claims. |
| `REQ-WERPC-023` | All five local workflows retain top-level `contents: read`, narrow maintenance writes, concurrency, full 40-character action SHAs with version comments, and checkout credential suppression where used. | Actions/default-token and branch-policy projections narrow only the evidence uncertainty; they neither strengthen nor prove per-run permission, authorization or enforcement, upstream action integrity, fork/bypass behavior, ruleset enforcement, secrets, or OIDC. | Preserve least privilege, immutable action references, script ownership, and explicit remote-setting evidence without treating any one control as supply-chain conformance. | `Partial`. Static Actions validators and the dated sanitized setting projection are distinct evidence; hosted effectiveness remains `DEFER` (`hosted-ci`). |
| `REQ-WERPC-024` | The quality contract retains targeted, affected, staged, tests, all-files, formatter-review, rerun, and diff-check evidence; frozen hooks cover repository formatting, lint, syntax, and security surfaces. | A configured hook or static contract does not prove every command ran. No general browser/end-to-end or mutation-testing lane is declared for this infrastructure/documentation topology. | For each change, record the exact command, version, path/index scope, and result; add executable-surface-specific unit, integration, end-to-end, mutation, and coverage contracts only when such a surface exists. | `Verified` at repository-static depth (`repo-static`); command-specific outcomes are separately required and cannot promote hosted or live status. |
| `REQ-WERPC-033` | Requirements Validation, Product/Artifact Verification, and Product/System Validation remain separate questions; testing is one method, not a synonym for any of them. | No current-HEAD requirement-result trace, discrepancy closure, risk-proportionate independent review, stakeholder/user participation, intended-use scenario, or representative environment was observed. | Bind an approved requirement/spec and artifact version to bidirectional verification evidence, then separately validate intended use with named stakeholders/users, representative scenarios/environment, discrepancies, corrective action, and closure. | `Partial`; product/stakeholder validation remains `DEFER` (`human-judgement`). A `VAL-*` identifier or static PASS is not a validation outcome. |

#### Delivery and QA control matrix

| Scope | Workspace As-Is | Gap / `DEFER` | Target | Verification rule |
| --- | --- | --- | --- | --- |
| Triggers and jobs | `ci.yml` declares `push`/`pull_request` on `main` plus manual dispatch, an explicit affected-surface `changes` job, selected static jobs, and fail-closed `ci-summary`; tag and maintenance workflows retain their narrower purposes. | Static YAML does not prove GitHub parsed, selected, scheduled, or completed the current revision. | Keep trigger, selection, dependency, timeout, and final failure semantics explicit. | Validate syntax/topology locally; use a retained hosted run identity for scheduler and conclusion claims. |
| Concurrency | All five workflows declare scoped concurrency; CI cancels superseded ref runs while changelog retains tag runs. | Queue and cancellation behavior remain hosted-system outcomes. | Preserve scope-specific cancellation policy and revisit it when release/promotion semantics change. | Static declaration is repository evidence; actual ordering/cancellation needs run metadata. |
| Artifact and environment | Changelog declares a seven-day `CHANGELOG.md` review artifact; delivery workflows declare no environment. Remote totals were both zero. | Neither declaration nor zero listing proves upload, access, retention/deletion, historical absence, protection, approval, secret handling, or integrity. | Define artifact identity, classification, retention, digest/signer checks, and protected environment only with an approved delivery design. | Require artifact/environment identifiers and dated administration or run evidence; otherwise `DEFER`. |
| Promotion and rollback | Desired state changes only through governed Git; no workflow performs promotion, deployment, or rollback. | A Git revert contract is not proof of reconciliation, recovery time, or health. | Give promotion and rollback separate owners, authorization, stop conditions, and post-change health method. | Verify the changed artifact, then validate recovery in an authorized representative environment. |
| Permissions and action references | Local defaults are read-only, maintenance writes are narrow, remote actions are full-SHA-pinned, and checkout credentials are suppressed where used. | A declaration or SHA does not audit source code, transitive dependencies, runner integrity, or effective token/secret use. | Retain least privilege and immutable references; review upstream code/provenance and runtime permission separately when risk requires it. | Run the static Actions/security validators; require per-run evidence for effective authorization. |
| Shell and script ownership | Workflow orchestration owns bounded inline shell; reusable repository checks are routed through named `scripts/` or `infrastructure/tests/` owners. | Inline install/selection shell remains workflow-owned and can drift from script contracts; successful syntax is not semantic correctness. | Keep reusable policy in reviewed scripts and leave only bounded orchestration inline; extract repeated or growing logic through its canonical owner. | `actionlint`/shell/static contract checks cover syntax and declared linkage; behavior needs direct tests or hosted evidence. |
| Supply chain | Frozen pre-commit revisions, full-SHA actions, hash-required binary-only Python installs, and a checksum-verified Gitleaks bootstrap are declared. | These controls do not establish transitive provenance, SLSA conformance, attestation, signer trust, or produced artifact integrity. | Bind dependencies and artifacts to digest, signer, provenance, and verification policy appropriate to the release. | Treat `SRC-WERPC-036`, `040`, `041`, and `043` as design benchmarks, not conformance evidence. |
| Formatting, lint, and syntax | Pre-commit and repository validators cover whitespace, structured data, Markdown, shell, Actions, Dockerfile, and manifest/static contracts when selected. | Formatter success can mutate bytes and cannot prove semantics; dormant Prettier is not coverage. | Review mutations, restage the exact logical set, and rerun the affected gates. | Report each named command and path/index scope as `PASS`, `SKIP`, `FAIL`, or `DEFER`. |
| Unit and integration tests | Validator self-tests and infrastructure/GitOps/secret/Vault-ESO contract tests exist for their named surfaces. | No generic application unit/integration suite or invented coverage percentage applies to this Bash/YAML/Markdown repository. | Add surface-specific tests and coverage criteria with a future executable feature. | A direct suite result proves only its selected behavior and fixture boundary. |
| End-to-end and mutation | No reviewed CI job declares browser/end-to-end or mutation testing. | Missing lanes are not passing or skipped evidence; production-user flow and fault-detection strength remain unmeasured. | Introduce them only with a product surface, representative journey/fault model, owner, stable fixture, and result contract. | Until then, record the lane as absent/`DEFER`, never `PASS`. |
| Affected, staged, all-files, and diff | The central quality contract defines affected selection, exact-index staged runner plus plain pre-commit, all-files pre-commit, formatter review/rerun, and unstaged/staged diff checks. | One lane cannot substitute for another, and a working-tree pass does not prove the Git index. | Preserve the ordered completion sequence and exact staged logical unit. | Record every command, selected path set, index state, formatter mutation, rerun, and final diff result independently. |

#### Verification and Validation implementation matrix

| Concern | Workspace As-Is | Gap / `DEFER` | Target | Required evidence |
| --- | --- | --- | --- | --- |
| Requirements Validation | PRD/Spec/acceptance review can inspect whether requirements are correct, complete, feasible, verifiable, and agreed before implementation (`SRC-WERPC-059`). | No named stakeholder agreement or current requirements-validation session was observed. | Resolve ambiguity and disagreement with requirements owners before treating the baseline as verification input. | Approved requirement revision, participants, review method, findings, changes, and agreement/closure. |
| Product/Artifact Verification | Targeted checks, tests, analysis, inspection, review, and demonstrations can compare an identified artifact with approved criteria (`SRC-WERPC-058`). | Static PASS is bounded to the named command and does not establish intended-use fitness. | Maintain bidirectional requirement-to-result trace for the exact artifact/commit and method environment. | Requirement and criterion IDs, artifact identity, method/tool/version, result, discrepancy, corrective action, and re-verification closure. |
| Product/System Validation | The workspace definition reserves validation for stakeholder expectations and intended use in an intended or representative environment (`SRC-WERPC-059`). | No named stakeholder/user/operator, intended-use scenario, representative environment, or acceptance result was collected. | Plan validation separately after sufficient verification, with realistic scenarios and affected users/operators. | Expected-versus-observed scenario results, participants, product/environment versions, discrepancies, corrective action, and revalidation. |
| Testing as a method | Tests are one admissible verification or validation method when their oracle and environment answer the stated question. | A test name alone does not identify the requirement, oracle, representativeness, or independence. | Select test, analysis, inspection, or demonstration according to the risk and question. | Method rationale, inputs, oracle, setup, observed result, and limitation. |
| Traceability | Spec/Task/Plan and `VAL-*` identifiers provide repository routing points. | Identifier presence is not a bidirectional requirement-to-result record or outcome. | Link requirements through design, implementation/artifact, method, result, discrepancy, and closure. | Both forward and backward links with versioned baselines and exact result identities. |
| Discrepancy handling | Fail-closed local lanes expose nonconformance at their bounded surface. | No generic root-cause, waiver, corrective-action, or recurrence-prevention record follows from a failing conclusion alone. | Classify the discrepancy, preserve evidence, correct the artifact or method, and re-run; control any waiver explicitly. | Finding identity, impact, owner, root cause where known, decision, corrective action, and closure/retest evidence. |
| Independence | Reviews and validators can be separated from implementation, proportionate to risk. | Tool execution or a second agent does not automatically establish organizational independence or IV&V. | Name reviewer authority, conflicts, method, and independence level required by risk. | Reviewer/authority record, scope, separation, findings, resolution, and approval limits. |
| Representative users and environment | No local static command claims a production user, operator, hosted runner, cloud trust, cluster, or live workload. | Stakeholder acceptance and intended-use fitness cannot be inferred from repository or remote metadata. | Use named anticipated users/operators and a justified representative environment without exposing secrets. | Participant roles, scenario, environment equivalence/limitations, safety controls, expected/observed results, and closure. |

The initial focused integration probe correctly returned
`ERROR INTEGRATION_SECTION` before this append. After integration, the same
probe returned `PASS validate-integration`; the Actions-security, CI-Python,
affected-surface, agent-governance-CI, strict Markdown, strict links/owners,
and diff checks also passed. These are named repository-static results only.
No result in this section authorizes workflow dispatch, rerun, approval,
setting mutation, deployment, publication, push, or merge.

### 2026-08-23 conditional OIDC and supply-chain increment

GitHub's current [OIDC security reference](https://docs.github.com/en/actions/reference/security/oidc)
adds a date-sensitive boundary: the immutable subject-format behavior applies
automatically to repositories created after 2026-07-15, while an existing
repository can enter that format by opt-in or by a qualifying rename or
transfer after that date. This public product rule does not establish this
repository's creation, rename, or transfer history, opt-in state, effective
subject format, issued JWT claims, cloud trust policy, token exchange, or
workload identity. Those
administration and runtime evidence classes remain `DEFER`.

The tracked workflows still declare no `id-token: write` permission or cloud
identity consumer. At repository-static depth, no immediate OIDC workflow or
trust-configuration change is justified. If OIDC is later introduced, the
owner must record the repository creation/rename/transfer history or opt-in
decision, exact subject and audience contract, least-privilege job boundary,
cloud-side trust conditions, and a separately authorized redacted exchange
result.

The [secure-use guidance](https://docs.github.com/en/actions/reference/security/secure-use)
and [artifact-attestation guidance](https://docs.github.com/en/actions/concepts/security/artifact-attestations)
do not change the existing boundary: a full commit SHA is the immutable action
reference, not an upstream-code or transitive-provenance audit, and generating
an attestation is distinct from consumer-side verification against explicit
repository, workflow, signer, and digest expectations. No attestation,
verification, hosted run, or release artifact was inspected; those outcomes
remain `DEFER`.

## Related Documents

- [Platform security](m0007-kubernetes-infrastructure-and-security.md)
- [Source coverage and migration ledger](m0012-source-coverage.md)
- [GitHub configuration hub](../../../../.github/README.md)
- [Quality and Evidence Policy](../../../00.agent-governance/policies/quality.md)
- [Validation routing registry](../../../../scripts/validation/registry.json)
- [Scripts inventory](../../../../scripts/README.md)
