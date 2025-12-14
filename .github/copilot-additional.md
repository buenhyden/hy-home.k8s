# 추가 예시 및 스크립트 (Copilot 추가 가이드)

## ArgoCD Application 예시

- Backend service 1 (apps/backend-service-1):

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: backend-service-1
  namespace: argocd
  annotations:
    argocd-image-updater.argoproj.io/image-list: myapp=buenhyden/service-1
    argocd-image-updater.argoproj.io/myapp.update-strategy: latest
    argocd-image-updater.argoproj.io/write-back-method: git
spec:
  source:
    repoURL: https://github.com/buenhyden/hy-home.service-1.git
    targetRevision: release
    path: apps/backend-service-1/overlays/dev
  destination:
    server: https://kubernetes.default.svc
    namespace: default
```

- Backend service 2 (apps/backend-service-2):
  - `repoURL`: <https://github.com/buenhyden/hy-home.service-2.git>
  - `targetRevision`: `release`
  - `path`: apps/backend-service-2/overlays/dev
  - Argo Image Updater 주석: `argocd-image-updater.argoproj.io/image-list: myapp=buenhyden/service-2`

- Frontend (apps/frontend):
  - `repoURL`: <https://github.com/buenhyden/hy-home.frontend.git>
  - `targetRevision`: `release`
  - `path`: apps/frontend/overlays/dev
  - Argo Image Updater 주석: `argocd-image-updater.argoproj.io/image-list: myapp=buenhyden/frontend`

## Quick setup script (요약)

```bash
# 1) Create kind cluster
cat > kind-config.yaml <<'EOF'
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
  - role: worker
EOF

kind create cluster --name desktop --config kind-config.yaml

# 2) Set routing
GATEWAY=$(docker network inspect infra_net --format "{{(index .IPAM.Config 0).Gateway}}")

docker exec -it desktop-control-plane ip route add 172.19.0.0/16 via $GATEWAY
# repeat for workers

# 3) Install ArgoCD
kubectl create namespace argocd || true
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 4) Apply root Application
kubectl apply -f clusters/docker-desktop/apps.yaml

# 5) Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

## CI/CD 예시: 이미지 빌드 → 푸시 → Git 업데이트 → ArgoCD 동기화

```bash
# Build & Push
docker build -t ghcr.io/buenhyden/service-1:v1.2.3 .
docker push ghcr.io/buenhyden/service-1:v1.2.3

# Update kustomize overlay (or rely on Argocd-image-updater)
cd apps/backend-service-1/overlays/dev
kustomize edit set image buenhyden/service-1=ghcr.io/buenhyden/service-1:v1.2.3

# Git commit
git add kustomization.yaml
git commit -m "chore: bump backend-service-1 to v1.2.3"
git push origin main

# Trigger sync (manual):
argocd app sync backend-service-1
```

---

위 파일은 Copilot/AI 에이전트가 자동화 작업을 수행할 때 유용한 예시 및 스크립트를 담고 있습니다. 필요하면 더 많은 예시나 자동화 스크립트(예: GitHub Actions)로 확장하겠습니다.
