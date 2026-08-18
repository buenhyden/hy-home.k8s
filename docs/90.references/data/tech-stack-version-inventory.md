---
title: 'Reference: Tech Stack Version Inventory'
type: content/reference
status: active
owner: platform
updated: 2026-07-30
---

# Tech Stack Version Inventory

## Overview

이 문서는 일반 참고 링크 모음이 아니라 검증 대상 버전 계약 인벤토리다. repo-backed manifest, GitHub Actions, pre-commit hook, cloud example snapshot의 기준 값을 한곳에서 추적한다.

### Purpose

이 문서는 `hy-home.k8s`의 repo-backed 매니페스트와 품질 게이트에서 읽어야 하는 버전 기준을 고정한다.
새 버전으로 올릴 때는 실제 manifest/config와 이 문서를 같은 변경으로 수정한다.

## Reference Type

- Type: version-contract-inventory / external-standard-snapshot
- Source checked: 2026-07-30
- Refresh trigger: repo manifest/config version bump, GitHub Actions/pre-commit pin change, cloud example target update, or official provider support range change.

## Authority Boundary

- **Authoritative for**:
  - Repo-backed version contract values listed in `Version Contracts`.
  - AWS/Azure example snapshot values used by `examples/aws` and `examples/azure`.
  - Ingress NGINX cloud-target warning context recorded on 2026-05-09.
- **Not authoritative for**:
  - Live cluster upgrade execution.
  - Cloud account deployment procedure.
  - Product requirements, architecture decisions, implementation plans, or runbooks.
  - Dependency updates that were not applied to the corresponding repo files.

## Scope

- repo-backed k3s/Helm chart/GitHub Actions/pre-commit 버전 계약
- `examples/aws`, `examples/azure`를 갱신할 때 사용한 공식 cloud example snapshot
- 버전 drift 검증과 README/docs 설명을 맞추기 위한 기준값
- 실제 cloud provider 계정 변경, live cluster upgrade, 자동 dependency bump는 제외한다.

## Definitions / Facts

- **Version Contracts**: 아래 YAML 블록의 값이며 repo manifest/config와 함께 검증되는 기준이다.
- **Cloud Example Snapshot**: AWS/Azure 예시와 upstream Kubernetes awareness를 재확인한 2026-05-22 기준 공식 지원 상태다.
- **Ingress NGINX boundary**: 로컬 k3d 계약은 유지하되 cloud target은 ALB/Gateway API/AGC 경로로 분리한다.

### Cloud Example Snapshot: 2026-05-22

이 섹션은 `examples/aws`와 `examples/azure`의 참조 구현을 검토할 때 사용하는 공식 기준이다. 로컬 k3d 실행 계약은 아래 `Version Contracts`의 `rancher/k3s:v1.35.0-k3s1`을 따른다. 이 snapshot은 freshness 기록이며 자동 upgrade 지시가 아니다.

| Area                        | Repo example target                                 | Official basis                                                                                      | Note                                                                                                                                                  |
| --------------------------- | --------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Kubernetes upstream         | 1.36 latest release awareness, 1.35 patch awareness | [Kubernetes releases](https://kubernetes.io/releases/)                                              | 2026-05-22 기준 active branches는 1.36/1.35/1.34이며, 최신 patch는 1.36.1과 1.35.5다. 로컬 k3d와 cloud managed cluster target을 자동 변경하지 않는다. |
| AWS EKS                     | 1.35 target, standard support set 1.35/1.34/1.33    | [AWS EKS versions](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html)       | `examples/aws/terraform`은 EKS 1.35 참조 구현으로 유지한다. EKS 1.35 standard support는 2027-03-27까지다.                                             |
| Azure AKS                   | 1.35 target                                         | [AKS supported versions](https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions) | `examples/azure/infrastructure`의 기본 AKS version과 docs target을 맞춘다. AKS 1.36 availability는 awareness only다.                                  |
| Terraform AWS provider      | `>= 6.28, < 7.0`                                    | [Terraform AWS provider](https://registry.terraform.io/providers/hashicorp/aws/latest)              | 2026-05-22 기준 latest는 6.46.0이며 현재 constraint가 허용한다. provider major drift는 피한다.                                                        |
| Terraform EKS module        | `21.20.0`                                           | [EKS module](https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/latest)            | 2026-05-22 기준 latest와 일치한다. EKS 1.35 target은 유지한다.                                                                                        |
| Terraform VPC module        | `6.6.1`                                             | [VPC module](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws)                   | 2026-05-22 기준 latest와 일치한다. AWS network example 기준이다.                                                                                      |
| Terraform RDS Aurora module | `10.2.0`                                            | [RDS Aurora module](https://registry.terraform.io/modules/terraform-aws-modules/rds-aurora/aws)     | 2026-05-22 기준 latest와 일치한다. Aurora Serverless v2 example 기준이다.                                                                             |
| Ingress NGINX               | Retired upstream since 2026-03-24                   | [Ingress NGINX retirement](https://kubernetes.io/blog/2026/01/29/ingress-nginx-statement/)          | 로컬 k3d 계약은 문서상 경고로 유지하고 cloud target은 ALB/Gateway API/AGC로 분리한다.                                                                 |

### Version Contracts

```yaml
# 이 핀은 의도적으로 유지한다. v1.35.7-k3s1 로의 이동은 Kubernetes 기준으로는 patch 7개지만,
# k3s 번들이 함께 올리는 구성요소는 patch가 아니다: containerd v2.1.5 -> v2.2.5, flannel
# v0.27.4 -> v0.28.4, coredns v1.13.1 -> v1.14.6, metrics-server v0.8.0 -> v0.9.0, kine
# v0.14.9 -> v0.16.3 (minor), 그리고 traefik v3.5.1 -> v3.7.8 (--disable=traefik 이므로 무관).
# 즉 버전 문자열이 변경 규모를 실제보다 작게 보이게 한다. 특히 flannel minor는 Istio CNI가
# conflist를 체이닝하는 바로 그 표면이며, 그 도입은 아직 live 검증되지 않았다(ADR 0025).
# 순서: Istio CNI의 Baseline warning 채널이 깨끗하게 확인된 뒤에 이 핀을 올린다.
# k3d에는 upgrade 명령이 없어 이 값의 변경은 delete-and-recreate를 의미한다. 매니페스트
# 편집이 아니라 운영 절차이며, 현재 저장소에는 그 재생성 절차 문서가 없다.
k3s_image: 'rancher/k3s:v1.35.0-k3s1'
# k3s_image를 실행하는 도구 자체의 계약이다. 저장소는 k3s 이미지를 핀하면서 그것을 구동하는
# k3d 바이너리는 `bootstrap-local.sh`에서 "명령이 존재하는가"만 확인해 왔다.
# 최소 버전은 선언하지 않는다. 근거가 없기 때문이다. 확인된 사실은 관측된 조합 하나뿐이다.
k3d_cli:
  observed: 'v5.8.3'
  observedOn: '2026-08-18'
  observedDefaultK3s: 'v1.31.5-k3s1'
  upstreamLatest: 'v5.9.0'
  note: 'k3d가 내장한 기본 k3s(v1.31.5-k3s1)보다 4개 마이너 앞선 v1.35.0-k3s1을 실제로 구동 중이므로, 기본값과의 격차 자체는 차단 요인이 아니다. 내장 기본값은 image를 명시하면 참조되지 않는다. v5.9.0은 cluster restart를 추가했을 뿐 upgrade 경로를 추가하지 않았다.'
# GitOps 매니페스트가 이미지 태그로 직접 핀하는 워크로드다. Helm 차트를 거치지 않으므로
# helm_charts 계약이 덮지 않는다. bootstrap_helm_charts와 같은 부류의 경계 구멍이었다.
workload_images:
  kube-state-metrics:
    image: 'registry.k8s.io/kube-state-metrics/kube-state-metrics'
    version: 'v2.19.1'
    declaredBy: 'gitops/platform/monitoring/kube-state-metrics.yaml'
    note: 'ClusterRole은 이 버전의 DefaultResources 28개와 정확히 일치해야 한다. 버전을 올릴 때 pkg/options/resource.go 를 함께 확인한다.'
  grafana-alloy:
    image: 'docker.io/grafana/alloy'
    version: 'v1.18.1'
    declaredBy: 'gitops/platform/monitoring/alloy-k8s-logs.yaml'
    note: 'v1.13.1에서 올렸다. 이 워크로드가 쓰는 컴포넌트는 loki.source.kubernetes / loki.source.kubernetes_events / loki.process(stage.static_labels) / loki.write / discovery.* 뿐이며, v1.14.0~v1.18.1의 breaking change는 모두 otelcol.* 와 loki.secretfilter 에만 있다. 버전을 올릴 때 CHANGELOG의 breaking change가 이 컴포넌트 목록에 걸리는지 확인한다.'
  adminer:
    image: 'adminer'
    version: '4.8.1'
    declaredBy: 'gitops/workloads/adminer/rollout.yaml'
    note: '업그레이드 이연. 공식 이미지 라인은 4(adminer 4.17.1)와 5(adminer 5.5.1)뿐이며 6.x 이미지는 없다.'
# bootstrap 단계에서 GitOps 소유권 확립 이전에 helm으로 직접 설치하는 chart다.
# `infrastructure/bootstrap-local.sh`의 `--version` 값과 반드시 일치해야 한다.
bootstrap_helm_charts:
  metallb:
    repoURL: 'https://metallb.github.io/metallb'
    chart: 'metallb'
    version: '0.16.1'
    appVersion: 'v0.16.1'
    installedBy: 'infrastructure/bootstrap-local.sh [5/11]'
  argo-cd:
    repoURL: 'https://argoproj.github.io/argo-helm'
    chart: 'argo-cd'
    version: '10.4.0'
    appVersion: 'v3.5.1'
    installedBy: 'infrastructure/bootstrap-local.sh [8/11]'
helm_charts:
  platform-cert-manager:
    repoURL: 'https://charts.jetstack.io'
    chart: 'cert-manager'
    targetRevision: 'v1.17.2'
  platform-external-secrets-operator:
    repoURL: 'https://charts.external-secrets.io'
    chart: 'external-secrets'
    targetRevision: '0.14.4'
  platform-headlamp:
    repoURL: 'https://kubernetes-sigs.github.io/headlamp/'
    chart: 'headlamp'
    targetRevision: '0.41.0'
  platform-ingress-nginx:
    repoURL: 'https://kubernetes.github.io/ingress-nginx'
    chart: 'ingress-nginx'
    targetRevision: '4.12.0'
  platform-istio-base:
    repoURL: 'https://istio-release.storage.googleapis.com/charts'
    chart: 'base'
    targetRevision: '1.25.2'
  # cni는 istiod와 반드시 같은 버전 라인을 유지한다. Istio는 1.x-1 ~ 1.x+1 호환을
  # 문서화하지만, 이 저장소는 두 값을 함께 올려 드리프트를 만들지 않는다.
  platform-istio-cni:
    repoURL: 'https://istio-release.storage.googleapis.com/charts'
    chart: 'cni'
    targetRevision: '1.25.2'
  platform-istiod:
    repoURL: 'https://istio-release.storage.googleapis.com/charts'
    chart: 'istiod'
    targetRevision: '1.25.2'
  platform-kiali:
    repoURL: 'https://kiali.org/helm-charts'
    chart: 'kiali-operator'
    targetRevision: '2.10.0'
  platform-rollouts:
    repoURL: 'https://argoproj.github.io/argo-helm'
    chart: 'argo-rollouts'
    targetRevision: '2.40.9'
ci_python: '3.12'
ci_python_dependencies:
  jsonschema: '4.26.0'
  pre-commit: '4.6.1'
  PyYAML: '6.0.3'
ci_python_lock:
  lane: 'linux-cpython-3.12'
  input: '.github/requirements/ci-validation.in'
  lock: '.github/requirements/ci-validation.txt'
  sha256: '6d0685e84a4fb19b24e44c5ae965f16d7215e8608b210cbf0559d4a203a9cc13' # pragma: allowlist secret
  resolved_packages: 16
ci_gitleaks:
  version: '8.30.0'
  asset: 'gitleaks_8.30.0_linux_x64.tar.gz'
  sha256: '79a3ab579b53f71efd634f3aaf7e04a0fa0cf206b7ed434638d1547a2470a66e' # pragma: allowlist secret
  install_path: '/usr/local/bin/gitleaks'
github_actions:
  'actions/checkout': '3d3c42e5aac5ba805825da76410c181273ba90b1' # pragma: allowlist secret
  'actions/first-interaction': '1c4688942c71f71d4f5502a26ea67c331730fa4d' # pragma: allowlist secret
  'actions/labeler': 'bf12e9b00b37c5c0ca2b87b79b2daf7891dbda13' # pragma: allowlist secret
  'actions/setup-python': '5fda3b95a4ea91299a34e894583c3862153e4b97' # pragma: allowlist secret
  'actions/stale': '1e223db275d687790206a7acac4d1a11bd6fe629' # pragma: allowlist secret
  'actions/upload-artifact': '043fb46d1a93c77aae656e7c1c64a875d1fc6a0a' # pragma: allowlist secret
  'orhun/git-cliff-action': 'f50e11560dce63f7c33227798f90b924471a88b5' # pragma: allowlist secret
pre_commit:
  'https://github.com/commitizen-tools/commitizen': 'efb1a7dc7a81934ff473100ae3a5a716f3022534' # pragma: allowlist secret
  'https://github.com/pre-commit/pre-commit-hooks': '3e8a8703264a2f4a69428a0aa4dcb512790b2c8c' # pragma: allowlist secret
  'https://github.com/gitleaks/gitleaks': '6eaad039603a4de39fddd1cf5f727391efe9974e' # pragma: allowlist secret
  'https://github.com/Yelp/detect-secrets': '01886c8a910c64595c47f186ca1ffc0b77fa5458' # pragma: allowlist secret
  'https://github.com/DavidAnson/markdownlint-cli2': '996abf60411a8d954288ac9856aae7602b80cbda' # pragma: allowlist secret
  'https://github.com/python-jsonschema/check-jsonschema': 'f805888065fdb6162e1f800e50bb9460cbd223d6' # pragma: allowlist secret
  'https://github.com/shellcheck-py/shellcheck-py': '745eface02aef23e168a8afb6b5737818efbea95' # pragma: allowlist secret
  'https://github.com/scop/pre-commit-shfmt': '05c1426671b9237fb5e1444dd63aa5731bec0dfb' # pragma: allowlist secret
  'https://github.com/zizmorcore/zizmor-pre-commit': 'a4727cbbcd26d7098e96b9cb738169b59711ae51' # pragma: allowlist secret
  'https://github.com/hadolint/hadolint': '57e1618d78fd469a92c1e584e8c9313024656623' # pragma: allowlist secret
  'https://github.com/rhysd/actionlint': '914e7df21a07ef503a81201c76d2b11c789d3fca' # pragma: allowlist secret
  'https://github.com/stackrox/kube-linter': '10ae003038c81855aca8489df5e35da150f4dc2e' # pragma: allowlist secret
pre_commit_source_tags:
  'https://github.com/commitizen-tools/commitizen': 'v4.15.1'
  'https://github.com/pre-commit/pre-commit-hooks': 'v6.0.0'
  'https://github.com/gitleaks/gitleaks': 'v8.30.0'
  'https://github.com/Yelp/detect-secrets': 'v1.5.0' # pragma: allowlist secret
  'https://github.com/DavidAnson/markdownlint-cli2': 'v0.22.1'
  'https://github.com/python-jsonschema/check-jsonschema': '0.37.2'
  'https://github.com/shellcheck-py/shellcheck-py': 'v0.11.0.1'
  'https://github.com/scop/pre-commit-shfmt': 'v3.13.1-1'
  'https://github.com/zizmorcore/zizmor-pre-commit': 'v1.24.1'
  'https://github.com/hadolint/hadolint': 'v2.14.0'
  'https://github.com/rhysd/actionlint': 'v1.7.12'
  'https://github.com/stackrox/kube-linter': 'v0.8.3'
```

## Sources

- cloud example snapshot의 각 행에 공식 기준 링크를 둔다.
- repo-backed version contracts는 `.github/`, `.pre-commit-config.yaml`, `gitops/`, `infrastructure/`의 실제 파일과 함께 유지한다.
- [pip secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/)의 all-or-nothing hash mode와 binary-only 설치 지침을 Linux/CPython 3.12 CI 잠금 계약에 적용한다.
- [pre-commit autoupdate options](https://pre-commit.com/#pre-commit-autoupdate-options)의 `--freeze` 동작을 non-local hook commit 고정 정책에 적용한다.

## Review and Freshness

- Review cadence: on dependency bump, cloud example refresh, or official support-range change.
- Last reviewed: 2026-07-30.
- Next review trigger: a PR that changes `gitops/**`, `infrastructure/**`, `.github/workflows/**`, `.pre-commit-config.yaml`, `examples/aws/**`, or `examples/azure/**` version pins.

## Related Documents

- [References README](../README.md)
- [Versions README](./README.md)
- [Reference Maintenance Runbook](../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
- [CI Workflow](../../../.github/workflows/ci.yml)
- [Pre-commit Config](../../../.pre-commit-config.yaml)
