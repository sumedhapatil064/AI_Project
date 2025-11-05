project_name = "AI_Resume_Builder_full"
region       = "ap-south-1"
image        = "ghcr.io/your-org/ai_resume_builder_full:latest"
container_port = 8501
healthcheck_path = "/"
vpc_id = "vpc-xxxxxxxx"
public_subnets  = ["subnet-111","subnet-222"]
private_subnets = ["subnet-333","subnet-444"]
lb_sg_id = "sg-aaaa"
service_sg_id = "sg-bbbb"
execution_role_arn = "arn:aws:iam::123456789012:role/ecsTaskExecutionRole"
task_role_arn      = "arn:aws:iam::123456789012:role/ecsTaskRole"
environment = [
  { name = "ENV", value = "prod" }
]
