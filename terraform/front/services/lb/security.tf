##### ELB SG #####
  resource "aws_security_group" "elb-security-group" {
    name        = "elb-sg-${terraform.workspace}-${lookup(var.name, terraform.workspace)}"
    description = "ELB security group for ${lookup(var.name, terraform.workspace)} in ${terraform.workspace}"
    vpc_id      = element(data.terraform_remote_state.network.outputs.vpc-id, 1)

    tags = {
      Name          = "lb-${terraform.workspace}-${lookup(var.name, terraform.workspace)}"
      Template      = var.template
      Purpose       = "Security groups for load balancer"
      Protocol      = "HTTPS"
      Creation_Date = var.created-on
      Environment = terraform.workspace
    }
  }

  resource "aws_security_group_rule" "elb-security-group-rule-01" {
    type              = "ingress"
    from_port         = 0
    to_port           = 0
    protocol          = "-1"
    cidr_blocks       = ["0.0.0.0/0"]
    security_group_id = aws_security_group.elb-security-group.id
    description       = "Rules that are going to allow traffic to the load balancer"
  }

  resource "aws_security_group_rule" "elb-security-group-rule-egress" {
    type              = "egress"
    from_port         = 0
    to_port           = 0
    protocol          = "-1"
    cidr_blocks       = ["0.0.0.0/0"]
    security_group_id = aws_security_group.elb-security-group.id
  }
