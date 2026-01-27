# Maintenance & Upgrades

## 1. Upgrading Kubernetes Versions

Since we use `kind`, upgrading Kubernetes means destroying and recreating the node containers.

1. **Backup Data**: Ensure all HostPath volumes are safe.
2. **Update Config**: Change the image version in `kind-config.yaml` or the bootstrap script.

    ```bash
    # Example: Update from v1.29.0 to v1.30.0
    kind create cluster --image kindest/node:v1.30.0
    ```

3. **Re-Bootstrap**: Run the full bootstrap process.

## 2. Upgrading ArgoCD

ArgoCD manages itself (if using a declarative setup), OR it is managed by the `argocd-install.sh` script.

- **Check Version**: Look at `bootstrap/argocd-install.sh`.
- **Update**: Change the URL to the newer manifest version.
- **Apply**: Run `kubectl apply -f <new-url> -n argocd`.

## 3. Upgrading System Components (Helm)

Most system components (Istio, Prometheus, etc.) are installed via Helm Charts managed by ArgoCD.

1. **Find the Application**: Locate the specific `Application` manifest in `infrastructure/`.
2. **Update Version**: Change `targetRevision` (chart version).
3. **Commit**: Push to Git. ArgoCD will upgrade the release.

## 4. Sealed Secrets Key Rotation

If the master key is compromised:

1. **Generate New Key**: Restart the controller triggers new key gen (if auto-rotate is on).
2. **Re-encrypt**: YOU MUST re-encrypt ALL secrets in the repo with the new public key.
    - `kubeseal --re-encrypt < existing-secret.yaml > new-secret.yaml`
3. **Commit**: Push new secrets.
