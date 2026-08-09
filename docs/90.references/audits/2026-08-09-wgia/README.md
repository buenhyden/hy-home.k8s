# 2026-08-09 Workspace Governance Implementation Audit

## Overview

This Stage 90 pack is the draft successor foundation for a repository-wide
workspace governance audit. It routes each requested scope to one report and
heading, freezes repository evidence to one exact Git tree, and establishes
finding, source, review, and freshness conventions for the later topic audits.
It is descriptive evidence and cannot redefine current policy, machine
contracts, workflows, permissions, document routes, or operations.

The collection's Current pointer remains the 2026-07-11 audit until WGIA-012
performs the separately validated atomic cutover. A draft report records only
the initial repository-static inventory and a conservative verdict; its topic
is not complete and is never treated as `Aligned` merely because an owner or
supporting surface exists.

## Snapshot Contract

- Pack role: Draft successor foundation; not Current.
- Observation date: 2026-08-09.
- Observation commit: `50628b84165479b03efc0a25be075a49c91a9aef`.
- Observation tree: 848 tracked files, including 461 under `docs/`, 48 under
  `scripts/`, 67 under `tests/`, and 16 under `.github/`.
- Protected boundary: the observation tree contains 44 Stage 98 files; this
  work does not modify any `docs/98.archive/**` path.
- Completion owner: the paired [Task](../../../04.execution/tasks/2026-08-09-workspace-governance-audit-and-remediation.md).
- Current-audit transition owner: WGIA-012, not this foundation task.

### Inventory Method

The baseline was read from the pinned Git tree with `git ls-tree -r
--name-only`, not inferred from older audits. Counts are inventory facts only;
they do not establish correctness, runtime consumption, or topic completeness.
Canonical-owner evidence is classified as policy owner, machine owner, human
index, evidence producer, or historical snapshot. A report links to those
owners without copying their full contracts into Stage 90.

### Request Coverage Matrix

Each row has one linked primary report-and-heading owner. `Partial` means that
the current workspace surface was identified at the observation commit but the
later topic audit and independent review are still pending.

| Request ID | Requested scope | Primary owner | Workspace evidence | Evidence depth | Verdict |
| --- | --- | --- | --- | --- | --- |
| REQ-WGA-001 | Purpose | [Workspace purpose](workspace-purpose-governance-and-operating-contracts.md#workspace-purpose) | `README.md`; `docs/00.agent-governance/rules/bootstrap.md` | `repository-static` | `Aligned` |
| REQ-WGA-002 | Roles | [Workspace roles](workspace-purpose-governance-and-operating-contracts.md#workspace-roles) | `docs/00.agent-governance/contracts/harness-contract.json`; `docs/00.agent-governance/harness-catalog.md`; `README.md` | `repository-static` | `Partial` |
| REQ-WGA-003 | CI/CD | [CI/CD](ci-cd-github-actions-qa-and-validation.md#cicd) | `.github/workflows/ci.yml`; `.github/workflows/generate-changelog.yml`; `docs/00.agent-governance/rules/quality-standards.md` | `repository-static` | `Partial` |
| REQ-WGA-004 | GitHub Actions | [GitHub Actions](ci-cd-github-actions-qa-and-validation.md#github-actions) | `.github/workflows/ci.yml`; `scripts/validate-github-actions-security.py`; `scripts/validate-agent-governance-ci.py` | `repository-static` | `Aligned` |
| REQ-WGA-005 | Spec-driven development | [Spec-driven development](spec-driven-sdlc-documentation-and-templates.md#spec-driven-development) | `docs/99.templates/support/document-profiles.json`; `docs/99.templates/support/sdlc-governance.md`; `docs/00.agent-governance/rules/stage-authoring-matrix.md` | `repository-static` | `Aligned` |
| REQ-WGA-006 | Harness engineering | [Harness engineering](harness-loop-fixtures-scripts-and-blockers.md#harness-engineering) | `docs/00.agent-governance/contracts/harness-contract.json`; `scripts/validate-agent-harness-contract.py`; `scripts/validate-agent-harness-semantics.py` | `repository-static` | `Partial` |
| REQ-WGA-007 | Loop engineering | [Loop engineering](harness-loop-fixtures-scripts-and-blockers.md#loop-engineering) | `docs/00.agent-governance/contracts/agent-loop-lifecycle.json`; `docs/00.agent-governance/contracts/agent-checkpoint.schema.json`; `scripts/validate-agent-loop-lifecycle.py`; `scripts/validate-agent-checkpoint.py` | `repository-static` | `Partial` |
| REQ-WGA-008 | QA | [QA](ci-cd-github-actions-qa-and-validation.md#qa) | `docs/00.agent-governance/rules/quality-standards.md`; `docs/00.agent-governance/contracts/validation-surfaces.json`; `tests/README.md` | `repository-static` | `Aligned` |
| REQ-WGA-009 | Formatting | [Formatting](ci-cd-github-actions-qa-and-validation.md#formatting) | `.editorconfig`; `.pre-commit-config.yaml`; `docs/00.agent-governance/rules/quality-standards.md` | `repository-static` | `DEFER` |
| REQ-WGA-010 | Linting | [Linting](ci-cd-github-actions-qa-and-validation.md#linting) | `.pre-commit-config.yaml`; `scripts/validate-repo-quality-gates.sh`; `tests/README.md` | `repository-static` | `Aligned` |
| REQ-WGA-011 | Overview | [Overview](README.md#overview) | `README.md`; `docs/90.references/audits/README.md` | `repository-static` | `Partial` |
| REQ-WGA-012 | Operating contracts | [Operating contracts](workspace-purpose-governance-and-operating-contracts.md#operating-contracts) | `AGENTS.md`; `README.md`; `docs/00.agent-governance/rules/bootstrap.md`; `docs/00.agent-governance/rules/approval-boundaries.md`; `docs/00.agent-governance/rules/quality-standards.md` | `repository-static` | `Partial` |
| REQ-WGA-013 | Fixtures | [Fixtures](harness-loop-fixtures-scripts-and-blockers.md#fixtures) | `tests/fixtures/`; `tests/README.md`; `scripts/README.md` | `repository-static` | `Aligned` |
| REQ-WGA-014 | Blockers | [Blockers](harness-loop-fixtures-scripts-and-blockers.md#blockers) | `docs/00.agent-governance/contracts/agent-loop-lifecycle.json`; `docs/00.agent-governance/rules/approval-boundaries.md`; `docs/04.execution/tasks/2026-08-09-workspace-governance-audit-and-remediation.md` | `repository-static` | `Partial` |
| REQ-WGA-015 | General checks | [General checks](ci-cd-github-actions-qa-and-validation.md#general-checks) | `scripts/validate-repo-quality-gates.sh`; `scripts/run-validation-lane.py`; `docs/00.agent-governance/contracts/validation-surfaces.json` | `repository-static` | `Aligned` |
| REQ-WGA-016 | Templates | [Templates](spec-driven-sdlc-documentation-and-templates.md#templates) | `docs/99.templates/support/document-profiles.json`; `docs/99.templates/templates/README.md`; `docs/03.specs/052-document-taxonomy-consolidation/spec.md` | `repository-static` | `Partial` |
| REQ-WGA-017 | Scripts | [Scripts](harness-loop-fixtures-scripts-and-blockers.md#scripts) | `scripts/README.md`; `scripts/archive_cutover_manifest.py`; `scripts/reference_information_architecture.py`; `scripts/validate-repo-quality-gates.sh` | `repository-static` | `Aligned` |
| REQ-WGA-018 | Integration guides | [Integration guides](spec-driven-sdlc-documentation-and-templates.md#integration-guides) | `docs/05.operations/guides/README.md`; `docs/99.templates/support/document-profiles.json`; `docs/03.specs/052-document-taxonomy-consolidation/spec.md` | `repository-static` | `Partial` |
| REQ-WGA-019 | Documents and documentation | [Documents and documentation](spec-driven-sdlc-documentation-and-templates.md#documents-and-documentation) | `docs/99.templates/support/document-profiles.json`; `docs/03.specs/052-document-taxonomy-consolidation/spec.md`; `docs/90.references/research/2026-08-08-wer/documentation-architecture-and-diataxis.md` | `repository-static` | `Partial` |
| REQ-WGA-020 | Verification | [Verification](ci-cd-github-actions-qa-and-validation.md#verification) | `docs/00.agent-governance/rules/quality-standards.md`; `docs/03.specs/054-workspace-governance-audit-and-remediation/spec.md` | `repository-static` | `Partial` |
| REQ-WGA-021 | Validation | [Validation](ci-cd-github-actions-qa-and-validation.md#validation) | `docs/00.agent-governance/contracts/validation-surfaces.json`; `scripts/validate-affected-surfaces.py`; `scripts/run-validation-lane.py` | `repository-static` | `Aligned` |
| REQ-WGA-022 | LLM-WIKI | [LLM-WIKI](llm-wiki-memory-and-knowledge-management.md#llm-wiki) | `docs/90.references/llm-wiki/README.md`; `scripts/generate-llm-wiki-index.sh`; `docs/90.references/llm-wiki/wiki-index.md`; `docs/90.references/data/reference-information-architecture.json` | `repository-static` | `Aligned` |
| REQ-WGA-023 | SDLC | [SDLC](spec-driven-sdlc-documentation-and-templates.md#sdlc) | `docs/99.templates/support/document-profiles.json`; `docs/99.templates/support/sdlc-governance.md`; `docs/03.specs/052-document-taxonomy-consolidation/spec.md` | `repository-static` | `Partial` |
| REQ-WGA-024 | Security | [Security](security-and-approval-boundaries.md#security) | `docs/00.agent-governance/rules/approval-boundaries.md#approval-matrix`; `.claude/settings.json#permissions`; `gitops/platform/monitoring/kube-state-metrics.yaml#kind=ClusterRole,metadata.name=kube-state-metrics`; `gitops/platform/network-policies/kustomization.yaml#resources` | `repository-static` | `Partial` |
| REQ-WGA-025 | Legacy and Deprecated documents | [Legacy and Deprecated documents](legacy-deprecated-and-one-shot-disposition-ledger.md#legacy-and-deprecated-documents) | `docs/99.templates/support/legacy-cleanup-rules.md#active-vs-historical-references`; `docs/00.agent-governance/contracts/agent-legacy-cutover.json#referencePolicy`; `scripts/validate-agent-legacy-cutover.py#main` | `repository-static` | `Partial` |
| REQ-WGA-026 | One-shot documents and scripts | [One-shot documents and scripts](legacy-deprecated-and-one-shot-disposition-ledger.md#one-shot-documents-and-scripts) | `scripts/validate-agent-legacy-cutover.py#_repository_candidates`; `scripts/validate-active-corpus-role-audit.py#main`; `docs/90.references/audits/2026-08-09-wgia/legacy-deprecated-and-one-shot-disposition-ledger.md#candidate-disposition-ledger` | `repository-static` | `Partial` |
| REQ-WGA-027 | Memory tiers and management | [Memory tiers and management](llm-wiki-memory-and-knowledge-management.md#memory-tiers-and-management) | `docs/00.agent-governance/memory/README.md`; `docs/00.agent-governance/contracts/harness-contract.json`; `docs/00.agent-governance/contracts/agent-checkpoint.schema.json`; `docs/00.agent-governance/contracts/agent-governance-closure.json` | `repository-static` | `Partial` |
| REQ-WGA-028 | AI Agents | [AI Agents](ai-agents-integrated-and-role-specific-agents.md#ai-agents) | `docs/00.agent-governance/contracts/harness-contract.json#currentInventory`; `docs/00.agent-governance/contracts/agent-model-fitness.json#roleProfiles` | `repository-static` | `Partial` |
| REQ-WGA-029 | Integrated AI Agent | [Integrated AI Agent](ai-agents-integrated-and-role-specific-agents.md#integrated-ai-agent) | `docs/00.agent-governance/contracts/harness-contract.json#canonicalRoles[id=supervisor]`; `docs/00.agent-governance/subagent-protocol.md#tool-scoping`; `docs/00.agent-governance/contracts/agent-loop-lifecycle.json#checkpointBoundary` | `repository-static` | `Partial` |
| REQ-WGA-030 | Individual AI Agents | [Individual AI Agents](ai-agents-integrated-and-role-specific-agents.md#individual-ai-agents) | `docs/00.agent-governance/contracts/harness-contract.json#canonicalRoles`; `docs/00.agent-governance/contracts/agent-evaluations.json#roleSuites`; `docs/00.agent-governance/contracts/agent-roster-admission.json#currentInventory` | `repository-static` | `Partial` |

## Report Index

| Report | Lifecycle | Foundation responsibility |
| --- | --- | --- |
| [Workspace Purpose, Governance, and Operating Contracts](workspace-purpose-governance-and-operating-contracts.md) | `draft` | Purpose, roles, hierarchy, provider shims, and operating-contract owner inventory. |
| [Spec-driven SDLC, Documentation, and Templates](spec-driven-sdlc-documentation-and-templates.md) | `draft` | Lifecycle, document, template, README, and guide owner inventory. |
| [CI/CD, GitHub Actions, QA, and Validation](ci-cd-github-actions-qa-and-validation.md) | `draft` | Delivery and quality-lane owner inventory with Validation/Verification separation. |
| [Harness, Loop, Fixtures, Scripts, and Blockers](harness-loop-fixtures-scripts-and-blockers.md) | `draft` | Harness, loop, fixture, script, recovery, and blocker owner inventory. |
| [LLM-WIKI, Memory, and Knowledge Management](llm-wiki-memory-and-knowledge-management.md) | `draft` | Knowledge-routing and four-class memory owner inventory. |
| [AI Agents, Integrated and Role-specific Agents](ai-agents-integrated-and-role-specific-agents.md) | `draft` | Orchestration, roster, adapter, model, evaluation, and handoff owner inventory. |
| [Security and Approval Boundaries](security-and-approval-boundaries.md) | `draft` | Repository, workflow, agent, secret, GitOps, and action-boundary inventory. |
| [Legacy, Deprecated, and One-shot Disposition Ledger](legacy-deprecated-and-one-shot-disposition-ledger.md) | `draft` | Seven rejected name-only noncandidates, fifteen exact `Integrate` dispositions, protected-history boundaries, and `Delete=0`. |
| [Remediation and Integration Roadmap](remediation-and-integration-roadmap.md) | `draft` | Twelve deduplicated findings: seven bounded admissions and five explicit `DEFER` rows. |

## Refresh and Succession

WGIA-002 through WGIA-009 own topical findings and review. WGIA-010 and
WGIA-011 own accepted canonical remediation. WGIA-012 alone may change Current
navigation and machine projections, WGIA-013 owns proof-gated deletion, and
WGIA-014 owns re-audit and closure. Refresh this foundation when the observation
commit, exact member set, request owner, canonical evidence surface, verdict,
or evidence depth changes.

## Evidence Boundary

The strongest evidence recorded here is `repository-static`: tracked content,
the pinned Git identity, and deterministic local parsing. The closed deeper
depths are `hosted`, `provider-runtime`, and `live`; all three remain `DEFER`
because this task did not inspect authenticated GitHub execution, provider
discovery or consumption, model resolution, permissions, hooks, cluster or
GitOps reconciliation, Vault/ESO, credentials, secrets, cloud, deployment, or
operator rehearsal. Repository-static presence and a passing local check never
promote one of those lanes.

## Related Documents

- [Audit Collection](../README.md)
- [Spec 054](../../../03.specs/054-workspace-governance-audit-and-remediation/spec.md)
- [Implementation Plan](../../../04.execution/plans/2026-08-09-workspace-governance-audit-and-remediation.md)
- [Implementation Task](../../../04.execution/tasks/2026-08-09-workspace-governance-audit-and-remediation.md)
- [Prior Current Audit](../2026-07-11-weia/README.md)
- [Reference Template](../../../99.templates/templates/common/reference.template.md)
