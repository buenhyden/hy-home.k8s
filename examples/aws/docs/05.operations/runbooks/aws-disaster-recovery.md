---
title: 'AWS Disaster Recovery Runbook'
type: sdlc/runbook
status: accepted
owner: platform
updated: 2026-07-06
---

# AWS Disaster Recovery Runbook

: AWS Migration and Operations

## Overview

이 런북은 hy-home.k8s AWS 인프라의 장애 상황(클러스터 파손, 데이터 손실 등)에서 시스템을 신속하게 복구하기 위한 절차를 정의한다. 운영자가 패닉 없이 즉시 따라 할 수 있는 실행 단계를 제공한다.

## Snapshot Boundary

This document is an example-local SDLC snapshot for cloud migration reference. It follows the repository's Cloud Example Snapshot boundary and is not live provider-latest guidance.

## Purpose

이 런북은 하부 인프라(EKS, RDS 등)의 치명적 결함 발생 시, IaC와 백업 데이터를 활용하여 서비스를 정상화하는 것을 목적으로 한다.

## Canonical References

- **AARD**: [../02.architecture/requirements/0001-aws-cloud-native-architecture.md](../../02.architecture/requirements/0001-aws-cloud-native-architecture.md)
- **ADR**: [../02.architecture/decisions/0001-aws-managed-services-selection.md](../../02.architecture/decisions/0001-aws-managed-services-selection.md)
- **Spec**: [../03.specs/aws-migration/spec.md](../../03.specs/aws-migration/spec.md)
- **Plan**: [../04.execution/plans/2026-03-31-aws-migration-roadmap.md](../../04.execution/plans/2026-03-31-aws-migration-roadmap.md)

## When to Use

- EKS 클러스터가 제어 불능 상태(Control Plane Failure)가 된 경우.
- RDS 데이터베이스의 데이터가 물리 데이터 오염으로 인해 복구가 필요한 경우.
- 잘못된 Helm 배포로 인해 클러스터 전체 하이재킹이 의심되는 경우.
- 이 문서는 `examples/aws` reference-only 런북이다. 실제 AWS 계정에서는 운영자 승인 DR 상황에서만 실행한다.

## Procedure or Checklist

### Checklist

- [ ] 현재 영향 받는 서비스 범위 확인 (Monitoring Dashboard)
- [ ] AWS Console 접속 권한 확인 (Root 또는 Admin Role)
- [ ] 최근 24시간 내의 Terraform 상태 파일 및 RDS 스냅샷 존재 확인

### Procedure

#### 1. 인프라 재구축 (EKS 클러스터)

```bash
# reference-only AWS DR; no live resource mutation
cd examples/aws/terraform
terraform plan -out dr-recovery.plan

# Kubeconfig access check with a temporary file
TMP_KUBECONFIG="$(mktemp)"
aws eks update-kubeconfig --name hyhome-cluster --region ap-northeast-2 --kubeconfig "$TMP_KUBECONFIG"
KUBECONFIG="$TMP_KUBECONFIG" kubectl get nodes
```

#### 2. 데이터 복구 (RDS Aurora)

1. RDS 콘솔에서 'Restore from Snapshot' 기능을 선택한다.
2. 장애 발생 직전의 최신 자동 스냅샷을 선택하여 복원한다.
3. 복원된 인스턴스의 엔드포인트를 애플리케이션 시크릿(Secrets Manager)에 업데이트한다.

#### 3. 서비스 배포 (GitOps)

```bash
argocd app diff root-apps --refresh
```

## Verification Steps

- [ ] `kubectl get pods -A` 명령으로 모든 시스템 Pod가 Running 상태인지 확인.
- [ ] `nc -zv <new-rds-endpoint> 5432` 명령으로 DB 연결 확인.
- [ ] 외부 엔드포인트(URL) 접속 및 서비스 정상 동작 여부 확인.

## Safe Rollback or Recovery Procedure

- 장애 복구 시도 중 실패할 경우, 최종 트래픽을 기존 로컬 K3s(만약 살아있다면)로 즉시 전환하거나 정적 점검 페이지로 롤백한다.
- 모든 수동 변경 사항은 복구 후 즉시 Terraform 코드로 역추출하여 반영한다.

## Runbook Type

Example-local cloud operations runbook.

## Observability and Evidence Sources

- Provider portal or CLI output captured outside the repository when sensitive.
- Repository task records for non-secret validation summaries.

## Related Documents

- **Policy**: [../05.operations/policies/aws-operations-policy.md](../policies/aws-operations-policy.md)
