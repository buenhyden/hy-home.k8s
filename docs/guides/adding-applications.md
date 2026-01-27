# Guide: Adding Applications

This guide explains how to deploy a new application to the `hy-home.k8s` cluster using the GitOps workflow.

## 1. Choose a Template

Navigate to [`apps/_templates/`](../../apps/_templates) and identify the template that fits your service type:

- `backend/`: For REST APIs, microservices, etc.
- `frontend/`: For React, Vue, or static web apps.

## 2. Copy the Template

Copy the desired template to a new directory in `apps/`:

```bash
# Example: Adding a new user-api
cp -r apps/_templates/backend apps/user-api
```

## 3. Customize Manifests

Search for placeholders in the copied directory and replace them with your application details.

### Key Placeholders

| Placeholder | Description | Example |
| :--- | :--- | :--- |
| `APP_NAME` | Unique name for your app | `user-api` |
| `REGISTRY` | Container registry URL | `ghcr.io/your-org` |
| `IMAGE_NAME` | Your image name | `user-api-service` |
| `TAG` | Image version tag | `v1.2.3` |
| `APP_PORT` | Port the container listens on | `8080` |

### Environment Overlays

Customize environment-specific settings in:

- `apps/user-api/overlays/dev/kustomization.yaml`
- `apps/user-api/overlays/prod/kustomization.yaml`

## 4. Register with ArgoCD

Create a new ArgoCD `Application` manifest in [`clusters/docker-desktop/applications/`](../../clusters/docker-desktop/applications/):

```bash
cp clusters/docker-desktop/applications/_app-template.yaml \
   clusters/docker-desktop/applications/user-api.yaml
```

Edit `user-api.yaml` to point to your app's overlay path:

```yaml
spec:
  source:
    path: apps/user-api/overlays/dev # or prod
```

## 5. Commit and Deploy

Push your changes to the main branch:

```bash
git add apps/user-api clusters/docker-desktop/applications/user-api.yaml
git commit -m "feat: add user-api application"
git push
```

ArgoCD will automatically detect the new application and start the deployment.

---

## 🛠️ Verification

1. **ArgoCD UI**: Visit the dashboard and check the sync status of `user-api`.
2. **Kubectl**:

   ```bash
   kubectl get pods -l app=user-api
   ```

3. **Logs**:

   ```bash
   kubectl logs -f -l app=user-api
   ```
