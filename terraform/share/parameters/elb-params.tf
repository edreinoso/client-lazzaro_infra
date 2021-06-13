data "terraform_remote_state" "elb_service" {
  backend = "s3"
  config = {
    bucket = "terraform-state-lazzaro"
    key    = "env:/${terraform.workspace}/services_lb_front.tfstate"
    region = "eu-central-1"
  }
}


# dynamic variables according to the environment
## alb
resource "aws_ssm_parameter" "alb_arn" {
  name  = "/${terraform.workspace}/front/services/elb/alb_arn"
  type  = "String"
  value = data.terraform_remote_state.elb_service.outputs.alb_arn
}
resource "aws_ssm_parameter" "alb_dns" {
  name  = "/${terraform.workspace}/front/services/elb/alb_dns"
  type  = "String"
  value = data.terraform_remote_state.elb_service.outputs.alb_dns
}
resource "aws_ssm_parameter" "alb_zone" {
  name  = "/${terraform.workspace}/front/services/elb/alb_zone"
  type  = "String"
  value = data.terraform_remote_state.elb_service.outputs.alb_zone
}

## certificate arn
resource "aws_ssm_parameter" "certifiacte_arn" {
  name  = "/${terraform.workspace}/front/services/elb/certifiacte_arn"
  type  = "String"
  value = "	arn:aws:acm:eu-central-1:648410456371:certificate/c46c4e19-264a-4c50-9f10-f85d95a182c3"
}