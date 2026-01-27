# Security Policy

This document defines the security posture and enforcement mechanisms for the `hy-home.k8s` platform.

## 1. Governance Engine: Kyverno

We use **Kyverno** as the Policy Admission Controller. It validates (and sometimes mutates) resources before they enter the cluster.

### Active Policies

- **Require Labels**: All Deployments must have standard labels (owner, team, cost-center).
- **Disallow `latest` Tag**: Production images must use specific tags or SHA digests.
- **Enforce Probes**: All Pods must have Liveness/Readiness probes.
- **Restrict HostPath**: Only specific infrastructure components can mount HostPaths.

## 2. Network Security

### Network Logic

- **CNI**: Kindnet (default) - rudimentary.
- **Service Mesh**: Istio - provides mTLS.
  - **PeerAuthentication**: `STRICT` mode is preferred for the mesh.
  - **AuthorizationPolicy**: Used to define who can talk to whom within the mesh.

### Ingress

All external access must go through the **Istio Ingress Gateway**. No internal Services should be exposed as `LoadBalancer` directly unless they are infrastructure components (Cost of MetalLB IPs, Security Surface).

## 3. RBAC (Role-Based Access Control)

- **Least Privilege**: Users/ServiceAccounts should only have the permissions they absolutely need.
- **ClusterAdmin**: Reserved for the Bootstrap process and critical break-glass scenarios.
- **Developers**: Should have limited rights within their `Namespace`.

## 4. Secret Management

- **Encryption at Rest**: Secrets in Git are ENCRYPTED using Sealed Secrets.
- **No Plaintext**: Never commit a `Secret` kind with `data` or `stringData` to the repository.
- **Secret Rotation**: Rotate API keys and database credentials periodically using the maintenance workflow.
