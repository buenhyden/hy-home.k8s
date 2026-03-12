# hy-home.k8s

![Kubernetes](https://img.shields.io/badge/kubernetes-v1.31.0-blue.svg)
![k3d](https://img.shields.io/badge/k3d-v5.x-orange.svg)
![WSL2](https://img.shields.io/badge/platform-WSL2-informational.svg)

> Operator-first local Kubernetes platform for WSL2, built around k3d, deterministic networking, and optional GitOps bootstrap with ArgoCD.

## Overview

`hy-home.k8s` is a local-first Kubernetes platform repository for running a reproducible multi-node k3s cluster inside Docker on WSL2. It is designed for operators who want a stable homelab or development environment with clear bootstrap steps, pinned infrastructure manifests, and documented operational workflows.

This repository combines three ideas:

- **WSL2 + k3d** for a lightweight but production-shaped local cluster
- **Deterministic networking** so ingress and LoadBalancer behavior stay predictable across rebuilds
- **GitOps as an optional control plane** using ArgoCD and Sealed Secrets once the base cluster is healthy

This repository is **not** a generic cloud deployment starter, a SaaS application scaffold, or a package-manager-driven web service. The primary target is a self-managed local cluster running on WSL2.

## Key Features

- Run a reproducible k3s cluster through [infrastructure/k3d/](./infrastructure/k3d/) with standard, GPU-enabled, and minimal profiles.
- Reserve a dedicated Docker bridge network so MetalLB can advertise stable local IPs from a known CIDR.
- Install pinned infrastructure components from this repo:
  - MetalLB
  - ingress-nginx
  - Sealed Secrets
  - ArgoCD
- Bootstrap GitOps through an App-of-Apps layout rooted at [gitops/clusters/local/root-application.yaml](./gitops/clusters/local/root-application.yaml).
- Keep platform knowledge close to the code through [docs/runbooks/](./docs/runbooks/), [docs/specs/](./docs/specs/), and root governance files.

## Tech Stack

| Category | Technology | Notes |
| --- | --- | --- |
| Cluster engine | k3d | Runs k3s nodes in Docker containers on WSL2 |
| Kubernetes distribution | k3s `v1.31.0-k3s1` | Pinned in the cluster manifests |
| Host platform | WSL2 (Ubuntu) | Default operating environment for this repo |
| Container runtime | Docker Engine | Expected to run inside WSL2 with `systemd=true` in the default workflow |
| Ingress | ingress-nginx | Exposed through NodePorts `30080` and `30443`, mapped to host ports `18080` and `18443` |
| Load balancing | MetalLB | Advertises `172.20.0.100-172.20.0.150` from the dedicated Docker network |
| GitOps | ArgoCD | Accessed by `kubectl port-forward` in the local setup |
| Secret management | Sealed Secrets | Supports Git-safe repository credentials and other Kubernetes secrets |
| Documentation model | Spec-Driven Development | Specs, ADRs, ARDs, and runbooks are treated as first-class operating assets |

## Prerequisites

Prepare the host before creating a cluster.

| Requirement | Minimum | Why it matters |
| --- | --- | --- |
| WSL2 | `0.67.6+` | Required for the supported Linux host environment |
| `systemd` in WSL2 | enabled | Required in the default workflow so Docker Engine can run as a service inside WSL2 |
| Docker Engine | current | k3d provisions k3s nodes as Docker containers |
| `k3d` CLI | `5.x+` | Creates and manages the local cluster |
| `kubectl` | compatible with Kubernetes `1.31` | Verifies and manages the cluster |
| Linux filesystem workspace | repo under `/home/...` | Avoids the performance penalty of `/mnt/c/...` |
| NVIDIA Container Toolkit | optional | Required only for the GPU-enabled cluster profile |

Before proceeding, confirm:

```bash
wsl --version
docker --version
k3d version
kubectl version --client
```

## Quick Start

Use this sequence for the fastest path from a fresh machine to a healthy local cluster.

### 1. Create the dedicated Docker network

MetalLB depends on a fixed bridge network and address pool. Create the network before creating any cluster profile.

```bash
docker network create --driver bridge --subnet 172.20.0.0/16 k3d-hy-k3d
```

### 2. Create a cluster profile

Choose one profile based on your hardware and intended workload density.

```bash
# Standard profile: 1 server + 3 agents
k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml

# GPU profile: same topology, adds GPU access to the runtime
k3d cluster create --config infrastructure/k3d/k3d-cluster.gpu.yaml

# Minimal profile: 1 server + 1 agent for lower-resource testing
k3d cluster create --config infrastructure/k3d/k3d-min.yaml
```

The standard and GPU profiles create a cluster named `hy-k3d`. The minimal profile creates `hy-k3d-min`.

### 3. Install the core infrastructure baseline

Apply the pinned manifests in this order:

```bash
# MetalLB controller
kubectl apply -f infrastructure/metallb/metallb-native.yaml

# MetalLB address pool and L2 advertisement
kubectl apply -f infrastructure/ipaddresspool.yaml

# ingress-nginx controller and deterministic NodePort service
kubectl apply -f infrastructure/ingress-nginx/ingress-nginx.yaml
kubectl apply -f infrastructure/ingress-nginx/nodeport-service.yaml

# Sealed Secrets controller
kubectl apply -f infrastructure/sealed-secrets/sealed-secrets.yaml

# Workload namespaces
kubectl apply -f infrastructure/namespaces/
```

### 4. Verify the platform baseline

```bash
kubectl get nodes
kubectl -n metallb-system get pods
kubectl -n ingress-nginx get pods
kubectl -n kube-system get pods -l name=sealed-secrets-controller
curl -I http://127.0.0.1:18080/
```

### 5. Bootstrap GitOps when you are ready

GitOps is optional for cluster creation, but required if you want ArgoCD to reconcile the manifests under [gitops/](./gitops/).

```bash
# Install ArgoCD
kubectl apply -f infrastructure/argocd/argocd-install.yaml

# Apply your sealed repository credential to the argocd namespace
# This repo does not commit plaintext credentials.

# Register the root application
kubectl apply -f gitops/clusters/local/root-application.yaml
```

Access ArgoCD locally:

```bash
kubectl -n argocd port-forward svc/argocd-server 8080:443
```

## Detailed Bootstrap Flow

### Cluster profiles

| Profile | Manifest | Topology | Use when |
| --- | --- | --- | --- |
| Standard | [infrastructure/k3d/k3d-cluster.yaml](./infrastructure/k3d/k3d-cluster.yaml) | `1` server, `3` agents, cluster name `hy-k3d` | Default operator workflow |
| GPU | [infrastructure/k3d/k3d-cluster.gpu.yaml](./infrastructure/k3d/k3d-cluster.gpu.yaml) | `1` server, `3` agents, cluster name `hy-k3d`, `gpuRequest: all` | AI/ML or media workloads that need GPU pass-through |
| Minimal | [infrastructure/k3d/k3d-min.yaml](./infrastructure/k3d/k3d-min.yaml) | `1` server, `1` agent, cluster name `hy-k3d-min` | Lower-memory or smoke-test environments |

All profiles:

- disable the bundled `traefik` ingress
- disable the bundled `servicelb`
- add `127.0.0.1` as a k3s TLS SAN
- map ingress traffic through the k3d load balancer

### Why the bootstrap order matters

1. The Docker network must exist first so MetalLB’s address pool matches the real container subnet.
2. The cluster must exist before applying any vendored infrastructure manifests.
3. MetalLB should be installed before expecting `LoadBalancer` services to receive external IPs.
4. ingress-nginx should be installed before testing localhost ingress access on `18080` and `18443`.
5. Sealed Secrets should be healthy before you apply any sealed credentials.
6. ArgoCD should be installed only after the base cluster is healthy, because the root application points to a private SSH Git URL and a pinned Git revision.

### GitOps bootstrap specifics

The root application at [gitops/clusters/local/root-application.yaml](./gitops/clusters/local/root-application.yaml):

- creates the `local-root` ArgoCD application in the `argocd` namespace
- points to `ssh://git@github.com/buenhyden/hy-home.k8s.git`
- pins `targetRevision` to a specific Git SHA
- recursively syncs manifests from `gitops/clusters/local/apps`
- enables `prune=true` and `selfHeal=true`

This means GitOps changes are deliberate and reproducible, but they are **not** “latest commit wins” by default. To advance GitOps state, update the pinned `targetRevision` intentionally.

## Project Structure

This repository is documentation-heavy by design. The cluster configuration, GitOps layout, and operating knowledge are kept separate on purpose.

```text
hy-home.k8s/
├── .agent/                 # Agent rules and workflows used by the repo's automation model
├── .claude/                # Shared instruction layer for agent-facing documentation
├── .github/                # CI workflow, issue templates, PR template, security policy
├── docs/
│   ├── adr/                # Architecture Decision Records
│   ├── ard/                # Architecture Reference Documents
│   ├── manuals/            # Process and collaboration manuals
│   ├── operations/         # Operational definitions and readiness docs
│   ├── plans/              # Execution plans
│   ├── prd/                # Product Requirements Documents
│   ├── runbooks/           # Executable operational procedures
│   └── specs/              # Technical specs and implementation plans
├── examples/               # Example materials and reference content
├── gitops/                 # ArgoCD applications and cluster reconciliation entrypoints
├── infrastructure/         # Vendored platform manifests and k3d cluster definitions
├── scripts/                # Reserved location for future utility automation
├── templates/              # Markdown templates for specs, runbooks, PRDs, ADRs, and guides
├── tests/                  # Global testing strategy and future cross-cutting suites
├── AGENTS.md               # Cross-agent root contract for repo work
├── ARCHITECTURE.md         # High-level architecture constraints
├── CONTRIBUTING.md         # Spec-first contribution rules
├── OPERATIONS.md           # Operations index
└── README.md               # Operator-facing entrypoint
```

## Architecture

### Spec-Driven Development

This repository treats documentation as an operational control surface, not a side artifact.

- [docs/specs/](./docs/specs/) defines the implementation source of truth for planned changes.
- [docs/adr/](./docs/adr/) records important architectural decisions.
- [docs/ard/](./docs/ard/) carries deeper reference designs and system structure.
- [docs/runbooks/](./docs/runbooks/) contains the executable steps used during bootstrap, troubleshooting, and recovery.

### Infrastructure vs. GitOps

The repository splits local platform responsibilities into two layers:

- **`infrastructure/`** contains the manifests and cluster definitions required to stand up the platform itself.
- **`gitops/`** contains the ArgoCD application layout used after the platform is healthy.

This split matters operationally:

- use `infrastructure/` to bootstrap the cluster and install controllers
- use `gitops/` when you want ArgoCD to become the reconciliation authority

### Local-only operational model

The supported operating model in this repository is:

1. WSL2 host with Docker Engine running inside Linux
2. k3d cluster using the dedicated `k3d-hy-k3d` bridge network
3. ingress exposed on `127.0.0.1:18080` and `127.0.0.1:18443`
4. ArgoCD accessed via `kubectl port-forward`, not via ingress

If you adapt this repository to a persistent remote cluster, treat that as a separate architecture decision and document it explicitly instead of assuming the current README applies unchanged.

## Configuration

This repository does **not** currently define a root `.env.example` or repo-wide environment variable contract for bootstrap. Configuration is expressed through:

- host prerequisites such as WSL2, `systemd`, Docker Engine, and optional GPU runtime support
- k3d cluster manifests under [infrastructure/k3d/](./infrastructure/k3d/)
- Kubernetes manifests under [infrastructure/](./infrastructure/)
- sealed Kubernetes secrets applied to the cluster when GitOps needs private repository access

### Host assumptions

| Area | Current expectation |
| --- | --- |
| WSL2 init | `/etc/wsl.conf` contains `systemd=true` for the default Docker-in-WSL workflow |
| Filesystem placement | Work from the Linux filesystem, for example `/home/hy/projects/...`, not `/mnt/c/...` |
| Docker network | `k3d-hy-k3d` exists with subnet `172.20.0.0/16` |
| MetalLB pool | [infrastructure/ipaddresspool.yaml](./infrastructure/ipaddresspool.yaml) advertises `172.20.0.100-172.20.0.150` |
| Ingress ports | k3d maps host `18080 -> 30080` and `18443 -> 30443` |
| ArgoCD access | local port-forward on `8080:443` |

## Verified Commands

Use these commands as the operator reference set. Each one is grounded in the repository or its runbooks.

| Command | Purpose |
| --- | --- |
| `docker network create --driver bridge --subnet 172.20.0.0/16 k3d-hy-k3d` | Create the dedicated bridge network required by MetalLB |
| `k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml` | Create the default multi-node local cluster |
| `k3d cluster create --config infrastructure/k3d/k3d-cluster.gpu.yaml` | Create the GPU-enabled cluster profile |
| `k3d cluster create --config infrastructure/k3d/k3d-min.yaml` | Create the minimal cluster profile |
| `kubectl apply -f infrastructure/metallb/metallb-native.yaml` | Install MetalLB |
| `kubectl apply -f infrastructure/ipaddresspool.yaml` | Register the local MetalLB address pool |
| `kubectl apply -f infrastructure/ingress-nginx/ingress-nginx.yaml` | Install ingress-nginx |
| `kubectl apply -f infrastructure/ingress-nginx/nodeport-service.yaml` | Expose ingress-nginx through the expected NodePorts |
| `kubectl apply -f infrastructure/sealed-secrets/sealed-secrets.yaml` | Install Sealed Secrets |
| `kubectl apply -f infrastructure/argocd/argocd-install.yaml` | Install ArgoCD for GitOps |
| `kubectl apply -f gitops/clusters/local/root-application.yaml` | Register the App-of-Apps root application |
| `kubectl -n argocd port-forward svc/argocd-server 8080:443` | Access the ArgoCD UI locally |
| `kubectl get nodes` | Confirm the cluster nodes are ready |
| `kubectl -n metallb-system get pods` | Verify MetalLB health |
| `kubectl -n ingress-nginx get pods` | Verify ingress-nginx health |
| `kubectl -n argocd get applications` | Verify GitOps application health |
| `curl -I http://127.0.0.1:18080/` | Confirm ingress reaches the local load balancer |

## Testing and Validation

### Current CI reality

The repository currently contains one verified GitHub Actions workflow at [.github/workflows/ci.yml](./.github/workflows/ci.yml). It runs `pre-commit` on pushes and pull requests targeting `main`.

That means the checked-in CI baseline currently verifies:

- repository checkout
- Python setup for `pre-commit`
- execution of configured pre-commit hooks

Do **not** assume this repository already runs a full automated infrastructure test matrix in CI. If you add those checks later, update this README to match the actual workflow files.

### Manual validation checklist

Run this checklist after bootstrap or after making cluster changes:

- [ ] `kubectl get nodes` shows the expected nodes in `Ready`
- [ ] `kubectl -n metallb-system get pods` shows MetalLB pods `Running`
- [ ] `kubectl -n ingress-nginx get pods` shows the ingress controller `Ready`
- [ ] `kubectl -n kube-system get pods -l name=sealed-secrets-controller` shows Sealed Secrets `Ready`
- [ ] `curl -I http://127.0.0.1:18080/` returns an HTTP response
- [ ] If GitOps is enabled, `kubectl -n argocd get pods` shows ArgoCD pods `Ready`
- [ ] If GitOps is enabled, `kubectl -n argocd get applications` shows expected applications and health states

### Test strategy references

- [tests/README.md](./tests/README.md) defines the repository-wide testing expectations and quality gates.
- [docs/specs/README.md](./docs/specs/README.md) explains why implementation work is expected to trace back to specs.

## Operations and Troubleshooting

Use the service runbooks for anything that changes infrastructure state or requires root-cause analysis.

| Problem area | Start here | Covers |
| --- | --- | --- |
| WSL2, Docker Engine, k3d lifecycle | [docs/runbooks/services/local-k3d-wsl2.md](./docs/runbooks/services/local-k3d-wsl2.md) | `systemd=true`, Docker daemon issues, port conflicts, MetalLB subnet mismatch, ingress not responding |
| ArgoCD bootstrap and reconciliation | [docs/runbooks/services/local-gitops-argocd.md](./docs/runbooks/services/local-gitops-argocd.md) | repo credential bootstrapping, root app sync, pinned `targetRevision` behavior |
| ArgoCD service access | [docs/runbooks/services/argocd-local.md](./docs/runbooks/services/argocd-local.md) | port-forward access, ArgoCD pod readiness, application visibility |
| Sealed Secrets | [docs/runbooks/services/sealed-secrets-local.md](./docs/runbooks/services/sealed-secrets-local.md) | controller health, re-sealing against the current certificate, generated Secret checks |

Common operator checks:

```bash
k3d cluster list
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
kubectl get events -A --sort-by=.lastTimestamp | tail -n 50
kubectl -n argocd get applications
kubectl -n ingress-nginx logs deploy/ingress-nginx-controller --tail=200
kubectl -n metallb-system logs deploy/controller --tail=200
```

## Contributing

This repository follows a spec-first contribution model.

1. Start with a specification in [docs/specs/](./docs/specs/).
2. Use the templates in [templates/](./templates/) for specs, ADRs, runbooks, and related project documents.
3. Follow the branch naming and Conventional Commit requirements in [CONTRIBUTING.md](./CONTRIBUTING.md).
4. Expect agent-assisted review against the repo’s documentation, QA, and security rules.

Read these files before contributing:

- [CONTRIBUTING.md](./CONTRIBUTING.md)
- [AGENTS.md](./AGENTS.md)
- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [OPERATIONS.md](./OPERATIONS.md)

## Further Reading

Use these references when the README is no longer deep enough:

- [infrastructure/README.md](./infrastructure/README.md) for the infrastructure component inventory
- [gitops/README.md](./gitops/README.md) for the GitOps layout and operating principles
- [docs/README.md](./docs/README.md) for the documentation map
- [docs/specs/README.md](./docs/specs/README.md) for the spec-driven workflow
- [docs/runbooks/README.md](./docs/runbooks/README.md) for runbook scope and expectations
- [scripts/README.md](./scripts/README.md) for the intended role of future automation scripts
- [tests/README.md](./tests/README.md) for the testing strategy

## License

This repository does not currently include a checked-in license file at the root. Do not assume the project is MIT-licensed until maintainers add a real root license file or document the intended license explicitly.
