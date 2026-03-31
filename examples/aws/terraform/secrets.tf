# Secret Management Configuration (AWS 2026)

# Secrets Manager Secret
resource "aws_secretsmanager_secret" "app_secrets" {
  name        = "${var.cluster_name}-app-secrets"
  description = "Secrets for applications migrated to AWS"

  recovery_window_in_days = 7 # 2026 기준 표준 보안 정책 반영
}

resource "aws_secretsmanager_secret_version" "example" {
  secret_id     = aws_secretsmanager_secret.app_secrets.id
  secret_string = jsonencode({
    DB_PASSWORD    = "dummy-password-from-terraform" # gitleaks:allow # pragma: allowlist secret
    REDIS_PASSWORD = "dummy-redis-password" # gitleaks:allow # pragma: allowlist secret
  })
}

# IAM Role for External Secrets Operator (Using Pod Identity)
resource "aws_iam_role" "eso_role" {
  name = "${var.cluster_name}-eso-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "pods.eks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eso_sm_access" {
  role       = aws_iam_role.eso_role.name
  policy_arn = "arn:aws:iam::aws:policy/SecretsManagerReadWrite" # 필요에 따라 권한 축소 권장
}

# Pod Identity Association for ESO
resource "aws_eks_pod_identity_association" "eso" {
  cluster_name    = module.eks.cluster_name
  namespace       = "external-secrets"
  service_account = "external-secrets-cert-controller" # 실제 설치된 SA명으로 조정 필요
  role_arn        = aws_iam_role.eso_role.arn
}
