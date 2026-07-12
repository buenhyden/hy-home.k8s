---
title: 'Template Contract Consolidation Technical Specification'
type: sdlc/spec
status: active
owner: platform
updated: 2026-07-12
---

# Template Contract Consolidation Technical Specification (Spec)

## Overview

This Spec aligns Stage 99 support contracts and template forms with the document
profile registry. It removes duplicate route and lifecycle ownership, deletes
legacy forms, and separates authoring guidance from authored section content.

## Strategic Boundaries & Non-goals

This tranche changes Stage 99 support and non-README template forms plus direct
Stage 00 mirrors. It may update only inventory and target-link rows in
`docs/99.templates/README.md` and `docs/99.templates/templates/README.md` when a
form is added, renamed, or deleted; Spec 028 owns their profile layout and all
other README body design. Authored population migration is owned by Spec 030.
This tranche does not rewrite historical Plans, Tasks, audits, research packs,
or archive Tombstones.

## Related Inputs

- **PRD**: [Workspace Document Assurance Modernization](../../01.requirements/005-workspace-document-assurance-modernization.md)
- **ARD**: [Workspace Document Assurance Operating Model](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- **Lineage ADR**: [Program-to-Tranche Document Lineage](../../02.architecture/decisions/0016-program-to-tranche-document-lineage.md)
- **Registry Spec**: [Document Contract Registry](../026-document-contract-registry/spec.md)
- **Current Contracts**: [Template Documentation Contract](../../99.templates/support/documentation-contract.md) and [SDLC Template Governance](../../99.templates/support/sdlc-governance.md)

## Contracts

- **Config Contract**: Each structural route has one template form and one
  registry profile. Native OpenAPI, GraphQL, and protobuf forms stay native.
- **Data / Interface Contract**: Template headings are required or allowed by the
  registry. Author instructions use comments or support prose and are not
  authored H2 sections.
- **Governance Contract**: Support documents explain responsibility boundaries;
  they link to machine contracts instead of reproducing their complete tables.
  A durable type-to-source matrix is maintained in the Current research pack at
  `docs/90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md`.

## Core Design

- **Component Boundary**: Six support contracts, non-README Markdown and native
  forms, Stage 99 README inventory/link rows only, direct Stage 00 lifecycle
  summaries, and legacy references.
- **Key Dependencies**: Spec 026 registry and inventory; current validator
  compatibility mode; cross-link search.
- **Tech Stack**: Markdown forms, HTML authoring comments, JSON registry, and
  repository-static validation.

Normalization rules:

- Remove `harness-task-contract.template.md` after merging its unique protected-
  surface and approval concepts into the standard Task profile.
- Remove authored headings such as `Suggested Types` and `Working Rules`; keep
  vocabulary and selection guidance in support contracts.
- Consolidate `Related Inputs`, `Parent Documents`, `Parent Spec`, and
  `Canonical References` into one type-appropriate `Traceability` owner.
- Use one opening intent section; remove `Overview` plus `Purpose` or `Summary`
  pairs that repeat the same responsibility.
- Keep Incident factual chronology separate from Postmortem cause, learning,
  and prevention.
- Keep Guide human-oriented guidance separate from Runbook executable operator
  procedure and Reference durable lookup facts.

The type-to-source matrix must cover every template family before its form is
changed. Each row records source authority, observed date, version or revision,
applicable guidance, rejected guidance with reason, local extension, and refresh
trigger. The initial minimum basis is:

| Document family | Primary external basis | Required comparison |
| --- | --- | --- |
| PRD | [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) and [Spec Kit](https://github.github.com/spec-kit/index.html) | Requirement quality, acceptance, scope, and downstream traceability; do not copy a paid standard's text. |
| ARD | [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) | Stakeholders, concerns, viewpoints, boundaries, and architecture-description versus implementation distinction. |
| ADR | [Michael Nygard's ADR practice](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) | One decision, context, decision, status, consequences, monotonic numbering, and preservation when superseded. |
| Spec, Plan, Task, tests | [Spec Kit](https://github.github.com/spec-kit/index.html) and [NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) | Spec-to-plan-to-task-to-implementation flow, cross-artifact analysis, secure-development verification; treat Spec Kit as a method, not a standard. |
| API and native contracts | [OpenAPI Specification](https://spec.openapis.org/oas/latest.html), [GraphQL Specification](https://spec.graphql.org/), and [Protocol Buffers](https://protobuf.dev/programming-guides/proto3/) | Native syntax and consumer contract; keep formats outside Markdown frontmatter. |
| Agent design | [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) plus official Claude, OpenAI, and Gemini documentation | Role, tools, permissions, safety, evaluation, stop/handoff, and provider-version boundary; no file-count parity. |
| Guide, Reference, README | [Diátaxis](https://diataxis.fr/start-here/), [GitHub README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes), and [Kubernetes documentation style](https://kubernetes.io/docs/contribute/style/style-guide/) | Reader job, how-to/reference/explanation separation, entrypoint versus contract owner, and freshness-sensitive wording. |
| Policy and Runbook | [NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final), [OpenGitOps](https://opengitops.dev/), and Kubernetes task guidance | Normative requirement, exception/enforcement owner, executable preflight/verify/rollback/stop boundary. |
| Incident and Postmortem | [NIST SP 800-61 Rev.3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) and [Google SRE postmortem practice](https://sre.google/sre-book/postmortem-culture/) | Detect/respond/recover facts versus blameless cause, learning, owned action, and measurable completion. |
| Archive, memory, progress | ADR preservation practice and Spec Kit traceability | Historical/current authority separation, append-only evidence, replacement link, and no resurrection of obsolete guidance. |

Diátaxis, Spec Kit, Nygard ADR, and Google SRE are documented practices rather
than universal format standards. The research matrix must label that status and
must not present repository extensions as externally mandated fields.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Template forms contain only required sections,
  conditional section comments, and minimal placeholders. Support contracts own
  reusable authoring and lifecycle rules.
- **Migration / Transition Plan**: Change support and forms in one compatibility
  wave, update registry/template fixtures, remove legacy references, and defer
  authored body cleanup to Spec 030.

## Interfaces & Data Structures

### Core Interfaces

```text
registry profile -> one template path
template path -> required/allowed headings
support contract -> rationale and authoring rules
authored document -> topic-specific content only
```

## Edge Cases & Error Handling

- Do not remove a duplicate-looking section until its unique content has an
  owning replacement section.
- Do not treat headings inside fenced examples as template structure.
- Do not turn native contracts into Markdown or add frontmatter to them.
- Do not silently alter accepted ADR history or completed execution evidence.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: A legacy template has a unique required behavior with no
  destination in the canonical form.
- **Fallback**: Add the behavior to the appropriate support rule or conditional
  canonical section before deleting the legacy file.
- **Human Escalation**: A genuinely distinct document role requires a separate
  profile decision rather than a second form with the same `type`.

## Verification Commands

```bash
python3 scripts/validate-document-contract-registry.py --root . --mode compatibility
bash scripts/validate-repo-quality-gates.sh .
rg -n "harness-task-contract|Suggested Types|SNIPPET LIBRARY" docs scripts .agents .claude .codex
git diff --check
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: Every routed document type has exactly one structural form.
- **VAL-SPC-002**: Legacy Task template and active references to it are zero.
- **VAL-SPC-003**: Support, Stage 00, README, and validator copies of full route
  and lifecycle tables are replaced by owner links or machine consumption.
- **VAL-SPC-004**: Template forms contain no authored guidance headings and all
  required/conditional section decisions have fixtures.
- **VAL-SPC-005**: Every template family has a reviewed type-to-source row with
  observation/version/applicability/rejection/refresh fields, and no form change
  is accepted without linking its row and local decision.

## Related Documents

- **Registry Spec**: [Document Contract Registry](../026-document-contract-registry/spec.md)
- **Plan**: [Template Contract Consolidation Implementation Plan](../../04.execution/plans/2026-07-12-template-contract-consolidation.md)
- **Task**: [Template Contract Consolidation Task](../../04.execution/tasks/2026-07-12-template-contract-consolidation.md)
- **Next Spec**: [README and Workspace Profiles](../028-readme-workspace-profiles/spec.md)
- **Template Support**: [Template Support Index](../../99.templates/support/README.md)
- **Documentation Method**: [Diátaxis](https://diataxis.fr/start-here/)
