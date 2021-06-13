resource "aws_ecs_cluster" "ecs-cluster" {
 name = "lazzaro-front-cluster-${terraform.workspace}"
#  name = "lazzaro-front-cluster"
 capacity_providers = ["FARGATE_SPOT", "FARGATE"]

 default_capacity_provider_strategy {
   capacity_provider = "FARGATE"
 }
}