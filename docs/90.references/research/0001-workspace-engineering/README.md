---
title: "Workspace Engineering Research Pack"
version: "0.1.0"
type: "common/readme-research-pack"
status: "active"
owner: "platform"
updated: "2026-09-05"
layer: "references"
---
# Workspace Engineering Research Pack

## Overview

This pack is the single successor research boundary for the three dated Workspace
Engineering Research (WER) packs. It establishes ownership and migration
interfaces before topical research is refreshed. It is descriptive evidence,
not a policy, runtime, provider, or deployment control surface.

## Research Contract

- **Pack date**: 2026-08-08.
- **Baseline**: 25 predecessor files deleted by WERPC-008 after exact
  disposition and consumer-cutover proof; Git history and source coverage
  retain their provenance.
- **Authority**: the named canonical workspace documents remain current truth;
  this pack records observation-dated research and routing evidence.
- **Status vocabulary**: findings use only `Verified`, `Partial`, `Unverified`,
  `DEFER`, or `Contradicted`; the completed WERPC work packages record the
  supporting evidence and remaining limits. A compound status cell states the
  base value first and then its bounded qualifier.
- **Path shorthand**: bare `rules/`, `scopes/`, `providers/`, `contracts/`,
  `memory/`, `model-policy.md`, and `harness-catalog.md` references in these
  reports refer to the historical `docs/00.agent-governance/` tree at each
  observation date. They are historical prose, never current load instructions.
  Current shared authority is [the common hub](../../../../.agents/README.md);
  [Archive](../../../98.archive/README.md) owns the Git-backed successor graph.
- **Correction record**: a 2026-08-10 coverage re-verification corrected the
  Claude gateway-import, common-instruction-topology, and LLM-WIKI freshness
  statements, and resolved a source-date self-contradiction in the CI/CD and QA
  report. Source and claim identifiers were not renumbered.
- **Freshness record**: on 2026-08-10 the five reports that the gap-only refresh
  did not touch had their external sources re-checked. Four returned no change
  inside the window: harness and loop, AI agents and agency agents, model
  routing, and memory. The Diátaxis sources were unreachable behind HTTP 429 and
  are recorded as `unreachable`, not `unchanged`; their claims retain the
  2026-08-08 observation date. Two findings were added as dated subsections
  without rewriting an existing claim: the pinned MCP `2025-11-25` revision is
  superseded by `2026-07-28`, registered as `SRC-WERPC-066`; and the two live
  Codex pages disagree on model identifiers, reasoning-effort values, and model
  precedence order. No requirement status changed.
- **Source-verification record**: a third published-page attempt on 2026-08-11
  returned HTTP 429 again, so the Diátaxis claims were instead verified against
  the upstream source that builds the site, registered as `SRC-WERPC-067`. That
  check also reconciled the recorded tutorial and explanation absence with
  approved Spec 052 `DOC-G2` and `DOC-G3`: the absence is a decision resting on
  the framework's own instruction, not an open question. `REQ-WERPC-020` keeps
  its `Partial` status, which now reflects unenforced `DOC-G1` enum work rather
  than an undecided route.

### Structure

```text
0001-workspace-engineering/
├── README.md
├── m0011-agent-memory-tiers-and-management.md
├── m0010-agent-model-routing-and-configuration.md
├── m0009-ai-agents-and-agency-agents.md
├── m0008-ci-cd-github-actions-and-qa.md
├── m0005-documentation-architecture-and-diataxis.md
├── m0002-harness-and-loop-engineering.md
├── m0007-kubernetes-infrastructure-and-security.md
├── m0006-llm-wiki-and-knowledge-routing.md
├── m0003-provider-implementation-status.md
├── m0013-scope-application-index.md
├── m0012-source-coverage.md
├── m0004-spec-driven-sdlc-and-document-contracts.md
└── m0001-workspace-governance-and-common-agent-environment.md
```

## Report Index

| Reference                                                                    | Role                                                   |
| ---------------------------------------------------------------------------- | ------------------------------------------------------ |
| [workspace governance](m0001-workspace-governance-and-common-agent-environment.md) | Common workspace and application routing               |
| [harness and loop](m0002-harness-and-loop-engineering.md)                          | Harness and control-loop analysis                      |
| [provider status](m0003-provider-implementation-status.md)                         | Claude/Codex surface separation                        |
| [SDLC contracts](m0004-spec-driven-sdlc-and-document-contracts.md)                 | Spec-driven lifecycle and document families            |
| [documentation architecture](m0005-documentation-architecture-and-diataxis.md)     | Diátaxis mapping                                       |
| [LLM-WIKI routing](m0006-llm-wiki-and-knowledge-routing.md)                        | Knowledge routing and freshness                        |
| [platform security](m0007-kubernetes-infrastructure-and-security.md)               | Kubernetes, infrastructure, and security               |
| [CI/CD and QA](m0008-ci-cd-github-actions-and-qa.md)                               | Delivery evidence lanes                                |
| [AI agents](m0009-ai-agents-and-agency-agents.md)                                  | Agent-system and agency-agents analysis                |
| [model routing](m0010-agent-model-routing-and-configuration.md)                    | Model-selection controls                               |
| [memory](m0011-agent-memory-tiers-and-management.md)                               | Memory-class lifecycle                                 |
| [source coverage](m0012-source-coverage.md)                                         | Sources, claims, and bounded historical disposition    |
| [scope application index](m0013-scope-application-index.md)                        | Governance-scope routing over the pack findings        |

### Requirement Coverage Matrix

Each request has one and only one primary research owner. Workspace evidence is
current local evidence; it does not establish external product or live-runtime
claims.

| Request ID    | Requested topic         | Primary owner                                                                                                         | Workspace evidence                                                                                  | External source class                                                                                                                                                                                                                                   | Status                                                                                                                                                                                                                                           |
| ------------- | ----------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| REQ-WERPC-001 | Harness                 | [Harness baseline](m0002-harness-and-loop-engineering.md#harness-baseline)                                                  | `.codex/CODEX.md`                                                                                   | Official OpenAI primary sources plus repository-static contracts, checked 2026-08-08                                                                                                                                                                    | Verified — static harness implementation; provider/runtime delivery remains DEFER                                                                                                                                                                |
| REQ-WERPC-002 | Loop                    | [Loop baseline](m0002-harness-and-loop-engineering.md#loop-baseline)                                                        | `docs/00.agent-governance/rules/agentic.md`                                                         | Repository-static machine contract plus official OpenAI product context, checked 2026-08-08                                                                                                                                                             | Verified — local state/retry contract; actual provider execution remains DEFER                                                                                                                                                                   |
| REQ-WERPC-003 | Workspace application   | [Workspace application baseline](m0001-workspace-governance-and-common-agent-environment.md#workspace-application-baseline) | `AGENTS.md`                                                                                         | Official Anthropic/OpenAI sources plus repository-static owners, checked 2026-08-08                                                                                                                                                                     | Verified — static control-plane application; native discovery/authentication remains DEFER                                                                                                                                                       |
| REQ-WERPC-004 | Claude                  | [Claude baseline](m0003-provider-implementation-status.md#claude-baseline)                                                  | `.claude/`                                                                                          | Official Anthropic provider documentation, checked 2026-08-08                                                                                                                                                                                           | Verified — bounded product surfaces and static adapter; local discovery/runtime remains DEFER                                                                                                                                                    |
| REQ-WERPC-005 | Codex                   | [Codex baseline](m0003-provider-implementation-status.md#codex-baseline)                                                    | `.codex/CODEX.md`                                                                                   | Official OpenAI provider documentation (manual cache first), checked 2026-08-08                                                                                                                                                                         | Verified — bounded product surfaces and static adapter; local discovery/runtime remains DEFER                                                                                                                                                    |
| REQ-WERPC-006 | Common system           | [Common-system baseline](m0001-workspace-governance-and-common-agent-environment.md#common-system-baseline)                 | `docs/00.agent-governance/harness-catalog.md`                                                       | Official provider sources plus repository-static control-plane evidence, checked 2026-08-08                                                                                                                                                             | Partial — static shared controls verified; provider parity/effective runtime remains DEFER                                                                                                                                                       |
| REQ-WERPC-007 | Spec-driven development | [Spec-driven baseline](m0004-spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline)                   | `docs/03.specs/`                                                                                    | GitHub Spec Kit primary documentation plus local contracts, checked 2026-08-08                                                                                                                                                                          | Verified — source-backed practice model and static local flow; generated-code/runtime outcomes remain DEFER                                                                                                                                      |
| REQ-WERPC-008 | Kubernetes              | [Kubernetes baseline](m0007-kubernetes-infrastructure-and-security.md#kubernetes-baseline)                                  | `gitops/` and `policy/`                                                                             | Official Kubernetes, kube-state-metrics v2.14.0, Argo CD, Helm, Gatekeeper, ESO, Vault, Sigstore, SLSA, and GitHub primary sources plus exact static selectors (`SRC-WERPC-023`–`034`, `SRC-WERPC-060`–`065`); admitted refresh checked 2026-08-10      | Partial — exact Secret collector/RBAC, Adminer token/hardening, and immutable delivery distinctions are source-backed; consumer need, compatibility, effective RBAC/admission/reconciliation, artifacts, registry, and runtime remain DEFER      |
| REQ-WERPC-009 | Infrastructure          | [Infrastructure baseline](m0007-kubernetes-infrastructure-and-security.md#infrastructure-baseline)                          | `infrastructure/` and `traefik/`                                                                    | Official Argo CD, SLSA, and NIST sources plus static/live boundary documentation, checked 2026-08-08                                                                                                                                                    | Partial — static bootstrap/GitOps/gateway boundary verified; k3d, gateway, registry, hosted CI, and cloud state remain DEFER                                                                                                                     |
| REQ-WERPC-010 | SDLC                    | [SDLC baseline](m0004-spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline)                          | `docs/01.requirements/`                                                                             | NIST SSDF, ISO official abstract, and local contracts, checked 2026-08-08                                                                                                                                                                               | Verified — external framework boundaries and static document lifecycle; conformance/effectiveness remains DEFER                                                                                                                                  |
| REQ-WERPC-011 | PRD                     | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `docs/01.requirements/`                                                                             | ISO requirements-engineering abstract, NASA systems guidance, and local profile/template/validator evidence (`SRC-WERPC-053`), checked 2026-08-10                                                                                                       | Verified gap — repository-defined product-intent contract with external requirements basis; current downstream terminology is AD, while stakeholder/product validation remains DEFER                                                             |
| REQ-WERPC-012 | Architecture Description (AD) | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)             | `docs/02.architecture/descriptions/`                                                                | ISO architecture-description abstract, NASA architecture guidance, and local profile/template/validator evidence (`SRC-WERPC-054`), checked 2026-08-10                                                                                                  | Verified gap — compact local architecture contract with proportional external review basis; current route and lineage use AD and `sdlc/ad`, while architecture effectiveness remains DEFER                                                     |
| REQ-WERPC-013 | ADR                     | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `docs/02.architecture/decisions/`                                                                   | AWS ADR guidance plus local profile/template evidence, checked 2026-08-08                                                                                                                                                                               | Verified gap — static contract and bounded ADR benchmark; current lineage is AD/ADR, while decision quality remains DEFER                                                                                                                       |
| REQ-WERPC-014 | Guide                   | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `docs/05.operations/guides/`                                                                        | Local profile/template plus Diátaxis guidance, checked 2026-08-08                                                                                                                                                                                       | Partial — typed how-to-shaped Guide; tutorial classification/usability remains DEFER                                                                                                                                                             |
| REQ-WERPC-015 | Incident                | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `docs/05.operations/incidents/`                                                                     | Google SRE guidance plus local profile/template evidence, checked 2026-08-08                                                                                                                                                                            | Verified — typed static incident contract; runtime response remains DEFER                                                                                                                                                                        |
| REQ-WERPC-016 | Postmortem              | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `docs/99.templates/templates/operations/postmortem.template.md`                                | Google SRE guidance plus local profile/template evidence, checked 2026-08-08                                                                                                                                                                            | Verified — typed static learning contract; action closure remains DEFER                                                                                                                                                                          |
| REQ-WERPC-017 | Policy                  | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `docs/05.operations/policies/`                                                                      | NIST policy/control/assessment guidance plus local profile/template/validator evidence (`SRC-WERPC-055`), checked 2026-08-10                                                                                                                            | Verified — normative policy, procedure, and assessment-evidence boundaries; enforcement remains DEFER                                                                                                                                            |
| REQ-WERPC-018 | Release                 | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `.github/workflows/`                                                                                | Google release engineering, GitHub immutable-release identity, existing SemVer/provenance sources, and local absence evidence (`SRC-WERPC-056`), checked 2026-08-10                                                                                     | Verified gap — broader auditable release-record semantics are sourced, but no family/approval/runtime is created; DOC-G5 remains intact                                                                                                          |
| REQ-WERPC-019 | Runbook                 | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `docs/05.operations/runbooks/`                                                                      | Google SRE playbook/toil guidance plus local profile/template/validator evidence (`SRC-WERPC-057`), checked 2026-08-10                                                                                                                                  | Verified — typed procedure and risk-aware automation boundary; rehearsal and live safety/execution remain DEFER                                                                                                                                  |
| REQ-WERPC-020 | Diátaxis                | [Diátaxis baseline](m0005-documentation-architecture-and-diataxis.md#diátaxis-baseline)                                     | `docs/99.templates/registry.json`                                                  | Official Diátaxis plus local profiles/templates, checked 2026-08-08                                                                                                                                                                                     | Partial — how-to/reference are partially expressed; tutorial/explanation typing and classification remain gap                                                                                                                                    |
| REQ-WERPC-021 | LLM-WIKI                | [Historical LLM-WIKI baseline](m0006-llm-wiki-and-knowledge-routing.md#llm-wiki-baseline)                                   | No current local owner; Git history preserves the retired generator and output                       | llms.txt proposal, MCP Resources specification, and historical local generator, checked 2026-08-08; local retirement recorded 2026-09-01                                                                                                                | Contradicted — the prior deterministic canonical-owner map was retired; external comparison remains descriptive, and publication, MCP, search, RAG, and retrieval remain DEFER                                                                  |
| REQ-WERPC-022 | CI/CD                   | [CI/CD baseline](m0008-ci-cd-github-actions-and-qa.md#cicd-baseline)                                                        | `.github/workflows/`, `.github/README.md`, and GitOps recovery owners                               | Official GitHub, SLSA, pre-commit, and pip primary sources plus static workflow/validation evidence, checked 2026-08-08                                                                                                                                 | Partial — static CI/release-review and QA controls verified; deployment/promotion/rollback execution remains DEFER                                                                                                                               |
| REQ-WERPC-023 | GitHub Actions          | [GitHub Actions baseline](m0008-ci-cd-github-actions-and-qa.md#github-actions-baseline)                                     | `.github/workflows/`, CI security and Python-contract validators                                    | Official GitHub Actions primary documentation plus static workflow inventory, checked 2026-08-08                                                                                                                                                        | Partial — workflow/permission/pinning/concurrency declarations verified; hosted runs, rulesets, secrets, environments, OIDC, artifacts, and effective permissions remain DEFER                                                                   |
| REQ-WERPC-024 | QA                      | [QA baseline](m0008-ci-cd-github-actions-and-qa.md#qa-baseline)                                                             | `scripts/validate-repo-quality-gates.sh`, `validation-surfaces.json`, and `.pre-commit-config.yaml` | Repository validation contract plus official pre-commit/pip sources, checked 2026-08-08                                                                                                                                                                 | Verified — static lane/result, formatter, contract, lint/syntax/test/security boundaries documented; hosted/browser/live outcome remains DEFER                                                                                                   |
| REQ-WERPC-025 | Security                | [Security baseline](m0007-kubernetes-infrastructure-and-security.md#security-baseline)                                      | `policy/`, GitOps, ESO/Vault contracts                                                              | Official Kubernetes, kube-state-metrics v2.14.0, Argo CD, Helm, Gatekeeper, ESO/Vault, Sigstore, SLSA, GitHub, and NIST sources plus exact static control selectors (`SRC-WERPC-023`–`034`, `SRC-WERPC-060`–`065`); admitted refresh checked 2026-08-10 | Partial — Secret-object RBAC, Adminer ServiceAccount/hardening, and identity/signature/attestation/provenance boundaries are source-backed; enforcement, Secret/backend state, compatibility, trust policy, artifacts, and recovery remain DEFER |
| REQ-WERPC-026 | AI-agent systems        | [AI-agent-system baseline](m0009-ai-agents-and-agency-agents.md#ai-agent-systems-baseline)                                  | `docs/00.agent-governance/harness-catalog.md`                                                       | Official OpenAI/Anthropic agent documentation plus local harness contracts, checked 2026-08-08                                                                                                                                                          | Partial — static role/control-plane design verified; discovery, permission enforcement, execution, and effectiveness remain DEFER                                                                                                                |
| REQ-WERPC-027 | agency-agents           | [Agency-agents baseline](m0009-ai-agents-and-agency-agents.md#agency-agents-baseline)                                       | `.agents/agents/`                                                                                   | Pinned upstream commit `ebe9c99acb5c96f9468de368d8bead775387d1a7`, checked 2026-08-08                                                                                                                                                                   | Verified — reproducible catalog/license/script comparison; adoption, conversion/install, provider discovery, and quality remain DEFER                                                                                                            |
| REQ-WERPC-028 | Model routing           | [Model-routing baseline](m0010-agent-model-routing-and-configuration.md#model-routing-baseline)                             | `docs/00.agent-governance/model-policy.md`                                                          | Official OpenAI/Anthropic configuration sources plus local model-fitness contract, checked 2026-08-08                                                                                                                                                   | Partial — static tier/configuration/routing gates verified; parsing, resolution, fitness, cost/latency, canary, and promotion remain DEFER                                                                                                       |
| REQ-WERPC-029 | Short-term memory       | [Short-term-memory baseline](m0011-agent-memory-tiers-and-management.md#short-term-memory-baseline)                         | `docs/00.agent-governance/contracts/agent-checkpoint.schema.json`                                   | Local checkpoint contract plus official provider memory/session sources, checked 2026-08-08                                                                                                                                                             | Verified — atomic redacted advisory lifecycle defined; actual checkpoint/provider-memory use remains DEFER                                                                                                                                       |
| REQ-WERPC-030 | Long-term memory        | [Long-term-memory baseline](m0011-agent-memory-tiers-and-management.md#long-term-memory-baseline)                           | `docs/00.agent-governance/memory/progress.md`                                                       | Local memory contract plus official provider memory/session sources, checked 2026-08-08                                                                                                                                                                 | Verified — durable canonical-owner/provenance lifecycle defined; provider persistence and runtime enforcement remain DEFER                                                                                                                       |
| REQ-WERPC-031 | Domain-scoped memory    | [Domain-memory baseline](m0011-agent-memory-tiers-and-management.md#domain-scoped-memory-baseline)                          | `docs/03.specs/`                                                                                    | Local memory/domain-owner contract plus official provider/MCP boundaries, checked 2026-08-08                                                                                                                                                            | Verified — Spec/Runbook/Incident/Postmortem authority and archive routing defined; actual retrieval and provider integration remain DEFER                                                                                                        |
| REQ-WERPC-032 | Memory management       | [Memory-management baseline](m0011-agent-memory-tiers-and-management.md#memory-management-baseline)                         | `docs/00.agent-governance/memory/README.md`                                                         | Official OpenAI, Anthropic, and MCP primary sources plus local memory contract, checked 2026-08-08                                                                                                                                                      | Partial — lifecycle/redaction/conflict rules verified; provider retention, deletion, compaction, and connected-resource behavior remain DEFER                                                                                                    |
| REQ-WERPC-033 | Verification/Validation | [Verification and Validation matrix](m0008-ci-cd-github-actions-and-qa.md#verification-and-validation-question-matrix)      | `docs/00.agent-governance/rules/quality-standards.md`                                               | NASA product verification, product validation, requirements validation, and traceability guidance plus local quality-lane evidence (`SRC-WERPC-058`–`SRC-WERPC-059`), checked 2026-08-10                                                                | Partial — external questions and static workspace mapping verified; stakeholder, intended-use, independent, hosted, remote, and live evidence remain DEFER                                                                                       |
| REQ-WERPC-034 | Spec                    | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `docs/03.specs/`                                                                                    | GitHub Spec Kit specification-driven and agentic SDD guidance plus local profile/template/validator evidence, checked 2026-08-08; re-observed 2026-08-14 (`SRC-WERPC-076`)                                                                              | Verified — structural contract (route, frontmatter, status domain, required H2 set, `bodyContract` reciprocity/identifier rule); content, implementation, and delivery effectiveness remain DEFER                                                |
| REQ-WERPC-035 | Task                    | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `docs/04.execution/tasks/`                                                                          | GitHub Spec Kit specification-driven and agentic SDD guidance plus local profile/template/validator evidence, checked 2026-08-08; re-observed 2026-08-14 (`SRC-WERPC-076`)                                                                              | Verified — structural contract (route, frontmatter, status domain, required H2 set, `bodyContract` reciprocity/identifier rule); content, implementation, and delivery effectiveness remain DEFER                                                |
| REQ-WERPC-036 | Plan                    | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                  | `docs/04.execution/plans/`                                                                          | GitHub Spec Kit specification-driven and agentic SDD guidance plus local profile/template/validator evidence, checked 2026-08-08; re-observed 2026-08-14 (`SRC-WERPC-076`)                                                                              | Verified — structural contract (route, frontmatter, status domain, required H2 set, `bodyContract` reciprocity/identifier rule); content, implementation, and delivery effectiveness remain DEFER                                                |

### 2026-08-10 gap-only refresh reconciliation

The WERG-004 closure snapshot recorded exactly 13 pack files, 33 unique request
owners, 65 unique source IDs, and 65 unique claim IDs: frozen rows through
`SRC-WERPC-052` and `CLM-WERPC-006-08`, document and Verification/Validation
additions `SRC-WERPC-053`–`059` and `CLM-WERPC-007-01`–`08`, and
Kubernetes/Security additions `SRC-WERPC-060`–`065` and
`CLM-WERPC-008-01`–`06`. The five mutable research owners for that closure were
this README, the SDLC report, the CI/CD and QA report, the Kubernetes/Security
report, and the source/claim ledger.

After the later scope index and freshness/upstream source rows, the pack
contained 14 physical Markdown files including this README, 33 unique request
owners, 67 unique source IDs, and 65 unique claim IDs. Static validation does
not promote any hosted, provider-runtime, remote, credential-bearing, secret,
artifact, or live evidence from `DEFER`.

### 2026-08-11 Partial/DEFER refresh reconciliation

The 2026-08-11 Partial/DEFER incremental refresh, executed and checked on
2026-08-12, admitted exactly twelve candidates: `REQ-WERPC-006`, `008`, `009`,
`014`, `020`, `022`, `023`, `025`, `026`, `028`, `032`, and `033`. It created no
new research folder and no duplicate report. Findings were appended to the
existing owners as dated 2026-08-11 sections in
[governance](m0001-workspace-governance-and-common-agent-environment.md#2026-08-11-partialdefer-incremental-refresh),
[AI agents](m0009-ai-agents-and-agency-agents.md#2026-08-11-partialdefer-incremental-refresh),
[model routing](m0010-agent-model-routing-and-configuration.md#2026-08-11-partialdefer-incremental-refresh),
[memory](m0011-agent-memory-tiers-and-management.md#2026-08-11-partialdefer-incremental-refresh),
[Kubernetes and security](m0007-kubernetes-infrastructure-and-security.md#2026-08-11-partialdefer-incremental-refresh),
[Diátaxis](m0005-documentation-architecture-and-diataxis.md#2026-08-11-partialdefer-incremental-refresh),
[SDLC and document contracts](m0004-spec-driven-sdlc-and-document-contracts.md#2026-08-11-partialdefer-incremental-refresh),
and [CI/CD, Actions, and QA](m0008-ci-cd-github-actions-and-qa.md#2026-08-11-partialdefer-incremental-refresh).

All twelve candidates closed as `Partial`; none was promoted to `Verified`, so
every Status cell in the request matrix above keeps its prior value. Rows
`REQ-WERPC-014` and `REQ-WERPC-020` also carry `exclude-duplicate`, because
Spec 052 `DOC-G1`, `DOC-G2`, and `DOC-G3` already own those questions.

The refresh adds `SRC-WERPC-068`–`073` and `CLM-WERPC-009-01`–`12`, so the
current pack contains 14 physical Markdown files including this README, 33
unique request owners, 73 unique source IDs, and 77 unique claim IDs. No
existing source or claim row was renumbered or rewritten: `SRC-WERPC-073`
records the package's 2026-08-12 re-verification of already registered sources,
whose baseline `Checked on` values are preserved by contract and therefore lag
that re-verification. Hosted-runtime, provider-runtime, product and stakeholder
validation, cluster, credential-bearing, and live evidence remain `DEFER`.

### 2026-08-14 consistency and Partial re-observation reconciliation

This cycle (WRCP-000–WRCP-007) admitted two separate candidate sets. First,
WRCP-002, WRCP-003, WRCP-004, and WRCP-005 re-observed all twelve `Partial`
requirement rows carried forward from the 2026-08-11 refresh: `REQ-WERPC-006`,
`008`, `009`, `014`, `020`, `022`, `023`, `025`, `026`, `028`, `032`, and
`033`. Every one closed as `Partial` again; none was promoted, so **no
Status cell in the request matrix above changed as a result of this cycle**.
Second, WRCP-004 separately re-observed `REQ-WERPC-034`, `035`, and `036` —
the Spec, Task, and Plan document families — as three brand-new
coverage-matrix owner rows admitted by Spec 057 amendment `C-WRCP-010`. Per
that contract, admitting a family neither raises nor lowers a status: each
new row's Status is `Verified` on structural contract (route, frontmatter,
status domain, required H2 set, `bodyContract` reciprocity/identifier rule)
and `DEFER` on content, implementation, and delivery effectiveness, exactly
as WRCP-004 recorded in the
[SDLC and document contracts](m0004-spec-driven-sdlc-and-document-contracts.md#2026-08-14-consistency-and-partial-re-observation)
dated section. `C-WRCP-010` caps this admission at exactly three rows; no
fourth owner was added.

These three rows were absent before this cycle because the
[document-family contract matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)
describes twelve document families (PRD, ARD, ADR, Spec, Plan, Task, Guide,
Incident, Postmortem, Policy, Release, Runbook), while the coverage matrix
above registered owner rows for only nine of them (PRD, ARD, ADR, Guide,
Incident, Postmortem, Policy, Release, Runbook) before this cycle. No prior
WRCP request line named Spec, Task, or Plan explicitly, so no request-driven
research had ever produced a coverage-matrix row for them; three prior
refresh cycles (the 2026-08-10 gap-only refresh, the 2026-08-11 Partial/DEFER
refresh, and the intervening freshness pass) missed this for the same
reason.

Findings for both sets are recorded in dated 2026-08-14 sections in
[governance](m0001-workspace-governance-and-common-agent-environment.md#2026-08-14-consistency-and-partial-re-observation),
[AI agents](m0009-ai-agents-and-agency-agents.md#2026-08-14-consistency-and-partial-re-observation),
[model routing](m0010-agent-model-routing-and-configuration.md#2026-08-14-consistency-and-partial-re-observation),
[memory](m0011-agent-memory-tiers-and-management.md#2026-08-14-consistency-and-partial-re-observation),
[Kubernetes and security](m0007-kubernetes-infrastructure-and-security.md#2026-08-14-consistency-and-partial-re-observation),
[Diátaxis](m0005-documentation-architecture-and-diataxis.md#2026-08-14-consistency-and-partial-re-observation),
[SDLC and document contracts](m0004-spec-driven-sdlc-and-document-contracts.md#2026-08-14-consistency-and-partial-re-observation),
and [CI/CD, Actions, and QA](m0008-ci-cd-github-actions-and-qa.md#2026-08-14-consistency-and-partial-re-observation).

The cycle registers `SRC-WERPC-074`–`077` (one per WRCP-002/003/004/005
package) and `CLM-WERPC-010-01`–`15` (four, three, five, and three claims
respectively). No existing source or claim row was renumbered or rewritten.
Counted directly against the tracked files rather than carried forward, the
pack now contains 14 physical Markdown files including this README
(unchanged), 36 unique request owners (33 plus the three admitted rows), 77
unique source IDs (73 plus `SRC-WERPC-074`–`077`), and 92 unique claim IDs
(77 plus `CLM-WERPC-010-01`–`15`). Hosted-runtime, provider-runtime, cluster,
credential-bearing, and live evidence remain `DEFER`.

### 2026-08-17 full-corpus refresh reconciliation

This cycle (WRFC-000–WRFC-012, Spec 058) is the first to re-observe **all
thirty-six** owner rows rather than a twelve-row `Partial` sample. Its scope was
byte-equivalent to the Spec 057 request, so the cycle was deliberately redirected
to the two places where new information was reachable: the twenty-four `Verified`
rows that had gone unchecked since 2026-08-08, and a terminal blocking-class
closure over every retained `Partial` and `DEFER` row.

**Six rows returned `changed` externally.** Three of them — `REQ-WERPC-004`,
`011`, and `021` — carry status `Verified` and were therefore structurally
outside the sample the three preceding cycles re-tested.

| Request ID    | Prior status  | External change observed 2026-08-17                                    |
| ------------- | ------------- | ---------------------------------------------------------------------- |
| REQ-WERPC-004 | Verified      | Claude Code advanced from observed `2.1.220` to `2.1.233` (2026-08-14) |
| REQ-WERPC-006 | Partial       | Claude memory and subagent pages grew beyond the adopted scope         |
| REQ-WERPC-008 | Partial       | kube-state-metrics pin `v2.14.0` versus upstream `v2.19.1`             |
| REQ-WERPC-011 | Verified      | `ISO/IEC/IEEE DIS 29148` entered ballot; 2018 edition not superseded   |
| REQ-WERPC-021 | Verified      | `llms.txt` reached v2; MCP `2026-07-28` superseded the cited path      |
| REQ-WERPC-025 | Partial       | Argo CD `sourceIntegrity` shipped GA in `3.5.0` and `3.5.1`            |

**Two of this pack's own recorded refresh triggers fired.** `SRC-WERPC-060`
declared a kube-state-metrics version change a trigger, and `SRC-WERPC-063`
declared an Argo CD source-integrity change a trigger. Both conditions are now
met. That is a contract signal, not a judgement call, and it means
`REQ-WERPC-008` and `REQ-WERPC-025` carry an admitted-but-unexecuted targeted
refresh as their next action.

**No status changed.** All thirty-six rows recorded `statusEffect` of
`no-change`; none was promoted, demoted, or contradicted, so **every Status cell
in the request matrix above keeps its prior value**. Under Spec 058 `C-WRFC-004`
that is a success provided the delta is recorded, and the six `changed` results
plus the two fired triggers are that delta.

**Zero rows returned `unreachable`,** which is itself a delta. Prior cycles
recorded `diataxis.fr` behind HTTP 429 on three separate attempts and fell back
to the upstream source that builds the site (`SRC-WERPC-067`). On 2026-08-17 the
published page responded directly, registered as `SRC-WERPC-089`, so that
fallback was not needed. Two other hosts, `iso.org` and once
`docs.aws.amazon.com`, returned HTTP 403 and were resolved through a
search-mediated fallback rather than recorded as unreachable.

**Terminal blocking-class closure** is recorded in the
[scope application index](m0013-scope-application-index.md#2026-08-17-full-corpus-re-projection-and-blocking-class-closure).
Twelve rows are unblocked, ten are reachable by repository-static work, and
fourteen are structurally unreachable and are closed against further static
re-testing with a named reopen condition each. This is why Specs 055, 056, and
057 promoted nothing: their sample was drawn without regard to whether the
blocking evidence was reachable at all.

Findings are recorded as dated 2026-08-17 sections in
[governance](m0001-workspace-governance-and-common-agent-environment.md#2026-08-17-full-corpus-refresh),
[harness and loop](m0002-harness-and-loop-engineering.md#2026-08-17-full-corpus-refresh),
[provider status](m0003-provider-implementation-status.md#2026-08-17-full-corpus-refresh),
[SDLC and document contracts](m0004-spec-driven-sdlc-and-document-contracts.md#2026-08-17-full-corpus-refresh),
[Diátaxis](m0005-documentation-architecture-and-diataxis.md#2026-08-17-full-corpus-refresh),
[LLM-WIKI](m0006-llm-wiki-and-knowledge-routing.md#2026-08-17-full-corpus-refresh),
[Kubernetes and security](m0007-kubernetes-infrastructure-and-security.md#2026-08-17-full-corpus-refresh),
[CI/CD, Actions, and QA](m0008-ci-cd-github-actions-and-qa.md#2026-08-17-full-corpus-refresh),
[AI agents](m0009-ai-agents-and-agency-agents.md#2026-08-17-full-corpus-refresh),
[model routing](m0010-agent-model-routing-and-configuration.md#2026-08-17-full-corpus-refresh),
and [memory](m0011-agent-memory-tiers-and-management.md#2026-08-17-full-corpus-refresh).

The cycle registers `SRC-WERPC-078`–`089` and `CLM-WERPC-011-01`–`39`, one claim
per owner row plus three cycle-level claims. No existing source, claim, or
requirement row was renumbered or rewritten. Counted directly against the tracked
files, the pack now contains **14 physical Markdown files** including this README
(unchanged), **36 unique request owners** (unchanged), **89 unique source IDs**
(77 plus twelve), and **131 unique claim IDs** (92 plus thirty-nine). Every
referenced identifier has a registered ledger row: 89 source rows and 131 claim
rows. Hosted-runtime, provider-runtime, cluster, credential-bearing, and live
evidence remain `DEFER`.

Two limitations are recorded rather than concealed. The package owning the
document-family rows executed without a shell tool, so `Spec`, `Task`, `Plan`,
and `Guide` instance tallies were **not** re-counted and the 2026-08-14 counts
are carried forward unverified; and the then-current LLM-WIKI generated-index
check was **not** executed, so index freshness was inferred from unchanged
frontmatter dates rather than proven.

Both limitations were closed with executed evidence before integration, so
neither carried into the successor cycle. The historical drift check returned
PASS, confirming the inferred freshness at that time; the generated index and
its generator were later retired from the current workspace.
A fresh frontmatter tally reproduces the 2026-08-14 Spec, Task, and Plan
baselines apart from one ordinary `active`-to-`done` transition per family, and
zero `archived` use still holds, so no recorded tally is contradicted. Direct
enumeration also corrected three counts that had been reported but deliberately
not recorded: ARD, ADR, and Runbook hold eight, seventeen, and nine dated
instances rather than nine, eighteen, and ten, each inflated by one because
`README.md` was counted as an instance.

### 2026-08-18 correction reconciliation

A follow-up verification on 2026-08-18 **withdrew one claim** made by the
2026-08-17 cycle. The cycle had stated that upstream kube-state-metrics added a
`serviceaccounts` resource absent at `v2.14.0`. Retrieving and diffing the shipped
standard `ClusterRole` at both tags shows them byte-identical except the version
label, so `serviceaccounts` was already present and upstream changed no
ClusterRole rule in that range. The statement is corrected in place in the
[Kubernetes and security report](m0007-kubernetes-infrastructure-and-security.md#2026-08-18-correction-to-the-2026-08-17-kube-state-metrics-statement)
and in the cycle Task, and is registered as `CLM-WERPC-012-01` with status
`Contradicted` — the first use of that status value in this pack.

The correction sharpens rather than weakens the underlying finding. The real
divergence is that this repository's hand-curated ClusterRole has always been a
trimmed subset of upstream's, and two of its omissions —
`certificates.k8s.io/certificatesigningrequests` and
`coordination.k8s.io/leases` — are documented default resources that the
deployment has been collecting without the required permissions for the life of
the current pin. That is a live pre-existing defect rather than an upgrade
consequence. Exactly one RBAC requirement is introduced by upgrading:
`discovery.k8s.io/endpointslices`, because `v2.18.0` swapped it in as a default
and the Deployment declares no `args:`.

The correction registers `SRC-WERPC-090` and `CLM-WERPC-012-01`–`04`. No existing
source, claim, or requirement row was renumbered, and no requirement owner was
created. Counted against the tracked files the pack now contains 14 physical
Markdown files, 36 unique request owners, **90 unique source IDs**, and **135
unique claim IDs**, with 90 source rows and 135 claim rows registered in the
ledger. `REQ-WERPC-008` keeps `Partial`; withdrawing a claim does not change a
status, and hosted-runtime, provider-runtime, cluster, and live evidence remain
`DEFER`.

### 2026-08-20 full-corpus reverification reconciliation

| Field | Value |
| --- | --- |
| Census | markdownFiles=14, requests=36, sources=91, claims=141 |
| External results | changed=3, unchanged=32, unreachable=1 |
| Workspace results | confirmed=29, drifted=6, absent=1 |
| Dispositions | Verified=20, Verified gap=4, Partial=12 |
| Evidence depths | repository-static=28, public-documentation=8 |
| Blocking classes | none=12, repo-static=10, provider-runtime=5, hosted-ci=2, live-cluster=3, human-judgement=4 |
| Changed requests | REQ-WERPC-004, REQ-WERPC-006, REQ-WERPC-008, REQ-WERPC-009, REQ-WERPC-011, REQ-WERPC-012, REQ-WERPC-013, REQ-WERPC-018, REQ-WERPC-025 |
| Unreachable requests | REQ-WERPC-033 |
| Allocated K3s observation | SRC-WERPC-091; request=REQ-WERPC-009 |
| Allocated claims | CLM-WERPC-013-01, CLM-WERPC-013-02, CLM-WERPC-013-03, CLM-WERPC-013-04, CLM-WERPC-013-05, CLM-WERPC-013-06 |
| Terminology claims | CLM-WERPC-013-01, CLM-WERPC-013-02, CLM-WERPC-013-03 |
| Drift claims | CLM-WERPC-013-04, CLM-WERPC-013-05, CLM-WERPC-013-06 |
| Out-of-ledger observations | observed proposals=1; allocated=1; unallocated=0; outside-request/new-owner=0; SRC-WERPC-091->REQ-WERPC-009 |

### 2026-09-05 external-only reverification reconciliation

The approved 2026-09-05 follow-on cycle re-observed the external evidence layer
for all thirty-six owners and deliberately excluded workspace re-observation at
the requester's direction. It appended one dated subsection to each topical
owner, extended the ledger to `SRC-WERPC-154`, opened the claim block
`CLM-WERPC-016-01` through `CLM-WERPC-016-18`, and changed no requirement
status.

Reported outcomes:

- **Changed with a superseded prior statement.** Three statements are superseded
  as of 2026-09-05 and their earlier forms remain truthful for their own dates:
  the subagent model-resolution order recorded on 2026-08-14; the claim that the
  upstream agent catalogue's default branch is byte-identical to the retained
  comparison pin; and one delivery citation confirmed dead by direct request and
  repointed to its current location.
- **Changed by coverage.** Official definitions of an agent harness and of loop
  types now exist and are registered for the first time; a cross-provider
  instruction-import bridge is documented by both providers; the permission-mode
  and hook surfaces are materially wider than any list this pack had enumerated;
  and the upstream spec-driven project reached a 1.0 line with additional
  command families.
- **Changed by currency.** A new orchestrator minor released after the previous
  increment and shifted the supported set; the node distribution and
  log-collection agent drifted further beyond their recorded pins; and a
  secret-management operator release was captured for the first time.
- **Unchanged.** The instruction-discovery chain and its size limit, the
  configuration reference, the sandbox and approval vocabulary, the second
  provider's memory default, the documentation framework's four modes, the
  current protocol revision and its resource semantics, the index proposal's
  informal status, the standards content behind a changed access path, and the
  delivery platform's permission, concurrency, retention, federated-identity,
  and API-version contracts.
- **Unreachable.** One vendor agent guide could not be read: its HTML mirror
  returned HTTP 403 and its document body was not extracted. It is recorded as
  `unreachable`, not `unchanged`, and no claim rests on it. Two public indexes
  disagree on the stage of one standards successor draft and the page that would
  settle it returned HTTP 403; that discrepancy is recorded as unresolved.
- **Rejected before allocation.** Three link-rot candidates raised during
  collection were withdrawn after direct requests contradicted them, and one
  redirect contradiction supported only by search results is recorded as
  unverified rather than as a finding.

This cycle records an external observation only. It does not meet the
dual-observation expectation of the earlier full-corpus cycles, every workspace
selector retains its previous observation date, and no statement here asserts
that the pack is currently reconciled against the repository tree.

## Refresh and Succession

WERPC-002 through WERPC-006 add dated source-backed findings to their assigned
owners. WERPC-007 classifies mutable consumers; WERPC-008 alone may delete
predecessor files after its fail-closed readiness proof.

## Evidence Boundary

This baseline records repository-static paths and historical predecessor
evidence. It does not claim hosted CI, provider runtime, authentication,
remote, credential-bearing, secret-value, or live-cluster evidence.

## Related Documents

- [WERPC Plan](../../../98.archive/completed/03.specs/0053-workspace-engineering-research-pack-consolidation/plan.md)
- [WERPC Plan](../../../98.archive/completed/03.specs/0053-workspace-engineering-research-pack-consolidation/plan.md)
- [Source coverage](m0012-source-coverage.md)
