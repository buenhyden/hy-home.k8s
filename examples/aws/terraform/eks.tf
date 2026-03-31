# EKS Cluster Configuration (AWS 2026)

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = var.cluster_name
  cluster_version = "1.31" # 2026년 기준 실무에서 널리 쓰이는 버전

  # Network
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  # Access Entry (New in 2024+)
  enable_cluster_creator_admin_permissions = true

  # Authentication (OIDC is still useful for some operators, but Pod Identity is preferred)
  enable_irsa = true

  # Managed Node Groups (Minimal for Core Services only, Others handled by Karpenter)
  eks_managed_node_groups = {
    core = {
      instance_types = ["t3.medium"]
      min_size       = 2
      max_size       = 3
      desired_size   = 2

      labels = {
        role = "core"
      }
    }
  }

  # EKS Pod Identity (v2026 Standard)
  # IAM Roles for Service Accounts (IRSA) legacy support is optional here,
  # but Karpenter/ESO will use Pod Identity.

  tags = {
    Environment = "production"
    GithubRepo  = "hy-home.k8s"
  }
}

# Karpenter IAM Role & Controller Policy (Example)
module "karpenter" {
  source = "terraform-aws-modules/eks/aws//modules/karpenter"

  cluster_name = module.eks.cluster_name

  enable_pod_identity = true
  create_node_iam_role = true

  node_iam_role_additional_policies = {
    AmazonSSMManagedInstanceCore = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
  }
}
