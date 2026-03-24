---
title: 'Architecture & Tech Stack Checklist'
status: 'Approved'
owner: 'buenhyden'
scope: 'master'
tags: ['ard', 'infra']
layer: "infra"
---

# Architecture & Tech Stack Checklist (ARD)

## Overview (KR)
이 문서는 신규 프로젝트 또는 아키텍처 문서(ARD/PRD/Spec)를 작성할 때 반드시 검토하고 준수해야 할 기술적/구조적 체크리스트를 정의합니다. Senior-level 아키텍처 기준(Pillar Alignment, Compliance, Scalability)을 포함합니다.

---

## 1. Metadata & Status

- **Status**: Approved
- **Owner**: buenhyden
- **Scope**: master
- **layer:** infra

## 2. Architecture Checklist (Operational)

| Category | Check Question | Priority | Notes / Decisions |
| :--- | :--- | :--- | :--- |
| **Architecture Style** | Is the style (Monolithic, Modular, Microservices) explicitly decided? | **Mandatory** | |
| **Service Boundaries** | Are responsibilities expressed in C4 diagrams? | **Mandatory** | |
| **Domain Model** | Are core entities and relations defined (ER/UML)? | **Mandatory** | |
| **Tech Stack (BE)** | Language, framework, and key libs (ORM, etc.) decided? | **Mandatory** | |
| **Tech Stack (FE)** | Framework (React/Next), state, and build tools decided? | **Mandatory** | |
| **Database** | DB Engine and schema strategy decided? | **Mandatory** | |
| **FinOps** | Is there a monthly cost estimate and optimization strategy? | **Mandatory** | |
| **Sustainability** | Resource footprint and "Greedy-Green" alignment? | **Mandatory** | |
| **Pillar Alignment** | Aligns with 6 Pillars (Security, Perf, Obs, GRC, Doc, L10n)? | **Mandatory** | |
| **Agent Compliance** | Selection complies with specific laws in `.agent/rules/`? | **Mandatory** | |

## 3. Resilience & Compliance

- **Decision Drivers**: Must justify departures from the Tech Stack Law.
- **Audit Requirement**: Every check marking "Mandatory" must have a corresponding link to a Spec or ADR.

## Related Documents

- [adr-template.md](../../templates/adr-template.md)
- [0001-k3d-local-cluster.md](../adr/0001-k3d-local-cluster.md)
