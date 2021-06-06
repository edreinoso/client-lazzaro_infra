resource "aws_ecs_cluster" "ecs-cluster" {
#  name = "lazzaro-back-cluster" # v2 version -- needs to be deprecated
 name = "lazzaro-back-cluster-${terraform.workspace}"
 capacity_providers = ["FARGATE_SPOT", "FARGATE"]

 default_capacity_provider_strategy {
   capacity_provider = "FARGATE"
  #  capacity_provider = "FARGATE_SPOT"
 }
}
