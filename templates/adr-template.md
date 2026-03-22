# Architecture Decision Record (ADR)

> Use this template for `docs/adr/NNNN-<short-title>.md`.
>
> Repository-derived contract:
>
> - Use exactly one meaningful H1.
> - Use relative links only.
> - Remove every placeholder before saving.
> - Keep the document decision-focused. Do not turn ADRs into implementation specs.
> - Allowed ADR status values: `Accepted | Superseded | Deprecated`.
> - Allowed scope values where your doc set uses them: `master | domain | historical`.
> - Allowed layer values: `meta | infra | gitops | app | ops`
> - Keep all structural and narrative content in English.
> - Add exactly one `Overview (KR)` summary near the top. That overview summary alone should be written in Korean.
>
> Shape guidance:
>
> - Use the extended shape for `content/` and `vault/` domain decisions or any decision that needs alternatives, trade-offs, and traceability detail.
> - Use the compact shape for lightweight governance or documentation-boundary ADRs such as the `docs/` V2 active chain.

## Optional Frontmatter

```yaml
---
title: 'ADR NNNN: [Short Decision Title]'
status: 'Accepted'
date: 'YYYY-MM-DD'
authors: ['buenhyden']
deciders: ['buenhyden']
tags: ['adr', '<topic>']
layer: 'app' # meta | infra | gitops | app | ops
---
```

Use frontmatter when the surrounding doc set already uses it. Skip it when the active document family is intentionally compact.

## H1 and Metadata

# ADR NNNN: [Short Decision Title]

- **Status:** [Accepted | Superseded | Deprecated]
- **Date:** YYYY-MM-DD
- **Scope:** [master | domain | historical]
- **layer:** [meta | infra | gitops | app | ops]
- **Authors:** [Optional]
- **Deciders:** [Optional]

**Overview (KR):** [Write a 1-2 sentence Korean summary of the decision intent, why it matters now, and what boundary it affects.]

## Required Core Sections

### Compact Form

Use this when the ADR is primarily establishing a boundary, naming a policy, or fixing document authority.

## Context

[Explain the context, the current conflict or limitation, and why a formal decision is needed now.]

### Assumptions

- [Assumption 1: e.g., We assume the traffic will remain under 10k RPS.]
- [Assumption 2: e.g., We assume the current infrastructure supports IPv6.]

### Explicit Non-goals

- [Non-goal 1: e.g., This decision does not cover the billing migration.]
- [Non-goal 2: e.g., We are not replacing the primary SQL database yet.]

## Decision

- [Decision point 1]
- [Decision point 2]
- [Decision point 3]

## Consequences

- [Positive consequence 1]
- [Trade-off or limitation 1]

## Success Criteria

- [Metric/Result 1: e.g., Build time reduced by 20%.]
- [Metric/Result 2: e.g., Zero reported P0 security incidents related to this flow.]

## Risks and Mitigations

- **[Risk 1]**: [Impact description] -> **Mitigation**: [How to prevent/fix]

## Open Questions

- [Unresolved item 1: e.g., Final selection of the logging sidecar is pending.]

## Related

- `[../specs/YYYY-MM-DD-feature.md]`
- `[../ard/system-or-domain-ard.md]`
- `[../prd/feature-or-system-prd.md]`
- `[./NNNN-related-decision.md]`

## Optional Extended Sections

Use these sections when the decision has substantial alternatives, engineering trade-offs, or explicit requirement traceability.

## 1. Context and Problem Statement

[Expanded version of the context if the compact form is not sufficient.]

## 2. Decision Drivers

- **[Driver 1]**: [Concrete driver]
- **[Driver 2]**: [Concrete driver]
- **[Driver 3]**: [Concrete driver]

## 3. Decision Outcome

**Chosen option: "[Selected Option]"**, because [clear justification].

### 3.1 Core Engineering Pillars Alignment

- **Security**: [How this decision reduces risk or prevents misuse]
- **Observability**: [How this decision improves traceability, incident handling, or evidence]
- **Compliance**: [How this decision aligns with repo rules, policy, or standards]
- **Performance**: [Performance impact or reason there is no impact]
- **Documentation**: [How this decision improves document structure and authority]
- **Localization**: [Language, bilingual, or locale implications]

### 3.2 Positive Consequences

- [Positive consequence 1]
- [Positive consequence 2]
- [Positive consequence 3]

### 3.3 Negative Consequences

- [Negative consequence 1]
- [Negative consequence 2]

## 4. Alternatives Considered (Pros and Cons)

### [Alternative 1]

- **Good**, because [benefit]
- **Bad**, because [trade-off]

### [Alternative 2]

- **Good**, because [benefit]
- **Bad**, because [trade-off]

## 5. Confidence Level & Technical Requirements

- **Confidence Rating:** [Low | Medium | High]
- **Notes:** [Why this confidence level is justified and what would improve it]
- **Technical Requirements Addressed:** [For example: REQ-PRD-FUN-01, REQ-SPC-001]

## 6. Related Documents (Traceability)

- **Parent Master ADR**: `[./NNNN-master-adr.md]` (Optional for `domain`)
- **Parent Master ARD**: `[../ard/system-master-ard.md]` (Optional for `domain`)
- **Parent Master PRD**: `[../prd/system-master-prd.md]` (Optional for `domain`)
- **Supersedes**: `[./NNNN-old-decision.md]` (Optional)
- **Superseded by**: `[./NNNN-new-decision.md]` (Required for `Superseded`)
- **Feature PRD**: `[../prd/feature-prd.md]` (Optional)
- **Feature ARD**: `[../ard/system-ard.md]` (Optional)
- **Feature Spec**: `[../specs/YYYY-MM-DD-feature.md]` (Optional)
- **Feature Plan**: `[../plans/YYYY-MM-DD-feature.md]` (Optional)
