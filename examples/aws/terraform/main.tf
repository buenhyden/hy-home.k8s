# Terraform Main Configuration (AWS 2026)

terraform {
  required_version = ">= 1.14.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 6.28, < 7.0" # 2026-05-09 공식 지원 스냅샷 기준
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.30"
    }
  }

  # Backend 설정 (S3/DynamoDB) - 로컬에서는 주석 처리 권장
  # backend "s3" {
  #   bucket         = "hyhome-terraform-state"
  #   key            = "aws-migration/terraform.tfstate"
  #   region         = "ap-northeast-2"
  #   dynamodb_table = "terraform-lock"
  # }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Project     = "hy-home.k8s"
      Environment = "production"
      ManagedBy   = "terraform"
      Migration   = "aws"
    }
  }
}

variable "region" {
  description = "AWS Region to deploy infrastructure"
  type        = string
  default     = "ap-northeast-2"
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "hyhome-cluster"
}
