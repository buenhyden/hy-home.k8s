---
title: 'Document Type Format and Evidence Contract Reference'
type: content/reference
status: active
owner: platform
updated: 2026-07-12
---

# Document Type Format and Evidence Contract Reference

## Overview

This source ledger records why each workspace document family adopts selected
format and evidence concepts. It compares the repository forms with formal
standards, normative technical specifications, government guidance, documented
methods, and official product guidance observed on `2026-07-12`.

## Purpose

Template maintainers use this ledger before changing a form. It preserves the
source authority, the local decision, and the freshness boundary without making
external guidance the owner of repository routes, Frontmatter, or lifecycle.

## Reference Type

- Type: source-ledger
- Source checked: 2026-07-12
- Refresh trigger: A cited revision, official provider contract, template
  family, or canonical local document-profile contract changes.

## Authority Boundary

- **Authoritative for**:
  - The sources reviewed for the ten template families and the local
    adopted/rejected decisions recorded below.
  - The observation and refresh boundary for those decisions.
- **Not authoritative for**:
  - Route, Frontmatter, lifecycle, or required-section schema. Those machine
    facts belong to the Stage 99 document-profile registry and its schema.
  - Active requirements, architecture decisions, implementation contracts,
    execution plans, policies, runbooks, provider availability, or live state.

ISO/IEC/IEEE standards cited here are paid standards. This ledger identifies
their public catalog records and high-level comparison concerns but does not
reproduce standard text. Diátaxis, Spec Kit, Michael Nygard's ADR format, and
Google SRE postmortem guidance are documented practices or methods, not formal
standards. Repository Frontmatter fields and section profiles are local
extensions, not requirements imposed by any cited source.

## Scope

- Covers the ten families required by the Template Contract Consolidation Spec.
- Covers format, evidence, authority, and freshness decisions for template
  maintenance.
- Excludes verbatim paid-standard content, topic-level authored-document
  research, provider runtime verification, and live operational claims.

## Definitions / Facts

- **Formal standard**: A published consensus standard identified by its issuing
  standards body and revision.
- **Normative technical specification**: A syntax or interoperability contract
  published by the technology's governing project.
- **Government guidance/framework**: Public risk or secure-development guidance
  issued by NIST.
- **Documented practice/method**: A reusable documentation or delivery approach
  that informs local design but is not represented as a universal standard.
- **Official living guidance**: Product or project documentation whose current
  contents may change without a new numbered edition.

## Decision Ledger

| Family | Source kind | Authority and link | Observed | Version/revision | Adopted guidance | Rejected guidance and reason | Local extension | Refresh trigger | Affected forms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRD | Formal consensus standard plus documented method | [ISO/IEC/IEEE 29148 catalog](https://www.iso.org/standard/72089.html); [Spec Kit](https://github.github.com/spec-kit/index.html) | 2026-07-12 | ISO/IEC/IEEE 29148:2018; Spec Kit living guidance observed 2026-07-12 | Separate problem, stakeholder need, scope, verifiable requirement, acceptance, and downstream traceability. | Reject copying paid-standard text and embedding architecture or task procedure in a PRD; copyright and stage ownership require local synthesis. | Five-key `sdlc/prd` Frontmatter, numbered Stage 01 route, repository requirement labels, and local status domain. | ISO revision or amendment; Spec Kit workflow change; PRD consumer or lifecycle contract change. | `docs/99.templates/templates/sdlc/requirements/prd.template.md` |
| ARD | Formal consensus standard | [ISO/IEC/IEEE 42010 catalog](https://www.iso.org/standard/74393.html) | 2026-07-12 | ISO/IEC/IEEE 42010:2022 | Identify stakeholders, concerns, boundaries, relevant viewpoints, quality attributes, and the distinction between architecture description and implementation. | Reject copying the standard's full conceptual model or requiring every possible viewpoint; the repository needs a proportional reference architecture, not a conformance claim. | Five-key `sdlc/ard` Frontmatter, Stage 02 requirement route, repository quality-attribute vocabulary, and PRD/Spec handoff links. | ISO revision or amendment; architecture profile, consumer, or lifecycle change. | `docs/99.templates/templates/sdlc/architecture/ard.template.md` |
| ADR | Documented practice | [Michael Nygard, Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) | 2026-07-12 | Published 2011; practice observed 2026-07-12 | Keep one decision with context, decision, status, and consequences; preserve history and record a superseding decision rather than rewriting it. | Reject deleting or renumbering superseded decisions and reject turning an ADR into a broad architecture description; both destroy decision history or duplicate ARD ownership. | Five-key `sdlc/adr` Frontmatter, global monotonic Stage 02 numbering, accepted-state semantics, alternatives, and reciprocal lineage links. | Material update to the cited practice; accepted local ADR lifecycle or numbering decision changes. | `docs/99.templates/templates/sdlc/architecture/adr.template.md` |
| Spec, Plan, Task, tests | Documented method plus government secure-development guidance | [Spec Kit](https://github.github.com/spec-kit/index.html); [NIST SP 800-218 SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) | 2026-07-12 | Spec Kit living guidance observed 2026-07-12; SSDF version 1.1 (2022) | Maintain Spec-to-Plan-to-Task-to-implementation flow, analyze cross-artifact consistency, define verification before implementation, and retain secure-development evidence. | Reject presenting Spec Kit as a formal standard or merging Spec, Plan, Task, and test evidence into one current owner; their reader jobs and lifecycle evidence differ. | Namespaced five-key Frontmatter, numbered Spec folders, dated Plan/Task records, repository validation commands, PASS/SKIP/FAIL/DEFER evidence, reviewer, and rollback fields. | Spec Kit method change; NIST SSDF revision; Stage 03/04 lifecycle, evidence, or QA contract change. | `docs/99.templates/templates/sdlc/specs/spec.template.md`; `docs/99.templates/templates/sdlc/execution/plan.template.md`; `docs/99.templates/templates/sdlc/execution/task.template.md`; `docs/99.templates/templates/sdlc/specs/tests.template.md` |
| API and native contracts | Normative technical specifications plus official language guidance | [OpenAPI Specification](https://spec.openapis.org/oas/latest.html); [GraphQL Specification](https://spec.graphql.org/); [Protocol Buffers proto3 guide](https://protobuf.dev/programming-guides/proto3/) | 2026-07-12 | Living specifications/guidance observed 2026-07-12 | Preserve native syntax, explicit consumer-facing operations and schemas, compatibility-relevant types, and machine validation in the native format. | Reject Markdown Frontmatter in native contracts and reject wrapping a native schema in prose as its canonical owner; either change would break native tooling or create two contracts. | Registry routes native files without Frontmatter; feature-local Markdown API/data-model documents explain rationale and link to, but do not replace, native contracts. | OpenAPI or GraphQL specification release; protobuf language-guide change; generator, validator, or API consumer change. | `docs/99.templates/templates/sdlc/specs/api-spec.template.md`; `docs/99.templates/templates/sdlc/specs/data-model.template.md`; `docs/99.templates/templates/sdlc/specs/openapi.template.yaml`; `docs/99.templates/templates/sdlc/specs/schema.template.graphql`; `docs/99.templates/templates/sdlc/specs/service.template.proto` |
| Agent design | Government risk framework plus official provider living guidance | [NIST AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework); [Claude Code subagents](https://code.claude.com/docs/en/sub-agents); [Codex subagents](https://developers.openai.com/codex/subagents); [Gemini CLI subagents](https://geminicli.com/docs/core/subagents/) | 2026-07-12 | AI RMF 1.0 (2023); provider living guidance observed 2026-07-12 | Define role, tools, permissions, prohibited actions, evaluation, stop and handoff behavior, fallback, and provider/runtime evidence boundaries. | Reject provider file-count parity, duplicated latest-model names in every role, and claims that a tracked adapter proves runtime discovery; these are not safety or availability evidence. | Shared semantic role contract plus provider-native adapter formats, capability tiers, repository sandbox/approval boundaries, and explicit repo-static versus runtime evidence. | NIST AI RMF revision; official Claude, Codex, or Gemini agent/tool/model contract change; local provider adapter or model-policy change. | `docs/99.templates/templates/sdlc/specs/agent-design.template.md` |
| Guide, Reference, README | Documented method plus official repository and platform style guidance | [Diátaxis](https://diataxis.fr/start-here/); [GitHub README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes); [Kubernetes documentation style guide](https://kubernetes.io/docs/contribute/style/style-guide/) | 2026-07-12 | Living guidance observed 2026-07-12 | Separate how-to, reference, and explanation reader jobs; keep README as an entrypoint; use direct, durable wording and route policy/schema detail to its owner. | Reject a universal seven-heading README and reject copying governance tables into entrypoints; path-specific reader jobs and single ownership require profile-specific forms. | Five-key Frontmatter for Guide/Reference, no README Frontmatter, six path-inferred README profiles, repository-relative links, and freshness labels for dated references. | Diátaxis method change; GitHub or Kubernetes guidance change; README profile, Stage 90 authority, or link-routing contract change. | `docs/99.templates/templates/sdlc/operations/guide.template.md`; `docs/99.templates/templates/common/reference.template.md`; `docs/99.templates/templates/common/readme.template.md` and its profile-specific successors |
| Policy and Runbook | Government secure-development guidance plus documented GitOps practice and official platform task guidance | [NIST SP 800-218 SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final); [OpenGitOps principles](https://opengitops.dev/); [Kubernetes task guidance](https://kubernetes.io/docs/contribute/style/page-content-types/#task) | 2026-07-12 | SSDF version 1.1 (2022); OpenGitOps and Kubernetes living guidance observed 2026-07-12 | Policy states normative controls, enforcement, exceptions, and ownership; Runbook states executable preflight, procedure, verification, rollback, and stop/escalation boundaries. | Reject combining policy and procedure into one document and reject treating repository desired state as proof of live reconciliation; both obscure authority and evidence depth. | Five-key `sdlc/policy` and `sdlc/runbook` Frontmatter, Stage 05 routes, GitOps-first local rules, approval boundary, and PASS/SKIP/FAIL/DEFER reporting. | NIST SSDF revision; OpenGitOps or Kubernetes task-guidance change; policy consumer, runbook command, or live-authority boundary change. | `docs/99.templates/templates/sdlc/operations/policy.template.md`; `docs/99.templates/templates/sdlc/operations/runbook.template.md` |
| Incident and Postmortem | Government incident-response guidance plus documented SRE practice | [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final); [Google SRE postmortem culture](https://sre.google/sre-book/postmortem-culture/) | 2026-07-12 | NIST SP 800-61 Rev. 3; Google SRE living book guidance observed 2026-07-12 | Incident owns detection, impact, factual timeline, response, recovery, and handoff; Postmortem owns blameless cause analysis, learning, measurable owned actions, and prevention. | Reject speculative root cause in the incident record, blame-oriented language, and fabricated live evidence; these corrupt factual chronology, learning, or evidence integrity. | Separate five-key `sdlc/incident` and `sdlc/postmortem` profiles, tabletop labeling, evidence lane, action owner, due-state, and documentation-feedback links. | NIST revision; Google SRE guidance change; incident tabletop finding; response, severity, or action-tracking contract change. | `docs/99.templates/templates/sdlc/operations/incident.template.md`; `docs/99.templates/templates/sdlc/operations/postmortem.template.md` |
| Archive, memory, progress | Documented preservation practice plus documented traceability method | [Michael Nygard, Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions); [Spec Kit](https://github.github.com/spec-kit/index.html) | 2026-07-12 | ADR practice published 2011; Spec Kit living guidance observed 2026-07-12 | Preserve historical decisions and evidence, distinguish current from superseded authority, keep replacement traceability, and record progress without presenting it as the final contract. | Reject silently rewriting historical bodies, resurrecting obsolete guidance as current, or using progress/memory as route or policy owner; those actions erase provenance or create authority conflicts. | Archive Tombstone traceability keys and fixed archived status; five-key governance memory/progress profiles; central archive index and canonical replacement links. | ADR or Spec Kit practice change; archive metadata, memory retention, progress evidence, or current-owner contract change. | `docs/99.templates/templates/common/archive-tombstone.template.md`; `docs/99.templates/templates/common/memory.template.md`; `docs/99.templates/templates/common/progress.template.md` |

## Sources

The authority links in the ledger are the reviewed source set. Formal standards
are referenced through their issuing bodies; technical syntax through the
governing specification; provider behavior through official provider guidance;
and documented practices through their primary publishers. No secondary blog
or market scan determines a template contract in this ledger.

## Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-07-12
- Next review trigger: Any trigger in a ledger row, addition or removal of a
  template family, or a changed registry consumer.
- Provider boundary: Claude, Codex, and Gemini documentation is living guidance.
  Any official model, tool, subagent, permission, or adapter-contract change
  requires refreshing the Agent design row before changing provider-facing
  forms. This ledger does not prove local availability or runtime resolution.

## Related Documents

- **Template consolidation Spec**: [Template Contract Consolidation](../../../03.specs/027-template-contract-consolidation/spec.md)
- **Current SDLC research**: [Spec, SDLC, CI, QA, and Formatting](./spec-sdlc-ci-qa-formatting.md)
- **Provider source ledger**: [Provider Implementation Status](./provider-implementation-status.md)
- **Template support index**: [Template Support](../../../99.templates/support/README.md)
- **Reference maintenance runbook**: [Reference Maintenance Runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
