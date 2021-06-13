data "terraform_remote_state" "ecs_service" {
  backend = "s3"
  config = {
    bucket = "terraform-state-lazzaro"
    # key    = "env:/${terraform.workspace}/infra_front.tfstate" # pre
    key    = "infra_front.tfstate" # prod
    region = "eu-central-1"
  }
}


# dynamic variables according to the environment
## ecr repo name
resource "aws_ssm_parameter" "repository_name" {
  name  = "/${terraform.workspace}/front/services/ecs/repo_name"
  type  = "String"
  value = "lazzaro-front-repo"
}

## cluster arn
resource "aws_ssm_parameter" "cluster_arn" {
  name  = "/${terraform.workspace}/front/services/ecs/cluster_arn"
  type  = "String"
  value = data.terraform_remote_state.ecs_service.outputs.cluster_id
}

## image
resource "aws_ssm_parameter" "image" {
  name  = "/${terraform.workspace}/front/services/ecs/image"
  type  = "String"
  value = "${data.terraform_remote_state.ecs_service.outputs.repository_url}:"
}

## container name
resource "aws_ssm_parameter" "container" {
  name  = "/${terraform.workspace}/front/services/ecs/container"
  type  = "String"
  value = "ecs-cluster-${terraform.workspace}"
}
