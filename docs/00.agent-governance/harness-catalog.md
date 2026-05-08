---
title: 'Reference: Local Harness Catalog'
type: reference
status: draft
owner: 'platform'
updated: 2026-04-20
---

# Reference: Local Harness Catalog

## Overview

This document is the canonical catalog for the local agent runtime used in `hy-home.k8s`.
It defines the supported agents, skills, model allocation, scope imports, and pattern families
that shape the runtime contract under `.claude/` and its Codex mirror under `.codex/`.

## Purpose

- Provide a single source of truth for the local runtime roster.
- Keep gateway files and runtime files in sync.
- Keep `.claude/agents/*.md` and `.codex/agents/*.toml` mirrors in sync.
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
- Codex mirror files are thin runtime bridges with the same contract as their `.claude` source.
- Skill files are workflow contracts and must remain specific to this cluster.

## Agents

| File                                   | Role                                   | Model    | Scope Imports  | Responsibility                                                          | Lineage Family                               |
| -------------------------------------- | -------------------------------------- | -------- | -------------- | ----------------------------------------------------------------------- | -------------------------------------------- |
| `.claude/agents/supervisor.md`         | Task routing and orchestration control | `opus`   | `meta`         | Select agents, enforce completion gates, synthesize outcomes            | orchestration                                |
| `.claude/agents/k8s-implementer.md`    | Kubernetes manifest authoring          | `sonnet` | `infra`        | Author GitOps-safe manifest changes and prepare validation-ready output | cicd-pipeline, infra-as-code, security-audit |
| `.claude/agents/gitops-reviewer.md`    | GitOps pipeline and ArgoCD review      | `sonnet` | `infra`        | Review sync targets, Kustomize structure, and GitOps release safety     | cicd-pipeline, infra-as-code, security-audit |
| `.claude/agents/security-auditor.md`   | Kubernetes security review             | `sonnet` | `security`     | Review RBAC, network isolation, and secret handling                     | security-audit                               |
| `.claude/agents/incident-responder.md` | Cluster incident analysis              | `sonnet` | `ops`, `infra` | Reconstruct timelines, assess impact, and define remediation            | incident-postmortem                          |
| `.claude/agents/code-reviewer.md`      | YAML, Helm, and shell quality review   | `sonnet` | `architecture` | Review correctness, maintainability, and policy alignment               | code-reviewer                                |
| `.claude/agents/doc-writer.md`         | Runbook and guide authoring            | `sonnet` | `docs`         | Produce template-aligned operational and explanatory documents          | technical-writer                             |

## Codex Mirrors

`.codex/agents/*.toml` mirrors the corresponding `.claude/agents/*.md` worker
contracts for Codex execution. Mirror files must keep the same name, role,
scope imports, guardrails, and postflight requirements. Update the `.claude`
source and Codex mirror in the same change set.

## Skills

| Path                                             | Purpose                                                                                                                          | Supported Workflows                                                                 | Lineage Family                               |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | -------------------------------------------- |
| `.claude/skills/gitops-workflow/skill.md`        | Define the approved GitOps workflow for onboarding, updating, and diagnosing workloads                                           | onboarding, change review, sync diagnosis                                           | cicd-pipeline, infra-as-code, security-audit |
| `.claude/skills/docs-stage-routing/skill.md`     | Route generated documentation into the canonical stage tree and block parallel doc hierarchies                                   | doc routing, template selection, stage mapping, superpowers rerouting                | governance, technical-writer                  |
| `.claude/skills/k8s-validate/skill.md`           | Define the manifest validation pipeline for YAML, GitOps structure, and secret scanning                                          | validation, pre-PR checks, failure triage                                           | cicd-pipeline, infra-as-code, security-audit |
| `.claude/skills/risk-report/skill.md`            | Define the cluster risk register workflow and output shape                                                                       | risk identification, risk tracking, review cadence                                  | risk-register                                |
| `.claude/skills/deployment-strategies/skill.md`  | Kubernetes and ArgoCD deployment strategy catalog with YAML patterns, health check probes, rollback procedures, and DORA metrics | deployment planning, strategy selection, rollback, DORA measurement                 | cicd-pipeline                                |
| `.claude/skills/incident-postmortem/skill.md`    | Full pipeline for cluster incident post-analysis: timeline → RCA → impact → remediation → postmortem report                      | postmortem authoring, incident review, RCA, remediation planning                    | incident-postmortem                          |
| `.claude/skills/rca-methodology/skill.md`        | Structured RCA technique reference: 5 Whys, Fishbone, Fault Tree Analysis, Change Analysis, and cognitive bias prevention        | root cause analysis, 5 Whys, fishbone, FTA, change analysis                         | incident-postmortem                          |
| `.claude/skills/k8s-security-audit/skill.md`     | Structured security audit workflow: RBAC, NetworkPolicy, Secret handling, container security context, and image supply chain     | security audit, RBAC review, network policy audit, secret scanning, CIS benchmark   | security-audit                               |
| `.claude/skills/vulnerability-patterns/skill.md` | Kubernetes manifest and Helm chart vulnerability pattern catalog with VULNERABLE/SAFE YAML examples and CIS benchmark mappings   | manifest hardening, YAML security review, Helm security, misconfiguration detection | security-audit, code-reviewer                |

## Consistency Rules

- `AGENTS.md` must route to this catalog instead of embedding a duplicate agent table.
- Root `CLAUDE.md` and `GEMINI.md` must point to this catalog when describing runtime agents.
- `.claude/CLAUDE.md` must remain the runtime baseline for local agent execution.
- `.codex/agents/*.toml` mirrors must stay aligned with `.claude/agents/*.md`.
- Document-generation workflows must use `.claude/skills/docs-stage-routing/skill.md` before proposing new authored-document paths.
- Any new local agent or skill must be added here in the same change set.

## Related Documents

- [AGENTS.md](../../AGENTS.md)
- [Runtime Baseline](../../.claude/CLAUDE.md)
- [Subagent Protocol](./subagent-protocol.md)
- [Claude Provider Notes](./providers/claude.md)
