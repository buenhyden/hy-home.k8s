---
title: 'Task: Workspace Document Governance Hardening'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-13
---

# Task: Workspace Document Governance Hardening

## Overview

This document tracks implementation and verification work for workspace
document governance hardening. It keeps the audit, contract, provider,
workspace application, and final validation work traceable to the parent Spec
and Plan.

## Inputs

- **Parent Spec**: [Workspace Document Governance Hardening Spec](../../03.specs/013-workspace-document-governance-hardening/spec.md)
- **Parent Plan**: [Workspace Document Governance Hardening Plan](../plans/2026-07-03-workspace-document-governance-hardening.md)

## Approval and Safety Boundaries

- Work audit-first and keep the current passing repository quality gate as the
  baseline.
- Every logical task must update this evidence file before commit.
- Documentation-only changes still require `git diff --check` and
  `bash scripts/validate-repo-quality-gates.sh .`.
- Repo-static validation must not be reported as live runtime readiness.
- Do not inspect secret values or mutate live Kubernetes, Argo CD, Vault,
  cloud, or publishing surfaces.
- Use sub-agent review for each major implementation unit when executing the
  plan.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Capture baseline document/provider/CI-QA audit inventory. | doc | Spec / Evaluation | Task 1 | Baseline scans, Stage 90 audit report, gate evidence | platform | Done |
| T-002 | Harden core template, frontmatter, routing, Stage 00, and validator contracts. | doc | Spec / Contracts | Task 2 | Route/profile scans and validator pass | platform | Done |
| T-003 | Harden provider entrypoint contracts for AGENTS, Claude, Codex, and Gemini surfaces. | doc | Spec / Agent Role & IO Contract | Task 3 | Provider topology scans and validator pass | platform | Done |
| T-004 | Apply document governance profiles to workspace README and authored documents. | doc | Spec / Guardrails | Task 4 | README/frontmatter/residue scans and validator pass | platform | Done |
| T-005 | Finalize deterministic validator checks, CI/QA evidence, and final review. | test | Spec / Success Criteria | Task 5 | Full local validation passed; final reviewer handoff ready | platform | Done |

### Suggested Types

- `doc`
- `test`
- `eval`
- `ops`
- `guardrail`

### Phase View

### Phase 1: Audit Inventory

- [x] T-001 Capture baseline document/provider/CI-QA audit inventory.

### Phase 2: Core Contracts

- [x] T-002 Harden core template, frontmatter, routing, Stage 00, and validator
  contracts.

### Phase 3: Provider Entrypoints

- [x] T-003 Harden provider entrypoint contracts for AGENTS, Claude, Codex, and
  Gemini surfaces.

### Phase 4: Workspace Application

- [x] T-004 Apply document governance profiles to workspace README and authored
  documents.

### Phase 5: Final Validation

- [x] T-005 Finalize deterministic validator checks, CI/QA evidence, and final
  review.

## Verification Summary

- **Test Commands**:
  - `git diff --check`
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `bash scripts/validate-harness.sh`
- **Conditional Manifest Commands**:
  - `bash infrastructure/tests/verify-contracts-static.sh`
  - `bash scripts/validate-gitops-structure.sh`
  - `bash scripts/validate-k8s-manifests.sh .`
  - `bash scripts/check-secret-handling.sh .`
  - `bash scripts/validate-policy-gates.sh .`
- **Logs / Evidence Location**:
  - This task record.
  - `docs/00.agent-governance/memory/progress.md`.
  - `docs/90.references/audits/2026-07-03-wdgh/workspace-document-governance-hardening-audit.md`
    if durable audit findings justify a separate Stage 90 report.

### Current Evidence

- Stage 03 Spec approved by user and committed in
  `ce5f6e2 docs(spec): Define workspace document governance hardening`.
- Stage 04 Plan and Task created from the approved Spec.

### T-001 Baseline Audit Inventory

#### Baseline Status

- `git status --short --branch`:

  ```text
  ## codex/template-governance-audit-enhancement
  ```

- `git diff --check` — PASS, no output.
- `bash scripts/validate-repo-quality-gates.sh .`:

  ```text
  [PASS] repository quality gates passed
  ```

#### Tracked File Inventory

- `git ls-files '*.md' '*.yaml' '*.yml' '*.graphql' '*.proto' | wc -l`:
  `480`.
- `git ls-files '*.md' | wc -l`: `358`.
- `find docs -maxdepth 1 -type d | sort` returned only the canonical docs
  taxonomy: `docs`, `docs/00.agent-governance`, `docs/01.requirements`,
  `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`,
  `docs/05.operations`, `docs/90.references`, `docs/98.archive`, and
  `docs/99.templates`. No `docs/superpowers` or other unsupported top-level
  docs folder was present.
- `find docs/99.templates/templates -maxdepth 5 -type f | sort`:

  ```text
  docs/99.templates/templates/README.md
  docs/99.templates/templates/common/archive-tombstone.template.md
  docs/99.templates/templates/common/memory.template.md
  docs/99.templates/templates/common/progress.template.md
  docs/99.templates/templates/common/readme.template.md
  docs/99.templates/templates/common/reference.template.md
  docs/99.templates/templates/sdlc/architecture/adr.template.md
  docs/99.templates/templates/sdlc/architecture/ard.template.md
  docs/99.templates/templates/sdlc/execution/plan.template.md
  docs/99.templates/templates/sdlc/execution/task.template.md
  docs/99.templates/templates/sdlc/operations/guide.template.md
  docs/99.templates/templates/sdlc/operations/incident.template.md
  docs/99.templates/templates/sdlc/operations/policy.template.md
  docs/99.templates/templates/sdlc/operations/postmortem.template.md
  docs/99.templates/templates/sdlc/operations/runbook.template.md
  docs/99.templates/templates/sdlc/requirements/prd.template.md
  docs/99.templates/templates/sdlc/specs/agent-design.template.md
  docs/99.templates/templates/sdlc/specs/api-spec.template.md
  docs/99.templates/templates/sdlc/specs/data-model.template.md
  # retired duplicate harness Task starter (removed by Spec 027)
  docs/99.templates/templates/sdlc/specs/openapi.template.yaml
  docs/99.templates/templates/sdlc/specs/schema.template.graphql
  docs/99.templates/templates/sdlc/specs/service.template.proto
  docs/99.templates/templates/sdlc/specs/spec.template.md
  docs/99.templates/templates/sdlc/specs/tests.template.md
  ```

- `find docs/99.templates/support -maxdepth 2 -type f | sort`:

  ```text
  docs/99.templates/support/README.md
  docs/99.templates/support/common-documentation-governance.md
  docs/99.templates/support/documentation-contract.md
  docs/99.templates/support/frontmatter-schema.md
  docs/99.templates/support/legacy-cleanup-rules.md
  docs/99.templates/support/sdlc-governance.md
  docs/99.templates/support/template-routing.md
  ```

- `find docs/00.agent-governance -maxdepth 3 -type f | sort`:

  ```text
  docs/00.agent-governance/README.md
  docs/00.agent-governance/common-governance.md
  docs/00.agent-governance/harness-catalog.md
  docs/00.agent-governance/harness-implementation-map.md
  docs/00.agent-governance/hooks/k8s-pre-edit.sh
  docs/00.agent-governance/hooks/lifecycle-guard.sh
  docs/00.agent-governance/hooks/post-validate.sh
  docs/00.agent-governance/hooks/session-start.sh
  docs/00.agent-governance/memory/README.md
  docs/00.agent-governance/memory/progress.md
  docs/00.agent-governance/model-policy.md
  docs/00.agent-governance/providers/agents-md.md
  docs/00.agent-governance/providers/claude.md
  docs/00.agent-governance/providers/codex.md
  docs/00.agent-governance/providers/gemini.md
  docs/00.agent-governance/rules/agentic.md
  docs/00.agent-governance/rules/approval-boundaries.md
  docs/00.agent-governance/rules/bootstrap.md
  docs/00.agent-governance/rules/document-stage-routing.md
  docs/00.agent-governance/rules/documentation-protocol.md
  docs/00.agent-governance/rules/git-workflow.md
  docs/00.agent-governance/rules/persona.md
  docs/00.agent-governance/rules/postflight-checklist.md
  docs/00.agent-governance/rules/preflight-checklist.md
  docs/00.agent-governance/rules/quality-standards.md
  docs/00.agent-governance/rules/stage-authoring-matrix.md
  docs/00.agent-governance/rules/stage-checklists.md
  docs/00.agent-governance/rules/standards.md
  docs/00.agent-governance/scopes/architecture.md
  docs/00.agent-governance/scopes/backend.md
  docs/00.agent-governance/scopes/docs.md
  docs/00.agent-governance/scopes/frontend.md
  docs/00.agent-governance/scopes/infra.md
  docs/00.agent-governance/scopes/meta.md
  docs/00.agent-governance/scopes/ops.md
  docs/00.agent-governance/scopes/product.md
  docs/00.agent-governance/scopes/qa.md
  docs/00.agent-governance/scopes/security.md
  docs/00.agent-governance/subagent-protocol.md
  ```

#### Frontmatter and README Surface Scan

- Ran the required broad frontmatter scan across root shims, `docs`,
  examples, GitOps, infrastructure, scripts, tests, Traefik, GitHub, and agent
  runtime surfaces. Output is high-volume because the pattern intentionally
  matches YAML document separators, fenced examples, generated Markdown
  frontmatter literals, template frontmatter, and authored document metadata.
- README-only focused metadata scan:

  ```text
  examples/aws/docs/README.md:72:---
  ```

  This is a body horizontal rule after `## Related Documents`, not YAML
  frontmatter. No README frontmatter was found.
- README deprecated related-document heading scan:

  ```text
  docs/00.agent-governance/README.md:99:## Related Folders
  ```

  This is current-contract README heading drift and is routed to T-004/T-005.
- Historical matches inside `docs/00.agent-governance/memory/progress.md` were
  treated as evidence and not active contract drift.

#### Provider and CI/QA Surface Scan

- Ran the required provider scan across `AGENTS.md`, `CLAUDE.md`,
  `GEMINI.md`, `.agents`, `.claude`, `.codex`, and Stage 00 governance.
  Provider-specific claims were concentrated in root shims, provider notes,
  runtime overlays, hook JSON/settings, the harness catalog, and subagent
  protocol. No unsupported provider documentation tree was found during T-001.
- Ran the required CI/QA scan across `.github`, `docs`, `scripts`, `tests`,
  and the root README. CI/QA claims trace to `.github/workflows/ci.yml`,
  `.github/ABOUT.md`, `scripts/README.md`, `tests/README.md`, and the CI/CD QA
  guide.
- Durable CI/QA drift found:

  ```text
  tests/README.md:58 uses the legacy Claude provider-local hook directory in
  the shell syntax command.
  ```

  The current CI/CD QA guide points hook syntax checks at
  `docs/00.agent-governance/hooks/<hook-name>.sh`; this is routed to T-004/T-005.

#### Audit Report Decision

- Created the Stage 90 audit report because durable findings exist:
  [Workspace Document Governance Hardening Audit](../../90.references/audits/2026-07-03-wdgh/workspace-document-governance-hardening-audit.md).
- Updated the audit index at `docs/90.references/audits/README.md`.
- Task 1 stayed audit-only: no Task 2 core contract fixes, Task 3 provider
  fixes, Task 4 workspace cleanup, or Task 5 validator changes were applied.

### T-002 Core Contract Hardening

#### Contract Changes

- Removed the feature-local README row as a second structural mapping from the
  Templates README route table. Feature-local README files remain covered by
  the generic README route.
- Updated the Template Routing Contract to make nested README targets use the
  generic README route and kept the duplicate harness Task starter
  supplemental rather than structural at that time; Spec 027 later retired it.
- Updated Stage 00 routing, documentation protocol, and authoring matrix docs
  so exact target-pattern/template routing points to
  `docs/99.templates/support/template-routing.md` instead of carrying a full
  duplicate map.
- Added deterministic validator coverage that compares the Templates README
  route table with the support Current Route Map and checks documented Markdown
  routes against README, memory/progress, or structural stage mapping coverage.
- Reworded active core-contract denylist prose so focused residue scans do not
  self-match on legacy strings outside templates and historical evidence.

#### Verification Evidence

- Route map scan:

  ```text
  rg -n "Template-Folder Mapping|Current Route Map|required_stage_templates|template_expected_types|template_locations" docs/99.templates/README.md docs/99.templates/support scripts/validate-repo-quality-gates.sh
  ```

  PASS. README mapping, support route map, and validator mappings are aligned.
- Frontmatter profile scan:

  ```text
  rg -n "sdlc/prd|sdlc/ard|sdlc/adr|sdlc/spec|sdlc/plan|sdlc/task|sdlc/guide|sdlc/policy|sdlc/runbook|sdlc/incident|sdlc/postmortem|content/reference|content/archive-tombstone|governance/template-support|governance/reference|governance/memory" docs/99.templates/support/frontmatter-schema.md docs/99.templates/templates scripts/validate-repo-quality-gates.sh
  ```

  PASS. Markdown template frontmatter, support schema, and validator expected
  types agree; README/progress templates remain frontmatter-free, and native
  OpenAPI, GraphQL, and protobuf templates remain native.
- Focused flat route scan:

  ```text
  rg -n "docs/99\\.templates/[a-z0-9-]+\\.template\\.(md|yaml|graphql|proto)" docs scripts .codex AGENTS.md RTK.md
  ```

  PASS, no matches.
- Focused support stale-wording scan:

  ```text
  rg -n "Phase [1-4]|during the migration|after Phase|current and target" docs/99.templates/support
  ```

  PASS, no matches.
- Focused legacy residue scan returned only template starter markers,
  historical completed Plan/Task/progress evidence, and one active authored
  runbook negative-checklist phrase in
  `docs/05.operations/runbooks/0011-reference-maintenance-runbook.md`; the
  authored runbook cleanup is outside T-002 and remains routed to T-004/T-005.
- `git diff --check` — PASS, no output.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.

#### Handoff

- T-002 is complete for core contract surfaces.
- No live Kubernetes, Argo CD, Vault, cloud, provider runtime, publishing, or
  secret-value checks were run.

### T-003 Provider Entrypoint Hardening

#### Provider and Shared Adapter Changes

- Kept root `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` as thin provider shims
  and clarified that `AGENTS.md` is the Codex/GPT gateway, not the Claude or
  Gemini loading path.
- Updated Claude and Gemini provider-native agent bootstrap lines so Claude
  agents load `CLAUDE.md` and Gemini agents load `GEMINI.md`; Codex agent
  mirrors continue to load `AGENTS.md`.
- Aligned `.claude/CLAUDE.md`, `.codex/CODEX.md`, and `.agents/GEMINI.md` so
  provider hook behavior is provider-specific: Claude settings are the native
  permission and hook surface, while `.codex/hooks.json` and
  `.agents/hooks.json` remain context/validation wiring.
- Updated shared `.agents` rules, workflows, and docs skills to route exact
  target-pattern/template decisions through
  `docs/99.templates/support/template-routing.md` instead of carrying a
  duplicate route matrix.
- Clarified Stage 00 common governance, provider notes, harness catalog,
  subagent protocol, and meta scope ownership so `.agents/skills`,
  `.agents/workflows`, and `.agents/output-styles` remain the shared asset
  source while provider-specific agent files remain per-provider.
- Updated root `README.md` provider-entrypoint wording only. Broader README
  heading cleanup remains routed to T-004/T-005.
- Review remediation tightened the three cited active runtime/provider
  references so `.agents/GEMINI.md`, `.codex/CODEX.md`, and
  `docs/00.agent-governance/rules/document-stage-routing.md` now point
  directly to `docs/99.templates/support/template-routing.md` for route
  selection. `.agents/GEMINI.md` now describes only shared
  skills/workflows/output-style symlink views and keeps provider-native files
  as real adapter/runtime surfaces.

#### Focused Scan Evidence

- Required provider/hook scan was run against active provider and Stage 00
  surfaces. Active matches were expected shared hook paths, provider hook JSON,
  Claude settings, and hook-boundary prose. The stale strings
  `CLAUDE.md + AGENTS.md`, `AGENTS.md only`, `Security Without Hooks`,
  `Not yet supported`, `Key Differences`, and the old Claude/Gemini
  `Load AGENTS.md` bootstrap forms returned no active matches.
- Required template residue scan was run against active provider and Stage 00
  surfaces. The only match was
  `.claude/hookify.postflight-reminder.local.md`, an ignored local advisory
  file; it was not edited or treated as shared policy.
- `DESIGN.md` is absent in this checkout, so the required scans were rerun
  against the existing requested surfaces and the absence is recorded here.
- Runtime topology inspection confirmed `.claude/skills`,
  `.claude/workflows`, `.claude/output-styles`, `.codex/skills`,
  `.codex/workflows`, and `.codex/output-styles` are symlinks to `.agents/*`,
  while `.claude/agents`, `.agents/agents`, and `.codex/agents` are
  provider-specific agent surfaces.
- RTK limitation repeated: `rtk` is not on PATH; `/home/hy/.local/bin/rtk
  --version` reported `rtk 0.34.3`; `/home/hy/.local/bin/rtk gain` could not
  initialize its tracking database. Required validation commands were run
  directly.

#### Verification Evidence

- `git diff --check` — PASS, no output.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS, no output.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS:

  ```text
  [PASS] repository quality gates passed
  ```

- `bash scripts/validate-harness.sh` — PASS. Optional `kube-linter` and
  `conftest` were not installed; the harness script used YAML syntax checks
  and the built-in policy fallback.
- Review remediation focused scans — PASS: the three cited files point to
  `docs/99.templates/support/template-routing.md`, and `.agents/GEMINI.md` no
  longer claims all of `.claude/` or `.codex/` symlink to `.agents/`.

#### Handoff

- T-003 is complete for provider entrypoint/profile alignment.
- No Task 4 authored-document cleanup, Task 5 final reconciliation, live
  Kubernetes, Argo CD, Vault, cloud, publishing, provider-runtime, or
  secret-value checks were run.

### T-004 Workspace Document Application

#### Document Cleanup Changes

- Normalized `docs/00.agent-governance/README.md` by moving folder inventory
  content into `## Structure` and removing the duplicate deprecated related
  folder heading.
- Removed the body delimiter after `## Related Documents` from
  `examples/aws/docs/README.md` and kept the task-reference sentence inside
  `## How to Work in This Area`.
- Updated `tests/README.md` shell syntax guidance from the old provider-local
  hook path to `docs/00.agent-governance/hooks`.
- Reworded the active checklist item in
  `docs/05.operations/runbooks/0011-reference-maintenance-runbook.md` so it
  refers to current `## Related Documents` usage without preserving the legacy
  heading literal as current guidance.
- Updated root/docs README onboarding text and active doc-writer/output-style
  guidance so exact target-pattern/template selection points to
  `docs/99.templates/support/template-routing.md`; the Templates README remains
  an inventory summary.
- Replaced duplicated route lists in `.agents/hooks.json`,
  `.claude/settings.json`, and `.codex/hooks.json` with support-contract
  routing guidance.
- Updated `docs/00.agent-governance/hooks/k8s-pre-edit.sh` advisory output to
  name the support routing contract while preserving the Templates README as
  inventory context required by the repository quality gate.

#### Focused Scan Evidence

- README deprecated related-heading scan:

  ```text
  rg -n '^## (Related Folders|Related Files|References|See Also|Links|Deprecated|Legacy)$' README.md .github docs examples gitops infrastructure policy scripts tests traefik .agents .claude .codex
  ```

  PASS, no matches.
- README frontmatter scan:

  ```text
  rg -n '^---$|^title:|^type:|^status:|^owner:|^updated:' README.md $(git ls-files '*README.md')
  ```

  PASS, no matches.
- Changed-surface residue scan checked the touched files for stale
  provider-local hook path wording, body delimiter wording, legacy README
  heading text, and old template-routing owner wording. PASS, no matches.
- Support-routing confirmation scan returned the touched README, doc-writer,
  output-style, hook, and provider custom-instruction surfaces pointing to
  `docs/99.templates/support/template-routing.md`.
- Broad high-risk command scan was reviewed. Remaining matches are unchanged
  prohibited-boundary, bootstrap-only, operator-approved, or historical
  evidence references; this Task 4 change introduced no new live mutation,
  secret-value, push, publish, or external-system action.

#### Verification Evidence

- `jq empty .agents/hooks.json .claude/settings.json .codex/hooks.json` —
  PASS, no output.
- `bash -n docs/00.agent-governance/hooks/k8s-pre-edit.sh` — PASS, no output.
- `git diff --check` — PASS, no output.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS, no output.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS:

  ```text
  [PASS] repository quality gates passed
  ```

#### Review Notes

- A callable subagent dispatcher was not exposed in this Codex tool surface.
  The Task 4 implementation therefore used the same staged discipline in this
  session: implement, run focused spec-compliance scans, run focused quality
  scans, and run the repo quality gate before commit.
- RTK limitation repeated: `rtk` is not on PATH; `/home/hy/.local/bin/rtk
  --version` works, but `/home/hy/.local/bin/rtk gain` cannot initialize its
  tracking database. Required validation commands were run directly.

#### Handoff

- T-004 is complete for active README/authored-document cleanup.
- T-005 should perform final reconciliation and decide whether additional
  deterministic validator coverage is warranted for README heading/profile or
  onboarding route-owner drift.
- No live Kubernetes, Argo CD, Vault, cloud, publishing, provider-runtime, or
  secret-value checks were run.

### T-005 Validator, CI/QA Evidence, and Final Review

#### Validator Decisions

- Added path-scoped deterministic checks for active README deprecated heading
  families, including legacy related-reference, folder/file, generic link,
  deprecation, and legacy headings.
- Reworked active template-residue scanning to cover root shims, docs,
  examples, GitOps, infrastructure, policy, scripts, tests, and Traefik
  surfaces while skipping `docs/99.templates/templates/**`,
  `docs/90.references/audits/**`, `docs/98.archive/**`, and the progress
  ledger so historical evidence is not rejected.
- Added deterministic route-owner checks for active onboarding, provider,
  hook, workflow, and doc-writer surfaces that must point exact template
  selection at `docs/99.templates/support/template-routing.md`.
- Extended shared-hook path coverage to `tests/README.md`, preserving
  `docs/00.agent-governance/hooks` as the active shell syntax owner.
- Added CI/QA source-basis checks requiring `.github/ABOUT.md` and the CI/CD
  QA guide to point external GitHub Actions/tooling claims back to the parent
  Spec's official-source basis. No `.github/workflows/ci.yml` behavior was
  changed.

#### CI/QA Reconciliation

- Compared `.github/workflows/ci.yml`, `.github/ABOUT.md`,
  `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md`,
  `scripts/README.md`, and `tests/README.md`.
- Confirmed `ci.yml` remains the required QA gate for branch policy,
  pre-commit, repo-quality-static, manifest-static, and `ci-summary`.
- Confirmed `generate-changelog.yml` is documented as release-evidence
  automation, while `labeler.yml`, `greetings.yml`, and `stale.yml` are
  repository maintenance automations, not QA gates.
- Confirmed local equivalents remain accurate:
  `repo-quality-static` maps to
  `bash scripts/validate-repo-quality-gates.sh .`, and `manifest-static` maps
  to `verify-contracts-static.sh`, GitOps structure, manifest syntax, secret
  handling, and policy gates.
- Added source-basis text to `.github/ABOUT.md` and the CI/CD QA guide, and
  updated the operations guides README index for the guide date.

#### Verification Evidence

- `rtk` limitation repeated: `rtk` is not on PATH; `/home/hy/.local/bin/rtk
  --version` works, but `/home/hy/.local/bin/rtk gain` cannot initialize its
  tracking database. Required validation commands were run directly.
- `git diff --check` — PASS, no output.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS, no output.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS:

  ```text
  [PASS] repository quality gates passed
  ```

- `bash scripts/validate-harness.sh` — PASS. The harness executed
  repository quality gates, GitOps structure, Kubernetes manifest syntax,
  secret handling, policy gates, static infrastructure contracts, and diff
  hygiene.
- Optional tooling limitations during harness execution:
  `kube-linter` was not installed, so manifest validation used YAML syntax
  checks only; `conftest` was not installed, so policy validation used the
  built-in fallback. Both fallback paths passed.

#### Review Boundary

- A callable final-review subagent dispatcher was not used by the Task 5
  implementer because the Task 5 assignment delegates the independent final
  sub-agent review to the parent agent after this commit.
- Handoff evidence is ready for that parent-dispatched reviewer. No live
  Kubernetes, Argo CD, Vault, cloud, publishing, provider-runtime, push, merge,
  or secret-value action was performed.

## Traceability

- [Spec](../../03.specs/013-workspace-document-governance-hardening/spec.md)
- [Plan](../plans/2026-07-03-workspace-document-governance-hardening.md)
- [Template Documentation Contract](../../99.templates/support/documentation-contract.md)
- [Template Frontmatter Schema](../../99.templates/support/frontmatter-schema.md)
- [Template Routing Contract](../../99.templates/support/template-routing.md)
- [Agent Governance Hub](../../00.agent-governance/README.md)
- [CI/CD & QA Reference Guide](../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- [Workspace Document Governance Hardening Audit](../../90.references/audits/2026-07-03-wdgh/workspace-document-governance-hardening-audit.md)
