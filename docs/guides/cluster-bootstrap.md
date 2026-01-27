# Guide: Cluster Bootstrap

This guide describes the process of setting up the `hy-home.k8s` environment from scratch.

## 🛠️ Prerequisites

Ensure you have the following tools installed:

- **Docker Desktop**: With Kubernetes disabled (we will use Kind).
- **kubectl**: Kubernetes CLI.
- **Kind**: [Kubernetes in Docker](https://kind.sigs.k8s.io/).
- **kustomize**: Manifest management.

---

## 🚀 Bootstrap Process

### 1. Provision Infrastructure

Run the `cluster-setup.sh` script to create a multi-node Kind cluster:

```bash
./bootstrap/cluster-setup.sh
```

This creates:

- 1 Control Plane
- 3 Workers
- Custom networking to allow communication with external Docker services.

### 2. Install ArgoCD

Deploy the GitOps controller:

```bash
./bootstrap/argocd-install.sh
```

Wait until all ArgoCD pods are running:

```bash
kubectl get pods -n argocd
```

### 3. Deploy Root Applications

The "App-of-Apps" pattern is used to manage all other components. Run:

```bash
./bootstrap/root-apps.sh
```

This deploys:

- **Infrastructure App**: Manages Istio, Prometheus, Kyverno, etc.
- **Applications App**: Manages all user-level services in `apps/`.

---

## 🔑 Accessing ArgoCD

Retrieve the initial admin password:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

Open a port-forward to access the UI:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Visit: `https://localhost:8080`

---

## 📡 Network Configuration (Hybrid Cloud)

To allow the cluster to reach Docker containers running outside of Kind (e.g., local DBs):

```bash
# Get the Docker network gateway
GATEWAY=$(docker network inspect bridge --format "{{(index .IPAM.Config 0).Gateway}}")

# Add routes to the Kind nodes (example for control plane)
docker exec -it docker-desktop-control-plane ip route add 172.19.0.0/16 via $GATEWAY
```

### Note

These routes are managed by the bootstrap scripts, but may need manual verification if networking issues occur.
