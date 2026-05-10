# Tech Stack Version Inventory

## Purpose

이 문서는 `hy-home.k8s`의 repo-backed 매니페스트와 품질 게이트에서 읽어야 하는 버전 기준을 고정한다.
새 버전으로 올릴 때는 실제 manifest/config와 이 문서를 같은 변경으로 수정한다.

## Reference Type

- Type: version-contract-inventory / external-standard-snapshot
- Source checked: 2026-05-09
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

## Overview (KR)

이 문서는 일반 참고 링크 모음이 아니라 검증 대상 버전 계약 인벤토리다. repo-backed manifest, GitHub Actions, pre-commit hook, cloud example snapshot의 기준 값을 한곳에서 추적한다.

## Scope

- repo-backed k3s/Helm chart/GitHub Actions/pre-commit 버전 계약
- `examples/aws`, `examples/azure`를 갱신할 때 사용한 공식 cloud example snapshot
- 버전 drift 검증과 README/docs 설명을 맞추기 위한 기준값
- 실제 cloud provider 계정 변경, live cluster upgrade, 자동 dependency bump는 제외한다.

## Definitions / Facts

- **Version Contracts**: 아래 YAML 블록의 값이며 repo manifest/config와 함께 검증되는 기준이다.
- **Cloud Example Snapshot**: AWS/Azure 예시를 갱신할 때 확인한 2026-05-09 기준 공식 지원 상태다.
- **Ingress NGINX boundary**: 로컬 k3d 계약은 유지하되 cloud target은 ALB/Gateway API/AGC 경로로 분리한다.

## Sources

- cloud example snapshot의 각 행에 공식 기준 링크를 둔다.
- repo-backed version contracts는 `.github/`, `.pre-commit-config.yaml`, `gitops/`, `infrastructure/`의 실제 파일과 함께 유지한다.

## Review and Freshness

- Review cadence: on dependency bump, cloud example refresh, or official support-range change.
- Last reviewed: 2026-05-09.
- Next review trigger: a PR that changes `gitops/**`, `infrastructure/**`, `.github/workflows/**`, `.pre-commit-config.yaml`, `examples/aws/**`, or `examples/azure/**` version pins.

## Cloud Example Snapshot: 2026-05-09

이 섹션은 `examples/aws`와 `examples/azure`의 참조 구현을 갱신할 때 사용한 공식 기준이다. 로컬 k3d 실행 계약은 아래 `Version Contracts`의 `rancher/k3s:v1.35.0-k3s1`을 따른다.

| Area | Repo example target | Official basis | Note |
| --- | --- | --- | --- |
| Kubernetes upstream | 1.36 latest release awareness | [Kubernetes v1.36 release](https://kubernetes.io/blog/2026/04/22/kubernetes-v1-36-release/) | 로컬 k3d와 cloud managed cluster target을 자동 변경하지 않는다. |
| AWS EKS | 1.35 target, standard support set 1.35/1.34/1.33 | [AWS EKS versions](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html) | `examples/aws/terraform`은 EKS 1.35 참조 구현으로 유지한다. |
| Azure AKS | 1.35 target | [AKS supported versions](https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions) | `examples/azure/infrastructure`의 기본 AKS version과 docs target을 맞춘다. |
| Terraform AWS provider | `>= 6.28, < 7.0` | [Terraform AWS provider](https://registry.terraform.io/providers/-/aws/latest) | provider major drift를 피하면서 6.x 최신 기준을 사용한다. |
| Terraform EKS module | `21.20.0` | [EKS module](https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/latest) | EKS 1.35 target과 함께 갱신한다. |
| Terraform VPC module | `6.6.1` | [VPC module](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws) | AWS network example 기준이다. |
| Terraform RDS Aurora module | `10.2.0` | [RDS Aurora module](https://registry.terraform.io/modules/terraform-aws-modules/rds-aurora/aws) | Aurora Serverless v2 example 기준이다. |
| Ingress NGINX | Retired upstream since 2026-03-24 | [Ingress NGINX retirement](https://kubernetes.io/blog/2026/01/29/ingress-nginx-statement/) | 로컬 k3d 계약은 문서상 경고로 유지하고 cloud target은 ALB/Gateway API/AGC로 분리한다. |

## Version Contracts

```yaml
k3s_image: "rancher/k3s:v1.35.0-k3s1"
helm_charts:
  platform-cert-manager:
    repoURL: "https://charts.jetstack.io"
    chart: "cert-manager"
    targetRevision: "v1.17.2"
  platform-external-secrets-operator:
    repoURL: "https://charts.external-secrets.io"
    chart: "external-secrets"
    targetRevision: "0.14.4"
  platform-headlamp:
    repoURL: "https://kubernetes-sigs.github.io/headlamp/"
    chart: "headlamp"
    targetRevision: "0.41.0"
  platform-ingress-nginx:
    repoURL: "https://kubernetes.github.io/ingress-nginx"
    chart: "ingress-nginx"
    targetRevision: "4.12.0"
  platform-istio-base:
    repoURL: "https://istio-release.storage.googleapis.com/charts"
    chart: "base"
    targetRevision: "1.25.2"
  platform-istiod:
    repoURL: "https://istio-release.storage.googleapis.com/charts"
    chart: "istiod"
    targetRevision: "1.25.2"
  platform-kiali:
    repoURL: "https://kiali.org/helm-charts"
    chart: "kiali-operator"
    targetRevision: "2.10.0"
  platform-rollouts:
    repoURL: "https://argoproj.github.io/argo-helm"
    chart: "argo-rollouts"
    targetRevision: "2.40.9"
github_actions:
  "actions/checkout": "v6"
  "actions/first-interaction": "v3"
  "actions/labeler": "v6"
  "actions/setup-python": "v6"
  "actions/stale": "v10"
  "actions/upload-artifact": "v4"
  "dorny/paths-filter": "v4.0.1"
  "orhun/git-cliff-action": "v4"
  "pre-commit/action": "v3.0.1"
pre_commit:
  "https://github.com/commitizen-tools/commitizen": "v4.13.9"
  "https://github.com/pre-commit/pre-commit-hooks": "v6.0.0"
  "https://github.com/gitleaks/gitleaks": "v8.30.1"
  "https://github.com/Yelp/detect-secrets": "v1.5.0" # pragma: allowlist secret
  "https://github.com/DavidAnson/markdownlint-cli2": "v0.21.0"
  "https://github.com/python-jsonschema/check-jsonschema": "0.37.0"
  "https://github.com/shellcheck-py/shellcheck-py": "v0.11.0.1"
  "https://github.com/scop/pre-commit-shfmt": "v3.12.0-2"
  "https://github.com/zizmorcore/zizmor-pre-commit": "v1.23.1"
  "https://github.com/hadolint/hadolint": "v2.14.0"
  "https://github.com/rhysd/actionlint": "v1.7.11"
  "https://github.com/stackrox/kube-linter": "v0.8.3"
```

## Related Documents

- [References README](../README.md)
- [Versions README](./README.md)
- [CI Workflow](../../../.github/workflows/ci.yml)
- [Pre-commit Config](../../../.pre-commit-config.yaml)
