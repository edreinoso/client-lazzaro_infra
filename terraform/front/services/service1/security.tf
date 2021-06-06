data "terraform_remote_state" "ec2_bastion" {
    backend = "s3"
    config = {
        bucket = "terraform-state-lazzaro"
        key    = "env:/v2/lb-ec2.tfstate"
        region = "eu-central-1"
    }
}

data "terraform_remote_state" "load_balancer" {
    backend = "s3"
    config = {
        bucket = "terraform-state-lazzaro"
        key    = "services_lb_front.tfstate"
        region = "eu-central-1"
    }
}

##### FARGATE CONTAINERS SG #####
  resource "aws_security_group" "fargate-security-group" {
    name        = "tcp-sg-fargate-${var.name}"
    description = "Fargate security group for ${var.name} in ${terraform.workspace}"
    vpc_id      = element(data.terraform_remote_state.network.outputs.vpc-id, 1)

    tags = {
      Name          = "fargate-${var.name}"
      Template      = var.template
      Purpose       = "Security groups for fargate containers"
      Protocol      = "HTTP, TCP"
      Port          = "80, 8080"
      Creation_Date = var.created-on
    }
  }

  # resource "aws_security_group_rule" "fargate-security-group-rule-01" {
  #   type                     = "ingress"
  #   from_port                = 0
  #   to_port                  = 0
  #   protocol                 = "-1"
  #   cidr_blocks = ["0.0.0.0/0"]
  #   # source_security_group_id = [data.terraform_remote_state.load_balancer.outputs.elb-security-group]
  #   security_group_id        = aws_security_group.fargate-security-group.id
  #   description              = "Rules to allow traffic from load balancer to the fargate containers"
  # }
#   resource "aws_security_group_rule" "fargate-security-group-rulev2-01" {
#     type                     = "ingress"
#     from_port                = 8080
#     to_port                  = 8080
#     protocol                 = "tcp"
#     source_security_group_id = data.terraform_remote_state.load_balancer.outputs.elb-security-group
#     security_group_id        = aws_security_group.fargate-security-group.id
#     description              = "Rules to allow traffic from load balancer to the fargate containers"
#   }

  resource "aws_security_group_rule" "fargate-security-group-rule-02" {
    type                     = "ingress"
    from_port                = 0
    to_port                  = 0
    protocol                 = "-1"
    source_security_group_id = data.terraform_remote_state.load_balancer.outputs.elb-security-group # needs to be dynamic
    # source_security_group_id = "sg-0fe4e01770999b222" # needs to be dynamic
    security_group_id        = aws_security_group.fargate-security-group.id
    description              = "Rules to allow traffic coming into the cluster through the NAT host"
  }

  resource "aws_security_group_rule" "fargate-security-group-rulev2-02" {
    type                     = "ingress"
    from_port                = 80
    to_port                  = 80
    protocol                 = "tcp"
    source_security_group_id = data.terraform_remote_state.ec2_bastion.outputs.bastion-security-group
    security_group_id        = aws_security_group.fargate-security-group.id
    description              = "Rules to allow HTTP traffic coming into the cluster through the NAT host"
  }

  resource "aws_security_group_rule" "fargate-security-group-rule-03" {
    type                     = "ingress"
    from_port                = 443
    to_port                  = 443
    protocol                 = "tcp"
    source_security_group_id = data.terraform_remote_state.ec2_bastion.outputs.bastion-security-group
    security_group_id        = aws_security_group.fargate-security-group.id
    description              = "Rules to allow HTTPS traffic coming into the cluster through the NAT host"
  }

  resource "aws_security_group_rule" "fargate-security-group-rule-egress" {
    type              = "egress"
    from_port         = 0
    to_port           = 0
    protocol          = "-1"
    cidr_blocks       = ["0.0.0.0/0"]
    security_group_id = aws_security_group.fargate-security-group.id
  }

