# Infrastructure: Service Mesh (Istio)

This project uses **Istio** as the core service mesh to provide mTLS, advanced traffic management, and deep observability.

## 🏗️ Architecture

- **Istiod**: The control plane managing certificates, configuration, and sidecar injection.
- **Envoy Sidecars**: Injected into every application pod to intercept and manage traffic.
- **Istio Ingress Gateway**: The dedicated entry point for external traffic to enter the mesh.

---

## 🔒 Security (mTLS)

Mutual TLS (mTLS) is enabled by default across the entire cluster.

- **PeerAuthentication**: Configured at the root to enforce `STRICT` mTLS mode.
- **Cert-Manager Integration**: Can be configured to use external CAs for signing Istio certificates.

---

## 🚦 Traffic Management

We use Istio's Custom Resource Definitions (CRDs) for routing:

### Virtual Services

Define how traffic should be routed to a destination.

- *Example*: Splitting traffic between `v1` and `v2` during a canary rollout.

### Destination Rules

Define policies that apply to traffic after routing has occurred.

- *Example*: Circuit breaking, load balancing pools, and outlier detection.

---

## 🌐 Ingress & Egress

- **Ingress**: External traffic hits the **LoadBalancer** (MetalLB), which routes it to the **Istio Ingress Gateway**.
- **Gateway Resource**: Defines the ports and protocols (HTTP/HTTPS) accepted by the gateway.
- **Service Entry**: Used to define DNS and routing for services *outside* of the mesh (e.g., external cloud databases).
