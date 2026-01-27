# Docker Desktop Cluster Configuration

This directory contains cluster-specific configurations for the `docker-desktop` Kubernetes cluster running on Kind.

## Overview

The `docker-desktop` cluster is a local Kubernetes environment managed using the GitOps pattern with ArgoCD. It consists of two main root applications that manage all platform components and user applications.

## Directory Structure

```text
clusters/docker-desktop/
├── apps.yaml                      # Apps root application
├── infrastructure.yaml            # Infrastructure root application
├── applications/                  # Application definitions
│   ├── _app-template.yaml        # Template for new applications
│   └── *.yaml                    # Individual app definitions
├── infrastructure/                # Infrastructure app definitions
│   ├── kustomization.yaml
│   ├── namespaces.yaml
│   ├── controllers-app.yaml
│   ├── observability-app.yaml
│   ├── security-app.yaml
│   ├── external-services-app.yaml
│   └── workflow-app.yaml
├── config/                        # Cluster-specific configs (future use)
├── bootstrap/                     # Cluster bootstrap scripts
│   └── bootstrap-argocd-repo.sh
└── scripts/                       # Cluster-specific scripts
```

## Root Applications

### apps.yaml - Applications Root

**Purpose**: Manages all user-facing application deployments using the App-of-Apps pattern.

**Source Path**: `clusters/docker-desktop/applications/`

**Key Configuration**:

```yaml
spec:
  project: default
  source:
    repoURL: https://github.com/buenhyden/hy-home.k8s.git
    targetRevision: main
    path: clusters/docker-desktop/applications
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

**How It Works**:

1. ArgoCD monitors the `applications/` directory
2. Any YAML file defining an Application is automatically deployed
3. Applications sync to their respective target paths in `apps/`

### infrastructure.yaml - Infrastructure Root

**Purpose**: Manages all platform infrastructure components in a specific order.

**Source Path**: `clusters/docker-desktop/infrastructure/`

**Key Configuration**:

```yaml
spec:
  project: default
  source:
    repoURL: https://github.com/buenhyden/hy-home.k8s.git
    targetRevision: main
    path: clusters/docker-desktop/infrastructure
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

**Infrastructure Components** (deployed in order):

1. **Namespaces** - Creates all required namespaces
2. **Controllers** - Istio (service mesh), MetalLB (load balancer)
3. **Observability** - Prometheus, Loki, Tempo, Grafana, Alloy
4. **Security** - Kyverno (policies), Cert-Manager, Sealed Secrets
5. **External Services** - PostgreSQL, Redis, Kafka, OpenSearch connectors
6. **Workflow** - Apache Airflow

## Adding Applications

### Method 1: Use Template (Recommended)

```bash
# 1. Copy template
cp clusters/docker-desktop/applications/_app-template.yaml \
   clusters/docker-desktop/applications/my-app.yaml

# 2. Edit the file and replace placeholders:
#    - APP_NAME: your application name
#    - YOUR_GIT_REPO_URL: repository URL
#    - TARGET_NAMESPACE: namespace (usually 'default')
#    - ENV: dev or prod

# 3. Commit and push
git add clusters/docker-desktop/applications/my-app.yaml
git commit -m "feat: add my-app application"
git push

# ArgoCD will auto-sync within 3 minutes
```

### Method 2: Manual kubectl

```bash
kubectl apply -f clusters/docker-desktop/applications/my-app.yaml
```

### Example Application Definition

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-backend
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/buenhyden/hy-home.k8s.git
    targetRevision: main
    path: apps/my-backend/overlays/dev
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## Network Configuration

### IP Allocation

- **Kind Cluster Network**: 172.18.0.0/16
- **External Services Network**: 172.19.0.0/16
- **MetalLB LoadBalancer Pool**: 172.18.255.200-250

### Hybrid Networking

The cluster can communicate with external Docker containers (PostgreSQL, Redis, etc.) via:

1. **Headless Services**: Created in `infrastructure/external-services/`
2. **Static Endpoints**: Point to Docker container IPs (172.19.0.x)
3. **Route Configuration**: Added during bootstrap via `cluster-setup.sh`

**Example**: PostgreSQL connection

```yaml
kind: Service
metadata:
  name: postgres-external
  namespace: default
spec:
  clusterIP: None  # Headless service
---
kind: Endpoints
metadata:
  name: postgres-external
  namespace: default
subsets:
  - addresses:
      - ip: 172.19.0.56  # PostgreSQL Docker container IP
    ports:
      - port: 15432
```

## Bootstrap Process

The cluster is bootstrapped using scripts in the `bootstrap/` directory:

```bash
# 1. Create Kind cluster (from repository root)
cd bootstrap
./cluster-setup.sh

# 2. Install ArgoCD
./argocd-install.sh

# 3. Deploy root applications
./root-apps.sh
```

### Cluster-Specific Bootstrap

After the main bootstrap, run:

```bash
cd clusters/docker-desktop/bootstrap
./bootstrap-argocd-repo.sh
```

This configures:

- Git repository credentials in ArgoCD
- SSH keys for private repositories (if needed)
- Webhook secrets

## Monitoring Applications

### Via ArgoCD UI

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
# Visit https://localhost:8080
```

**Credentials**:

- Username: `admin`
- Password: Retrieved via:

  ```bash
  kubectl -n argocd get secret argocd-initial-admin-secret \
    -o jsonpath="{.data.password}" | base64 -d
  ```

### Via CLI

```bash
# List all applications
kubectl get applications -n argocd

# Watch specific application
kubectl get application my-app -n argocd -w

# Describe application for debugging
kubectl describe application my-app -n argocd
```

## Sync Policies

### Automated Sync

All applications use automated sync with:

- **prune: true** - Removes resources deleted from Git
- **selfHeal: true** - Corrects manual changes back to Git state

### Manual Sync

If needed, manually sync an application:

```bash
# Via kubectl
kubectl patch application my-app -n argocd \
  --type merge -p '{"operation":{"sync":{"revision":"HEAD"}}}'

# Via ArgoCD CLI
argocd app sync my-app
```

## Troubleshooting

### Application Not Syncing

Check application status:

```bash
kubectl describe application my-app -n argocd
```

Common issues:

- **Invalid YAML**: Check ArgoCD UI for syntax errors
- **Namespace doesn't exist**: Verify target namespace is created
- **Image not found**: Check image registry and credentials

### Infrastructure Deployment Order

If infrastructure components fail:

1. Check namespaces are created first
2. Verify CRDs are installed (e.g., Istio CRDs via istio-base)
3. Check dependencies (e.g., Kyverno requires Istio)

### Network Connectivity

Test external service connection:

```bash
# Deploy test pod
kubectl run test --image=busybox -it --rm -- sh

# Test PostgreSQL
nc -zv postgres-external 15432

# Test Redis
nc -zv redis-external 16379
```

## Security Considerations

### Git Repository Credentials

**For private repositories**, create sealed secrets:

```bash
# 1. Create SSH key
ssh-keygen -t ed25519 -f argocd-repo-key

# 2. Add public key to GitHub/GitLab

# 3. Create secret
kubectl create secret generic argocd-repo-key \
  --from-file=identity=argocd-repo-key \
  --dry-run=client -o yaml | \
  kubeseal -o yaml > argocd-git-ssh-sealedsecret.yaml

# 4. Apply the sealed secret
kubectl apply -f argocd-git-ssh-sealedsecret.yaml -n argocd
```

### ArgoCD RBAC

Default project permissions are permissive for development. For production:

1. Create project-specific AppProjects
2. Define RBAC policies in `argocd-rbac-cm` ConfigMap
3. Limit source repositories and destination namespaces

## Best Practices

1. **One Application per File**: Keep application definitions separate
2. **Use Templates**: Copy `_app-template.yaml` for consistency
3. **Descriptive Names**: Use clear, lowercase-hyphenated names
4. **Namespace Isolation**: Deploy apps to specific namespaces, not `argocd`
5. **Review Before Merge**: Check application syncs in dev environment first
6. **Monitor Sync Status**: Watch ArgoCD UI after Git pushes

## Next Steps

- **Deploy Your First App**: See [Adding Applications Guide](../../docs/guides/adding-applications.md)
- **Configure Monitoring**: Set up Grafana dashboards for your apps
- **Set Up Alerts**: Configure Prometheus alerts via PrometheusRule CRDs
- **Enable Image Updates**: Configure Argo Image Updater for automatic updates

## References

- [ArgoCD App-of-Apps Pattern](https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/)
- [ArgoCD Sync Policies](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/)
- [Kustomize](https://kustomize.io/)
