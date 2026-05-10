# AWS Infrastructure Recovery Runbook

: AWS EKS, RDS, ElastiCache Recovery

## Overview (KR)

이 런북은 AWS 클라우드 인프라 장애 또는 오설정 발생 시 즉각적으로 서비스를 복구하기 위한 단계별 실행 절차를 정의한다. 운영자가 비상 상황에서 판단을 최소화하고 매뉴얼에 따라 빠르게 대응할 수 있도록 한다.

## Purpose

이 런북은 클러스터 중단, 데이터베이스 연결 오류, 네트워크 차단 등 핵심 인프라 장애를 해결하기 위한 목적을 가진다.

## Canonical References

- **AARD**: [../02.architecture/requirements/2026-03-31-aws-migration-ard.md](../../02.architecture/requirements/2026-03-31-aws-migration-ard.md)
- **ADR**: [../02.architecture/decisions/2026-03-31-replace-vault-with-secrets-manager.md](../../02.architecture/decisions/2026-03-31-replace-vault-with-secrets-manager.md)
- **Spec**: [../03.specs/aws-migration/spec.md](../../03.specs/aws-migration/spec.md)
- **Plan**: [../04.execution/plans/2026-03-31-aws-migration-plan.md](../../04.execution/plans/2026-03-31-aws-migration-plan.md)

## When to Use

- AWS RDS 또는 ElastiCache의 갑작스러운 가동 중단 시.
- EKS 노드 그룹 스케일링 오류 또는 Control Plane 접속 불가 시.
- 아키텍처 변경 후 네트워크 단절로 인한 서비스 통신 장애 시.

## Procedure or Checklist

### Checklist

- [ ] [ ] AWS Console 로그인 및 CloudWatch Alert 확인.
- [ ] [ ] Terraform State 파일의 이상 유무(`terraform state list`) 확인.
- [ ] [ ] 관련 리소스(EKS, RDS)의 AWS Service Health Dashboard 상태 확인.

### Procedure

1. **상태 진단**: `aws eks describe-cluster --name hy-home-eks` 명령으로 클러스터 상태가 `ACTIVE`인지 확인.
2. **네트워크 확인**: 장애가 발생한 서비스의 Security Group 및 NACL 설정이 최근 변경되었는지 감사 로그(`CloudTrail`) 확인.
3. **데이터 소스 복구**: RDS 인스턴스 중단 시 Multi-AZ Failover가 자동으로 발생했는지 확인하고, 필요시 최신 스냅샷에서 수동 복원.
4. **IaC 동기화**: `terraform apply`를 실행하여 의도하지 않은 수동 변경 사항을 백업된 코드로 복구(Force overwrite).

## Verification Steps

- [x] [ ] `kubectl get pods -A` 명령으로 모든 시스템 컴포넌트가 `Running` 상태인지 확인.
- [x] [ ] `aws rds describe-db-instances` 명령으로 DB 인스턴스 주소 응답 확인.

## Observability and Evidence Sources

- **Signals**: CloudWatch Metrics (CPU %, Memory Usage, Connection Count).
- **Evidence to Capture**: `kubectl describe pod <failed-pod>`, CloudTrail Event Log (.json).

## Safe Rollback or Recovery Procedure

- [ ] [ ] **Snapshot Recovery**: `aws rds restore-db-instance-from-db-snapshot --db-instance-identifier restored-db --snapshot-identifier latest-snapshot` 실행.
- [ ] [ ] **Git Rollback**: `git revert <commit-hash>` 실행 후 `terraform apply`.

## Related Operational Documents

- **Incident examples**: [../../05.operations/incidents/2026-03-31-aws-db-outage.md](../../../05.operations/incidents/2026-03-31-aws-db-outage.md)
- **Operation**: [../05.operations/policies/aws-management.md](../policies/aws-management.md)
