data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "terraform-state-lazzaro"
    key    = "env:/v1/network.tfstate"
    region = "eu-central-1"
  }
}

module "elb" {
  source         = "github.com/edreinoso/terraform_infrastructure_as_code/modules/compute/load-balancer/elb"
  elb-name       = "lb-${terraform.workspace}-${lookup(var.name, terraform.workspace)}"
  internal-elb   = var.internal-elb
  elb-type       = var.elb-type
  # security-group = split(",", data.terraform_remote_state.load_balancer.outputs.elb-security-group)
  security-group = split(",", aws_security_group.elb-security-group.id)
  subnet-ids = [
    element(element(data.terraform_remote_state.network.outputs.pub-subnet-id-a, 0),0,),
    element(element(data.terraform_remote_state.network.outputs.pub-subnet-id-b, 0),0,)
  ]
  bucket-name = var.bucket-name
  tags = {
    Name          = "lb-${terraform.workspace}--${lookup(var.name, terraform.workspace)}"
    Template      = var.template
    Purpose       = "Load balancer set up that sits in front of the cluster"
    Environment = terraform.workspace
    Creation_Date = var.created-on
  }
}

resource "aws_s3_bucket" "s3" {
  bucket        = var.bucket-name
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
    Environment = terraform.workspace
    Creation_Date = var.created-on
  }
}
