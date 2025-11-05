project_name = "Semantic_Product_Search_Engine_full"
region       = "ap-south-1"
image        = "ghcr.io/your-org/semantic_product_search_engine_full:latest"
container_port = 8000
healthcheck_path = "/search"
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
