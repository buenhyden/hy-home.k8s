# Bootstrap Process

The bootstrap process enables a reproducible "Zero-to-Hero" build of the entire platform.

## Architecture

The process is split into 3 stages, corresponding to the scripts in `bootstrap/`.

### Stage 1: Infrastructure Layer (`cluster-setup.sh`)

**Goal**: Get a working Kubernetes API with Networking basics.

1. **Check Prereqs**: docker, kind, kubectl.
2. **Create Cluster**: `kind create cluster`.
    - Mounts host directories for persistence if configured.
    - Maps ports 80/443 to localhost.
3. **Network Setup**:
    - Installs **Ingress Nginx**.
    - Installs **MetalLB** and applies the IP Address Pool (subnet of Docker Network).
    - Injects `ip route` so Kind nodes can reach Host IPs.

### Stage 2: CD Layer (`argocd-install.sh`)

**Goal**: Install the GitOps controller.

1. **Install ArgoCD**: Applies upstream manifests.
2. **Patch ArgoCD**: Reduces resource limits for local dev (HA disabled).
3. **Wait**: Blocks until ArgoCD is healthy.

### Stage 3: App Layer (`root-apps.sh`)

**Goal**: Hand over control to Git.

1. **Apply App-of-Apps**: Applies `bootstrap/root.yaml` (or similar initial manifest).
2. **Sync**: ArgoCD takes over. It sees the `infrastructure` root app and the `apps` root app.
3. **Reconciliation**: ArgoCD pulls all other manifests (Istio, Prometheus, User Apps) and syncs them.

## Verification

After bootstrap, run:

```bash
kubectl get applications -n argocd
```

All applications should eventually become `Synced` and `Healthy`.
