---
title: 'Reference: CI/CD, GitHub Actions, and QA'
type: content/reference
status: active
owner: platform
updated: 2026-08-12
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
records are in [the pack ledger](source-coverage-and-migration-ledger.md).

## Authority Boundary

`.github/workflows/` owns tracked workflow declarations; `.github/README.md`
routes their repository purpose; and
[`quality-standards.md`](../../../00.agent-governance/rules/quality-standards.md)
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
([SRC-WERPC-035](source-coverage-and-migration-ledger.md#source-register)).
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
([SRC-WERPC-036](source-coverage-and-migration-ledger.md#source-register)).

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
observed ([SRC-WERPC-037](source-coverage-and-migration-ledger.md#source-register)).

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
| Verification | Was the artifact realized right: does the identified product or work product conform to its approved specified requirements?             | Implementer/engineer with QA or an independent reviewer proportionate to risk. Full IV&V is not implied.                       | Versioned requirement/specification baseline, acceptance criteria, artifact/commit version, approved method, tools, and environment.                        | Bidirectional requirement-to-result trace plus test, analysis, inspection, or demonstration record; method/tool/environment versions; pass/fail; discrepancies, waivers, corrective action, and closure ([SRC-WERPC-058](source-coverage-and-migration-ledger.md#source-register)).                       | The artifact is nonconforming, or the method/procedure/environment was invalid. Stop, diagnose, correct and reverify, or process an explicitly controlled waiver.                                                                       | During SDLC implementation/review, targeted/affected/staged/tests and structural validators provide bounded conformance evidence. Release readiness links the approved Spec/Plan/Task/Policy baseline to artifact identity and results; operations use Runbook verification/evidence steps. `VAL-*` names a criterion, and static PASS is not intended-use or live fitness. |
| Validation   | Was the right product realized: does the verified product satisfy stakeholder expectations and intended use in its intended environment? | Product/requirements owner, affected stakeholders, and anticipated users/operators; independent review strength is risk-based. | Verified product version, stakeholder expectation or requirement baseline, intended use/ConOps, scenarios, validation plan, and representative environment. | Expected-versus-observed scenario results under realistic or justified simulated conditions; participating stakeholder/user identities; environment/tool versions; discrepancies, corrective action, and revalidation closure ([SRC-WERPC-059](source-coverage-and-migration-ledger.md#source-register)). | The setup was not representative, or the product/requirements/design cannot satisfy intended use. Correct the setup and repeat, or rework the expectation, requirement, design, or product with stakeholder involvement and revalidate. | Requirements validation begins during PRD/ARD/Spec review; product/system validation belongs at release readiness and operational scenarios with stakeholders/users. Without separately authorized intended-use, user/operator, hosted, remote, or live evidence, release/operations validation is `DEFER`, never inferred from repository-static PASS.                     |

Testing is a method available to both terms, not a synonym for either one.
Requirements validation is an earlier agreement and quality check on the
requirements themselves; it must not be conflated with later product/system
validation. Traceability must bind stable identities and versions in both
directions so a change can select affected verification and intended-use
scenarios rather than merely link filenames.

### Supply-chain, cache, artifact, environment, and identity boundaries

| Control                 | Repository-static finding                                                                                                                                                            | Evidence and follow-up boundary                                                                                                                                                                                                      |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Dependencies            | Four validation jobs use Python 3.12 and the reviewed fully pinned/all-hash Linux lock with `--only-binary :all:` and `--require-hashes`; direct pins and lock are separately owned. | pip describes hash checking and binary-only resolution as installation constraints ([SRC-WERPC-043](source-coverage-and-migration-ledger.md#source-register)); this does not prove downloaded bytes, package safety, or portability. |
| Gitleaks bootstrap      | Two CI jobs download a fixed v8.30.0 Linux asset and verify its recorded SHA-256 before installation; a local contract validator reconciles the declaration.                         | Runtime download, publisher identity, GitHub-managed secrets, and history settings are `DEFER`.                                                                                                                                      |
| Artifacts               | One pinned upload action retains a changelog artifact for seven days.                                                                                                                | GitHub artifact retention/deletion behavior is source-backed ([SRC-WERPC-038](source-coverage-and-migration-ledger.md#source-register)); upload, retrieval, access control, and retention outcome are hosted/admin evidence.         |
| Cache                   | No `actions/cache`, dependency cache, or cache-key policy was found.                                                                                                                 | Do not claim cache isolation or poisoning resistance. Before adding cache, model trusted writers/readers, keys, invalidation, secret exclusion, and release-input boundary.                                                          |
| Environments/deployment | No job `environment`, deployment API/action, registry publish, or cloud login was found.                                                                                             | Protected environment, approval, and deployment state are `DEFER`; a deploy design needs a dedicated owner and evidence plan.                                                                                                        |
| OIDC                    | No `id-token: write` or cloud trust declaration was found.                                                                                                                           | GitHub OIDC uses job-scoped tokens and requires claim-aware trust design ([SRC-WERPC-039](source-coverage-and-migration-ledger.md#source-register)); no workload is currently evidenced as using it.                                 |
| Attestation/SLSA        | No attestation permission/action, provenance/SBOM, signer verification, reusable build workflow, or admission enforcement was found.                                                 | GitHub attestation and SLSA documents provide a future benchmark ([SRC-WERPC-040](source-coverage-and-migration-ledger.md#source-register)); no level or conformance is claimed.                                                     |
| Hook supply chain       | Remote pre-commit repositories use unique full commits and frozen tag comments.                                                                                                      | The pre-commit update procedure preserves revision provenance ([SRC-WERPC-042](source-coverage-and-migration-ledger.md#source-register)); transitive hook environments and cold offline replay remain `DEFER`.                       |

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

## Sources

Current primary-source rows are `SRC-WERPC-035` through `SRC-WERPC-044` in the
[source register](source-coverage-and-migration-ledger.md#source-register).
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

| Evidence class | Sanitized observation | Bounded interpretation and rejected inference |
| --- | --- | --- |
| Workflow inventory | The projected repository list returned seven active workflows. Five paths match the five tracked workflows in this checkout; two projected active paths do not. | This proves a dated hosted inventory difference, not the content, safety, trigger, or current-branch provenance of either unmatched workflow. The tracked five remain the only locally reconciled workflow bodies. |
| Run sample | The bounded latest-20 projection returned 20 completed runs: 15 `success` and five `failure`, across push, pull-request, schedule, and dynamic events. None used the current local HEAD. | Hosted execution exists for sampled historical revisions. Conclusion alone does not identify root cause, requirement coverage, current-HEAD status, deployment, promotion, rollback, or live GitOps outcome. |
| Actions policy | Actions is enabled; the repository policy allows all actions. The default workflow token setting is `read`, and workflow approval of pull-request reviews is disabled. | This is a repository-setting snapshot. Local full-SHA pins, read-default workflow declarations, and narrow job writes remain separate static controls; neither layer proves effective per-run token use, upstream integrity, fork behavior, or runner isolation. |
| Rules and branch protection | The projected ruleset list was empty. The `main` branch-protection projection returned one required status check, with strict up-to-date checking disabled; administrator enforcement was false and required approving review count was zero. | This records only projected settings at collection time. It does not prove a merge was blocked, a check mapped to the current local revision, higher-order review quality, bypass history, or policy effectiveness. Null projected fields are not generalized beyond the queried branch-protection shape. |
| Environments and artifacts | Both projected repository totals were zero. | No environment or retained artifact was listed at collection time. This does not prove historical absence, deletion/retention correctness, secret absence, release state, deployment absence, or artifact integrity. The tracked changelog upload declaration remains static only. |
| OIDC | The read executed, but the checker rejected the officially valid nullable projected claim-key shape. A reviewed local-only recovery recorded `unavailable` with empty identities and a fixed non-body limitation. | OIDC customization is `UNPROVEN`/`DEFER`. No retry, raw recovery, token request, claim observation, cloud trust, identity exchange, deployment, or absence inference is permitted. |

The local reconciliation remains internally consistent. Five tracked workflow
bodies declare default `contents: read`; remote actions are full-commit pinned
with version comments; checkout credentials are disabled where used; `ci.yml`
selects affected surfaces and fails closed through `ci-summary`; four validation
jobs use the fully hashed binary-only Linux/CPython 3.12 lock; pre-commit uses
frozen remote revisions; and the affected/staged/all-files contract keeps
syntax and repository-static evidence distinct. The hosted inventory difference
does not authorize importing or interpreting the two unmatched workflow bodies.

| Request | Final disposition | Evidence gained | Remaining boundary and follow-up |
| --- | --- | --- | --- |
| `REQ-WERPC-022` | `Partial` | Bounded hosted workflow/run metadata now establishes a dated inventory and historical run sample. | No sampled run matches current local HEAD. Current-revision hosted verification, run root cause, deployment, promotion, rollback, reconciliation, and live health remain `DEFER`; refresh on workflow/run topology change or with an approved current-revision run identity. |
| `REQ-WERPC-023` | `Partial` | Projected Actions/default-token, ruleset, branch-protection, environment, and artifact settings materially narrow the prior administration gap. | OIDC is unavailable; effective per-run permissions, merge enforcement, bypass/fork behavior, secret values, artifact integrity/retention, and any environment or identity use remain `DEFER`; refresh when an allowlisted class or named local workflow/validator changes. |
| `REQ-WERPC-033` | `Partial` | The sampled hosted conclusions are bounded verification metadata for identified historical revisions, and local lanes remain reproducible static conformance methods. | No current-HEAD requirements-to-result trace, discrepancy/root-cause record, independence evidence, stakeholder/user participation, intended-use scenario, representative environment, deployment, or live-system result was observed. Product/stakeholder validation remains `DEFER`. |

Syntax/static validation, hosted run metadata, repository administration,
product/stakeholder validation, and deployment/live effects therefore remain
five separate evidence depths. No row is promoted to `Verified`: all three
admitted requests remain `Partial`, with the explicit `DEFER` boundaries above.

## Related Documents

- [Platform security](kubernetes-infrastructure-and-security.md)
- [Source coverage and migration ledger](source-coverage-and-migration-ledger.md)
- [GitHub configuration hub](../../../../.github/README.md)
- [Quality standards](../../../00.agent-governance/rules/quality-standards.md)
- [Validation surface contract](../../../00.agent-governance/contracts/validation-surfaces.json)
- [Scripts inventory](../../../../scripts/README.md)
