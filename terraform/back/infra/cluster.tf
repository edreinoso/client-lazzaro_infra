resource "aws_ecs_cluster" "ecs-cluster" {
 name = "lazzaro-back-cluster-${terraform.workspace}"
 capacity_providers = ["FARGATE_SPOT", "FARGATE"]

 default_capacity_provider_strategy {
   capacity_provider = "FARGATE"
 }
}
