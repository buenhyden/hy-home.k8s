---
title: "Workspace Document Assurance Modernization Requirement Package"
version: "1.0.0"
type: "sdlc/requirement"
status: "superseded"
owner: "platform"
updated: "2026-07-14"
layer: "requirements"
artifact_id: "REQ-0005"
superseded_by: "REQ-0008"
---

# Workspace Document Assurance Modernization Requirement Package

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

At program approval, the Current audit showed that structural consistency was
not semantic consistency. Canonical Stage 00 and Stage 99 contracts remained
`draft`, one README template mixed unrelated profiles, Task authoring guidance
was copied into authored records, duplicate AWS and Azure SDLC documents owned
overlapping scope, and CI selectors omitted paths consumed by repository
validators. The quality gate then passed these conditions because route,
profile, heading, and selector facts were duplicated in multiple owners. This
historical baseline is retained as the problem the completed program addressed,
not as a description of the current repository contract.

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
- **STORY-05**: AWS and Azure reference implementations and their local guidance
  are owned together under `examples/**`; Stage 90 does not duplicate them as
  snapshots.
- **STORY-06**: Protected workflow and GitOps changes receive static security
  checks without reading secrets or mutating live systems.

## Functional Requirements

- **REQ-0005-FR-0001**: Define one machine-readable registry for document routes,
  types, frontmatter keys, status domains, section profiles, and explicit
  exceptions.
- **REQ-0005-FR-0002**: Align Stage 99 support contracts and templates with the
  registry and remove legacy or duplicate forms.
- **REQ-0005-FR-0003**: Define repository, stage, collection, implementation,
  audit-pack, data-pack, research-pack, and workspace-staging README profiles.
- **REQ-0005-FR-0004**: Validate YAML frontmatter as a repository convention,
  parse Markdown with fenced-code awareness, and maintain positive and negative
  fixtures.
- **REQ-0005-FR-0005**: Migrate authored documents in bounded waves, preserving
  completed Task evidence, the latest external research, ADR history, and
  Git-recoverable historical evidence.
- **REQ-0005-FR-0006**: Keep example-local cloud guidance with its executable
  provider implementation under `examples/**` and repair every index and
  cross-link without creating Stage 90 snapshot copies.
- **REQ-0005-FR-0007**: Create one affected-surface contract consumed by local
  hooks, AI-agent guidance, repository validation, and CI job selection.
- **REQ-0005-FR-0008**: Pin third-party GitHub Actions to full commit SHAs and
  harden repository-static Vault, ESO, GitOps, and policy validation without
  claiming live readiness.
- **REQ-0005-FR-0009**: Keep provider-native agent metadata distinct from SDLC
  frontmatter while enforcing shared role semantics and model-policy routing.
- **REQ-0005-FR-0010**: Use logical commits, independent review, explicit
  rollback points, and no remote publication without approval.
- **REQ-0005-NFR-0001**: For every document type, record the applicable official or
  primary format/governance sources, observation date, version boundary,
  adopted and rejected guidance, and refresh trigger before changing its form.
- **REQ-0005-NFR-0002**: For every migrated current authored document, record a
  topic/title research decision that joins repository evidence with applicable
  official external sources; purely repository-specific claims must state why
  external technical validation is not applicable rather than omitting review.

## Success / Acceptance Criteria

- **Acceptance criterion 01**: The 433-file approved target Markdown corpus at baseline
  SHA `8e1b00b4dfb84b8431ba4d3d31b4ad0445a0019d`, plus every program-created
  target Markdown file, matches exactly one profile or explicit native/control
  exception; ambiguous and uncovered routes are zero.
- **Acceptance criterion 02**: Every README matches exactly one README profile; duplicate
  structural headings outside fenced code are zero.
- **Acceptance criterion 03**: Invalid frontmatter keys, values, dates, type-specific
  states, placeholders, and authored template residue are rejected by fixtures.
- **Acceptance criterion 04**: Duplicate current owners for the same role, scope, and
  lineage are zero, including the current AWS and Azure overlap.
- **Acceptance criterion 05**: Internal broken links and stale references to deleted
  templates or example-local SDLC paths are zero.
- **Acceptance criterion 06**: Every changed protected path selects its required local
  and CI validators in positive and negative selector fixtures.
- **Acceptance criterion 07**: Every third-party GitHub Action uses a full commit SHA;
  disabled unpinned-action checks are zero.
- **Acceptance criterion 08**: Repository-static quality, manifest, secret-handling,
  policy, shell-syntax, diff, and all-files gates pass with PASS, SKIP, FAIL,
  and DEFER reported accurately.
- **Acceptance criterion 09**: A type-to-source matrix covers every template family and
  every migrated current authored document has a reviewed research-ledger row
  with applicability and content-change disposition.

Repository-static completion is recorded by `status: done` on Specs 026–032
and each linked canonical Plan and Task. Together they deliver the registry,
template and README profiles, semantic validation, authored-corpus migration,
affected-surface QA, and protected-surface hardening required by this PRD. The
evidence is limited to tracked repository state and local static checks; it
does not claim remote publication, live-system readiness, secret validation,
or external environment verification.

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

- **AD**: [Workspace Document Assurance Operating Model](../02.architecture/descriptions/0008-workspace-document-assurance-operating-model.md)
- **ADRs**: [Declarative Document Contract Registry](../02.architecture/decisions/0015-declarative-document-contract-registry.md) and [Program-to-Tranche Lineage](../02.architecture/decisions/0016-program-to-tranche-document-lineage.md)
- **Specs**: [Document Contract Registry](../98.archive/completed/03.specs/0026-document-contract-registry/spec.md) through [Protected Surface and Supply Chain Hardening](../98.archive/completed/03.specs/0032-protected-surface-supply-chain-hardening/spec.md)
- **Current External Research**: [Workspace Engineering Research Pack](../90.references/research/0001-workspace-engineering/README.md)
