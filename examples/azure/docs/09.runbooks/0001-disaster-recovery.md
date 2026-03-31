# Azure Infrastructure Disaster Recovery Runbook

## Overview (KR)

이 런북은 Azure 기반 인프라(AKS, PostgreSQL, Redis)의 중단 상황 발생 시 복구 절차를 정의한다. 데이터 손실 최소화와 서비스 조기 복구를 위한 단계별 가이드를 제공한다.

## Purpose

지역(Region) 장애, 리소스 완전 삭제 또는 보안 사고 등으로 인해 프로젝트 리소스가 가동 불가 상태가 되었을 때, 인프라를 재구축하고 데이터를 복구하는 절차를 표준화한다.

## Canonical References

- **ARD**: [../02.ard/0001-azure-migration-architecture.md](../02.ard/0001-azure-migration-architecture.md)
- **ADR**: [../03.adr/README.md](../03.adr/README.md)
- **Spec**: [../04.specs/azure-migration/spec.md](../04.specs/azure-migration/spec.md)
- **Plan**: [../05.plans/2026-03-31-migration-strategy.md](../05.plans/2026-03-31-migration-strategy.md)

## When to Use

- Azure 리전 전체 장애로 인한 서비스 가동 중단.
- 실수로 인한 AKS 클러스터 또는 리소스 그룹 삭제.
- 랜섬웨어 또는 악성 행위로 인한 데이터베이스 오염.

## Procedure or Checklist

### Checklist

- [ ] Azure 서비스 상태 확인 (Azure Status Dashboard).
- [ ] 최근 성공한 Bicep 배포 템플릿 확보 (infrastructure/ dir).
- [ ] PostgreSQL의 가장 최근 Point-in-time Recovery(PITR) 가능 시점 확인.
- [ ] ArgoCD GitOps 설정 저장소 접근 가능 여부 확인.

### Procedure

#### 1. 인프라 재배포 (Bicep)
기존 Resource Group이 유실된 경우 새로 생성하고 Bicep을 통해 기초 인프라를 복원한다.
```bash
az group create --name hy-home-k8s-prod-dr --location <dr-region>
az deployment group create --resource-group hy-home-k8s-prod-dr --template-file infrastructure/main.bicep
```

#### 2. 데이터베이스 복구 (PITR)
Azure Database for PostgreSQL Flexible Server의 복원을 수행한다.
```bash
az postgres flexible-server restore --resource-group hy-home-k8s-prod-dr --name <new-db-name> --source-server <old-db-name> --restore-time <timestamp>
```

#### 3. Kubernetes 워크로드 배포 (GitOps)
ArgoCD를 통해 클러스터 내부에 애플리케이션 리소스를 재배포한다.
```bash
# ArgoCD context update
kubectl config use-context <new-aks-context>
argocd cluster add <new-aks-context>
argocd app sync hy-home-root-app
```

## Verification Steps

- [ ] `kubectl get pods -A` 모든 Pod가 Running 상태인지 확인.
- [ ] `kubectl get gateway` AGC Gateway가 정상 동작하며 공인 IP 주소를 확보했는지 확인.
- [ ] App 로그에서 DB 연결(Handshake) 성공 여부 확인.

## Observability and Evidence Sources

- **Signals**: Service Health Alerts, Log Analytics (KubePodInventory).
- **Evidence to Capture**: `kubectl describe nodes`, `az resource list --resource-group hy-home-k8s-prod-dr`.

## Safe Rollback or Recovery Procedure

- 데이터 복구 실패 시, 보관 중인 오프라인 덤프를 수동으로 SQL 주입 처리한다.
- AGC 설정 에러 시, 가용성이 보장되는 별도의 외부 LoadBalancer로 임시 전환을 고려한다.

## Related Operational Documents

- **Maintenance**: [../08.operations/azure-maintenance-policy.md](../08.operations/azure-maintenance-policy.md)
- **Spec**: [../04.specs/azure-migration/spec.md](../04.specs/azure-migration/spec.md)
