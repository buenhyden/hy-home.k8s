---
title: 'Workspace Document Assurance Operating Model Architecture Reference Document'
type: sdlc/ard
status: accepted
owner: platform
updated: 2026-07-12
---

# Workspace Document Assurance Operating Model Architecture Reference Document (ARD)

## Overview

This architecture defines how human-readable governance, machine-readable
document profiles, template forms, authored documents, validators, provider
adapters, and CI selectors interact. The operating model has one owner per
fact and treats every copied table or prose summary as a non-authoritative view.

## Summary

Stage 99 owns document profile and form contracts; Stage 00 owns agent-facing
execution policy; authored stages own topic facts and evidence; validators and
CI consume machine contracts; README and provider shims only route readers to
owners. Seven sequential Specs migrate these responsibilities without a
big-bang gate cutover.

## Boundaries & Non-goals

- **Owns**: Contract ownership, registry interfaces, document and README
  profiles, validation lanes, migration waves, provider semantic parity,
  protected-surface static assurance, and rollback boundaries.
- **Consumes**: Current research and audit findings, accepted ADRs, tracked
  repository behavior, provider-native schemas, official external sources, and
  existing quality gates.
- **Does Not Own**: Product runtime behavior, remote repository settings,
  provider entitlements, cluster state, secret values, or operator credentials.
- **Non-goals**: Replacing provider-native adapters with one file format,
  generating unsupported metadata, claiming runtime readiness from repository
  evidence, or creating a root architecture summary.

## Quality Attributes

- **Performance**: Affected-file validation remains fast; all-files and domain
  gates are reserved for task completion and CI.
- **Security**: Exact metadata profiles, least-privilege workflow permissions,
  immutable Action identity, secret-safe validation, and no live mutation.
- **Reliability**: One registry, negative fixtures, compatibility mode, strict
  cutover only after migration, and deterministic failure output.
- **Scalability**: New document profiles and validation surfaces are data
  entries with fixtures rather than repeated shell conditionals and tables.
- **Observability**: Task evidence records command, tool version, lane,
  PASS/SKIP/FAIL/DEFER, limitation, reviewer, and rollback.
- **Operability**: Every tranche has an independent Spec, Plan, Task, logical
  commit range, and rollback point.

## System Overview & Context

The control flow is:

```text
approved PRD/ARD/ADR
  -> document profile registry + schema
  -> Stage 99 support contracts and template forms
  -> authored documents and README profiles
  -> semantic document validator + fixture corpus
  -> affected-surface registry
  -> local hooks / AI-agent obligations / CI selectors
  -> repository-static protected-surface gates
```

Human-readable documents explain intent and exceptions. Machine-readable
registries own exact values, paths, status domains, required and allowed
sections, and validator selection. Generated or mirrored views are checked
against their source rather than becoming new owners.

| Responsibility | Canonical tranche owner | Consumer/handoff boundary |
| --- | --- | --- |
| Document registry/schema | Spec 026 | All later tranches consume it. |
| Stage 99 non-README support/forms and direct Stage 00 template mirrors | Spec 027 | Spec 030 may repair links but does not redefine them. |
| README forms, all README bodies, `_workspace` boundary | Spec 028 | Spec 030 may make relocation-driven index/link changes only. |
| Parser, semantic validator, validation fixtures | Spec 029 | Later tranches add cases through the declared fixture interface. |
| Remaining authored non-README content and cloud relocation | Spec 030 | Provider and protected machine surfaces are excluded. |
| Affected-surface registry, selector blocks, Agent/provider QA semantics | Spec 031 | Workflow identity/permissions and domain behavior pass to Spec 032. |
| Action identity/permissions and GitOps/infrastructure/security behavior | Spec 032 | It preserves Spec 031 selector semantics and records static-only evidence. |

## Data Architecture

- **Key Entities / Flows**: `DocumentProfile`, `Route`, `FrontmatterSchema`,
  `SectionProfile`, `ReadmeProfile`, `ValidationSurface`, `EvidenceResult`, and
  `MigrationDisposition`.
- **Storage Strategy**: Versioned JSON contracts live beside their canonical
  governance domain; Markdown support explains rationale and links to them;
  fixture directories hold positive and negative samples.
- **Data Boundaries**: Frontmatter is parsed as one YAML mapping before the body
  is parsed as Markdown. Fenced code is excluded from structural heading checks.
  Provider-native metadata and GitHub-native control Markdown are explicit
  non-SDLC profiles.

## Infrastructure & Deployment

- **Runtime / Platform**: Repository-local scripts, pre-commit, GitHub Actions,
  GitOps manifests, policy checks, and provider adapters.
- **Deployment Model**: Changes are committed in an isolated worktree and only
  affect live systems after a separately approved Git-based operator workflow.
- **Operational Evidence**: Static rendering, manifest checks, secret scanning,
  policy fallback, selector fixtures, and full-SHA Action checks. Live evidence
  remains explicitly unverified.

## AI Agent Architecture Requirements (If Applicable)

- **Model/Provider Strategy**: Capability tiers are canonical; provider notes
  map Claude, Codex, and Gemini to available native models without duplicating
  model names in every role.
- **Tooling Boundary**: Agents may use repository and read-only research tools;
  remote mutation and secret access require separate authority.
- **Memory & Context Strategy**: Durable decisions live in PRD/ARD/ADR/Spec and
  Task evidence; `_workspace` stores only ignored, temporary, non-secret support
  artifacts.
- **Guardrail Boundary**: Shared roles define responsibility, output, prohibited
  action, stop, and handoff semantics; native adapters preserve provider syntax.
- **Latency / Cost Budget**: Affected-file checks are narrow; all-files and broad
  reviewers run at defined completion gates rather than after every edit.

## Related Documents

- **PRD**: [Workspace Document Assurance Modernization](../../01.requirements/005-workspace-document-assurance-modernization.md)
- **ADRs**: [Declarative Document Contract Registry](../decisions/0015-declarative-document-contract-registry.md) and [Program-to-Tranche Lineage](../decisions/0016-program-to-tranche-document-lineage.md)
- **Specs**: [Document Contract Registry](../../03.specs/026-document-contract-registry/spec.md) through [Protected Surface and Supply Chain Hardening](../../03.specs/032-protected-surface-supply-chain-hardening/spec.md)
- **Current Audit Roadmap**: [Integrated Remediation Roadmap](../../90.references/audits/2026-07-11-weia/remediation-roadmap.md)
