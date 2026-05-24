---
title: 'Workspace Harness Gap Analysis Technical Specification'
type: spec
status: active
owner: 'platform'
updated: 2026-05-24
---

# Workspace Harness Gap Analysis Technical Specification (Spec)

## Overview (KR)

이 문서는 `hy-home.k8s` 워크스페이스가 WSL2, WSL Linux native Docker, k3d,
ArgoCD GitOps, External Secrets, Vault, PostgreSQL, Valkey, SDD(Spec-Driven
Development), QA(Quality Assurance), CI/CD(Continuous Integration/Continuous
Delivery), AI Agent 협업 규칙을 일관되게 지탱하는지 감사하고 보강하는 기술 계약이다.

## Strategic Boundaries & Non-goals

This spec owns the repository-static improvement contract for the workspace
harness gap analysis. The original pass did not approve live cluster mutation,
direct ArgoCD sync, Vault writes, Kubernetes resource semantic changes, GitHub
branch protection changes, or plaintext secret handling.

On 2026-05-24 the human approved a separate P3 follow-up for ArgoCD, Vault,
External Secrets, secret, and runtime remediation. That approval allows
repository-backed desired-state changes and read-only runtime metadata checks
under the linked P3 plan. Direct live mutation, secret value inspection, Vault
KV writes, ArgoCD sync, and plaintext secret handling remain out of scope.

## Related Inputs

- **PRD**: N/A. This is a workspace governance and validation improvement.
- **ARD**: [../02.architecture/requirements/0001-wsl-k3d-argocd-platform.md](../../02.architecture/requirements/0001-wsl-k3d-argocd-platform.md)
- **Related ADRs**:
  [ADR-0002](../../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md),
  [ADR-0003](../../02.architecture/decisions/0003-eso-vault-k8s-auth.md),
  [ADR-0004](../../02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md)

## Contracts

- **Config Contract**: root gateway files remain thin; recurring workflow and
  task-to-skill routing are recorded in `docs/00.agent-governance/harness-catalog.md`.
- **Data / Interface Contract**: no new runtime API is introduced. New
  execution evidence lives in `docs/03.specs/`, `docs/04.execution/plans/`,
  `docs/04.execution/tasks/`, and `docs/00.agent-governance/memory/progress.md`.
- **Governance Contract**: all findings are classified as low, medium, or high
  risk. High-risk runtime, secret, ArgoCD, and CI/CD policy items are either
  deferred with explicit pre-checks or handled through a separate approved plan
  with its own verification and rollback record.

## Core Design

- **Component Boundary**: repository documentation, governance, validation
  scripts, and static GitOps checks only.
- **Key Dependencies**: existing subagent review results, repo templates,
  `scripts/validate-repo-quality-gates.sh`, `scripts/validate-gitops-structure.sh`,
  and static infrastructure tests.
- **Tech Stack**: Bash, Markdown, YAML, ArgoCD Application manifests, repo-local
  Claude/Codex harness files.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Coverage Ledger, Integrated Gap Analysis,
  Implementation Plan, checklist gate, and Final Report are stored as Markdown
  tables in the linked plan and task documents.
- **Migration / Transition Plan**: no data migration is included. A temporary
  empty spec directory from the interrupted planning turn is reused by adding
  this `spec.md` file.

## Interfaces & Data Structures

### Core Interfaces

```text
Coverage Ledger -> Integrated Gap Analysis -> Implementation Plan -> Task evidence -> Verification summary
```

## API Contract (If Applicable)

Not applicable. This work does not expose an API.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Codex implements the approved plan using previous subagent
  review outputs as investigation input.
- **Inputs**: six role-based review results, baseline static validation, repo
  governance documents, and the user-approved implementation plan.
- **Outputs**: updated spec/task/plan artifacts, scoped P1/P2 changes, deferred
  P3 follow-up records, and verification evidence.
- **Success Definition**: repository-static checks pass or limitations are
  recorded, and all high-risk items remain planned rather than silently omitted.

## Tools & Tool Contract (If Applicable)

- **Tool List**: `rg`, `find`, `bash`, `python3`, repo validation scripts.
- **Permission Boundary**: no live `kubectl`, ArgoCD, Vault, cloud, or secret
  value inspection is performed without explicit approval. Approved live checks
  are limited to metadata/status reads unless a follow-up explicitly authorizes
  mutation.
- **Failure Handling**: if repo-static validation fails, fix the scoped change
  or roll back the affected file set.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: `AGENTS.md` remains the thin gateway.
  Detailed workflow routing stays in governance docs.
- **Policy Constraints**: do not reduce scope, omit high-risk gaps, bypass
  safety gates, or implement high-risk runtime changes without a linked approval
  plan, verification method, and rollback path.
- **Versioning Rule**: this is a dated repository-static snapshot for
  2026-05-24.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: previous subagent results and baseline command output.
- **Long-term Memory**: append a concise progress entry to
  `docs/00.agent-governance/memory/progress.md`.
- **Retrieval Boundary**: memory is supporting context; current repository files
  remain authoritative.

## Guardrails (If Applicable)

- **Input Guardrails**: compare prompt requests against repository governance
  before editing.
- **Output Guardrails**: all new authored documents must use the template
  contract and `Related Documents`.
- **Blocked Conditions**: direct live mutation, plaintext secret writes, or
  missing rollback path.
- **Escalation Rule**: high-risk runtime or policy decisions require human
  approval and a separate implementation plan.

## Evaluation (If Applicable)

- **Eval Types**: static repository validation and documentation conformance.
- **Metrics**: zero repo quality errors, generated LLM Wiki current, GitOps
  structure validation pass, manifest syntax pass, secret scan pass, static
  contract pass, shell syntax pass, diff whitespace pass.
- **Datasets / Fixtures**: existing repository files and manifests.
- **How to Run**: use the verification commands in the linked plan.

## Edge Cases & Error Handling

- **Empty root app set**: `scripts/validate-gitops-structure.sh` must fail when
  `gitops/apps/root` has no non-kustomization ArgoCD root app manifests.
- **Local optional tools absent**: record skipped tools instead of treating them
  as passed.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: high-risk GitOps or secret changes appear necessary.
- **Fallback**: defer the change and record pre-checks in the plan.
- **Human Escalation**: required for live k3d/ArgoCD/Vault mutation or runtime
  policy changes. The 2026-05-24 P3 follow-up approval covers repo-backed
  ArgoCD/Vault/ESO desired-state changes and read-only metadata checks only.

## Verification Commands

```bash
bash scripts/validate-repo-quality-gates.sh .
bash scripts/generate-llm-wiki-index.sh --check
bash scripts/validate-gitops-structure.sh
bash scripts/validate-k8s-manifests.sh .
bash scripts/check-secret-handling.sh .
bash infrastructure/tests/verify-contracts-static.sh
find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +
python3 -m json.tool .claude/settings.json
python3 -m json.tool .codex/hooks.json
git diff --check
```

## Success Criteria & Verification Plan

- **VAL-SPC-006-001**: Coverage Ledger, Integrated Gap Analysis, and
  Implementation Plan are recorded.
- **VAL-SPC-006-002**: P1/P2 scoped changes pass repo-static validation.
- **VAL-SPC-006-003**: P3 high-risk items are deferred with pre-checks and
  follow-up work.
- **VAL-SPC-006-004**: Required external `SKILL.md` paths are checked and
  missing paths, if any, are recorded as Gaps.
- **VAL-SPC-006-005**: Repeated broad workspace audit workflow is captured in a
  repo-local Skill or explicitly deferred with rationale.
- **VAL-SPC-006-006**: Hybrid refresh evidence preserves current role-based
  subagent results, path-level external skill checks, repo-static verification,
  and any new safe P1/P2 guardrail changes.
- **VAL-SPC-006-007**: Named additive review skills are recorded with applied,
  skipped, missing, or conflict status, and any design-only skill boundary is
  preserved in the linked plan/task.
- **VAL-SPC-006-008**: `superpowers:brainstorming` is applied as a design lens
  for initial-contract delta review, with alternatives, selected approach,
  skipped default design-doc gate rationale, implementation plan, and
  verification evidence preserved in canonical SDD artifacts.
- **VAL-SPC-006-009**: approved P3 ArgoCD/Vault/ESO secret/runtime remediation
  is implemented through repository desired-state changes, static contract
  validation, and read-only runtime metadata checks with unavailable-live-state
  results recorded instead of treated as passed.
- **VAL-SPC-006-010**: `gstack-plan-ceo-review` is applied as a HOLD SCOPE
  current-state review for first-input coverage drift, with exact named skill
  path evidence, P3 supersession status, implementation plan, and verification
  preserved in canonical SDD artifacts.
- **VAL-SPC-006-011**: `superpowers:executing-plans` is applied to the CEO
  review plan delta, with plan load/review/execution, required sub-skill path
  evidence, verification, and finish boundary preserved in canonical SDD
  artifacts.
- **VAL-SPC-006-012**: `skill-creator`, `skillify`, `skill-developer`, and
  `skill-improver` are applied as skill-quality lenses for the repo-local
  `workspace-harness-audit` Skill, with not-applicable boundaries and skipped
  automated reviewer limits recorded.

## Related Documents

- **Plan**: [../../04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md](../../04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md)
- **P3 Plan**: [../../04.execution/plans/2026-05-24-p3-gitops-secret-runtime-remediation.md](../../04.execution/plans/2026-05-24-p3-gitops-secret-runtime-remediation.md)
- **Tasks**: [../../04.execution/tasks/2026-05-24-workspace-harness-gap-analysis.md](../../04.execution/tasks/2026-05-24-workspace-harness-gap-analysis.md)
- **P3 Tasks**: [../../04.execution/tasks/2026-05-24-p3-gitops-secret-runtime-remediation.md](../../04.execution/tasks/2026-05-24-p3-gitops-secret-runtime-remediation.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Subagent Protocol**: [../../00.agent-governance/subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)
- **Workspace Harness Audit Skill**: [../../../.claude/skills/workspace-harness-audit/skill.md](../../../.claude/skills/workspace-harness-audit/skill.md)
- **Scripts README**: [../../../scripts/README.md](../../../scripts/README.md)
