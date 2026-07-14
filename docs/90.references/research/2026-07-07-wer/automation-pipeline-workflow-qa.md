---
title: 'Reference: Automation Pipeline Workflow QA Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-11
---

# Reference: Automation Pipeline Workflow QA Research

## Overview

이 문서는 `hy-home.k8s`의 automation, pipeline, workflow, CI/CD, QA
feedback topology를 2026-07-11 fixed repository evidence와 공식 GitHub
Actions, pre-commit, DORA, OpenGitOps 자료에 대조한다. Current pack의 짧은
요약과 Historical pack의 유효한 조사 내용을 현재 파일·조건·소유권으로 다시
검증해 이 문서에 통합했다.

이 문서는 설명용 Stage 90 reference다. 활성 workflow, path filter, hook,
validator, GitOps manifest, branch protection, remote Actions 설정 또는 live
runtime을 정의하거나 변경하지 않는다.

### Purpose

- 다섯 workflow와 전체 열 job(`ci.yml` 여섯 job)의 실제 trigger,
  dependency, condition, output 관계를 설명한다.
- local hook/pre-commit, CI job, validator, optional dependency의 coverage를
  변경 surface별로 연결한다.
- CI의 static QA와 Argo CD의 pull-based delivery 경계를 분리한다.
- 확인된 automation gap을 severity, risk rationale, recommendation, canonical
  follow-up route가 있는 비변경 제안으로 기록한다.

## Reference Type

- Type: durable-concept / external-standard-snapshot /
  dated-implementation-audit
- External sources checked: 2026-07-10
- Repository snapshot checked: 2026-07-11 at
  `ab3556b8d5a9ae6f469a751057d9ad5ef261cdf7`
- Refresh trigger: GitHub workflow, path filter, Dependabot, pre-commit,
  provider hook wiring, validator, GitOps root/ApplicationSet, CI/CD QA guide,
  DORA metric definition, or OpenGitOps principle changes.

## Authority Boundary

- **Authoritative for**:
  - 2026-07-11 fixed repository snapshot에서 다시 도출한 workflow/job/filter/hook/
    validator/GitOps ownership mapping.
  - 아래 URL의 공식·primary 외부 자료와 local evidence의 dated comparison.
  - 이후 scoped task로 보낼 automation 개선 권고.
- **Not authoritative for**:
  - 활성 Actions semantics, branch protection/ruleset, required-check 설정,
    `GITHUB_TOKEN` 권한, hook enforcement, validator 동작 또는 GitOps 정책.
  - remote GitHub run, live Kubernetes/Argo CD/Vault/ESO, credential, secret,
    deployment, reconciliation 또는 service readiness.
  - 외부 benchmark만으로 추론한 local implementation 상태.

## Scope

- 포함: `.github/workflows/*.yml`, `.github/dependabot.yml`, labeler/Zizmor
  설정, `.pre-commit-config.yaml`, shared hook scripts와 provider hook wiring,
  repository/manifest/policy validators, infrastructure static/live tests,
  GitOps root Application/ApplicationSet, QA guide, delivery-metric context.
- 제외: 활성 파일 수정, workflow dispatch, remote setting 확인, live command,
  credential/secret-value 검사, deployment, publish, push, merge, release 생성.

## Definitions / Facts

### Automation, Workflow, Pipeline, CI, and CD

- **Automation**은 event 또는 local action으로 실행되는 기계 작업이다. 현재
  CI, changelog artifact 생성, PR labeling, first-interaction greeting, stale
  maintenance, Dependabot update, pre-commit과 provider-wired validation hook이
  여기에 해당한다.
- **Workflow**는 `.github/workflows/` 아래 하나의 Actions YAML이다. 현재 다섯
  파일이 있다.
- **Pipeline**은 trigger에서 job/step/validator/summary/artifact/task evidence로
  이어지는 ordered 또는 conditional evidence path다.
- **CI**는 변경을 통합하기 전후에 정적 품질 evidence를 생성하는 현재
  `ci.yml` QA gate다.
- **CD**는 승인된 desired state가 target environment에 전달·조정되는 별도
  delivery surface다. 이 저장소의 CI workflow에는 deploy job이 없고, Argo CD
  manifests가 pull/reconcile 의도를 선언한다. Repo-static 선언은 실제 배포
  또는 reconciliation proof가 아니다.

### Current Automation Inventory

| Surface | Repo-backed role | Trigger | Produced evidence | Boundary |
| --- | --- | --- | --- | --- |
| `.github/workflows/ci.yml` | Static QA gate | `push` to `main`, `pull_request` targeting `main`, `workflow_dispatch` | Branch-policy, path-filter, pre-commit, repo-quality, manifest-static results and aggregate result | No deploy, publish, live mutation, or remote-setting evidence |
| `.github/workflows/generate-changelog.yml` | Release-evidence generator | Tag push matching `v*.*.*` | Generated `CHANGELOG.md` run artifact and step summary | Does not commit, push, publish a release, or deploy |
| `.github/workflows/labeler.yml` | PR maintenance | PR opened or synchronized | Labels from `.github/labeler.yml` | Not CODEOWNERS, approval, QA, or deployment |
| `.github/workflows/greetings.yml` | Intake maintenance | First issue or PR opened | Greeting comment | Not QA or approval |
| `.github/workflows/stale.yml` | Scheduled maintenance | `30 1 * * *` | Stale labels/comments and configured closure | Not QA, release, or deployment evidence |
| `.github/dependabot.yml` | Dependency proposal automation | Weekly `github-actions` ecosystem scan | Grouped/cooldown Dependabot PRs | A proposal is not dependency safety proof |
| `.pre-commit-config.yaml` | Local/CI toolchain | Git hook, manual command, and `pre-commit/action` | File hygiene, secret, Markdown, JSON/TOML/YAML, shell, workflow, Dockerfile, and manifest tool results | Tool result only; not live or delivery evidence |
| Shared hook scripts | Provider-wired edit/lifecycle feedback | Provider event wiring in `.claude/settings.json`, `.agents/hooks.json`, `.codex/hooks.json` | Pre-edit warnings, scoped post-edit checks, lifecycle checks/advice | Wiring files do not prove every provider consumed or enforced the hook |

### Fixed Snapshot Counts and Tool Wiring

The fixed snapshot is
`ab3556b8d5a9ae6f469a751057d9ad5ef261cdf7`. No active workflow, hook,
validator, manifest, policy, or operations path changed between that commit and
the Task 4 branch state; only the approved Stage 90 roots changed. Counts below
therefore describe the fixed snapshot, not live GitHub or provider execution.

| Surface | Exact count / topology | Evidence meaning and limitation |
| --- | --- | --- |
| Workflow files and jobs | 5 workflows, 10 jobs total: CI 6; changelog, greeting, labeler, and stale 1 each. | Tracked YAML topology only; no remote run or required-check state was inspected. |
| CI path-filter outputs | 3: `precommit`, `repo_quality`, `manifests`; `precommit: '**'`, while the other two are specialist subsets. | Every observed change selects the configured pre-commit lane, but specialist-validator input coverage is incomplete. |
| CI DAG | Parallel roots `branch-policy` (PR only) and `changes`; `changes` fans out to `pre-commit`, `repo-quality-static`, and `manifest-static`; `ci-summary` needs all five predecessor jobs and runs `always()`. | A skipped conditional lane is reported but is not treated as failure; the aggregate rejects failure/cancelled results. |
| Pre-commit | 21 hook IDs; `default_install_hook_types` includes `pre-commit` and `commit-msg`. | Configured hook coverage, not proof that a developer installed the hook. The CI pre-commit job provides a separate declared execution lane. |
| Shared hooks | 4 scripts wired through three provider JSON surfaces for SessionStart, PreToolUse, PostToolUse, Stop/SubagentStop, and PreCompact. | Claude has a native permission list; Codex/Gemini JSON remains context/validation wiring. Consumption is runtime-Unverified. |
| Prettier | Root `.prettierrc.json` defines six options and `.prettierignore` defines 11 ignore entries. Zero pre-commit hook, workflow step, shared-hook call, or package script invokes Prettier. | Configuration is tracked but execution/enforcement is absent. Markdownlint and file-hygiene hooks are the active formatting/quality evidence. |
| Action dependencies | 15 `uses:` occurrences, 0 full 40-hex commit SHA pins. Dependabot proposes weekly Actions updates; Zizmor disables `unpinned-uses`. | Version tags are reproducible only while upstream tags remain stable; immutable dependency identity is not enforced. |
| Artifact | 1 `actions/upload-artifact` step uploads generated `CHANGELOG.md`; no explicit `retention-days` is declared. | A run artifact is configured, but there is no checked release publication, provenance/attestation, signature, or repository mutation. Retention follows the unverified remote default. |
| Optional tools | `manifest-static` installs PyYAML only. `validate-k8s-manifests.sh` skips kube-linter when absent; `validate-policy-gates.sh` runs its built-in four-category fallback and adds Conftest only when installed. The pre-commit job separately provisions its configured kube-linter hook. | CI-declared evidence must name which lane/tool produced it; a manifest-static PASS is not automatically a kube-linter or Conftest PASS. |
| Supply chain and DORA | No active workflow contains CodeQL, dependency-review, SBOM, provenance/attestation, signature verification, or Scorecard. No automation emits the five DORA metrics. | These remain relevance/threat-model decisions and measurement gaps, not implicit failures of an artifact-building product pipeline. |

### Actual CI Job DAG

The compact expression below is a mnemonic, not a serial `needs` chain:

```text
branch-policy || changes -> pre-commit/repo-quality-static/manifest-static -> ci-summary
```

Here `||` means **parallel roots**, not logical fallback. The exact DAG is:

```text
branch-policy (PR only) ------------------------------------------+
                                                                |
changes --------+--> pre-commit (precommit == true) ------------+--> ci-summary
                +--> repo-quality-static (repo_quality == true) -+
                +--> manifest-static (manifests == true) --------+
```

- `branch-policy` and `changes` declare no `needs`, so they begin independently.
  `branch-policy` has `if: github.event_name == 'pull_request'`; it is skipped on
  `push` and manual dispatch.
- `changes` is the only dependency of `pre-commit`, `repo-quality-static`, and
  `manifest-static`. It exports `precommit`, `repo_quality`, and `manifests`
  from `dorny/paths-filter`.
- `pre-commit` is selected by `precommit: '**'`, so an observed changed path
  selects it. `repo-quality-static` and `manifest-static` use narrower filter
  sets described below.
- `ci-summary` directly `needs` all five preceding jobs and uses `if: always()`.
  Its final step fails when any needed result contains `failure` or `cancelled`;
  a conditionally `skipped` job is summarized but is not itself treated as a
  failure.
- Workflow concurrency is `ci-${{ github.ref }}` with
  `cancel-in-progress: true`. Official GitHub documentation confirms that a
  concurrency group limits simultaneous runs and may cancel the in-progress
  member when configured this way.
- All CI jobs are static or toolchain checks. No job calls `kubectl`, `argocd`,
  a deployment API, a registry publish action, or a Git push command.

The earlier Current summary described
`branch-policy -> changes -> pre-commit -> ...` as a sequence. Current `needs`
evidence contradicts that ordering, so this document classifies the old wording
as a corrected **Fact defect**.

### Path Filter and Gate Coverage Matrix

| Changed surface | Local hook/pre-commit | CI job | Validator | Optional dependency | Coverage verdict |
| --- | --- | --- | --- | --- | --- |
| Any tracked changed path | Installed pre-commit runs staged files; manual `pre-commit run --all-files` runs the repository | `changes` then `pre-commit` because `precommit: '**'` | Full configured hook matrix, subject to each hook file selector/type | Local `pre-commit`; CI uses `pre-commit/action` and managed hook environments | **Sufficient** for configured toolchain scope; not full semantic or live proof |
| Markdown, Stage documents, governance, templates, shared/provider agent assets | File-hygiene and Markdown hooks; provider PostToolUse routes matching docs/assets to repo-quality | `pre-commit`; `repo-quality-static` for `docs/**`, `.agents/**`, `.claude/**`, `.codex/**`, root gateways, scripts, tests, examples, and listed config | `validate-repo-quality-gates.sh .` | Python + PyYAML are required; Markdown/pre-commit tool availability varies locally | **Sufficient repo-static** for encoded contracts; semantic correctness still needs review |
| GitHub workflows and `.github` config | `actionlint` and Zizmor target workflow YAML; `check-dependabot` targets Dependabot; provider PostToolUse selects workflow style only for workflow YAML | `pre-commit` and `repo-quality-static` because `.github/**` is included | Pre-commit tools plus repo workflow/config contracts | Hook environments; Zizmor `unpinned-uses` is locally disabled | **Needs strengthening** for immutable action provenance |
| Shell under `scripts/**`, `infrastructure/**`, shared hooks | `shellcheck`/`shfmt`; tracked provider JSON declares PostToolUse and Stop/SubagentStop routing to shared scripts that run repository-wide `bash -n` after matching shell edits | `pre-commit`; `repo-quality-static` for `scripts/**` and shared hooks through `docs/**`; `manifest-static` for `infrastructure/tests/**/*.sh` | ShellCheck, shfmt; explicit `bash -n` exists in the shared scripts and QA guide | Local pre-commit; CI has no separate `bash -n` step; declared wiring does not prove provider-native consumption | **Needs strengthening**: CI pre-commit has shell static/style checks, but repo-quality/harness do not themselves provide Bash syntax evidence |
| GitOps, infrastructure, examples, and Traefik YAML | Pre-commit kube-linter selector plus YAML/file hooks; provider PostToolUse runs manifest syntax and secret handling for matching YAML | `pre-commit` and `manifest-static`; `repo-quality-static` additionally selects only `gitops/apps/root/**` among GitOps paths | Static contracts, GitOps structure, YAML/PyYAML, kube-linter when present, secret handling, policy gate/fallback | `kube-linter` is optional inside `validate-k8s-manifests`; CI pre-commit has a managed kube-linter hook | **Needs strengthening**: manifest bundle is broad, while repo-quality filter coverage is narrower than contracts it can inspect |
| Policy bundle and policy validator | No targeted PostToolUse policy-gate invocation; general pre-commit hooks may apply by file type | `pre-commit` and `manifest-static` for `policy/**` or validator changes | `validate-policy-gates.sh .`; Conftest if installed, then built-in fallback always | `conftest` optional; CI installs PyYAML but not Conftest, so fallback is the direct manifest-static evidence | **Implementation gap** in edit-hook parity; CI fallback coverage exists |
| Static infrastructure contracts | Shell hooks apply when `infrastructure/tests/*.sh` changes | `pre-commit` and `manifest-static` | `infrastructure/tests/verify-contracts-static.sh` plus the full manifest-static bundle | GNU grep/Python/PyYAML and optional manifest tools | **Sufficient repo-static** for encoded patterns; regex contracts are not runtime proof |
| Root lint/security configs such as `.kube-linter.yaml`, `.gitleaks.toml`, `.secrets.baseline`, Markdown/Hadolint configs | Their consuming pre-commit hooks can run, but provider PostToolUse routing is file-specific and not uniform for every root config | `pre-commit`; `.kube-linter.yaml` also selects `manifest-static`; several other root tool configs do not select `repo-quality-static` | The consuming hook/tool configuration | Individual tool environments | **Needs strengthening**: filter-to-validator dependency ownership is not complete or machine-checked |
| Live test scripts and live cluster/runtime | Shell style/static checks only; no live execution in pre-commit or provider edit hook | No live CI job | `infrastructure/tests/run-all.sh` and component scripts are operator-run live surfaces | Reachable cluster, correct context, `kubectl`, network/TLS prerequisites | **Unverified** in this audit; repo-static/CI PASS cannot promote live readiness |

Dedicated Bash parser evidence must be named precisely: tracked provider JSON
declares routing to shared PostToolUse and lifecycle scripts, and those scripts
run `bash -n` after a matching shell edit when invoked. The CI/CD QA guide also
documents direct manual `bash -n` commands. Tracked wiring and payload/static
checks do not prove every provider host consumed the hooks. `ci.yml` does not
declare a separate `bash -n` step, and neither
`validate-repo-quality-gates.sh` nor `validate-harness.sh` is itself a general
shell syntax gate. CI shell evidence comes from the pre-commit ShellCheck/shfmt
hooks unless a task separately records explicit manual or consumed shared-hook
`bash -n` output.

### Permissions and Workflow Security Boundary

- `ci.yml` and `generate-changelog.yml` declare workflow-level
  `permissions: contents: read`; their checkout steps set
  `persist-credentials: false`.
- Labeler grants `contents: read` and `pull-requests: write`; greeting and stale
  grant only the issue/PR write scopes their maintenance actions use.
- Official `GITHUB_TOKEN` guidance recommends the least access required at
  workflow or job scope. The tracked permission declarations are repo evidence;
  no remote default permission or ruleset was inspected.
- All external Actions references in the five workflows use version tags such
  as `@v7.0.0`, `@v4`, or `@v3`, not full commit SHAs. GitHub secure-use
  guidance states that full-length commit SHA pinning is the immutable action
  reference. `.github/zizmor.yml` explicitly disables `unpinned-uses`, so the
  current tool configuration does not enforce that benchmark.

### Prettier Configuration Boundary

The repository does contain a root `.prettierrc.json` and `.prettierignore`.
The earlier 2026-07-05 audit statement that no tracked Prettier configuration
existed is a superseded fact defect. The current six configuration keys are
`printWidth`, `singleQuote`, `semi`, `trailingComma`, `arrowParens`, and
`endOfLine`; the ignore file excludes editor/cache/build/generated areas and
`package-lock.json`.

No `prettier` hook, workflow step, shared hook command, `package.json`, or
package-manager script exists in the checked repository. Therefore the correct
verdict is **configured but unwired**, not active formatting enforcement. A
later owner should either remove an intentionally unused config or define the
languages, version, execution command, diff/migration scope, and CI/pre-commit
consumer before wiring it. This Stage 90 refresh makes neither choice.

### GitOps Delivery Boundary

| Surface | Declared owner/path | Delivery behavior in tracked desired state | Evidence boundary |
| --- | --- | --- | --- |
| `root-platform` Application | `gitops/clusters/local/root-application.yaml` points to `gitops/apps/root` in `main` under project `platform` | Automated prune and self-heal are declared; `gitops/apps/root/kustomization.yaml` lists 18 platform Application manifests | Proves configuration and platform-app ownership, not a live sync or healthy controller |
| `platform-cluster-config` child Application | Root kustomization includes an Application whose source is `gitops/clusters/local` | Makes cluster-local AppProjects, root/ApplicationSet declarations part of the platform desired-state tree | Static ownership only; actual creation order and convergence were not observed |
| `apps-generator` ApplicationSet | `gitops/clusters/local/applicationset-apps.yaml` discovers `gitops/workloads/*` under project `apps` | Generates one application per workload directory, targeting namespace `apps`, with automated prune/self-heal | Proves workload-directory generator intent, not generated live Applications or health |
| GitHub `ci.yml` | Repository QA workflow | Validates changed desired state and repository contracts | It does not push desired state or invoke Argo CD/Kubernetes; therefore it is CI/static QA, not deployment CD |

OpenGitOps describes desired state as Declarative, Versioned and Immutable,
Pulled Automatically, and Continuously Reconciled. The repository contains
declarative, Git-versioned desired state plus pull/reconcile configuration.
Immutability enforcement, automatic pull occurrence, and continuous convergence
were not checked remotely or live and remain **Unverified**. The safe local
boundary is therefore:

```text
repository change -> local/static QA -> GitHub CI verdict -> review/merge
  -> Argo CD pull/reconcile intent (configured, not observed here)
```

### QA Feedback and Delivery Measurement

The current feedback topology produces repository and workflow evidence close
to a change: provider-wired edit feedback where consumed, pre-commit, conditional
CI jobs, `ci-summary`, changelog artifacts, and Stage 04 task records. GitHub's
visualization graph exposes job status and dependency lines, matching the need
to distinguish root, conditional, skipped, and aggregate jobs.

DORA's current model has five service/application-level software-delivery
metrics: change lead time, deployment frequency, failed deployment recovery
time, change fail rate, and deployment rework rate. Current repository searches
found descriptive DORA references but no workflow/script/task automation that
emits, stores, or dashboards these five measurements. They remain benchmark
vocabulary, not local performance evidence.

### Automation Gap Register

Every row below is a **recommendation only**. This research pass does not change
the named active files.

| Classification | Severity | Finding | Current evidence | Risk rationale | Recommendation | Canonical follow-up route |
| --- | --- | --- | --- | --- | --- | --- |
| Implementation gap | Medium | Path-filter-to-validator dependencies are incomplete | `repo_quality` includes `gitops/apps/root/**` but omits other `gitops/**`, `policy/**`, most infrastructure, Traefik, and several root tool configs; `manifest-static` covers many of those paths, but does not execute repo-quality | A contract added to repo-quality for an omitted surface can be bypassed on a surface-only PR even though another static lane passes | Define an explicit validator-input inventory and regression-test each path filter against it before changing filters | `.github/workflows/ci.yml`, `.github/ABOUT.md`, CI/CD QA guide, and a new Stage 03/04 CI-filter hardening spec/task |
| Implementation gap | Medium | Local provider edit hooks do not mirror the complete manifest-static policy bundle | `post-validate.sh` and `lifecycle-guard.sh` run manifest syntax and secret handling for manifest edits, but not static contracts, GitOps structure, or policy gates; `.rego` edits have no targeted PostToolUse policy run | Fast local feedback can be green while the later CI policy/static-contract lane fails | Design a bounded cost-aware hook matrix or explicit task checklist; retain CI as final authority | Shared hook scripts, three provider wiring files, `validate-harness.sh`, and a separately approved hook/validator task |
| Implementation gap | Medium | Two live ingress/TLS findings are warn-only | `verify-ingress-tls.sh` emits `[WARN]` for missing/mismatched Headlamp and Kiali TLS secrets and continues; `run-all.sh` can therefore reach its final PASS | A broad live-run PASS can be read as stronger than the component assertions actually enforce | Classify required versus advisory endpoints, make the final summary report both, and change failure semantics only through an operations-approved task | `infrastructure/tests/verify-ingress-tls.sh`, `run-all.sh`, Stage 05 setup/maintenance runbooks, and a Stage 03/04 live-test contract task |
| Implementation gap | High | Third-party Actions are tag-pinned rather than immutable-SHA-pinned | Every `uses:` entry in the five workflows uses a version tag; `.github/zizmor.yml` disables `unpinned-uses`; GitHub secure-use recommends full-length SHAs | Mutable upstream tags expand workflow supply-chain risk and make exact executed code less reproducible | Inventory each action, verify official repositories and SHAs, define update automation/rollback, then enable enforcement in one coordinated change | `.github/workflows/*.yml`, `.github/zizmor.yml`, version inventory, Dependabot policy, and a Stage 03/04 Actions-hardening task |
| Implementation gap | High | No active CI supply-chain evidence lane for code scanning, dependency review, SBOM, provenance, or attestation | Focused scans of workflows, Dependabot, and pre-commit found no CodeQL, dependency-review, SBOM, provenance, attestation, Cosign, or SLSA automation; changelog artifact generation is not provenance | Static lint/secret checks do not establish dependency-change review or build/release provenance | Threat-model applicable artifacts first, then adopt only the controls that match this manifest/document repository and define retention/verification evidence | Security policy/ARD, `.github/workflows`, Stage 05 release/runbook owner, and a new Stage 03/04 supply-chain task |
| Needs strengthening | Medium | Key static contracts rely heavily on textual/regex matching | `verify-contracts-static.sh` uses `grep -P`/`grep -Pz`; repo-quality and secret validators use extensive regex/text contracts alongside YAML parsing | Semantically equivalent YAML or document changes can cause false positives/negatives, while a text match may not prove object semantics | Classify contracts by schema/AST/text need, migrate high-risk checks to parsed structures, and add negative fixtures before removing proven sentinels | Validator scripts, `infrastructure/tests`, `tests`, scripts inventory, and a Stage 03/04 validator-quality task |
| Needs strengthening | Medium | DORA telemetry is absent | DORA terms appear in research/task context, but no checked workflow, script, or operations automation emits/stores the current five metrics | Delivery-improvement claims cannot be measured consistently and repo CI duration is not deployment performance | Select one service and define event sources, ownership, privacy, baselines, and dashboard/retention before instrumenting | New Stage 03 measurement spec and Stage 04 task; then approved operations observability and workflow changes |
| Needs strengthening | Low | Prettier is configured but has no execution consumer | `.prettierrc.json` and `.prettierignore` are tracked, but focused searches found no Prettier hook, workflow step, shared-hook call, package script, or package manifest | Readers can mistake dormant configuration for an enforced formatter, while wiring it without scope control could create a repository-wide formatting diff | Decide explicitly to remove the dormant config or adopt a versioned, language-scoped formatter with measured migration and rollback | New Stage 03 formatting-toolchain decision/spec; then `.prettierrc.json`, `.prettierignore`, pre-commit/CI/hooks, and CI/CD QA guide in one approved task |
| Needs strengthening | Low | Changelog artifact retention is implicit | One changelog upload step exists and declares `if-no-files-found: error`, but no `retention-days`; no remote repository default was inspected | Evidence lifetime is controlled outside the tracked workflow and may not match a future release-record retention need | Define the release-evidence consumer and retention requirement before adding an explicit workflow value | Release-contract ADR/Spec, then `generate-changelog.yml`, GitHub automation hub, and Stage 05 release evidence owner |

### Automation Restructuring Options

| Option | Scope and benefit | Cost / blast radius | Prerequisites | Migration | Rollback | Decision owner |
| --- | --- | --- | --- | --- | --- | --- |
| Minimal | Repair documentation facts, add focused regression tests for the existing three path filters, and explicitly classify dormant Prettier/optional tools. Lowest-risk improvement to evidence honesty. | Low / CI tests, guides, and references; existing job graph remains. | Exact validator-input inventory and baseline CI durations. | Add tests and summaries before any filter/tool change. | Revert tests/documentation; existing workflow topology remains usable. | QA Engineer with repository maintainer approval. |
| **Consolidated (default)** | Minimal work plus one machine-readable path-to-validator inventory, a cost-aware changed-surface local wrapper, explicit optional-tool evidence in summaries, and a single delivery-evidence contract connecting CI, changelog artifact, GitOps boundary, and applicable DORA events. | Medium / CI, pre-commit, shared hooks, validators, QA guide, and release-evidence owner; no deploy job is introduced. | Stage 03 CI/automation spec, latency budget, negative fixtures, tool version policy, artifact consumer/retention decision, and remote required-check review. | Introduce inventory/tests, run old and new selection in parallel, compare results/latency, then switch filters and summaries lane by lane. | Restore old filters and hook matrix; retain the inventory as documentation and keep Argo CD delivery separate. | System Architect and QA Engineer; Operations owns delivery metrics. |
| Full redesign | Replace conditional specialist lanes with reusable workflows/generated matrices, enforce immutable action identities and a broad supply-chain suite, wire Prettier globally, and build DORA telemetry. Potentially stronger uniformity and observability. | High / every workflow, formatter-sensitive file, hook/validator consumer, artifact/metric store, remote ruleset, and contributor toolchain. | Threat model, artifact/build inventory, reusable-workflow design, formatter migration sample, credentials/retention/privacy owners, cost/latency budget, and remote rollback access. | Shadow workflows and non-blocking telemetry first; pin/migrate one dependency or format family at a time; promote only after false-positive and runtime review. | Keep prior CI required checks available, disable new matrices/telemetry, and revert formatter enforcement without rewriting already reviewed history. | Product/Platform owner and Security/Operations decision group. |

`Consolidated` is the default because the observed failures are fragmented
ownership, incomplete filter dependency mapping, and ambiguous optional-tool
evidence. The repository has no build/publish/deploy pipeline or telemetry
consumer that justifies a full supply-chain/formatter/metrics redesign today.

## Sources

### Official and Primary External Sources

All eight sources below were opened read-only and checked on 2026-07-10.

- GitHub Actions workflow syntax (`jobs.<job_id>.needs`, conditions, filters,
  permissions, workflow/job structure):
  <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax>
- GitHub Actions visualization graph (job status and dependency lines):
  <https://docs.github.com/en/actions/how-tos/monitor-workflows/use-the-visualization-graph>
- GitHub Actions secure use (full-length action SHA benchmark):
  <https://docs.github.com/en/actions/reference/security/secure-use>
- GitHub `GITHUB_TOKEN` authentication and least-required permissions:
  <https://docs.github.com/en/actions/tutorials/authenticate-with-github_token>
- GitHub Actions concurrency groups and cancellation:
  <https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency>
- pre-commit installation and local/CI execution model:
  <https://pre-commit.com/>
- DORA's current five software-delivery performance metrics:
  <https://dora.dev/guides/dora-metrics/>
- OpenGitOps principles and pull/reconciliation benchmark:
  <https://opengitops.dev/>

These sources define external behavior or benchmark context. Current repository
files, not the external sources, establish local implementation claims.

### Repository Sources

- [GitHub configuration hub](../../../../.github/ABOUT.md)
- [CI workflow](../../../../.github/workflows/ci.yml)
- [Generate changelog workflow](../../../../.github/workflows/generate-changelog.yml)
- [Labeler workflow](../../../../.github/workflows/labeler.yml)
- [Greeting workflow](../../../../.github/workflows/greetings.yml)
- [Stale workflow](../../../../.github/workflows/stale.yml)
- [Dependabot configuration](../../../../.github/dependabot.yml)
- [Labeler configuration](../../../../.github/labeler.yml)
- [Zizmor configuration](../../../../.github/ABOUT.md)
- [Pre-commit configuration](../../../../.pre-commit-config.yaml)
- [Prettier configuration](../../../../.prettierrc.json)
- [Prettier ignore configuration](../../../../.prettierignore)
- [Shared pre-edit guard](../../../00.agent-governance/hooks/k8s-pre-edit.sh)
- [Shared post-edit validator](../../../00.agent-governance/hooks/post-validate.sh)
- [Shared lifecycle guard](../../../00.agent-governance/hooks/lifecycle-guard.sh)
- [Shared session-start hook](../../../00.agent-governance/hooks/session-start.sh)
- [Claude settings and hook wiring](../../../../.claude/settings.json)
- [Codex hook wiring](../../../../.codex/hooks.json)
- [Gemini/Antigravity hook wiring](../../../../.agents/hooks.json)
- [Scripts inventory](../../../../scripts/README.md)
- [CI/CD and QA guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- [GitOps root Application](../../../../gitops/clusters/local/root-application.yaml)
- [Workload ApplicationSet](../../../../gitops/clusters/local/applicationset-apps.yaml)
- [Root platform kustomization](../../../../gitops/apps/root/kustomization.yaml)
- [Historical automation reference integrated after re-verification](../2026-07-04-wer/automation-pipeline-workflow-qa.md)

## Review and Freshness

- Review cadence: on source change.
- Last reviewed: 2026-07-11.
- Next review trigger: any workflow/job/filter/action reference, Dependabot,
  pre-commit, hook routing, validator, GitOps root/ApplicationSet, live-test
  assertion, DORA metric, or OpenGitOps principle change.
- Refresh method: re-open the exact external URLs; re-parse every workflow and
  owning config; compare job `needs`/`if`/outputs and filter inputs; inventory
  hooks/validators/optional tools; recheck GitOps paths; record live and remote
  lanes as Unverified unless separately approved and observed.

## Related Documents

- **Current pack README**: [README.md](README.md)
- **Parent research README**: [../README.md](../README.md)
- **Parent references README**: [../../README.md](../../README.md)
- **Workspace baseline**: [Workspace Governance Baseline](workspace-governance-baseline.md)
- **SDLC/CI/QA reference**: [Spec SDLC CI QA Formatting](spec-sdlc-ci-qa-formatting.md)
- **Kubernetes/security reference**: [Kubernetes Infrastructure Security](kubernetes-infrastructure-security.md)
- **Current hardening spec**: [Workspace Engineering Research Pack Spec](../../../03.specs/017-workspace-engineering-research-pack/spec.md)
- **Current hardening plan**: [Current Research Pack Fact-First Hardening Plan](../../../04.execution/plans/2026-07-10-current-research-pack-fact-first-hardening.md)
- **Current hardening task**: [Current Research Pack Fact-First Hardening Task](../../../04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md)
- **Reference maintenance runbook**: [Reference Maintenance Runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
