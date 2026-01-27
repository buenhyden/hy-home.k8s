# Storage Architecture

This guide covers how persistent storage is managed within the `hy-home.k8s` cluster.

## 1. Storage Classes

The cluster provides the following StorageClasses:

### `standard` (Default)

- **Provisioner**: `rancher.io/local-path` (Kind default) or `kubernetes.io/host-path`.
- **Behavior**: Creates a directory on the underlying node (the Docker container in Kind) and mounts it into the pod.
- **Reclaim Policy**: `Delete` (Data is lost when PVC is deleted).

## 2. Persistent Volume Claims (PVC)

Applications request storage via PVCs.

```yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: my-app-data
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

## 3. Storage Strategy for Stateful Sets

For stateful applications (databases, queues), we use `StatefulKey` controllers or Operators (like Postgres Operator) which manage the PVC templates automatically.

### Local Persistence

Since this is a Kind cluster:

- **Data Location**: `/var/local-path-provisioner/<pvc-name>` inside the Kind node container.
- **Host persistence**: To persist data across Kind cluster rebuilds, the Kind nodes must have Docker volumes mounted to these paths.

## 4. Backup & Restore

Currently, there is no automated Volume Snapshot integration (e.g., Velero) configured for the local environment. Data backup responsibility lies with the application level (e.g., specific `pg_dump` jobs) or backing up the mapped Host directories.
