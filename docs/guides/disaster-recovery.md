# Disaster Recovery

This document outlines the procedures for recovering the `hy-home.k8s` platform in the event of partial or catastrophic failure.

## 1. The GitOps Model & Recovery

In this project, **Git is the single source of truth**. This means that recovering the cluster state (infrastructure, applications, configurations) is primarily achieved by re-synchronizing the cluster with the repository.

### Scenario A: Accidental Resource Deletion

If a Kubernetes resource (Deployment, Service, ConfigMap) is manually deleted:

- **Automatic Recovery**: ArgoCD is configured to self-heal. It will detect the configuration drift (missing resource) and automatically re-apply the manifest from Git.
- **Manual Recovery**: If auto-sync is disabled, click "Sync" in the ArgoCD UI.

### Scenario B: Total Cluster Failure

If the `docker-desktop` (Kind) cluster is corrupted or deleted:

1. **Delete the old cluster** (to ensure a clean slate):

   ```bash
   kind delete cluster --name hy-home
   ```

2. **Run the Bootstrap Process**:
   Follow the [Cluster Bootstrap](./cluster-bootstrap.md) guide.

   ```bash
   ./bootstrap/cluster-setup.sh
   ./bootstrap/argocd-install.sh
   ./bootstrap/root-apps.sh
   ```

3. **Restoration**: ArgoCD will pull the latest configuration from `main` and redeploy the entire stack.

## 2. Persistent Data Strategy

While the *configuration* is stateless, the *data* in persistent volumes (PVs) is not automatically recovered by GitOps.

### Local Environment (Kind)

In the current local development setup, PVs are backed by the host filesystem (docker volumes or bind mounts).

- **Risk**: Deleting the Docker container/volume deletes the data.
- **Backup**: Critical data directories should be mounted from known host paths if persistence across cluster rebuilds is required.

### External Services

For stateful services (Databases, etc.) running outside the cluster (on the Host machine):

- These are unaffected by cluster failure.
- Ensure regular backups of your external Postgres/Redis instances.

## 3. Secret Recovery

Secrets are managed via **Sealed Secrets**.

- **The Master Key**: The private key used by the Sealed Secrets controller to decrypt secrets is CRITICAL.
- **Backup Location**: The master key should be backed up securely (e.g., in a password manager or secure vault), distinct from the Git repository.
- **Restoration**: after a fresh bootstrap, you must restore the master key *before* ArgoCD tries to sync sealed secrets, otherwise decryption will fail.

```bash
# Example restoration command (if key is a file)
kubectl apply -f master-key-backup.yaml
# Restart controller to pick up new key
kubectl delete pod -n kube-system -l name=sealed-secrets-controller
```
