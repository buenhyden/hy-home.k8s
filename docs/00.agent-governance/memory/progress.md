# Agent Progress and Memory Ledger

This file is the repo-local progress and reusable memory ledger for AI agent
work in `hy-home.k8s`. Use `docs/99.templates/progress.template.md` for new
entries. Memory here supports future task intake, but current runtime truth
stays in `docs/00.agent-governance/harness-catalog.md` and current script
inventory stays in `scripts/README.md`.

## Work Entries

### 2026-05-18 — 04.execution README normalization

- **Date**: 2026-05-18
- **Layer**: docs, execution, meta
- **Status**: complete
- **Tags**: #execution #readme #templates #validation

#### Progress

- Normalized the three `docs/04.execution` README surfaces to the repository
  README base structure: Overview, Audience, Scope, Structure,
  How to Work in This Area, Link Basis, and Related Documents.
- Removed duplicate legacy sections from `docs/04.execution/plans/README.md`
  and `docs/04.execution/tasks/README.md` while preserving their Structure
  trees and document indexes.
- Clarified the default routing split: plans own execution order, risk,
  gates, rollout, and rollback; tasks own executable work state and evidence.
- Standardized the touched execution README headings from Related References to
  Related Documents.

#### Memory

- `docs/04.execution/plans/README.md` and
  `docs/04.execution/tasks/README.md` should stay as compact entrypoints, not
  mixed template fragments plus historical duplicate sections.
- Existing Plan and Task artifact files were intentionally not normalized in
  this pass. Their historical status, date, and evidence fields remain owned by
  the artifact documents.
- The repository quality gate still allows `Related References` in some README
  surfaces, so touched-scope heading consistency needs a targeted check until
  the validator explicitly includes `docs/04.execution`.

#### Evidence

- Changed-file scope was limited to the three execution READMEs and this
  progress ledger entry.
- Targeted `docs/04.execution` Related References scan: PASS.
- Targeted execution README document-index scan: PASS.
- Targeted duplicate legacy heading scan: PASS.
- `git diff --check` PASS.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.

#### Handoff

- No Plan/Task artifact body, validator, template, Kubernetes manifest, ArgoCD
  object, cluster state, or Secret was changed.
- No live cluster mutation, direct ArgoCD action, or external service action was
  performed.

---

### 2026-05-18 — 03.specs traceability backfill

- **Date**: 2026-05-18
- **Layer**: docs, architecture, execution, operations
- **Status**: complete
- **Tags**: #specs #traceability #rollouts #notifications #validation

#### Progress

- Added current-contract ARD, Spec, Plan, and Task chains for Argo Rollouts
  progressive delivery and ArgoCD Notifications Slack integration.
- Replaced Rollouts/Notifications PRD downstream-gap wording with links to the
  new ARD/Spec/Plan/Task documents.
- Added downstream traceability backlinks to ADR-0011, ADR-0012, and the
  Rollouts/Notifications/Headlamp operations policy and runbook.
- Rebuilt `docs/03.specs/README.md` as a single stage README with five indexed
  specs and explicit currentness notes.
- Updated Spec 001, 002, and 003 frontmatter. Spec 003 now keeps Dashboard and
  `172.19.x` content only as superseded historical context, with Headlamp and
  `172.18.x` as the current contract.

#### Memory

- Rollouts chart notifications and ArgoCD Notifications are separate contracts:
  Rollouts keeps chart-level notifications disabled while ArgoCD Notifications
  owns Slack templates, triggers, and the Vault/ESO credential boundary.
- Spec 003 should use Headlamp, `mkcert-ca-issuer`, and `172.18.x` external
  service endpoints as current contract evidence; Dashboard-era values are
  historical only.
- Closeout for this task intentionally stayed in this progress ledger. No
  standalone memory note was created.

#### Evidence

- Targeted stale PRD gap scan over `docs/01.requirements` returned no matches.
- Dashboard terms in Spec 003 are marked historical/superseded or appear only
  in historical document/link names.
- Rollouts chart `notifications.enabled: false` is documented separately from
  ArgoCD Notifications `notifications.enabled: true`.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS.
- `bash scripts/check-secret-handling.sh .` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- `git diff --check` PASS.

#### Handoff

- No runtime manifest change, cluster mutation, Secret change, live ArgoCD
  action, or external Slack action was performed.
- Live cluster validation remains deferred unless a human explicitly requests
  an operator run against an available cluster.

---

### 2026-05-17 — 01.requirements PRD currentness remediation

- **Date**: 2026-05-17
- **Layer**: product, docs, meta
- **Status**: complete
- **Tags**: #requirements #prd #docs #validation

#### Progress

- Updated `docs/01.requirements/README.md` with PRD reading order,
  lifecycle/status interpretation, current-vs-historical contract guidance,
  and downstream gap visibility for Rollouts/Notifications PRDs.
- Clarified currentness and historical contract boundaries across the five
  existing PRDs in `docs/01.requirements/`.
- Aligned the platform expansion PRD around Headlamp as the current cluster UI,
  while preserving Kubernetes Dashboard as superseded ADR-linked history.
- Reframed Rollouts and Notifications requirements away from manifest-level
  implementation instructions and toward PRD-level value, constraints, and
  verifiable acceptance evidence.

#### Memory

- `docs/01.requirements` PRDs should preserve historical requirements instead
  of deleting them, but must label stale runtime values as historical or
  superseded when current `gitops/**` contracts own execution truth.
- Missing ARD/Spec/Plan/Task documents for a draft PRD should be recorded as
  downstream gaps, not linked as nonexistent Markdown targets.
- PRD success criteria should pair user/operator capability with evidence, not
  only list Kubernetes object states.

#### Evidence

- `git diff --check` PASS.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- Direct mutation / secret-literal scan over `docs/01.requirements` PASS.
- Dashboard supersession scan for the platform expansion PRD PASS.

#### Handoff

- Rollouts and Notifications ARD/Spec/Plan/Task documents remain follow-up
  gaps and were not created in this PRD-focused pass.
- No live cluster mutation, ArgoCD action, Vault write, Slack action, manifest
  change, or plaintext secret change was performed.

---

### 2026-05-17 — 90.references template hardening

- **Date**: 2026-05-17
- **Layer**: docs, meta
- **Status**: complete
- **Tags**: #docs #references #templates #validation

#### Progress

- Added template-aligned frontmatter to the two authored reference documents
  that were missing it:
  `docs/90.references/learning/infrastructure-to-theory-roadmap.md` and
  `docs/90.references/versions/tech-stack-version-inventory.md`.
- Strengthened their `## Related Documents` sections with the owning category
  README or reference maintenance runbook links.
- Added target-relative link-basis guidance to fixed-target Markdown templates
  under `docs/99.templates/`.
- Added variable-target guidance to `readme.template.md`, `memory.template.md`,
  and `progress.template.md` without inventing fixed target paths.
- Added syntax-safe owner comments to OpenAPI, GraphQL, and proto contract
  templates.

#### Memory

- `docs/90.references/llm-wiki/wiki-index.md` remains generated-only and was
  not edited by hand.
- Reference frontmatter alignment is treated as a template conformance
  improvement, not as a new hard validator rule.
- Template placeholder and code-literal cross-links should be calculated from
  the final authored Target location; actual Markdown links inside template
  files still must resolve from `docs/99.templates/`.

#### Evidence

- Targeted template target-relative guidance check: PASS.
- `git diff --check` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.

#### Handoff

- No live cluster mutation, secret read/write, deployment approval, direct
  ArgoCD action, generated LLM Wiki manual edit, or external version refresh was
  performed.

---

### 2026-05-17 — 90.references operations maintenance runbook

- **Date**: 2026-05-17
- **Layer**: docs, ops, meta
- **Status**: complete
- **Tags**: #docs #references #operations #templates #validation

#### Progress

- Created one operations runbook for `docs/90.references` maintenance:
  `docs/05.operations/runbooks/0011-reference-maintenance-runbook.md`.
- Updated `docs/05.operations` and `docs/05.operations/runbooks` README
  discoverability for the new runbook.
- Standardized the touched `docs/90.references/**/README.md` and
  `docs/99.templates/README.md` related-link heading to
  `## Related Documents`.
- Added target-relative reference maintenance links to
  `docs/99.templates/reference.template.md` and a touched-scope validation check
  in `scripts/validate-repo-quality-gates.sh`.

#### Memory

- Local `main` was clean but ahead of `origin/main` by 1 commit before this work;
  implementation was done on `codex/90-references-operations-maintenance`.
- `docs/90.references` remains the SSoT for reference facts and version values.
  The new runbook owns only the repeated maintenance checklist.
- `scripts/generate-llm-wiki-index.sh` and
  `docs/90.references/llm-wiki/wiki-index.md` were not edited by hand.
- No frontmatter date fallback list was needed; the new runbook uses the
  plan-approved date `2026-05-17`.

#### Evidence

- Targeted touched README heading check: PASS.
- Targeted new runbook frontmatter/section/scenario check: PASS.
- Targeted `reference.template.md` target-relative link check: PASS.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `git diff --check` PASS.

#### Handoff

- No live cluster mutation, Vault write, deployment approval, secret change, or
  direct ArgoCD action was performed.

---

### 2026-05-17 — 05.operations metadata and template alignment

- **Date**: 2026-05-17
- **Layer**: docs, ops, meta
- **Status**: complete
- **Tags**: #docs #operations #templates #validation

#### Progress

- Standardized the related-link heading to `## Related Documents` for the root
  README, docs README, `docs/05.operations/README.md`, and the four
  `docs/05.operations/*/README.md` entrypoints.
- Added template-aligned frontmatter to 26 authored operations documents:
  9 guides, 7 operations policies, and 10 runbooks.
- Updated the README quality gate to accept legacy README headings outside the
  touched scope while requiring the canonical heading in the root/docs/operations
  entrypoints.
- Aligned directly affected templates in `docs/99.templates/` with the canonical
  README heading and numeric operations policy/runbook naming placeholders.

#### Memory

- `## Related Documents` is the canonical related-link heading for root/docs and
  `docs/05.operations` README entrypoints; older `## Related References` headings
  remain temporarily allowed only outside this touched scope.
- Operations policy documents keep `type: operation` to match
  `operation.template.md` and the stage authoring matrix.
- Frontmatter `updated` values for the 26 operations documents came from the
  owning README document index. No fallback date was used.

#### Evidence

- Targeted README heading check for root/docs/operations entrypoints: PASS.
- Targeted frontmatter shape check for 26 operations documents: PASS.
- Targeted policy `type: operation` check: PASS.
- Targeted frontmatter updated-date check against README index dates: PASS.
- Targeted template placeholder check: PASS.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `git diff --check` PASS.

#### Handoff

- No live cluster mutation, secret change, deployment, or direct ArgoCD action
  was performed.

---

### 2026-05-17 — template cross-link completion

- **Date**: 2026-05-17
- **Layer**: docs, meta
- **Status**: complete
- **Tags**: #docs #templates #cross-links #validation

#### Progress

- Completed the remaining target-relative placeholders in `incident.template.md`,
  `postmortem.template.md`, `operation.template.md`, and `reference.template.md`.
- Aligned generated `docs/**` Markdown code-link labels with their actual
  relative hrefs so rendered paths match the file location that owns the link.
- Aligned root, docs stage, and examples README code-link labels with their
  actual relative hrefs.
- Refreshed the execution plan index and completion state for the template
  cross-link pass.

#### Memory

- Template placeholder links shown as code literals are authored from the
  template `Target` location, not from `docs/99.templates/`.
- Actual Markdown links inside template files still resolve relative to the
  template file location, per the template link policy.
- For `docs/05.operations/incidents/YYYY/`, links to runbooks and policies
  resolve through `../../runbooks/` and `../../policies/`; postmortem links
  resolve through `../postmortems/YYYY/`.
- For `docs/05.operations/incidents/postmortems/YYYY/`, links back to incident
  records resolve through `../../YYYY/`, and runbooks/policies through
  `../../../`.

#### Evidence

- Fenced-code-aware Markdown link scanner over `README.md`, `docs/**/*.md`, and
  `examples/**/README.md`: missing target 0, code-label/href mismatch 0.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `git diff --check` PASS.

#### Handoff

- No live cluster mutation, secret change, deployment, or direct ArgoCD action
  was performed.

---

### 2026-05-17 — scripts cleanup retention evidence refresh

- **Date**: 2026-05-17
- **Layer**: qa, docs, meta
- **Status**: complete
- **Tags**: #scripts #quality-gates #governance #docs

#### Progress

- Refreshed `scripts/README.md` in-place to separate Tier A/B retention evidence
  from Tier C command/documentation surfaces.
- Narrowed the missing `scripts/<name>.sh` reference check in
  `scripts/validate-repo-quality-gates.sh` to an explicit active command-contract
  allowlist instead of broad docs/runtime tree globs.
- Added 2026-05-17 evidence refresh sections to the scripts remediation plan and
  task records while preserving the 2026-05-09 four-script historical snapshot.

#### Memory

- Current script inventory is maintained in `scripts/README.md`; historical
  four-script references in the 2026-05-09 remediation docs are snapshot context,
  not current inventory.
- Retention evidence now has three tiers: Tier A direct CI/post-edit execution,
  Tier B indirect required quality-gate dependency with generated artifact/check
  ownership, and Tier C command/documentation/allowlist references that do not
  prove retention by themselves.
- `scripts/generate-llm-wiki-index.sh` is a Tier B indirect quality-gate
  dependency because `scripts/validate-repo-quality-gates.sh` runs its `--check`
  mode and it owns the generated LLM Wiki index contract.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash -n scripts/*.sh .claude/hooks/*.sh infrastructure/tests/*.sh infrastructure/*.sh` PASS.
- `find scripts .claude/hooks infrastructure -type f -name '*.sh' -exec bash -n {} \;` PASS.
- `git diff --check` PASS.
- Controller final validation is expected after review.

#### Handoff

- Review the scripts cleanup diff and rerun the final controller checks. No live
  cluster mutation, commit, script deletion, rename, or merge was part of this
  work.

---

### 2026-05-16 — Cycle 2 implementation: local toolchain setup documentation

- **Date**: 2026-05-16
- **Layer**: docs, operations
- **Status**: complete
- **Tags**: #docs #toolchain #dx #wsl2

#### Progress

- Extended `docs/05.operations/guides/0002-wsl2-k3d-argocd-ha-setup-guide.md` in-place with
  a local toolchain prerequisites section covering: shellcheck, actionlint, zizmor, pre-commit,
  kube-linter (required tools); graphify, rtk (optional); WSL2 non-interactive shell PATH
  configuration via `~/.profile` or `/etc/environment`; and local verification commands.
  Inserted before "Step-by-step Instructions", after existing Prerequisites subsections.

#### Memory

- WSL2 non-interactive shells do not source `.bashrc`/`.zshrc`, so `~/.local/bin` and
  `~/.go/bin` are absent from PATH. Fix: add `export PATH="$HOME/.local/bin:$(go env GOPATH)/bin:$PATH"`
  to `~/.profile` or set PATH in `/etc/environment` for system-wide effect.
- CI uses `pre-commit/action@v3.0.1` which auto-installs all hook dependencies at runtime;
  CI coverage is complete. Local PATH inconsistency is a DX concern only, not a CI gap.
- Cycle 2 Batch 2 (harness-catalog.md and agentic.md lifecycle hook boundary documentation):
  Already implemented in Cycle 1/PR #35. harness-catalog.md Stop/SubagentStop/PreCompact rows
  already show Partial status with policy-driven remediation notes. agentic.md lines 21 and 49
  already document the policy-only completion/compaction safeguard boundary.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS
- `bash scripts/generate-llm-wiki-index.sh --check` PASS
- `bash infrastructure/tests/verify-contracts-static.sh` PASS
- `bash scripts/validate-gitops-structure.sh` exit 0, all 11 directories PASS
- `bash scripts/validate-k8s-manifests.sh .` No lint errors found
- `bash scripts/check-secret-handling.sh .` PASS
- `bash -n scripts/*.sh .claude/hooks/*.sh infrastructure/tests/*.sh infrastructure/*.sh` PASS
- Changed file: `docs/05.operations/guides/0002-wsl2-k3d-argocd-ha-setup-guide.md` (+60 lines)
- Skipped: cluster bootstrap (BLOCKED, requires human approval); per-service README files
  (DEFERRED, no human request); Batch 3 aggregate service docs (DEFERRED, requires human approval).

---

### 2026-05-15 — Workspace audit pipeline: housekeeping and quality-gate alignment

- **Date**: 2026-05-15
- **Layer**: meta, runtime, docs
- **Status**: complete
- **Tags**: #governance #quality-gates #versions #hooks #gitops

#### Progress

- Updated `docs/90.references/versions/tech-stack-version-inventory.md` to match actual pinned versions in `.pre-commit-config.yaml` and `.github/workflows/`: commitizen, gitleaks, markdownlint-cli2, check-jsonschema, shfmt, zizmor, actionlint (pre-commit); actions/labeler, actions/upload-artifact (github_actions). Total: 9 version entries corrected.
- Added `Validation Note` section to `infrastructure/README.md` to distinguish CI-runnable static test (`verify-contracts-static.sh`) from live-cluster-only tests.
- Added `--no-verify` prohibition rule to `docs/00.agent-governance/rules/git-workflow.md`, referencing the commitizen commit-msg hook enforcement.
- Aligned `.codex/hooks.json` PreToolUse graphify matcher from `Bash|Glob|Grep` to `Glob|Grep` to match `.claude/settings.json`.
- Removed empty `.github/gates/` directory (no files, no references, no purpose documented).
- Removed `.agents/skills/` from git tracking (`git rm -r --cached`) and added `.agents/` to `.gitignore`. Files remain on disk; duplication of `.claude/skills/` content is resolved.
- Updated `scripts/validate-repo-quality-gates.sh`:
  - Excluded `.agent-work/` from README base-section check (gitignored pipeline output directory).
  - Excluded `docs/00.agent-governance/rules/document-stage-routing.md` from stale-path scan (authoritative migration map that intentionally references legacy paths).
  - Updated Codex hook phrase check from `Bash|Glob|Grep` to `Glob|Grep` to reflect the corrected hook contract.

#### Memory

- `tech-stack-version-inventory.md` had 9 version entries drifted from actual pinned versions. Source-checked date was 2026-05-09; actual pins diverged over subsequent dependabot/pre-commit updates.
- `validate-repo-quality-gates.sh` README base-section check must exclude gitignored pipeline output directories (`.agent-work/`, analogous to existing `.agents/` and `.git/` exclusions).
- `document-stage-routing.md` is the authoritative legacy-path migration map and must be exempt from the stale-path scanner.
- When changing Codex hook matchers, update the corresponding quality-gate phrase check in the same change.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS.
- `bash scripts/check-secret-handling.sh .` PASS.
- `bash -n scripts/*.sh .claude/hooks/*.sh` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `git ls-files .agents/` returns 0 (untracked).

#### Handoff

- None.

### 2026-05-10 — Hook payload and post-edit validation hardening

- **Date**: 2026-05-10
- **Layer**: runtime
- **Status**: complete
- **Tags**: #hooks #governance #validation #gitops

#### Progress

- Hardened `.claude/hooks/k8s-pre-edit.sh` to parse Claude hook JSON stdin
  with environment-variable fallback, normalize workspace-relative paths, and
  emit structured `systemMessage` warnings for Kubernetes manifest and
  secret-adjacent edits.
- Hardened `.claude/hooks/post-validate.sh` to parse hook JSON stdin and run
  scoped validation for JSON runtime files, shell hooks/scripts, Kubernetes
  manifests, secret handling, and repo-quality surfaces.
- Wired `.codex/hooks.json` to the same SessionStart, PreToolUse, and
  PostToolUse event contract where Codex supports repo-local hooks, while
  preserving the boundary that Codex hooks are context/validation wiring rather
  than Claude-equivalent permission gates.
- Added a recursion guard for post-edit repo-quality validation so the central
  quality gate can simulate hook payloads without recursively invoking itself.
- Extended `scripts/validate-repo-quality-gates.sh` to validate hook payload
  parsing behavior, not only JSON and shell syntax.

#### Memory

- Claude hook scripts in this repo must read `tool_input` from JSON stdin and
  keep `CLAUDE_TOOL_INPUT_FILE_PATH` only as a fallback.
- When a PostToolUse hook runs `scripts/validate-repo-quality-gates.sh`, set
  `HY_HOME_K8S_SKIP_HOOK_SIMULATION=1` to avoid recursive hook simulation.
- `.codex/hooks.json` should reuse `.claude/hooks/*.sh` through `CODEX_PROJECT_DIR`
  / `CLAUDE_PROJECT_DIR` mapping instead of carrying separate hook logic.
- Manifest-edit hook validation should use a non-root-app manifest path for
  payload simulation so manifest checks run without also triggering the
  repo-quality path-filter lane.

#### Evidence

- `bash -n .claude/hooks/k8s-pre-edit.sh .claude/hooks/post-validate.sh .claude/hooks/session-start.sh scripts/validate-repo-quality-gates.sh` PASS.
- `printf '{"tool_input":{"file_path":"gitops/apps/root/kustomization.yaml"}}' | CLAUDE_PROJECT_DIR="$PWD" bash .claude/hooks/k8s-pre-edit.sh` PASS.
- `printf '{"tool_input":{"file_path":"gitops/platform/headlamp/headlamp-ingress.yaml"}}' | CLAUDE_PROJECT_DIR="$PWD" bash .claude/hooks/post-validate.sh` PASS.
- `printf '{"tool_input":{"file_path":".claude/hooks/post-validate.sh"}}' | CLAUDE_PROJECT_DIR="$PWD" bash .claude/hooks/post-validate.sh` PASS.
- `printf '{"tool_input":{"file_path":".claude/settings.json"}}' | CLAUDE_PROJECT_DIR="$PWD" bash .claude/hooks/post-validate.sh` PASS.
- Codex PreToolUse/PostToolUse payload simulation through `.codex/hooks.json` command extraction PASS.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.

#### Handoff

- None.

### 2026-05-10 — Runtime wiki-curator and generated LLM Wiki index

- **Date**: 2026-05-10
- **Layer**: docs
- **Status**: complete
- **Tags**: #governance #runtime #references #quality-gates

#### Progress

- Added `wiki-curator` as a real local worker agent under `.claude/agents/`
  with a matching `.codex/agents/` mirror and docs scope import.
- Updated the local harness catalog, runtime baseline, document routing, and
  Claude permission allowlist so LLM Wiki curation is a cataloged runtime
  surface with `sonnet` model allocation.
- Added `scripts/generate-llm-wiki-index.sh` and generated
  `docs/90.references/llm-wiki/wiki-index.md` as a Markdown-only canonical
  owner link map.
- Added `docs/05.operations/guides/0009-llm-wiki-curation-guide.md` and updated
  related README indexes for scripts, guides, docs, and references.
- Extended `scripts/validate-repo-quality-gates.sh` to check generated index
  freshness and block runtime/cache/vector/static-site artifacts under
  `docs/90.references/llm-wiki/`.

#### Memory

- `wiki-curator` is a real `.claude`/`.codex` worker agent in this repo, not
  only a documented responsibility.
- LLM Wiki remains a deterministic generated Markdown link map; policy and procedure
  changes must still go to canonical owners.
- `docs/90.references/llm-wiki/wiki-index.md` should be regenerated through
  `scripts/generate-llm-wiki-index.sh`, not edited by hand.

#### Evidence

- `bash scripts/generate-llm-wiki-index.sh` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS with optional
  `kube-linter` skipped locally because it is not installed.
- `bash scripts/check-secret-handling.sh .` PASS.
- `bash -n scripts/*.sh .claude/hooks/*.sh` PASS.
- `git diff --check` PASS.

#### Handoff

- None.

### 2026-05-10 — Examples docs and LLM WIKI reference guardrails

- **Date**: 2026-05-10
- **Layer**: docs
- **Status**: complete
- **Tags**: #examples #references #quality-gates #secret-handling

#### Progress

- Aligned AWS and Azure example documentation with the canonical in-place
  taxonomy under `01.requirements`, `02.architecture`, `03.specs`,
  `04.execution`, and `05.operations`.
- Added `docs/90.references/llm-wiki/README.md` as a repo-local,
  reference-only LLM-readable link map. It does not define policy, create a
  static wiki site, or introduce a retrieval/vector runtime.
- Extended `scripts/validate-repo-quality-gates.sh` to validate example
  Markdown links, block legacy stage references, reject file-scheme and local
  absolute paths, enforce LLM WIKI reference-only boundaries, and scan examples
  for unmarked risky command patterns.
- Updated `scripts/check-secret-handling.sh` so findings print
  `path:line kind=<kind> key=<key> value=<redacted>` instead of raw matched
  lines or secret-like values.

#### Memory

- Cloud example docs remain dated reference-only material, not live deployment
  instructions.
- LLM WIKI in this repo means a Markdown link map and ownership index only.
- Example command snippets that mention kubeconfig mutation must use an
  explicit temporary kubeconfig file marker such as `--file` or `--kubeconfig`.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS with optional
  `kube-linter` skipped locally because it is not installed.
- `bash scripts/check-secret-handling.sh .` PASS.
- `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` PASS.
- `git diff --check` PASS.
- Targeted example taxonomy and stale-reference scans returned no active drift.
- Fake plaintext-secret fixture failed as expected and printed
  `value=<redacted>` without echoing the fixture value.

#### Handoff

- None.

### 2026-05-10 — Docs taxonomy and progress memory contract

- **Date**: 2026-05-10
- **Layer**: meta
- **Status**: complete
- **Tags**: #governance #docs #memory

#### Progress

- Migrated the canonical docs taxonomy from the old stage folders to
  `01.requirements`, `02.architecture`, `03.specs`, `04.execution`, and
  `05.operations`.
- Added `docs/99.templates/progress.template.md` as the template for this
  `progress.md` ledger.
- Updated bootstrap, preflight, postflight, documentation protocol, runtime
  baseline, and memory README guidance so AI agents read and write this ledger
  during repo-changing work.

#### Memory

- `docs/00.agent-governance/memory/progress.md` is the mandatory local ledger
  for repo-changing agent progress, reusable memory, evidence, and handoff.
- Standalone memory notes may still use `docs/99.templates/memory.template.md`,
  but normal agent work should append to this file using
  `docs/99.templates/progress.template.md`.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` PASS.

#### Handoff

- None.

### 2026-05-10 — 90.references role and format contract

- **Date**: 2026-05-10
- **Layer**: docs
- **Status**: complete
- **Tags**: #docs #references #governance

#### Progress

- Audited `docs/90.references/README.md`, `docs/90.references/agents/README.md`,
  current reference documents, `docs/99.templates/reference.template.md`, and
  document routing rules.
- Clarified that `90.references` owns durable lookup facts, dated external
  snapshots, version inventories, and learning references, but not requirements,
  architecture decisions, implementation contracts, plans, policies, runbooks,
  release approval, or live mutation procedures.
- Added required `Reference Type`, `Authority Boundary`, and
  `Review and Freshness` sections to `reference.template.md` and aligned current
  reference documents to that format.

#### Memory

- `90.references` can be authoritative for factual lookup and dated snapshot
  values only when the document states its source checked date and freshness
  trigger.
- `tech-stack-version-inventory.md` remains a version-contract inventory only
  when repo manifests/config/examples are updated with it in the same change.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- Targeted stale taxonomy/reference grep returned no matches.

#### Handoff

- None.

### 2026-05-10 — 90.references learning and version inventory routing

- **Date**: 2026-05-10
- **Layer**: docs
- **Status**: complete
- **Tags**: #docs #references #versions

#### Progress

- Added `docs/90.references/learning/README.md` to define the learning
  reference scope, authoring rules, routing boundaries, and related references.
- Moved the root-level tech stack inventory into
  `docs/90.references/versions/tech-stack-version-inventory.md` because it is a
  version-contract inventory and dated external-standard snapshot.
- Added `docs/90.references/versions/README.md` and updated root/docs/examples,
  infrastructure, Traefik, and repo-quality validator references to the new
  version inventory path.

#### Memory

- Learning roadmaps and durable theory connections belong under
  `docs/90.references/learning/` and need a local README index.
- Version inventories, cloud support snapshots, and repo-backed dependency
  contract references belong under `docs/90.references/versions/`.
- `docs/90.references/README.md` should stay the routing hub, not a mixed
  document dump for every reference type.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS with optional
  `kube-linter` skipped locally because it is not installed.
- `bash scripts/check-secret-handling.sh .` PASS.
- `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` PASS.
- Targeted old root-level inventory path grep returned no matches.

#### Handoff

- None.

### 2026-05-10 — Memory template and progress ledger enforcement

- **Date**: 2026-05-10
- **Layer**: meta
- **Status**: complete
- **Tags**: #governance #memory #templates

#### Progress

- Strengthened `docs/00.agent-governance/memory/README.md` so agents must use
  `docs/99.templates/progress.template.md` for `progress.md` updates and
  `docs/99.templates/memory.template.md` for standalone memory files.
- Updated bootstrap, documentation protocol, preflight, postflight, and the
  local runtime baseline so repo-changing agent work plans and records
  `memory/progress.md` updates.
- Added repo-quality gate checks for the memory template inventory, standalone
  memory file template headings, and progress-ledger coupling.

#### Memory

- `docs/00.agent-governance/memory/progress.md` is the mandatory progress
  ledger for repo-changing agent work.
- Standalone files under `docs/00.agent-governance/memory/` must use
  `docs/99.templates/memory.template.md` and include a `Related Progress`
  section.
- Standalone memory file changes must be accompanied by a related
  `progress.md` entry in the same change.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.

#### Handoff

- None.

### 2026-05-16 — Prompt-kit implementation executor pass

- **Date**: 2026-05-16
- **Layer**: meta, infra, qa, docs
- **Status**: complete
- **Tags**: #prompt-kit #gitops #ci #governance #docs

#### Progress

- Executed the approved file-by-file plan from `.agent-work/report/08_integrated_implementation_planner.md`.
- Added omitted NetworkPolicy resources to the active Kustomize entrypoint for `gitops/platform/network-policies/`.
- Extended `scripts/validate-gitops-structure.sh` to detect sibling GitOps YAML manifests that are not listed in their local `kustomization.yaml`.
- Aligned branch, PR, and QA governance for `test/`, WIP/draft PRs, every-PR/no-exceptions language, and coverage applicability.
- Documented hook lifecycle coverage as policy/report-driven for Stop, SubagentStop, and PreCompact safeguards instead of adding runtime hooks.
- Consolidated `docs/99.templates/README.md` and added aggregate service coverage matrices to existing GitOps and infrastructure READMEs.

#### Memory

- Kustomize resource completeness is now part of the GitOps static validation path.
- Current completion and compaction safeguards remain report, handoff, memory/progress, and postflight-checklist responsibilities unless a future approved plan adds lifecycle hooks.
- Current infrastructure coverage uses a validation matrix; future testable application code should target 90% line and branch coverage where applicable.

#### Evidence

- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-repo-quality-gates.sh .` PASS before memory entry.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS, including resource completeness checks.
- `bash scripts/validate-k8s-manifests.sh .` PASS with optional `kube-linter` skipped locally because it is not installed.
- `bash scripts/check-secret-handling.sh .` PASS.
- `bash -n scripts/*.sh .claude/hooks/*.sh infrastructure/tests/*.sh infrastructure/*.sh` PASS.
- `git diff --check` PASS.

#### Handoff

- Write `.agent-work/report/09_implementation_executor_agent.md`.
- Hand off to `.agent-work/prompts/10_verification_completion_reporter_agent.md`.
- Live k3d, ArgoCD sync, external service, ingress/TLS, network policy, and secret reconciliation checks remain deferred unless a live environment is intentionally available.

### 2026-05-18 — 05.operations README routing cleanup

- **Date**: 2026-05-18
- **Layer**: docs, ops
- **Status**: complete
- **Tags**: #docs #operations #readme #validation

#### Progress

- Added a concise routing table to `docs/05.operations/README.md` so operators can choose guide, policy, runbook, or incident documents by task.
- Consolidated duplicate purpose, related-folder, template, example, and SSoT sections in the guides, policies, runbooks, and incidents README entrypoints.
- Reframed `docs/05.operations/policies/README.md` around controls and exception rules instead of executable command examples.
- Clarified that `docs/05.operations/incidents/` currently has no tracked incident or postmortem documents and should create dated subfolders only when a real record is needed.
- Did not create new operations documents, move files, or rewrite individual guide/policy/runbook bodies.

#### Memory

- `docs/05.operations/*/README.md` should act as operator routing and index entrypoints; detailed commands belong in runbooks, policy controls in policies, and background/onboarding material in guides.
- Keep empty incident state explicit in `docs/05.operations/incidents/README.md`; do not add placeholder incident or postmortem files.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/check-secret-handling.sh .` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS with optional `kube-linter` skipped locally because it is not installed.
- `bash scripts/validate-gitops-structure.sh` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- `git diff --check` PASS.

#### Handoff

- None.

## Historical Entries

### Harness Implementation Progress

- **Date**: 2026-04-13
- **Layer**: meta
- **Tags**: #governance #harness #settings
- **Record type**: historical initial implementation snapshot.

Current runtime truth is maintained in `docs/00.agent-governance/harness-catalog.md`.
Current script inventory is maintained in `scripts/README.md`. This memory entry
preserves the initial remediation history and must not be treated as the current
runtime or script roster when those files disagree.

### Problem

Harness layers L1–L6 were incomplete: no `settings.json`, no agent files, no hooks, no k8s scripts, scopes lacked §File Ownership, and no subagent protocol existed.

### Context

- Affected paths: `.claude/`, `scripts/`, `docs/00.agent-governance/scopes/`, `AGENTS.md`, `CLAUDE.md`
- Environment: k3d local cluster, WSL2, ArgoCD GitOps
- Preconditions: Only `settings.local.json` and empty `.claude/` subdirectories existed.

### Resolution

**P0 (complete):**

- `AGENTS.md` restructured to §1–§8 with Agent Catalog, Settings, Role Separation.
- `CLAUDE.md` and `GEMINI.md` updated to ≤30/25 lines gateway overlays.
- `documentation-protocol.md` updated with §Docs 3 Rules (HALT).
- `bootstrap.md` updated with in-place refactor rule.
- `postflight-checklist.md` updated with §6 Docs 3 Rules Compliance.

**P1 (complete):**

- All `scopes/*.md` updated with §File Ownership and §Subagent Bridge.
- `providers/agents-md.md` created.
- `subagent-protocol.md` created.
- `memory/progress.md` created (this file).

**P2 (complete):**

- `.claude/settings.json` — created; git-tracked with allow/deny permission lists and 3 hooks (SessionStart, PreToolUse, PostToolUse).
- `.claude/hooks/` — 3 scripts created: `session-start.sh`, `k8s-pre-edit.sh`, `post-validate.sh`.
- `.claude/agents/` — 7 agent files created: `supervisor.md`, `k8s-implementer.md`, `gitops-reviewer.md`, `security-auditor.md`, `incident-responder.md`, `code-reviewer.md`, `doc-writer.md`.
- `scripts/` — 3 validation scripts created: `validate-k8s-manifests.sh`, `validate-gitops-structure.sh`, `check-secret-handling.sh`.
  Current script inventory is maintained in `scripts/README.md`; this memory entry records the initial harness implementation state.

**P4 (complete, 2026-04-13):**

- Legacy harness examples were migrated into workspace-specific skills under `.claude/skills/`:
  - `deployment-strategies` — k8s/ArgoCD deployment strategy catalog (cicd-pipeline lineage)
  - `incident-postmortem` — cluster incident post-analysis pipeline (incident-postmortem lineage)
  - `rca-methodology` — 5 Whys / Fishbone / FTA / Change Analysis reference (incident-postmortem lineage)
  - `k8s-security-audit` — structured RBAC/NetworkPolicy/Secret/container/supply-chain audit workflow (security-audit lineage)
  - `vulnerability-patterns` — k8s manifest and Helm chart misconfiguration catalog with CIS 5.x mappings (security-audit, code-reviewer lineage)
- `docs/00.agent-governance/harness-catalog.md` Skills table updated from 3 to 8 entries.
- Legacy source example directory removed after migration.

**P3 (complete):**

- Local harness catalog authored under `docs/00.agent-governance/`.
- Model policy standardized: agents use sonnet; supervisor uses opus.
- Legacy source-directory references removed from gateway and protocol files.

### Prevention

- Run `postflight-checklist.md §6 Docs 3 Rules` before every PR.
- `settings.json` must be git-tracked; `settings.local.json` must stay `.gitignore`d.
- Runtime catalog entries in `docs/00.agent-governance/harness-catalog.md` must
  stay in sync with `.claude/agents/`, `.codex/agents/`, `.claude/skills/`,
  and the hook boundary between `.claude/settings.json` and `.codex/hooks.json`.
