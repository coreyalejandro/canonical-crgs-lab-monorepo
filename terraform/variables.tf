# ─────────────────────────────────────────────────────────────────────────────
# terraform/variables.tf — Input variables for CRGS Lab cloud infrastructure
# ─────────────────────────────────────────────────────────────────────────────

variable "aws_region" {
  description = "AWS region to deploy into."
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for the enterprise VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "cluster_name" {
  description = "EKS cluster name."
  type        = string
  default     = "constitutional-ai-cluster"
}

variable "instance_type" {
  description = "EC2 instance type for EKS managed node group (Standard Enterprise tier)."
  type        = string
  default     = "m5.2xlarge"
}

variable "node_min" {
  description = "Minimum number of EKS worker nodes."
  type        = number
  default     = 2
}

variable "node_max" {
  description = "Maximum number of EKS worker nodes (auto-scaling ceiling)."
  type        = number
  default     = 10
}

variable "node_desired" {
  description = "Desired number of EKS worker nodes at steady state."
  type        = number
  default     = 3
}
