---
layer: 'infra' # meta | infra | gitops | app | ops
---
# Tier Manual (TIER.md)

_Target Location: `docs/manuals/<tier-name>/README.md`_
_Description: Defines the governance, shared standards, and operational expectations for a logical infrastructure layer (Tier)._

## Overview (KR)
이 문서는 특정 인프라 계층(Tier)의 운영 표준과 거버넌스를 정의합니다. 해당 티어에 속한 서비스들이 준수해야 할 기술 표준, 보안 요구사항, 그리고 티어 간 상호작용 모델을 포함합니다.

---

## 1. Tier Metadata

- **Tier Name**: `<tier-name>`
- **Scope**: [Internal | Edge | Shared]
- **Criticality**: [High | Critical]
- **layer**: [infra | gitops | ops]

## 2. Tier Scope & Responsibility

- **Owns**: [e.g., Shared database clusters, Object storage]
- **Allowed Service Types**: [e.g., Relational DBs, NoSQL, Cache]
- **Constraints**: [e.g., No public internet access allowed for this tier]

## 3. Tier Standards (Governance)

### 3.1 Runtime Standards
- [ ] All services must use [Image Registry]
- [ ] Mandatory resource limits (CPU/MEM)
- [ ] Standardized health endpoints (`/health`)

### 3.2 Security Standards
- [ ] Encryption at rest required
- [ ] NetworkPolicy: Default Deny All (Whitelist only)
- [ ] Secret mounting via Vault/SealedSecrets

## 4. Cross-Tier Interaction Model

- **Upstream Tiers**: [Who depends on us?]
- **Downstream Tiers**: [Who do we depend on?]
- **Allowed Traffic**:
  | Source Tier | Destination Tier | Protocol | Port |
  | :--- | :--- | :--- | :--- |
  | Application | Data | TCP | 5432 |

## 5. Observability & Reliability

- **Tier-wide SLOs**: [Global targets for all services in this tier]
- **Shared Dashboards**: [Link]
- **Critical Alerts**: [List of alerts that pager the tier owner]

## 6. Deployment & Promotion
- **Promotion Flow**: Dev -> Staging -> Prod (via GitOps)
- **Change Management**: Major changes require ADR + ARD update.

## 7. Inventory (Managed Services)
| Service Name | Description | Status |
| :--- | :--- | :--- |
| `service-a` | Primary database | [Production] |
| `service-b` | Distributed cache | [Production] |

## 8. Related Artifacts
- **Tier ARD**: `[docs/ard/<tier>-ard.md]`
- **Tier Policies**: `[docs/manuals/<tier>/policies.md]`
