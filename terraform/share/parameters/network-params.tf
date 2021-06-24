data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "terraform-state-lazzaro"
    key    = "env:/v1/network.tfstate"
    region = "eu-central-1"
  }
}


# dynamic variables according to the environment
## vpc
resource "aws_ssm_parameter" "vpc_id" {
  name  = "/${terraform.workspace}/share/network/vpc_id"
  type  = "String"
  value = element(data.terraform_remote_state.network.outputs.vpc-id, 1)
}

## subnets
resource "aws_ssm_parameter" "client_subnet_2_a" {
  name  = "/${terraform.workspace}/share/network/subnet_2_a"
  type  = "String"
  value = element(element(data.terraform_remote_state.network.outputs.pub-subnet-id-a, 0),1,)
}
resource "aws_ssm_parameter" "client_subnet_2_b" {
  name  = "/${terraform.workspace}/share/network/subnet_2_b"
  type  = "String"
  value = element(element(data.terraform_remote_state.network.outputs.pub-subnet-id-b, 0),1,)
}
resource "aws_ssm_parameter" "client_subnet_3_a" {
  name  = "/${terraform.workspace}/share/network/subnet_3_a"
  type  = "String"
  value = element(element(data.terraform_remote_state.network.outputs.pub-subnet-id-a, 0),2,)
}
resource "aws_ssm_parameter" "client_subnet_3_b" {
  name  = "/${terraform.workspace}/share/network/subnet_3_b"
  type  = "String"
  value = element(element(data.terraform_remote_state.network.outputs.pub-subnet-id-b, 0),2,)
}