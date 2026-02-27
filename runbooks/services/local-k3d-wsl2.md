# Service Runbook: Local k3d Cluster (WSL2)

*Target Directory: `runbooks/services/local-k3d-wsl2.md`*
*Note: This is strictly for operational context. It MUST follow the deterministic rules in `0381-runbooks-oncall.md`.*

---

## 1. Service Overview & Ownership

- **Description**: Local multi-node Kubernetes cluster (`hy-k3d`) for development/home workloads using `k3d` (k3s in Docker) on WSL2.
- **Owner Team**: hy (self-managed)
- **Primary Contact**: hy

## 2. Dependencies

| Dependency | Type | Impact if Down | Link to Runbook |
| ---------- | ---- | -------------- | --------------- |
| WSL2 (systemd enabled) | Platform | Docker Engine cannot run as a service | N/A |
| Docker Engine (inside WSL2) | Runtime | Cluster cannot start | N/A |
| k3d CLI | Tooling | Cluster lifecycle commands unavailable | N/A |
| kubectl | Tooling | Cluster access/verification unavailable | N/A |
| MetalLB | In-cluster | LoadBalancer external IPs not assigned | N/A |
| ingress-nginx | In-cluster | No ingress routing baseline | N/A |
| NVIDIA Container Toolkit (optional) | Runtime | GPU workloads cannot run | N/A |

## 3. Observability & Dashboards

- **Primary Dashboard**: N/A (local environment)
- **SLIs**:
  - `kubectl get nodes` reports 4 nodes `Ready`
  - `curl -I http://127.0.0.1:18080/` returns HTTP (2xx–4xx)
- **Useful commands**:
  - `k3d cluster list`
  - `docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'`
  - `kubectl -n metallb-system get pods`
  - `kubectl -n ingress-nginx get pods`
  - `kubectl get events -A --sort-by=.lastTimestamp | tail -n 50`

## 4. Alerts & Common Failures

### Scenario 0: First-time bootstrap (WSL2 + Docker Engine)

- **Symptoms**: You do not have a working Docker daemon inside WSL2.
- **Investigation Steps**:
  1. Confirm systemd enabled: `cat /etc/wsl.conf`
  2. Confirm Docker present: `docker --version`
- **Remediation Action**:
  - [ ] Enable systemd in `/etc/wsl.conf`:
    - Set:
      - `[boot]`
      - `systemd=true`
  - [ ] Restart WSL from Windows: `wsl.exe --shutdown`
  - [ ] Install Docker Engine (Ubuntu/Debian example): `sudo apt-get update && sudo apt-get install -y docker.io`
  - [ ] Enable Docker service: `sudo systemctl enable --now docker`
  - [ ] Add user to docker group: `sudo usermod -aG docker $USER` (then start a new shell)
  - [ ] Verify: `docker info`

### Scenario A: Docker daemon not running

- **Symptoms**: `docker info` fails; `k3d cluster create` fails immediately.
- **Investigation Steps**:
  1. `systemctl is-active docker`
  2. `journalctl -u docker --no-pager -n 200`
- **Remediation Action**:
  - [ ] Start Docker: `sudo systemctl start docker`
  - [ ] Enable on boot: `sudo systemctl enable docker`
  - [ ] Re-check: `docker info`

### Scenario B: Dedicated Docker network missing or wrong CIDR

- **Symptoms**: MetalLB address pool does not match container subnet; External IP assignment fails.
- **Investigation Steps**:
  1. `docker network inspect k3d-hy-k3d | rg -n 'Subnet|Gateway'`
- **Remediation Action**:
  - [ ] Create network: `docker network create --driver bridge --subnet 172.20.0.0/16 k3d-hy-k3d`
  - [ ] If the name exists with a different CIDR, delete/recreate only if safe: `docker network rm k3d-hy-k3d`

### Scenario C: Port conflict (6443/18080/18443 already in use)

- **Symptoms**: `k3d cluster create` fails; `bind: address already in use`.
- **Investigation Steps**:
  1. `ss -ltnp | rg '(:6443|:18080|:18443)\\b'`
- **Remediation Action**:
  - [ ] Stop the conflicting service (preferred), or adjust port mappings in `infrastructure/k3d/`.

### Scenario D: ingress-nginx not responding on `127.0.0.1:18080`

- **Symptoms**: Connection failure or 5xx from `curl`.
- **Investigation Steps**:
  1. `kubectl -n ingress-nginx get pods`
  2. `kubectl -n ingress-nginx get svc ingress-nginx-controller-nodeport -o wide`
  3. `kubectl -n ingress-nginx logs deploy/ingress-nginx-controller --tail=200`
- **Remediation Action**:
  - [ ] Re-apply manifests:
    - `kubectl apply -f infrastructure/ingress-nginx/ingress-nginx.yaml`
    - `kubectl apply -f infrastructure/ingress-nginx/nodeport-service.yaml`
  - [ ] Confirm k3d port mapping matches NodePorts in `infrastructure/k3d/k3d-cluster.yaml`.

### Scenario E: MetalLB External IP not assigned to LoadBalancer Services

- **Symptoms**: `EXTERNAL-IP` remains `<pending>`.
- **Investigation Steps**:
  1. `kubectl -n metallb-system get pods`
  2. `kubectl -n metallb-system get ipaddresspools,l2advertisements`
  3. `kubectl -n metallb-system logs deploy/controller --tail=200`
- **Remediation Action**:
  - [ ] Re-apply: `kubectl apply -f infrastructure/ipaddresspool.yaml`
  - [ ] Verify address range matches `k3d-hy-k3d` subnet.

## 5. Safe Rollback Procedure

- [ ] Delete the cluster: `k3d cluster delete hy-k3d`
- [ ] (Optional) Remove dedicated network: `docker network rm k3d-hy-k3d`

## 6. Data Safety Notes (If Stateful)

- This local cluster is intended for development and local experimentation. Do not treat it as a durable production store without adding backup/restore workflows.

## 7. Escalation Path

1. **Primary On-Call**: hy
2. **Secondary Escalation**: N/A
3. **Management Escalation (SEV-1)**: N/A

## 8. Verification Steps (Post-Fix)

- [ ] `kubectl get nodes` shows 4 nodes `Ready`
- [ ] `kubectl -n metallb-system get pods` all `Running`
- [ ] `kubectl -n ingress-nginx get pods` controller `Ready`
- [ ] `curl -I http://127.0.0.1:18080/` returns HTTP (2xx–4xx)
