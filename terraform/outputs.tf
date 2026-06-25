# ─────────────────────────────────────────────────────────────────────────────
# terraform/outputs.tf — Outputs surfaced after terraform apply
# ─────────────────────────────────────────────────────────────────────────────

output "cluster_endpoint" {
  description = "EKS cluster API server endpoint."
  value       = module.eks.cluster_endpoint
  sensitive   = false
}

output "cluster_name" {
  description = "EKS cluster name — use in: aws eks update-kubeconfig --name <value>"
  value       = module.eks.cluster_name
}

output "ecr_repository_url" {
  description = "ECR repository URL for the constitutional engine image. Use in k8s/production-stack.yaml."
  value       = aws_ecr_repository.constitutional_engine.repository_url
}

output "vpc_id" {
  description = "Enterprise VPC ID."
  value       = aws_vpc.enterprise_vpc.id
}

output "private_subnet_ids" {
  description = "Private subnet IDs where EKS nodes and core services run."
  value       = aws_subnet.private[*].id
}

output "nat_gateway_ip" {
  description = "Elastic IP of the NAT Gateway — whitelist this in OpenAI org settings if needed."
  value       = aws_eip.nat.public_ip
}
