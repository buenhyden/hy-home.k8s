# Directory Structure

Overview of the GitOps repository structure.

## Top-Level Structure

```
hy-home.k8s/
├── apps/                   # Application workloads
├── bootstrap/              # Cluster bootstrap scripts
├── clusters/               # Cluster-specific configurations
├── docs/                   # Documentation
├── infrastructure/         # Platform infrastructure
└── README.md              # Project overview
```

## Apps Directory

```
apps/
├── _templates/            # Reusable application templates
│   ├── backend/          # Backend service template
│   ├── frontend/         # Frontend application template
│   └── README.md
├── _examples/            # Reference implementations
│   ├── demo-backend/     # FastAPI backend example
│   ├── demo-frontend/    # React frontend example
│   └── README.md
└── README.md            # Apps usage guide
```

**Purpose**: Contains application templates and examples. Actual applications would be added here as subdirectories.

## Bootstrap Directory

```
bootstrap/
├── README.md            # Bootstrap instructions
├── cluster-setup.sh     # Creates Kind cluster
├── argocd-install.sh    # Installs ArgoCD
└── root-apps.sh         # Deploys root applications
```

**Purpose**: Scripts to set up a new cluster from scratch.

## Clusters Directory

```
clusters/
└── docker-desktop/              # Cluster-specific config
    ├── apps.yaml                # Apps root application
    ├── infrastructure.yaml      # Infrastructure root application
    ├── applications/            # Application definitions
    │   ├── _template.yaml      # Template for new apps
    │   ├── backend-1.yaml      # (optional - from legacy)
    │   ├── backend-2.yaml      # (optional - from legacy)
    │   └── frontend.yaml       # (optional - from legacy)
    ├── infrastructure/          # Infrastructure app definitions
    │   ├── kustomization.yaml
    │   ├── namespaces.yaml
    │   ├── controllers-app.yaml
    │   ├── observability-app.yaml
    │   ├── security-app.yaml
    │   ├── external-services-app.yaml
    │   └── workflow-app.yaml
    ├── config/                  # Cluster-specific configs (future use)
    └── bootstrap/               # Cluster-specific setup scripts
        └── bootstrap-argocd-repo.sh
```

**Purpose**: Cluster-specific ArgoCD Applications and configurations.

## Infrastructure Directory

```
infrastructure/
├── controllers/             # Cluster controllers
│   ├── istio-base/
│   ├── istio-istiod/
│   ├── istio-gateway/
│   └── metallb/
├── observability/          # Monitoring and logging
│   ├── kube-prometheus-stack/
│   ├── loki/
│   ├── tempo/
│   └── alloy/
├── security/               # Security tools
│   ├── cert-manager/
│   ├── kyverno/
│   └── sealed-secrets/
├── external-services/      # External service connectors
│   ├── postgres/
│   ├── redis/
│   ├── kafka/
│   └── opensearch/
└── workflow/               # Workflow orchestration
    └── airflow/
```

**Purpose**: Platform infrastructure managed via ArgoCD.

## Docs Directory

```
docs/
├── README.md                  # Documentation index
├── guides/                    # User guides
│   ├── getting-started.md
│   ├── adding-applications.md
│   ├── credentials.md
│   └── troubleshooting.md
├── reference/                 # Technical reference
│   ├── directory-structure.md (this file)
│   └── infrastructure-tools.md
├── architecture/              # Architecture documentation
│   └── overview.md
└── templates/                 # Documentation templates
    └── service-readme.md
```

**Purpose**: All project documentation organized by type.

## GitOps Workflow

### Application Deployment Flow

```
Developer → Git Push → ArgoCD Watches → Sync to Cluster → Application Running
```

1. Developer commits application manifests to `apps/my-app/`
2. ArgoCD detects changes (every 3 minutes or via webhook)
3. ArgoCD syncs manifests to Kubernetes cluster
4. Application is deployed using Argo Rollouts (canary)

### Infrastructure Management Flow

```
Ops Team → Git Push → ArgoCD Infrastructure App → Component Apps → Infrastructure Ready
```

1. Update infrastructure component in `infrastructure/`
2. ArgoCD infrastructure root app detects change
3. Component-specific apps sync changes
4. Infrastructure is updated (Helm charts deployed)

## ArgoCD App-of-Apps Pattern

### Root Applications

- `clusters/docker-desktop/apps.yaml` - Manages application workloads
- `clusters/docker-desktop/infrastructure.yaml` - Manages infrastructure components

### Child Applications

**Infrastructure Children:**

- `controllers` → Istio, MetalLB
- `observability` → Prometheus, Loki, Tempo, Alloy
- `security` → Kyverno, Cert-Manager, Sealed Secrets
- `external-services` → PostgreSQL, Redis connectors
- `workflow` → Apache Airflow

**Apps Children:**

- Created dynamically for each application in `apps/`

## File Naming Conventions

- **Directories**: lowercase with hyphens (e.g., `kube-prometheus-stack`)
- **YAML files**: lowercase with hyphens (e.g., `rollout.yaml`, `virtual-service.yaml`)
- **Scripts**: lowercase with hyphens, `.sh` extension (e.g., `cluster-setup.sh`)
- **Templates**: prefix with underscore (e.g., `_templates/`, `_examples/`)

## Next Steps

- **Add Application**: Copy from `apps/_templates/`
- **Modify Infrastructure**: Edit files in `infrastructure/`
- **Bootstrap New Cluster**: Run scripts in `bootstrap/`
- **View Architecture**: See `docs/architecture/overview.md`
