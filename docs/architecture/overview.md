# Architecture Overview

High-level architecture of the hy-home.k8s GitOps platform.

## System Architecture

```mermaid
graph TB
    subgraph "GitOps (This Repository)"
        Git[GitHub Repository<br/>hy-home.k8s]
    end
    
    subgraph "Kind Cluster - 172.18.0.0/16"
        subgraph "ArgoCD"
            ArgoCD[ArgoCD Controller]
            AppsRoot[Apps Root App]
            InfraRoot[Infrastructure Root App]
        end
        
        subgraph "Applications"
            App1[Backend Services]
            App2[Frontend Apps]
        end
        
        subgraph "Infrastructure"
            Istio[Istio Service Mesh]
            Prometheus[Prometheus Stack]
            Loki[Loki]
            Kyverno[Kyverno]
        end
    end
    
    subgraph "Docker Network - 172.19.0.0/16"
        PostgreSQL[(PostgreSQL<br/>Patroni HA)]
        Redis[(Redis Cluster)]
    end
    
    Git -->|Sync| ArgoCD
    ArgoCD --> AppsRoot
    ArgoCD --> InfraRoot
    AppsRoot --> App1
    AppsRoot --> App2
    InfraRoot --> Istio
    InfraRoot --> Prometheus
    InfraRoot --> Loki
    InfraRoot --> Kyverno
    
    App1 -.->|Headless Service| PostgreSQL
    App1 -.->|Headless Service| Redis
```

## Core Principles

### 1. GitOps

- **Git as Source of Truth**: All configuration in Git
- **Declarative**: Describe desired state, not procedures
- **Automated Sync**: ArgoCD continuously reconciles
- **Auditable**: All changes tracked via Git history

### 2. App-of-Apps Pattern

```
Root Application
├── Infrastructure Apps
│   ├── Controllers
│   ├── Observability
│   ├── Security
│   ├── External Services
│   └── Workflow
└── Application Apps
    ├── Backend Services
    └── Frontend Apps
```

Benefits:

- Centralized management
- Dependency ordering
- Easy rollback (revert Git commit)
- Consistent deployment process

### 3. Kustomize Overlays

```
Base Manifests (generic)
├── Dev Overlay (low resources, debug enabled)
└── Prod Overlay (high resources, optimized)
```

Advantages:

- DRY (Don't Repeat Yourself)
- Environment-specific customization
- No templating complexity

## Component Architecture

### Service Mesh (Istio)

**Purpose**: Traffic management, security, observability

```
Request → Istio Gateway → VirtualService → Envoy Sidecar → Pod
```

- **mTLS**: Automatic encryption between services
- **Traffic Control**: Canary deployments via VirtualService
- **Observability**: Auto-instrumented metrics and traces

### Observability Stack

**Components**:

- **Prometheus**: Metrics collection and storage
- **Loki**: Log aggregation
- **Tempo**: Distributed tracing
- **Alloy**: Unified telemetry agent
- **Grafana**: Visualization

**Data Flow**:

```
Applications → Alloy → Prometheus/Loki/Tempo → Grafana
```

### Security

**Kyverno Policies**:

- Enforce non-root containers
- Block `:latest` image tags
- Require resource limits

**Cert-Manager**:

- Automatic TLS certificate management
- Let's Encrypt integration

**Sealed Secrets**:

- Encrypted secrets safe for Git

### Progressive Delivery

**Argo Rollouts**:

```
Deploy v2 → 20% traffic → Wait 30s → 50% traffic → Wait 30s → 100%
```

- Automated rollback on failures
- Istio integration for traffic splitting
- Blue/Green and Canary strategies

## Network Architecture

### IP Allocation

- **Kind Cluster**: 172.18.0.0/16
- **External Services**: 172.19.0.0/16
- **MetalLB Pool**: 172.18.255.200-250

### Service Communication

**Internal (within cluster)**:

```
Service A → Kubernetes Service → Istio Sidecar → Service B
```

**External (to Docker containers)**:

```
Pod → Headless Service → Static Endpoints → Docker IP
```

Example: PostgreSQL connection

```yaml
Service: postgres-external (ClusterIP: None)
Endpoints: 172.19.0.56:15432
```

## Deployment Workflow

### 1. Bootstrap (One-time)

```bash
bootstrap/cluster-setup.sh     # Create Kind cluster
bootstrap/argocd-install.sh    # Install ArgoCD
bootstrap/root-apps.sh         # Deploy root apps
```

### 2. Infrastructure Deployment

```
infrastructure.yaml (root)
  ├── Controllers (Istio, MetalLB)
  ├── Observability (Prometheus, Loki, etc.)
  ├── Security (Kyverno, Cert-Manager)
  └── External Services (DB connectors)
```

**Sequence**:

1. Namespaces created
2. Istio CRDs and control plane
3. Observability stack
4. Security policies
5. Applications can now deploy

### 3. Application Deployment

```
apps.yaml (root)
  ├── Backend Services (Argo Rollouts)
  └── Frontend Apps (Argo Rollouts)
```

**For each app**:

1. Create manifests in `apps/my-app/`
2. Commit to Git
3. ArgoCD auto-syncs (or manual sync)
4. Canary deployment begins
5. Progressive traffic shift
6. Monitor in ArgoCD/Grafana

## High Availability

### Application HA

- **PodDisruptionBudget**: Min 1 pod during updates
- **Multiple Replicas**: 3 for backends, 2 for frontends
- **HPA**: Auto-scale based on CPU/memory
- **Canary Deployment**: Zero-downtime updates

### Infrastructure HA

- **Istio**: Multi-replica control plane
- **Prometheus**: 10-day retention, persistent storage
- **PostgreSQL**: Patroni HA (3 nodes)
- **Redis**: 6-node cluster (3 masters, 3 replicas)

## Failure Handling

### Application Failures

- **Rollout Failure**: Automatic rollback to previous version
- **Pod Crash**: Kubernetes auto-restart
- **Resource Exhaustion**: HPA scales up

### Infrastructure Failures

- **ArgoCD Down**: Manual kubectl still works; ArgoCD recovers
- **Istio Down**: Traffic fails; critical issue
- **Prometheus Down**: No metrics; logs still work

## Security Model

### Defense in Depth

1. **Network**: Istio mTLS for all traffic
2. **Runtime**: Non-root containers (Kyverno enforced)
3. **Secrets**: Sealed Secrets, never plain text in Git
4. **RBAC**: Minimal privileges for service accounts
5. **Policies**: Kyverno validates all deployments

### Secret Management

```
1. Create secret locally
2. Encrypt with kubeseal
3. Commit encrypted SealedSecret to Git
4. Sealed Secrets controller decrypts in-cluster
5. Application uses decrypted Secret
```

## Scalability

### Horizontal Scaling

- **Applications**: HPA manages replicas (2-10)
- **Infrastructure**: Fixed replicas (tuned per component)

### Resource Management

- **Requests**: Guaranteed resources
- **Limits**: Maximum allowed
- **Namespace Quotas**: Prevent resource hogging

## Monitoring & Alerting

### Metrics

- **Application**: Custom metrics via Prometheus client
- **Infrastructure**: Node, pod, container metrics
- **Business**: Request rate, latency, errors

### Alerting

- **Prometheus Alertmanager**: Alert routing
- **Grafana**: Dashboard-based alerts
- **Integration**: Slack, email, PagerDuty

## Backup & Recovery

### GitOps = Backup

- All configuration in Git
- Redeployment = restore from Git

### Stateful Data

- **PostgreSQL**: External, managed separately
- **Prometheus**: 10-day retention, acceptable loss
- **Loki**: Short retention, acceptable loss

## Future Enhancements

- Multi-cluster support
- Progressive delivery experiments (A/B testing)
- Cost optimization policies
- Enhanced secret rotation
- Service-level SLOs

## References

- [Directory Structure](../reference/directory-structure.md)
- [Infrastructure Tools](../reference/infrastructure-tools.md)
- [Getting Started](../guides/getting-started.md)
