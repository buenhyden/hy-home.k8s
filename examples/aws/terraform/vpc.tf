# VPC Configuration (AWS 2026)

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "6.6.1"

  name = "${var.cluster_name}-vpc"
  cidr = "10.100.0.0/16"

  azs             = ["ap-northeast-2a", "ap-northeast-2b", "ap-northeast-2c"]
  public_subnets  = ["10.100.1.0/24", "10.100.2.0/24", "10.100.3.0/24"]
  private_subnets = ["10.100.11.0/24", "10.100.12.0/24", "10.100.13.0/24"]
  intra_subnets   = ["10.100.21.0/24", "10.100.22.0/24", "10.100.23.0/24"] # Isolated for DB/Cache

  enable_nat_gateway     = true
  single_nat_gateway     = false # Production 고가용성을 위해 3개 배치 (비용 고려 시 single=true 조정 가능)
  one_nat_gateway_per_az = true

  enable_dns_hostnames = true
  enable_dns_support   = true

  # VPC Endpoints (Interface Endpoints for Security)
  enable_flow_log                      = true
  create_flow_log_cloudwatch_iam_role  = true
  create_flow_log_cloudwatch_log_group = true

  # Tags for Karpenter & ALB Discovery
  public_subnet_tags = {
    "kubernetes.io/role/elb"                    = "1"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb"           = "1"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "karpenter.sh/discovery"                    = var.cluster_name
  }

  tags = {
    Terraform = "true"
    Environment = "production"
  }
}
