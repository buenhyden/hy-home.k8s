---
title: 'Audit: CI, QA, Automation, Pipeline, and Workflow'
type: content/reference
status: done
owner: platform
updated: 2026-07-14
---

# Audit: CI, QA, Automation, Pipeline, and Workflow

## Overview

이 문서는 Current research의 CI/CD, QA, formatting, linting, automation,
pipeline, workflow, 공급망 기준을 고정된 repository snapshot과 대조한
dated implementation audit다. 33개 통제를 delivery topology, QA/AI-agent
obligations, supply-chain automation 범주로 나누어 채점한다. 설정,
로컬 실행, CI wiring, optional fallback, remote/live proof는 서로 다른
evidence lane으로 유지한다.

이 보고서는 CI job DAG, workflow 개수, QA wiring의 canonical audit
owner다. Kubernetes, GitOps, infrastructure, security desired-state 상세는
후속 `kubernetes-infrastructure-security.md`가 소유하며, 여기서는
delivery boundary와 QA 연결점만 채점한다.

### Purpose

- Audit workflow triggers, permissions, concurrency, job dependencies, path
  filters, aggregate gates, artifacts, and delivery ownership.
- Separate formatting, linting, parsing, static policy, optional tools, and live
  QA evidence by configuration and execution lane.
- Compare gateways, role bodies, postflight, shared workflows, hooks, and guidance
  with the risk-based AI-agent `pre-commit run --all-files` benchmark.
- Assess supply-chain controls according to this documentation/manifest home-lab
  repository's actual artifacts and threat surface, not an assumed product build.

## Reference Type

- Type: dated-implementation-audit
- Audit observation SHA: `a85df194bbb8ebc61187b905afaef7f95215cc2f`
- Research cutoff: `2026-07-10 10:00 KST`
- Source checked: 2026-07-11
- Refresh trigger: workflow/job/filter/action reference, pre-commit hook, validator,
  provider QA wiring, artifact/release contract, GitOps delivery owner, DORA
  consumer, or audit method change.

## Authority Boundary

- **Authoritative for**:
  - The 33 scored controls and repository evidence at the audit observation SHA.
  - CI workflow/job/DAG/path-filter counts, QA wiring, AI-agent all-files
    obligation comparison, and routed delivery/automation findings.
- **Not authoritative for**:
  - Active workflows, pre-commit configuration, scripts, hooks, agent adapters,
    guidance, GitOps manifests, branch protection, permissions, or operations.
  - Remote GitHub Actions runs/rulesets, live Kubernetes/Argo CD/Vault/ESO,
    provider hook consumption, deployment, credential, or secret-value readiness.
  - Detailed Kubernetes/security controls owned by
    `kubernetes-infrastructure-security.md`.

## Scope

- Includes the five GitHub workflows, CI's six-job DAG, Dependabot, pre-commit,
  formatter/linter/parser/static-policy lanes, shared provider QA wiring, local/CI
  guidance, changelog artifact, GitOps pull boundary, DORA evidence, and relevant
  supply-chain automation.
- Excludes active-owner edits, remote workflow dispatch or setting inspection,
  live cluster commands, credentials/secrets, release publication, deployment,
  push, and merge.

## Definitions / Facts

### Evidence and Scoring Basis

All repository claims below are read from audit observation SHA
`a85df194bbb8ebc61187b905afaef7f95215cc2f` using `git show` and
`git ls-tree`, not from the evolving audit branch. The exact 12 fields and
`sum(maturity) / (4 * applicable controls)` formula come from the
[pack audit method](README.md#audit-method). Static configuration and local
PASS evidence cannot prove a remote GitHub run or live reconciliation.

`Not in scope`/`N/A` rows state why the control is irrelevant or conditional and
are excluded from maturity arithmetic. Every actionable row has a priority,
one canonical SDLC owner, and measurable acceptance evidence. Every no-action
row uses the exact required `N/A — no action` value in the final three fields.

### Fixed Workflow and Delivery Topology

At the observation SHA there are five workflow files and ten jobs: six in
`ci.yml`, plus one each in changelog, greeting, labeler, and stale. The exact CI
DAG is:

```text
branch-policy (PR only) ------------------------------------------+
                                                                |
changes --------+--> pre-commit (precommit == true) ------------+--> ci-summary
                +--> repo-quality-static (repo_quality == true) -+
                +--> manifest-static (manifests == true) --------+
```

`branch-policy` and `changes` are independent roots. `changes` exports three
path-filter outputs; `precommit: '**'` selects every observed changed path, while
the specialist filters are narrower. `ci-summary` needs all five predecessors,
runs under `always()`, and rejects failure/cancelled while allowing an expected
conditional skip. This is tracked topology, not proof of a remote run or
required-check ruleset.

The five workflows contain 15 `uses:` references, zero full 40-hex action SHA
pins, one `upload-artifact`, zero explicit cache configuration, and zero
`workflow_call` or local reusable-workflow invocation. `ci.yml` has no deploy,
publish, registry, `kubectl`, `argocd`, or Git push step. The declared delivery
path is therefore:

```text
repository change -> local/static QA -> GitHub CI declaration -> review/merge
  -> Argo CD pull/reconcile intent (configured, not observed here)
```

### Delivery Topology Controls

| ID | Benchmark | Expected control | Repository evidence | Maturity | Verdict | Confidence | Gap | Recommendation | Priority | Follow-up owner | Acceptance evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CICD-001 | [Automation, Pipeline, Workflow, and QA](../../research/2026-07-07-wer/automation-pipeline-workflow-qa.md); GitHub workflow syntax | CI and maintenance workflows use explicit, bounded events and branch/tag filters. | At the observation SHA, `ci.yml` selects push/PR to `main` plus manual dispatch; changelog selects `v*.*.*` tags; labeler/greeting use bounded PR/issue events; stale uses one schedule. | 2 repository-static | Implemented | Verified repo-static | No missing tracked trigger contract; remote event delivery is separately excluded. | Preserve explicit event and branch/tag scopes. | N/A — no action | N/A — no action | N/A — no action |
| CICD-002 | GitHub least-privilege `GITHUB_TOKEN` guidance | Each workflow declares only the token permissions its steps need and checkout does not retain credentials unnecessarily. | CI and changelog declare `contents: read` and set checkout `persist-credentials: false`; labeler grants `contents: read`/`pull-requests: write`; greeting and stale grant only issue/PR write scopes. | 2 repository-static | Implemented | Verified repo-static | No excess tracked scope identified for the declared jobs; effective remote defaults are not inferred. | Preserve least-required scopes and disabled checkout credential persistence. | N/A — no action | N/A — no action | N/A — no action |
| CICD-003 | GitHub concurrency guidance | Duplicate runs have explicit grouping and cancellation semantics appropriate to CI, maintenance, and evidence generation. | All five workflows declare concurrency. CI cancels the same ref; greeting/labeler/stale cancel duplicate maintenance; changelog preserves an in-progress tag evidence run with `cancel-in-progress: false`. | 2 repository-static | Implemented | Verified repo-static | No missing tracked concurrency declaration; remote queue behavior was not observed. | Preserve workload-specific cancellation semantics. | N/A — no action | N/A — no action | N/A — no action |
| CICD-004 | Current automation DAG benchmark; GitHub `needs`/conditions | Independent roots, conditional specialist jobs, and one aggregate gate expose failure/cancelled/skipped results without implying a serial chain. | `git show` of `ci.yml` proves two roots, three `changes` dependents, and `ci-summary` needing all five predecessor jobs under `always()`; the summary rejects failure/cancelled and reports skipped jobs. | 2 repository-static | Implemented | Verified repo-static | No missing tracked DAG/aggregate behavior; this configuration is not a remote run result. | Keep the exact DAG and skipped-versus-failed semantics documented together. | N/A — no action | N/A — no action | N/A — no action |
| CICD-005 | Current path-filter-to-validator benchmark | Every validator has a machine-checked inventory of the paths that can affect its contract, and CI selects it for each such path. | `precommit: '**'` is broad, but `repo_quality` omits most `gitops/**`, `policy/**`, infrastructure, Traefik, and several root tool configs even though repo-quality contracts can inspect related surfaces; `manifest-static` covers many but runs a different bundle. | 2 repository-static | Partial | Verified repo-static | Missing: an executable filter-to-validator dependency inventory; a surface-only change can bypass the validator whose contract later expands to consume it. | Define one path-to-validator inventory and regression-test positive/negative fixtures before changing filters. | P1 near-term integrity | New Stage 03 Spec: ci-filter-and-validator-dependency-contract | Fixtures cover every validator input/config path, fail one deliberately omitted relevant path, prove intentional exclusions, and keep aggregate skip/failure behavior unchanged. |
| CICD-006 | Current relevance-based cache/reuse benchmark | Cache or reusable workflow complexity is introduced only for repeated dependency/build cost or duplicated job bodies with measured benefit. | Focused fixed-tree scans find zero cache declarations and zero reusable workflow definitions/invocations; the repository has no application build/package pipeline, and current small jobs install only PyYAML or pre-commit environments. | N/A — excluded until latency or duplication evidence establishes a consumer | Not in scope | Conditional | Excluded: no measured cache bottleneck or repeated publish/build workflow justifies additional state or abstraction. | Keep direct jobs; reassess only from CI duration/duplication evidence. | N/A — no action | N/A — no action | N/A — no action |
| CICD-007 | Current changelog/artifact benchmark | Tag-triggered changelog automation produces bounded evidence without silently mutating tracked history, releasing, or deploying. | `generate-changelog.yml` has read-only contents permission, runs git-cliff for `v*.*.*`, fails if `CHANGELOG.md` is absent, uploads one run artifact, and says tracked updates require PR merge; it has no push/release/deploy step. | 2 repository-static | Implemented | Verified repo-static | No missing behavior for a preview artifact; retention and release-family relevance are assessed separately. | Preserve preview-only wording and non-mutation boundary. | N/A — no action | N/A — no action | N/A — no action |
| CICD-008 | OpenGitOps pull/reconcile principles; Current delivery boundary | CI owns static verification while Git owns desired state and Argo CD declares pull/reconciliation; no CI job impersonates deployment. | `ci.yml` has no deploy command. `root-application.yaml` and `applicationset-apps.yaml` point to `main`, declare automated prune/self-heal, and separate platform root from workload discovery. | 2 repository-static | Implemented | Verified repo-static | No CI/CD ownership conflation in tracked configuration; actual pull, health, drift, and convergence remain live-Unverified. | Preserve CI/static and Argo CD reconciliation as separate owners. | N/A — no action | N/A — no action | N/A — no action |
| CICD-009 | DORA's current five delivery metrics | Metric automation begins only with a named service, deployment event source, failure/recovery semantics, owner, privacy boundary, and retention consumer. | Fixed-tree scans find no automation that emits change lead time, deployment frequency, failed deployment recovery time, change fail rate, or deployment rework rate; research is the only vocabulary owner. | 0 absent | Gap | Verified repo-static | Missing: application/service delivery telemetry. Repository CI duration and commits cannot be relabeled as deployment performance. | Pilot metrics for one service only after defining merge, Argo CD deployment, failure, recovery, and rework events. | P3 optional/telemetry-gated | New Stage 03 Spec: service-delivery-metrics-pilot | One named service has documented event joins, owner/privacy/retention, five reproducible metric queries, baseline output, and tests rejecting CI-only proxy events. |
| CICD-010 | Pack evidence boundary; GitHub ruleset and run semantics | Remote runs, required checks, branch protection, artifact defaults, and Argo CD reconciliation are claimed only from approved remote/live evidence. | The observation SHA contains workflow declarations and static GitOps intent, but this audit did not inspect GitHub settings/runs or execute live Argo CD/Kubernetes checks. | N/A — excluded remote/live evidence lane | Not in scope | Unverified live | Excluded: repository declarations cannot prove remote enforcement or live reconciliation. | Keep readiness unclaimed until separately approved read-only evidence exists. | N/A — no action | N/A — no action | N/A — no action |

### QA Evidence Lane Separation

| Lane | Fixed-tree owner/evidence | What it can prove | Boundary |
| --- | --- | --- | --- |
| Configuration | `.pre-commit-config.yaml` has 21 hook IDs; `.editorconfig`, `.prettierrc.json`, `.prettierignore`, tool configs, validators, and provider JSON are tracked. | Declared tool version, selector, config, and routing intent. | Configuration alone is not local execution, CI result, provider consumption, or live proof. |
| Local execution | Manual changed-file/all-files pre-commit, repo-static scripts, explicit `bash -n`, and consumed PostToolUse/lifecycle hooks can produce command evidence. | Only the files/tools and exit results actually recorded by the task. | An installed hook is not universal; PostToolUse is changed-surface feedback, not full-suite proof. |
| CI declaration | `changes` selects `pre-commit` for `**`; specialist jobs run repo-quality and manifest/static bundles under declared conditions. | Deterministic workflow wiring and tool commands when GitHub executes the declared event. | The fixed tree does not prove a remote run, required-check setting, or branch protection. |
| Optional/fallback | Manifest validation prints `SKIP` when local kube-linter is absent; policy validation prints Conftest `SKIP` and always runs its PyYAML fallback; CI pre-commit separately provisions the kube-linter hook. | Exact optional/fallback semantics and which baseline remains. | A fallback PASS is not a Conftest PASS; manifest-static alone is not automatically kube-linter evidence. |
| Live/operator | `infrastructure/tests/run-all.sh` and component scripts are operator-run surfaces requiring approved context and prerequisites. | Only a separately approved, executed, recorded observation. | No live test ran for this audit; no Kubernetes, Argo CD, Vault, ESO, TLS, network, or deployment claim is made. |

### AI-Agent Verification Surface Comparison

| Surface at observation SHA | Active wording/wiring | Comparison with primary risk-based benchmark |
| --- | --- | --- |
| `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | Require explicit QA, CI/static validation, and template routing before handoff. | Strong general obligation, but no changed-file iteration/all-files trigger rule. |
| [Canonical provider adapter inventory](governance-harness-loop-providers.md#common-system-controls) | The canonical inventory records provider role adapters that route to generic postflight requirements; individual roles name bounded validation expectations. | Common handoff exists, but no adapter contains `pre-commit run --all-files`; duplicating the command into every adapter would create drift. |
| Stage 00 postflight and agentic rules | Require relevant commands, output review, hook-or-equivalent evidence, unresolved risks, and unavailable/SKIP/CI-only disclosure. | Owns completion semantics but does not encode the exact risk-based all-files triggers. |
| Shared `qa-cicd-workflow.md` | Requires predetermined local validation and repo-quality or equivalent before `Done`. | Does not name all-files pre-commit or hook/toolchain/global-format triggers. |
| Stage 05 CI/CD QA guide | Names `pre-commit run --all-files` as the pre-PR command and also says to run it for every change. | Provides an active command but is broader than changed-file iteration and omits the specific high-blast-radius retrigger list. |
| Shared hooks/provider JSON | Routes changed paths to formatting/style, shell parser, manifest/secret, and repo-quality commands where consumed. | Correct fast-feedback layer; static JSON and hook output do not replace full-suite command evidence. |
| `ci.yml` | Every observed change selects `pre-commit/action`; event/specialist checks remain separate. | CI matrix coverage complements local all-files evidence but cannot prove that the agent ran the pre-PR local obligation. |

### QA, Formatting, Linting, and AI-Agent Controls

| ID | Benchmark | Expected control | Repository evidence | Maturity | Verdict | Confidence | Gap | Recommendation | Priority | Follow-up owner | Acceptance evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QA-001 | [Current SDLC/QA benchmark](../../research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md); pre-commit | One versioned hook matrix is reproducible locally and selected in CI for every observed change, with hook file selectors preserved. | `.pre-commit-config.yaml` declares 21 hook IDs and pre-commit/commit-msg install types; the guide documents changed/all-files commands; CI's `precommit: '**'` invokes `pre-commit/action`. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing configured local/CI matrix; local installation and remote execution are not inferred. | Preserve pinned hook revisions, selectors, and local/CI command parity. | N/A — no action | N/A — no action | N/A — no action |
| QA-002 | Current formatting lane; EditorConfig | File hygiene and shell formatting have explicit versions, selectors, changed-file feedback, and CI execution. | End-of-file, trailing-whitespace, mixed-line-ending, and `shfmt` hooks are configured; shared PostToolUse routes applicable changed files; CI pre-commit runs the same hook configuration. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing active file-hygiene/shell-format lane; semantic correctness is outside formatting. | Preserve narrow selectors and review formatter-induced diffs. | N/A — no action | N/A — no action | N/A — no action |
| QA-003 | Current Prettier boundary; official Prettier guidance | A tracked formatter config is either explicitly dormant or has one versioned, scoped execution consumer with migration/rollback evidence. | `.prettierrc.json` and `.prettierignore` exist, but fixed-tree scans find no Prettier hook, workflow step, shared-hook command, package manifest, or script. | 1 documented/routed | Partial | Verified repo-static | Corrective: readers can mistake dormant configuration for enforced formatting; global wiring could also cause an unbounded repository rewrite. | Decide remove-versus-adopt from a representative diff and overlap analysis before changing any consumer. | P3 optional/telemetry-gated | New Stage 03 Spec: prettier-scope-and-consumer-decision | A sampled dry-run quantifies touched paths and conflicts; the Spec chooses removal or a pinned scoped consumer, defines migration/rollback, and makes docs/config/tool output agree. |
| QA-004 | CommonMark/local Markdown benchmark | Markdown style and repository-specific document structure run as distinct deterministic checks. | `markdownlint-cli2` is in pre-commit/CI; `validate-repo-quality-gates.sh` separately enforces taxonomy, template routes, headings, links/inventories, and generated/reference contracts. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing configured Markdown/style-versus-structure split. | Preserve independent tool and repository-contract failure messages. | N/A — no action | N/A — no action | N/A — no action |
| QA-005 | YAML 1.2.2 and data-format parser benchmark | YAML, JSON, TOML, provider JSON, and manifest YAML have explicit parser coverage without treating parse as schema/runtime proof. | Pre-commit config contains `check-yaml`, `check-json`, and `check-toml`; manifest-static uses PyYAML; shared hooks parse provider JSON on affected edits. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing configured data parser lane; Kubernetes admission and provider consumption remain excluded. | Preserve parser-versus-semantic wording and selectors. | N/A — no action | N/A — no action | N/A — no action |
| QA-006 | Current shell lint/format benchmark | Repository shell surfaces receive versioned ShellCheck and shfmt coverage in changed-file/local and CI lanes. | Both hooks select `scripts/**`, `infrastructure/**`, and shared hook scripts; provider PostToolUse invokes them for changed shell files; CI pre-commit uses the same config. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing configured shell lint/style lane; parser evidence is separately scored. | Preserve the shared file selector across both tools and hooks. | N/A — no action | N/A — no action | N/A — no action |
| QA-007 | Current syntax-lane benchmark | Bash grammar is explicitly checked in CI or another completion command, and evidence never upgrades tracked hook wiring into consumed provider proof. | The guide documents manual `bash -n`; shared post-validation/lifecycle scripts run repository-wide `bash -n` after matching shell edits when invoked. `ci.yml`, repo-quality, and harness have no dedicated Bash parser command. | 2 repository-static | Partial | Verified repo-static | Complementary: CI relies on ShellCheck/shfmt rather than an explicitly named Bash parser lane, while provider consumption is runtime-Unverified. | Add a bounded parser command to the owning CI/static bundle or prove with fixtures that the existing required shell tool is the deliberate grammar authority. | P2 planned improvement | New Stage 04 Task: shell-parser-evidence-alignment | A malformed shell fixture fails the selected required CI/local completion command; guide, scripts inventory, hook output, and CI summary name the same authority without claiming provider consumption. |
| QA-008 | GitHub workflow syntax/security tooling benchmark | Workflow edits deterministically run syntax/lint and security-style tools in local changed-file and CI lanes. | `actionlint` and Zizmor hooks are versioned; PostToolUse selects both for workflow YAML; `.github/**` selects pre-commit and repo-quality CI lanes. Immutable action identity is scored in supply-chain controls. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing configured workflow syntax/style lane; disabled immutable-pin enforcement is not hidden here. | Preserve separate syntax and supply-chain findings. | N/A — no action | N/A — no action | N/A — no action |
| QA-009 | Hadolint/Dockerfile benchmark | Any Dockerfile introduced or changed is selected by a versioned lint hook locally and in the all-change CI pre-commit lane. | `hadolint-docker` has an explicit Dockerfile filename selector; shared PostToolUse mirrors it; CI pre-commit runs the hook matrix, which may legitimately SKIP when no Dockerfile exists. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing prospective Dockerfile selector; SKIP with no applicable file is not a failure. | Preserve selector tests if Dockerfiles are added. | N/A — no action | N/A — no action | N/A — no action |
| QA-010 | Current manifest/static contract benchmark | Kubernetes/GitOps changes receive parser, linter, structure, static-contract, secret, and policy checks, with static/live limits explicit. | Kube-linter is a managed pre-commit hook; `manifest-static` runs static contracts, GitOps structure, YAML validation, secret handling, and policy gates for its broad manifest filter. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing required static bundle; API admission, reconciliation, health, and NetworkPolicy enforcement are not inferred. | Preserve the bundle and route detailed platform/security findings to its sole report owner. | N/A — no action | N/A — no action | N/A — no action |
| QA-011 | NIST SSDF/current secret-evidence benchmark | Source/history pattern scans and manifest plaintext-secret checks run without reading external secret values. | Gitleaks and detect-secrets are in the pre-commit/CI matrix; `check-secret-handling.sh` is in manifest-static and affected-path shared hooks. No command reads Vault/ESO values. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing assessed repo-static secret scan; rotation, delivery, auth, and live values are excluded. | Preserve value-free evidence and baseline/config ownership. | N/A — no action | N/A — no action | N/A — no action |
| QA-012 | Current policy-as-code benchmark | A deterministic baseline policy lane runs even when an optional richer engine is absent, and its result is not mislabeled. | `validate-policy-gates.sh` requires Python/PyYAML, optionally runs Conftest, and always runs a four-category built-in fallback; `manifest-static` invokes it for policy/relevant changes. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing deterministic fallback; it is not cluster admission or full Rego equivalence. | Preserve explicit fallback scope and PASS/SKIP labels. | N/A — no action | N/A — no action | N/A — no action |
| QA-013 | Current optional-tool evidence rule | Optional tools report SKIP distinctly while a named deterministic baseline remains, and CI lanes identify which tool supplied evidence. | `validate-k8s-manifests.sh` prints optional kube-linter SKIP but still parses YAML; policy prints Conftest SKIP but runs fallback; CI pre-commit separately manages kube-linter. | 2 repository-static | Implemented | Verified repo-static | No missing declared fallback/SKIP semantics; remote output is not claimed. | Keep task evidence tool-specific instead of collapsing all lanes into one PASS. | N/A — no action | N/A — no action | N/A — no action |
| QA-014 | Task 2 primary AI-agent QA obligation benchmark | Agents use changed-file/affected lanes during iteration, require all-files before PR/merge and after hook/validator/toolchain/global-format changes, and record PASS/SKIP/FAIL/unavailable boundaries from one active owner. | Three gateways require general QA; the [canonical provider adapter inventory](governance-harness-loop-providers.md#common-system-controls) records role adapters that point to generic postflight; postflight and shared QA workflow require relevant/static checks; the Stage 05 guide names all-files but says every change. None encodes the complete risk-based trigger rule. | 1 documented/routed | Partial | Verified repo-static | Corrective: active surfaces can yield both under-validation before PR/high-blast-radius changes and unnecessary all-files runs after every edit; Current research cannot become the active rule. | Put the nuanced rule in one active owner and make gateways, postflight, shared workflow, role bodies, and guide point to it rather than copy it. | P1 near-term integrity | New Stage 03 Spec: ai-agent-validation-obligation-alignment | Fixtures cover iteration, PR/merge, hook/validator/toolchain/global-format, unavailable, and live-excluded cases; three gateways, shared workflow, postflight, guide, and all adapters in the canonical inventory resolve to one rule with no conflicting trigger wording. |
| QA-015 | Current PostToolUse versus completion-proof benchmark | Fast changed-surface feedback mirrors affected CI owners at bounded cost, while explicit completion commands remain authoritative and provider consumption stays unclaimed. | Shared hooks cover formatting/style, provider JSON, Bash parser, manifest/secret, and repo-quality. They omit targeted static-contract/GitOps-structure/policy execution; provider JSON only declares wiring. | 2 repository-static | Partial | Conditional | Complementary: affected policy/static-contract edits can be locally green until CI, and static hook wiring cannot prove provider invocation. | Define a cost-aware changed-surface matrix with explicit defer-to-CI semantics; do not make provider hooks a permission or full-suite gate. | P2 planned improvement | New Stage 03 Spec: affected-surface-feedback-matrix | Positive/negative fixtures map every CI validator input to local run/defer behavior, record latency budget and PASS/SKIP/DEFER, and keep provider-native consumption in separately approved canaries. |

### Supply-Chain Automation Controls

The relevance test begins with the artifacts this repository actually produces.
It proposes GitOps desired state and a changelog preview artifact; it does not
build or publish a first-party application, container, package, or release
artifact. Action identity and secret scanning are relevant now. CodeQL,
dependency review, SBOM, provenance, attestation, and Scorecard remain explicit
decision gates rather than seven automatic implementation failures.

| ID | Benchmark | Expected control | Repository evidence | Maturity | Verdict | Confidence | Gap | Recommendation | Priority | Follow-up owner | Acceptance evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SUP-001 | GitHub Actions secure-use guidance; Current automation benchmark | Every third-party Action executes an immutable reviewed commit, while update automation and human-readable version context keep pins maintainable. | The five workflows contain 15 `uses:` references and zero full 40-hex pins; every reference uses a tag. `.github/zizmor.yml` disables `unpinned-uses`. | 1 documented/routed | Partial | Verified repo-static | Corrective: mutable tags do not provide immutable action identity, and the configured security linter deliberately does not enforce the official benchmark. | Inventory owners/SHAs, record version comments and rollback, verify Dependabot behavior, then enable immutable-pin enforcement in one coordinated change. | P1 near-term integrity | New Stage 03 Spec: github-actions-immutable-dependency-identity | All 15 references resolve to reviewed full SHAs with source/version annotations; a fixture with a tag fails Zizmor/CI; Dependabot update and rollback rehearsal preserves least privilege and workflow behavior. |
| SUP-002 | Dependabot GitHub Actions ecosystem | Action dependency updates are proposed on a bounded schedule with grouping/cooldown, while proposal automation is not called security proof. | `.github/dependabot.yml` declares weekly `github-actions` updates, labels, one group, and a seven-day cooldown; the file is checked by pre-commit. Remote proposal delivery was not inspected. | 2 repository-static | Implemented | Verified repo-static | No missing tracked proposal configuration; Action immutability and review remain separate controls. | Preserve bounded update proposals and review every resulting workflow diff. | N/A — no action | N/A — no action | N/A — no action |
| SUP-003 | GitHub CodeQL relevance gate | CodeQL is adopted only when a supported first-party source language and analysis/build owner enter the repository. | Fixed-tree workflow/config scans find no CodeQL lane and no first-party application build pipeline in the audited delivery surface; current executable QA owners are shell/static validators. | N/A — excluded until supported first-party source and build ownership exist | Not in scope | Conditional | Excluded: adding CodeQL without an analyzable source/build owner would create an empty enterprise lane rather than evidence. | Reassess if supported application source is added. | N/A — no action | N/A — no action | N/A — no action |
| SUP-004 | GitHub dependency-review relevance gate | Dependency-review automation is added only for a defined dependency graph/manifest and protected PR change class not already owned by Action pinning. | Fixed-tree scans find no dependency-review workflow. Current automated dependencies are GitHub Actions, owned by Dependabot plus SUP-001; GitOps image/chart risks belong to the platform/security audit. | N/A — excluded until an applicable dependency graph and PR policy exist | Not in scope | Conditional | Excluded: no distinct package dependency-change consumer is identified in this report's scope. | Reassess with the first package/build dependency graph or a security-owned GitOps dependency decision. | N/A — no action | N/A — no action | N/A — no action |
| SUP-005 | NIST SSDF/SBOM relevance gate | An SBOM describes a built or distributed artifact with an owner, format, generator, retention, and vulnerability consumer. | The audited workflow set builds no application/package/container; the only uploaded file is a generated changelog preview. Fixed-tree scans find no SBOM generator or consumer. | N/A — excluded because no first-party build/distribution artifact exists | Not in scope | Conditional | Excluded: an SBOM for a Markdown preview would not improve the actual GitOps dependency threat model. | Reassess when an owned build/publish artifact is introduced. | N/A — no action | N/A — no action | N/A — no action |
| SUP-006 | SLSA/GitHub provenance and attestation relevance gate | Provenance/attestation binds a promotable artifact to an approved build identity and verification consumer. | No workflow builds, publishes, signs, deploys, or promotes a first-party artifact; fixed-tree scans find no provenance/attestation action. Changelog preview is explicitly non-release evidence. | N/A — excluded because no promotable build artifact or verifier exists | Not in scope | Conditional | Excluded: attesting a non-promotable preview would add ceremony without a verification decision. | Reassess with the first approved artifact build/promotion design. | N/A — no action | N/A — no action | N/A — no action |
| SUP-007 | OpenSSF Scorecard relevance gate | Scorecard is introduced as an owned risk signal only when a public/dependency consumer, triage process, false-positive budget, and retention decision justify it. | Fixed-tree workflow/config scans find no Scorecard lane or local consumer; current actionable workflow risk is the directly testable immutable-pin failure in SUP-001. | N/A — excluded pending a consumer and triage contract | Not in scope | Conditional | Excluded: a broad score would not replace the concrete action-identity control or prove home-lab runtime security. | Reassess from dependency/public-consumer demand after immutable pinning is resolved. | N/A — no action | N/A — no action | N/A — no action |
| SUP-008 | GitHub artifact retention; Current changelog evidence benchmark | Artifact lifetime is explicit when a named release/audit consumer requires it; otherwise remote defaults are acknowledged rather than guessed. | The one `upload-artifact` step sets name/path/`if-no-files-found` but no `retention-days`; no remote repository default was inspected and no active Release family/retention consumer exists. | 1 documented/routed | Partial | Conditional | Complementary: the preview exists, but its evidence lifetime is controlled by an unverified remote default and has no approved consumer requirement. | Decide whether the preview is transient diagnostics or retained release evidence before setting a duration. | P3 optional/telemetry-gated | New Stage 04 Task: changelog-artifact-consumer-and-retention-decision | The Task names the consumer or records transient disposition; if retained, workflow/tests assert an approved duration and deletion/rollback path; if transient, guide and summary explicitly say so. |

### Score and Distribution Summary

| Category | Applicable controls | Maturity numerator | Denominator | Implementation | Maturity distribution (`0/1/2/3/4`, applicable only) | Verdict distribution (`Implemented/Partial/Gap/Not in scope`, all rows) | Confidence distribution (`Verified repo-static/Unverified live/Conditional`, all rows) | N/A exclusions |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| Delivery topology | 8 | 14 | 32 | 43.8% | `1/0/7/0/0` | `6/1/1/2` | `8/1/1` | CICD-006 cache/reuse; CICD-010 remote/live |
| QA and AI-agent obligations | 15 | 38 | 60 | 63.3% | `0/2/3/10/0` | `11/4/0/0` | `14/0/1` | None |
| Supply-chain automation | 3 | 4 | 12 | 33.3% | `0/2/1/0/0` | `1/2/0/5` | `2/0/6` | SUP-003 CodeQL; SUP-004 dependency review; SUP-005 SBOM; SUP-006 provenance/attestation; SUP-007 Scorecard |
| **Overall** | **26** | **56** | **104** | **53.8%** | **`1/4/11/10/0`** | **`18/7/1/7`** | **`24/1/8`** | **Seven rows** |

Arithmetic is `14 + 38 + 4 = 56` over
`4 * (8 + 15 + 3) = 104`. The seven listed N/A controls are excluded from the
numerator and denominator. The eight actionable findings comprise three P1,
two P2, and three P3 findings; there are no P0 findings. No maturity 4 is
awarded because this evidence set contains no approved remote workflow,
provider-native hook, deployment, reconciliation, or live runtime observation.

### Actionable Finding Register

| Priority | Controls | Dependency-aware disposition |
| --- | --- | --- |
| P1 near-term integrity | CICD-005, QA-014, SUP-001 | Align the active validation obligation and executable path ownership first, then pin Actions with filter/validator fixtures so CI hardening cannot silently bypass required gates. |
| P2 planned improvement | QA-007, QA-015 | Use the affected-surface matrix to choose the shell parser authority and local DEFER semantics without promoting hooks to full-suite or permission enforcement. |
| P3 optional/telemetry-gated | CICD-009, QA-003, SUP-008 | Pilot only after a named service/formatter/artifact consumer and measured cost exist; absence alone does not justify a full delivery-platform redesign. |

### Comparison Analysis

- The strongest category is QA (63.3%): file hygiene, Markdown, data formats,
  shell lint/style, Actions, Dockerfile selection, Kubernetes, secrets, and
  fallback policy all have deterministic local/CI wiring.
- Delivery topology is explicit but remains repository-static. Correctly
  configured triggers, permissions, concurrency, and DAG cannot be promoted to
  remote required-check or Argo CD runtime proof.
- The primary AI-agent weakness is not absence of validation language; it is
  fragmented trigger semantics. General gateway/postflight obligations, an
  over-broad guide rule, changed-file hooks, and CI all-change selection need one
  active risk-based owner.
- The actionable supply-chain issue is immutable Action identity. Treating every
  absent enterprise scanner as a gap would obscure that concrete risk and invent
  build/release consumers the repository does not have.
- Consolidated improvement is preferred: one path-to-validator inventory, one
  active agent validation obligation, immutable Action pins, and explicit
  PASS/SKIP/DEFER semantics. A reusable-workflow/cache/SBOM/provenance/Scorecard
  redesign is not supported by current artifact or telemetry evidence.

### Residual Risks

- Path filters and workflow semantics were parsed from YAML; no remote event,
  ruleset, permission, artifact default, or result was observed.
- Pre-commit and validator configuration proves available commands, not that each
  developer installed hooks or that every AI provider consumed JSON wiring.
- Static manifest, secret, and policy PASS evidence cannot prove Kubernetes
  admission, Argo CD convergence, Vault/ESO delivery, network enforcement, or
  deployment health.
- A future first-party application or artifact pipeline would change the N/A
  relevance decisions and require a new dated audit rather than retroactive
  promotion of this score.

## Sources

- [Audit pack README and method](README.md)
- [Current Automation, Pipeline, Workflow, and QA Research](../../research/2026-07-07-wer/automation-pipeline-workflow-qa.md)
- [Current Spec, SDLC, CI, QA, and Formatting Research](../../research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md)
- [CI workflow](../../../../.github/workflows/ci.yml)
- [Generate changelog workflow](../../../../.github/workflows/generate-changelog.yml)
- [Dependabot configuration](../../../../.github/dependabot.yml)
- [Zizmor configuration](../../../../.github/ABOUT.md)
- [Pre-commit configuration](../../../../.pre-commit-config.yaml)
- [Shared QA workflow](../../../../.agents/workflows/qa-cicd-workflow.md)
- [Agentic execution rules](../../../00.agent-governance/rules/agentic.md)
- [Postflight checklist](../../../00.agent-governance/rules/postflight-checklist.md)
- [CI/CD and QA guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- [Scripts inventory](../../../../scripts/README.md)
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use)
- [GitHub workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [DORA metrics](https://dora.dev/guides/dora-metrics/)
- [OpenGitOps principles](https://opengitops.dev/)

Repository links above identify the active path; every implementation claim was
read from that path at the audit observation SHA.

## Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-07-11
- Next review trigger: workflow/job/filter/action reference, QA/hook/all-files
  obligation, artifact consumer, delivery metric, GitOps owner, or audit method
  change.
- Refresh method: retain the prior observation SHA, reparse every workflow and
  hook/validator selector, recount jobs/hooks/actions/artifacts, reevaluate N/A
  relevance from current artifacts, recalculate all distributions, and keep
  remote/live evidence separate.

## Related Documents

- **Audit pack**: [2026-07-11 WEIA README](README.md)
- **Implementation plan**: [WEIA implementation plan](../../../04.execution/plans/2026-07-11-workspace-engineering-research-audit-integration.md)
- **Current research pack**: [2026-07-07 WER README](../../research/2026-07-07-wer/README.md)
- **Parent audits index**: [Audits README](../README.md)
- **Platform/security audit owner**: `kubernetes-infrastructure-security.md`
- **Integrated remediation owner**: `remediation-roadmap.md`
