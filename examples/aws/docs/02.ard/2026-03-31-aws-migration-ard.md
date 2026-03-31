# AWS Infrastructure Migration Architecture Reference Document (ARD)

## Overview (KR)

이 문서는 로컬 K3s/k3d 환경에서 AWS 환경으로 전환되는 시스템의 아키텍처 원칙과 표준을 정의한다. 고가용성, 확장성, 보안성이 강화된 클라우드 네이티브 참조 모델을 제공하여 구현의 정합성을 보장한다.

## Summary

이 시스템은 AWS 매니지드 기반의 컨테이너 오케스트레이션 플랫폼(EKS)과 전용 데이터 플랫폼(RDS/ElastiCache)을 소유하며, 마이크로서비스 아키텍처(MSA) 운영을 위한 인프라 계층을 제공한다.

## Boundaries & Non-goals

- **Owns**: VPC 네트워크, EKS 클러스터(Control Plane, Node), RDS Instance, ElastiCache Instance, ALB/NLB.
- **Consumes**: AWS API (EC2, IAM, Route53, ACM), Docker Registry (ECR).
- **Does Not Own**: 개별 마이크로서비스의 비즈니스 로직, 외부 타 서비스(GCP, On-premise).
- **Non-goals**: 온프레미스 연동(Direct Connect), 서버리스 Fargate 단독 구성.

## Quality Attributes

- **Performance**: AWS Load Balancer 및 로컬 캐싱(ElastiCache)을 통한 낮은 지연 시간 보장.
- **Security**: IAM IRSA (IAM Roles for Service Accounts)를 활용한 최소 권한 원칙(Least Privilege) 적용.
- **Reliability**: Multi-AZ 구성을 통한 데이터 및 컴퓨팅 가용성 보장 (99.9% 이상).
- **Scalability**: Cluster Autoscaler 및 Horizontal Pod Autoscaling (HPA) 지원으로 가변적 트래픽 대응.
- **Observability**: CloudWatch 및 EKS Control Plane Logging을 통한 운영 가시성 확보.
- **Operability**: Terraform을 통한 코드 기반 인프라 관리(IaC) 및 GitOps 배포 표준화.

## System Overview & Context

이 아키텍처는 3계층(Web-App-DB) 구조를 따르며, EKS 노드 그룹은 프라이빗 서브넷에, ALB는 퍼블릭 서브넷에 배치하여 외부 직접 접근을 제한한다. 통신은 Ingress Controller를 통해 제어되며 서비스 간 통신은 Istio Service Mesh로 관리 가능하다.

## Data Architecture

- **Key Entities / Flows**: Pod -> RDS (Write/Read), Pod -> ElastiCache (Caching).
- **Storage Strategy**: RDS PostgreSQL (Persistent Data), ElastiCache Redis (Session/Cache).
- **Data Boundaries**: DB 서브넷은 별도의 격리된 네트워크에 위치하며 EKS 노드 보안 그룹의 인바운드만 허용한다.

## Infrastructure & Deployment

- **Runtime / Platform**: Amazon EKS (Kubernetes 1.28+)
- **Deployment Model**: Terraform 기반 인프라 프로비저닝 + ArgoCD 기반 애플리케이션 배포
- **Operational Evidence**: AWS CloudWatch Metrics, EKS Control Plane Logs.

## Related Documents

- **PRD**: [../01.prd/2026-03-31-aws-migration-prd.md](../01.prd/2026-03-31-aws-migration-prd.md)
- **ADR**: [../03.adr/2026-03-31-replace-vault-with-secrets-manager.md](../03.adr/2026-03-31-replace-vault-with-secrets-manager.md)
- **Plan**: [../05.plans/2026-03-31-aws-migration-plan.md](../05.plans/2026-03-31-aws-migration-plan.md)
- **Spec**: [../04.specs/aws-migration/spec.md](../04.specs/aws-migration/spec.md)
- **Task**: [../06.tasks/2026-03-31-bootstrap-aws.md](../06.tasks/2026-03-31-bootstrap-aws.md)
- **Guide**: [../07.guides/aws-setup-guide.md](../07.guides/aws-setup-guide.md)
