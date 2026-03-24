---
layer: 'app' # meta | infra | gitops | app | ops
---
# Service Manual (SERVICE.md)

_Target Location: `SERVICE.md` (Project Root) or `docs/manuals/<service>/README.md`_
_Description: The authoritative operational and technical guide for a specific service. It follows the Index Pattern for scalability._

## Overview (KR)
이 문서는 특정 서비스의 설계, 구성, 배포 및 운영에 관한 모든 기술적 맥락을 제공합니다. 서비스의 역할, 아키텍처, 의존성, 그리고 장애 대응 절차를 포함합니다.

> [!TIP]
> **Index Pattern**: 이 문서가 500라인을 초과할 경우, `docs/manuals/<service>/` 폴더 내에 `README.md`로 위치시키고, 아키텍처, 설정, 트러블슈팅 등을 별도 파일로 분리하여 링크하십시오.

---

## 1. Quick Facts & Ownership

| Field | Value |
| :--- | :--- |
| **Service Name** | `<service-name>` |
| **Tier** | `<edge | gateway | platform | security | data | app>` |
| **Criticality** | `<low | medium | high | critical>` |
| **Owner** | `<Team/Person>` |
| **On-call** | [PagerDuty/Slack Channel] |

## 2. Service Summary & Role

- **Definition**: [One-sentence description]
- **Value Proposition**: [Why this service exists]
- **Core Responsibilities**:
  - [Responsibility 1]
  - [Responsibility 2]

## 3. Architecture & Data Flow (Senior)

### 3.1 Component Diagram (C4)
[Refer to `ARD.md` for deep architecture. This section focuses on runtime components.]

### 3.2 Request Path
[e.g., Client -> Ingress -> [This Service] -> PostgeSQL]

## 4. Configuration & Environment

- **Config Source**: [e.g., ConfigMap, Secret, Environment Variables]
- **Key Variables**:
  | Variable | Required | Default | Description |
  | :--- | :--- | :--- | :--- |
  | `PORT` | Yes | 8080 | Listening port |
  | `DB_URL` | Yes | - | Connection string |

## 5. Developer Experience (DX) & Tooling (Senior)

- **Local Setup**: `nix-shell` or `devcontainer` (One-command setup)
- **Mocking Strategy**: [How to run without external deps / local-stack]
- **Tooling References**: [CLI tools, specific scripts]

## 6. Deployment & GitOps (Senior)

- **Runtime**: [e.g., K8s / Docker Compose]
- **GitOps Tool**: [e.g., ArgoCD / Flux]
- **Sync Policy**: [e.g., Automated pruning, Self-healing enabled]
- **Health Probes**:
  - **Liveness**: `/healthz`
  - **Readiness**: `/readyz`

## 7. Observability & SLIs

### 7.1 Service Level Indicators (SLIs)
- **Availability**: 99.9%
- **Latency (p95)**: < 200ms
- **Error Rate**: < 0.1%

### 7.2 Monitoring Links
- **Dashboard**: [Grafana Link]
- **Logs**: [Datadog/ELK Link]

## 8. Reliability & Failure Modes (Senior)

| Mode | Symptom | Immediate Action |
| :--- | :--- | :--- |
| **Throttled** | CPU usage 100%, high latency | Scale up (HPA) |
| **OOM Killed** | Container restarts frequently | Increase Memory limit |
| **Conn Pool Full** | 500 errors, timeout | check DB locks |

## 9. Operational Procedures (Day-2)
- **Scaling**: `kubectl scale deployment <name> --replicas=5`
- **Manual Restart**: `kubectl rollout restart deployment <name>`
- **Credential Rotation**: [Refer to Runbook]

## 10. Related Artifacts
- **Architecture**: `[ARD.md]`
- **Decisions**: `[docs/adr/]`
- **Runbook**: `[docs/runbooks/<service>.md]`
- **Spec**: `[docs/specs/<service>-spec.md]`
