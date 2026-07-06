---
title: 'AWS Cloud Architecture (Migration from K3s/k3d)'
type: sdlc/ard
status: accepted
owner: platform
updated: 2026-07-06
---

# AWS Cloud Architecture (Migration from K3s/k3d)

이 문서는 2026-05-09 공식 지원 스냅샷 기준 AWS 관리형 서비스를 활용하여 로컬 K3s 인프라를 AWS로 이식하기 위한 아키텍처를 정의합니다.

## Overview

로컬의 `k3d` 클러스터와 외부 Docker 서비스들을 AWS의 고가용성 관리형 서비스로 대체합니다.

### Resource Mapping Table

| 카테고리 | 로컬 환경 (k3d/Docker) | AWS 환경 (Target) | 상세 서비스 |
| :--- | :--- | :--- | :--- |
| **Compute** | k3d (1 Master, 3 Worker) | **Amazon EKS** | Managed Node Groups (M5.large) |
| **Networking** | MetalLB (L2 Adv) | **VPC + Load Balancer** | AWS Load Balancer Controller (ALB/NLB) |
| **Database** | Postgres (Docker) | **Amazon RDS** | Aurora PostgreSQL / RDS Multi-AZ |
| **Cache** | Valkey (Docker) | **Amazon ElastiCache** | ElastiCache for Redis (Valkey Compatible) |
| **Secrets** | HashiCorp Vault (Docker) | **AWS Secrets Manager** | External Secrets Operator (ESO) 연동 |
| **Storage** | Local Path Provisioner | **Amazon EBS / EFS** | AWS EBS CSI Driver |
| **DNS** | nip.io | **Amazon Route 53** | ExternalDNS 연동 |
| **Registry** | Local Registry | **Amazon ECR** | Private Repository |

---

## Snapshot Boundary

This document is an example-local SDLC snapshot for cloud migration reference. It follows the repository's Cloud Example Snapshot boundary and is not live provider-latest guidance.

## Network Architecture

VPC는 3개의 Availability Zone(AZ)을 사용하며, 각 AZ마다 Public/Private/Database 서브넷을 구성합니다.

- **Public Subnet**: ALB, NLB, NAT Gateway 가 위치합니다.
- **Private Subnet**: EKS Worker Node들이 위치하며, 인터넷 통신은 NAT GW를 거칩니다.
- **Database Subnet**: RDS 및 ElastiCache 클러스터가 위치하며 외부 접근이 차단됩니다.

---

## Security Best Practices

1. **IRSA (IAM Roles for Service Accounts)**:
   - 각 Pod에 필요한 최소 권한의 IAM Role을 부여하여 보안을 강화합니다.
   - 예: AWS Load Balancer Controller, External Secrets Operator.

2. **Secrets Management**:
   - `External Secrets Operator`를 사용하여 AWS Secrets Manager의 시크릿을 K8s Secret으로 자동 동기화합니다.
   - 로컬의 Vault 의존성을 제거하고 AWS 매니지드 환경으로 통합합니다.

3. **Inbound Traffic**:
   - `AWS Load Balancer Controller`를 통해 Ingress 자원 생성 시 ALB(Application Load Balancer)를 자동으로 프로비저닝합니다.
   - SSL/TLS 인증서는 **AWS Certificate Manager (ACM)**을 통해 관리합니다.

---

## Cost Optimization (FinOps)

- **Spot Instances**: 비수행 작업(CI/CD Runner, Dev App)에 대해 Spot Instance를 활용하여 비용을 최대 90% 절감합니다.
- **RDS Proxy**: DB 연결 효율성을 높이고 리소스 낭비를 방지합니다.
- **S3 Intelligent-Tiering**: 로그 및 백업 데이터 스토리지 비용을 최적화합니다.

## Related Documents

- [AWS Example Documentation Hub](../../README.md)
