# ONLY UNCOMMENT IN V2 TERRAFORM WORKSPACE

module "elb" {
  source         = "github.com/edreinoso/terraform_infrastructure_as_code/modules/compute/load-balancer/elb"
  elb-name       = "lb-${var.name}"
  # elb-name       = "lazzaro-back-alb-${terraform.workspace}"
  internal-elb   = var.internal-elb
  elb-type       = var.elb-type
  security-group = split(",", aws_security_group.elb-security-group.id)
  subnet-ids = [
    element(element(data.terraform_remote_state.network.outputs.pub-subnet-id-a, 0),0,),
    element(element(data.terraform_remote_state.network.outputs.pub-subnet-id-b, 0),0,)
  ]
  bucket-name = var.bucket-name
  tags = {
    Name          = "lb-${var.name}"
    Template      = var.template
    Purpose       = "Load balancer set up that sits in front of the cluster"
    Creation_Date = var.created-on
  }
}

module "target-group" {
  source = "github.com/edreinoso/terraform_infrastructure_as_code/modules/compute/load-balancer/tg"
  vpc-id         = element(data.terraform_remote_state.network.outputs.vpc-id, 1)
  elb-tg-name    = "${var.elb-tg-name}-${terraform.workspace}"
  # elb-tg-name    = "tg-${var.name}"
  tg-port        = var.tg-port
  deregistration = var.tg-deregister
  tg-target-type = var.tg-target-type
  tg-protocol    = "HTTP" # TCP
  path           = var.path # this is for the health checks

  tags = {
    Name          = "${var.elb-tg-name}-${terraform.workspace}"
    Template      = var.template
    Purpose       = "Target groups for fargate containers that are sitting behind ECS cluster"
    Creation_Date = var.created-on
  }
}

module "listener" {
 source            = "github.com/edreinoso/terraform_infrastructure_as_code/modules/compute/load-balancer/listener"
 elb-arn           = module.elb.elb-arn
 target-group-arn  = module.target-group.target-arn
 listener-port     = "8080"
 ssl-policy        = "ELBSecurityPolicy-2016-08"
 listener-protocol = "HTTPS"
 certificate-arn   = "arn:aws:acm:eu-central-1:648410456371:certificate/92887f51-ea40-418f-bd00-c6da4d3ec36d"
#  certificate-arn   = "arn:aws:acm:eu-central-1:648410456371:certificate/230ceb9c-1872-437d-bcdc-45e744833603"
}

resource "aws_s3_bucket" "s3" {
  bucket        = var.bucket-name
  # bucket        = "${var.bucket-name}-${terraform.workspace}"
  acl           = var.acl
  force_destroy = var.destroy

  policy = <<POLICY
{
 "Id": "Policy1566872708101",
 "Version": "2012-10-17",
 "Statement": [
     {
         "Sid": "Stmt1566872706748",
         "Action": [
             "s3:PutObject"
         ],
         "Effect": "Allow",
         "Resource": "arn:aws:s3:::${var.bucket-name}/AWSLogs/${var.account-id}/*",
         "Principal": {
             "AWS": [
                 "054676820928"
             ]
         }
     }
 ]
}
POLICY

  tags = {
    Name          = var.bucket-name
    Template      = var.template
    Purpose       = "S3 bucket for logging the load balancer connections"
    Creation_Date = var.created-on
  }
}

resource "aws_route53_record" "elb_record" {
 zone_id = "Z02368721HBX9HT236NI2"
 name    = "elb"
#  name    = "elb${lookup(var.r53-record-name, terraform.workspace)}"
 type    = "A"
 alias {
   name                   = module.elb.elb-dns-name
   zone_id                = module.elb.elb-zone-id
   evaluate_target_health = true
 }
}
