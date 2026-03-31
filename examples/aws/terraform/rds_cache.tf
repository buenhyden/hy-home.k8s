# Managed Data Services Configuration (AWS 2026)

# RDS Aurora Serverless v2 (PostgreSQL)
module "db" {
  source  = "terraform-aws-modules/rds-aurora/aws"
  version = "~> 9.0"

  name           = "${var.cluster_name}-rds"
  engine         = "aurora-postgresql"
  engine_version = "16.1"
  instance_class = "db.serverless"

  vpc_id               = module.vpc.vpc_id
  db_subnet_group_name = module.vpc.database_subnet_group_name
  security_group_rules = {
    ex_ingress = {
      source_security_group_id = module.eks.node_security_group_id
    }
  }

  serverlessv2_scaling_configuration = {
    min_capacity = 0.5
    max_capacity = 4.0
  }

  manage_master_user_password = true
  master_username             = "adminuser"
  database_name               = "hyhomedb"

  tags = {
    Environment = "production"
  }
}

# ElastiCache Serverless (Redis OSS)
resource "aws_elasticache_serverless_cache" "redis" {
  engine = "redis"
  name   = "${var.cluster_name}-redis"
  
  cache_usage_limits {
    data_storage {
      maximum = 10
      unit    = "GB"
    }
    ecpu_per_second {
      maximum = 5000
    }
  }

  description = "Serverless Redis for hy-home.k8s"
  subnet_ids  = module.vpc.intra_subnets
  security_group_ids = [aws_security_group.redis_sg.id]
}

resource "aws_security_group" "redis_sg" {
  name        = "${var.cluster_name}-redis-sg"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [module.eks.node_security_group_id]
  }

  tags = {
    Name = "redis-sg"
  }
}
