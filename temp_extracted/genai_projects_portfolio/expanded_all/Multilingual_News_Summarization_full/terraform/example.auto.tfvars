project_name = "Multilingual_News_Summarization_full"
region       = "ap-south-1"
image        = "ghcr.io/your-org/multilingual_news_summarization_full:latest"
container_port = 8000
healthcheck_path = "/health"
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
