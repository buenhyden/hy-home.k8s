# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Shared cross-agent contract: [AGENTS.md](AGENTS.md)
Detailed agent instructions: [docs/agent-instructions.md](docs/agent-instructions.md)

@./docs/agentic/CLAUDE.md

Nearest scoped `CLAUDE.md` files under `docs/` take precedence for local document work.

---

## Linting and Validation

There is no root package manager. Linting and formatting run exclusively through `pre-commit`:

```bash
# Run all hooks against all files
pre-commit run --all-files

# Run a single hook
pre-commit run markdownlint-cli2 --all-files
pre-commit run kube-linter --all-files
pre-commit run prettier --all-files
```

CI runs `pre-commit` on every push and PR to `main` via `.github/workflows/ci.yml`. There are no separate build or test commands.

## Cluster Bootstrap Commands

Bootstrap order matters. Each step depends on the previous being healthy.

```bash
# 1. Create the dedicated Docker bridge (required before any cluster)
docker network create --driver bridge --subnet 172.20.0.0/16 k3d-hy-k3d

# 2. Create a cluster profile
k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml        # standard
k3d cluster create --config infrastructure/k3d/k3d-cluster.gpu.yaml    # GPU
k3d cluster create --config infrastructure/k3d/k3d-min.yaml            # minimal

# 3. Install infrastructure (in this order)
kubectl apply -f infrastructure/metallb/metallb-native.yaml
kubectl apply -f infrastructure/ipaddresspool.yaml
kubectl apply -f infrastructure/ingress-nginx/ingress-nginx.yaml
kubectl apply -f infrastructure/ingress-nginx/nodeport-service.yaml
kubectl apply -f infrastructure/sealed-secrets/sealed-secrets.yaml
kubectl apply -f infrastructure/namespaces/

# 4. Verify the baseline
kubectl get nodes
curl -I http://127.0.0.1:18080/

# 5. Bootstrap GitOps (optional, after baseline is healthy)
kubectl apply -f infrastructure/argocd/argocd-install.yaml
kubectl apply -f gitops/clusters/local/root-application.yaml
kubectl -n argocd port-forward svc/argocd-server 8080:443
```

## Key Architecture Decisions

**`infrastructure/` vs `gitops/` split**: `infrastructure/` contains pinned manifests to bootstrap the platform itself (MetalLB, ingress-nginx, Sealed Secrets, ArgoCD). `gitops/` contains the ArgoCD App-of-Apps layout that takes over reconciliation after the platform is healthy. Do not use GitOps manifests for bootstrapping, and do not hand-apply GitOps-managed resources after ArgoCD is running.

**Spec-first contribution**: All infrastructure or documentation changes must start with a spec in `docs/specs/`. PRs without a corresponding spec are automatically rejected. Use `templates/` for all document types (ADR, PRD, runbook, spec, plan).

**GitOps pinning**: The root application at `gitops/clusters/local/root-application.yaml` pins `targetRevision` to a specific Git SHA. Advancing GitOps state requires updating that SHA intentionally — it is not "latest commit wins."

**Networking assumptions**: MetalLB pool is `172.20.0.100–172.20.0.150` on the `172.20.0.0/16` bridge. Ingress is exposed at `127.0.0.1:18080` (NodePort 30080) and `127.0.0.1:18443` (NodePort 30443). ArgoCD is accessed via `kubectl port-forward` only, not through ingress.
