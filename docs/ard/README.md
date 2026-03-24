---
layer: "meta"
---

# ARD

- **Status**: Approved
- **layer:** meta

**Overview (KR):** 아키텍처 참조 문서(ARD) 목록 및 인덱스.
요구사항과 제약 조건을 정의하는 문서들의 모음입니다.

This directory contains Architecture Requirements Documents that define the technical requirements and constraints for system architecture.

## What is an ARD?

An Architecture Requirements Document (ARD) captures the "how" of system architecture - the technical requirements, constraints, and non-functional requirements that shape the system design. Unlike ADRs which capture decisions, ARDs capture requirements.

### ARD vs ADR

| Document | Focus | Question Answered |
| --- | --- | --- |
| **ADR** | Decisions | "Why did we choose X?" |
| **ARD** | Requirements | "What must the system do?" |

## When to Create an ARD

Create an ARD when:

- Starting a new project or major feature
- Defining technical constraints and NFRs
- Documenting system boundaries and scope
- Establishing performance/security requirements

## How to Create an ARD

1. **File Placement**: All ARDs MUST be placed directly in `docs/ard/`. Do NOT create subdirectories.
2. **Metadata**: Include `layer:` metadata in the frontmatter.
3. **Use the Template**: Copy `templates/ard-template.md` to this directory
4. **Name Convention**: `[system]-requirements.md` (e.g., `payment-service-requirements.md`)
5. **Fill All Sections**: Business goals, scope, functional/non-functional requirements, constraints

```bash
# Example workflow
mkdir -p docs/ard/users
cp templates/ard-template.md docs/ard/users/user-service-requirements.md
# Edit the file with your requirements
```

## ARD Template

All ARDs MUST use `templates/ard-template.md`. The template includes:

| Section | Purpose |
| --- | --- |
| **Introduction** | High-level overview |
| **Business Goals** | Top-level objectives |
| **Scope** | System boundaries |
| **Functional Requirements** | Core technical capabilities |
| **Non-Functional Requirements** | Performance, scalability, reliability, security |
| **Constraints** | External limitations |

## Key Sections

### Non-Functional Requirements (NFRs)

NFRs are critical for ARDs. Document:

- **Performance**: Latency, throughput, response times
- **Scalability**: Load projections, scaling strategy
- **Reliability**: Uptime SLA, RTO/RPO
- **Security**: Encryption, compliance, authentication
- **Observability**: Logging, metrics, tracing

### Constraints

Document factors that limit architectural choices:

- Budget limitations
- Technology constraints
- Team expertise
- Regulatory compliance
- Legacy system integration

## Relationship to Other Documents

```text
[Business Need]
      ↓
docs/prd/ (What - Product Requirements)
      ↓
docs/ard/ (How - Architecture Requirements, validated via 6 Core Engineering Pillars)
      ↓
docs/adr/ (Why - Architecture Decisions)
      ↓
specs/ (Implementation Specifications)
```

## Related Documents

- [docs/prd/2026-02-27-home-cluster-infra-prd.md](../prd/2026-02-27-home-cluster-infra-prd.md)
- [docs/specs/2026-03-16-infra-spec.md](../specs/2026-03-16-infra-spec.md)

## AI Agent Guidelines

When working with ARDs:

1. **Read before designing**: Check existing ARDs for technical constraints.
2. **Use template**: Always use `templates/ard-template.md`.
3. **Be specific**: Quantify NFRs (e.g., "99.9% uptime" not "high availability").
4. **Link to ADRs**: Reference relevant ADRs in the constraints section.
5. **Pillar Validation**: Ensure alignment with the 6 Core Engineering Pillars (Security, Observability, Performance, Compliance, Documentation, Localization) as defined in `.agent/rules/`.

## Index of ARDs

| Last Updated | Document | Description | Status |
| :--- | :--- | :--- | :--- |
| 2026-03-24 | [k3d-cluster-ard](./2026-02-27-k3d-cluster-ard.md) | Standard for local k3s/k3d cluster layout on WSL2. | Approved |
| 2026-03-24 | [argocd-gitops-ard](./2026-03-07-argocd-gitops-ard.md) | GitOps and Sealed Secrets architecture. | Approved |
| 2026-03-24 | [documentation-architecture-ard](./2026-03-15-documentation-architecture-ard.md) | Taxonomy, metadata, and doc system standards. | Approved |
| 2026-03-24 | [agent-instruction-system-ard](./2026-03-16-agent-instruction-system-ard.md) | AI agent collaboration and lazy-loading architecture. | Approved |
| 2026-03-24 | [architecture-checklist-ard](./2026-03-16-architecture-checklist-ard.md) | Mandatory tech stack and structure checklist. | Approved |

> [!NOTE]
> All ARDs have been modernized to the "Elite" enterprise standard as of 2026-03-24.
