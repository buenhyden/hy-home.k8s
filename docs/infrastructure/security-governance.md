# Infrastructure: Security & Governance

This document details the security layers and policy enforcement mechanisms within the `hy-home.k8s` platform.

## 🛡️ Policy Enforcement (Kyverno)

We use **Kyverno** as a Kubernetes-native policy engine to manage and enforce cluster-wide security standards without requiring custom admission controllers.

### Key Policies

- **Pod Security Admission**: Enforces the restricted profile (prevents root users, privileged containers).
- **Label Validation**: Ensures every deployment has the required `app.kubernetes.io/name` labels.
- **Image Provenance**: (Optional) Can be configured to verify image signatures using Cosign.

---

## 🔐 Automated Secrets (Sealed Secrets)

To maintain the GitOps principle of "everything in Git", we use **Bitnami Sealed Secrets**.

### Security Model

- **Public Key**: Located in the cluster, used by developers to encrypt secrets.
- **Private Key**: Encapsulated within the Sealed Secrets controller; never leaves the cluster.
- **Scoped Decryption**: Secrets are tied to specific namespaces and names to prevent cross-account decoding.

Refer to the [Secret Management Guide](../guides/secret-management.md) for operational commands.

---

## 📜 Certificate Lifecycle (Cert-Manager)

**Cert-Manager** automates the issuance and renewal of TLS certificates for internal and external services.

### Integration with Istio

Cert-manager is configured to:

1. Issue certificates for the **Istio Ingress Gateway**.
2. Provide the backing CA for internal service-to-service mTLS (optional, default is Istiod's self-signed CA).
3. Support both **ACME (Let's Encrypt)** for public domains and **Self-Signed** for local testing.

---

## 🚦 Network Security

- **mTLS**: Enforced by Istio `PeerAuthentication` on a whole-mesh basis.
- **Egress Control**: Strictly controlled via Istio `ServiceEntry`. By default, pods are restricted from making external requests unless explicit egress rules are defined.
