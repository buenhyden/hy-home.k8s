---
title: 'Observability and Network Review Agents Agent Design'
type: sdlc/agent-design
status: done
owner: platform
updated: 2026-07-11
---

# Observability and Network Review Agents Agent Design

## Overview

This document defines the behavior of two worker-tier review agents,
`observability-reviewer` and `network-reviewer`, added to the `hy-home.k8s`
runtime roster. Both are repository-static, review-only delegated subagents.

## Parent Documents

- **Spec**: [./spec.md](./spec.md)
- **Gap-analysis reference**: [../../90.references/research/2026-07-04-wer/ai-agents-roster-and-gap-analysis.md](../../90.references/research/2026-07-04-wer/ai-agents-roster-and-gap-analysis.md)

## Scope & Non-goals

- **Covers**: manifest-static and documentation review for observability and
  network domains, plus provider-adapter and roster wiring.
- **Does Not Cover**: live metric scraping, live ingress probing, manifest
  authoring, RBAC/secret/network-isolation review (stays with
  `security-auditor`), or GitOps sync-structure review (stays with
  `gitops-reviewer`).

## Agent Role

- **Primary Role**: `observability-reviewer` reviews monitoring/observability
  manifests and SLO documentation; `network-reviewer` reviews ingress,
  Traefik, NetworkPolicy, DNS, and TLS wiring at the manifest level.
- **Primary User / Caller**: `supervisor` routing, or a human requesting a
  domain review.
- **Success Definition**: severity-ranked, evidence-cited findings that a
  human or `k8s-implementer` can act on, with no live-cluster claims.

## Inputs / Outputs

- **Inputs**: PR diff or manifest paths under `gitops/`, `traefik/`, or
  `infrastructure/`; optional review constraints.
- **Outputs**: findings with `file:line` evidence, severity, and remediation.
- **Expected Structured Format**: severity-ranked list plus a merge-readiness
  statement.

## Orchestration Model

- `router-specialist`
- **Why this model**: each agent owns a narrow domain and is dispatched by the
  supervisor when a change touches that domain.
- **Escalation / Handoff rules**: implementation to `k8s-implementer`;
  secret/RBAC/network-isolation to `security-auditor`; GitOps release
  structure to `gitops-reviewer`; ambiguous routing to `supervisor`.

## Tools & Permissions

| Tool | Purpose                | Allowed Actions                | Forbidden Actions                 | Failure Handling           |
| ---- | ---------------------- | ------------------------------ | --------------------------------- | -------------------------- |
| Read | Inspect manifests      | Read repo files                | Read secrets/credentials          | Report and stop            |
| Grep | Find patterns          | Search repo text               | Search outside repo               | Report empty results       |
| Glob | Enumerate manifests    | Match repo paths               | Match outside repo                | Report empty results       |
| Bash | Repo-static validation | Run read-only validators/tests | Live cluster or external mutation | Report tool/limit and stop |

## Prompt / Policy Contract

- **System Instruction Summary**: review-only domain reviewer bound to
  GitOps-first, no-plaintext-secrets, and manifest-static boundaries.
- **Policy Constraints**: policy stays in Stage 00 governance and is imported
  via `docs/00.agent-governance/scopes/infra.md`, not duplicated inline.
- **Versioning Rule**: adapter bodies stay aligned across three providers;
  changes route through this spec.

## Context & Memory Strategy

- **Session Context**: the current diff/manifests and review constraints.
- **Retrieval Strategy**: repository reads only.
- **Persistent Memory Rule**: durable lessons go to
  `docs/00.agent-governance/memory/progress.md`; no per-agent memory files.
- **Privacy / Retention Notes**: never read or echo secret values.

## Guardrails

- **Input Guardrails**: reject requests for live metrics or live ingress state.
- **Output Guardrails**: no live-runtime readiness claims; repo-static only.
- **Blocked Conditions**: any manifest mutation or cluster mutation.
- **Human Escalation Rule**: escalate destructive or cross-scope requests to
  `supervisor` and the human operator.

## Failure Modes & Fallback

- **Failure Mode 1**: overlap with `security-auditor`/`gitops-reviewer`.
- **Fallback 1**: hand off rather than duplicate findings.
- **Failure Mode 2**: request requires live data.
- **Fallback 2**: decline and state the repo-static boundary.

## Evaluation Plan

- **Offline Evals**: adapter parity, catalog rows, repo-static validation.
- **Online Signals**: not applicable; no live runtime.
- **Acceptance Thresholds**: `bash scripts/validate-repo-quality-gates.sh .`
  PASS and three-provider adapter parity.
- **Linked Task / Eval Docs**: [../../04.execution/tasks/2026-07-06-observability-and-network-review-agents.md](../../04.execution/tasks/2026-07-06-observability-and-network-review-agents.md)

## Observability

- **Trace fields**: not applicable to repo-static review.
- **Logs / Events**: findings recorded in review output and task evidence.
- **Redaction / Privacy Rules**: never surface secret values in findings.

## Related Documents

- **Spec**: [./spec.md](./spec.md)
- **Plan**: [../../04.execution/plans/2026-07-06-observability-and-network-review-agents.md](../../04.execution/plans/2026-07-06-observability-and-network-review-agents.md)
- **Harness catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Model policy**: [../../00.agent-governance/model-policy.md](../../00.agent-governance/model-policy.md)
