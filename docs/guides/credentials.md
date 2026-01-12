# Credentials and Secrets Guide

This repository uses GitHub Actions, ArgoCD, and Argo Image Updater. For automation and secure operations, configure the following secrets and credentials in your environment.

## GitHub Actions Secrets (repository or organization level)

- `GHCR_TOKEN` (recommended): Personal access token or GitHub Actions `GITHUB_TOKEN` for GHCR. Required for pushing images to `ghcr.io`. If using `GITHUB_TOKEN`, ensure repository permissions include `packages: write`.
- `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` (optional): If using Docker Hub for image pushes.
- `ARGOCD_SERVER`: ArgoCD API server URL, e.g. `argocd.example.local:443` or internal cluster address.
- `ARGOCD_USERNAME` / `ARGOCD_PASSWORD` or `ARGOCD_TOKEN`: Credentials to call the ArgoCD API (used to trigger sync from workflows). Prefer using a dedicated automation account or token with minimal permission.

## ArgoCD Credentials for write-back and Image Updater

### Git write-back

- `argocd-image-updater` can commit updated image tags back to Git. To allow write-back, configure repository credentials for ArgoCD:
  1. Use `argocd repo add <git-url> --username <user> --password <token>` to let ArgoCD access and update the repo, OR
  2. Create a Kubernetes secret containing SSH keys or HTTP credentials and reference it in ArgoCD repository configuration (recommended: SSH).
  3. Confirm Argo Image Updater is configured with `write-back-method: git` in your Application annotations.

### SSH-based repository credentials (recommended for write-back)

- Do not commit private keys into Git. Instead:
  1. Generate an SSH key pair: `ssh-keygen -t rsa -b 4096 -f ./id_rsa -N ''`
  2. Add the public key to the Git provider (GitHub/Bitbucket) as a deploy key with write access.
  3. Create a Kubernetes secret in the `argocd` namespace locally:

```bash
kubectl -n argocd create secret generic argocd-git-ssh --from-file=sshPrivateKey=./id_rsa
```

- Or use Sealed Secrets to store the private key safely in Git. Example sealedsecret template exists at `clusters/docker-desktop/argocd-git-ssh-sealedsecret-template.yaml` (create locally and use `kubeseal` to generate the encrypted YAML), or use `sops` with `clusters/docker-desktop/argocd-git-ssh-sops-template.yaml` to encrypt via SOPS.

- You can also add the repository to ArgoCD using the CLI with the SSH key:

```bash
argocd repo add git@github.com:buenhyden/hy-home.k8s.git --ssh-private-key-path ./id_rsa
```

- If ArgoCD runs in a cluster without direct network access to the Git provider, use a bastion or deploy-key proxy as needed.

- A convenience bootstrap helper script is available at `clusters/docker-desktop/scripts/bootstrap-argocd-repo.sh` to generate keys, create the `argocd` secret locally, optionally add a GitHub deploy key, and add the repo to ArgoCD via the `argocd` CLI.

### SealedSecret 자동 생성 예시

`bootstrap-argocd-repo.sh`에 `CREATE_SEALED_SECRET` 옵션을 설정하면 `kubeseal`을 사용해 SealedSecret YAML을 자동으로 생성합니다. 사용 예시:

```bash
REPO_URL=git@github.com:owner/repo.git \
CREATE_SEALED_SECRET=true \
SEALED_SECRET_FILE=clusters/docker-desktop/argocd-git-ssh-sealedsecret.yaml \
APPLY_SEALED=false \
./clusters/docker-desktop/scripts/bootstrap-argocd-repo.sh
```

- `CREATE_SEALED_SECRET=true` : SealedSecret YAML을 생성합니다.
- `SEALED_SECRET_FILE` : SealedSecret 출력 경로(디폴트: `./clusters/docker-desktop/argocd-git-ssh-sealedsecret.yaml`).
- `APPLY_SEALED=true` : 생성된 SealedSecret을 클러스터에 적용합니다 (컨트롤러에 의해 Secret이 자동으로 생성됩니다).
- `SKIP_CREATE_SECRET=true` : Plain Secret(암호 해제 가능한)을 클러스터에 생성하지 않으려면 이 옵션을 사용하세요.

kubeseal이 설치되어 있지 않거나 클러스터의 SealedSecrets 컨트롤러에 접근할 수 없으면, 다음 명령으로 수동으로 SealedSecret을 생성할 수도 있습니다:

```bash
kubectl -n argocd create secret generic argocd-git-ssh --from-file=sshPrivateKey=./id_rsa --dry-run=client -o yaml > argocd-git-ssh-secret.yaml
kubeseal --controller-name=sealed-secrets --controller-namespace=kube-system --format=yaml < argocd-git-ssh-secret.yaml > argocd-git-ssh-sealedsecret.yaml
```

또는 `kubeseal`이 컨트롤러에 접근할 수 없다면 공개 키 기반 sealing도 가능합니다:

```bash
kubeseal --cert sealed-secrets-controller.crt --format yaml < argocd-git-ssh-secret.yaml > argocd-git-ssh-sealedsecret.yaml
```

### Registry access

- Argo Image Updater only needs read access to find latest tags, and optionally push only if custom behavior exists. Provide a registry token via:
  - `argocd-image-updater` configuration (see upstream docs) or
  - set environment/secret inside the Argo CD namespace for the image-updater.

## ArgoCD automation token best practice

- Create a dedicated ArgoCD service account (or user) with token: `argocd account generate-token --account <automation-account>`.
- Grant minimal necessary permissions using ArgoCD RBAC (avoid using `admin` credentials in CI).
- Store server and token as GitHub Actions secrets: `ARGOCD_SERVER` and `ARGOCD_TOKEN`.

## Example GitHub Actions settings

1. In repository Settings → Secrets → Actions, add:
   - `GHCR_TOKEN` — PAT with `packages: write` permission.
   - `ARGOCD_SERVER`, `ARGOCD_USERNAME`, `ARGOCD_PASSWORD` or `ARGOCD_TOKEN`.
2. Use secrets from workflows to log in to registries and run ArgoCD commands securely.

## Notes and references

- Argo Image Updater docs: <https://argocd-image-updater.readthedocs.io/en/stable/>
- ArgoCD repo credentials docs: <https://argo-cd.readthedocs.io/en/stable/user-guide/private-repositories/>
- GHCR token scopes: `write:packages` when pushing images; prefer `repo` and `packages` as-needed.

If you'd like, I can add a sample `kubectl` manifest to create an `argocd` repo secret for write-back, or create a GitHub Actions secret configuration checklist as an artifact.
