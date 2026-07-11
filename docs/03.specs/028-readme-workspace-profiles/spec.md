---
title: 'README and Workspace Profiles Technical Specification'
type: sdlc/spec
status: active
owner: platform
updated: 2026-07-12
---

# README and Workspace Profiles Technical Specification (Spec)

## Overview

This Spec replaces the monolithic README snippet library and universal
seven-heading rule with path-specific README profiles. It preserves `_workspace`
as temporary, ignored, non-secret repository-support staging and keeps local
diagnostics and authentication state outside that boundary.

## Strategic Boundaries & Non-goals

This tranche owns README forms, README route classification, README body
migration, and the tracked `_workspace/README.md` contract. It does not add
frontmatter to README files, convert GitHub-native control Markdown into README,
or move durable SDLC evidence into `_workspace`.

## Related Inputs

- **PRD**: [Workspace Document Assurance Modernization](../../01.requirements/005-workspace-document-assurance-modernization.md)
- **ARD**: [Workspace Document Assurance Operating Model](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- **Lineage ADR**: [Program-to-Tranche Document Lineage](../../02.architecture/decisions/0016-program-to-tranche-document-lineage.md)
- **Registry Spec**: [Document Contract Registry](../026-document-contract-registry/spec.md)
- **Template Spec**: [Template Contract Consolidation](../027-template-contract-consolidation/spec.md)
- **Current Workspace Contract**: [Workspace Support Staging](../../../_workspace/README.md)

## Contracts

- **Config Contract**: Every tracked README resolves by path to exactly one of
  six profiles: repository, stage-index, collection-index, implementation,
  snapshot-pack, or workspace-staging.
- **Data / Interface Contract**: A profile declares one H1, required and allowed
  H2 headings, inventory expectations, and canonical-owner link boundaries.
- **Governance Contract**: README files are entrypoints and inventories. They
  may summarize but must not own lifecycle, schema, policy, or validation rules.

## Core Design

- **Component Boundary**: README profile registry entries, six minimal template
  forms, the 67 tracked README files, and README-specific fixtures.
- **Key Dependencies**: Specs 026 and 027, path inventory, Markdown fence-aware
  parsing, and link validation.
- **Tech Stack**: Frontmatter-free Markdown, registry-driven routing, and
  repository-local structural checks.

Profile responsibilities:

- `repository`: purpose, repository map, supported entrypoints, setup, and QA.
- `stage-index`: stage role, accepted artifact classes, lifecycle owner links,
  and contained-document index.
- `collection-index`: collection scope, item inventory, and add/find workflow.
- `implementation`: component purpose, structure, configuration boundary,
  validation, and operations entrypoints.
- `snapshot-pack`: observation date/SHA, authority boundary, report index,
  refresh trigger, and successor.
- `workspace-staging`: permitted temporary non-secret artifacts, forbidden local
  state, promotion destinations, cleanup, and tracking rules.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: README profile is inferred from path; no hidden
  body marker or frontmatter key is added. Required and allowed headings live in
  the registry and profile template.
- **Migration / Transition Plan**: Classify all README paths, replace the legacy
  monolithic form with six forms, migrate one profile at a time, and delete the
  old snippet library after all links and fixtures are updated.

## Interfaces & Data Structures

### Core Interfaces

```text
README path -> one profile -> one template -> allowed sections
README body -> canonical owner links + path-specific inventory
```

## Edge Cases & Error Handling

- Ignore H1/H2-looking lines inside fenced code when checking duplicates.
- Reject repeated structural headings such as the current duplicate `Overview`
  in the LLM Wiki README.
- Allow profile-specific optional sections only when declared; do not permit an
  unbounded catch-all section list.
- Preserve provider-native and GitHub-native control files as explicit
  frontmatter-free exceptions rather than forcing a README profile.
- Never enumerate, read, move, or delete ignored `.env`, token, key, certificate,
  kubeconfig, shell history, local setting, or diagnostic content.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: A README appears to serve two profiles.
- **Fallback**: Retain one entrypoint responsibility and route the other concern
  to its canonical child or support document.
- **Human Escalation**: A new profile is justified only when multiple paths share
  a distinct reader job that cannot be represented by an existing profile.

## Verification Commands

```bash
python3 scripts/validate-document-contract-registry.py --root . --mode compatibility
python3 scripts/validate-markdown-profiles.py --self-test
python3 scripts/validate-markdown-profiles.py --root . --profile readme
bash scripts/validate-repo-quality-gates.sh .
git diff --check
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: All 67 baseline README dispositions are accounted for, and
  every final tracked README after cloud relocation resolves to exactly one
  profile; the baseline and final counts are reported separately.
- **VAL-SPC-002**: README frontmatter, duplicate structural headings, legacy
  snippet markers, and unsupported sections are zero.
- **VAL-SPC-003**: Full governance and route tables are absent from README files;
  links resolve to their canonical owners.
- **VAL-SPC-004**: `_workspace` continues to track only its README, ignore scratch
  children, forbid secret/local diagnostic state, and define durable promotion.

## Related Documents

- **Template Spec**: [Template Contract Consolidation](../027-template-contract-consolidation/spec.md)
- **Next Spec**: [Semantic Document Validation](../029-semantic-document-validation/spec.md)
- **Workspace Contract**: [Workspace Support Staging](../../../_workspace/README.md)
- **Markdown Basis**: [CommonMark fenced code blocks](https://spec.commonmark.org/0.31.2/#fenced-code-blocks)
