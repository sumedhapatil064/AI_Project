variable "project_name" { type = string }
variable "region" { type = string }
variable "image" { type = string } // e.g., ghcr.io/owner/repo:latest
variable "container_port" { type = number, default = 8000 }
variable "healthcheck_path" { type = string, default = "/health" }

variable "vpc_id" { type = string }
variable "public_subnets" { type = list(string) }
variable "private_subnets" { type = list(string) }

variable "lb_sg_id" { type = string }       // ALB security group
variable "service_sg_id" { type = string }  // Service security group
variable "execution_role_arn" { type = string }
variable "task_role_arn" { type = string }

variable "environment" {
  type = list(object({
    name  = string
    value = string
  }))
  default = []
}
