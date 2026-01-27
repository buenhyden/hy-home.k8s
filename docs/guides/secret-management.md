# Guide: Secret Management

In a GitOps workflow, all cluster configurations are kept in Git. To prevent sensitive data (passwords, API keys) from being exposed, we use **Sealed Secrets**.

## 🛡️ How It Works

1. **Bitnami Sealed Secrets** controller is installed in the cluster.
2. Developers encrypt a regular Kubernetes `Secret` using the `kubeseal` CLI.
3. The resulting `SealedSecret` (encrypted) is safe to commit to Git.
4. The controller in the cluster decrypts it back into a standard `Secret`.

---

## 🛠️ Usage

### 1. Install kubeseal CLI

Follow the instructions for your OS on the [Sealed Secrets GitHub](https://github.com/bitnami-labs/sealed-secrets#kubeseal).

### 2. Create a Sealed Secret

First, create a regular secret locally (do NOT commit this file):

```bash
kubectl create secret generic my-api-secret \
  --from-literal=API_KEY=super-secret-value \
  --namespace default \
  --dry-run=client -o yaml > secret.yaml
```

Encrypt the secret using `kubeseal`:

```bash
kubeseal --format=yaml < secret.yaml > apps/my-api/base/sealed-secrets.yaml
```

### 3. Commit to Git

Now you can safely commit the `SealedSecret`:

```bash
git add apps/my-api/base/sealed-secrets.yaml
git commit -m "docs: add encrypted secrets for my-api"
git push
```

---

## 🏗️ Managing Cluster-Wide Secrets

For repository-wide configurations like Git SSH keys, follow the templates in:
[`clusters/docker-desktop/`](../../clusters/docker-desktop/)

Example:

```bash
# Encrypt Git SSH key for ArgoCD
kubectl create secret generic argocd-repo-key \
  --from-file=ssh-privatekey=~/.ssh/id_ed25519 \
  -n argocd --dry-run=client -o yaml | \
  kubeseal -o yaml > clusters/docker-desktop/argocd-git-ssh-sealedsecret.yaml
```

---

## ⚠️ Best Practices

- **Never** commit unencrypted `Secret` YAMLs.
- Always include the `--namespace` flag when sealing secrets, as they are namespace-bound by default.
- Use distinct sealed secrets per application to minimize the blast radius.
