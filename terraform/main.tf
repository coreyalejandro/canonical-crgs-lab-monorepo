# ─────────────────────────────────────────────────────────────────────────────
# terraform/main.tf — CRGS Lab Enterprise Cloud Infrastructure
#
# Phase 6 Build Contract — Section I
# Governed by: The Living Constitution 2.0 — Sociotechnical Constitution v2.0.0
#
# Provisions:
#   1. VPC with public + private subnets across two AZs
#   2. Internet Gateway + NAT Gateway (engine can reach OpenAI; sandbox cannot)
#   3. Strict security group for the math sandbox (inbound VPC-only, no egress)
#   4. EKS cluster (Standard Enterprise tier: m5.2xlarge, 2–10 nodes)
#   5. ECR repository for the constitutional engine image
# ─────────────────────────────────────────────────────────────────────────────

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Remote state — replace bucket/key with your own S3 bucket before apply
  backend "s3" {
    bucket = "crgs-lab-terraform-state"
    key    = "production/terraform.tfstate"
    region = "us-east-1"
    encrypt = true
  }
}

# ── Provider ──────────────────────────────────────────────────────────────────

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "Constitutional_AI_RnD"
      Environment = "Production"
      Strict_IaC  = "True"
      ManagedBy   = "Terraform"
      GovernedBy  = "TLC_2.0"
    }
  }
}

# ── Data sources ──────────────────────────────────────────────────────────────

data "aws_availability_zones" "available" {
  state = "available"
}

# ── VPC ───────────────────────────────────────────────────────────────────────

resource "aws_vpc" "enterprise_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = { Name = "crgs-lab-enterprise-vpc" }
}

# Public subnets (load balancer lives here)
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.enterprise_vpc.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = { Name = "crgs-lab-public-${count.index}" }
}

# Private subnets (EKS nodes, Neo4j, sandbox all live here)
resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.enterprise_vpc.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + 10)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = { Name = "crgs-lab-private-${count.index}" }
}

# Internet Gateway (public subnets → internet)
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.enterprise_vpc.id
  tags   = { Name = "crgs-lab-igw" }
}

# Elastic IP for NAT Gateway
resource "aws_eip" "nat" {
  domain = "vpc"
  tags   = { Name = "crgs-lab-nat-eip" }
}

# NAT Gateway (private subnets → internet via single egress point)
# Engine can reach OpenAI API; sandbox security group blocks it entirely
resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public[0].id
  tags          = { Name = "crgs-lab-nat" }
  depends_on    = [aws_internet_gateway.igw]
}

# Route tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.enterprise_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = { Name = "crgs-lab-public-rt" }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.enterprise_vpc.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }
  tags = { Name = "crgs-lab-private-rt" }
}

resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count          = 2
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}

# ── Security Groups ───────────────────────────────────────────────────────────

# Math sandbox — inbound from VPC only, NO outbound egress (constitutional isolation)
resource "aws_security_group" "math_sandbox_sg" {
  name        = "strict_sandbox_isolation"
  description = "Blocks ALL outbound internet access for the Python REPL sandbox"
  vpc_id      = aws_vpc.enterprise_vpc.id

  ingress {
    description = "Constitutional engine → sandbox only"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  # Egress locked to loopback — no external routing possible
  egress {
    description = "Nullify external routing — sandbox cannot call out"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["127.0.0.1/32"]
  }

  tags = { Name = "crgs-lab-sandbox-sg" }
}

# Constitutional engine — can reach OpenAI API via NAT, accepts dashboard traffic
resource "aws_security_group" "engine_sg" {
  name        = "constitutional_engine_sg"
  description = "Allows engine to reach OpenAI API and serve the Streamlit dashboard"
  vpc_id      = aws_vpc.enterprise_vpc.id

  ingress {
    description = "Streamlit dashboard from load balancer"
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    description = "Full outbound — engine must reach OpenAI API via NAT"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "crgs-lab-engine-sg" }
}

# ── EKS Cluster ───────────────────────────────────────────────────────────────

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  version         = "19.15.3"
  cluster_name    = var.cluster_name
  cluster_version = "1.27"

  vpc_id     = aws_vpc.enterprise_vpc.id
  subnet_ids = aws_subnet.private[*].id

  cluster_endpoint_public_access = true

  eks_managed_node_groups = {
    ai_compute_nodes = {
      min_size       = var.node_min
      max_size       = var.node_max
      desired_size   = var.node_desired
      instance_types = [var.instance_type]

      # Nodes run in private subnets — no public IPs
      subnet_ids = aws_subnet.private[*].id
    }
  }

  tags = { Name = var.cluster_name }
}

# ── ECR Repository ────────────────────────────────────────────────────────────

resource "aws_ecr_repository" "constitutional_engine" {
  name                 = "constitutional_engine"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = { Name = "crgs-lab-ecr" }
}
