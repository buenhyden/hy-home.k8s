#!/usr/bin/env bash
set -euo pipefail

# Bootstrap ArgoCD repository access with SSH key and optional GitHub deploy key.
# Usage:
#   REPO_URL=git@github.com:owner/repo.git ./bootstrap-argocd-repo.sh
# Optional environment variables:
#   REPO_URL, KEY_FILE, ADD_GITHUB_DEPLOY_KEY, GITHUB_REPO (owner/repo), GITHUB_TOKEN

REPO_URL=${REPO_URL:-}
KEY_FILE=${KEY_FILE:-./id_rsa}
ADD_GITHUB_DEPLOY_KEY=${ADD_GITHUB_DEPLOY_KEY:-false}
GITHUB_REPO=${GITHUB_REPO:-}
GITHUB_TOKEN=${GITHUB_TOKEN:-}

# SealedSecret and kubeseal options
CREATE_SEALED_SECRET=${CREATE_SEALED_SECRET:-false}
SEALED_SECRET_FILE=${SEALED_SECRET_FILE:-./clusters/docker-desktop/argocd-git-ssh-sealedsecret.yaml}
APPLY_SEALED=${APPLY_SEALED:-false}
SKIP_CREATE_SECRET=${SKIP_CREATE_SECRET:-false}
KUBESEAL_CONTROLLER_NAME=${KUBESEAL_CONTROLLER_NAME:-sealed-secrets}
KUBESEAL_CONTROLLER_NAMESPACE=${KUBESEAL_CONTROLLER_NAMESPACE:-kube-system}

if [ -z "$REPO_URL" ]; then
  echo "REPO_URL must be set" >&2
  echo "Usage: REPO_URL=git@github.com:owner/repo.git ./bootstrap-argocd-repo.sh" >&2
  exit 1
fi

if [ ! -f "$KEY_FILE" ]; then
  echo "Generating SSH key: $KEY_FILE"
  ssh-keygen -t rsa -b 4096 -f "$KEY_FILE" -N ""
fi

PUBLIC_KEY_FILE=${KEY_FILE}.pub
PUB_KEY_CONTENT=$(cat "$PUBLIC_KEY_FILE")

if [ "$SKIP_CREATE_SECRET" != "true" ]; then
  echo "Create Kubernetes secret in argocd namespace from private key"
  kubectl -n argocd create secret generic argocd-git-ssh --from-file=sshPrivateKey="$KEY_FILE" --dry-run=client -o yaml | kubectl apply -f -
else
  echo "SKIP_CREATE_SECRET=true set. Not creating plain Kubernetes secret in cluster."
fi

# If requested generate a SealedSecret YAML using kubeseal and optionally apply it
if [ "$CREATE_SEALED_SECRET" = "true" ]; then
  TMP_SECRET_FILE="/tmp/argocd-git-ssh-secret.yaml"
  echo "Generating dry-run secret YAML for sealing: $TMP_SECRET_FILE"
  kubectl -n argocd create secret generic argocd-git-ssh --from-file=sshPrivateKey="$KEY_FILE" --dry-run=client -o yaml > "$TMP_SECRET_FILE"

  if command -v kubeseal >/dev/null 2>&1; then
    echo "kubeseal found — creating SealedSecret ($SEALED_SECRET_FILE) using controller $KUBESEAL_CONTROLLER_NAME in namespace $KUBESEAL_CONTROLLER_NAMESPACE"
    set +e
    kubeseal --controller-name="$KUBESEAL_CONTROLLER_NAME" --controller-namespace="$KUBESEAL_CONTROLLER_NAMESPACE" --format=yaml < "$TMP_SECRET_FILE" > "$SEALED_SECRET_FILE"
    KUBESEAL_EXIT=$?
    set -e
    if [ $KUBESEAL_EXIT -ne 0 ]; then
      echo "kubeseal failed to create sealed secret (exit=$KUBESEAL_EXIT). You may need to run kubeseal with --cert or verify the sealed-secrets controller and access." >&2
    else
      echo "SealedSecret written to: $SEALED_SECRET_FILE"
      if [ "$APPLY_SEALED" = "true" ]; then
        echo "Applying SealedSecret to cluster ($SEALED_SECRET_FILE)"
        kubectl apply -f "$SEALED_SECRET_FILE"
      fi
    fi
  else
    echo "kubeseal not found. Install kubeseal to generate SealedSecret automatically. Skipping SealedSecret generation." >&2
    echo "You can run: kubectl -n argocd create secret generic argocd-git-ssh --from-file=sshPrivateKey=$KEY_FILE --dry-run=client -o yaml | kubeseal --controller-name=$KUBESEAL_CONTROLLER_NAME --controller-namespace=$KUBESEAL_CONTROLLER_NAMESPACE -o yaml > $SEALED_SECRET_FILE"
  fi
fi

echo "Add repo to ArgoCD (requires argocd CLI and access to the ArgoCD server)"
if command -v argocd >/dev/null 2>&1; then
  echo "Adding repo to ArgoCD using SSH private key"
  argocd repo add "$REPO_URL" --ssh-private-key-path "$KEY_FILE" || true
else
  echo "argocd CLI not found; skipping CLI repo add. You can 'argocd repo add $REPO_URL --ssh-private-key-path $KEY_FILE' manually."
fi

if [ "$ADD_GITHUB_DEPLOY_KEY" = "true" ] && [ -n "$GITHUB_REPO" ] && [ -n "$GITHUB_TOKEN" ]; then
  echo "Adding deploy key to GitHub repository $GITHUB_REPO"
  if ! command -v gh >/dev/null 2>&1; then
    echo "gh CLI not found; attempt using GitHub API"
    curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github+json" \
      https://api.github.com/repos/$GITHUB_REPO/keys -d "{\"title\": \"argocd-deploy-key\",\"key\": \"$PUB_KEY_CONTENT\", \"read_only\": false }" || true
  else
    echo "$PUB_KEY_CONTENT" | gh api repos/$GITHUB_REPO/keys --method POST -F title='argocd-deploy-key' -F key="@$PUBLIC_KEY_FILE" -F read_only=false || true
  fi
fi

echo "Done. Public key (for Git host):"
echo "$PUB_KEY_CONTENT"
