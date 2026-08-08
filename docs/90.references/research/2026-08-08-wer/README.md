# Workspace Engineering Research Pack (2026-08-08)

## Overview

This pack is the single successor research boundary for the three dated Workspace
Engineering Research (WER) packs. It establishes ownership and migration
interfaces before topical research is refreshed. It is descriptive evidence,
not a policy, runtime, provider, or deployment control surface.

## Snapshot Contract

- **Pack date**: 2026-08-08.
- **Baseline**: 25 tracked predecessor files, retained in place until WERPC-008.
- **Authority**: the named canonical workspace documents remain current truth;
  this pack records dated research and routing evidence.
- **Status vocabulary**: initial implementation findings are `Unverified` unless
  a later WERPC work package records supporting evidence.

## Report Index

| Reference | Role |
| --- | --- |
| [workspace governance](workspace-governance-and-common-agent-environment.md) | Common workspace and application routing |
| [harness and loop](harness-and-loop-engineering.md) | Harness and control-loop analysis |
| [provider status](provider-implementation-status.md) | Claude/Codex surface separation |
| [SDLC contracts](spec-driven-sdlc-and-document-contracts.md) | Spec-driven lifecycle and document families |
| [documentation architecture](documentation-architecture-and-diataxis.md) | Diátaxis mapping |
| [LLM-WIKI routing](llm-wiki-and-knowledge-routing.md) | Knowledge routing and freshness |
| [platform security](kubernetes-infrastructure-and-security.md) | Kubernetes, infrastructure, and security |
| [CI/CD and QA](ci-cd-github-actions-and-qa.md) | Delivery evidence lanes |
| [AI agents](ai-agents-and-agency-agents.md) | Agent-system and agency-agents analysis |
| [model routing](agent-model-routing-and-configuration.md) | Model-selection controls |
| [memory](agent-memory-tiers-and-management.md) | Memory-class lifecycle |
| [source and migration ledger](source-coverage-and-migration-ledger.md) | Sources, predecessor disposition, and cutover evidence |

### Requirement Coverage Matrix

Each request has one and only one primary research owner. Workspace evidence is
current local evidence; it does not establish external product or live-runtime
claims.

| Request ID | Requested topic | Primary owner | Workspace evidence | External source class | Status |
| --- | --- | --- | --- | --- | --- |
| REQ-WERPC-001 | Harness | [Harness baseline](harness-and-loop-engineering.md#harness-baseline) | `.codex/CODEX.md` | Official OpenAI primary sources plus repository-static contracts, checked 2026-08-08 | Verified — static harness implementation; provider/runtime delivery remains DEFER |
| REQ-WERPC-002 | Loop | [Loop baseline](harness-and-loop-engineering.md#loop-baseline) | `docs/00.agent-governance/rules/agentic.md` | Repository-static machine contract plus official OpenAI product context, checked 2026-08-08 | Verified — local state/retry contract; actual provider execution remains DEFER |
| REQ-WERPC-003 | Workspace application | [Workspace application baseline](workspace-governance-and-common-agent-environment.md#workspace-application-baseline) | `AGENTS.md` | Official Anthropic/OpenAI sources plus repository-static owners, checked 2026-08-08 | Verified — static control-plane application; native discovery/authentication remains DEFER |
| REQ-WERPC-004 | Claude | [Claude baseline](provider-implementation-status.md#claude-baseline) | `.claude/` | Official Anthropic provider documentation, checked 2026-08-08 | Verified — bounded product surfaces and static adapter; local discovery/runtime remains DEFER |
| REQ-WERPC-005 | Codex | [Codex baseline](provider-implementation-status.md#codex-baseline) | `.codex/CODEX.md` | Official OpenAI provider documentation (manual cache first), checked 2026-08-08 | Verified — bounded product surfaces and static adapter; local discovery/runtime remains DEFER |
| REQ-WERPC-006 | Common system | [Common-system baseline](workspace-governance-and-common-agent-environment.md#common-system-baseline) | `docs/00.agent-governance/harness-catalog.md` | Official provider sources plus repository-static control-plane evidence, checked 2026-08-08 | Partial — static shared controls verified; provider parity/effective runtime remains DEFER |
| REQ-WERPC-007 | Spec-driven development | [Spec-driven baseline](spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline) | `docs/03.specs/` | Later primary research | Unverified |
| REQ-WERPC-008 | Kubernetes | [Kubernetes baseline](kubernetes-infrastructure-and-security.md#kubernetes-baseline) | `gitops/` | Later primary research | Unverified |
| REQ-WERPC-009 | Infrastructure | [Infrastructure baseline](kubernetes-infrastructure-and-security.md#infrastructure-baseline) | `infrastructure/` | Later primary research | Unverified |
| REQ-WERPC-010 | SDLC | [SDLC baseline](spec-driven-sdlc-and-document-contracts.md#sdlc-baseline) | `docs/01.requirements/` | Later primary research | Unverified |
| REQ-WERPC-011 | PRD | [PRD baseline](spec-driven-sdlc-and-document-contracts.md#prd-baseline) | `docs/01.requirements/` | Later primary research | Unverified |
| REQ-WERPC-012 | ARD | [ARD baseline](spec-driven-sdlc-and-document-contracts.md#ard-baseline) | `docs/02.architecture/requirements/` | Later primary research | Unverified |
| REQ-WERPC-013 | ADR | [ADR baseline](spec-driven-sdlc-and-document-contracts.md#adr-baseline) | `docs/02.architecture/decisions/` | Later primary research | Unverified |
| REQ-WERPC-014 | Guide | [Guide baseline](spec-driven-sdlc-and-document-contracts.md#guide-baseline) | `docs/05.operations/guides/` | Later primary research | Unverified |
| REQ-WERPC-015 | Incident | [Incident baseline](spec-driven-sdlc-and-document-contracts.md#incident-baseline) | `docs/05.operations/incidents/` | Later primary research | Unverified |
| REQ-WERPC-016 | Postmortem | [Postmortem baseline](spec-driven-sdlc-and-document-contracts.md#postmortem-baseline) | `docs/99.templates/templates/sdlc/operations/postmortem.template.md` | Later primary research | Unverified |
| REQ-WERPC-017 | Policy | [Policy baseline](spec-driven-sdlc-and-document-contracts.md#policy-baseline) | `docs/05.operations/policies/` | Later primary research | Unverified |
| REQ-WERPC-018 | Release | [Release baseline](spec-driven-sdlc-and-document-contracts.md#release-baseline) | `.github/workflows/` | Later primary research | Unverified |
| REQ-WERPC-019 | Runbook | [Runbook baseline](spec-driven-sdlc-and-document-contracts.md#runbook-baseline) | `docs/05.operations/runbooks/` | Later primary research | Unverified |
| REQ-WERPC-020 | Diátaxis | [Diátaxis baseline](documentation-architecture-and-diataxis.md#diátaxis-baseline) | `docs/99.templates/support/document-profiles.json` | Later primary research | Unverified |
| REQ-WERPC-021 | LLM-WIKI | [LLM-WIKI baseline](llm-wiki-and-knowledge-routing.md#llm-wiki-baseline) | `docs/90.references/llm-wiki/` | Later primary research | Unverified |
| REQ-WERPC-022 | CI/CD | [CI/CD baseline](ci-cd-github-actions-and-qa.md#cicd-baseline) | `.github/workflows/` | Later primary research | Unverified |
| REQ-WERPC-023 | GitHub Actions | [GitHub Actions baseline](ci-cd-github-actions-and-qa.md#github-actions-baseline) | `.github/workflows/` | Later official product research | Unverified |
| REQ-WERPC-024 | QA | [QA baseline](ci-cd-github-actions-and-qa.md#qa-baseline) | `scripts/validate-repo-quality-gates.sh` | Later primary research | Unverified |
| REQ-WERPC-025 | Security | [Security baseline](kubernetes-infrastructure-and-security.md#security-baseline) | `policy/` | Later primary research | Unverified |
| REQ-WERPC-026 | AI-agent systems | [AI-agent-system baseline](ai-agents-and-agency-agents.md#ai-agent-systems-baseline) | `docs/00.agent-governance/harness-catalog.md` | Later primary research | Unverified |
| REQ-WERPC-027 | agency-agents | [Agency-agents baseline](ai-agents-and-agency-agents.md#agency-agents-baseline) | `.agents/agents/` | Later pinned upstream research | Unverified |
| REQ-WERPC-028 | Model routing | [Model-routing baseline](agent-model-routing-and-configuration.md#model-routing-baseline) | `docs/00.agent-governance/model-policy.md` | Later official provider research | Unverified |
| REQ-WERPC-029 | Short-term memory | [Short-term-memory baseline](agent-memory-tiers-and-management.md#short-term-memory-baseline) | `docs/00.agent-governance/contracts/agent-checkpoint.schema.json` | Later primary research | Unverified |
| REQ-WERPC-030 | Long-term memory | [Long-term-memory baseline](agent-memory-tiers-and-management.md#long-term-memory-baseline) | `docs/00.agent-governance/memory/progress.md` | Later primary research | Unverified |
| REQ-WERPC-031 | Domain-scoped memory | [Domain-memory baseline](agent-memory-tiers-and-management.md#domain-scoped-memory-baseline) | `docs/03.specs/` | Later primary research | Unverified |
| REQ-WERPC-032 | Memory management | [Memory-management baseline](agent-memory-tiers-and-management.md#memory-management-baseline) | `docs/00.agent-governance/memory/README.md` | Later primary research | Unverified |

## Refresh and Succession

WERPC-002 through WERPC-006 add dated source-backed findings to their assigned
owners. WERPC-007 classifies mutable consumers; WERPC-008 alone may delete
predecessor files after its fail-closed readiness proof.

## Evidence Boundary

This baseline records repository-static paths and historical predecessor
evidence. It does not claim hosted CI, provider runtime, authentication,
remote, credential-bearing, secret-value, or live-cluster evidence.

## Related Documents

- [WERPC Task](../../../04.execution/tasks/2026-08-08-workspace-engineering-research-pack-consolidation.md)
- [WERPC Plan](../../../04.execution/plans/2026-08-08-workspace-engineering-research-pack-consolidation.md)
- [Source coverage and migration ledger](source-coverage-and-migration-ledger.md)
