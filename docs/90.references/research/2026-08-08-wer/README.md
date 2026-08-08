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
| REQ-WERPC-007 | Spec-driven development | [Spec-driven baseline](spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline) | `docs/03.specs/` | GitHub Spec Kit primary documentation plus local contracts, checked 2026-08-08 | Verified — source-backed practice model and static local flow; generated-code/runtime outcomes remain DEFER |
| REQ-WERPC-008 | Kubernetes | [Kubernetes baseline](kubernetes-infrastructure-and-security.md#kubernetes-baseline) | `gitops/` and `policy/` | Official Kubernetes, Argo CD, Gatekeeper, ESO, and Vault primary sources plus static platform paths, checked 2026-08-08 | Verified — desired-state/control inventory; admission, RBAC, CNI, reconciliation, and workload runtime remain DEFER |
| REQ-WERPC-009 | Infrastructure | [Infrastructure baseline](kubernetes-infrastructure-and-security.md#infrastructure-baseline) | `infrastructure/` and `traefik/` | Official Argo CD, SLSA, and NIST sources plus static/live boundary documentation, checked 2026-08-08 | Partial — static bootstrap/GitOps/gateway boundary verified; k3d, gateway, registry, hosted CI, and cloud state remain DEFER |
| REQ-WERPC-010 | SDLC | [SDLC baseline](spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline) | `docs/01.requirements/` | NIST SSDF, ISO official abstract, and local contracts, checked 2026-08-08 | Verified — external framework boundaries and static document lifecycle; conformance/effectiveness remains DEFER |
| REQ-WERPC-011 | PRD | [Document-family matrix](spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix) | `docs/01.requirements/` | Local profile/template/validator evidence, checked 2026-08-08 | Verified — typed static contract; product outcome and semantic quality remain DEFER |
| REQ-WERPC-012 | ARD | [Document-family matrix](spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix) | `docs/02.architecture/requirements/` | Local profile/template/validator evidence, checked 2026-08-08 | Verified — typed static contract; architecture effectiveness remains DEFER |
| REQ-WERPC-013 | ADR | [Document-family matrix](spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix) | `docs/02.architecture/decisions/` | AWS ADR guidance plus local profile/template evidence, checked 2026-08-08 | Verified — static contract and bounded ADR benchmark; decision quality remains DEFER |
| REQ-WERPC-014 | Guide | [Document-family matrix](spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix) | `docs/05.operations/guides/` | Local profile/template plus Diátaxis guidance, checked 2026-08-08 | Partial — typed how-to-shaped Guide; tutorial classification/usability remains DEFER |
| REQ-WERPC-015 | Incident | [Document-family matrix](spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix) | `docs/05.operations/incidents/` | Google SRE guidance plus local profile/template evidence, checked 2026-08-08 | Verified — typed static incident contract; runtime response remains DEFER |
| REQ-WERPC-016 | Postmortem | [Document-family matrix](spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix) | `docs/99.templates/templates/sdlc/operations/postmortem.template.md` | Google SRE guidance plus local profile/template evidence, checked 2026-08-08 | Verified — typed static learning contract; action closure remains DEFER |
| REQ-WERPC-017 | Policy | [Document-family matrix](spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix) | `docs/05.operations/policies/` | Local profile/template/validator evidence, checked 2026-08-08 | Verified — typed static control document; enforcement remains DEFER |
| REQ-WERPC-018 | Release | [Document-family matrix](spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix) | `.github/workflows/` | SemVer plus local profile/template/validator absence check, checked 2026-08-08 | Verified gap — no typed release family; no release approval/runtime claim |
| REQ-WERPC-019 | Runbook | [Document-family matrix](spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix) | `docs/05.operations/runbooks/` | Local profile/template/validator evidence, checked 2026-08-08 | Verified — typed static procedure contract; live safety/execution remains DEFER |
| REQ-WERPC-020 | Diátaxis | [Diátaxis baseline](documentation-architecture-and-diataxis.md#diátaxis-baseline) | `docs/99.templates/support/document-profiles.json` | Official Diátaxis plus local profiles/templates, checked 2026-08-08 | Partial — how-to/reference are partially expressed; tutorial/explanation typing and classification remain gap |
| REQ-WERPC-021 | LLM-WIKI | [LLM-WIKI baseline](llm-wiki-and-knowledge-routing.md#llm-wiki-baseline) | `docs/90.references/llm-wiki/` | llms.txt proposal, MCP Resources specification, and local generator, checked 2026-08-08 | Verified — deterministic canonical-owner map; publication, MCP, search, RAG, and retrieval remain DEFER |
| REQ-WERPC-022 | CI/CD | [CI/CD baseline](ci-cd-github-actions-and-qa.md#cicd-baseline) | `.github/workflows/`, `.github/README.md`, and GitOps recovery owners | Official GitHub, SLSA, pre-commit, and pip primary sources plus static workflow/validation evidence, checked 2026-08-08 | Partial — static CI/release-review and QA controls verified; deployment/promotion/rollback execution remains DEFER |
| REQ-WERPC-023 | GitHub Actions | [GitHub Actions baseline](ci-cd-github-actions-and-qa.md#github-actions-baseline) | `.github/workflows/`, CI security and Python-contract validators | Official GitHub Actions primary documentation plus static workflow inventory, checked 2026-08-08 | Partial — workflow/permission/pinning/concurrency declarations verified; hosted runs, rulesets, secrets, environments, OIDC, artifacts, and effective permissions remain DEFER |
| REQ-WERPC-024 | QA | [QA baseline](ci-cd-github-actions-and-qa.md#qa-baseline) | `scripts/validate-repo-quality-gates.sh`, `validation-surfaces.json`, and `.pre-commit-config.yaml` | Repository validation contract plus official pre-commit/pip sources, checked 2026-08-08 | Verified — static lane/result, formatter, contract, lint/syntax/test/security boundaries documented; hosted/browser/live outcome remains DEFER |
| REQ-WERPC-025 | Security | [Security baseline](kubernetes-infrastructure-and-security.md#security-baseline) | `policy/`, GitOps, ESO/Vault contracts | Official Kubernetes, Gatekeeper, ESO/Vault, SLSA, and NIST sources plus static control evidence, checked 2026-08-08 | Partial — static controls and bounded gaps verified; enforcement, secret/backend state, supply-chain artifacts, and recovery exercise remain DEFER |
| REQ-WERPC-026 | AI-agent systems | [AI-agent-system baseline](ai-agents-and-agency-agents.md#ai-agent-systems-baseline) | `docs/00.agent-governance/harness-catalog.md` | Official OpenAI/Anthropic agent documentation plus local harness contracts, checked 2026-08-08 | Partial — static role/control-plane design verified; discovery, permission enforcement, execution, and effectiveness remain DEFER |
| REQ-WERPC-027 | agency-agents | [Agency-agents baseline](ai-agents-and-agency-agents.md#agency-agents-baseline) | `.agents/agents/` | Pinned upstream commit `ebe9c99acb5c96f9468de368d8bead775387d1a7`, checked 2026-08-08 | Verified — reproducible catalog/license/script comparison; adoption, conversion/install, provider discovery, and quality remain DEFER |
| REQ-WERPC-028 | Model routing | [Model-routing baseline](agent-model-routing-and-configuration.md#model-routing-baseline) | `docs/00.agent-governance/model-policy.md` | Official OpenAI/Anthropic configuration sources plus local model-fitness contract, checked 2026-08-08 | Partial — static tier/configuration/routing gates verified; parsing, resolution, fitness, cost/latency, canary, and promotion remain DEFER |
| REQ-WERPC-029 | Short-term memory | [Short-term-memory baseline](agent-memory-tiers-and-management.md#short-term-memory-baseline) | `docs/00.agent-governance/contracts/agent-checkpoint.schema.json` | Local checkpoint contract plus official provider memory/session sources, checked 2026-08-08 | Verified — atomic redacted advisory lifecycle defined; actual checkpoint/provider-memory use remains DEFER |
| REQ-WERPC-030 | Long-term memory | [Long-term-memory baseline](agent-memory-tiers-and-management.md#long-term-memory-baseline) | `docs/00.agent-governance/memory/progress.md` | Local memory contract plus official provider memory/session sources, checked 2026-08-08 | Verified — durable canonical-owner/provenance lifecycle defined; provider persistence and runtime enforcement remain DEFER |
| REQ-WERPC-031 | Domain-scoped memory | [Domain-memory baseline](agent-memory-tiers-and-management.md#domain-scoped-memory-baseline) | `docs/03.specs/` | Local memory/domain-owner contract plus official provider/MCP boundaries, checked 2026-08-08 | Verified — Spec/Runbook/Incident/Postmortem authority and archive routing defined; actual retrieval and provider integration remain DEFER |
| REQ-WERPC-032 | Memory management | [Memory-management baseline](agent-memory-tiers-and-management.md#memory-management-baseline) | `docs/00.agent-governance/memory/README.md` | Official OpenAI, Anthropic, and MCP primary sources plus local memory contract, checked 2026-08-08 | Partial — lifecycle/redaction/conflict rules verified; provider retention, deletion, compaction, and connected-resource behavior remain DEFER |

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
