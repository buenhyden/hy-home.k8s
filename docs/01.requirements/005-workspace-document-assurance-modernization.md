---
title: 'Workspace Document Assurance Modernization Product Requirements'
type: sdlc/prd
status: active
owner: platform
updated: 2026-07-13
---

# Workspace Document Assurance Modernization Product Requirements

## Overview

This program makes document type, ownership, lifecycle, template, validation,
and delivery rules internally consistent across the repository. It replaces
duplicated contract tables and generic README rules with profile-specific,
machine-verifiable contracts while preserving historical execution evidence
and provider-native formats.

## Vision

Repository contributors and AI agents can determine one authoritative document
form, one current owner, and one complete validation path for every tracked
surface without copying governance prose or inferring rules from scattered
scripts.

## Problem Statement

The Current audit shows that structural consistency is not semantic
consistency. Canonical Stage 00 and Stage 99 contracts remain `draft`, one
README template mixes unrelated profiles, Task authoring guidance is copied
into authored records, duplicate AWS and Azure SDLC documents own overlapping
scope, and CI selectors omit paths consumed by repository validators. The
existing quality gate passes these conditions because route, profile, heading,
and selector facts are duplicated in multiple owners.

## Personas

- **Repository contributor**: needs one form and one verification route for a
  change.
- **Platform operator**: needs protected-surface changes to remain reviewable,
  reversible, and separate from live mutation.
- **Documentation maintainer**: needs profile-specific templates without
  boilerplate residue.
- **AI agent and reviewer**: need deterministic scope, stop rules, evidence,
  and handoff obligations.

## Key Use Cases

- **STORY-01**: An author selects exactly one document profile from the target
  path and creates topic-specific content without copying support rules.
- **STORY-02**: A validator rejects unsupported metadata, lifecycle states,
  placeholders, duplicate headings, and duplicate current ownership.
- **STORY-03**: A README uses a path-specific profile and routes durable rules
  to their canonical contract owner.
- **STORY-04**: A repository change selects all required local and CI validators
  from one affected-surface contract.
- **STORY-05**: AWS and Azure reference knowledge has one dated snapshot owner
  under `docs/90.references`, while `examples/**` contains executable assets.
- **STORY-06**: Protected workflow and GitOps changes receive static security
  checks without reading secrets or mutating live systems.

## Functional Requirements

- **REQ-PRD-FUN-01**: Define one machine-readable registry for document routes,
  types, frontmatter keys, status domains, section profiles, and explicit
  exceptions.
- **REQ-PRD-FUN-02**: Align Stage 99 support contracts and templates with the
  registry and remove legacy or duplicate forms.
- **REQ-PRD-FUN-03**: Define repository, stage, collection, implementation,
  snapshot-pack, and workspace-staging README profiles.
- **REQ-PRD-FUN-04**: Validate YAML frontmatter as a repository convention,
  parse Markdown with fenced-code awareness, and maintain positive and negative
  fixtures.
- **REQ-PRD-FUN-05**: Migrate authored documents in bounded waves, preserving
  completed Plans, Tasks, audits, research snapshots, ADR history, and archive
  evidence.
- **REQ-PRD-FUN-06**: Consolidate example-local cloud SDLC documents into
  provider snapshots under `docs/90.references` and repair every index and
  cross-link.
- **REQ-PRD-FUN-07**: Create one affected-surface contract consumed by local
  hooks, AI-agent guidance, repository validation, and CI job selection.
- **REQ-PRD-FUN-08**: Pin third-party GitHub Actions to full commit SHAs and
  harden repository-static Vault, ESO, GitOps, and policy validation without
  claiming live readiness.
- **REQ-PRD-FUN-09**: Keep provider-native agent metadata distinct from SDLC
  frontmatter while enforcing shared role semantics and model-policy routing.
- **REQ-PRD-FUN-10**: Use logical commits, independent review, explicit
  rollback points, and no remote publication without approval.
- **REQ-PRD-FUN-11**: For every document type, record the applicable official or
  primary format/governance sources, observation date, version boundary,
  adopted and rejected guidance, and refresh trigger before changing its form.
- **REQ-PRD-FUN-12**: For every migrated current authored document, record a
  topic/title research decision that joins repository evidence with applicable
  official external sources; purely repository-specific claims must state why
  external technical validation is not applicable rather than omitting review.

## Success / Acceptance Criteria

- **REQ-PRD-MET-01**: The 433-file approved target Markdown corpus at baseline
  SHA `8e1b00b4dfb84b8431ba4d3d31b4ad0445a0019d`, plus every program-created
  target Markdown file, matches exactly one profile or explicit native/control
  exception; ambiguous and uncovered routes are zero.
- **REQ-PRD-MET-02**: Every README matches exactly one README profile; duplicate
  structural headings outside fenced code are zero.
- **REQ-PRD-MET-03**: Invalid frontmatter keys, values, dates, type-specific
  states, placeholders, and authored template residue are rejected by fixtures.
- **REQ-PRD-MET-04**: Duplicate current owners for the same role, scope, and
  lineage are zero, including the current AWS and Azure overlap.
- **REQ-PRD-MET-05**: Internal broken links and stale references to deleted
  templates or example-local SDLC paths are zero.
- **REQ-PRD-MET-06**: Every changed protected path selects its required local
  and CI validators in positive and negative selector fixtures.
- **REQ-PRD-MET-07**: Every third-party GitHub Action uses a full commit SHA;
  disabled unpinned-action checks are zero.
- **REQ-PRD-MET-08**: Repository-static quality, manifest, secret-handling,
  policy, shell-syntax, diff, and all-files gates pass with PASS, SKIP, FAIL,
  and DEFER reported accurately.
- **REQ-PRD-MET-09**: A type-to-source matrix covers every template family and
  every migrated current authored document has a reviewed research-ledger row
  with applicability and content-change disposition.

## Scope and Non-goals

- **In Scope**: The 433 baseline Markdown files and other tracked files under
  the roots named in the approved request;
  Stage 00/99 governance and contracts; templates; authored document migration;
  CI, hooks, validators, agent adapters, GitOps, infrastructure, policy, tests,
  and repository-static security configuration.
- **Out of Scope**: Secret values, ignored authentication state, personal logs,
  shell history, local certificates, remote branch-rule mutation, pushes, pull
  requests, and live cluster, Vault, Argo CD, ESO, or provider mutation.
- **Non-goals**: Unrequested Markdown outside the approved target corpus,
  including `RTK.md` and `graphify-out/**`; a root `DESIGN.md`; universal
  consumer-free frontmatter keys;
  provider file-count parity; SLSA or OpenSSF compliance claims; a new Release
  document family without a separate consumer decision.

## Risks, Dependencies, and Assumptions

- The profile registry must land before templates, documents, and selectors can
  safely migrate.
- Compatibility validation must remain available until the authored population
  is migrated; strict enforcement cannot precede its corpus.
- Destructive consolidation can erase unique knowledge unless inventories,
  source comparisons, link graphs, and rollback commits are captured first.
- Optional tools may be unavailable locally; fallback validation and tool SKIP
  must remain separate evidence.
- Provider and cloud facts can change, so dated external-source boundaries and
  refresh triggers are required.

### Agent execution and approval requirements

- **Allowed Actions**: Read tracked repository state, research official sources,
  edit approved tracked surfaces in the isolated worktree, run static validation,
  and create logical commits.
- **Disallowed Actions**: Read secret values, mutate live systems, publish
  remotely, treat SKIP as PASS, or delete ignored local state.
- **Human-in-the-loop Requirement**: Resolve plan contradictions, approve any
  expansion beyond the seven tranches, and choose the final integration option.
- **Evaluation Expectation**: Fresh implementer and independent reviewer per
  task, followed by one whole-branch review and merged-result verification.

## Traceability

- **ARD**: [Workspace Document Assurance Operating Model](../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- **ADRs**: [Declarative Document Contract Registry](../02.architecture/decisions/0015-declarative-document-contract-registry.md) and [Program-to-Tranche Lineage](../02.architecture/decisions/0016-program-to-tranche-document-lineage.md)
- **Specs**: [Document Contract Registry](../03.specs/026-document-contract-registry/spec.md) through [Protected Surface and Supply Chain Hardening](../03.specs/032-protected-surface-supply-chain-hardening/spec.md)
- **Current Audit**: [2026-07-11 Workspace Engineering Implementation Audit](../90.references/audits/2026-07-11-weia/README.md)
