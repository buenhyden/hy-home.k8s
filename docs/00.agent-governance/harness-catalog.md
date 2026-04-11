---
title: "Reference: Local Harness Catalog"
type: reference
status: draft
owner: "platform"
updated: 2026-04-11
---

# Reference: Local Harness Catalog

## Overview

This document is the canonical catalog for the local agent runtime used in `hy-home.k8s`.
It defines the supported agents, skills, model allocation, scope imports, and pattern families
that shape the runtime contract under `.claude/`.

## Purpose

- Provide a single source of truth for the local runtime roster.
- Keep gateway files and runtime files in sync.
- Record the model hierarchy for supervising and worker agents.
- Preserve pattern lineage without exposing source directory paths.

## Scope

- Covers local runtime agents, skills, scope imports, and model allocation.
- Does not duplicate rule text from `rules/`, `scopes/`, or `providers/`.

## Runtime Principles

- The local runtime is cluster-specific and GitOps-first.
- Supervising agents use `opus`.
- Task and worker agents use `sonnet`.
- Agent files are thin runtime bridges and must not duplicate governance policy.
- Skill files are workflow contracts and must remain specific to this cluster.

## Agents

| File | Role | Model | Scope Imports | Responsibility | Lineage Family |
| --- | --- | --- | --- | --- | --- |
| `.claude/agents/supervisor.md` | Task routing and orchestration control | `opus` | `meta` | Select agents, enforce completion gates, synthesize outcomes | orchestration |
| `.claude/agents/k8s-implementer.md` | Kubernetes manifest authoring | `sonnet` | `infra` | Author GitOps-safe manifest changes and prepare validation-ready output | cicd-pipeline, infra-as-code, security-audit |
| `.claude/agents/gitops-reviewer.md` | GitOps pipeline and ArgoCD review | `sonnet` | `infra` | Review sync targets, Kustomize structure, and GitOps release safety | cicd-pipeline, infra-as-code, security-audit |
| `.claude/agents/security-auditor.md` | Kubernetes security review | `sonnet` | `security` | Review RBAC, network isolation, and secret handling | security-audit |
| `.claude/agents/incident-responder.md` | Cluster incident analysis | `sonnet` | `ops`, `infra` | Reconstruct timelines, assess impact, and define remediation | incident-postmortem |
| `.claude/agents/code-reviewer.md` | YAML, Helm, and shell quality review | `sonnet` | `architecture` | Review correctness, maintainability, and policy alignment | code-reviewer |
| `.claude/agents/doc-writer.md` | Runbook and guide authoring | `sonnet` | `docs` | Produce template-aligned operational and explanatory documents | technical-writer |

## Skills

| Path | Purpose | Supported Workflows | Lineage Family |
| --- | --- | --- | --- |
| `.claude/skills/gitops-workflow/skill.md` | Define the approved GitOps workflow for onboarding, updating, and diagnosing workloads | onboarding, change review, sync diagnosis | cicd-pipeline, infra-as-code, security-audit |
| `.claude/skills/k8s-validate/skill.md` | Define the manifest validation pipeline for YAML, GitOps structure, and secret scanning | validation, pre-PR checks, failure triage | cicd-pipeline, infra-as-code, security-audit |
| `.claude/skills/risk-report/skill.md` | Define the cluster risk register workflow and output shape | risk identification, risk tracking, review cadence | risk-register |

## Consistency Rules

- `AGENTS.md §3` must match the Agents table in this document.
- Root `CLAUDE.md` and `GEMINI.md` must point to this catalog when describing runtime agents.
- `.claude/CLAUDE.md` must remain the runtime baseline for local agent execution.
- Any new local agent or skill must be added here in the same change set.

## Related Documents

- [AGENTS.md](../../AGENTS.md)
- [Runtime Baseline](../../.claude/CLAUDE.md)
- [Subagent Protocol](./subagent-protocol.md)
- [Claude Provider Notes](./providers/claude.md)
