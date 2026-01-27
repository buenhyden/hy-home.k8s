# Infrastructure: External Services Integration

In a home lab environment, it is common to have persistent databases or services running as standard Docker containers or bare-metal instances outside of the Kubernetes cluster.

## 🔗 The Connectivity Pattern

We use the **Headless Service + Manual Endpoints** pattern to expose external services as if they were internal Kubernetes services.

### 1. Service Definition

A Service is created without a `selector`. This prevents Kubernetes from trying to manage endpoints automatically.

```yaml
kind: Service
metadata:
  name: postgres-external
spec:
  ports:
    - port: 5432
      targetPort: 5432
  clusterIP: None  # This is "Headless"
```

### 2. Endpoints Definition

We manually map the service name to an external IP address.

```yaml
kind: Endpoints
metadata:
  name: postgres-external
subsets:
  - addresses:
      - ip: 172.19.0.56  # The Host Docker IP
    ports:
      - port: 5432
```

---

## 📂 Managed External Services

The following connectors are maintained in [`infrastructure/external-services/`](../../infrastructure/external-services/):

| Service | Protocol | Default Port |
| :--- | :--- | :--- |
| **PostgreSQL** | TCP | 5432 |
| **Redis** | TCP | 6379 |
| **Kafka** | TCP/Bootstrap | 9092 |
| **OpenSearch** | HTTP/S | 9200 |

---

## 📡 Cross-Network Routing

The `hy-home.k8s` cluster runs on the `kind` network, while external Docker containers typically run on a separate bridge network.

### Route Injection

The bootstrap process injects static routes into the Kind nodes using `ip route`.

- **Cluster Side**: Kind Control/Worker nodes.
- **Host Side**: The Docker network gateway.

**Verification command:**

```bash
docker exec -it docker-desktop-control-plane ip route
```

You should see a route for `172.19.0.0/16` (or your specific host network) via the Docker bridge gateway.
