resource "aws_ecs_cluster" "ecs-cluster" {
 name = "lazzaro-front-cluster-${terraform.workspace}"
 capacity_providers = ["FARGATE_SPOT", "FARGATE"]

 default_capacity_provider_strategy {
   capacity_provider = "FARGATE"
 }
}

resource "aws_ecr_repository" "ecr" {
  name = "lazzaro-front-repo-${terraform.workspace}" # this is the todo app
}

resource "aws_cloudwatch_log_group" "ecs-cloudwatch-logs" {
  name = "/ecs/front/${terraform.workspace}"
}