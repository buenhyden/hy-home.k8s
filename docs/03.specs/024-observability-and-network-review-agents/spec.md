---
title: 'Observability and Network Review Agents Technical Specification'
type: sdlc/spec
status: draft
owner: platform
updated: 2026-07-06
---

# Observability and Network Review Agents Technical Specification

## Overview

This spec defines two new worker-tier review agents for the `hy-home.k8s`
runtime roster: `observability-reviewer` and `network-reviewer`. Both are
repository-static, review-only agents that close roster gaps identified in the
AI agents roster and gap-analysis reference. The workspace already carries
observability manifests (`gitops/platform/monitoring/`, external Prometheus and
Grafana services, kube-state-metrics, Alloy, Kiali) and a non-trivial network
surface (`traefik/`, multiple ingress manifests, `gitops/platform/network-policies/`,
`infrastructure/tests/verify-ingress-tls.sh`) with no dedicated review owner.

## Strategic Boundaries & Non-goals

- **In scope**: two worker agents, their three provider adapters each, the
  harness catalog roster additions, and the Stage 03/04 governance chain.
- **Out of scope**: live cluster scraping, Prometheus/Grafana query execution,
  live ingress probing, editing manifests, changing model-policy tiers, or
  altering existing agents beyond adding handoff targets.
- **Non-goal**: replacing `security-auditor` (network isolation/RBAC/secrets
  stay there) or `gitops-reviewer` (sync-target/Kustomize structure stays
  there); the new agents review domain correctness, not those concerns.

## Related Inputs

- AI agents roster and gap-analysis reference:
  `../../90.references/research/2026-07-04-wer/ai-agents-roster-and-gap-analysis.md`
- Canonical roster: `../../00.agent-governance/harness-catalog.md`
- Canonical tier policy: `../../00.agent-governance/model-policy.md`
- Existing worker adapter pattern: `.claude/agents/gitops-reviewer.md`

## Contracts

- Both agents are `worker` tier and adhere to
  `docs/00.agent-governance/model-policy.md` tier identifiers.
- Both agents import `docs/00.agent-governance/scopes/infra.md`.
- Both agents are mirrored across `.claude/agents/*.md`,
  `.agents/agents/*.md`, and `.codex/agents/*.toml` with aligned role, scope
  import, guardrails, handoff, and postflight while preserving provider keys.

## Core Design

Each agent follows the existing worker-agent body skeleton (Runtime Bootstrap,
scope `@import`, Role, When to Use, Inputs, Outputs, Guardrails,
Handoff / Escalation, Postflight). They differ only in domain:

- `observability-reviewer`: monitoring/observability manifest and SLO-doc
  review — Prometheus/Grafana/kube-state-metrics/Alloy/Kiali manifests, scrape
  and alert wiring correctness at the manifest level, and SLO/error-budget
  documentation upkeep.
- `network-reviewer`: ingress/network manifest review — Traefik configuration,
  ingress objects, NetworkPolicy structure, DNS and TLS wiring correctness at
  the manifest level.

## Data Modeling & Storage Strategy

No new data stores. Durable lessons route to
`docs/00.agent-governance/memory/progress.md`; no per-agent memory files.

## Interfaces & Data Structures

### Core Interfaces

- Input: PR diff or manifest paths under `gitops/`, `traefik/`, or
  `infrastructure/` plus optional constraints.
- Output: severity-ranked findings with file:line evidence and a readiness
  statement for the relevant merge flow.

## API Contract (If Applicable)

Not applicable; these are delegated subagents, not network services.

## Agent Role & IO Contract (If Applicable)

Defined in the sibling `agent-design.md`.

## Tools & Tool Contract (If Applicable)

Least-privilege `tools: Read, Grep, Glob, Bash`, matching existing review
workers. Bash is limited to read-only repository inspection and repo-static
validators; no live cluster or external mutation.

## Prompt / Policy Contract (If Applicable)

System instruction summarized in each adapter body; policy stays in Stage 00
governance and is imported by scope, not duplicated inline.

## Memory & Context Strategy (If Applicable)

Session-scoped only. Persistent lessons go to the progress ledger.

## Guardrails (If Applicable)

- Review-only unless a human explicitly requests implementation.
- No live cluster scraping, querying, or probing; manifest-static review only.
- Enforce GitOps-first and no-plaintext-secrets boundaries.
- Escalate secret/RBAC/network-isolation findings to `security-auditor`.

## Evaluation (If Applicable)

Acceptance is repo-static: adapter parity across three providers, catalog
roster rows present, and `bash scripts/validate-repo-quality-gates.sh .` PASS.

## Edge Cases & Error Handling

- Overlap with `security-auditor` or `gitops-reviewer`: defer to those owners
  via handoff rather than duplicating findings.
- Requests for live metrics or live ingress state: decline and state the
  repo-static boundary.

## Failure Modes & Fallback / Human Escalation

- If a change spans implementation, hand off to `k8s-implementer`.
- If routing is ambiguous, escalate to `supervisor`.

## Verification Commands

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

## Success Criteria & Verification Plan

- Two agents exist across all three provider adapters with aligned contracts.
- Harness catalog roster and adapter tables list both agents.
- Repo-static validation passes and evidence is recorded in the Stage 04 task.

## Related Documents

- **Agent Design**: [./agent-design.md](./agent-design.md)
- **Plan**: [../../04.execution/plans/2026-07-06-observability-and-network-review-agents.md](../../04.execution/plans/2026-07-06-observability-and-network-review-agents.md)
- **Task**: [../../04.execution/tasks/2026-07-06-observability-and-network-review-agents.md](../../04.execution/tasks/2026-07-06-observability-and-network-review-agents.md)
- **Gap-analysis reference**: [../../90.references/research/2026-07-04-wer/ai-agents-roster-and-gap-analysis.md](../../90.references/research/2026-07-04-wer/ai-agents-roster-and-gap-analysis.md)
- **Harness catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Model policy**: [../../00.agent-governance/model-policy.md](../../00.agent-governance/model-policy.md)
