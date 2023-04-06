# DEPRECATED - DELETE SOON 🚧

# resource "aws_ecs_cluster" "ecs-cluster" {
#  name = "lazzaro-back-cluster-${terraform.workspace}"
#  capacity_providers = ["FARGATE_SPOT", "FARGATE"]

#  default_capacity_provider_strategy {
#    capacity_provider = "FARGATE"
#  }
# }


resource "aws_ecs_cluster" "ecs_cluster" {
  name = "lazzaro-back-cluster-${terraform.workspace}"
}

resource "aws_ecs_cluster_capacity_providers" "ecs_cluster_capacity_provider" {
  cluster_name = aws_ecs_cluster.ecs_cluster.name

  capacity_providers = ["FARGATE_SPOT","FARGATE"]

  default_capacity_provider_strategy {
    capacity_provider = "FARGATE"
  }
}