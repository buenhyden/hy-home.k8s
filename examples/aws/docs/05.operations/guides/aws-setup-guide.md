# AWS EKS Setup and Access Guide

## Overview (KR)

이 문서는 hy-home.k8s 마이그레이션 후 AWS EKS 클러스터에 접속하고 로컬 개발 환경을 설정하는 가이드다. 운영자와 개발자가 클러스터 리소스에 안전하게 접근하고 관리하는 방법을 제공한다.

## Guide Type

`onboarding | how-to`

## Target Audience

- Operator (인프라 관리자)
- Developer (애플리케이션 배포자)

## Purpose

이 가이드는 사용자가 AWS 계정 인증을 완료하고 EKS 클러스터의 API 서버와 상호작용할 수 있도록 돕는다.

## Prerequisites

- AWS CLI v2.20+ 설치 및 프로필 설정 (`aws configure`)
- kubectl 1.35-compatible version 설치
- 해당 AWS 계정에 대한 `EKS:DescribeCluster` 권한 보유

## Step-by-step Instructions

### 1. Kubeconfig 업데이트

로컬 환경에서 EKS 클러스터로의 컨텍스트를 추가한다.

```bash
aws eks update-kubeconfig --name hyhome-cluster --region ap-northeast-2
```

### 2. 접속 확인

클러스터 노드 상태를 확인하여 연결이 정상인지 검증한다.

```bash
kubectl get nodes
```

### 3. IAM Pod Identity 권한 확인 (개발자용)

애플리케이션 Pod가 적절한 IAM 권한을 가졌는지 확인하기 위해 테스트 Pod를 실행해볼 수 있다.

```bash
kubectl run aws-cli --image=amazon/aws-cli:latest --restart=Never -- aws sts get-caller-identity
```

## Common Pitfalls

- **권한 오류 (Unauthorized)**: `aws sts get-caller-identity`를 통해 현재 사용 중인 IAM Entity가 클러스터의 `aws-auth` ConfigMap 또는 EKS Access Entry에 등록되어 있는지 확인하라.
- **네트워크 연결 실패**: VPC 내부에서만 접근 가능한 경우 VPN 환경 또는 Bastion Host 확인이 필요하다.

## Related Documents

- **Spec**: [../03.specs/aws-migration/spec.md](../../03.specs/aws-migration/spec.md)
- **Operation**: [../05.operations/policies/aws-operations-policy.md](../policies/aws-operations-policy.md)
