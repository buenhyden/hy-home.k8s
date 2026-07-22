---
title: 'Workspace Agent Roster and Projection Design'
type: sdlc/agent-design
status: draft
owner: platform
updated: 2026-07-22
---

# Workspace Agent Roster and Projection Design

## Overview

This document defines the provider-neutral role shape consumed by the Stage 00
harness contract. It fixes the intended target at 12 canonical roles and four
projections per role, while leaving provider-surface admission to Spec 042 and
role admission/final model fitness to Spec 044. Spec 041 encodes, but does not
expand, the implemented 10-role/30-adapter baseline. The external-fact cutoff
is **2026-07-10 10:00 Asia/Seoul**.

## Scope & Non-goals

- **Covers**: canonical role boundaries, structured input/output, permission
  classes, stop/handoff rules, evaluation obligations, orchestration, and the
  four-surface projection invariant.
- **Does not cover**: provider installation/authentication, credentials, live
  provider claims, unbounded autonomous execution, or direct adoption of an
  external persona catalog.
- The current 10-role/30-adapter implementation remains authoritative until
  Specs 041–045 complete their consumer-first migration.

## Agent Role

| Role | Primary responsibility | Default risk class |
| --- | --- | --- |
| `supervisor` | Route work, enforce dependencies, synthesize evidence | R2 |
| `k8s-implementer` | Author GitOps-safe manifest changes | R2 |
| `gitops-reviewer` | Review ArgoCD/Kustomize release structure | R2 read-only |
| `security-auditor` | Review RBAC, secret, isolation, and supply-chain risk | R2 read-only |
| `incident-responder` | Reconstruct incidents and hand off remediation | R2 read-only |
| `code-reviewer` | Review correctness, maintainability, and policy alignment | R1 read-only |
| `doc-writer` | Route and author governed documentation | R1 |
| `wiki-curator` | Maintain generated owner/link maps | R1 |
| `observability-reviewer` | Review telemetry manifests and SLO documents | R2 read-only |
| `network-reviewer` | Review ingress, TLS, DNS, and NetworkPolicy manifests | R2 read-only |
| `docs-researcher` | Verify official sources and produce cited evidence ledgers | R1 read-only |
| `quality-engineer` | Design QA/eval fixtures and reconcile CI evidence | R2, mutation by task |

At target promotion, each role must have exactly one adapter under
`.agents/agents`, `.claude/agents`, `.codex/agents`, and `.gemini/agents`,
producing **12 roles / 48 adapters**. Before that promotion, the contract must
report the current 10/30 set and the pending target separately; target entries
are not counted as implemented parity.

## Inputs / Outputs

- **Common inputs**: task ID, authorized scope, repository paths, upstream
  requirements, risk class, allowed evidence sources, expected result class,
  and explicit external-action approvals.
- **Common outputs**: result summary, changed or reviewed paths, findings or
  artifacts, validation commands/results, limitations, stop reason, and next
  owner.
- Provider adapters may encode fields differently, but must not drop the
  canonical input/output semantics.
- Output must never include credential values, tokens, private auth files,
  shell history, or a raw provider transcript.

## Orchestration Model

- Use a `supervisor -> specialist -> reviewer -> supervisor` hierarchy.
- Fan-out is allowed only for independent, non-overlapping ownership. Fan-in
  requires explicit evidence reconciliation before synthesis.
- Writers and implementers do not approve their own work. Requirements review
  precedes quality/security review for each logical tranche.
- Specs 041–046 execute sequentially; an unfinished predecessor blocks routing
  to a later tranche.
- Subagents cannot silently expand task authority or delegate beyond the
  provider's supported recursion boundary.

## Tools & Permissions

| Permission class | Typical roles | Allowed | Forbidden without approval |
| --- | --- | --- | --- |
| Read-only evidence | reviewers, `docs-researcher` | Repository reads, search, static analysis | File mutation, secrets, external writes |
| Scoped authoring | implementer, writers, `quality-engineer` | Owned paths and deterministic local validation | Live cluster/provider mutation, credential changes |
| Orchestration | `supervisor` | Delegate bounded tasks and reconcile evidence | Grant broader authority than the parent task |

Provider-native tool lists are least-privilege projections. Claude `tools`,
Codex sandbox/approval and Gemini tool/policy settings are not interchangeable
enforcement claims.

## Prompt / Policy Contract

Every role projection carries or imports:

- purpose and non-responsibilities;
- canonical inputs and structured outputs;
- allowed/prohibited actions and approval boundaries;
- validation and evidence obligations;
- bounded stop conditions and handoff targets;
- provider-specific model/effort reference, never an unverified capability
  claim;
- Stage 00 and scope imports rather than copied durable policy.

Role descriptions are operational contracts, not personality prompts.
`agency-agents` may suggest a capability family but cannot supply local
authority, permissions, acceptance thresholds, or model fitness.

## Context & Memory Strategy

- Load Stage 00 and the minimum provider/scope context just in time.
- Treat repository state as authoritative after compaction or handoff.
- Use `.agent-work/checkpoint.json` only as ignored recovery metadata under
  Spec 043; never as durable governance or conversation storage.
- Promote durable decisions and evidence to the canonical SDLC document or
  progress ledger; discard local scratch after handoff.

## Guardrails

- Keep GitOps-first, no-plaintext-secret, no unapproved live mutation, and
  least-privilege boundaries across all projections.
- Distinguish repo-static, provider-runtime, CI, and remote-live evidence.
- Stop on scope expansion, repeated no-progress, missing required approval,
  ambiguous current owner, or a provider schema/runtime mismatch.
- A role/model fallback must name the actual model, reason, limitation, and
  affected evidence; silent substitution is prohibited.

## Failure Modes & Fallback

- **Partial adapter set**: fail exact parity and roll back the incomplete role
  admission.
- **Overlapping role**: reject admission or narrow responsibilities before
  creating adapters.
- **Unavailable provider/model**: record ABSENT/BLOCKED and route only if an
  approved fallback preserves the task contract; never claim parity.
- **Self-review conflict**: assign a fresh reviewer or escalate to the human
  owner.
- **Unsafe request**: stop and request explicit authority rather than weakening
  the role prompt.

## Evaluation Plan

- Each role has positive, negative, refusal, handoff, evidence-quality, and
  provider-projection fixtures.
- `docs-researcher` must prefer official primary sources, label cutoff
  uncertainty, and reject unsupported recency claims.
- `quality-engineer` must select the correct validation lane, distinguish
  formatter mutations, and reject waiver-based completion.
- Model/effort candidates are compared per role on correctness, safety,
  refusal, evidence quality, latency/cost observation, and repeatability.
- Spec 044 owns corpus versioning, independent adjudication, admission
  threshold, rollback, and final 12/48 proof.

## Observability

Record task ID, role, provider, adapter path, actual model/effort, tool class,
attempt count, result class, validation summary, stop/handoff reason, and
redaction status. Logs contain summaries and stable evidence references, not
prompts, full transcripts, credentials, or secret-bearing tool output.

## Traceability

- **Parent Spec**: [Spec 041](./spec.md)
- **Program requirement**: [PRD 003](../../01.requirements/003-workspace-agent-governance-platform.md)
- **Architecture**: [ARD 0006](../../02.architecture/requirements/0006-workspace-agent-governance-platform.md)
- **Proposed decision**: [ADR 0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- **Admission and eval owner**: [Spec 044](../044-agent-roster-evaluation-and-admission/spec.md)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-PRD-FUN-12](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-SAGC-AD-001 | Exact-set fixtures prove 12 canonical roles and one projection per role per surface. |
| [REQ-PRD-MET-06](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-SAGC-AD-002 | Roster/schema validators reject missing, extra, duplicate, or orphan adapters. |
| [REQ-PRD-MET-10](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-SAGC-AD-003 | Role eval and model-fitness records prove structured semantics and provider-specific selection. |
