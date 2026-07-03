---
title: 'Task: Workspace Document Governance Hardening'
type: sdlc/task
status: draft
owner: platform
updated: 2026-07-03
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

## Working Rules

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
| T-003 | Harden provider entrypoint contracts for AGENTS, Claude, Codex, and Gemini surfaces. | doc | Spec / Agent Role & IO Contract | Task 3 | Provider topology scans and validator pass | platform | Open |
| T-004 | Apply document governance profiles to workspace README and authored documents. | doc | Spec / Guardrails | Task 4 | README/frontmatter/residue scans and validator pass | platform | Open |
| T-005 | Finalize deterministic validator checks, CI/QA evidence, and final review. | test | Spec / Success Criteria | Task 5 | Full local validation and final sub-agent READY | platform | Open |

## Suggested Types

- `doc`
- `test`
- `eval`
- `ops`
- `guardrail`

## Phase View

### Phase 1: Audit Inventory

- [x] T-001 Capture baseline document/provider/CI-QA audit inventory.

### Phase 2: Core Contracts

- [x] T-002 Harden core template, frontmatter, routing, Stage 00, and validator
  contracts.

### Phase 3: Provider Entrypoints

- [ ] T-003 Harden provider entrypoint contracts for AGENTS, Claude, Codex, and
  Gemini surfaces.

### Phase 4: Workspace Application

- [ ] T-004 Apply document governance profiles to workspace README and authored
  documents.

### Phase 5: Final Validation

- [ ] T-005 Finalize deterministic validator checks, CI/QA evidence, and final
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
  - `docs/90.references/audits/2026-07-03-workspace-document-governance-hardening-audit.md`
    if durable audit findings justify a separate Stage 90 report.

## Current Evidence

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
  docs/99.templates/templates/sdlc/specs/harness-task-contract.template.md
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
  [Workspace Document Governance Hardening Audit](../../90.references/audits/2026-07-03-workspace-document-governance-hardening-audit.md).
- Updated the audit index at `docs/90.references/audits/README.md`.
- Task 1 stayed audit-only: no Task 2 core contract fixes, Task 3 provider
  fixes, Task 4 workspace cleanup, or Task 5 validator changes were applied.

### T-002 Core Contract Hardening

#### Contract Changes

- Removed the feature-local README row as a second structural mapping from the
  Templates README route table. Feature-local README files remain covered by
  the generic README route.
- Updated the Template Routing Contract to make nested README targets use the
  generic README route and keep `harness-task-contract.template.md`
  supplemental rather than structural.
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

## Related Documents

- [Spec](../../03.specs/013-workspace-document-governance-hardening/spec.md)
- [Plan](../plans/2026-07-03-workspace-document-governance-hardening.md)
- [Template Documentation Contract](../../99.templates/support/documentation-contract.md)
- [Template Frontmatter Schema](../../99.templates/support/frontmatter-schema.md)
- [Template Routing Contract](../../99.templates/support/template-routing.md)
- [Agent Governance Hub](../../00.agent-governance/README.md)
- [CI/CD & QA Reference Guide](../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- [Workspace Document Governance Hardening Audit](../../90.references/audits/2026-07-03-workspace-document-governance-hardening-audit.md)
