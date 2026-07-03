# Agent Progress and Memory Ledger

This file is the repo-local progress and reusable memory ledger for AI agent
work in `hy-home.k8s`. Use `docs/99.templates/templates/common/progress.template.md` for new
entries. Memory here supports future task intake, but current runtime truth
stays in `docs/00.agent-governance/harness-catalog.md` and current script
inventory stays in `scripts/README.md`.

## Work Entries

### 2026-07-04 — Workspace document governance hardening Task 5 final validation

- **Date**: 2026-07-04
- **Layer**: docs, qa, governance
- **Status**: complete
- **Tags**: #docs #governance #validation #ci-qa

#### Progress

- Completed T-005 for the workspace document governance hardening plan and
  updated the
  [Plan](../../04.execution/plans/2026-07-03-workspace-document-governance-hardening.md)
  and
  [Task evidence](../../04.execution/tasks/2026-07-03-workspace-document-governance-hardening.md).
- Hardened `scripts/validate-repo-quality-gates.sh` with deterministic,
  path-scoped checks for active README deprecated headings, active authored
  template residue, active template-routing owner drift, shared hook path
  drift, and CI/QA source-basis documentation.
- Reconciled `.github/ABOUT.md` and the CI/CD QA guide so external
  GitHub/tooling claims route back to the parent Spec's official-source basis.
- Marked the Stage 04 Plan and Task indexes as done for this workstream.

#### Memory

- Active route-selection guidance should point exact target/template decisions
  to `docs/99.templates/support/template-routing.md`; the Templates README is
  an inventory summary.
- Historical evidence paths such as the progress ledger, Stage 90 audit
  reports, and archive Tombstones should not be used as broad currentness
  denylist targets.
- `ci.yml` is the required QA gate. `generate-changelog.yml` is release
  evidence automation, while `labeler.yml`, `greetings.yml`, and `stale.yml`
  are maintenance automations.

#### Evidence

- `git diff --check` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash scripts/validate-harness.sh` — PASS.
- Harness limitations: optional `kube-linter` was not installed and manifest
  validation used YAML syntax checks; optional `conftest` was not installed
  and policy validation used the built-in fallback. Both fallback paths passed.
- RTK limitation repeated: `rtk` is not on PATH; `/home/hy/.local/bin/rtk
  --version` works, but `/home/hy/.local/bin/rtk gain` cannot initialize its
  tracking database, so required validation commands were run directly.

#### Handoff

- Task 5 implementation is complete and ready for the parent-dispatched final
  independent review.
- No live Kubernetes, Argo CD, Vault, cloud, publishing, provider-runtime,
  push, merge, or secret-value action was performed.

### 2026-07-03 — Workspace document governance hardening Task 4 document cleanup

- **Date**: 2026-07-03
- **Layer**: docs, meta, governance, qa
- **Status**: complete
- **Tags**: #docs #governance #readme #validation

#### Progress

- Completed T-004 for the workspace document governance hardening plan and
  updated the
  [Task evidence](../../04.execution/tasks/2026-07-03-workspace-document-governance-hardening.md).
- Cleaned active README/profile drift in the governance hub, AWS example docs
  README, tests README, root README, and docs hub.
- Updated active onboarding guidance in provider doc-writer surfaces, shared
  output style, provider hook custom instructions, and the Stage 00 pre-edit
  advisory so exact template route selection points to
  `docs/99.templates/support/template-routing.md`.
- Kept the Templates README as an inventory summary and removed duplicated
  route-list prose from provider custom instructions.

#### Memory

- README files should keep `## Related Documents`; folder inventories belong
  in `## Structure` or other topic-specific sections, not as deprecated
  related-document heading families.
- Tests and onboarding guidance should reference shared hook scripts under
  `docs/00.agent-governance/hooks`, not provider-local hook directories.
- Exact target-pattern/template selection belongs in
  `docs/99.templates/support/template-routing.md`; `docs/99.templates/README.md`
  remains the synchronized inventory summary.

#### Evidence

- Focused README heading scan — PASS, no deprecated related-heading matches.
- Focused README frontmatter scan — PASS, no README frontmatter matches.
- Changed-surface residue scan — PASS, no stale hook, body delimiter, legacy
  heading, or old template-routing owner matches.
- JSON syntax check for `.agents/hooks.json`, `.claude/settings.json`, and
  `.codex/hooks.json` — PASS.
- `bash -n docs/00.agent-governance/hooks/k8s-pre-edit.sh` — PASS.
- `git diff --check` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- RTK limitation repeated: `rtk` is not on PATH; direct local binary version
  check works, but `rtk gain` cannot initialize its tracking database, so
  required validation commands were run directly.

#### Handoff

- T-004 is complete. Continue with T-005 final reconciliation and any final
  deterministic validator decisions.
- No live Kubernetes, Argo CD, Vault, cloud, publishing, provider-runtime, or
  secret-value action was performed.

### 2026-07-03 — Workspace document governance hardening Task 3 provider entrypoints

- **Date**: 2026-07-03
- **Layer**: docs, meta, governance, qa
- **Status**: complete
- **Tags**: #docs #governance #providers #validation

#### Progress

- Completed T-003 for the workspace document governance hardening plan and
  updated the
  [Task evidence](../../04.execution/tasks/2026-07-03-workspace-document-governance-hardening.md).
- Kept root `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` thin while aligning their
  provider roles: Codex/GPT starts from `AGENTS.md`, Claude starts from
  `CLAUDE.md`, and Gemini starts from `GEMINI.md`.
- Updated Claude and Gemini provider-native agent bootstrap lines to match
  their root shims, while Codex TOML mirrors continue to load `AGENTS.md`.
- Aligned shared `.agents` skills, rules, and workflows with the Stage 00
  canonical adapter model and routed exact document-template mapping to
  `docs/99.templates/support/template-routing.md`.
- Review remediation tightened `.agents/GEMINI.md`, `.codex/CODEX.md`, and
  `docs/00.agent-governance/rules/document-stage-routing.md` so active
  provider/runtime guidance names
  `docs/99.templates/support/template-routing.md` for route selection.

#### Memory

- `.agents/{skills,workflows,output-styles}` is the shared asset SSoT;
  `.claude/{skills,workflows,output-styles}` and
  `.codex/{skills,workflows,output-styles}` expose symlink views, while
  provider-native files remain real adapter/runtime surfaces.
- `.claude/settings.json` is the native Claude permission and hook surface.
  `.codex/hooks.json` and `.agents/hooks.json` are context/validation wiring,
  not Claude-style permission gates.
- Root provider shims should stay as routing files. Durable rules belong in
  Stage 00 governance, template support contracts, or shared `.agents` assets.

#### Evidence

- Required provider/hook and template-residue scans completed. Active hook
  matches were expected provider wiring and shared hook references; the only
  template-residue match was an ignored `.claude/*.local.md` advisory file.
- `DESIGN.md` is absent in this checkout; scans were rerun against the existing
  requested surfaces.
- RTK limitation repeated: `rtk` is not on PATH; direct local binary version
  check works, but `rtk gain` cannot initialize its tracking database, so
  required exact validation commands were run directly.
- `git diff --check` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash scripts/validate-harness.sh` — PASS; optional `kube-linter` and
  `conftest` were unavailable and covered by harness fallbacks.
- Review remediation focused scans — PASS: cited provider/runtime route
  guidance points to `docs/99.templates/support/template-routing.md`, and the
  false broad provider-directory symlink claim is removed.

#### Handoff

- T-003 is complete. Continue with T-004 workspace README/authored-document
  application and T-005 final reconciliation.
- No live Kubernetes, Argo CD, Vault, cloud, publishing, provider-runtime, or
  secret-value action was performed.

### 2026-07-03 — Workspace document governance hardening Task 2 core contracts

- **Date**: 2026-07-03
- **Layer**: docs, governance, templates, qa
- **Status**: complete
- **Tags**: #docs #governance #templates #validation

#### Progress

- Completed T-002 for the workspace document governance hardening plan and
  updated the
  [Task evidence](../../04.execution/tasks/2026-07-03-workspace-document-governance-hardening.md).
- Kept exact target-pattern/template routing in
  `docs/99.templates/support/template-routing.md`, with the Templates README as
  a synchronized route inventory.
- Removed the optional feature-local README row as a second structural mapping;
  nested README files now rely on the generic README route only.
- Updated Stage 00 routing, protocol, and authoring matrix docs to reference
  the support route contract instead of carrying a full duplicate map.
- Added deterministic route parity coverage to
  `scripts/validate-repo-quality-gates.sh` so the Templates README route table,
  support Current Route Map, and structural validator coverage drift together
  fail closed.

#### Memory

- `harness-task-contract.template.md` remains a supplemental task starter and
  must not become a second structural route for
  `docs/04.execution/tasks/*.md`.
- Feature-local README files under `docs/03.specs/<feature-id>/` are README
  entrypoints, not a separate structural template family.
- Active core-contract surfaces should avoid carrying exact legacy residue
  literals as prose; use current contract wording and let the validator own
  deterministic denylist enforcement.

#### Evidence

- Route/profile scans completed for Template-Folder Mapping, Current Route Map,
  frontmatter profiles, template expected types, and validator mappings.
- Focused flat template route scan — PASS, no matches.
- Focused support migration-wording scan — PASS, no matches.
- Focused residue scan returned only template starter markers, historical
  completed Plan/Task/progress evidence, and one active authored runbook
  negative-checklist phrase routed to T-004/T-005.
- `git diff --check` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.

#### Handoff

- T-002 is complete. Continue with T-003 provider entrypoint hardening, then
  T-004/T-005 cleanup and final reconciliation.
- No live Kubernetes, Argo CD, Vault, cloud, publishing, provider-runtime, or
  secret-value action was performed.

### 2026-07-03 — Workspace document governance hardening Task 1 audit inventory

- **Date**: 2026-07-03
- **Layer**: docs, meta, qa
- **Status**: complete
- **Tags**: #docs #governance #audit #validation

#### Progress

- Completed Task 1 for the workspace document governance hardening plan:
  baseline status, tracked file inventory, frontmatter/README scans, provider
  scans, and CI/QA scans are recorded in the
  [Task evidence](../../04.execution/tasks/2026-07-03-workspace-document-governance-hardening.md).
- Created the Stage 90
  [workspace document governance hardening audit](../../90.references/audits/2026-07-03-workspace-document-governance-hardening-audit.md)
  because durable findings were found and should route to later tasks instead
  of being fixed during the audit-only pass.
- Registered the audit report in the Stage 90 audits README.

#### Memory

- Current Task 1 drift classes are README heading drift, README body delimiter
  evidence that is not frontmatter, and active CI/QA shell syntax drift around
  the legacy Claude provider-local hook directory versus
  `docs/00.agent-governance/hooks`.
- Provider and CI/QA claims should keep routing through root shims, Stage 00
  provider notes, runtime overlays, `.github/ABOUT.md`,
  `.github/workflows/ci.yml`, `scripts/README.md`, `tests/README.md`, and the
  CI/CD QA guide.

#### Evidence

- `git status --short --branch` — PASS, on
  `codex/template-governance-audit-enhancement`.
- `git diff --check` — PASS, no output.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- Inventory count: 480 tracked Markdown/YAML/YML/GraphQL/proto files and 358
  tracked Markdown files.
- Required frontmatter, README heading, provider, and CI/QA scans completed and
  summarized in the Task record.

#### Handoff

- T-001 is complete. Continue with T-002/T-005 routing from the audit report;
  no live cluster, Argo CD, Vault, cloud, provider runtime, or secret checks
  were requested or run.

### 2026-07-03 — Workspace document governance hardening design

- **Date**: 2026-07-03
- **Layer**: docs, governance, qa, meta
- **Status**: in-progress
- **Tags**: #docs #governance #templates #providers #validation

#### Progress

- Created the Stage 03
  [workspace document governance hardening spec](../../03.specs/013-workspace-document-governance-hardening/spec.md)
  for the approved staged scope that combines audit inventory, core template
  contract hardening, provider entrypoint hardening, workspace-wide application,
  and final validation.
- Registered the new Spec in the Stage 03 README index.
- Preserved the existing docs taxonomy by routing the design into
  `docs/03.specs/` instead of adding the Superpowers default
  `docs/superpowers/` top-level folder, which the repository quality gate
  rejects.
- Created the Stage 04
  [implementation plan](../../04.execution/plans/2026-07-03-workspace-document-governance-hardening.md)
  and
  [task record](../../04.execution/tasks/2026-07-03-workspace-document-governance-hardening.md)
  after user approval of the Stage 03 Spec.
- Registered the new Plan and Task in the Stage 04 README indexes.

#### Memory

- Workspace-wide document hardening should proceed audit-first, then core
  contracts, then provider entrypoints, then broad authored-document
  application.
- The Stage 04 Plan decomposes execution into audit inventory, core contract
  hardening, provider entrypoint hardening, workspace application, and final
  validation.

#### Evidence

- `git diff --check` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- Spec self-review placeholder scan — PASS, no incomplete markers.
- Plan self-review links the approved Spec to executable Stage 04 Plan/Task
  records.

#### Handoff

- Await user choice of subagent-driven or inline plan execution.

### 2026-07-03 — Template governance audit enhancement plan

- **Date**: 2026-07-03
- **Layer**: docs, meta, qa
- **Status**: complete
- **Tags**: #templates #governance #audit #validation

#### Progress

- Created the Stage 04
  [implementation plan](../../04.execution/plans/2026-07-03-template-governance-audit-enhancement.md)
  and
  [task record](../../04.execution/tasks/2026-07-03-template-governance-audit-enhancement.md)
  for the approved follow-up audit and targeted enhancement pass over
  `docs/99.templates/**`.
- Registered the new Plan and Task in the Stage 04 README indexes.
- Seeded the task finding ledger with current support-contract and validator
  improvement candidates: migration-phase wording, harness task route
  ambiguity, deterministic validator guardrail, and authored-doc audit
  evidence.
- Added repository quality gate guardrails for stale support-doc wording and
  harness starter overlap in the structural route map.
- Completed T-006 final validation and synchronized the Plan, Task, Stage 04
  README indexes, and this progress entry to complete.
- Recorded final scan evidence showing the categorized template tree remains
  intact, active contracts contain no flat template routes, and support docs
  contain no stale migration-phase wording.
- Recorded final-review remediation: the Spec now links to the dated Stage 04
  Plan and Task, and the support stale-wording validator includes the support
  README while preserving its frontmatter exemption.

#### Memory

- `harness-task-contract.template.md` should remain a supplemental starter for
  high-risk Stage 04 Task records, not a second structural route that competes
  with `task.template.md`.
- Active support contracts should describe the current steady-state template
  model; completed migration phase wording belongs in completed plan/task
  evidence, not current support rules.

#### Evidence

- `git diff --check` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- Task 4 focused support drift scan — PASS, no stale support-doc wording.
- Task 4 harness route overlap scan — PASS, no structural route overlap.
- RTK limitation observed: `which rtk` did not find `rtk`; direct
  `/home/hy/.local/bin/rtk --version` reported `rtk 0.34.3`; direct
  `/home/hy/.local/bin/rtk gain` could not initialize its tracking database,
  so required exact validation commands were run directly.
- Task 6 final `git diff --check` — PASS, no output.
- Task 6 final `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- Task 6 final template tree scan — PASS, files remain under
  `docs/99.templates/README.md`, `support/**`, and `templates/**`.
- Task 6 final flat template route scan — PASS, no matches and no
  self-referential evidence exceptions.
- Task 6 final support stale wording scan — PASS, no matches.
- Final-review remediation: Spec Plan/Task placeholders were replaced with
  dated Stage 04 links.
- Final-review remediation: stale support wording checks include
  `docs/99.templates/support/README.md`; README frontmatter exemption remains.
- Final-review polish: the completed Plan's procedural checklist now matches
  the completed Task evidence and checked completion criteria.
- Final-review polish: the completed Plan's validator snippet now mirrors
  support README stale-wording coverage while preserving README's frontmatter
  exemption.

#### Handoff

- None. The template governance audit enhancement is complete in local
  execution records.

### 2026-07-03 — Template governance migration final sync

- **Date**: 2026-07-03
- **Layer**: docs, meta, qa
- **Status**: complete
- **Tags**: #templates #sdlc #governance #validation

#### Progress

- Reviewed active template support docs, Stage 00 documentation rules, the
  migration spec, the migration plan, and the migration task for post-migration
  wording that still described Phase 3 as future work.
- Updated authored migration records so the plan and task now reflect completed
  support contracts, categorized template routes, frontmatter profile
  enforcement, authored-doc application, and final validation.
- Confirmed authored docs no longer contain active flat template paths, old
  legacy literals, simple frontmatter type values, quoted platform owners, or
  generator-only frontmatter keys.
- Marked T-006 and T-007 in the migration task record as complete.

#### Memory

- `docs/99.templates/support/frontmatter-schema.md` is now the canonical
  profile source for Markdown frontmatter.
- `scripts/validate-repo-quality-gates.sh` enforces the active template
  routing, README frontmatter absence, frontmatter profile, and legacy literal
  denylist contracts.
- `docs/99.templates/templates/**` contains copy-ready forms only; contract,
  governance, routing, schema, and cleanup rules stay under
  `docs/99.templates/support/**`.

#### Evidence

- `git diff --check` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- Active legacy literal scan across docs, scripts, `.codex`, `AGENTS.md`, and
  `RTK.md` returned no matches.
- Active flat template path scan across README, docs, scripts, `.codex`,
  `.agents`, `.github`, and examples returned no matches.
- Authored-doc template residue scan returned only template/support-owned
  matches under `docs/99.templates/**`.

#### Handoff

- None. The approved template contract and governance migration is complete in
  local commits.

### 2026-07-03 — Template frontmatter profile normalization

- **Date**: 2026-07-03
- **Layer**: docs, meta, qa
- **Status**: complete
- **Tags**: #templates #frontmatter #governance #validation

#### Progress

- Migrated active Markdown frontmatter `type` values from simple document
  roles to namespaced profile values such as `sdlc/spec`,
  `sdlc/policy`, `content/reference`, `content/archive-tombstone`,
  `governance/reference`, and `governance/template-support`.
- Normalized quoted platform owner values to `owner: platform`.
- Removed YAML frontmatter from template README files and added the
  `governance/memory` frontmatter profile to the standalone memory template.
- Updated the LLM wiki generator so the generated index uses the canonical
  `content/reference` profile without generator-only frontmatter keys.
- Extended `scripts/validate-repo-quality-gates.sh` to enforce frontmatter
  keys, namespaced `type` values, README frontmatter absence, archive
  Tombstone status, support-doc profiles, Stage 00 governance profiles, and
  the legacy literal denylist.
- Marked T-005 in the migration task record as complete.

#### Memory

- README files remain frontmatter-free; README traceability belongs in
  `Related Documents`.
- Generated Markdown outputs must be regenerated from their scripts after
  frontmatter schema changes, otherwise freshness checks will revert the old
  schema.
- Frontmatter validation now treats `docs/99.templates/support/**` as
  governance support docs, Stage 90 references as content docs, and Stage 01
  through Stage 05 lifecycle documents as SDLC docs.

#### Evidence

- `git diff --check` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- Legacy literal scan across docs, scripts, `.codex`, `AGENTS.md`, and
  `RTK.md` returned no matches.
- Simple-type, quoted-owner, and generator-key scan across docs and scripts
  returned no active schema violations.

#### Handoff

- Next action: start Phase 4 authored docs application and final sync.

### 2026-07-03 — Template path migration

- **Date**: 2026-07-03
- **Layer**: docs, meta, qa
- **Status**: complete
- **Tags**: #templates #routing #governance #validation

#### Progress

- Moved active template forms from the flat `docs/99.templates/` root into the
  categorized `docs/99.templates/templates/**` tree using `git mv`.
- Added `docs/99.templates/templates/README.md` as the template-form index.
- Updated Stage 00 routing docs, hook hints, support contracts, README indexes,
  local skills, examples, and the repository quality gate to resolve template
  routes through the categorized template tree.
- Marked T-003 and T-004 in the migration task record as complete.

#### Memory

- `docs/99.templates/README.md` remains the public inventory and entrypoint for
  the template system.
- `docs/99.templates/templates/**` now owns reusable document forms; support
  rules, contracts, routing, and schema guidance remain under
  `docs/99.templates/support/**`.
- Generated or archived snapshots can retain historical flat-path text only
  when active repository routing and quality gates do not consume those paths.

#### Evidence

- `git mv` preserved history for moved template files.
- `find docs/99.templates -maxdepth 5 -type f -print | sort` confirmed the
  categorized template tree.
- Active legacy path scan across README, docs, scripts, `.codex`, `.agents`,
  `.github`, and examples returned no actionable flat template references.
- `git diff --check` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.

#### Handoff

- Next action: start Phase 3 frontmatter profile normalization and legacy
  cleanup.

### 2026-07-03 — Template support contract baseline

- **Date**: 2026-07-03
- **Layer**: docs, meta, qa
- **Status**: complete
- **Tags**: #templates #governance #frontmatter #sdlc #validation

#### Progress

- Added the initial `docs/99.templates/support/` contract layer for template
  documentation contract, SDLC governance, common documentation governance,
  frontmatter schema, template routing, and legacy cleanup rules.
- Updated `docs/99.templates/README.md` with the support directory inventory
  and support contract index while preserving current flat template routes for
  Phase 1 compatibility.
- Marked T-002 in the migration task record as in progress.

#### Memory

- Phase 1 must not move flat template files yet because current validators,
  hooks, and Stage 00 route docs still depend on flat template paths.
- Support docs can introduce the target contract before validators enforce it,
  as long as current route enforcement still passes.

#### Evidence

- `git diff --check` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `find docs/99.templates/support -maxdepth 1 -type f -print | sort`
  confirmed the support contract file set.

#### Handoff

- Next action: start Phase 2 template path migration.

### 2026-07-03 — Template contract and governance migration execution plan

- **Date**: 2026-07-03
- **Layer**: docs, meta, qa
- **Status**: complete
- **Tags**: #templates #governance #frontmatter #sdlc #validation

#### Progress

- Created the Stage 04
  [implementation plan](../../04.execution/plans/2026-07-03-template-contract-governance-migration.md)
  and
  [task record](../../04.execution/tasks/2026-07-03-template-contract-governance-migration.md)
  for the approved template contract and governance migration.
- Registered both execution documents in the Stage 04 plan and task README
  indexes.
- Preserved the four-phase commit boundary from the parent spec: support
  baseline, path migration, frontmatter/legacy cleanup, and authored docs
  application/final sync.

#### Memory

- Template path migration must update validator and hook routing in the same
  logical unit as `git mv` changes, because the current repository gate assumes
  flat template paths.
- Frontmatter cleanup should be split by profile or stage if authored document
  churn becomes too large for one reviewable commit.

#### Evidence

- `git diff --check` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- Korean-syllable scan for the new English-first Stage 04 plan/task returned no
  matches.

#### Handoff

- Next action: start Phase 1 support contract baseline.

### 2026-07-03 — Template contract and governance migration spec

- **Date**: 2026-07-03
- **Layer**: docs, meta, qa
- **Status**: complete
- **Tags**: #templates #governance #frontmatter #sdlc #validation

#### Progress

- Created the Stage 03
  [Template Contract and Governance Migration Spec](../../03.specs/011-template-contract-governance-migration/spec.md)
  from the approved four-phase migration design.
- Recorded the target `docs/99.templates/` model that separates template forms
  under `templates/**` from support contracts under `support/**`.
- Defined the first-pass frontmatter profile model, legacy cleanup boundaries,
  validator/hook impact surfaces, and implementation phase commit boundaries.
- Updated the Stage 03 README index so the migration spec is discoverable from
  the canonical spec stage.

#### Memory

- Large template-system changes should start with a Stage 03 migration spec
  before moving or deleting template files.
- `docs/99.templates/README.md` should remain an inventory and entrypoint;
  detailed contract, governance, schema, routing, and legacy cleanup rules
  should live in `docs/99.templates/support/**` or Stage 00 governance.
- Future migration work should preserve separate commits for support-contract
  baseline, path migration, frontmatter and legacy cleanup, and authored docs
  application.

#### Evidence

- User approved the A design: template forms under `templates/**`, support
  contracts under `support/**`, and a four-phase migration.
- External research basis was limited to official or durable documentation
  sources for frontmatter metadata, documentation type taxonomy, style
  consistency, lintable frontmatter, and machine-readable API contract shape.
- `git diff --check` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- Korean-syllable scan for the new English-first spec returned no matches.

#### Handoff

- Next action: create the implementation plan before any template file
  migration.

### 2026-07-02 — Workspace harness implementation audit pack

- **Date**: 2026-07-02
- **Completed**: 2026-07-03
- **Layer**: docs, meta, qa
- **Status**: complete
- **Tags**: #audit #harness #loop-engineering #sdlc #validation

#### Progress

- Completed the follow-up audit pack under
  [docs/90.references/audits/](../../90.references/audits/) using the completed
  [research pack](../../90.references/research/) as the benchmark model.
- Created the
  [audits README](../../90.references/audits/README.md) and four dated audit
  reports:
  [workspace governance](../../90.references/audits/2026-07-02-workspace-governance-implementation-audit.md),
  [harness/loop](../../90.references/audits/2026-07-02-harness-loop-implementation-audit.md),
  [provider harness/loop](../../90.references/audits/2026-07-02-provider-harness-loop-implementation-audit.md),
  and
  [SDLC delivery practices](../../90.references/audits/2026-07-02-sdlc-delivery-practices-implementation-audit.md).
- Finalized the parent
  [Spec](../../03.specs/010-workspace-harness-implementation-audit-pack/spec.md),
  [Plan](../../04.execution/plans/2026-07-02-workspace-harness-implementation-audit-pack.md),
  and
  [Task](../../04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md)
  traceability by setting plan/task status and Stage 04 indexes to `Done`.
- Updated the parent
  [references README](../../90.references/README.md), audits README, Stage 04
  indexes, task evidence, and this progress entry for final handoff.

#### Memory

- The approved audit output structure is four dated audit reports plus
  `docs/90.references/audits/README.md`.
- Audit reports must compare research benchmark items against repo-backed
  evidence, not upstream capability alone.
- Audit outputs may identify automation opportunities and checklist follow-up
  routes, but active policy or runtime changes belong in a future Spec, Plan,
  Task, operations policy, script, or provider adapter change.
- Implementation audit statuses use only `Implemented`, `Partial`, `Gap`, and
  `Not in scope`.
- Every `Implemented` and `Partial` status should cite repo-backed evidence.
  Upstream provider capability, external SDLC standards, or market-scan
  context do not prove local implementation without a tracked repository
  surface.
- Static repository validation, generated-index freshness, task evidence, and
  local file review are not live k3d, ArgoCD, Vault, ESO, Kubernetes, cloud,
  provider runtime, GitHub CI run, paid-job, deployment, or secret readiness.

#### Evidence

- `git status --short` was clean before starting the audit pack branch.
- User approved the four audit reports plus audits README design.
- Plan/task self-review confirmed no placeholder markers and six independent
  logical units for subagent-driven execution.
- Plan creation validation: `git diff --check` — PASS; `bash
  scripts/generate-llm-wiki-index.sh --check` — PASS; `bash
  scripts/validate-repo-quality-gates.sh .` — PASS.
- T-002 manual matrix review — PASS; compared the governance benchmark against
  repo-backed evidence for purpose, rules, provider adapters, templates,
  scripts, CI/CD QA lanes, approval boundaries, and automation opportunities.
- T-002 validation: `git diff --check` — PASS; `bash
  scripts/validate-repo-quality-gates.sh .` — PASS.
- RTK limitation observed: `which rtk` did not find `rtk`; direct
  `/home/hy/.local/bin/rtk --version` reported `rtk 0.34.3`; `rtk gain` could
  not initialize its tracking database, so required task commands were run
  directly where exact command evidence was needed.
- T-003 through T-005 audit reports were completed and reviewed with
  subagent-assisted spec and quality checks. The T-003 section-contract issue
  and T-005 stale README wording issue were remediated and re-reviewed.
- Final T-006 validation: `git diff --check` — PASS; `bash
  scripts/generate-llm-wiki-index.sh --check` — PASS; `bash
  scripts/validate-repo-quality-gates.sh .` — PASS.
- Progress singleton validation: `rg --files | rg '(^|/)progress\.md$'` —
  PASS; returned only `docs/00.agent-governance/memory/progress.md`.
- Audit-pack status alignment scans — PASS; no audit-pack frontmatter remained
  `draft`, no audit-pack checklist remained unchecked, and no audit-pack README
  row remained `Draft`.

#### Handoff

- No remaining audit-pack task handoff. Future automation or remediation
  opportunities identified by the reports should start from a new scoped Spec,
  Plan, Task, script, CI, template, provider-adapter, or operations change.
- No live k3d, ArgoCD, Vault, ESO, Kubernetes, cloud, provider runtime, GitHub
  CI run-history, paid-job, deployment, external-service, or secret readiness
  checks were requested or run for this audit pack.

### 2026-07-02 — Workspace harness research pack

- **Date**: 2026-07-02
- **Layer**: docs, meta, qa
- **Status**: complete
- **Tags**: #research #harness #loop-engineering #sdlc #validation

#### Progress

- Completed the repo-first workspace harness research pack under
  [docs/90.references/research/](../../90.references/research/): one README
  plus four durable references covering governance baseline, harness/loop
  engineering, provider implementation status, and spec/SDLC/CI/QA/formatting.
- Finalized
  [T-006](../../04.execution/tasks/2026-07-02-workspace-harness-research-pack.md)
  by marking the task and phase complete and recording the final repo-static
  validation bundle.
- Confirmed the pack remains documentation-only reference material. Static
  repository gates were run; no live k3d, ArgoCD, Vault, ESO, Kubernetes,
  cloud, provider runtime, or secret readiness checks were requested or run.

#### Memory

- The research pack must remain durable reference material. It may summarize
  candidate improvements, but active policy changes belong in Stage 00,
  operations policy, plans, tasks, scripts, or templates.
- Current provider implementation claims for Claude, Codex/OpenAI, and
  Gemini/Google must be verified through current external sources before they
  are written into `docs/90.references/research/`.
- Workspace governance baseline summaries should name canonical owners and
  follow-up routes instead of restating or changing active Stage 00, CI,
  scripts, template, or provider-adapter policy.
- Repo-static validation for this research pack is completion evidence for
  Markdown structure, generated-index freshness, quality gates, and progress
  ledger uniqueness only. It is not live cluster or runtime readiness.

#### Evidence

- `git diff --check` — PASS; no output.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS;
  `[PASS] LLM WIKI generated index is current`.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS;
  `[PASS] repository quality gates passed`.
- `rg --files | rg '(^|/)progress\.md$'` — PASS; returned only
  `docs/00.agent-governance/memory/progress.md`.
- Read-only index review confirmed the research README, parent references
  README, plan README, and task README already index the research pack.
- Final review remediation aligned the plan/task lifecycle status and checklist
  markers to the completed task evidence.

#### Handoff

- None for the research pack itself. Future implementation of checklist items
  should start from a new Spec or Plan owned by the relevant canonical stage.

### 2026-06-05 — Harness governance V2 overlay

- **Date**: 2026-06-05
- **Layer**: meta, qa, docs
- **Status**: complete
- **Tags**: #harness #governance #codex #claude #eval #hookify #memory

#### Progress

- Extended the Stage 00
  [Harness Catalog](../harness-catalog.md) with the ECC DAILY/LIBRARY Surface
  and the Agent Eval Completion Contract.
- Classified repo-local gateway/runtime baselines, Stage 00 rules, shared
  hooks, local agents, GitOps/K8s/docs skills, and validators as `DAILY`
  surfaces; classified explicitly requested external skills such as
  `agent-sort`, `skill-creator`, `workflow-skill-design`, `eval-harness`,
  `harness-writing`, `enhance-prompt`, Hookify rule writing, and Claude MD
  improvement lenses as `LIBRARY` surfaces.
- Updated
  [workspace-harness-audit](../../../.agents/skills/workspace-harness-audit/skill.md)
  with numbered workflow phases, Entry Criteria, Exit Criteria, Verification
  Criteria, and named-skill boundaries.
- Added Codex/Claude adapter pointers for canonical progress ledger uniqueness,
  deterministic eval completion evidence, and Hookify local advisory vs shared
  enforcement boundaries.
- Added common Stage 00 rules requiring
  `docs/00.agent-governance/memory/progress.md` to be the only tracked
  `progress.md`, while standalone memory files remain allowed under the memory
  template contract.
- Extended
  [repository quality gates](../../../scripts/validate-repo-quality-gates.sh)
  to fail on non-canonical tracked `progress.md`, missing DAILY/LIBRARY,
  missing eval contract, missing Hookify advisory boundary, and missing
  workflow-skill phase criteria.
- Recorded the implementation plan and task evidence:
  - [Plan](../../04.execution/plans/2026-06-05-harness-governance-v2-overlay.md)
  - [Task](../../04.execution/tasks/2026-06-05-harness-governance-v2-overlay.md)

#### Memory

- `progress.md` is now a singleton filename in tracked files. The canonical
  progress ledger is `docs/00.agent-governance/memory/progress.md`.
- DAILY/LIBRARY classification is a routing contract, not a new install system;
  no `skill-library` router exists because `.agents/skills` remains the shared
  SSoT and `harness-catalog.md` is the catalog router.
- Hookify `.claude/hookify.*.local.md` files are ignored local advisory files.
  Shared enforcement belongs in tracked hooks, settings, hook JSON, scripts,
  and validators.
- Agent eval completion must be explicit deterministic command evidence or
  recorded human/operator approval. Static repo gates do not prove live k3d,
  ArgoCD, Vault, ESO, secret, or deployment readiness.
- `enhance-prompt` is a named-skill near-miss for this task because the work is
  not a UI/Stitch prompt task.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `git diff --check` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `python3 -m json.tool .claude/settings.json` — PASS.
- `python3 -m json.tool .codex/hooks.json` — PASS.
- `python3 -m json.tool .agents/hooks.json` — PASS.
- `find infrastructure scripts docs/00.agent-governance/hooks -type f -name '*.sh' -exec bash -n {} +` — PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
- `rg --files | rg '(^|/)progress\.md$'` — PASS, returned only
  `docs/00.agent-governance/memory/progress.md`.
- `git check-ignore -v .claude/hookify.postflight-reminder.local.md` — PASS,
  `.gitignore:66:.claude/*.local.md`.
- `/home/hy/.local/bin/pre-commit run --files <changed files>` — PASS after
  approved outside-sandbox execution. The first sandbox run failed because EOF
  fixer could not open `.agents/**` and `.codex/**` files.

#### Handoff

- None.

### 2026-06-04 — Harness four-element alignment

- **Date**: 2026-06-04
- **Layer**: meta, qa, docs
- **Status**: complete
- **Tags**: #harness #governance #codex #claude #validation

#### Progress

- Audited the current workspace harness against the four required elements:
  instruction and settings documents, architecture constraints, feedback loops,
  and knowledge stores.
- Added the canonical four-element control model to
  [Harness Catalog](../harness-catalog.md), including the relationship
  `instructions -> constraints -> feedback -> knowledge -> next-session instructions`.
- Updated [Claude Runtime Baseline](../../../.claude/CLAUDE.md) and
  [Codex Runtime Baseline](../../../.codex/CODEX.md) with provider-specific
  four-element runtime contracts.
- Added common governance for documentation folder responsibilities, canonical
  template-routing ownership, AI-agent-facing English sections, and drift
  garbage collection across code, documents, and structure.
- Updated the repo-local
  [workspace-harness-audit skill](../../../.agents/skills/workspace-harness-audit/skill.md)
  so future broad audits must preserve the four-element relationship model,
  language/template boundary evidence, drift cleanup evidence, and named-skill
  boundary evidence.
- Added regression checks to
  [repository quality gates](../../../scripts/validate-repo-quality-gates.sh)
  so the common model, provider runtime contracts, audit skill phrases,
  AI-agent-facing English sections, and drift cleanup contract cannot be
  removed silently.
- Recorded the implementation plan and task evidence:
  - [Plan](../../04.execution/plans/2026-06-04-harness-four-element-alignment.md)
  - [Task](../../04.execution/tasks/2026-06-04-harness-four-element-alignment.md)

#### Memory

- The harness is now documented as a control loop rather than a static file
  inventory: instructions load first, constraints block unsafe/off-domain work,
  feedback validates outputs, and knowledge stores feed the next session.
- Claude and Codex share Stage 00 governance, skills, hooks, validators, and
  memory, but they do not have identical enforcement mechanics: Claude has a
  native `.claude/settings.json` permission gate; Codex uses sandbox/approval
  boundaries plus `.codex/hooks.json` context and validation wiring.
- Repo-static validation remains mandatory completion evidence. Live k3d,
  ArgoCD, Vault, ESO, or deployment readiness must be proven separately with
  approved read-only runtime checks.
- Human-facing README and overview prose should remain Korean, while explicit
  AI-agent-facing sections such as `AI Agent Requirements` should remain
  English even inside otherwise Korean authored docs.
- Repeated code drift, document drift, or structure drift should update the
  harness surface that would prevent recurrence: rule, skill/prompt, hook,
  validator, template, README index, archive Tombstone, or memory entry.
- The direct RTK binary works (`/home/hy/.local/bin/rtk --version` reports
  `rtk 0.34.3`), but `/home/hy/.local/bin/rtk gain` cannot initialize its
  tracking database; commands were run through RTK where practical without
  inspecting private RTK state.

#### Evidence

- `git diff --check` — PASS.
- `python3 -m json.tool .claude/settings.json` — PASS.
- `python3 -m json.tool .codex/hooks.json` — PASS.
- `python3 -m json.tool .agents/hooks.json` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `find infrastructure scripts docs/00.agent-governance/hooks -type f -name '*.sh' -exec bash -n {} +` — PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash scripts/validate-gitops-structure.sh` — PASS.
- `bash scripts/validate-k8s-manifests.sh .` — PASS with optional
  `kube-linter` skip because it is not installed locally.
- `bash scripts/check-secret-handling.sh .` — PASS.
- `bash scripts/validate-policy-gates.sh .` — PASS with built-in fallback
  because optional `conftest` is not installed locally.
- `bash infrastructure/tests/verify-contracts-static.sh` — PASS.
- `zsh -lc 'command -v pre-commit'` — PASS,
  `/home/hy/.local/bin/pre-commit`.
- `/home/hy/.local/bin/pre-commit run --files <changed files>` — PASS after
  approved outside-sandbox execution.
- `/home/hy/.local/bin/pre-commit run --all-files` — FAILED in sandbox because
  EOF fixer could not open some `.agents/**` / `.codex/**` files and
  `detect-secrets` reported existing `graphify-out/**` generated-output false
  positives; changed-file pre-commit passed.

#### Handoff

- None.

### 2026-06-04 — Scripts QA and CI/CD alignment

- **Date**: 2026-06-04
- **Layer**: qa, ci, docs, meta
- **Status**: complete
- **Tags**: #scripts #qa #ci #validation #governance

#### Progress

- Re-audited the current `scripts/*.sh` inventory and confirmed there are seven
  tracked executable Bash scripts.
- Updated [scripts README](../../../scripts/README.md) so the inventory,
  structure, retention decision, local tool availability, deletion precheck,
  and command contracts match the current scripts and CI usage.
- Clarified `render-platform-chart-kinds.sh` as a retained manual chart-render
  review helper, not a default local/remote QA gate, because it may fetch remote
  Helm chart indexes.
- Promoted `validate-policy-gates.sh` to the documented Tier A
  `manifest-static` CI script and aligned local QA guidance, GitHub routing, and
  Claude command allow-list with that current contract.
- Hardened `render-platform-chart-kinds.sh` and `validate-policy-gates.sh` with
  explicit usage output, repo-root validation, Python/PyYAML checks, and
  deterministic policy target ordering.
- Extended `validate-repo-quality-gates.sh` so CI must keep
  `validate-policy-gates.sh` in `manifest-static`, Claude must allow the local
  QA script bundle, every current script has a fixed classification, and scripts
  reject hardcoded absolute machine paths.

#### Memory

- Current scripts inventory is seven files:
  `check-secret-handling.sh`, `generate-llm-wiki-index.sh`,
  `render-platform-chart-kinds.sh`, `validate-gitops-structure.sh`,
  `validate-k8s-manifests.sh`, `validate-policy-gates.sh`, and
  `validate-repo-quality-gates.sh`.
- Local fast feedback remains `pre-commit` when available. Local repo-static
  scripts reproduce CI/debug evidence; GitHub CI remains the required remote
  verdict for `branch-policy`, `pre-commit`, `repo-quality-static`, and
  `manifest-static`.
- `conftest` and `kube-linter` are optional locally; their scripts continue
  with built-in fallback or YAML-only validation when the binaries are missing.
- `render-platform-chart-kinds.sh` should be run for platform Helm chart or
  platform AppProject allow-list changes, but it is intentionally excluded from
  default CI because remote chart index fetches can vary.

#### Evidence

- `find scripts -maxdepth 1 -type f -name '*.sh'` — seven scripts found.
- Script reference sweep showed no unused or one-off deletion candidates; the
  only Tier C script is the retained chart render review helper.
- `command -v pre-commit` — not installed locally; pre-commit was not run.
- `bash -n scripts/*.sh docs/00.agent-governance/hooks/*.sh infrastructure/*.sh infrastructure/tests/*.sh` — PASS.
- `python3 -m json.tool .claude/settings.json` — PASS.
- `git diff --check` — PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash scripts/validate-gitops-structure.sh` — PASS.
- `bash scripts/validate-k8s-manifests.sh .` — PASS with optional
  `kube-linter` skip because it is not installed locally.
- `bash scripts/check-secret-handling.sh .` — PASS.
- `bash scripts/validate-policy-gates.sh .` — PASS with built-in fallback
  because optional `conftest` is not installed locally.
- `bash infrastructure/tests/verify-contracts-static.sh` — PASS.
- `bash scripts/render-platform-chart-kinds.sh .` — PASS after approved network
  access for Helm chart index fetches.
- Negative repo-root checks for `validate-k8s-manifests.sh gitops`,
  `check-secret-handling.sh gitops`, `validate-policy-gates.sh gitops`, and
  `render-platform-chart-kinds.sh gitops` failed clearly with usage output.
- Targeted stale/hardcode scans found no remaining stale five-script inventory,
  conftest no-op wording, Tier drift wording, or hardcoded absolute machine path
  in `scripts/*.sh`.

#### Handoff

- None.

### 2026-06-04 — Docs 01-05 current implementation alignment

- **Date**: 2026-06-04
- **Layer**: docs, architecture, ops, qa, meta
- **Status**: complete
- **Tags**: #docs #currentness #archive #validation #governance

#### Progress

- Re-audited active `docs/01.requirements`, `docs/02.architecture`,
  `docs/03.specs`, `docs/04.execution`, and `docs/05.operations` against
  repo-backed implementation evidence in `gitops/**`, `infrastructure/**`,
  `examples/**`, `traefik/**`, and `scripts/**`.
- Confirmed the existing central archive model in
  [Archive Index](../../98.archive/README.md) already matches the required
  `docs/98.archive` Tombstone and Index Only structure; no new active document
  required archival in this pass.
- Updated Rollouts PRD/ARD/ADR/Spec language so current Prometheus
  `AnalysisTemplate` usage is not described as future-only or analysis-free.
- Corrected the app onboarding policy to match the current `apps` AppProject
  allow-list, where `Deployment` is not included and new app workloads use
  `Rollout`.
- Repointed the P3 remediation plan from a removed active plan path to the
  current audit reference.
- Hardened the repository quality gate and CI/QA guide so these currentness
  drift classes are rejected in future edits.

#### Memory

- Current app workload evidence is `gitops/workloads/adminer/rollout.yaml` plus
  `gitops/workloads/adminer/analysis-template.yaml`; sample onboarding evidence
  is `examples/sample-app/analysis-template.yaml`.
- Current `apps` AppProject evidence is
  `gitops/clusters/local/appproject-apps.yaml`; it allows `Rollout` and
  `AnalysisTemplate`, not `Deployment`.
- `traefik/` is a current reference-only external Traefik dynamic-config
  surface, not a stale docs-only artifact.
- RTK is not available on PATH in this session, and direct
  `/home/hy/.local/bin/rtk gain` failed to initialize its tracking database.
  Commands were run directly without inspecting private RTK databases.

#### Evidence

- Static implementation evidence read from `gitops/clusters/local/appproject-apps.yaml`,
  `gitops/workloads/adminer/rollout.yaml`,
  `gitops/workloads/adminer/analysis-template.yaml`, and
  `examples/sample-app/analysis-template.yaml`.
- Targeted active stale scans covered legacy/deprecated/archive wording,
  Rollouts analysis-provider drift, removed plan references, and apps
  AppProject Deployment claims.
- `git diff --check` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash scripts/validate-gitops-structure.sh` — PASS.
- `bash scripts/validate-k8s-manifests.sh .` — PASS with optional
  `kube-linter` skip because it is not installed locally.
- `bash scripts/check-secret-handling.sh .` — PASS.
- `bash scripts/validate-policy-gates.sh .` — PASS with built-in fallback
  because optional `conftest` is not installed locally.
- `bash infrastructure/tests/verify-contracts-static.sh` — PASS.

#### Handoff

- None.

### 2026-06-02 — Phase 4 ESO Vault runtime diagnosis

- **Date**: 2026-06-02
- **Layer**: ops, infra, security, qa
- **Status**: complete
- **Tags**: #phase-4 #eso #vault #runtime #runbook #validation

#### Progress

- Created the Phase 4 ESO/Vault runtime diagnosis pair:
  - [Plan](../../04.execution/plans/2026-06-02-phase-4-eso-vault-runtime-diagnosis.md)
  - [Task](../../04.execution/tasks/2026-06-02-phase-4-eso-vault-runtime-diagnosis.md)
- Performed read-only diagnosis of the Phase 3 live validation failure.
- Confirmed `vault-external` Service, `vault-external-1` EndpointSlice,
  `vault-backend` ClusterSecretStore, `external-secrets` ServiceAccount, and
  token reviewer binding match the repo desired-state contract.
- Updated [ArgoCD ESO Vault Recovery Runbook](../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md)
  so it distinguishes Vault sealed state from EndpointSlice/network drift and
  marks Vault unseal as operator-bound.
- Updated the Runbooks README index row and linked Phase 4 from Phase 3
  downstream evidence.

#### Memory

- Root cause class: Vault is reachable at `172.18.0.8:8200`, but it is sealed.
  ESO Kubernetes auth login fails with HTTP 503 and `Vault is sealed`.
- `ClusterSecretStore/vault-backend Ready=False` and dependent
  `ExternalSecret` `SecretSyncedError` are downstream symptoms when Vault is
  sealed.
- Do not patch EndpointSlice for this signature. EndpointSlice hotfix is for
  unreachable/refused endpoint drift, not for sealed Vault.
- Do not request, read, paste, log, or commit Vault unseal keys, root tokens,
  Vault tokens, or secret values. Vault unseal remains operator-bound.

#### Evidence

- `kubectl get clustersecretstore vault-backend -o yaml` — live spec matches
  repo contract and reports `Ready=False`, reason `InvalidProviderConfig`.
- `kubectl -n argocd get externalsecret argocd-external-valkey -o yaml` —
  reports `Ready=False`, reason `SecretSyncedError`.
- `kubectl -n platform get svc vault-external -o yaml` and
  `kubectl -n platform get endpointslice vault-external-1 -o yaml` — live
  service/endpoint match repo values.
- `curl -sS --max-time 5 http://172.18.0.8:8200/v1/sys/health` — PASS command
  exit 0; response reports `sealed:true`.
- `kubectl -n external-secrets logs deploy/external-secrets --since=2h --tail=80`
  — PASS command exit 0; logs show `Vault is sealed`.
- `docker ps --format ...` — PASS; `vault` container is running and attached to
  `k3d-hyhome`.

#### Handoff

- Static repo remediation for this diagnosis is complete.
- Live readiness remains blocked until a Vault operator unseals Vault using
  secret-bearing key material outside the agent/chat/repo surfaces.
- After unseal, rerun `bash infrastructure/tests/run-all.sh` and update the
  Phase 4 task/progress evidence if live readiness changes.

### 2026-06-02 — Phase 3 protected surface hardening

- **Date**: 2026-06-02
- **Layer**: meta, docs, qa, ci, runtime
- **Status**: complete
- **Tags**: #governance #phase-3 #ci #runtime #validation

#### Progress

- Created the Phase 3 protected-surface traceability pair:
  - [Plan](../../04.execution/plans/2026-06-02-phase-3-protected-surface-hardening.md)
  - [Task](../../04.execution/tasks/2026-06-02-phase-3-protected-surface-hardening.md)
- Added `.agents/**` to the GitHub Actions `repo_quality` path filter so shared
  asset SSoT changes trigger repository quality validation.
- Hardened shared post/lifecycle hooks so `.agents/*` changes trigger
  repository quality gates and `.agents/hooks.json` is parsed with the other
  runtime hook JSON files.
- Clarified SessionStart live probes as read-only runtime evidence, not
  repo-static readiness proof.
- Added non-structural Plan/Task template guidance for human approval and live
  runtime readiness boundaries.
- Updated Phase 2 downstream links, Plans/Tasks README indexes, governance
  quality guidance, the CI/QA guide, `.github` workflow evidence, and the
  harness catalog.

#### Memory

- Approval was granted for policy, runtime hook, CI, template, CI topology,
  model policy, provider config, GitOps manifest, and live validation scope.
- Approval does not require speculative edits. Model policy, provider config,
  and GitOps manifest surfaces were reviewed as no-op because no concrete drift
  was found in this Phase 3 scope.
- Treat repo-static validation, CI/toolchain validation, and live runtime
  validation as separate evidence lanes.
- Current approved read-only live validation shows live ESO/Vault readiness is
  not clean: `ClusterSecretStore/vault-backend` is `Ready=False` with
  `InvalidProviderConfig`, and `argocd-external-valkey` is `Ready=False` with
  `SecretSyncedError`.

#### Evidence

- `bash -n docs/00.agent-governance/hooks/post-validate.sh docs/00.agent-governance/hooks/lifecycle-guard.sh docs/00.agent-governance/hooks/session-start.sh scripts/validate-repo-quality-gates.sh` — PASS.
- `git diff --check` — PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- Targeted `.agents/**` and `.agents/hooks.json` trigger scan — PASS.
- Targeted Phase 3 index/frontmatter/related-documents scans — PASS.
- Protected-surface no-op diff review for model policy, provider config, and
  GitOps manifests — PASS; no diff under `docs/00.agent-governance/model-policy.md`,
  `.codex/agents`, `.claude/agents`, `.agents/agents`, `gitops`, or
  `infrastructure`.
- `HY_HOME_K8S_ENABLE_SESSION_LIVE_PROBES=1 bash docs/00.agent-governance/hooks/session-start.sh` — PASS command exit 0; reported k3d `hyhome`, three Terminating pods, and Degraded `adminer`, `platform-argocd-config`, and `platform-eso-config` ArgoCD apps.
- `bash infrastructure/tests/run-all.sh` — FAIL at ESO/Vault integration:
  `vault-backend Ready is not True (actual=False)`.
- `bash infrastructure/tests/verify-external-services.sh` — PASS.
- `bash infrastructure/tests/verify-network-policies.sh` — PASS.
- `bash infrastructure/tests/verify-ingress-tls.sh` — PASS with warning that
  Kiali ingress TLS secret was not found or mismatched.

#### Handoff

- Phase 3 static guardrail implementation is complete and validated.
- Live runtime readiness is not complete. Follow-up should diagnose
  `vault-backend` `InvalidProviderConfig`, `argocd-external-valkey`
  `SecretSyncedError`, Terminating pods, and Degraded ArgoCD apps without
  inspecting secret values or mutating the cluster unless the next task
  explicitly scopes that remediation.

### 2026-06-02 — Phase 2 governance alignment planning artifact

- **Date**: 2026-06-02
- **Layer**: meta, docs, qa
- **Status**: complete
- **Tags**: #governance #phase-2 #planning #traceability #validation

#### Progress

- Created the Phase 2 planning pair:
  - [Plan](../../04.execution/plans/2026-06-02-phase-2-governance-alignment.md)
  - [Task](../../04.execution/tasks/2026-06-02-phase-2-governance-alignment.md)
- Routed Phase 2 through the canonical `docs/04.execution` stage instead of
  creating off-taxonomy `docs/superpowers/**` artifacts.
- Updated Plans and Tasks README indexes so the Phase 2 artifacts are
  discoverable.
- Added downstream Phase 2 links to the Phase 1 governance alignment audit task.

#### Memory

- Phase 2 governance alignment is a docs-only planning artifact that preserves
  ADR-0013 and the Phase 1 audit decisions.
- Do not treat Phase 2 static checks as live runtime readiness. k3d, ArgoCD,
  Vault, ESO, deployment, external service, and secret inspection remain
  deferred unless a human approves a separate runtime validation task.
- Do not change model policy, provider TOML, hook scripts, CI workflow, GitOps
  manifests, or Kubernetes desired state for this Phase 2 artifact.

#### Evidence

- `git diff --check` — PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- Targeted Phase 2 index scan — PASS.
- Targeted Phase 2 frontmatter and related-documents scan — PASS.

#### Handoff

- No live k3d, ArgoCD, Vault, ESO, Kubernetes mutation, deployment, external
  service, secret inspection, private RTK database, model policy, provider
  config, hook script, CI workflow, or GitOps manifest action was performed.

### 2026-06-02 — Phase 1 governance alignment audit

- **Date**: 2026-06-02
- **Layer**: meta, docs, qa, infra
- **Status**: complete
- **Tags**: #governance #phase-1 #adapter #gitops #validation

#### Progress

- Created [Phase 1 Governance Alignment Audit Task](../../04.execution/tasks/2026-06-02-phase-1-governance-alignment-audit.md)
  as repo-static evidence for the user-provided audit plan.
- Re-audited Stage 00 canonical governance, provider adapters, docs lifecycle,
  QA/CI/CD gates, and GitOps boundaries against current repository evidence.
- Confirmed ADR-0013 remains the accepted adapter architecture: Stage 00 owns
  durable governance, `.agents/**` owns shared assets, and `.claude/**` plus
  `.codex/**` expose provider adapters.
- Corrected the stale 2026-05-30 Antigravity plan/task lifecycle from `active`
  to `done` after confirming its scoped tasks were already complete and current
  adapter ownership is covered by the Stage 00 canonical adapter workstream.

#### Memory

- Treat the Phase 1 governance alignment audit as current-state evidence, not
  a new Stage 00 redesign.
- Historical `.claude/hooks/*.sh` mentions in older progress entries are not
  active hook contracts. Current provider hook wiring points to
  `docs/00.agent-governance/hooks/*.sh`.
- Static repository gates do not prove live k3d, ArgoCD, Vault, ESO,
  deployment, or external service health. Live checks require a separate
  human-approved runtime validation scope.

#### Evidence

- Root shim line count and import scan — PASS.
- Shared asset symlink and provider agent roster scan — PASS.
- Hook config/path existence scan — PASS.
- Prohibited docs path scan — PASS.
- Stale execution status scan found the 2026-05-30 Antigravity `active` status
  and this change remediated it in place.
- `git diff --check` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS after adding the
  required `## Suggested Types` heading caught by the first run.
- `bash scripts/validate-gitops-structure.sh` — PASS.
- `bash scripts/validate-k8s-manifests.sh .` — PASS for YAML syntax and
  kustomization coverage; optional `kube-linter` was not installed and was
  skipped by the script.
- `bash scripts/check-secret-handling.sh .` — PASS.

#### Handoff

- No live k3d, ArgoCD, Vault, ESO, Kubernetes mutation, deployment, external
  service, secret inspection, or private RTK database action was performed.
- Optional `kube-linter` was unavailable during manifest validation.

### 2026-06-02 — Stage 00 Codex harness coverage reconciliation

- **Date**: 2026-06-02
- **Layer**: docs, governance, codex, qa
- **Status**: complete
- **Tags**: #governance #codex #docs #traceability #validation

#### Progress

- Created the corrective traceability pair:
  - [Plan](../../04.execution/plans/2026-06-02-stage-00-codex-harness-coverage-reconciliation.md)
  - [Task](../../04.execution/tasks/2026-06-02-stage-00-codex-harness-coverage-reconciliation.md)
- Preserved the completed
  [Phase 1 Decision Follow-up Plan](../../04.execution/plans/2026-06-02-phase-1-decision-follow-up.md)
  and added a current-state coverage reconciliation note without reopening its
  `status: done`.
- Mapped the original attachment's broader Stage 00/Codex harness requirements
  to existing completed evidence from the 2026-05-31 Codex harness alignment
  and 2026-06-01 Stage 00 canonical adapter workstreams.
- Updated Plans and Tasks README indexes so the corrective Plan/Task artifacts
  are discoverable from the execution stage.

#### Memory

- Treat the 2026-06-02 coverage reconciliation as a traceability correction, not
  a new Stage 00 redesign.
- Before changing Stage 00, Codex TOML, CI workflow, or Kubernetes manifests for
  this topic, first verify that the claimed gap is not already covered by the
  2026-05-31 or 2026-06-01 completed Plan/Task evidence.
- Keep live k3d, ArgoCD, Vault, Kubernetes mutation, secret inspection, and CI
  topology changes out of this reconciliation unless a human approves a new
  implementation scope.

#### Evidence

- Targeted Plan/Task frontmatter and heading scan — PASS
- Targeted Plans/Tasks README index scan — PASS
- `git diff --check` — PASS
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS
- `bash scripts/validate-repo-quality-gates.sh .` — PASS

#### Handoff

- No live k3d, ArgoCD, Vault, Kubernetes mutation, secret inspection, CI
  topology change, or provider configuration change was performed.

### 2026-06-02 — Operations documentation template conformance

- **Date**: 2026-06-02
- **Layer**: docs, operations, qa
- **Status**: complete
- **Tags**: #docs #operations #templates #readme #validation

#### Progress

- Audited authored Guide, Policy, and Runbook documents under
  [05.operations](../../05.operations/README.md) against their required
  templates:
  [guide.template.md](../../99.templates/templates/sdlc/operations/guide.template.md),
  [policy.template.md](../../99.templates/templates/sdlc/operations/policy.template.md), and
  [runbook.template.md](../../99.templates/templates/sdlc/operations/runbook.template.md).
- Confirmed the existing non-README Guide, Policy, and Runbook documents keep
  the required frontmatter, `owner: platform`, `type`, and required template
  headings.
- Added README template snippet alignment to:
  - [Guides README](../../05.operations/guides/README.md)
  - [Policies README](../../05.operations/policies/README.md)
  - [Runbooks README](../../05.operations/runbooks/README.md)
  - [Incidents README](../../05.operations/incidents/README.md)
- Confirmed there are no tracked authored Incident Record or Postmortem files
  under `docs/05.operations/incidents/` yet, so no placeholder incident or
  postmortem document was created.

#### Memory

- `docs/05.operations/incidents/` stays README-only until a real incident
  record or postmortem is needed. Use `incident.template.md` and
  `postmortem.template.md` only when recording a real event or stabilized
  post-incident analysis.
- README template alignment for operations folders should use only the snippets
  that match the folder responsibility; do not paste the full snippet library
  into authored READMEs.
- Code fences in operational docs contain shell comments beginning with `#`;
  heading checks should ignore fenced code before treating them as duplicate
  H1s.

#### Evidence

- Targeted README heading scan — PASS
- Targeted Guide/Policy/Runbook frontmatter and required heading scan — PASS
- `git diff --check` — PASS
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS
- `bash scripts/validate-repo-quality-gates.sh .` — PASS

#### Handoff

- No live k3d, ArgoCD, Vault, Kubernetes mutation, or external service action
  was performed.

### 2026-06-02 — Phase 1 decision follow-up plan

- **Date**: 2026-06-02
- **Layer**: docs, meta, qa
- **Status**: complete
- **Tags**: #governance #docs #phase-1 #planning #validation

#### Progress

- Created [Phase 1 Decision Follow-up Plan](../../04.execution/plans/2026-06-02-phase-1-decision-follow-up.md)
  as a Phase 2 planning artifact for the 2026-06-02 Phase 1 continuation decisions.
- Updated [Plans README](../../04.execution/plans/README.md) so the new plan is indexed in the stage structure and document table.
- Implemented the plan by promoting it to `status: done` and checking its completion criteria after static validation.
- Kept the scope documentation-only: no Stage 00 policy edits, Codex TOML edits, CI workflow edits, Kubernetes manifests, ArgoCD, Vault, or live cluster changes.

#### Memory

- Phase 1 decision follow-up should preserve the completed Stage 00 canonical adapter model unless a future task finds a concrete drift.
- HADS remains an optional documentation-structure lens; `docs/99.templates` remains the canonical authored-document contract.
- The exact `qa(ouroboros-qa)` skill path is still a local roster gap. Do not invent a path; update `harness-catalog.md` only if the exact skill becomes available.
- When `node`, `npm`, or `rtk` are missing from the current shell PATH, use `/home/hy/.local/bin` direct calls or an explicit PATH prefix. Do not inspect private RTK databases or credentials when `rtk gain` fails.

#### Evidence

- `git diff --check` — PASS
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS
- `bash scripts/validate-repo-quality-gates.sh .` — PASS
- `git status --short --branch` — changed files limited to the new plan,
  plans README, and progress ledger.

#### Handoff

- None for this documentation-only planning artifact. Live k3d, ArgoCD, Vault,
  Kubernetes mutation, and external service actions remain out of scope unless explicitly approved.

### 2026-05-31 — Codex governance harness alignment

- **Date**: 2026-05-31
- **Layer**: meta, docs, qa
- **Status**: complete
- **Tags**: #governance #codex #model-policy #template-contract #validation

#### Progress

- Created the approved Phase 2/3 traceability pair:
  - [Plan](../../04.execution/plans/2026-05-31-codex-governance-harness-alignment.md)
  - [Task](../../04.execution/tasks/2026-05-31-codex-governance-harness-alignment.md)
- Updated Stage 00 model policy and harness catalog so Codex worker tier stays
  `gpt-5.3-codex`, with explicit Codex `model_reasoning_effort` expectations.
- Added `model_reasoning_effort` to all eight `.codex/agents/*.toml` mirrors:
  `xhigh` for `supervisor`, `high` for implementation/review/security/incident
  workers, and `medium` for docs/wiki workers.
- Clarified `AGENTS.md` and provider docs so `AGENTS.md` is the Codex/GPT
  gateway while Claude and Gemini use their provider shims.
- Normalized active policy template routing from the nonexistent
  `deprecated operations-template route` to `policy.template.md`.
- Normalized all seven `docs/05.operations/policies/*.md` files from
  `type: operation` to `type: sdlc/policy`.
- Extended `scripts/validate-repo-quality-gates.sh` to catch Codex TOML
  model/effort drift, active `deprecated operations-template route` routing drift, and
  operations policy frontmatter type drift.

#### Memory

- `gpt-5.3-codex` is the Codex worker model for this repository's local agent
  roster; do not reintroduce `gpt-5.4-mini` as the worker baseline unless the
  Stage 00 Model Policy and harness catalog are deliberately updated together.
- Active operations policy routing uses `docs/99.templates/templates/sdlc/operations/policy.template.md`.
  `deprecated operations-template route` is not a valid template in this repository.
- `AGENTS.md` is the Codex/GPT gateway. Root `CLAUDE.md` and `GEMINI.md` remain
  provider shims for their runtimes.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` — PASS
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS
- `rg -n "GPT-5.4-mini|gpt-5.4-mini" docs/00.agent-governance .codex AGENTS.md -g '!docs/00.agent-governance/memory/**'` — no output
- `rg -n "model_reasoning_effort" .codex/agents` — eight TOML entries found
- `rg -n "^type: operation$" docs/05.operations/policies` — no output
- `rg -n "operation\\.template\\.md" .agents docs/00.agent-governance .codex -g '!docs/00.agent-governance/memory/**'` — no output
- `bash -n docs/00.agent-governance/hooks/k8s-pre-edit.sh scripts/validate-repo-quality-gates.sh` — PASS
- `git diff --check` — PASS

#### Handoff

- None. The approved repo-static Phase 3 scope is complete; no live cluster,
  ArgoCD, Vault, or secret-value action was performed.

### 2026-05-29 — Docs governance consistency residual fix (owner normalization, CI/CD guide, template audit)

- **Date**: 2026-05-29
- **Layer**: docs, governance, ci
- **Status**: complete
- **Tags**: #governance #docs #consistency #ci-cd

#### Progress

- Normalized `owner: deprecated owner value` → `owner: platform` across 37 files in stages 01–04 (`docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`).
- Fixed one-off `owner: 'deprecated owner value'` (quoted) in `docs/04.execution/plans/2026-05-17-template-crosslink-fix.md`.
- Created missing task file: `docs/04.execution/tasks/2026-05-17-template-crosslink-fix.md` (retrospective; the plan was done 2026-05-21).
- Audited all 23 `docs/99.templates/*.md` files: all structural templates have 5-field frontmatter + `## Related Documents`; `memory.template.md` and `progress.template.md` intentionally use append-style without frontmatter — no changes needed.
- Created `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md` — CI/CD local-vs-GitHub Actions boundary reference guide.
- Updated `docs/05.operations/guides/README.md` structure tree and document index table.
- Updated `docs/00.agent-governance/rules/documentation-protocol.md` with canonical `owner: platform` rule.

#### Verification

- `bash scripts/validate-repo-quality-gates.sh .` — PASS
- `grep -r "^owner: deprecated owner value" docs/ | wc -l` → 0

#### Follow-up

- None. PLN-G final validation pass completes this work.

### 2026-05-28 — Workspace skill expansion P0-16 (5 new repo-local skills)

- **Date**: 2026-05-28
- **Layer**: governance, skills, docs, validation
- **Status**: complete
- **Tags**: #governance #skills #sdd #harness #p0-16

#### Progress

- Created 5 new repo-local skills under `.claude/skills/`:
  - `requirements-to-design/skill.md` — PRD→ARD/ADR traceability and coverage matrix
  - `execution-plan/skill.md` — design artifact to plan transformation
  - `task-breakdown/skill.md` — plan to agent-executable task unit decomposition
  - `ops-runbook/skill.md` — bootstrap, recovery, deployment, and incident runbooks
  - `knowledge-map/skill.md` — governance index maintenance and stale-link detection
- Updated `docs/00.agent-governance/harness-catalog.md` Skills table with 5 new entries.
- Updated `docs/00.agent-governance/harness-catalog.md` Task-to-Skill Routing table
  with 3 new SDD lifecycle rows (SDD lifecycle traceability, Operations runbook authoring,
  Governance index maintenance).
- Fixed `scripts/validate-repo-quality-gates.sh` pipe-table normalization to handle
  markdownlint auto-padded table headers (prevents future whitespace-induced false failures).
- Created plan artifact: `docs/04.execution/plans/2026-05-28-workspace-skill-expansion.md`
- Created task artifact: `docs/04.execution/tasks/2026-05-28-workspace-skill-expansion.md`
- Deferred: Compose Stack Agent (Docker Compose scope belongs to external-services workspace),
  Policy Gate Agent (consolidated into workspace-harness-audit; OPA/Conftest P3).

#### Verification

- `bash scripts/validate-repo-quality-gates.sh .` — PASS
- All 5 skill files exist on disk.

#### Follow-up

- P3-01: Install conftest; enable CI enforcement for `validate-policy-gates.sh`.
- P3-02: Start hy-home.docker gateway, rerun `verify-ingress-tls.sh` with `CHECK_TRAEFIK_443=true`.
- P3-03: After human approval, run `kubectl diff -k gitops/clusters/local` and ArgoCD sync.

### 2026-05-26 — Workspace-wide P0 audit overlay (VAL-SPC-006-059)

- **Date**: 2026-05-26
- **Layer**: meta, governance, docs, infra, GitOps, validation
- **Status**: complete
- **Tags**: #governance #sdd #harness #skills #p0-audit

#### Progress

- Confirmed VAL-SPC-006-001 through VAL-SPC-006-058 already address all 22 P0
  workstreams and 6 additional review criteria from the workspace improvement
  prompt.
- Fixed `.agents/skills/` mirror parity: added `docs-stage-conformance` and
  `workspace-harness-audit` mirrors (2 skills; `risk-report` was already
  present).
- Re-evaluated 7 workspace-specific AI Agent skill candidates:
  - 5 rejected (Compose Stack, Requirements-to-Design, Execution Plan, Task
    Breakdown, Knowledge Map) — covered by existing agents, skills, and
    templates.
  - Ops Runbook: no gap found; `doc-writer.md` + `runbook.template.md` +
    11 existing runbooks provide sufficient coverage.
  - Policy Gate: consolidated into `workspace-harness-audit` skill scope; no
    separate skill needed.
- Recorded VAL-SPC-006-059 overlay in
  `docs/03.specs/006-workspace-harness-gap-analysis/spec.md`.
- P3 deferrals carried forward: OPA/Conftest CI enforcement, Traefik 443 live
  proof, ArgoCD live reconciliation.

#### Verification

- `bash scripts/validate-repo-quality-gates.sh .` — PASS (post-implementation)
- `bash scripts/generate-llm-wiki-index.sh --check` — run after progress.md
  update

#### Follow-up

- P3-01: Install conftest and add CI step for `validate-policy-gates.sh`.
- P3-02: Start hy-home.docker gateway, then rerun `verify-ingress-tls.sh`
  with `CHECK_TRAEFIK_443=true`.
- P3-03: After human approval, run `kubectl diff -k gitops/clusters/local`
  and ArgoCD sync to confirm AppProject desired-state.

### 2026-05-26 — OPA/Conftest policy gate follow-up

- **Date**: 2026-05-26
- **Layer**: policy, GitOps, Kubernetes, validation, SDD
- **Status**: partial
- **Tags**: #policy #opa #conftest #gitops #validation #sdd

#### Progress

- Added `policy/conftest/kubernetes.rego` for plaintext Secret,
  `CreateNamespace=true`, AppProject wildcard, and `latest` image checks.
- Added `scripts/validate-policy-gates.sh` to run Conftest when installed and a
  built-in fallback otherwise.
- Documented the policy gate script in `scripts/README.md` and routed
  GitOps policy bundle ownership in `gitops/README.md`.
- Fixed `examples/azure/kubernetes/sample-app.yaml` from `nginx:latest` to a
  pinned image tag.
- Recorded `VAL-SPC-006-058` and `T-282` through `T-288` in the existing 006
  Spec/Plan/Task chain.

#### Verification

- `command -v conftest` — NOT INSTALLED.
- `bash -n scripts/validate-policy-gates.sh` — PASS.
- `bash scripts/validate-policy-gates.sh .` — PASS via built-in fallback.

#### Follow-up

- Add CI installation/execution for Conftest if policy enforcement must move
  from manual/repo-local validation into the required CI job graph.

### 2026-05-26 — Platform chart render review follow-up

- **Date**: 2026-05-26
- **Layer**: GitOps, Helm, ArgoCD, validation, SDD
- **Status**: partial
- **Tags**: #gitops #helm #argocd #validation #sdd

#### Progress

- Added `scripts/render-platform-chart-kinds.sh` to render Helm chart
  Applications under `gitops/apps/root` and compare rendered kinds with the
  platform AppProject allow-list.
- Updated `scripts/README.md` with the script inventory, classification, and
  command contract.
- Added `gitops/README.md` Platform Chart Render Review Matrix.
- Tightened `gitops/clusters/local/appproject-platform.yaml` to remove unused
  kind grants not supported by raw platform manifests or rendered chart output.
- Recorded `VAL-SPC-006-057` and `T-275` through `T-281` in the existing 006
  Spec/Plan/Task chain.

#### Verification

- `bash -n scripts/render-platform-chart-kinds.sh` — PASS.
- `bash scripts/render-platform-chart-kinds.sh .` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` — PASS.
- `bash scripts/validate-k8s-manifests.sh .` — PASS; optional kube-linter remains
  skipped when not installed.

#### Follow-up

- Confirm ArgoCD reconciliation after the committed desired state is available
  to the cluster source revision.

### 2026-05-26 — AppProject and namespace semantic hardening follow-up

- **Date**: 2026-05-26
- **Layer**: GitOps, ArgoCD, validation, SDD
- **Status**: partial
- **Tags**: #gitops #argocd #validation #sdd

#### Progress

- Removed the `apps` AppProject cluster-scoped `Namespace` grant.
- Trimmed the `apps` AppProject namespace allow-list to active workload kinds
  plus policy-optional `ExternalSecret`.
- Removed `CreateNamespace=true` from GitOps Application/ApplicationSet YAML.
- Updated `gitops/README.md` AppProject and Namespace Ownership matrices.
- Updated `scripts/validate-repo-quality-gates.sh` and
  `infrastructure/tests/verify-contracts-static.sh` to enforce the tightened
  desired state.
- Recorded `VAL-SPC-006-056` and `T-269` through `T-274` in the existing 006
  Spec/Plan/Task chain.

#### Verification

- Live namespace inspection — PASS; required namespaces already exist.
- Live ArgoCD status inspection — PASS with caveat; platform apps are
  Synced/Healthy and `adminer` remains Synced/Degraded outside this cleanup.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `bash -n infrastructure/tests/verify-contracts-static.sh` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` — PASS.
- `bash scripts/validate-gitops-structure.sh` — PASS.
- `bash scripts/validate-k8s-manifests.sh .` — PASS; optional kube-linter remains
  skipped when not installed.
- `bash scripts/check-secret-handling.sh .` — PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
- `bash infrastructure/tests/run-all.sh` — PASS; Traefik 443 enforcement remains
  opt-in through `CHECK_TRAEFIK_443=true`.
- `kubectl diff -k gitops/clusters/local` — DIFF EXPECTED; pending AppProject
  and root/ApplicationSet desired-state changes were shown.
- `kubectl diff -k gitops/apps/root` — DIFF EXPECTED; pending platform root
  Application sync-option changes were shown.
- `argocd app diff --core --local ...` — NOT USABLE; local ArgoCD CLI core
  diff could not find `argocd-cm`, so `kubectl diff` was used as the read-only
  alternative.

#### Follow-up

- Confirm ArgoCD reconciliation after the committed desired state is available
  to the cluster source revision.

### 2026-05-26 — AppProject allow-list rationale guardrail follow-up

- **Date**: 2026-05-26
- **Layer**: GitOps, ArgoCD, validation, SDD
- **Status**: partial
- **Tags**: #gitops #argocd #validation #sdd

#### Progress

- Rechecked `apps` and `platform` AppProject allow-list surfaces against active
  workload manifests and chart-managed platform boundaries.
- Added `gitops/README.md` AppProject Allow-list Rationale Matrix.
- Extended `scripts/validate-repo-quality-gates.sh` to compare the `apps`
  cluster allow-list, active workload kinds, reserved namespace kinds, and
  platform chart-managed boundary wording against current manifests.
- Updated `scripts/README.md` command-contract wording.
- Recorded `VAL-SPC-006-055` and `T-264` through `T-268` in the existing 006
  Spec/Plan/Task chain.

#### Verification

- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
- `bash scripts/validate-gitops-structure.sh` — PASS.
- `bash scripts/validate-k8s-manifests.sh .` — PASS; optional kube-linter remains
  skipped when not installed.
- `bash scripts/check-secret-handling.sh .` — PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` — PASS.
- Shell syntax sweep for `infrastructure`, `scripts`, and `.claude/hooks` — PASS.
- JSON parse for `.claude/settings.json` and `.codex/hooks.json` — PASS.
- Workflow YAML parse for `.github/workflows/*.yml` — PASS.
- `.env.example` vs `.env` key-name-only comparison — PASS; values were not
  printed.
- Targeted sample backend check — PASS; no active `k3d-hyhome-serverlb:443`
  reference remains in `examples/sample-app`.
- `git diff --check` — PASS.
- `bash infrastructure/tests/run-all.sh` — BLOCKED; not rerun in this pass
  because live kubeconfig TLS trust remains blocked by the previously recorded
  `x509: certificate signed by unknown authority` failure.

#### Follow-up

- Keep actual allow-list kind removal, AppProject permission tightening,
  `Namespace` removal, platform chart-render review, and live ArgoCD sync impact
  as separate follow-up work.

### 2026-05-26 — Destructive Git permission hardening follow-up

- **Date**: 2026-05-26
- **Layer**: agent governance, Git workflow, validation, SDD
- **Status**: partial
- **Tags**: #agent-governance #git #validation #sdd

#### Progress

- Rechecked `.claude/settings.json`, `git-workflow.md`, harness catalog, and
  repository quality coverage for destructive Git command boundaries.
- Added shared Claude deny rules for destructive or history-rewriting Git
  command classes.
- Documented the human-approved recovery exception path in
  `docs/00.agent-governance/rules/git-workflow.md`.
- Extended `scripts/validate-repo-quality-gates.sh` to validate the deny list
  and related Git workflow phrases.
- Recorded `VAL-SPC-006-054` and `T-259` through `T-263` in the existing 006
  Spec/Plan/Task chain.

#### Verification

- `python3 -m json.tool .claude/settings.json >/dev/null` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `git diff --check` — PASS.
- Destructive Git commands — NOT RUN.

#### Follow-up

- Keep GitHub branch protection/ruleset changes and any actual destructive Git
  recovery command outside normal agent execution unless explicitly approved
  with scope, branch, rollback/backup, and verification evidence.

### 2026-05-26 — Traefik serverlb boundary guardrail follow-up

- **Date**: 2026-05-26
- **Layer**: Traefik, infrastructure, validation, SDD
- **Status**: partial
- **Tags**: #traefik #infrastructure #validation #sdd

#### Progress

- Re-ran the read-only Traefik 443 proof after default kubeconfig repair.
- Confirmed Docker inventory shows `k3d-hyhome-serverlb` bound to host `:443`,
  but no separate external Traefik gateway container.
- Clarified in `traefik/README.md` that `k3d-hyhome-serverlb` is not proof of
  the `hy-home.docker` external gateway or dynamic config state.
- Extended `scripts/validate-repo-quality-gates.sh` to keep the serverlb versus
  external gateway boundary explicit.
- Recorded `VAL-SPC-006-053` and `T-254` through `T-258` in the existing 006
  Spec/Plan/Task chain.

#### Verification

- `kubectl version --request-timeout=5s` — PASS; client/server minor version
  skew warning observed.
- `docker ps --format '{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'` —
  PASS; no separate external Traefik gateway container was present.
- `CHECK_TRAEFIK_443=true bash infrastructure/tests/verify-ingress-tls.sh` —
  FAIL as boundary evidence: `Traefik 443 endpoint is not reachable
(argocd.127.0.0.1.nip.io:443)`.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `git diff --check` — PASS.

#### Follow-up

- Keep external Traefik gateway startup, dynamic config application, and
  `hy-home.docker` runtime proof as separate operator-owned follow-up work.

### 2026-05-26 — Kube-linter optional boundary guardrail follow-up

- **Date**: 2026-05-26
- **Layer**: scripts, manifests, QA, validation, SDD
- **Status**: partial
- **Tags**: #scripts #manifests #qa #validation #sdd

#### Progress

- Rechecked current kube-linter behavior in `scripts/validate-k8s-manifests.sh`
  and `.kube-linter.yaml`.
- Added `scripts/README.md` Kube-linter Exclusion Matrix to record rationale,
  boundary, and follow-up for each excluded check.
- Extended `scripts/validate-repo-quality-gates.sh` to compare
  `.kube-linter.yaml` exclusions, inline rationale comments, and README matrix
  rows.
- Recorded `VAL-SPC-006-052` and `T-249` through `T-253` in the existing 006
  Spec/Plan/Task chain.

#### Verification

- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
- `bash scripts/validate-gitops-structure.sh` — PASS.
- `bash scripts/validate-k8s-manifests.sh .` — PASS; optional
  `kube-linter` skipped locally because it is not installed.
- `bash scripts/check-secret-handling.sh .` — PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` — PASS.
- `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` — PASS.
- JSON parse for `.claude/settings.json` and `.codex/hooks.json` — PASS.
- Workflow YAML parse for `.github/workflows/*.yml` — PASS for 5 files.
- `.env.example` and `.env` key-name-only comparison — PASS for 18 keys.
- `git diff --check` — PASS.

#### Follow-up

- Keep kube-linter installation, mandatory local enforcement, CI failure-mode
  changes, and broader policy bundle work as separate follow-up work.

### 2026-05-26 — GitOps namespace ownership guardrail follow-up

- **Date**: 2026-05-26
- **Layer**: GitOps, validation, SDD
- **Status**: partial
- **Tags**: #gitops #validation #sdd

#### Progress

- Rechecked current `CreateNamespace=true` usage across root Application, apps
  ApplicationSet, and platform root Applications.
- Added `gitops/README.md` Namespace Ownership Matrix to connect current
  namespace creation fallback behavior with namespace owner manifests.
- Extended `scripts/validate-repo-quality-gates.sh` to compare
  `CreateNamespace=true` surfaces against the README matrix and
  `gitops/platform/namespaces` owner manifests.
- Recorded `VAL-SPC-006-051` and `T-243` through `T-248` in the existing 006
  Spec/Plan/Task chain.

#### Verification

- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
- `bash scripts/validate-gitops-structure.sh` — PASS.
- `bash scripts/validate-k8s-manifests.sh .` — PASS; optional
  `kube-linter` skipped locally because it is not installed.
- `bash scripts/check-secret-handling.sh .` — PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` — PASS.
- `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` — PASS.
- JSON parse for `.claude/settings.json` and `.codex/hooks.json` — PASS.
- Workflow YAML parse for `.github/workflows/*.yml` — PASS for 5 files.
- `.env.example` and `.env` key-name-only comparison — PASS for 18 keys.
- `git diff --check` — PASS.

#### Follow-up

- Keep actual sync option removal, AppProject `Namespace` allow-list changes,
  live reconciliation, bootstrap ordering changes, and Kubernetes desired-state
  semantics as separate follow-up work.

### 2026-05-26 — GitOps image and workload-kind policy scan guardrail follow-up

- **Date**: 2026-05-26
- **Layer**: GitOps, validation, SDD
- **Status**: partial
- **Tags**: #gitops #validation #sdd

#### Progress

- Rechecked the active image tag and workload-kind policy scan gap from the
  current worktree.
- Added `gitops/README.md` Workload Image and Kind Policy Matrix for active
  `gitops/workloads/*`, raw `gitops/platform/*` pod templates, and
  `examples/sample-app/*` placeholder boundaries.
- Extended `scripts/validate-repo-quality-gates.sh` to reject active
  workload/platform pod template images that use `latest` or lack an explicit
  tag/digest.
- Extended the same gate to compare active workload manifest kinds against the
  `apps` AppProject `namespaceResourceWhitelist`.
- Recorded `VAL-SPC-006-050` and `T-237` through `T-242` in the existing 006
  Spec/Plan/Task chain.

#### Verification

- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
- `bash scripts/validate-gitops-structure.sh` — PASS.
- `bash scripts/validate-k8s-manifests.sh .` — PASS; optional
  `kube-linter` skipped locally because it is not installed.
- `bash scripts/check-secret-handling.sh .` — PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` — PASS.
- `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` — PASS.
- JSON parse for `.claude/settings.json` and `.codex/hooks.json` — PASS.
- Workflow YAML parse for `.github/workflows/*.yml` — PASS for 5 files.
- `.env.example` and `.env` key-name-only comparison — PASS for 18 keys.
- `git diff --check` — PASS.

#### Follow-up

- Keep AppProject allow-list tightening, `CreateNamespace=true` ownership, CI
  failure-mode changes, OPA/Conftest, kube-linter enforcement, and live runtime
  mutation as separate follow-up work.

### 2026-05-26 — Targeted residual-area audit follow-up

- **Date**: 2026-05-26
- **Layer**: scripts, GitOps, infrastructure, operations, validation, SDD
- **Status**: partial
- **Tags**: #scripts #gitops #infrastructure #operations #validation #sdd

#### Progress

- Re-audited `scripts/`, `gitops/`, `infrastructure/`, and
  `docs/05.operations/` from the current worktree.
- Confirmed the remaining safe implementation is documentation/governance
  SSoT hardening, not Kubernetes semantic changes or script deletion.
- Added an operations mutation-boundary section to
  `docs/05.operations/README.md`.
- Aligned `scripts/README.md` with the broader high-risk command boundary
  checks already enforced by `scripts/validate-repo-quality-gates.sh`.
- Recorded external Traefik 443 proof as outside GitOps desired state and
  outside default `run-all.sh` ingress-nginx fallback proof.
- Recorded `VAL-SPC-006-049` and `T-231` through `T-236` in the existing 006
  Spec/Plan/Task chain.

#### Verification

- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
- `bash scripts/validate-gitops-structure.sh` — PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` — PASS.
- `bash scripts/validate-k8s-manifests.sh .` — PASS; optional
  `kube-linter` skipped locally because it is not installed.
- `bash scripts/check-secret-handling.sh .` — PASS.
- `bash infrastructure/tests/run-all.sh` — PASS with Traefik 443 enforcement
  skipped by default.
- `CHECK_TRAEFIK_443=true bash infrastructure/tests/verify-ingress-tls.sh` —
  EXPECTED FAIL: external Traefik endpoint is not reachable and Docker
  inventory has no separate external Traefik gateway container.

#### Follow-up

- Keep AppProject allow-list tightening, namespace ownership changes,
  image/workload-kind policy scans, OPA/Conftest, and external Traefik gateway
  runtime proof as separate follow-up work.

### 2026-05-26 — Traefik 443 runtime proof follow-up

- **Date**: 2026-05-26
- **Layer**: Traefik, Docker, ingress, TLS, validation, SDD
- **Status**: partial
- **Tags**: #traefik #docker #ingress #tls #validation #sdd

#### Progress

- Used the explicit approval for approval-gated items to run the optional
  Traefik 443 live proof.
- Confirmed default `run-all.sh` passes through the ingress-nginx fallback path.
- Ran `CHECK_TRAEFIK_443=true bash infrastructure/tests/verify-ingress-tls.sh`
  and confirmed the external Traefik endpoint is not reachable.
- Inspected Docker runtime and found no external Traefik gateway container in
  the current container inventory.
- Added a `traefik/README.md` note that this failure is a `hy-home.docker`
  gateway runtime/dynamic-config proof gap, not a k3d GitOps desired-state
  failure.
- Recorded `VAL-SPC-006-048` and `T-227` through `T-230` in the existing 006
  Spec/Plan/Task chain.

#### Verification

- `CHECK_TRAEFIK_443=true bash infrastructure/tests/verify-ingress-tls.sh` —
  FAIL: `Traefik 443 endpoint is not reachable (argocd.127.0.0.1.nip.io:443)`.
- `docker ps --format '{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'` —
  PASS for inventory capture; no external Traefik gateway container was
  running.
- `bash infrastructure/tests/run-all.sh` — PASS with Traefik 443 enforcement
  skipped by default.

#### Follow-up

- External gateway startup and dynamic-config application belong to
  `hy-home.docker` operations; do not create or mutate that runtime from this
  repository without a separate gateway maintenance pass.

### 2026-05-26 — Default kubeconfig TLS repair follow-up

- **Date**: 2026-05-26
- **Layer**: WSL2, k3d, Kubernetes, kubeconfig, validation, SDD
- **Status**: partial
- **Tags**: #wsl2 #k3d #kubernetes #kubeconfig #validation #sdd

#### Progress

- Used the explicit approval for approval-gated items to repair the local
  default kubeconfig TLS trust blocker.
- Backed up `~/.kube/config` before repair.
- Merged the k3d `hyhome` kubeconfig into the default kubeconfig and switched
  context to `k3d-hyhome`.
- Verified that default `kubectl` can now reach the API server.
- Ran the aggregate live validation with the default kubeconfig and proved it
  passes.
- Recorded `VAL-SPC-006-047` and `T-222` through `T-226` in the existing 006
  Spec/Plan/Task chain.

#### Verification

- Default kubeconfig backup — PASS:
  `~/.kube/config.codex-backup-20260526T-k3d-hyhome-tls-repair`.
- `k3d kubeconfig merge hyhome --kubeconfig-merge-default --kubeconfig-switch-context` — PASS.
- `kubectl config current-context` — PASS; current context is `k3d-hyhome`.
- `kubectl version --request-timeout=5s` — PASS with a kubectl
  client/server version-skew warning.
- `bash infrastructure/tests/run-all.sh` — PASS.

#### Follow-up

- Traefik 443 enforcement remains optional because `run-all.sh` skips it unless
  `CHECK_TRAEFIK_443=true` is set.
- Rollback is to restore the backup file to `~/.kube/config` if the local
  default kubeconfig must be reverted.

### 2026-05-26 — Temporary kubeconfig live validation follow-up

- **Date**: 2026-05-26
- **Layer**: WSL2, Docker, k3d, Kubernetes, ArgoCD, External Secrets, Vault, validation, SDD
- **Status**: partial
- **Tags**: #wsl2 #docker #k3d #kubernetes #argocd #external-secrets #vault #validation #sdd

#### Progress

- Used the explicit approval for approval-gated items to run read-only live
  runtime checks.
- Confirmed Docker context, running external-service containers, and the
  `hyhome` k3d cluster are present.
- Reproduced the default kubeconfig TLS blocker:
  `x509: certificate signed by unknown authority`.
- Generated a k3d kubeconfig under `/tmp` and used it only through the
  `KUBECONFIG` environment variable, without modifying `~/.kube/config`.
- Ran `infrastructure/tests/run-all.sh` with the temporary kubeconfig and
  proved the live aggregate checks pass.
- Recorded `VAL-SPC-006-046` and `T-217` through `T-221` in the existing 006
  Spec/Plan/Task chain.

#### Verification

- `docker context show` — PASS; context is `default`.
- `docker ps --format '{{.Names}}\t{{.Status}}\t{{.Ports}}'` — PASS; PostgreSQL,
  Vault, Valkey, and k3d containers were running.
- `k3d cluster list` — PASS; `hyhome` reported `1/1` server and `3/3` agents.
- `kubectl config current-context` — PASS; current context is `k3d-hyhome`.
- `kubectl version --request-timeout=5s` — BLOCKED for default kubeconfig with
  `x509: certificate signed by unknown authority`.
- `k3d kubeconfig get hyhome > /tmp/hy-home-k8s-k3d-hyhome.kubeconfig` — PASS.
- `KUBECONFIG=/tmp/hy-home-k8s-k3d-hyhome.kubeconfig kubectl version --request-timeout=5s` — PASS with a kubectl client/server version-skew warning.
- `KUBECONFIG=/tmp/hy-home-k8s-k3d-hyhome.kubeconfig bash infrastructure/tests/run-all.sh` — PASS.
- Temporary kubeconfig cleanup — PASS; `/tmp/hy-home-k8s-k3d-hyhome.kubeconfig`
  was removed after validation.

#### Follow-up

- Default kubeconfig TLS trust repair remains an operator-owned local runtime
  action; the temporary kubeconfig result proves live cluster health, not
  default kubeconfig repair.
- Traefik 443 enforcement remains optional because `run-all.sh` skips it unless
  `CHECK_TRAEFIK_443=true` is set.

### 2026-05-26 — Script classification matrix guardrail follow-up

- **Date**: 2026-05-26
- **Layer**: scripts, validation, SDD
- **Status**: partial
- **Tags**: #scripts #validation #sdd

#### Progress

- Rechecked the `scripts/` deletion/consolidation review evidence against the
  task-contract classification terms.
- Found that the 006 plan recorded script classifications, but
  `scripts/README.md` and the reusable repository quality gate did not enforce
  those terms as the scripts SSoT.
- Added a Script Classification Matrix covering every active `scripts/*.sh`
  file with current deletion and consolidation candidate state.
- Extended `scripts/validate-repo-quality-gates.sh` to validate the matrix
  header, row coverage, allowed classification terms, expected current
  classifications, and non-deletion/non-consolidation state.
- Recorded `VAL-SPC-006-045` and `T-212` through `T-216` in the existing 006
  Spec/Plan/Task chain.

#### Verification

- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- Targeted script classification matrix check — PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
- `bash scripts/validate-gitops-structure.sh` — PASS.
- `bash scripts/validate-k8s-manifests.sh .` — PASS; optional
  `kube-linter` remained unavailable, so this was YAML syntax validation.
- `bash scripts/check-secret-handling.sh .` — PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` — PASS.
- `git diff --check` — PASS.

#### Follow-up

- Keep actual script deletion, rename, or consolidation deferred until a
  separate task/plan proves reference checks, rollback, and replacement
  command contracts.

### 2026-05-26 — Docker network and RBAC create boundary guardrail follow-up

- **Date**: 2026-05-26
- **Layer**: docs/05.operations, WSL2, Docker, Kubernetes RBAC, validation, SDD
- **Status**: partial
- **Tags**: #operations #wsl2 #docker #kubernetes #rbac #validation #sdd

#### Progress

- Rechecked operations command boundary coverage for Docker network mutation
  and RBAC create examples.
- Found that `docker network connect` and `kubectl create clusterrolebinding`
  examples were not directly covered by the reusable command-boundary rule.
- Marked the WSL2/Vault Docker network connection example as human-approved
  bootstrap/break-glass work.
- Synced the touched guide frontmatter date and Stage 05 guides README index
  row to `2026-05-26`.
- Extended `scripts/validate-repo-quality-gates.sh` so Docker network mutation
  and `kubectl create clusterrolebinding` examples require approved context.
- Updated `scripts/README.md` command contract wording.
- Recorded `VAL-SPC-006-044` and `T-207` through `T-211` in the existing 006
  Spec/Plan/Task chain.

#### Verification

- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- Targeted Docker network/RBAC create boundary check — PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
- `git diff --check` — PASS.

#### Follow-up

- Keep actual Docker network changes, Kubernetes RBAC creation, and live
  cluster validation deferred to a separately approved runtime/bootstrap pass.

### 2026-05-26 — Vault policy write boundary guardrail follow-up

- **Date**: 2026-05-26
- **Layer**: docs/05.operations, Vault, External Secrets, validation, SDD
- **Status**: partial
- **Tags**: #operations #vault #external-secrets #validation #sdd

#### Progress

- Rechecked operations command boundary coverage for live or external secret
  mutation examples.
- Found that `vault kv put` examples were guarded, but `vault policy write`
  examples were not explicitly covered by the reusable command-boundary rule.
- Marked active app onboarding guide/runbook `vault policy write` examples as
  human-approved external secret policy changes.
- Synced the touched guide/runbook frontmatter dates and Stage 05 README index
  rows to `2026-05-26`.
- Extended `scripts/validate-repo-quality-gates.sh` so `vault policy write`
  examples require nearby external-secret, human-approved, operator-approved,
  or break-glass context.
- Updated `scripts/README.md` command contract wording.
- Recorded `VAL-SPC-006-043` and `T-202` through `T-206` in the existing 006
  Spec/Plan/Task chain.

#### Verification

- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- Targeted Vault policy write boundary check — PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
- `git diff --check` — PASS.

#### Follow-up

- Keep actual Vault policy writes, Vault auth changes, secret values, and live
  ESO/Vault validation deferred to a separately approved GitOps/secret-runtime
  pass.

### 2026-05-26 — App onboarding secret path contract guardrail follow-up

- **Date**: 2026-05-26
- **Layer**: docs/05.operations, examples, GitOps, External Secrets, validation, SDD
- **Status**: partial
- **Tags**: #operations #gitops #external-secrets #vault #validation #sdd

#### Progress

- Rechecked whether active app onboarding operations docs, the sample
  ExternalSecret, and GitOps secret responsibility docs consistently separate
  the Vault CLI path from the ESO `remoteRef.key` value.
- Clarified `gitops/README.md` sample app wording so `apps/<appname>/config`
  is explicitly the ESO remoteRef key and `secret/apps/<appname>/config` is the
  Vault CLI path.
- Extended `scripts/validate-repo-quality-gates.sh` so the active guide,
  policy, runbook, sample ExternalSecret, and GitOps README must preserve that
  distinction.
- Updated `scripts/README.md` command contract wording.
- Recorded `VAL-SPC-006-042` and `T-197` through `T-201` in the existing 006
  Spec/Plan/Task chain.

#### Verification

- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- Targeted app secret path contract check — PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
- `git diff --check` — PASS.

#### Follow-up

- Keep AppProject `ExternalSecret` allow-list semantics, Vault policy changes,
  secret values, and live ESO/Vault validation deferred to a separately
  approved GitOps/secret-runtime pass.

### 2026-05-26 — GitHub workflow responsibility matrix guardrail follow-up

- **Date**: 2026-05-26
- **Layer**: GitHub Actions, QA, CI/CD, validation, SDD
- **Status**: partial
- **Tags**: #github-actions #qa #cicd #validation #sdd

#### Progress

- Rechecked whether `.github/` workflow roles had a guarded SSoT tied to the
  actual workflow inventory.
- Added Workflow Responsibility Matrix to `.github/ABOUT.md`.
- Extended `scripts/validate-repo-quality-gates.sh` so every
  `.github/workflows/*.yml` file has an ABOUT matrix row with role,
  trigger/scope, evidence, and no-deploy/no-live-mutation boundary text.
- Updated `scripts/README.md` command contract wording.
- Recorded `VAL-SPC-006-041` and `T-192` through `T-196` in the existing 006
  Spec/Plan/Task chain.

#### Verification

- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- Workflow YAML parse for `.github/workflows/*.yml` — PASS; 5 workflow files
  parsed.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
- `git diff --check` — PASS.

#### Follow-up

- Keep workflow job topology, branch policy enforcement, publish behavior, and
  GitHub remote ruleset changes deferred to a separately approved CI policy
  pass.

### 2026-05-26 — Bootstrap boundary matrix guardrail follow-up

- **Date**: 2026-05-26
- **Layer**: infrastructure, bootstrap, GitOps, validation, SDD
- **Status**: partial
- **Tags**: #infrastructure #bootstrap #gitops #wsl2 #k3d #argocd #validation #sdd

#### Progress

- Rechecked whether k3d cluster creation, ArgoCD installation, root app
  application, Vault connection, and PostgreSQL/Valkey connection boundaries
  had a guarded SSoT.
- Added Bootstrap Boundary Matrix to `infrastructure/README.md`.
- Extended `scripts/validate-repo-quality-gates.sh` so bootstrap-only command
  surfaces, operator/external ownership, repo responsibilities, verification
  evidence, and fail-closed boundaries stay explicit.
- Updated `scripts/README.md` command contract wording.
- Recorded `VAL-SPC-006-040` and `T-187` through `T-191` in the existing 006
  Spec/Plan/Task chain.

#### Verification

- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` — PASS.
- `bash scripts/validate-gitops-structure.sh` — PASS.
- `bash scripts/validate-k8s-manifests.sh .` — PASS; optional
  `kube-linter` skipped locally because it is not installed.
- `bash scripts/check-secret-handling.sh .` — PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
- `git diff --check` — PASS.

#### Follow-up

- Keep cluster creation, ArgoCD installation, root app apply, Vault auth
  refresh, external runtime startup, and kubeconfig TLS repair deferred to an
  approved operator/runtime pass.

### 2026-05-26 — Secret management responsibility matrix guardrail follow-up

- **Date**: 2026-05-26
- **Layer**: GitOps, External Secrets, Vault, validation, SDD
- **Status**: partial
- **Tags**: #gitops #external-secrets #vault #secrets #validation #sdd

#### Progress

- Rechecked whether ESO, ClusterSecretStore, Vault auth, ExternalSecret target
  naming, owner boundaries, value-handling rules, and sample app secret
  enablement had a guarded SSoT.
- Added Secret Management Responsibility Matrix to `gitops/README.md`.
- Extended `scripts/validate-repo-quality-gates.sh` so the matrix protects
  `vault-backend`, platform PostgreSQL secret wiring, ArgoCD Valkey and
  notifications secrets, and the optional sample app ExternalSecret boundary.
- Updated `scripts/README.md` command contract wording.
- Recorded `VAL-SPC-006-039` and `T-182` through `T-186` in the existing 006
  Spec/Plan/Task chain.

#### Verification

- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` — PASS.
- `bash scripts/validate-gitops-structure.sh` — PASS.
- `bash scripts/validate-k8s-manifests.sh .` — PASS; optional
  `kube-linter` skipped locally because it is not installed.
- `bash scripts/check-secret-handling.sh .` — PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
- `git diff --check` — PASS.

#### Follow-up

- Keep Vault policy changes, secret value inspection, live Vault auth refresh,
  and kubeconfig TLS repair deferred to an approved runtime/security pass.

### 2026-05-26 — External service contract matrix guardrail follow-up

- **Date**: 2026-05-26
- **Layer**: GitOps, infrastructure, external services, validation, SDD
- **Status**: partial
- **Tags**: #gitops #infrastructure #external-services #vault #postgresql #valkey #validation #sdd

#### Progress

- Rechecked whether PostgreSQL, Valkey, and Vault interface contracts had a
  guarded SSoT for host/service, port, database or Vault path, secret keys,
  TLS/CA responsibility, rotation owner, namespace convention, and validation.
- Added External Service Contract Matrix to `gitops/README.md`.
- Extended `scripts/validate-repo-quality-gates.sh` so the matrix stays aligned
  with current static contract fields and ownership boundaries.
- Updated `scripts/README.md` command contract wording.
- Recorded `VAL-SPC-006-038` and `T-177` through `T-181` in the existing 006
  Spec/Plan/Task chain.

#### Verification

- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` — PASS.
- `bash scripts/validate-gitops-structure.sh` — PASS.
- `bash scripts/validate-k8s-manifests.sh .` — PASS; optional
  `kube-linter` skipped locally because it is not installed.
- `bash scripts/check-secret-handling.sh .` — PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
- `git diff --check` — PASS.

#### Follow-up

- Keep live PostgreSQL, Valkey, Vault, ESO, and kubeconfig TLS proof deferred
  until an approved runtime pass repairs the current live validation blocker.

### 2026-05-26 — WSL2 runtime prerequisite guardrail follow-up

- **Date**: 2026-05-26
- **Layer**: infrastructure, WSL2, validation, SDD
- **Status**: partial
- **Tags**: #infrastructure #wsl2 #docker #k3d #validation #sdd

#### Progress

- Rechecked whether WSL2, WSL-native Docker, k3d, kubectl, kubeconfig/TLS,
  local port, and WSL networking prerequisites had a single reusable SSoT.
- Added WSL2 Runtime Prerequisite Matrix to `infrastructure/README.md`.
- Extended `scripts/validate-repo-quality-gates.sh` so Docker context,
  `k3d-hyhome`, `kubectl config current-context`, kubeconfig/TLS trust,
  `x509: certificate signed by unknown authority`, current `172.18.x` service
  contracts, and WSL networking/Traefik ownership boundaries are validated.
- Kept the change repo-static. No Docker context, kubeconfig, k3d cluster,
  local port binding, external service, GitOps manifest, secret, CI job, or
  live runtime state was changed.
- Documented the guardrail as VAL-SPC-006-037 and T-172 through T-176 in the
  existing 006 SDD chain.

#### Memory

- Static WSL2 prerequisite checks should protect the documentation SSoT and
  failure boundaries only. Docker context switching, kubeconfig CA trust repair,
  Windows/WSL gateway state, and external service startup remain operator-owned
  runtime actions.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS; optional `kube-linter`
  skipped locally because it is not installed.
- `bash scripts/check-secret-handling.sh .` PASS.
- `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` PASS.
- JSON parse for `.claude/settings.json` and `.codex/hooks.json` PASS.
- Workflow YAML parse for `.github/workflows/*.yml` PASS.
- `.env.example` vs `.env` key-name-only comparison PASS; values were not
  printed.
- `git diff --check` PASS.

### 2026-05-26 — examples role matrix guardrail follow-up

- **Date**: 2026-05-26
- **Layer**: examples, validation, SDD
- **Status**: partial
- **Tags**: #examples #validation #sdd

#### Progress

- Rechecked whether `examples/README.md` and `examples/sample-app/README.md`
  had reusable validation coverage for the intended examples boundary.
- Added Example Role Matrix to keep `sample-app/` as the minimal local k3d
  GitOps onboarding template and `aws/` plus `azure/` as Cloud Example Snapshot
  references rather than provider-latest or live desired-state sources.
- Extended `scripts/validate-repo-quality-gates.sh` so the examples role
  matrix, sample-app minimal file set, sample-app/adminer reference boundary,
  and richer adminer reference files are validated.
- Kept the change repo-static. No sample manifest, cloud-reference manifest,
  GitOps workload, provider contract, live cluster state, secret, or CI job
  structure was changed.
- Documented the guardrail as VAL-SPC-006-036 and T-167 through T-171 in the
  existing 006 SDD chain.

#### Memory

- `examples/sample-app/` should stay a minimal copy-start template. Richer
  workload behavior belongs in active GitOps references such as
  `gitops/workloads/adminer/`, and cloud example folders should remain tied to
  the version inventory snapshot unless a separate provider refresh is done.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS; optional `kube-linter`
  skipped locally because it is not installed.
- `bash scripts/check-secret-handling.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` PASS.
- JSON parse for `.claude/settings.json` and `.codex/hooks.json` PASS.
- Workflow YAML parse for `.github/workflows/*.yml` PASS.
- `.env.example` vs `.env` key-name-only comparison PASS; values were not
  printed.
- `git diff --check` PASS.

### 2026-05-26 — scripts broad reference guardrail follow-up

- **Date**: 2026-05-26
- **Layer**: scripts, validation, SDD
- **Status**: partial
- **Tags**: #scripts #validation #sdd

#### Progress

- Rechecked whether the `scripts/` deletion and rename precheck had reusable
  validation coverage for broad `scripts/*.sh` references beyond the
  command-contract allowlist.
- Extended `scripts/validate-repo-quality-gates.sh` so tracked text references
  matching `scripts/*.sh` must point to existing script files.
- Updated `scripts/README.md` to keep three concepts separate: Tier A/B
  retention evidence, Tier C command/documentation surfaces, and broad
  dangling-reference safety checks.
- Kept the change repo-static. No script was deleted, renamed, consolidated, or
  reclassified; live cluster state, GitOps manifests, secrets, external service
  state, and CI job structure were not changed.
- Documented the guardrail as VAL-SPC-006-035 and T-162 through T-166 in the
  existing 006 SDD chain.

#### Memory

- The command-contract allowlist identifies maintained execution surfaces. The
  broad script-reference sweep is a deletion/rename safety net only; it should
  prevent dangling references without treating every historical or explanatory
  mention as Tier A/B retention evidence.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` PASS.
- tracked script reference spot check PASS; 183 tracked `scripts/*.sh`
  references resolved to existing files.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS; optional `kube-linter`
  skipped locally because it is not installed.
- `bash scripts/check-secret-handling.sh .` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` PASS.
- JSON parse for `.claude/settings.json` and `.codex/hooks.json` PASS.
- Workflow YAML parse for `.github/workflows/*.yml` PASS.
- `.env.example` vs `.env` key-name-only comparison PASS; values were not
  printed.
- `git diff --check` PASS.

### 2026-05-26 — operations incidents boundary guardrail follow-up

- **Date**: 2026-05-26
- **Layer**: operations docs, validation, SDD
- **Status**: partial
- **Tags**: #operations #incidents #validation #sdd

#### Progress

- Rechecked whether `docs/05.operations/incidents/README.md` had reusable
  validation coverage for incident record and postmortem routing beyond the
  stage-level Operations Routing Matrix.
- Added Incident Boundary Matrix to make incident record and postmortem path,
  template, creation, and current no-incident state explicit.
- Extended `scripts/validate-repo-quality-gates.sh` so incident and postmortem
  rows must match the canonical path rules and template links, creation rules
  must identify their intended use, and the current no-incident state must not
  accumulate placeholder directories.
- Kept the change repo-static. No incident record, postmortem, placeholder
  incident directory, live cluster state, GitOps manifest, secret policy,
  external service state, or CI job structure was created or changed.
- Documented the guardrail as VAL-SPC-006-034 and T-157 through T-161 in the
  existing 006 SDD chain.

#### Memory

- Stage-level operations routing and incidents boundary validation catch
  different drift classes. The stage matrix decides which bucket to use; the
  incidents matrix protects path/template creation rules and the no-incident
  placeholder boundary.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS; optional `kube-linter`
  skipped locally because it is not installed.
- `bash scripts/check-secret-handling.sh .` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` PASS.
- `git diff --check` PASS.

### 2026-05-26 — infrastructure coverage matrix guardrail follow-up

- **Date**: 2026-05-26
- **Layer**: infrastructure, validation, SDD
- **Status**: partial
- **Tags**: #infrastructure #validation #sdd

#### Progress

- Rechecked whether `infrastructure/README.md` Infrastructure Coverage Matrix
  had reusable validation coverage beyond the infrastructure test inventory
  guardrail.
- Added README wording that identifies the matrix-to-entrypoint synchronization
  contract for bootstrap and runtime-support infrastructure surfaces.
- Extended `scripts/validate-repo-quality-gates.sh` so Infrastructure Coverage
  Matrix rows must match actual `argocd/`, `k3d/`, `tests/`, `vault/`,
  `bootstrap-local.sh`, `ipaddresspool.yaml`, and `l2advertisement.yaml`
  entrypoints, name ownership, and cite validation or operation evidence.
- Kept the change repo-static. Bootstrap behavior, live cluster state,
  kubeconfig TLS trust, Kubernetes resource semantics, secrets, external
  service state, and CI job structure were not changed.
- Documented the guardrail as VAL-SPC-006-033 and T-152 through T-156 in the
  existing 006 SDD chain.

#### Memory

- Infrastructure coverage matrix validation and infrastructure test inventory
  validation catch different drift classes. The former protects entrypoint and
  ownership coverage; the latter protects test command lifecycle and live
  aggregate parity.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS; optional `kube-linter`
  skipped locally because it is not installed.
- `bash scripts/check-secret-handling.sh .` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` PASS.
- `git diff --check` PASS.

### 2026-05-26 — GitOps coverage matrix guardrail follow-up

- **Date**: 2026-05-26
- **Layer**: gitops, validation, SDD
- **Status**: partial
- **Tags**: #gitops #validation #sdd

#### Progress

- Rechecked whether `gitops/README.md` Service Coverage Matrix and
  `gitops/workloads/README.md` Workload Coverage Matrix had reusable validation
  coverage beyond the GitOps hierarchy validator.
- Added README wording that identifies the matrix-to-directory synchronization
  contract for platform and workload entrypoints.
- Extended `scripts/validate-repo-quality-gates.sh` so GitOps coverage matrix
  rows must match actual `clusters/local`, `apps/root`, `platform/*`, and
  `workloads/*` directories, include ownership text, and cite expected
  validation commands for workloads.
- Kept the change repo-static. Kubernetes resource semantics, AppProject
  permissions, ApplicationSet behavior, live cluster state, secrets, and CI job
  structure were not changed.
- Documented the guardrail as VAL-SPC-006-032 and T-147 through T-151 in the
  existing 006 SDD chain.

#### Memory

- GitOps hierarchy validation and README coverage validation catch different
  drift classes. The former protects ArgoCD ownership boundaries; the latter
  keeps the human/agent entrypoint synchronized with actual platform and
  workload directories.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS; optional `kube-linter`
  skipped locally because it is not installed.
- `bash scripts/check-secret-handling.sh .` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` PASS.
- `git diff --check` PASS.

### 2026-05-25 — operations routing matrix guardrail follow-up

- **Date**: 2026-05-25
- **Layer**: operations docs, validation, SDD
- **Status**: partial
- **Tags**: #operations #validation #sdd

#### Progress

- Rechecked whether `docs/05.operations/README.md` stage-level routing had a
  reusable validation target beyond the existing subfolder index/frontmatter
  guardrail.
- Added an explicit Operations Routing Matrix heading to the stage README so
  the routing table is targetable by the repository quality gate.
- Extended `scripts/validate-repo-quality-gates.sh` so required operations
  buckets, routing row order, target links, and template links are validated
  for guides, policies, runbooks, incident records, and postmortems.
- Kept the change structural. Authored operations content semantics, live
  cluster state, GitOps manifests, secrets, and CI job structure were not
  changed.
- Documented the guardrail as VAL-SPC-006-031 and T-142 through T-146 in the
  existing 006 SDD chain.

#### Memory

- `docs/05.operations` needs both subfolder index/frontmatter parity and
  stage-level bucket/template routing validation. They catch different drift
  classes.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `git diff --check` PASS.

### 2026-05-25 — Traefik route inventory guardrail follow-up

- **Date**: 2026-05-25
- **Layer**: traefik, validation, SDD
- **Status**: partial
- **Tags**: #traefik #validation #sdd

#### Progress

- Rechecked whether `traefik/*.yaml` route and backend contracts had reusable
  validation coverage beyond ad hoc stale-backend checks.
- Added Traefik Route Inventory to `traefik/README.md` with config filename,
  router host, backend URL, reference-only boundary, and validation surface.
- Extended `scripts/validate-repo-quality-gates.sh` so each Traefik dynamic
  config must match the README inventory for router host and backend URL, use
  `websecure`, define TLS, preserve service transport, and avoid stale backend
  references.
- Included `examples/sample-app/traefik-k3d.yaml.example` in the stale backend
  guardrail so onboarding examples stay aligned with the ingress-nginx
  `LoadBalancer` backend.
- Documented the guardrail as VAL-SPC-006-030 and T-137 through T-141 in the
  existing 006 SDD chain.

#### Memory

- Traefik dynamic configs are reference-only, but their host/backend contracts
  still need row-level repo-static validation because they bridge this GitOps
  workspace with the external `hy-home.docker` gateway.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS; optional `kube-linter`
  skipped locally because it is not installed.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `git diff --check` PASS.

### 2026-05-25 — infrastructure test inventory guardrail follow-up

- **Date**: 2026-05-25
- **Layer**: infrastructure, validation, SDD
- **Status**: partial
- **Tags**: #infrastructure #validation #sdd

#### Progress

- Rechecked whether `infrastructure/tests/*.sh` had row-level inventory and
  deletion/consolidation evidence comparable to the `scripts/` guardrail.
- Added Infrastructure Test Inventory to `infrastructure/README.md` with test
  type, preconditions, result semantics, and retention or command surface.
- Extended `scripts/validate-repo-quality-gates.sh` so infrastructure shell
  entrypoints must be executable, use the expected Bash shebang, and have exact
  inventory coverage for `infrastructure/tests/*.sh`.
- Added `run-all.sh` parity validation so every test marked `Live` in the
  inventory is called by the live aggregate and the aggregate does not call
  unlisted live tests.
- Documented the guardrail as VAL-SPC-006-029 and T-132 through T-136 in the
  existing 006 SDD chain.

#### Memory

- Infrastructure test review should preserve both static/live separation and
  row-level command contracts. `run-all.sh` parity is the cheap repo-static
  guardrail for live test inventory drift.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` PASS.
- `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `git diff --check` PASS.

### 2026-05-25 — GitOps hierarchy guardrail follow-up

- **Date**: 2026-05-25
- **Layer**: gitops, scripts, validation, SDD
- **Status**: partial
- **Tags**: #gitops #validation #sdd

#### Progress

- Rechecked whether `scripts/validate-gitops-structure.sh` protected the
  current root Application, platform App-of-Apps, and workload ApplicationSet
  responsibility split.
- Extended `scripts/validate-gitops-structure.sh` so `root-platform` must own
  `gitops/apps/root`, `apps-generator` must own `gitops/workloads/*`, required
  `gitops/clusters/local` resources must remain present, root app manifests
  must use the `platform` project, and local source paths must stay under
  `gitops/platform/` or `gitops/clusters/local`.
- Updated `gitops/README.md` and `scripts/README.md` so the executable command
  contract names the hierarchy guardrail.
- Documented the guardrail as VAL-SPC-006-028 and T-127 through T-131 in the
  existing 006 SDD chain.

#### Memory

- GitOps hierarchy validation should check the concrete root/ApplicationSet
  ownership contract, not only manifest kind and kustomization parseability.

#### Evidence

- `bash scripts/validate-gitops-structure.sh` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS; optional `kube-linter`
  skipped locally because it is not installed.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash -n scripts/validate-gitops-structure.sh` PASS.
- `git diff --check` PASS.

### 2026-05-25 — environment key contract guardrail follow-up

- **Date**: 2026-05-25
- **Layer**: environment, scripts, validation, SDD
- **Status**: partial
- **Tags**: #env #validation #sdd

#### Progress

- Rechecked whether `.env.example` and local `.env` key-name-only comparison
  had reusable validation coverage.
- Extended `scripts/validate-repo-quality-gates.sh` so `.env` must remain
  ignored and untracked, `.env.example` must exist with unique keys, and local
  `.env` keys must match `.env.example` when `.env` exists.
- Kept the check key-only. Values are not printed or recorded, and `.env`
  absence in CI-capable contexts does not fail the gate.
- Documented the guardrail as VAL-SPC-006-027 and T-122 through T-126 in the
  existing 006 SDD chain.

#### Memory

- Environment validation can be promoted into repo quality only when it remains
  key-name-only and preserves the ignored/untracked `.env` contract.

#### Evidence

- Env key-only guardrail targeted check PASS with `.env.example` keys=18 and
  local `.env` keys=18.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` PASS.
- `git diff --check` PASS.

### 2026-05-25 — scripts inventory guardrail follow-up

- **Date**: 2026-05-25
- **Layer**: scripts, validation, SDD
- **Status**: partial
- **Tags**: #scripts #validation #sdd

#### Progress

- Rechecked whether the `scripts/` deletion/consolidation review had
  validation strong enough to prevent future drift.
- Extended `scripts/validate-repo-quality-gates.sh` so each tracked shell
  script must be executable, start with the expected Bash shebang, and have
  exactly one `scripts/README.md` inventory row.
- The scripts inventory row must now include an allowed decision and non-empty
  retention evidence, command/documentation surface, and purpose. A `Keep`
  decision must cite Tier A or Tier B retention evidence.
- Documented the guardrail as VAL-SPC-006-026 and T-117 through T-121 in the
  existing 006 SDD chain.

#### Memory

- For `scripts/`, checking that a filename appears somewhere in the README is
  weaker than checking the inventory row and retention tier. Future script
  deletion or consolidation work should preserve the row-level contract.

#### Evidence

- Scripts inventory guardrail targeted check PASS.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` PASS.
- `git diff --check` PASS.

### 2026-05-25 — operations index guardrail follow-up

- **Date**: 2026-05-25
- **Layer**: operations docs, scripts, validation
- **Status**: partial
- **Tags**: #operations #validation #sdd

#### Progress

- Rechecked `docs/05.operations/{guides,policies,runbooks}` README index rows
  against document frontmatter.
- Aligned stale final-updated rows for superseded guide/runbook entries and
  policy entries whose frontmatter had newer `updated` dates.
- Extended `scripts/validate-repo-quality-gates.sh` so guides, policies, and
  runbooks README indexes must cover all sibling documents, avoid stale links,
  and match each document's `status` and `updated` frontmatter.
- Documented the guardrail as VAL-SPC-006-025 and T-112 through T-116 in the
  existing 006 SDD chain.

#### Memory

- `docs/05.operations` freshness is not just whether a file exists in an index.
  The index status and final-updated cells must match the document frontmatter.

#### Evidence

- Operations index/frontmatter sync targeted check PASS.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` PASS.
- `git diff --check` PASS.

### 2026-05-25 — residual objective completion audit

- **Date**: 2026-05-25
- **Layer**: docs, governance, examples, env, qa, ci, skills, runtime-boundary
- **Status**: partial
- **Tags**: #sdd #governance #verification #runtime-boundary

#### Progress

- Rechecked broad objective axes that were outside the explicit four-path
  follow-up: `traefik/`, `examples/`, `.env` key parity, QA/CI, agent
  governance, repo-local Skills, bootstrap, WSL2/Docker prerequisites,
  secret-management responsibility, external-service contracts, and
  documentation SSoT ownership.
- Added VAL-SPC-006-024 and T-107 through T-111 to the existing 006 SDD chain
  instead of creating a parallel task tree.
- Kept this pass evidence-only. No Kubernetes resource semantics, AppProject
  permissions, CI job structure, secret policy, live cluster state, or `.env`
  values were changed.

#### Memory

- When a broad workspace objective has already been represented in a large
  overlay, add a residual matrix only for genuinely weak proof areas; do not
  restart the full audit or duplicate the task tree.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS for YAML syntax; optional
  `kube-linter` skipped locally.
- `bash scripts/check-secret-handling.sh .` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- Shell syntax for `infrastructure`, `scripts`, and `.claude/hooks` PASS.
- Workflow YAML parse for `.github/workflows/*.yml` PASS for 5 files.
- `.env.example` vs `.env` key-name-only comparison PASS with missing=0,
  extra=0, and 18 keys each; values were not printed or inspected.
- Targeted residual content checks PASS for Traefik backend, sample/adminer
  wording, version inventory wording, JIT/progress routing, `doc-writer`, and
  Skill descriptions.
- `git diff --check` PASS.
- `bash infrastructure/tests/run-all.sh` remains BLOCKED by kubeconfig TLS
  trust: `x509: certificate signed by unknown authority`.

### 2026-05-25 — unreviewed-area follow-up for scripts/gitops/infrastructure/operations

- **Date**: 2026-05-25
- **Layer**: scripts, gitops, infrastructure, operations docs, qa
- **Status**: partial
- **Tags**: #scripts #gitops #infrastructure #operations #validation

#### Progress

- Rechecked the objective for areas where the prior overlay could have been too
  broad or weakly evidenced, focusing on `scripts/`, `gitops/`,
  `infrastructure/`, and `docs/05.operations/`.
- Updated `scripts/README.md` so the script inventory/deletion review reflects
  the 2026-05-25 state and the repo quality gate's canonical JIT runtime
  contract check.
- Added a `gitops/README.md` current hardening deferrals section for AppProject
  allow-list minimization, `CreateNamespace=true` ownership, and future
  image/workload policy scans without changing manifests.
- Improved `infrastructure/tests/verify-cluster.sh` so a kubeconfig TLS trust
  failure reports the `x509: certificate signed by unknown authority` blocker
  directly, and documented that boundary in `infrastructure/README.md`.
- Updated the modified GitHub app onboarding guide/runbook `updated` metadata
  and their `docs/05.operations` README index rows to `2026-05-25`.
- Added VAL-SPC-006-023 and T-101 through T-106 to the existing 006 SDD chain.

#### Memory

- After content edits under `docs/05.operations`, check both document
  frontmatter and the owning subfolder README index before claiming the
  operations stage is aligned.
- Live validation failure messages are part of the operator contract. If a
  known blocker is TLS trust, prefer a precise diagnostic over a generic
  kubeconfig/context message.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS for YAML syntax; optional
  `kube-linter` skipped locally.
- `bash scripts/check-secret-handling.sh .` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- Shell syntax for `infrastructure`, `scripts`, and `.claude/hooks` PASS.
- Targeted operations metadata/index and follow-up content checks PASS.
- `git diff --check` PASS.
- `bash infrastructure/tests/run-all.sh` remains BLOCKED, now with explicit
  kubeconfig TLS trust output: `x509: certificate signed by unknown authority`.

### 2026-05-25 — documentation/governance-first workspace improvement

- **Date**: 2026-05-25
- **Layer**: docs, governance, examples, skills, qa
- **Status**: partial
- **Tags**: #sdd #governance #gitops #wsl2 #skills #validation

#### Progress

- Implemented the approved documentation/governance-first plan in the existing
  006 SDD chain instead of creating a parallel task tree.
- Added VAL-SPC-006-022 and T-091 through T-100 to record baseline instruction
  review, six fresh read-only subagent results, P0-01 through P0-22 coverage,
  Integrated Gap Analysis, Implementation Plan, Checklist Gate, and Final
  Report.
- Normalized JIT shorthand so agent/provider/rule docs include the
  `progress.md` step.
- Clarified that agents and subagents do not mutate live clusters by default;
  human-approved bootstrap or break-glass actions are operator-bound and must
  record scope, rollback, and verification evidence.
- Narrowed `doc-writer` runtime wording to template/routing and delegated stage
  document updates.
- Aligned `examples/sample-app/traefik-k3d.yaml.example` with the current
  ingress-nginx LoadBalancer backend `172.18.0.240:443`.
- Reworded onboarding docs so `examples/sample-app` is a minimal onboarding
  template and `gitops/workloads/adminer` is the fuller active reference
  pattern.
- Normalized cloud example wording to the current Tech Stack Version Inventory
  `Cloud Example Snapshot` instead of asserting a refreshed latest-provider
  claim.
- Updated existing repo-local Skill frontmatter descriptions to trigger-style
  `Use when...` wording and deferred the seven duplicate candidate
  workspace-specific agents/skills.
- Synced only the existing ignored `.agents/skills/**` mirrors for the Skill
  files changed in this pass because the repo quality gate treats present local
  mirrors as parity-checked convenience copies; broader `.agents` cleanup
  remains deferred.

#### Memory

- For broad workspace improvement prompts, prefer extending the active 006 SDD
  chain when the work is a current-state overlay for the same harness/system
  objective.
- Keep `.claude/skills/**` canonical. Do not create duplicate local agent or
  Skill surfaces unless the harness matrix first records a concrete gap that an
  existing surface cannot close.
- Treat live `kubectl` TLS trust repair as runtime work, not a docs/governance
  cleanup. Record the blocker and defer repair unless the human approves a live
  runtime pass.

#### Evidence

- Verification is recorded in the linked 006 plan/task overlay.
- Live `infrastructure/tests/run-all.sh` remains blocked in this pass by
  kubeconfig TLS trust: `x509: certificate signed by unknown authority`.

### 2026-05-25 — live bootstrap runtime closure

- **Date**: 2026-05-25
- **Layer**: runtime, gitops, docs, qa
- **Status**: complete
- **Tags**: #runtime #bootstrap #gitops #vault #validation

#### Progress

- Continued after PR #40 was merged into `main` and created
  `codex/live-bootstrap-runtime-closure` for forward-only follow-up work.
- Started the approved local runtime dependencies for verification: k3d
  `hyhome`, Vault, Valkey, PostgreSQL router, and required PostgreSQL cluster
  dependencies. Secret values were not printed.
- Fixed live bootstrap blockers found during the run:
  - MetalLB `0.16.0` needed explicit
    `frr-k8s.prometheus.serviceMonitor.enabled=false` and a 300s wait timeout
    for cold image pulls.
  - ArgoCD excludes EndpointSlice resources, so bootstrap must initialize all
    external-service `Service` and `EndpointSlice` objects before ESO/Vault
    validation.
  - Vault Kubernetes auth needed the current k3d reviewer JWT/CA and a
    GitOps-owned `system:auth-delegator` ClusterRoleBinding for the
    `external-secrets` serviceAccount.
  - Live TLS validation must use ingress-nginx `LoadBalancer` IP with
    host/SNI resolve by default; external Traefik host 443 remains optional
    runtime proof.
- Updated the 006 Spec/Plan/Task chain with VAL-SPC-006-021 and T-084 through
  T-090.

#### Memory

- For this repo's current k3d + MetalLB topology, external Traefik dynamic
  config should target ingress-nginx `LoadBalancer` IP `172.18.0.240:443`,
  not the k3d serverlb DNS backend.
- EndpointSlice desired state remains in `gitops/platform/external-services/`,
  but ArgoCD exclusion means bootstrap or human-approved break-glass must apply
  those EndpointSlices in the live cluster.
- Vault Kubernetes auth can show `token_reviewer_jwt_set=True` and still fail
  after cluster recreation if the reviewer token/CA is stale or the reviewer
  serviceAccount lacks TokenReview permission.

#### Evidence

- `infrastructure/bootstrap-local.sh` PASS.
- Vault Kubernetes login metadata check returned HTTP `200`; tokens were not
  printed.
- `kubectl auth can-i create tokenreviews.authentication.k8s.io --as system:serviceaccount:external-secrets:external-secrets` PASS.
- `bash infrastructure/tests/verify-secrets.sh` PASS.
- `bash infrastructure/tests/run-all.sh` PASS.
- Repo-static validation bundle PASS: repo quality gate, LLM Wiki check, GitOps
  structure, Kubernetes manifest syntax, secret handling, static contracts,
  shell syntax, JSON parse, workflow/Traefik YAML parse, env key-name-only
  comparison, and `git diff --check`.
- 006 Spec/Plan/Task include VAL-SPC-006-021 and T-084 through T-090.

#### Handoff

- External Traefik gateway runtime proof with `CHECK_TRAEFIK_443=true` remains a
  separate approved run because this closure did not start or mutate the
  external gateway service.

---

### 2026-05-25 — post-merge completion audit

- **Date**: 2026-05-25
- **Layer**: ci, docs, runtime
- **Status**: partial
- **Tags**: #ci #github #validation #runtime

#### Progress

- Confirmed PR #39 was merged into `main` at `2026-05-25T04:28:51Z` with merge
  commit `780fb7601e51ec534a11bca9a4b645d86bf6e470`.
- Fast-forwarded local `main` to the merge commit and deleted the merged local
  branch `codex/approval-bound-completion-audit`.
- Re-ran merged-main repo-static verification: repo quality gate, LLM Wiki
  check, GitOps structure, Kubernetes manifest syntax, secret handling,
  infrastructure static contracts, shell syntax, JSON parse, workflow YAML
  parse, env key-name-only comparison, and diff whitespace checks passed.
- Rechecked live runtime without printing secrets. Docker context is `default`,
  but no Docker containers or k3d clusters are running and the `k3d-hyhome`
  Kubernetes API still refuses connection.
- Ran no-secret-output bootstrap prechecks. Required commands, inotify, ports,
  and certificate files are ready, and `VAULT_TOKEN` is set. Vault health,
  PostgreSQL write/read, and Valkey connectivity are currently unavailable.

#### Memory

- PR #39 is no longer a blocker; merged `main` is the repo-static SSoT.
- Live bootstrap is not ready merely because `VAULT_TOKEN` is set. External
  Vault, PostgreSQL, and Valkey connectivity must pass before running
  `infrastructure/bootstrap-local.sh`.

#### Evidence

- `gh pr view 39` reports state `MERGED`.
- `gh run list --branch main` reports success for merge commit `780fb76`.
- `git status --short --branch` reports clean `main...origin/main`.
- 006 Spec/Plan/Task include VAL-SPC-006-020 and T-081 through T-083.

#### Handoff

- Start the external service stack that owns Vault, PostgreSQL, and Valkey;
  then rerun `infrastructure/bootstrap-local.sh` and
  `infrastructure/tests/run-all.sh` for live proof.
- Continue to avoid printing secret values in command output or reports.

---

### 2026-05-25 — approval-bound evidence refresh

- **Date**: 2026-05-25
- **Layer**: ci, docs
- **Status**: complete
- **Tags**: #ci #github #validation #evidence

#### Progress

- Rechecked PR #39 after the approval-bound audit branch updates.
- Confirmed PR #39 is open, mergeable, non-draft, and has passing checks for
  `ci-summary`, `pre-commit`, `repo-quality-static`, `branch-policy`,
  `changes`, `label`, and GitGuardian.
- Corrected the 006 Plan/Task PR check evidence to remove the stale `greeting`
  check name, which is not present in the current GitHub check rollup.

#### Memory

- Treat PR check evidence as current-state data. Re-run `gh pr view ...` before
  copying check names into authored SSoT artifacts.

#### Evidence

- `gh pr view 39 --json number,state,isDraft,mergeable,statusCheckRollup` PASS.
- 006 Task includes T-080 for this evidence refresh.

#### Handoff

- PR #39 still requires normal protected-branch handling before the branch can
  become the `main` SSoT.

---

### 2026-05-25 — approval-bound completion audit

- **Date**: 2026-05-25
- **Layer**: ci, qa, docs, runtime
- **Status**: complete
- **Tags**: #ci #github #runtime #validation #version-inventory

#### Progress

- Added VAL-SPC-006-019 plus T-076 through T-079 to the existing 006 SDD
  chain for the approval-bound completion audit.
- Re-ran approved read-only live checks. Docker context is `default`, no Docker
  containers are running, no k3d clusters are listed, and the `k3d-hyhome`
  Kubernetes API at `https://0.0.0.0:6550` refuses connection.
- Queried GitHub remote state. The repository has no rulesets returned by the
  rulesets API; main branch protection requires `ci-summary`, has PR review
  settings with zero required approvals, disables force-push/deletion, and does
  not enforce admins.
- Confirmed latest main commit `d8b9c19` has successful CI, including
  `ci-summary`.
- Found Dependabot PR #38 failing because `actions/stale` changed to `v10.2.0`
  without the matching version inventory update.
- Updated `.github/workflows/stale.yml` and
  `docs/90.references/data/tech-stack-version-inventory.md` together to
  `actions/stale@v10.2.0` on a `codex/` branch instead of bypassing `main`.
- Opened replacement PR #39 and confirmed its remote CI passed, including
  `ci-summary`, `pre-commit`, `repo-quality-static`, and `branch-policy`.
- Closed PR #38 as superseded by PR #39 to remove the stale failing duplicate.

#### Memory

- Branch protection, not repository rulesets, is the current remote policy SSoT
  for `main`.
- `ci-summary` is the required status check; direct pushes by admins can bypass
  PR routing but should not be used for normal follow-up work.
- Live runtime proof remains a current-state limitation when Docker has no
  running containers and k3d has no cluster rows.

#### Evidence

- 006 Spec/Plan/Task include the approval-bound completion audit overlay.
- `gh run view` for `d8b9c19` shows successful main CI.
- `gh pr view 38` and `gh run view 26363778043 --job 77603867367 --log` show
  the open Dependabot PR failure and `actions/stale` version drift.

#### Handoff

- PR #39 should be merged through the normal protected branch path; do not
  repeat direct `main` bypass for this follow-up.
- Do not inspect secret values, run Vault KV reads/writes, force ArgoCD sync, or
  run cluster mutation commands as part of this audit.

---

### 2026-05-25 — task-unit commit follow-up

- **Date**: 2026-05-25
- **Layer**: meta, docs, qa
- **Status**: complete
- **Tags**: #git #governance #validation #commit-discipline

#### Progress

- Added VAL-SPC-006-018 plus T-071 through T-075 to the existing 006 SDD
  chain for the task-unit commit follow-up.
- Recorded published commit `870febd` as a forward-only historical exception:
  it bundled authored SSoT overlay, deferred repo-static overlay, and lifecycle
  hook work after reaching `origin/main`.
- Preserved public history by avoiding reset, rebase, amend, and force-push.
- Strengthened lifecycle hook guidance so future dirty states that span
  multiple SDD overlays, runtime docs, hooks, validators, or env contracts are
  split before commit.
- Extended the repo quality gate to check the stronger Stop and PreCompact
  task-unit commit guidance.

#### Memory

- If a broad commit is already published on a shared branch, do not rewrite it
  for cleanup without explicit approval; record the exception and use a
  forward-only corrective commit.
- Future human-requested commits should stage only one logical task/spec unit at
  a time and review `git diff --cached` before each commit.

#### Evidence

- Spec 006 includes VAL-SPC-006-018.
- The linked 006 Plan includes the Task-Unit Commit Follow-up Overlay.
- The linked 006 Task tracks T-071 through T-075.
- `.claude/hooks/lifecycle-guard.sh` and
  `scripts/validate-repo-quality-gates.sh` carry the stronger guidance and
  self-test coverage.

#### Handoff

- This follow-up is one logical corrective task and should be committed as one
  forward-only Conventional Commit.
- No live runtime proof, secret value review, reset, rebase, amend, or
  force-push is part of this work.

---

### 2026-05-25 — lifecycle hook task-unit commit advisory

- **Date**: 2026-05-25
- **Layer**: meta, qa
- **Status**: complete
- **Tags**: #hooks #git #validation #commit-discipline

#### Progress

- Added task-unit commit discipline guidance to `.claude/hooks/lifecycle-guard.sh`
  for Stop/SubagentStop and PreCompact events.
- Kept the hook non-mutating: it does not stage files, create commits, or bypass
  human approval; it advises logical task/spec-unit commits when commits are
  requested.
- Extended `scripts/validate-repo-quality-gates.sh` lifecycle hook simulation so
  the task-unit commit advisory remains covered by repo quality gates.
- Updated `.claude/CLAUDE.md`, `docs/00.agent-governance/harness-catalog.md`,
  and `docs/00.agent-governance/rules/git-workflow.md` to describe the shared
  hook behavior.

#### Memory

- Shared hooks may remind agents to split commits by task unit, but they must
  not auto-commit or stage files.
- If repo-changing work intentionally remains uncommitted, the final response
  should name the files and reason.

#### Evidence

- `.claude/hooks/lifecycle-guard.sh` emits task-unit commit discipline advisory
  output for tracked dirty state.
- `scripts/validate-repo-quality-gates.sh` checks the advisory phrase in Stop
  and PreCompact payload simulations.

#### Handoff

- Actual commits remain explicit user-requested work and must follow the
  repository's Conventional Commit and task-unit staging rules.

---

### 2026-05-25 — deferred item repo-static improvement overlay

- **Date**: 2026-05-25
- **Layer**: docs, ops, qa, meta
- **Status**: complete
- **Tags**: #docs #gitops #operations #validation #deferred

#### Progress

- Reused the existing 006 Spec/Plan/Task chain and added VAL-SPC-006-017 plus
  T-063 through T-070 for deferred item repo-static improvements.
- Clarified EndpointSlice desired-state ownership versus human-approved
  break-glass patch/apply boundaries.
- Separated external Traefik backend wording from direct host fallback checks.
  VAL-SPC-006-021 later superseded the backend target with ingress-nginx
  `LoadBalancer` IP evidence.
- Aligned operations policy wording with current CI job names and recorded that
  OPA/Conftest remains deferred until owner, bundle, install path, and failure
  semantics exist.
- Documented Vault endpoint roles without adding or removing `.env.example`
  keys.
- Added script deletion precheck rules for broad reference sweep, task linkage,
  and rollback evidence.
- Kept `.claude/skills/**` canonical and `.agents/**` as ignored local mirror;
  no skill file movement or deletion was performed.

#### Memory

- For deferred-item follow-ups, split repo-static wording fixes from live proof,
  remote ruleset review, secret value review, and actual deletion/consolidation.
- Traefik backend port and direct fallback port are different contracts. This
  entry is historical; current backend target is maintained by VAL-SPC-006-021
  as ingress-nginx `LoadBalancer` IP `172.18.0.240:443`.
- OPA/Conftest should not become a required gate without a named policy owner,
  policy bundle location, installation contract, and failure semantics.

#### Evidence

- `docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md`
  includes the deferred item repo-static improvement overlay.
- `docs/04.execution/tasks/2026-05-24-workspace-harness-gap-analysis.md`
  tracks T-063 through T-070.
- `docs/05.operations/policies/0002-wsl2-k3d-gitops-ha-operations-policy.md`,
  `gitops/README.md`, `traefik/README.md`, `.env.example`, and
  `scripts/README.md` carry the repo-static wording updates.

#### Handoff

- Live runtime proof, secret value review, remote GitHub ruleset/SHA policy, and
  actual script deletion or `.agents` consolidation remain separate
  approval-bound work.

---

### 2026-05-25 — authored SSoT large-scale overlay

- **Date**: 2026-05-25
- **Layer**: docs, meta, qa
- **Status**: complete
- **Tags**: #docs #sdd #p0 #traceability

#### Progress

- Added exact `P0-01` through `P0-22` traceability to the existing 006 Plan
  instead of creating a parallel SDD bundle.
- Added VAL-SPC-006-016 and T-058 through T-062 for authored SSoT large-scale
  overlay evidence.
- Marked earlier overlapping verification evidence as historical and kept one
  current verification summary in the 006 Task.
- Added reciprocal P3 GitOps Secret Runtime Remediation links from the 006 Plan
  and Task.
- Recorded six subagent-derived SSoT gaps for future scoped work without
  changing runtime, secret, CI ruleset, or GitOps semantics.

#### Memory

- For large workspace prompts, preserve the human-facing P0 IDs in the existing
  006 chain even when repo-local task IDs already exist.
- Treat `.claude/skills/**` as the skill SSoT; `.agents/**` remains local or
  ignored until owner-reviewed consolidation.
- Script deletion requires broad `rg` reference checks in addition to the
  command-contract allowlist.

#### Evidence

- `docs/03.specs/006-workspace-harness-gap-analysis/spec.md` includes
  VAL-SPC-006-016.
- `docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md`
  includes the authored SSoT large-scale overlay and P0 crosswalk.
- `docs/04.execution/tasks/2026-05-24-workspace-harness-gap-analysis.md`
  tracks T-058 through T-062.

#### Handoff

- Live runtime proof, secret value review, CI ruleset/SHA policy, EndpointSlice
  ownership semantics, Traefik wording, Vault endpoint role notes,
  OPA/Conftest feasibility, and `.agents` consolidation remain follow-up items.

---

### 2026-05-25 — P0 mandatory workspace revalidation overlay

- **Date**: 2026-05-25
- **Layer**: docs, infra, qa, meta
- **Status**: complete
- **Tags**: #governance #docs #validation #gitops #p0

#### Progress

- Reused the existing `006-workspace-harness-gap-analysis` Spec/Plan/Task as
  the canonical SDD artifact set.
- Ran a fresh P0 baseline, full target inventory, and five read-only subagent
  reviews across documentation lifecycle, agent governance, scripts, GitOps and
  infrastructure, and environment/QA/CI.
- Recorded P0 status, coverage, gap analysis, implementation plan, and final
  report skeleton in the linked plan.
- Implemented only safe P1/P2 items: 006 Plan/Task README currentness, preserved
  Hybrid reviewer historical framing, GitOps validator no-arg contract, and
  Codex provider resolution clarification.
- Restored executable mode for `infrastructure/tests/verify-ingress-tls.sh`
  after the required script executability gate found it non-executable.
- Deferred live runtime proof, secret values, CI rulesets/SHA policy, semantic
  Kubernetes/GitOps changes, and deletion/consolidation candidates.

#### Memory

- Future P0 refreshes should append current-state overlays to Spec 006 instead
  of creating a parallel docs tree.
- Keep `.env` reviews key-name-only unless a human explicitly approves secret
  value inspection outside agent output.
- Treat deletion and consolidation candidates as reference-check work, not as a
  default cleanup action.

#### Evidence

- `docs/03.specs/006-workspace-harness-gap-analysis/spec.md` includes
  VAL-SPC-006-015.
- `docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md`
  includes the 2026-05-25 P0 Mandatory Workstream Revalidation overlay.
- `docs/04.execution/tasks/2026-05-24-workspace-harness-gap-analysis.md`
  tracks T-049 through T-057.

#### Handoff

- Repo-static verification passed. Remaining work is P3: live runtime proof,
  secret value review, CI ruleset/SHA policy, semantic GitOps changes, and
  deletion/consolidation after reference checks.

---

### 2026-05-25 — multi-area workspace improvement overlay

- **Date**: 2026-05-25
- **Layer**: docs, infra, qa, meta
- **Status**: complete
- **Tags**: #governance #docs #validation #gitops #qa

#### Progress

- Implemented the approved P1/P2 overlay against the existing
  `006-workspace-harness-gap-analysis` Spec/Plan/Task artifacts.
- Corrected Spec/Plan/Task README currentness drift so completed repo
  desired-state P3 work is no longer shown as still active, while live runtime
  proof remains follow-up.
- Hardened `scripts/check-secret-handling.sh` so quoted literal sensitive
  manifest values are detected and findings redact the value.
- Clarified `.claude/hooks/post-validate.sh` and `.claude/hooks/lifecycle-guard.sh`
  manifest path matching without changing hook behavior.
- Recorded deletion, consolidation, and P3 semantic/runtime items as deferred;
  no bulk deletion, live mutation, secret value inspection, or CI policy rewrite
  was performed.

#### Memory

- For future `hy-home.k8s` refreshes, keep P3 historical rows honest by adding
  current-state overlays instead of rewriting old evidence.
- Secret scanning changes should include a negative fixture that proves quoted
  literal values fail and quoted placeholders remain allowed.
- Bash `case` globs in these hooks intentionally match nested paths through
  `*`; do not narrow them without comparing CI path-filter scope.

#### Evidence

- `docs/03.specs/006-workspace-harness-gap-analysis/spec.md` includes
  VAL-SPC-006-014.
- `docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md`
  includes the 2026-05-25 Multi-Area Workspace Improvement Overlay.
- `docs/04.execution/tasks/2026-05-24-workspace-harness-gap-analysis.md`
  tracks T-044 through T-048 and the overlay verification summary.
- Verification bundle passed after final rerun; optional `kube-linter` remains
  skipped by the manifest validator because it is not installed locally.

#### Handoff

- Remaining P3 work requires separate approval and prechecks: live runtime
  proof, secret value review, CI rulesets/SHA-pinning policy, and Kubernetes or
  Vault semantic changes.

---

### 2026-05-24 — docs-stage conformance skill creation

- **Date**: 2026-05-24
- **Layer**: docs, meta, skills
- **Status**: complete
- **Tags**: #governance #skills #docs #validation #memory

#### Progress

- Reviewed current task evidence and Codex memory for repeated workflow
  candidates.
- Selected the recurring docs-stage conformance workflow: audit templates and
  READMEs first, narrow to concrete defects, apply in-place fixes, and verify
  with repo quality gates plus wiki index checks.
- Created `.claude/skills/docs-stage-conformance/skill.md` as a repo-local
  workflow Skill.
- Registered the Skill in `docs/00.agent-governance/harness-catalog.md` and
  updated `workspace-harness-audit` to route narrow docs cleanup to the new
  Skill.
- Recorded `skillify` as not applicable because no successful `/scrape` flow
  exists in this task.

#### Memory

- Use `docs-stage-conformance` for narrow authored-doc cleanup, template
  conformance, README/index drift, duplicate-H1 cleanup, link drift, and docs
  validation evidence.
- Use `workspace-harness-audit` only when the prompt spans workspace-wide
  GitOps, scripts, QA, CI/CD, SDD lifecycle, and agent governance coverage.

#### Evidence

- `.claude/skills/docs-stage-conformance/skill.md` contains the new workflow
  Skill.
- `docs/00.agent-governance/harness-catalog.md` registers the Skill and task
  routing.
- `docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md`
  contains the Skill Creation Follow-up section.
- `docs/04.execution/tasks/2026-05-24-workspace-harness-gap-analysis.md`
  tracks T-039 through T-043.
- `docs/03.specs/006-workspace-harness-gap-analysis/spec.md` includes
  VAL-SPC-006-013.

#### Handoff

- Do not promote this repo-local Skill to a global Codex package unless the
  human explicitly asks to package it outside `.claude/skills`.

---

### 2026-05-24 — workspace harness skill quality follow-up

- **Date**: 2026-05-24
- **Layer**: docs, meta, skills
- **Status**: complete
- **Tags**: #governance #skills #validation #harness #skill-quality

#### Progress

- Applied `skill-creator`, `skill-developer`, and `skill-improver` quality
  guidance to `.claude/skills/workspace-harness-audit/skill.md`.
- Reviewed `skillify` and recorded it as not applicable because this task did
  not include a repeated browser scrape flow to codify.
- Added a `When NOT to Use` section to the repo-local audit Skill so the trigger
  boundary is explicit.
- Recorded exact path checks and skill-quality findings in the linked plan and
  task.
- Ran `skill-creator` quick validation once; it failed as expected because this
  repository's `.claude/skills` convention uses lowercase `skill.md` rather than
  Codex package `SKILL.md`.

#### Memory

- For repo-local `.claude/skills/*/skill.md`, use the skill-creator quality
  principles manually, but do not rename files to `SKILL.md` unless the repo
  changes its tracked skill convention.
- `skillify` should only produce permanent browser-skill artifacts after a real
  successful scrape flow.

#### Evidence

- `docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md`
  contains the Skill Quality Follow-up section.
- `docs/04.execution/tasks/2026-05-24-workspace-harness-gap-analysis.md`
  tracks T-035 through T-038 and the Skill Quality verification summary.
- `docs/03.specs/006-workspace-harness-gap-analysis/spec.md` includes
  VAL-SPC-006-012.
- `.claude/skills/workspace-harness-audit/skill.md` includes a `When NOT to Use`
  section and remains under the 500-line limit.

#### Handoff

- Automated `skill-improver` review remains deferred until a `plugin-dev`
  `skill-reviewer` agent is available in the active harness.

---

### 2026-05-24 — superpowers executing-plans follow-up

- **Date**: 2026-05-24
- **Layer**: docs, meta, governance
- **Status**: complete
- **Tags**: #governance #superpowers #validation #harness #executing-plans

#### Progress

- Applied `superpowers:executing-plans` to the existing CEO Review Follow-up
  plan delta, using canonical SDD artifacts rather than a separate off-taxonomy
  plan file.
- Recorded the plan load, critical review, execution tasks, verification, and
  finish boundary in the linked plan and task.
- Verified the exact executing-plans path and its required companion workflow
  skill paths: `finishing-a-development-branch`, `using-git-worktrees`, and
  `writing-plans`.
- Recorded the branch/worktree boundary: this pass ran in a normal repo on
  `main` under the existing human-requested task-unit commit flow; no separate
  linked worktree existed.
- Updated `workspace-harness-audit` so future prompts that name an execution
  workflow require execution evidence, not just named-skill mention evidence.

#### Memory

- For `hy-home.k8s` harness follow-ups, if the human names an execution skill,
  preserve the execution flow: plan load, critical review, task execution,
  verification, and finish boundary.
- Do not create duplicate off-taxonomy plan files when a canonical SDD plan
  already owns the work, unless the human explicitly asks for that separate
  workflow.

#### Evidence

- `docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md`
  contains the Executing-Plans Follow-up section.
- `docs/04.execution/tasks/2026-05-24-workspace-harness-gap-analysis.md`
  tracks T-031 through T-034 and the Executing-Plans verification summary.
- `docs/03.specs/006-workspace-harness-gap-analysis/spec.md` includes
  VAL-SPC-006-011.
- `.claude/skills/workspace-harness-audit/skill.md` now requires execution-skill
  evidence when a prompt names an execution workflow.

#### Handoff

- Remaining unresolved items are unchanged: live runtime proof, GitHub Actions
  SHA/ruleset policy, `.claude/settings.local.json` precedence, and ignored
  graphify local cleanup.

---

### 2026-05-24 — gstack plan CEO review follow-up

- **Date**: 2026-05-24
- **Layer**: docs, meta, governance
- **Status**: complete
- **Tags**: #governance #gstack #validation #harness #ceo-review

#### Progress

- Applied `gstack-plan-ceo-review` in HOLD SCOPE mode to check whether the first
  workspace improvement task contract still had weak or missing evidence in the
  Hybrid Refresh plan after the approved P3 remediation work.
- Recorded that the skill's external-write preamble, design-doc persistence, and
  telemetry steps were not run because this repository keeps durable evidence in
  canonical SDD artifacts and the preamble writes under `~/.gstack`.
- Added missing exact path evidence for
  `/home/hy/.agents/skills/brainstorming/SKILL.md` and
  `/home/hy/.agents/skills/gstack/plan-ceo-review/SKILL.md`.
- Added a current-state overlay so Hybrid P3 rows that were later implemented by
  the approved P3 plan no longer read as the only active status.
- Updated `workspace-harness-audit` so future follow-up work records stale
  deferral overlays instead of leaving old P3 rows as the last visible truth.

#### Memory

- When a later approved task resolves a deferred item from a prior workspace
  harness audit, do not rewrite historical evidence. Add a current-state overlay
  linking the resolving plan/task/commit and leave remaining risk explicit.
- Treat `gstack-plan-ceo-review` as a review lens for this repository unless the
  human explicitly approves external `~/.gstack` writes or asks for gstack's
  separate design-doc workflow.

#### Evidence

- `docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md`
  contains the CEO Review Follow-up, initial-contract coverage ledger, P3
  current-state overlay, implementation plan, and deferred items.
- `docs/04.execution/tasks/2026-05-24-workspace-harness-gap-analysis.md`
  tracks T-027 through T-030 and the CEO Review verification summary.
- `docs/03.specs/006-workspace-harness-gap-analysis/spec.md` includes
  VAL-SPC-006-010 for the CEO review follow-up.
- `.claude/skills/workspace-harness-audit/skill.md` now requires current-state
  overlays when follow-up work changes earlier deferred status.

#### Handoff

- Remaining unresolved items are live runtime proof, GitHub Actions SHA/ruleset
  policy, `.claude/settings.local.json` precedence, and ignored graphify local
  cleanup.

---

### 2026-05-24 — approved P3 GitOps secret runtime remediation

- **Date**: 2026-05-24
- **Layer**: gitops, vault, eso, docs, qa
- **Status**: complete
- **Tags**: #gitops #argocd #vault #eso #secrets #validation #p3

#### Progress

- Used `grill-with-docs` and `workspace-harness-audit` as review lenses for the
  approved P3 follow-up, answering repository-evident questions without
  widening into direct runtime mutation.
- Implemented repository-backed desired-state changes for ESO DNS/API egress,
  Vault `platform/notifications` read policy, app `ExternalSecret` AppProject
  permission, sample app `remoteRef.key` semantics, and ArgoCD-owned
  cluster-local AppProject/ApplicationSet reconciliation.
- Added static contract assertions for the approved P3 contracts in
  `infrastructure/tests/verify-contracts-static.sh`.
- Clarified operations docs so Vault CLI paths that include `secret/` are not
  confused with ESO `remoteRef.key` values when the ClusterSecretStore path is
  already `secret`.

#### Memory

- For this repository, `vault kv put secret/apps/<name>/config ...` corresponds
  to ESO `remoteRef.key: apps/<name>/config` when the ClusterSecretStore path is
  `secret`.
- Approved P3 runtime work should remain GitOps-first: change repo desired
  state, run static contracts, then perform metadata-only live checks. Do not
  run `kubectl apply`, ArgoCD sync, Vault writes, or secret value reads unless
  a human explicitly approves that separate operation.
- `gitops/clusters/local/` now has a root child app path through
  `gitops/apps/root/platform-cluster-config-app.yaml`; existing clusters may
  need a bootstrap handoff if their live AppProject policy predates this commit.

#### Evidence

- `docs/04.execution/plans/2026-05-24-p3-gitops-secret-runtime-remediation.md`
  records implementation results, verification results, runtime unavailability,
  and remaining follow-up.
- `docs/04.execution/tasks/2026-05-24-p3-gitops-secret-runtime-remediation.md`
  records task completion, implementation decisions, rollback, static checks,
  and skipped/deferred live checks.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS with root app manifest
  count 18 and cluster-local kustomization validation.
- `bash scripts/validate-k8s-manifests.sh .` PASS for YAML syntax; optional
  `kube-linter` skipped because it is not installed locally.
- `bash scripts/check-secret-handling.sh .` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- Shell syntax, runtime JSON parse, `.env` key-name-only comparison, and
  `git diff --check` PASS after final doc updates.
- Read-only `kubectl get` runtime checks were attempted after human approval,
  but `https://0.0.0.0:6550` refused connection. `docker ps` listed no running
  containers and `k3d cluster list` returned no cluster rows.

#### Handoff

- Rerun read-only ArgoCD, ESO, Vault-status, AppProject, and ApplicationSet
  metadata checks after starting `k3d-hyhome`.
- Do not treat this commit as proof of live reconciliation; it proves repository
  desired-state and static contracts only.

---

### 2026-05-24 — workspace harness brainstorming reflection follow-up

- **Date**: 2026-05-24
- **Layer**: docs, meta
- **Status**: complete
- **Tags**: #governance #skills #validation #harness #brainstorming

#### Progress

- Applied `superpowers:brainstorming` as a design-lens review to check whether
  the Hybrid Refresh and Office-Hours follow-up still missed material items
  from the initial broad task contract.
- Recorded the brainstorming application boundary in the linked plan/task:
  standalone design-doc and user-approval defaults were deferred because this
  was an already-approved implementation objective and existing Spec 006 is the
  canonical SDD artifact.
- Added alternatives and selected design tables: strict Superpowers design-doc
  flow was rejected for this task, no-change was rejected, and canonical SDD
  delta recording was selected.
- Updated `.claude/skills/workspace-harness-audit/skill.md` so future broad
  audits prefer canonical spec/task/plan evidence over off-taxonomy design-doc
  locations unless the human explicitly requests a separate design document.

#### Memory

- For broad `hy-home.k8s` workspace improvement follow-ups, use named review
  skills as additive lenses and preserve the application boundary in canonical
  SDD artifacts.
- Do not create `docs/superpowers/specs/...` for this workflow unless the human
  explicitly asks for a separate Superpowers design-doc cycle.
- Keep P3 runtime, GitOps, Vault, CI/CD, and secret/env policy changes deferred
  unless a separate approved task opens those boundaries.

#### Evidence

- `docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md`
  contains the Superpowers Brainstorming Reflection Follow-up, alternatives,
  selected design, implementation plan, and deferred items.
- `docs/04.execution/tasks/2026-05-24-workspace-harness-gap-analysis.md`
  tracks T-024 through T-026 and the Brainstorming follow-up verification
  summary.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS for YAML syntax; optional
  `kube-linter` skipped because it is not installed locally.
- `bash scripts/check-secret-handling.sh .` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- Shell syntax, runtime JSON parse, `.env` key-name-only comparison,
  brainstorming evidence search, plan H1 check, and `git diff --check` PASS.

#### Handoff

- No new runtime, GitOps, Vault, CI/CD, or secret/env policy changes were
  implemented in this follow-up.
- If a future task starts as a new unapproved design idea rather than a
  continuation of this approved implementation objective, run the full
  Superpowers brainstorming design-doc and user-review gate.

---

### 2026-05-24 — workspace harness office-hours reflection follow-up

- **Date**: 2026-05-24
- **Layer**: docs, meta
- **Status**: complete
- **Tags**: #governance #skills #validation #harness #office-hours

#### Progress

- Applied `office-hours` as a problem-framing lens to check whether the Hybrid
  Refresh plan still missed any material items from the initial broad task
  contract.
- Recorded the `office-hours` application boundary in the linked plan/task:
  design-doc-only guidance was used for review, while implementation stayed
  under the direct human request and repository P1/P2/P3 safety rules.
- Added an Initial Contract Delta Ledger covering `grill-with-docs`, risk-tier
  treatment, exact skill path checks, subagent evidence, template-change impact,
  deletion/consolidation safeguards, and task-sized commit handling.
- Demoted the remaining post-title `Input Reflection Follow-up` H1 to H2.
- Updated `.claude/skills/workspace-harness-audit/skill.md` so future broad
  audits preserve named-skill application status and conflict boundaries.

#### Memory

- When a broad workspace prompt names an additive review skill, record whether
  it was applied, skipped, missing, or in conflict with the implementation
  contract.
- Design-only review skills can be used as a lens for repo-static planning, but
  they must not override a direct human request to implement safe P1/P2 work.
- Do not run `office-hours` preamble steps that write to `~/.gstack` unless the
  human approves that external write or a design-doc workflow truly needs it.

#### Evidence

- `docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md`
  contains the Office-Hours Reflection Follow-up, Initial Contract Delta Ledger,
  and Office-Hours Implementation Plan.
- `docs/04.execution/tasks/2026-05-24-workspace-harness-gap-analysis.md`
  tracks T-021 through T-023 and the Office-Hours follow-up verification
  summary.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- plan H1 heading check PASS; only the document title remains as H1.
- `git diff --check` PASS.

#### Handoff

- No new P3 runtime, GitOps, Vault, CI/CD, or secret/env policy changes were
  implemented in this follow-up.
- Live checks and external `office-hours` preamble writes remain approval-gated.

---

### 2026-05-24 — workspace harness hybrid refresh

- **Date**: 2026-05-24
- **Layer**: docs, meta, scripts, qa
- **Status**: complete
- **Tags**: #governance #skills #validation #harness #hybrid-refresh

#### Progress

- Reran six read-only role reviews for the workspace harness Hybrid Refresh:
  Documentation Lifecycle, Agent Governance, Scripts, GitOps Infrastructure,
  Environment Quality, and Skills & Harness.
- Preserved the fresh role review tables in the linked plan and added a
  path-level external `SKILL.md` presence ledger; all requested paths were
  present in the current WSL environment.
- Promoted Spec 006 from `draft` to `active` to match the stage README index and
  added `VAL-SPC-006-006` for Hybrid Refresh evidence.
- Made `.claude/hooks/session-start.sh` skip live `k3d`/`kubectl` probes unless
  `HY_HOME_K8S_ENABLE_SESSION_LIVE_PROBES=1` is explicitly set.
- Added `_workspace/` and `_workspace_prev/` to `.gitignore` as approved scratch
  paths for checked-in skills that define temporary analysis workspaces.
- Clarified meta ownership for tracked hook/skill/Codex runtime contract
  surfaces and added per-skill workflow/reference-pattern contract type in the
  harness catalog.
- Refreshed scripts/examples evidence wording so inventory and cloud example
  freshness point to the current 2026-05-24/Cloud Example Snapshot evidence.

#### Memory

- For no-live audit tasks, leave `HY_HOME_K8S_ENABLE_SESSION_LIVE_PROBES`
  unset. Set it to `1` only when the human approves read-only live startup
  probes.
- Store external skill checks path-by-path when a prompt requires exact
  `SKILL.md` path verification.
- Treat `_workspace/` and `_workspace_prev/` as scratch-only; durable evidence
  must move into the canonical docs taxonomy before completion.
- Keep P3 GitOps, Vault, AppProject, bootstrap ownership, CI supply-chain,
  local settings precedence, graphify cleanup, and live validation decisions in
  separate reviewed tasks.

#### Evidence

- `docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md`
  contains the Hybrid Refresh Coverage Ledger, Integrated Gap Analysis,
  Implementation Plan, raw role review tables, path-level skill check,
  verification results, checklist gate, and Hybrid Final Report.
- `docs/04.execution/tasks/2026-05-24-workspace-harness-gap-analysis.md`
  tracks T-014 through T-020 and the Hybrid Refresh verification summary.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS with root app manifest
  count 17.
- `bash scripts/validate-k8s-manifests.sh .` PASS for YAML syntax; optional
  `kube-linter` skipped because it is not installed locally.
- `bash scripts/check-secret-handling.sh .` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` PASS.
- `python3 -m json.tool .claude/settings.json` PASS.
- `python3 -m json.tool .codex/hooks.json` PASS.
- `.env.example` and `.env` key-name-only comparison PASS after Bash rerun
  without printing values.
- `git diff --check` PASS.

#### Handoff

- Live k3d/ArgoCD/Vault/ESO state remains unknown by design; run only
  explicitly approved read-only live checks.
- `.claude/settings.local.json` precedence and ignored graphify cleanup remain
  deferred owner decisions.

---

### 2026-05-24 — workspace harness input reflection follow-up

- **Date**: 2026-05-24
- **Layer**: docs, meta
- **Status**: complete
- **Tags**: #governance #skills #validation #harness

#### Progress

- Re-audited the workspace harness implementation against the earlier broad
  task contract to find weakly reflected input tasks.
- Verified exact external required `SKILL.md` paths in the current WSL
  environment; all listed paths were present.
- Added `.claude/skills/workspace-harness-audit/skill.md` for repeated
  workspace-wide Gap analysis and input-reflection audits.
- Added row-level `Required skill` evidence to the Implementation Plan so each
  implemented or deferred action carries the chosen skill group.
- Updated the harness catalog with the new repo-local Skill and updated the
  plan/task/spec evidence with input reflection follow-up requirements.
- Added an explicit `Skill and Harness Updates` Final Report section to cover
  the broader original report contract.

#### Memory

- Broad workspace improvement prompts should use
  `.claude/skills/workspace-harness-audit/skill.md` after baseline governance
  loading.
- Exact external `SKILL.md` path checks must be recorded in plan/task evidence,
  not only implied by a routing table.
- Broad implementation plans must keep a `Required skill` field on P1/P2/P3
  rows when the task contract asks for task-to-skill mapping before
  implementation.
- Future subagent-driven workspace audits must persist raw role Summary/Ledger
  tables directly in durable plan/task evidence when those raw tables are part
  of the task contract.

#### Evidence

- `docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md`
  contains the Input Reflection Follow-up and skill path check result.
- `docs/04.execution/tasks/2026-05-24-workspace-harness-gap-analysis.md`
  tracks T-010 through T-012 for the follow-up work.
- Final validation evidence is recorded in the linked task.

#### Handoff

- Historical raw subagent output tables were not reconstructed from chat
  history; future runs must preserve them as first-class evidence when required.

---

### 2026-05-24 — workspace harness gap analysis and limited implementation

- **Date**: 2026-05-24
- **Layer**: docs, meta, infra, qa
- **Status**: complete
- **Tags**: #governance #docs #gitops #validation #harness

#### Progress

- Created the workspace harness Gap analysis Spec, Plan, and Task records,
  including Coverage Ledger, Integrated Gap Analysis, Implementation Plan,
  deletion/consolidation/deferred/unknown tables, verification results,
  checklist gate, and Final Report.
- Preserved the six role-based subagent review findings as investigation input
  and avoided rerunning subagents because the implementation plan already
  treated them as current evidence.
- Corrected docs and infra scope bridge drift by linking `wiki-curator` and
  `gitops-reviewer` from the relevant governance scope files.
- Clarified that `_workspace/` scratch directories are allowed only when a
  checked-in skill explicitly defines them, and that durable outputs must move
  to the canonical docs taxonomy.
- Added task-to-skill routing and workflow/reference-pattern skill boundaries
  to the harness catalog while keeping `AGENTS.md` as a thin gateway.
- Hardened GitOps static validation so the root app directory must contain at
  least one non-kustomization ArgoCD root app manifest.
- Clarified that `HY_HOME_K8S_SKIP_HOOK_SIMULATION=1` is an internal hook
  wrapper bypass, not the normal manual validation contract.
- Deferred P3 runtime, secret policy, AppProject permission, bootstrap
  ownership, CI supply-chain, local settings precedence, ignored graphify
  cleanup, and live validation items for owner-approved follow-up.

#### Memory

- Keep `AGENTS.md` thin; recurring task-to-skill routing belongs in
  `docs/00.agent-governance/harness-catalog.md`.
- Treat medium-risk validation hardening as acceptable when it does not change
  runtime manifests or execution semantics.
- High-risk GitOps, Vault, CI policy, and live validation changes need a
  separate plan, explicit pre-checks, and human approval where live systems or
  secret boundaries are involved.
- `HY_HOME_K8S_SKIP_HOOK_SIMULATION=1` is hook-wrapper internal plumbing only.
  Maintainers should keep hook simulation enabled during manual validation.

#### Evidence

- Final verification evidence is recorded in
  `../../04.execution/tasks/2026-05-24-workspace-harness-gap-analysis.md`.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS with root app manifest
  count 17.
- `bash scripts/validate-k8s-manifests.sh .` PASS for YAML syntax; optional
  `kube-linter` was skipped because it is not installed locally.
- `bash scripts/check-secret-handling.sh .` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` PASS.
- `python3 -m json.tool .claude/settings.json` PASS.
- `python3 -m json.tool .codex/hooks.json` PASS.
- `.env.example` and `.env` key-name-only comparison PASS without printing
  values.
- `git diff --check` PASS.

#### Handoff

- P3 deferred items remain: ESO NetworkPolicy DNS/API egress, Vault
  `platform/notifications` policy, app `ExternalSecret` AppProject permission,
  `gitops/clusters/local` bootstrap CR ownership, GitHub Actions SHA pinning,
  `.claude/settings.local.json` precedence, ignored graphify cleanup, and live
  k3d/ArgoCD/Vault/ESO validation.

---

### 2026-05-22 — post-edit style and commit discipline hooks

- **Date**: 2026-05-22
- **Layer**: meta, docs
- **Status**: complete
- **Tags**: #hooks #style #formatting #commits #validation

#### Progress

- Committed the workspace-purpose alignment work in two logical units, merged
  the development branch into local `main`, and deleted the development branch.
- Updated the ignored local Hookify stop reminder so AI agents are reminded to
  split repo-changing work into logical commits before final stop unless the
  human explicitly asks not to commit.
- Extended `.claude/hooks/post-validate.sh` so file edits run scoped
  auto-format hooks before existing validation.
- Added scoped style checks for Markdown, shell, GitHub Actions workflows, and
  Dockerfiles through the existing pre-commit hook inventory.
- Updated the runtime baseline and harness catalog to describe the new
  PostToolUse auto-format/style validation responsibility.

#### Memory

- Keep the logical-commit reminder in ignored Hookify `.local.md` files unless a
  human asks for a shared blocking policy. Shared repository enforcement should
  remain deterministic and validation-focused.
- Post-edit formatting should stay scoped to edited files. Avoid running a full
  repository formatter from PostToolUse because that creates unrelated churn.
- Use the repo's pre-commit hook inventory as the style source of truth instead
  of inventing a parallel style toolchain.

#### Evidence

- `git log --oneline -3` showed logical commits:
  `docs(governance): Record workspace purpose audit` and
  `chore(agent): Harden direct command guardrails`.
- Local `main` was fast-forward merged to `425a3f3`.
- `codex/workspace-purpose-alignment` was deleted locally.
- `bash -n .claude/hooks/post-validate.sh` PASS.
- Synthetic PostToolUse payload for `.claude/hooks/post-validate.sh` PASS:
  auto-format hooks, shell style, shell syntax, and repository quality gates.
- Synthetic PostToolUse payload for runtime/governance docs PASS:
  auto-format hooks, Markdown style, and repository quality gates.
- Full static validation PASS:
  repo quality gates, LLM wiki index check, GitOps structure, Kubernetes
  manifest syntax, secret handling, static infrastructure contracts, runtime
  JSON parse, shell syntax, and `git diff --check`.

#### Handoff

- The logical-commit Hookify reminder is local-only and ignored by Git. It is
  active in this workspace but not part of the shared repository state.

---

### 2026-05-22 — workspace purpose alignment audit

- **Date**: 2026-05-22
- **Layer**: docs, meta, infra, ops
- **Status**: complete
- **Tags**: #governance #docs #gitops #hooks #versions #validation

#### Progress

- Re-audited the workspace against its full purpose: WSL2 native Docker, k3d,
  ArgoCD GitOps, External Secrets/Vault, external PostgreSQL/Valkey contracts,
  SDD document lifecycle, Agent governance, hooks, CI, validation scripts,
  examples, README layers, and version references.
- Confirmed the existing README/template/lifecycle/Agent governance baseline was
  already covered by the repo quality gate and did not need broad rewrites.
- Added Plan/Task evidence for this purpose-alignment workstream and indexed
  both documents under `docs/04.execution/`.
- Refreshed the tech stack version inventory from official Kubernetes, EKS,
  AKS, and Terraform Registry sources without changing repo desired-state pins.
- Expanded the shared Claude deny boundary for direct `kubectl`, `argocd app`,
  and Vault write commands, and aligned local Hookify advisory wording with the
  tracked allow/deny boundary.

#### Memory

- Version inventory refreshes should distinguish "official latest awareness"
  from "repo desired-state upgrade." Do not change k3s, cloud example, or
  Terraform pins unless the corresponding manifest/config changes in the same
  work item.
- Keep direct live commands behind human-approved bootstrap or break-glass
  paths. The shared Claude permission gate should deny common mutation and live
  access command families; local Hookify files remain ignored advisory rules.
- When a broad purpose audit finds the baseline already valid, record that
  outcome and avoid rewriting templates, README files, or historical lifecycle
  documents just to create churn.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS for YAML syntax; optional
  `kube-linter` was skipped because it is not installed locally.
- `bash scripts/check-secret-handling.sh .` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- `python3 -m json.tool .claude/settings.json` PASS.
- `python3 -m json.tool .codex/hooks.json` PASS.
- `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` PASS.
- `git diff --check` PASS.
- Official source refresh performed on 2026-05-22 against Kubernetes releases,
  AWS EKS versions, Azure AKS supported versions, and Terraform Registry provider
  / module APIs.
- `pre-commit`, `shellcheck`, `actionlint`, `zizmor`, `kube-linter`,
  `graphify`, and `rtk` are not installed in this local environment.
- Final validation evidence is recorded in
  `../../04.execution/tasks/2026-05-22-workspace-purpose-alignment.md`.

#### Handoff

- Live k3d/ArgoCD reconciliation, direct cluster mutation, Vault writes, cloud
  account changes, and plaintext Kubernetes secret authoring were intentionally
  not executed.

---

### 2026-05-22 — docs governance Full A+B hardening

- **Date**: 2026-05-22
- **Layer**: docs, meta
- **Status**: complete
- **Tags**: #docs #templates #governance #hooks #validation

#### Progress

- Implemented the Full A+B documentation and governance alignment plan on
  `codex/docs-governance-full-ab-hardening`.
- Updated the README template contract so `Link Basis` and `Related Documents`
  are required for README files, and normalized README files across root,
  docs, GitOps, infrastructure, scripts, tests, traefik, and examples paths.
- Preserved historical lifecycle document meaning while removing authored-doc
  template residue from the template cross-link plan.
- Clarified Claude/Codex hook ownership and Hookify `.local.md` boundaries in
  the runtime baseline, harness catalog, provider notes, agentic rules,
  documentation protocol, postflight checklist, and scripts README.
- Hardened `scripts/validate-repo-quality-gates.sh` to reject README legacy
  headings, missing README link bases, tracked `.claude/*.local.md` files, and
  malformed local Hookify frontmatter.
- Added and closed Plan/Task evidence records under `docs/04.execution/`.

#### Memory

- README changes must preserve `Link Basis` and `Related Documents`; `Related
References` is now a legacy heading that should not return.
- Hookify `.local.md` files are local warning rules only. Keep shared
  enforcement in tracked hooks, provider/Codex hook wiring, and validators.
- For historical lifecycle docs, prefer narrow structure/link cleanup over
  rewriting the past decision or evidence record as a current contract.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS for YAML syntax; optional
  `kube-linter` was skipped because it is not installed locally.
- `bash scripts/check-secret-handling.sh .` PASS.
- `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` PASS.
- `python3 -m json.tool .claude/settings.json` PASS.
- `python3 -m json.tool .codex/hooks.json` PASS.
- `git diff --check` PASS.
- Targeted scans found no README `## deprecated README heading`, no README missing
  `## Link Basis`, no authored lifecycle template residue, and no tracked
  `.claude/*.local.md` files.
- `git status --short --ignored .claude` confirmed Hookify local rule files are
  ignored (`!!`) and not tracked.

#### Handoff

- Live k3d/ArgoCD reconciliation, direct cluster mutation, external Vault
  writes, and plaintext Kubernetes secret authoring were intentionally not
  executed.

---

### 2026-05-22 — runtime premise and local skill mirror remediation

- **Date**: 2026-05-22
- **Layer**: docs, meta, runtime
- **Status**: complete
- **Tags**: #governance #docs #runtime #skills #validation

#### Progress

- Aligned active entrypoints, guides, runbooks, and infrastructure README
  wording with the current WSL2 + WSL-native Docker + k3d runtime premise.
- Preserved historical Docker Desktop context in older PRD/ARD/Spec records
  and added current-contract notes where readers could confuse historical
  runtime assumptions with the active execution contract.
- Updated README indexes and template guidance so runtime premise changes are
  handled through current-contract notes, index freshness, and validation rather
  than broad historical rewrites.
- Clarified that `.claude/skills/**` is the repo-backed skill source of truth
  and workspace-local `.agents/skills/**` files are ignored convenience mirrors.
- Extended `scripts/validate-repo-quality-gates.sh` to verify `.agents/`
  remains ignored and untracked, and to compare existing local skill mirrors
  byte-for-byte against tracked `.claude/skills/<name>/skill.md` sources.
- Synced the ignored local `.agents/skills/docs-stage-routing/skill.md` mirror
  with `.claude/skills/docs-stage-routing/skill.md` and refined the ignored
  local hookify mirror-parity rule.
- Used sub agents for documentation, validation/hook, and security/GitOps
  review, then applied the non-conflicting findings in this worktree.

#### Memory

- Current runtime truth for active docs is WSL2 + WSL-native Docker. Historical
  Docker Desktop wording in PRD/ARD/Spec records can remain when paired with a
  current-contract note.
- Keep ignored `.agents/**` non-canonical. Quality gates may inspect local
  mirrors when present, but canonical skill ownership stays in tracked
  `.claude/skills/**`.
- Avoid widening lifecycle Stop hooks to scan ignored local trees on every
  completion; use explicit repo quality validation for local mirror drift.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS, including `.agents/`
  ignore/untracked checks and local skill mirror parity.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS.
- `bash scripts/check-secret-handling.sh .` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS for YAML syntax; optional
  `kube-linter` was skipped because it is not installed locally.
- `bash -n scripts/validate-repo-quality-gates.sh .claude/hooks/post-validate.sh .claude/hooks/lifecycle-guard.sh` PASS.
- `git diff --check` PASS.
- `rg "Docker Desktop"` only returned historical mentions paired with
  current-contract context.
- `diff -u .claude/skills/docs-stage-routing/skill.md .agents/skills/docs-stage-routing/skill.md`
  produced no output.
- `git ls-files .agents/` produced no output, and `git check-ignore -v`
  confirmed `.agents/` remains ignored.

#### Handoff

- Live k3d/ArgoCD reconciliation was intentionally not executed because this
  task only changed documentation, governance, validation, and local ignored
  mirror state.

---

### 2026-05-22 — governance docs lifecycle hook hardening

- **Date**: 2026-05-22
- **Layer**: docs, meta, runtime
- **Status**: complete
- **Tags**: #governance #templates #hooks #validation

#### Progress

- Added structural template coverage to `scripts/validate-repo-quality-gates.sh`
  so every non-README authored Markdown file under `docs/01.requirements`,
  `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`,
  `docs/05.operations`, and `docs/90.references` must match exactly one
  template mapping.
- Documented the structural template mapping contract in `docs/99.templates`,
  documentation governance rules, and doc-writer Claude/Codex mirrors.
- Added `.claude/hooks/lifecycle-guard.sh` and wired Stop, SubagentStop, and
  PreCompact in `.claude/settings.json` plus compatible Codex wiring in
  `.codex/hooks.json`.
- Extended the repo quality gate to verify lifecycle hook wiring and simulate
  clean, failing, and advisory lifecycle payloads.
- Updated the harness catalog, Agent-first rules, provider notes, postflight
  checklist, runtime baseline, and execution task evidence to describe the new
  lifecycle contract.

#### Memory

- Structural template enforcement must cover both document headings and path
  coverage. A canonical docs path that is not mapped to exactly one template is
  a governance drift, even if the document has plausible headings.
- Lifecycle hooks should stay thin. Keep subjective policy in governance docs
  and use Stop/SubagentStop only for objective repo-state validation failures;
  keep PreCompact advisory.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS, including structural
  template coverage and lifecycle hook payload simulation.
- `git diff --check` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS for YAML syntax; optional
  `kube-linter` was skipped because it is not installed locally.
- `bash scripts/check-secret-handling.sh .` PASS.
- `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` PASS.
- `python3 -m json.tool .claude/settings.json` and
  `python3 -m json.tool .codex/hooks.json` PASS.
- Direct lifecycle self-tests confirmed clean Stop did not block,
  forced-failure Stop/SubagentStop emitted `decision=block`, and PreCompact
  emitted advisory `systemMessage` without blocking.
- `command -v rtk` returned not found, so direct repo-backed commands were used.

#### Handoff

- Live k3d/ArgoCD reconciliation, external Vault changes, plaintext secret
  creation, and GitHub settings/ruleset changes were intentionally not
  executed.

---

### 2026-05-22 — documentation system contract alignment

- **Date**: 2026-05-22
- **Layer**: docs, meta
- **Status**: complete
- **Tags**: #docs #templates #links #validation

#### Progress

- Aligned root and docs README navigation with the canonical
  `docs/99.templates` template-folder mapping and validator-backed README
  section rules.
- Clarified governance and memory README link bases without moving governance
  policy or duplicating runtime rules.
- Normalized stage README purpose lines for execution, incidents, references,
  and templates while preserving existing folder ownership.
- Strengthened template `Related Documents` upstream examples and placeholder
  naming for operation, runbook, incident, postmortem, agent design, and
  reference templates.
- Converted stale or conflicting generated/operations documents to historical
  or evidence-focused wording without deleting, moving, or renaming files.

#### Memory

- When template examples describe links from a future authored document, keep
  them as code literals and calculate them from the final target location.
- Superseded operations documents can preserve historical procedures, but the
  active path must be called out explicitly and linked to the current policy,
  guide, or runbook.

#### Evidence

- Local Markdown link scan over `README.md` and `docs/**/*.md` reported
  `BROKEN=0`.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- `bash scripts/validate-gitops-structure.sh` PASS.
- `bash scripts/validate-k8s-manifests.sh .` PASS for YAML syntax; optional
  `kube-linter` was skipped by the script because it was not installed in the
  command environment.
- `bash scripts/check-secret-handling.sh .` PASS.
- `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` PASS.
- `git diff --check` PASS.

#### Handoff

- None.

---

### 2026-05-21 — operations policy runbook boundary clarification

- **Date**: 2026-05-21
- **Layer**: docs, operations
- **Status**: complete
- **Tags**: #docs #operations #runbooks #validation

#### Progress

- Reviewed executable command and checklist blocks under
  `docs/05.operations/policies/` against the owning operations runbooks.
- Clarified that policies own controls, approval boundaries, and required
  evidence, while runbooks own command order, recovery procedures, and
  bootstrap/break-glass execution.
- Converted duplicated policy verification command blocks into evidence tables
  with runbook-owner links for GitOps platform, HA, Rollouts/Notifications/
  Headlamp, observability platform, k8s observability, and app onboarding.
- Routed remaining service-mesh/cert-manager procedural command literals to
  the owning platform-expansion runbook while keeping policy contract values in
  place.
- Updated the operation template and policies index so future policy documents
  keep procedural commands in the owning runbook.

#### Memory

- When an operations policy needs verification, prefer evidence descriptions
  and runbook-owner links over executable command blocks. Keep command sequences
  in runbooks unless the command literal is part of the policy contract itself.

#### Evidence

- `rg` scan confirmed no executable `bash` code blocks remain under
  `docs/05.operations/policies/`; remaining command-like literals are policy
  contract values, prohibitions, or runbook-owner references.
- `git diff --check` PASS.
- `bash scripts/validate-repo-quality-gates.sh .` PASS, including repo-local
  Markdown link target checks.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/check-secret-handling.sh .` PASS.

#### Handoff

- None.

---

### 2026-05-21 — docs office-hours taxonomy follow-up

- **Date**: 2026-05-21
- **Layer**: docs, meta
- **Status**: complete
- **Tags**: #docs #templates #links #validation

#### Progress

- Inspected root README, docs hub, target stage READMEs, governance routing,
  templates, and generated spec/plan documents for taxonomy and link alignment.
- Clarified `spec.template.md` so `Related Documents` carries upstream and
  downstream traceability, while `Related Inputs` remains an upstream summary.
- Added the same upstream links to existing generated `docs/03.specs/*/spec.md`
  documents without changing their implementation contracts.
- Clarified `readme.template.md` snippet-library handling and the templates
  README spec mapping.
- Converted the completed template cross-link plan's active execution wording
  into historical-record wording and marked its no-task-record case as a
  historical exception in the plans index.

#### Memory

- Do not remove `Related Inputs` from specs; the repo quality gate derives
  required headings from the template. Add traceability to `Related Documents`
  when policy requires upstream links.
- Completed execution plans should not retain active agent execution prompts.
  Preserve migration context, but label completed exceptions as historical.

#### Evidence

- `git status --short` was clean before edits.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS before edits.
- `bash scripts/validate-repo-quality-gates.sh .` PASS before edits.
- Read-only subagent link scan found 0 broken local Markdown links across
  root README and `docs/**/*.md`.
- `git diff --check` PASS after edits.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS after edits.
- `bash scripts/validate-repo-quality-gates.sh .` PASS after edits.
- `bash infrastructure/tests/verify-contracts-static.sh` PASS after edits.
- `bash scripts/validate-gitops-structure.sh` PASS after edits.
- `bash scripts/validate-k8s-manifests.sh .` PASS for YAML syntax after edits;
  optional `kube-linter` was skipped because it is not installed locally.
- `bash scripts/check-secret-handling.sh .` PASS after edits.
- `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +`
  PASS after edits.

#### Handoff

- None.

---

### 2026-05-19 — docs template enforcement hardening

- **Date**: 2026-05-19
- **Layer**: docs, meta
- **Status**: complete
- **Tags**: #docs #templates #validation #agents

#### Progress

- Clarified template enforcement in `rules/documentation-protocol.md`,
  `rules/document-stage-routing.md`, and `rules/stage-authoring-matrix.md`.
- Updated `docs-stage-routing` and the `doc-writer` Claude/Codex runtime
  contracts so agents must confirm the template map, read the matching
  template, preserve required headings, set new authored docs to draft, and
  report validation evidence.
- Aligned the harness catalog row for `doc-writer` with its broader
  stage-document authoring role.
- Added authored-stage documentation detection to the shared Claude/Codex
  PreToolUse edit hook so template guidance is surfaced before document edits.
- Added PostToolUse documentation template enforcement for authored stage docs
  through `scripts/validate-repo-quality-gates.sh`.
- Extended hook payload simulation so both Claude and Codex hook paths are
  checked for documentation template warnings and post-edit enforcement output.
- Added a local Hookify file-rule reminder for authored stage documentation and
  ignored `.claude/*.local.md` so Hookify local rules stay out of shared Git
  history.
- Extended `scripts/validate-repo-quality-gates.sh` so `03.specs` helper docs
  (`api-spec.md`, `agent-design.md`, `data-model.md`, and `tests.md`) are
  checked against their matching templates.
- Added regression phrase checks for the template enforcement contract across
  governance, skill, and agent mirror surfaces.

#### Memory

- Template enforcement now spans policy, routing skill, doc-writer agent
  contracts, Codex mirror, edit hooks, and repo quality gates. Keep these
  surfaces aligned in the same change when the template contract changes.
- Generated reference outputs such as `docs/90.references/llm-wiki/wiki-index.md`
  stay under their generator contract rather than manual authoring.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `git diff --check` PASS.
- Targeted `rg` scan for template enforcement references reviewed.
- `bash -n .claude/hooks/k8s-pre-edit.sh .claude/hooks/post-validate.sh scripts/validate-repo-quality-gates.sh` PASS.
- Claude docs PreToolUse payload simulation surfaced `docs/99.templates/templates/sdlc/specs/api-spec.template.md`.
- Claude docs PostToolUse payload simulation returned `[hook] PASS documentation template enforcement`.
- Hookify local rule created at `.claude/hookify.require-doc-templates.local.md`
  and kept untracked by `.gitignore`.

#### Handoff

- None.

---

### 2026-05-19 — docs taxonomy and template alignment

- **Date**: 2026-05-19
- **Layer**: docs, meta
- **Status**: complete
- **Tags**: #docs #templates #links #validation

#### Progress

- Clarified root and docs hub entrypoints with the documentation map,
  lifecycle contract, template-to-folder mapping, stale-document rules, and
  target-relative link expectations.
- Hardened canonical PRD, ARD, ADR, Spec, Plan, Task, README, and Runbook
  templates without adding new files.
- Aligned safely identifiable generated documents with updated template
  structure, including PRD acceptance criteria headings, Spec verification
  command headings, selected ADR section order, and selected operations
  document section placement.
- Consolidated the completed template cross-link plan's stale unchecked task
  detail section into historical execution notes and a migration note.

#### Memory

- Template heading changes affect quality-gate-required headings for generated
  docs. Update the template and every authored document using that template in
  the same change.
- Keep optional or placeholder cross-link examples as code literals unless the
  target exists and the link resolves from the current Markdown file.
- Completed execution plans should not retain unchecked step-by-step execution
  checklists unless they clearly describe historical evidence rather than future
  work.

#### Evidence

- `git diff --check` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.

#### Handoff

- No files were deleted, moved, or renamed.
- External version inventory values were not refreshed; this pass only aligned
  documentation structure, templates, and local cross-link rules.

---

### 2026-05-18 — docs stage README link-basis normalization

- **Date**: 2026-05-18
- **Layer**: docs, product, architecture, ops
- **Status**: complete
- **Tags**: #docs #readme #templates #validation

#### Progress

- Normalized root, docs hub, and affected stage README entrypoints against
  the repository README template base structure.
- Added missing `Link Basis` sections to root/docs/architecture/operations/
  references README surfaces and translated touched link-basis guidance for
  human-facing README files.
- Added missing one-line purpose statements to `docs/README.md`,
  `docs/02.architecture/README.md`,
  `docs/02.architecture/requirements/README.md`,
  `docs/02.architecture/decisions/README.md`,
  `docs/03.specs/README.md`, `docs/04.execution/README.md`, and
  `docs/05.operations/README.md`.
- Added operations template routing in `docs/05.operations/README.md` so Guide,
  Policy, Runbook, Incident, and Postmortem entrypoints point to their starting
  templates.
- Clarified `docs/90.references/README.md` so non-README reference documents
  keep the full reference template contract while README index files can remain
  navigation surfaces.

#### Memory

- README template conformance in this repository should include a short purpose
  statement, `## Link Basis`, and `## Related Documents` for root, stage, and
  nested README entrypoints.
- Reference README index files are not standalone reference documents; they can
  summarize reference metadata instead of duplicating every
  `reference.template.md` section.
- `/latest` external URLs in version references should be treated as dated
  source-check URLs unless a stable release permalink is explicitly recorded.

#### Evidence

- `git diff --check` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- Targeted README scan over root, docs hub, requested stage READMEs, and nested
  `02.architecture`, `04.execution`, `05.operations`, and `90.references`
  READMEs found no missing `## Link Basis` or `## Related Documents` sections.
- Read-only subagent audits reviewed `01.requirements`/`02.architecture`/
  `03.specs`, `04.execution`/`05.operations`, and `90.references`/root
  README scopes; accepted concrete gaps were folded into this change.

#### Handoff

- No PRD, ARD, ADR, Spec, Plan, Task, operations document body, GitOps
  manifest, live cluster state, Vault secret, or plaintext Kubernetes Secret
  was changed.
- External version facts were not refreshed in this pass; only the README rule
  for interpreting `/latest` source URLs was clarified.

---

### 2026-05-18 — docs template link-basis clarification

- **Date**: 2026-05-18
- **Layer**: docs, meta
- **Status**: complete
- **Tags**: #docs #templates #links #validation

#### Progress

- Clarified README template link-basis rules without forcing a single target for
  the multi-target README template.
- Clarified `memory.template.md` and `progress.template.md` link-basis wording
  so generated links are calculated from their final authored memory location,
  not from the template file.
- Added a concise `docs/99.templates/README.md` note for the README, memory, and
  progress template link-basis exceptions.
- Left existing PRD, ARD, ADR, Spec, Plan, Task, Guide, Policy, Runbook, and
  Reference documents unchanged because scans did not identify concrete broken
  links, template residue, stale placeholders requiring correction, or README
  inventory drift.

#### Memory

- `readme.template.md` is intentionally multi-target and should not receive a
  single `Target:` comment.
- `memory.template.md` uses a target family under
  `docs/00.agent-governance/memory/<topic>.md`; `progress.template.md` is an
  append-entry template for `docs/00.agent-governance/memory/progress.md`.
- Target-relative placeholder scans are useful validation evidence, but
  no-single-target helper templates must be treated as explicit exceptions.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `git diff --check` PASS.
- Markdown link scan over root, agent gateway, `.claude/CLAUDE.md`, and
  `docs/**/*.md`: `MISSING_LINKS: 0`.
- Target-relative placeholder scan over target-bearing templates:
  `TARGET_REL_LINK_ISSUES: 0`.
- Authored docs template residue scan outside `docs/99.templates/**`: no matches.
- Placeholder scan reviewed; matches were code literals, historical plans, or
  command examples outside the scoped defect criteria.

#### Handoff

- No runtime API, Kubernetes manifest, GitOps desired state, live cluster state,
  plaintext Secret, or external service action was changed.

---

### 2026-05-18 — docs stage conformance follow-up

- **Date**: 2026-05-18
- **Layer**: docs, meta
- **Status**: complete
- **Tags**: #docs #templates #readme #validation

#### Progress

- Demoted duplicate actionable H1 headings in the Plan and Spec templates while
  preserving their primary document title H1.
- Demoted the duplicate H1 in the completed template cross-link plan without
  changing its status, update date, or execution-history content.
- Added `graphify-out/` to the root README repository map because tracked
  graphify outputs are shared exploration artifacts and `.claude/CLAUDE.md`
  treats `GRAPH_REPORT.md` as architecture/codebase context when present.
- Left `readme.template.md`, `memory.template.md`, `progress.template.md`, and
  the generated LLM Wiki index unchanged as intentional exceptions.

#### Memory

- Duplicate H1 checks for templates must ignore fenced code and HTML comments;
  `readme.template.md` intentionally includes instructional H1 examples.
- Stale Dashboard scans should target old Kubernetes Dashboard markers, not
  `Rollouts Dashboard`, which is a current contract.
- `memory.template.md` uses `Related Progress` intentionally, and
  `progress.template.md` is an append-entry template rather than a standalone
  authored document.

#### Evidence

- `git diff --check` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- Authored non-README frontmatter/status/Overview/Related Documents scan PASS.
- README index sync scan PASS.
- Duplicate H1 scan reviewed; only the intentional `readme.template.md`
  instructional examples remain.
- Stale contract boundary scan PASS after treating historical, superseded,
  bootstrap, break-glass, and operator-triggered reconciliation contexts as
  explicit boundaries.

#### Handoff

- No PRD, ARD, ADR, Spec, Plan, Task, GitOps manifest, generated wiki index,
  live cluster state, Vault secret, or plaintext Kubernetes Secret was changed.
- No follow-up is required for this scoped conformance follow-up.

---

### 2026-05-18 — docs template conformance pass

- **Date**: 2026-05-18
- **Layer**: docs, meta
- **Status**: complete
- **Tags**: #docs #templates #frontmatter #validation

#### Progress

- Audited the target-bearing templates under `docs/99.templates/` against their
  `Target` comments and target-relative code-literal link examples.
- Confirmed no concrete template path defect required changes in this pass.
- Added minimal YAML frontmatter to legacy template-governed authored documents
  that lacked it: ARD 0001-0003, ADR 0001-0012, the 2026-03-27/28/29 execution
  plans, and the 2026-03-27/28/29 execution tasks.
- Normalized the governance README related-link heading from
  `deprecated README heading` to `Related Documents` in the governance hub and memory
  README without changing their English body content.

#### Memory

- Template code-literal placeholder links are calculated from the final authored
  `Target` location, while real Markdown links inside template files still
  resolve from `docs/99.templates/`.
- Code-label versus href scans are advisory unless the label claims an exact
  path that points readers to a different target. Short labels that route to a
  folder README are acceptable when the Markdown link resolves.
- Legacy document frontmatter status should be evidence-backed from the
  document body or owning README index, not inferred from file age alone.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `git diff --check` PASS.
- Targeted legacy frontmatter check PASS.
- Target-relative template placeholder scanner PASS.
- README and `docs/**/*.md` missing-link scanner: `MISSING_LINKS: 0`.
- Code-label/href advisory report reviewed; remaining items are short labels or
  anchor comparison noise, not broken links.

#### Handoff

- No generated/index file, Kubernetes manifest, ArgoCD object, live cluster
  state, Vault secret, Slack configuration, or plaintext Kubernetes Secret was
  changed.
- No follow-up is required for this scoped conformance pass.

---

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
- Standardized the touched execution README headings from deprecated README heading to
  Related Documents.

#### Memory

- `docs/04.execution/plans/README.md` and
  `docs/04.execution/tasks/README.md` should stay as compact entrypoints, not
  mixed template fragments plus historical duplicate sections.
- Existing Plan and Task artifact files were intentionally not normalized in
  this pass. Their historical status, date, and evidence fields remain owned by
  the artifact documents.
- The repository quality gate still allows `deprecated README heading` in some README
  surfaces, so touched-scope heading consistency needs a targeted check until
  the validator explicitly includes `docs/04.execution`.

#### Evidence

- Changed-file scope was limited to the three execution READMEs and this
  progress ledger entry.
- Targeted `docs/04.execution` deprecated README heading scan: PASS.
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
  `docs/90.references/data/tech-stack-version-inventory.md`.
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
  `docs/99.templates/templates/common/reference.template.md` and a touched-scope validation check
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
  `docs/05.operations` README entrypoints; older `## deprecated README heading` headings
  remain temporarily allowed only outside this touched scope.
- Operations policy documents keep `type: operation` to match
  `policy.template.md` and the stage authoring matrix.
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
  `postmortem.template.md`, `policy.template.md`, and `reference.template.md`.
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
- For `docs/05.operations/incidents/YYYY/INC-###-<title>/`, links to runbooks
  and policies resolve through `../../../runbooks/` and `../../../policies/`;
  postmortem links resolve to same-folder `postmortem.md`.
- For `docs/05.operations/incidents/YYYY/INC-###-<title>/postmortem.md`,
  links back to incident records resolve to same-folder `INC-###-<title>.md`,
  and runbooks/policies through `../../../runbooks/` and `../../../policies/`.

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

- Updated `docs/90.references/data/tech-stack-version-inventory.md` to match actual pinned versions in `.pre-commit-config.yaml` and `.github/workflows/`: commitizen, gitleaks, markdownlint-cli2, check-jsonschema, shfmt, zizmor, actionlint (pre-commit); actions/labeler, actions/upload-artifact (github_actions). Total: 9 version entries corrected.
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
- Added `docs/99.templates/templates/common/progress.template.md` as the template for this
  `progress.md` ledger.
- Updated bootstrap, preflight, postflight, documentation protocol, runtime
  baseline, and memory README guidance so AI agents read and write this ledger
  during repo-changing work.

#### Memory

- `docs/00.agent-governance/memory/progress.md` is the mandatory local ledger
  for repo-changing agent progress, reusable memory, evidence, and handoff.
- Standalone memory notes may still use `docs/99.templates/templates/common/memory.template.md`,
  but normal agent work should append to this file using
  `docs/99.templates/templates/common/progress.template.md`.

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

- Audited `docs/90.references/README.md`, `docs/90.references/data/README.md`,
  current reference documents, `docs/99.templates/templates/common/reference.template.md`, and
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
  `docs/90.references/data/tech-stack-version-inventory.md` because it is a
  version-contract inventory and dated external-standard snapshot.
- Added `docs/90.references/data/README.md` and updated root/docs/examples,
  infrastructure, Traefik, and repo-quality validator references to the new
  version inventory path.

#### Memory

- Learning roadmaps and durable theory connections belong under
  `docs/90.references/learning/` and need a local README index.
- Version inventories, cloud support snapshots, durable Agent reference
  catalogs, and repo-backed dependency contract references belong under
  `docs/90.references/data/`.
- `docs/90.references/README.md` should stay the routing hub, not a mixed
  document dump for every reference type.
- In the 2026-07-03 Codex shell, `rtk` was not on PATH. The local binary at
  `/home/hy/.local/bin/rtk` reported version `0.34.3`, but `rtk gain` failed to
  initialize its tracking database, so validation ran with direct shell
  commands without inspecting private runtime state.

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
  `docs/99.templates/templates/common/progress.template.md` for `progress.md` updates and
  `docs/99.templates/templates/common/memory.template.md` for standalone memory files.
- Updated bootstrap, documentation protocol, preflight, postflight, and the
  local runtime baseline so repo-changing agent work plans and records
  `memory/progress.md` updates.
- Added repo-quality gate checks for the memory template inventory, standalone
  memory file template headings, and progress-ledger coupling.

#### Memory

- `docs/00.agent-governance/memory/progress.md` is the mandatory progress
  ledger for repo-changing agent work.
- Standalone files under `docs/00.agent-governance/memory/` must use
  `docs/99.templates/templates/common/memory.template.md` and include a `Related Progress`
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

### 2026-05-18 — 90.references learning roadmap boundary clarification

- **Date**: 2026-05-18
- **Layer**: docs, meta
- **Status**: complete
- **Tags**: #docs #references #learning #validation

#### Progress

- Clarified `docs/90.references/learning/infrastructure-to-theory-roadmap.md`
  Module C wording so the learning roadmap reads as an offline concept exercise,
  not as repository, live cluster, ArgoCD, Vault, or manifest work.
- Left `docs/90.references/README.md` untouched because its existing overview,
  work rules, and authority boundary already cover the reference-only scope.
- Did not create new files, edit generated LLM Wiki output, change version
  inventory values or freshness dates, or modify runtime/GitOps/secret surfaces.

#### Memory

- When `90.references` learning material uses exercises, keep the exercise
  explicitly offline unless a separate spec, plan, or runbook authorizes repo or
  cluster work.

#### Evidence

- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `git diff --check` PASS.
- Targeted negative checks confirmed no generated LLM Wiki, version inventory,
  new file, runtime, manifest, secret, cluster, or deployment changes.

#### Handoff

- None.

### 2026-05-29 — 3-provider governance parity and capability symmetry

- **Date**: 2026-05-29
- **Layer**: meta
- **Status**: complete
- **Tags**: #governance #docs #validation

#### Progress

- Reconciled the `.agents/` framing: corrected `.claude/CLAUDE.md` and `harness-catalog.md` to treat `.agents/**` as a git-tracked Gemini provider surface (peer of `.codex/**`), matching `bootstrap.md` and the actual tracked state. Prior "ignored convenience mirror" wording was stale.
- Fixed provider-note pointers: `providers/claude.md` and `providers/gemini.md` no longer claim root shims import `@AGENTS.md` (they import `@bootstrap.md` + provider note + local baseline + `@RTK.md`); `providers/gemini.md` baseline pointer corrected to `.agents/GEMINI.md`.
- Added a canonical Model Tier Mapping (`top`/`worker`) to `harness-catalog.md` with per-provider IDs (Claude opus/sonnet, Gemini `Gemini 3 Pro`/`Gemini 2.5 Flash`, Codex `gpt-5-codex`/`GPT-5.1-mini`); generalized `subagent-protocol.md` Model Hierarchy and added Model Hierarchy + Validation and Tooling sections to `.agents/GEMINI.md` and `.codex/CODEX.md`.
- Reflected provider models: `.agents/agents/*.md` frontmatter set to Gemini tiers; `.codex/agents/*.toml` gained `model` keys.
- Replaced speculative `/imp-*` capability text in `.agents/GEMINI.md` and `.codex/CODEX.md` with repo-backed skill-routing, hook-behavior, and provider-tuning bullets; added Template-First and graphify pointers to both baselines.
- Added a Provider Capability Parity Matrix (9 dimensions) + Output-style Contract + Provider-Specific Surfaces note to `harness-catalog.md`; included Gemini in the Template-First clause of `documentation-protocol.md`.
- Added a Tool Scoping contract to `subagent-protocol.md` and least-privilege `tools:` frontmatter to the eight `.claude/agents/*.md`; created `.claude/output-styles/hy-home-k8s.md`.

#### Memory

- `.agents/` is git-tracked (27 files) and is the Gemini provider surface; do not describe it as ignored.
- The quality gate compares agent mirrors by stem, scope imports, and runtime-contract phrases only — `model` is not compared, so per-provider model IDs are safe to diverge.
- Gemini has no native hook/output-style file; it honors those contracts behaviorally — recorded as Partial/Gap in the parity matrix rather than as fabricated files.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS (after each phase).
- `python3 tomllib` parse of all `.codex/agents/*.toml` OK after adding model keys.

#### Handoff

- None.

### 2026-05-29 — Claude-first governance reframing (v2)

- **Date**: 2026-05-29
- **Layer**: meta
- **Status**: complete
- **Tags**: #governance #docs #validation

#### Progress

- Reconciled baseline declaration-vs-reality gaps under the Claude-canonical + governance-mapping decision: corrected `.claude/CLAUDE.md`, `.agents/GEMINI.md`, `.codex/CODEX.md` so mirror claims match disk (only `.agents/skills` is a real mirror; `.codex/skills`, `.agents/output-styles`, `.claude/workflows` are not physical dirs and are consumed via mapping or marked Gap). `.agents/hooks.json` (`{}`) documented as a placeholder.
- Verified latest model identifiers via WebSearch (2026-05-29) and corrected unverified names: GPT worker `gpt-5.4-mini`/`gpt-5.4-nano` → `GPT-5.3-Codex` (`gpt-5.3-codex` in `.codex/agents/*.toml`); confirmed Opus 4.8 / Sonnet 4.6, Gemini 3.1 Pro / 3.5 Flash, GPT-5.5. Gemini agent mirrors set to Gemini 3.1 Pro / 3.5 Flash.
- Completed the ten-dimension capability set in `harness-catalog.md`: added QA and CI/CD dimensions, a Model Selection Policy, a Support / Deferred Capabilities list, a Memory Scope Mapping, and Output-style placement criteria.
- Added a deferred-fields note to `subagent-protocol.md` (`permissionMode`/`memory`/`effort` pending schema verification).

#### Memory

- Claude-first means `.claude/` is canonical; `.agents/` and `.codex/` are adapters mapped via `docs/00.agent-governance/**`, not physical full mirrors.
- Verified model set (2026-05-29): top = Opus 4.8 / Gemini 3.1 Pro / GPT-5.5; worker = Sonnet 4.6 / Gemini 3.5 Flash / gpt-5.3-codex. Avoid unverified `gpt-5.4-*` names.
- When a baseline declares a surface, confirm it exists on disk or mark it Gap/deferred — declaration-reality drift is a recurring failure.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS after Phase A and Phases B–C.
- `grep` scan: zero residual unverified model names outside the progress ledger.
- All `.codex/agents/*.toml` parse via `tomllib`.

#### Handoff

- None.

### 2026-05-30 — Hybrid SSoT reconciliation (symlinks + per-provider agents)

- **Date**: 2026-05-30
- **Layer**: meta
- **Status**: complete
- **Tags**: #governance #docs #validation

#### Progress

- A concurrent commit (`475116b`) made `.agents/` the SSoT via symlinks for `.claude/{agents,skills,workflows,output-styles}` and `.codex/{skills,workflows,output-styles}`. This broke Claude subagents (the `.claude/agents` symlink served Gemini model frontmatter and no `tools:`). Reconciled to the user-approved hybrid: shared content (`skills/`, `workflows/`, `output-styles/`) stays symlinked to the `.agents/` SSoT; `agents/` are per-provider real files.
- Restored `.claude/agents/` as a real directory with Claude frontmatter (`opus`/`sonnet`, `.claude/CLAUDE.md` pointer, least-privilege `tools:`). `.agents/agents/*.md` (Gemini) and `.codex/agents/*.toml` (GPT) remain per-provider real files.
- Updated baselines and `harness-catalog.md` so SSoT/symlink statements match disk (skills SSoT = `.agents/skills`; `.claude`/`.codex` symlink to it).

#### Memory

- Symlinked trees share inodes: `sed -i` through a symlinked path edits the SSoT target. Verify the real target before in-place edits in this repo (hit and reverted via `git checkout` once).
- Single shared agent files cannot carry per-provider model frontmatter; keep `agents/` per-provider real, share only model-neutral content via symlink.

#### Evidence

- `bash scripts/validate-repo-quality-gates.sh .` PASS after reconciliation.
- Structure verified: `.claude/agents` real (opus/sonnet+tools), `.claude/skills|workflows|output-styles` and `.codex/skills` symlinks to `.agents/`.

#### Handoff

- Commit pending user confirmation (repo is being co-edited; avoid racing concurrent commits).

### 2026-06-01 — Claude agent surface restoration Phase 2/3

- **Date**: 2026-06-01
- **Layer**: meta
- **Status**: complete
- **Tags**: #governance #claude #validation

#### Progress

- Added and completed Phase 2/3 artifacts for restoring `.claude/agents` as real Claude-specific agent files:
  - [Plan](../../04.execution/plans/2026-06-01-claude-agent-surface-restoration.md)
  - [Task](../../04.execution/tasks/2026-06-01-claude-agent-surface-restoration.md)
- Pre-remediation inspection contradicted the older 2026-05-30 memory entry: `.claude/agents` was again a symlink to `../.agents/agents`, so prior memory was not treated as current runtime truth.
- Replaced the `.claude/agents` symlink with real Claude agent files carrying Claude `model` and least-privilege `tools:` frontmatter.
- Hardened `scripts/validate-repo-quality-gates.sh` to fail if `.claude/agents` is a symlink or if Claude agent model/tool frontmatter drifts.

#### Memory

- Before this remediation, `scripts/validate-repo-quality-gates.sh .` could pass while `.claude/agents` was a symlink, because the mirror check followed the symlink and verified stems/scope text rather than provider-specific model/tool semantics.
- Future remediation must preserve explicit checks for `test ! -L .claude/agents`, Claude `model:` tiers, and least-privilege `tools:` frontmatter.

#### Evidence

- `ls -l .claude/agents .agents/agents .codex/agents` showed `.claude/agents -> ../.agents/agents`.
- Phase 2 planning files were routed through `docs/99.templates/templates/sdlc/execution/plan.template.md` and `docs/99.templates/templates/sdlc/execution/task.template.md`.
- `test -d .claude/agents && test ! -L .claude/agents` PASS after restoration.
- `find .claude/agents -maxdepth 1 -type f -name '*.md' | sort` lists eight Claude agent files.
- `rg -n "model: Gemini|Gemini 3\\." .claude/agents` returned no matches.
- `bash scripts/validate-repo-quality-gates.sh .` PASS after validator hardening.
- Negative validator smoke in `/tmp` confirmed symlink regression fails with `.claude/agents must be a real Claude-specific directory, not a symlink`.
- Negative validator smoke in `/tmp` confirmed reduced Claude `tools:` frontmatter fails with `.claude/agents/code-reviewer.md tools must be 'Read, Grep, Glob, Bash'`.

#### Handoff

- None.

### Stage 00 Canonical Adapter Redesign

- **Date**: 2026-06-01
- **Layer**: meta
- **Status**: complete
- **Tags**: #governance #codex #claude #gemini #validation

#### Progress

- Completed Phase 3 for [Stage 00 Canonical Adapter Redesign](../../04.execution/plans/2026-06-01-stage-00-canonical-adapter-redesign.md) with task evidence in [2026-06-01-stage-00-canonical-adapter-redesign.md](../../04.execution/tasks/2026-06-01-stage-00-canonical-adapter-redesign.md).
- Added the Stage 00 canonical adapter ownership model to the governance hub, common governance mapping, harness catalog, and provider/runtime baselines.
- Normalized active shared hook path references to `docs/00.agent-governance/hooks/*.sh` and expanded validator coverage for `.agents/hooks.json`, shared hook shell coverage, pre-commit shellcheck/shfmt scope, and stale `shell-static` guide drift.
- Set authored-document template owner defaults to `platform` and recorded status/owner lifecycle expectations in the template README without turning additive lifecycle suggestions into required headings for all historical docs.
- Added branch completion strategy to `git-workflow.md` and `postflight-checklist.md`.
- Marked the older 2026-05-30 common governance plan/task as superseded, with dated links to the canonical adapter stream.

#### Memory

- Template H2 changes are broad contract changes in this repository: `validate-repo-quality-gates.sh` treats template H2 headings as required for all mapped authored documents. Additive lifecycle guidance should be documented as optional or safely backfilled before adding new required H2 headings.
- `.agents/hooks.json` is an active event-wiring surface, not a placeholder. It should be validated alongside `.codex/hooks.json`, while permission-gate claims remain Claude-specific.
- RTK may exist at `/home/hy/.local/bin/rtk` even when `rtk` is absent from PATH. If `rtk gain` cannot initialize its tracking database, do not inspect private DB/auth state; record the limitation and run underlying commands directly.

#### Evidence

- `command -v rtk` exited 1 in this shell.
- `/home/hy/.local/bin/rtk --version` returned `rtk 0.34.3`.
- `/home/hy/.local/bin/rtk gain` failed with `Failed to initialize tracking database: unable to open database file`.
- `git diff --check` PASS.
- `bash -n docs/00.agent-governance/hooks/post-validate.sh docs/00.agent-governance/hooks/lifecycle-guard.sh scripts/validate-repo-quality-gates.sh` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.

#### Handoff

- No live k3d, ArgoCD, Vault, external service, or deployment action was performed.
- Existing staged Claude agent restoration changes remain in the worktree and should be reviewed as a separate task unit if committing.

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

**P5 (complete, 2026-05-29) — Docs Governance Consistency (spec-007):**

- Template: `docs/99.templates/templates/sdlc/operations/runbook.template.md` — added `## Runbook Type` section.
- Legacy removed: `guides/0005-new-app-gitops-onboarding-guide.md`, `runbooks/0006-new-app-onboarding-runbook.md`, `plans/2026-05-24-workspace-harness-gap-analysis.md`, `tasks/2026-05-24-workspace-harness-gap-analysis.md`.
- Reference moved: `docs/90.references/audits/2026-05-24-workspace-harness-gap-analysis.md` created as thin reference wrapper.
- Policies 7/7: `## AI Agent Policy Section (If Applicable)` added to all 7 ops policy files.
- Runbooks 10/10: `## Runbook Type` standardized + `## Agent Operations (If Applicable)` added to all 10 active runbooks.
- Guides: H2 orphan sections demoted to H3 under `## Step-by-step Instructions` in 0002, 0006, 0007, 0008.
- Execution: `status: complete` → `status: done` in 12 files; `## Agent Rollout & Evaluation Gates` added to 4 plans.
- CI: `bash scripts/validate-policy-gates.sh .` added to `manifest-static` job.
- Hook: `.claude/hooks/post-validate.sh` scoped to workspace-local files only (skips absolute paths outside PROJECT_DIR).
- Spec/Plan/Task: `docs/03.specs/007-docs-governance-consistency/spec.md`, `docs/04.execution/plans/2026-05-28-docs-governance-consistency.md`, `docs/04.execution/tasks/2026-05-28-docs-governance-consistency.md` created.

### Prevention

- Run `postflight-checklist.md §6 Docs 3 Rules` before every PR.
- `settings.json` must be git-tracked; `settings.local.json` must stay `.gitignore`d.
- Runtime catalog entries in `docs/00.agent-governance/harness-catalog.md` must
  stay in sync with `.claude/agents/`, `.codex/agents/`, `.claude/skills/`,
  and the hook boundary between `.claude/settings.json` and `.codex/hooks.json`.

---

## 2026-06-01 — Phase 1 Skill-Axis Governance Audit Overlay

### Metadata

- **Date**: 2026-06-01
- **Layer**: governance, skills, qa, ci, gitops
- **Tags**: #phase1 #governance #skills #canonical-adapter #validation
- **Record type**: current-state overlay for the Stage 00 canonical adapter workstream.

### Problem

The Phase 1 objective named external process, documentation, QA, DevOps,
CI/CD, security, and Kubernetes skills that should be reflected in governance
and process guidance. The existing Stage 00 canonical adapter workstream proved
the broad model, but the named skill axes were not all explicit in the
Task-to-Skill Routing table.

### Resolution

- Updated `docs/00.agent-governance/harness-catalog.md` to add explicit routing
  for Phase 1 process/branch governance, development quality workflow, code
  review workflow, documentation format/readability, QA, CI/CD, and Kubernetes
  strategy lenses.
- Updated
  `docs/04.execution/tasks/2026-06-01-stage-00-canonical-adapter-redesign.md`
  with a `Phase 1 Skill-Axis Completion Audit` overlay.
- Recorded that `qa(ouroboros-qa)` was not present by exact local skill name;
  available alternatives are `gstack-qa`, `gstack-qa-only`, and
  `imp-qa-test-planner`.

### Evidence

- `git status --short --branch` showed a clean branch before this overlay.
- Exact named external skill paths were checked from local skill directories.
- `git diff --check` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- `/home/hy/.local/bin/node --version` PASS (`v24.14.0`).
- `/home/hy/.local/bin/rtk --version` PASS (`rtk 0.34.3`).
- `command -v node; command -v npm; command -v rtk` produced no paths in the
  current tool shell; `/home/hy/.local/bin/npm --version` failed because the
  wrapper calls `env node` and `node` was not on PATH.

### Prevention

- Future broad workspace improvement prompts that name external skills should
  update `harness-catalog.md` routing when the skill should become a durable
  strategy lens.
- Do not migrate Stage 00 templates to HADS without a separate template-policy
  plan and validation scope.

---

## 2026-06-01 — Workspace Agent Governance PRD/ARD Traceability Backfill

### Metadata

- **Date**: 2026-06-01
- **Layer**: requirements, architecture, governance, sdd
- **Tags**: #phase2 #requirements #architecture #stage00 #traceability
- **Record type**: current-state SDD traceability backfill.

### Problem

The Stage 00 canonical adapter plan and task existed and were completed, but the
upstream `docs/01.requirements` and `docs/02.architecture` stages did not have a
PRD/ARD/ADR that explicitly owned workspace AI Agent governance, Stage 00
canonical adapter architecture, or skill-axis routing requirements.

### Resolution

- Added `docs/01.requirements/2026-06-01-workspace-agent-governance-platform.md`.
- Added `docs/02.architecture/requirements/0006-workspace-agent-governance-platform.md`.
- Added `docs/02.architecture/decisions/0013-stage-00-canonical-adapter-model.md`.
- Updated the `docs/01.requirements`, `docs/02.architecture/requirements`, and
  `docs/02.architecture/decisions` README indexes.
- Added current upstream traceability overlays and Related Documents links to
  the existing Stage 00 canonical adapter plan/task without rewriting historical
  evidence.

### Evidence

- `git diff --check` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- Targeted traceability scan found the new PRD/ARD/ADR links in
  `docs/01.requirements`, `docs/02.architecture`, and the Stage 00 plan/task.
- The remaining `Parent Spec: N/A` string is explicitly marked as historical
  task evidence in the task overlay.

### Prevention

- Future governance workstreams that start directly in `docs/04.execution`
  should add or link a `docs/01.requirements` PRD and `docs/02.architecture`
  ARD/ADR when the work establishes durable workspace behavior.
- Historical `Parent Spec: N/A` task lines may remain, but current upstream
  ownership must be documented through a dated overlay when later backfilled.

---

## 2026-06-02 — Stage 00 Codex Harness Coverage Reconciliation

### Metadata

- **Date**: 2026-06-02
- **Layer**: governance, codex, skills, qa
- **Tags**: #phase1 #stage00 #codex #coverage #qa
- **Record type**: corrective traceability and approved protected-surface follow-up.

### Problem

The Phase 1 decision follow-up plan intentionally kept a narrow scope, but the
original request also named broader Stage 00/Codex harness coverage areas. The
first reconciliation linked those omitted areas to existing completed evidence,
while the QA routing row still carried the 2026-06-01 finding that the exact
`qa(ouroboros-qa)` path was absent.

### Resolution

- Added
  `docs/04.execution/plans/2026-06-02-stage-00-codex-harness-coverage-reconciliation.md`.
- Added
  `docs/04.execution/tasks/2026-06-02-stage-00-codex-harness-coverage-reconciliation.md`.
- Added a coverage reconciliation note to
  `docs/04.execution/plans/2026-06-02-phase-1-decision-follow-up.md`.
- Updated `docs/04.execution/plans/README.md` and
  `docs/04.execution/tasks/README.md` indexes for the new artifacts.
- After explicit human approval for protected-surface edits, confirmed
  `/home/hy/.codex/skills/ouroboros-qa/SKILL.md` exists and updated
  `docs/00.agent-governance/harness-catalog.md` so the QA row records the
  Codex-local path.

### Evidence

- `/home/hy/.codex/skills/ouroboros-qa/SKILL.md` existence check PASS.
- `/home/hy/.local/bin/node`, `/home/hy/.local/bin/npm`, and
  `/home/hy/.local/bin/rtk` path check PASS.
- `git diff --check` PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` PASS.
- `bash scripts/validate-repo-quality-gates.sh .` PASS.
- Protected-surface diff review PASS: no model policy, Codex TOML, CI workflow,
  Kubernetes manifest, secret, credential, live k3d, ArgoCD, Vault, or
  Kubernetes runtime mutation was performed.

### Prevention

- Treat `harness-catalog.md` as the durable source for named skill availability
  and update the exact routing row when a previously missing skill path appears.
- Human approval for protected-surface edits allows repo-tracked governance
  evidence updates, but live infrastructure and secret-bearing state still need
  separate concrete scope and validation evidence.

---

## 2026-06-02 — Current Implementation Docs Alignment And Archive Cleanup

### Metadata

- **Date**: 2026-06-02
- **Layer**: docs, architecture, qa, governance
- **Tags**: #docs #archive #current-contract #qa #gitops
- **Record type**: implementation-alignment and archive governance update.

### Problem

Active `01.requirements`, `02.architecture`, `03.specs`, and `04.execution`
documents still carried old implementation contracts or superseded-only chains
that no longer matched repo-backed desired state. Link-only or historical-marker
validation was not enough because the requested standard was comparison against
current implementation evidence.

### Resolution

- Added a current local GitOps platform PRD/ARD/ADR/Spec chain for the repo-backed
  baseline: Headlamp, ingress-nginx, ArgoCD App-of-Apps, ESO/Vault, external
  services, Kiali/Istio, Rollouts, Notifications, monitoring, and adminer.
- Added `docs/98.archive/README.md` and
  `docs/99.templates/templates/common/archive-tombstone.template.md`.
- Moved old conflicting 01-04 documents into `docs/98.archive/` with original
  path mirroring and metadata-only Tombstone bodies.
- Updated active README indexes and related-document links so active docs use
  current replacements and expose archived material only through the archive
  index.
- Updated AI Agent governance, QA/CI documentation, PR checklist, hooks, and
  `scripts/validate-repo-quality-gates.sh` to enforce archive Tombstones,
  reject active stale runtime contracts, and keep `reference.template.md` free
  of archive policy.

### Evidence

- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `bash -n docs/00.agent-governance/hooks/k8s-pre-edit.sh` — PASS.
- `bash -n docs/00.agent-governance/hooks/post-validate.sh` — PASS.
- `git diff --check` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` — PASS.
- `bash scripts/validate-gitops-structure.sh` — PASS.
- `bash scripts/validate-k8s-manifests.sh .` — PASS.
- `bash scripts/check-secret-handling.sh .` — PASS.
- `bash scripts/validate-policy-gates.sh .` — PASS.
- Active stale runtime scan over `docs/01-05` returned no stale endpoint or old
  cluster UI contract matches.
- `docs/99.templates/templates/common/reference.template.md` archive-wording scan returned no
  matches.

### Prevention

- Current implementation conflicts must be resolved by updating active docs or
  moving old docs to `docs/98.archive` Tombstones; historical or superseded
  markers are not sufficient for active docs.
- Active documents should link archived material only through
  `docs/98.archive/README.md`.
- Any future archive movement must include current replacement coverage and pass
  the repository quality gate before handoff.

---

## 2026-06-02 — Docs 01-05 Current Implementation Alignment

### Metadata

- **Date**: 2026-06-02
- **Layer**: docs, operations, qa, governance
- **Tags**: #docs #operations #archive #currentness #qa #ci
- **Record type**: implementation-alignment follow-up.

### Problem

Active `docs/05.operations` still exposed Headlamp OIDC/Keycloak guide and
runbook contracts that did not exist in the current GitOps desired state. Some
active execution docs also retained stale provider-local hook command examples
or stale CI job wording, and completed Phase 1-4 evidence still used draft
lifecycle state.

### Resolution

- Moved the Headlamp OIDC guide and Keycloak runbook to
  `docs/98.archive/05.operations/**` metadata-only Tombstones.
- Moved the superseded docs governance consistency Spec/Plan/Task snapshot to
  `docs/98.archive/**` and removed it from active Specs/Plans/Tasks indexes.
- Added `docs/04.execution/plans/2026-06-02-docs-01-05-current-implementation-alignment.md`
  and `docs/04.execution/tasks/2026-06-02-docs-01-05-current-implementation-alignment.md`.
- Extended `docs/98.archive/README.md` with 01-05 stage sections and the
  `05.operations/{guides,policies,runbooks,incidents}` mirror boundary.
- Updated active operations docs to point at current Headlamp chart/ingress/TLS
  operations and clarified HA as the local `servers: 1`, `agents: 3`
  multi-node validation baseline, not production HA.
- Hardened `scripts/validate-repo-quality-gates.sh` and QA/CI docs so active
  docs cannot reintroduce archived Headlamp OIDC, stale hook path, stale CI job,
  or missing Headlamp desired-state file contracts.

### Evidence

- `git diff --check` — PASS.
- `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash scripts/validate-gitops-structure.sh` — PASS.
- `bash scripts/validate-k8s-manifests.sh .` — PASS; optional kube-linter was
  not installed, so YAML syntax validation ran.
- `bash scripts/check-secret-handling.sh .` — PASS.
- `bash scripts/validate-policy-gates.sh .` — PASS through built-in fallback;
  optional conftest was not installed.
- Targeted active stale scan for archived Headlamp OIDC docs, moved governance
  consistency docs, stale provider hook path, stale CI job wording, and missing
  Headlamp desired-state file references returned no active hits.

### Prevention

- Treat repo desired state, scripts, CI workflow, provider/agent governance, and
  validation scripts as the currentness evidence basis for active `docs/01-05`.
- Move old or missing-contract operations docs to `docs/98.archive` Tombstones
  rather than preserving them as active operational guidance.
- Keep `reference.template.md` free of archive policy and enforce archive
  behavior through routing docs, archive Tombstones, and repo-quality gates.

## 2026-06-05 — Harness Engineering Connective Layer

### Metadata

- **Date**: 2026-06-05
- **Layer**: governance, infra, qa
- **Tags**: #harness #governance #approval-boundaries #ci #validation
- **Record type**: harness implementation map, approval boundaries, task
  contract template, validation wrapper, and PR/gate wiring.

### Problem

Harness engineering surfaces (governance, GitOps, validation scripts, CI,
secrets, operations) were already mature but spread across many files. There was
no single navigation map from surface to source/role/validation/evidence, no
single approval-boundary matrix, no harness-specific task contract template, no
one-command repo-static validation entry point, and no PR-level Harness Impact
section separating static from live evidence.

### Resolution

- Added `docs/00.agent-governance/harness-implementation-map.md` as a
  navigation map (not policy) linking each harness surface to its canonical
  owner, required repo-static validation, and evidence location.
- Added `docs/00.agent-governance/rules/approval-boundaries.md` as the single
  approval matrix: default state, approval triggers, validation, evidence, and
  rollback per surface, plus mandatory live-mutation and secret-handling policy.
- Added `docs/99.templates/templates/sdlc/specs/harness-task-contract.template.md` and registered it
  in `docs/99.templates/README.md`.
- Added `scripts/validate-harness.sh` as a repo-static wrapper over the existing
  gates (no new validation logic, no live checks) and registered it in the
  `scripts/README.md` Structure, Inventory, Classification, and Command Contract
  surfaces.
- Added a `## 8. Harness Impact` section to `.github/PULL_REQUEST_TEMPLATE.md`
  separating static evidence from operator-approved live evidence.
- Extended `scripts/validate-repo-quality-gates.sh` with existence and
  cross-reference checks for the new surfaces only (no duplication of the
  existing inventory or template checks).
- Linked the new surfaces from `harness-catalog.md`, root `README.md`, and
  `docs/05.operations/README.md`.

### Evidence

- `bash scripts/validate-harness.sh` — PASS (repo-quality, GitOps structure,
  k8s manifests, secret handling, policy gates via built-in fallback, static
  infrastructure contracts, `git diff --check`).
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- Optional `conftest` and `kube-linter` were not installed; policy and manifest
  checks ran through their documented fallbacks.
- No live k3d / ArgoCD / Vault / ESO validation was run; live runtime evidence
  is operator-approved only and was intentionally skipped.

### Prevention

- Treat new harness surfaces as a connective-layer change: update the
  implementation map, approval boundaries, and the relevant README/inventory in
  the same change set.
- Keep `validate-harness.sh` a wrapper only; add new validation logic to the
  owning validator, not to the wrapper.
- Keep `Ready` scoped to repo-static readiness; never present static PASS as
  live ArgoCD, Vault, ESO, or deployment readiness.

## 2026-06-05 — Harness Connective Layer Risk Closure

### Metadata

- **Date**: 2026-06-05
- **Layer**: governance, qa, evidence
- **Tags**: #harness #risk-closure #follow-up #validation
- **Record type**: Remaining Risk and Follow-up Task closure.

### Resolution

- Added
  [Harness Connective Layer Risk Closure](../../04.execution/tasks/2026-06-05-harness-connective-layer-risk-closure.md)
  as the durable task evidence for closing the connective-layer Remaining Risk
  and Follow-up Tasks.
- Classified optional `kube-linter` absence as a closed local-tool boundary
  because `validate-k8s-manifests.sh` documents and passes the YAML syntax
  fallback path.
- Classified optional `conftest` absence as a closed local-tool boundary
  because `validate-policy-gates.sh` documents and passes the built-in policy
  fallback path.
- Classified skipped live k3d / ArgoCD / Vault / ESO validation as an explicit
  operator-approved boundary, not as incomplete repo-static harness work.
- Confirmed the follow-up to commit logical units was completed by local
  commits `db9df84` and `9019c92`.

### Evidence

- `bash scripts/validate-harness.sh` — PASS.
- `git diff --check` — PASS.
- `git status --short` — clean at intake before closure edits.
- No live cluster, ArgoCD, Vault, ESO, Kubernetes mutation, secret value read,
  or external service action was performed.

### Handoff

- No active repo-static Remaining Risk or Follow-up Task remains for the harness
  connective-layer work.
- Future live runtime evidence remains a separate operator-approved runbook or
  incident workflow.

## 2026-06-05 — Language Boundary Alignment

### Metadata

- **Date**: 2026-06-05
- **Layer**: docs, governance, operations
- **Tags**: #language-policy #document-release #humanize-korean #stage-03 #stage-04
- **Record type**: language boundary audit, remediation, and validation.

### Progress

- Applied the requested document-release and humanize-korean skills as
  documentation synchronization and Korean-prose quality lenses.
- Audited the current language boundary across Stage 03 specs, Stage 04 plans,
  Stage 04 tasks, and Stage 05 operations documents.
- Strengthened the canonical language policy so `docs/03.specs/**/spec.md`,
  `docs/04.execution/plans/*.md`, and `docs/04.execution/tasks/*.md` are
  explicit English-first artifacts.
- Updated `spec.template.md`, `plan.template.md`, and `task.template.md` so
  newly authored specs, plans, and task records no longer ask for Korean
  overviews.
- Reinforced the operations hub with folder roles and the Korean human-facing /
  English AI-agent execution boundary.
- Converted the newly added harness connective-layer risk closure task to
  English.
- Translated legacy `docs/03.specs/**/spec.md`, `docs/04.execution/plans/*.md`,
  and `docs/04.execution/tasks/*.md` English-first artifacts to remove Korean
  body text.
- Reinforced `docs/90.references` root and subfolder READMEs with reference
  roles and the Korean human-facing / English authority-source-freshness
  boundary.
- Updated root `README.md` and `docs/README.md` so the language policy is
  visible from the primary human-facing entrypoints.
- Hardened `scripts/validate-repo-quality-gates.sh` to reject Korean syllables
  in Stage 03/04 English-first artifacts.
- Added
  [Language Boundary Alignment](../../04.execution/tasks/2026-06-05-language-boundary-alignment.md)
  as the current task record for this broader objective.

### Evidence

- A ripgrep scan for Korean syllables in `docs/03.specs/**/spec.md` returns no
  matches.
- A ripgrep scan for Korean syllables in `docs/04.execution/plans/*.md`
  excluding the human-facing README index returns no matches.
- A ripgrep scan for Korean syllables in `docs/04.execution/tasks/*.md`
  excluding the human-facing README index returns no matches.
- `scripts/validate-repo-quality-gates.sh` now includes a deterministic
  English-first Stage 03/04 language gate.

### Handoff

- Stage 03 specs, Stage 04 plans, and Stage 04 task records are now aligned
  with the English-first policy.
- Human-facing README, operations, and reference areas retain Korean where
  appropriate, with AI-agent and factual-contract fields kept English-first.

## 2026-07-03 — Reference Taxonomy and Incident Layout Alignment

### Metadata

- **Date**: 2026-07-03
- **Layer**: docs, governance, operations, templates
- **Tags**: #references #incident-management #templates #quality-gates
- **Record type**: reference taxonomy migration, incident routing contract, and validation.

### Progress

- Consolidated `docs/90.references` top-level categories to `audits`, `data`,
  `research`, `learning`, and `llm-wiki`.
- Moved repo-backed version inventory ownership into
  `docs/90.references/data/tech-stack-version-inventory.md`.
- Added `docs/90.references/data/README.md` and
  `docs/90.references/data/agent-reference-index.md` as the data reference
  category index and Agent reference boundary.
- Created commit `4ec068e` for the references category migration.
- Updated incident and postmortem routing so a real incident bundle lives at
  `docs/05.operations/incidents/YYYY/INC-###-<title>/`, with the fact record at
  `INC-###-<title>.md` and postmortem at `postmortem.md`.
- Updated Stage 00 routing, Stage 05 incidents README, SDLC template support,
  operation templates, hook hints, shared `.agents` skills, and
  `scripts/validate-repo-quality-gates.sh` to enforce the new incident layout.

### Memory

- `docs/90.references/data/` now owns repo-backed inventories, durable
  reference catalogs, and factual lookup data; do not recreate
  `docs/90.references/agents/` or `docs/90.references/versions/`.
- Incident fact records and postmortems are now same-folder siblings under an
  incident bundle directory. Relative links from either file to runbooks and
  policies use `../../../runbooks/` and `../../../policies/`.
- The repository quality gate now checks tracked incident document path shape,
  not only template heading coverage.
- In this Codex shell, `rtk` was not on PATH; `/home/hy/.local/bin/rtk --version`
  worked, but `rtk gain` could not initialize its database, so validation used
  direct shell commands without inspecting private runtime state.

### Evidence

- `bash scripts/generate-llm-wiki-index.sh --check` — PASS after the
  references migration.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS after the references
  migration.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS after the incident
  layout migration.
- `git diff --check` — PASS after the incident layout migration.

### Handoff

- No tracked incident or postmortem documents were created; the incidents stage
  remains README-only until a real event needs a record.
- `graphify-out/**` remains a historical generated graph artifact and was not
  regenerated in this pass.

## 2026-07-04 — Workspace Document Contract Normalization Spec

### Metadata

- **Date**: 2026-07-04
- **Layer**: docs, governance, templates, qa
- **Status**: in-progress
- **Tags**: #docs #governance #templates #validation

### Progress

- Created the Stage 03 design spec for a follow-up workspace document contract
  normalization pass:
  [Workspace Document Contract Normalization Spec](../../03.specs/014-workspace-document-contract-normalization/spec.md).
- Updated the Stage 03 README index to register the new spec.
- Captured the approved scope decision: active documents and historical
  evidence will both be normalized to the current frontmatter, section, and
  template contracts, while historical facts remain preserved in explicit
  historical or superseded sections.

### Memory

- For broad document-governance work, keep the repo-local Stage 03 spec in
  `docs/03.specs/<feature-id>/spec.md` when the design affects the repository
  SDLC system itself; use planned paths as code literals until Stage 04 plan and
  task documents exist.
- Historical evidence can be normalized aggressively when explicitly approved,
  but old facts must remain distinguishable from current operating guidance.

### Evidence

- Read the current Stage 99 frontmatter, routing, documentation, and SDLC
  governance support contracts before drafting the spec.
- Checked official or primary references for GitHub Actions, SLSA, OpenSSF
  Scorecard, CommonMark, YAML, OpenAPI, GraphQL, Protocol Buffers, GitHub Spec
  Kit, OWASP SAMM, and SDLC terminology.

### Handoff

- Complete spec self-review, run repository validation, commit the spec, then
  ask for user review before creating the Stage 04 implementation plan.

## 2026-07-04 — Workspace Document Contract Normalization Plan

### Metadata

- **Date**: 2026-07-04
- **Layer**: docs, governance, templates, qa
- **Status**: in-progress
- **Tags**: #docs #governance #templates #plans #validation

### Progress

- Created the Stage 04 implementation plan:
  [Workspace Document Contract Normalization Plan](../../04.execution/plans/2026-07-04-workspace-document-contract-normalization.md).
- Created the Stage 04 task record:
  [Workspace Document Contract Normalization Tasks](../../04.execution/tasks/2026-07-04-workspace-document-contract-normalization.md).
- Indexed the new Plan and Task in their stage README files.
- Split execution into six logical commits: audit inventory, contract/template
  normalization, active SDLC document application, historical evidence
  normalization, references/CI-QA alignment, and final validator
  reconciliation.

### Memory

- For broad document normalization, plan tasks should provide exact scan
  commands, target files, expected outcomes, and commit messages so subagents
  can execute without inheriting controller context.
- Historical evidence normalization requires explicit evidence preservation
  language in both the plan and task record.

### Evidence

- Read `plan.template.md` and `task.template.md` before authoring Stage 04
  documents.
- Confirmed Stage 04 README index structure and relative link basis.

### Handoff

- Run plan self-review, repository validation, and commit the Stage 04 planning
  artifacts. After user approval, execute with subagent-driven development.
