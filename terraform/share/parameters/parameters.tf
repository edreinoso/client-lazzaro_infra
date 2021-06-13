data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "terraform-state-lazzaro"
    key    = "env:/v1/network.tfstate"
    region = "eu-central-1"
  }
}


resource "aws_ssm_parameter" "vpc_id" {
  name  = "${terraform.workspace}/back/network/vpc_id"
  type  = "String"
  value = element(data.terraform_remote_state.network.outputs.vpc-id, 1)
}
resource "aws_ssm_parameter" "role_arn" {
  name  = "${terraform.workspace}/back/network/vpc-id"
  type  = "String"
  value = element(data.terraform_remote_state.network.outputs.vpc-id, 1)
}