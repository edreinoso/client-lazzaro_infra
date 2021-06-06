data "terraform_remote_state" "load_balancer" {
  backend = "s3"
  config = {
    bucket = "terraform-state-lazzaro"
    key    = "env:/v2/lb-ec2.tfstate"
    # key    = "env:/${terraform.workspace}/lb-ec2.tfstate"
    region = "eu-central-1"
  }
}

data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "terraform-state-lazzaro"
    key    = "env:/v1/network.tfstate"
    region = "eu-central-1"
  }
}

# data "terraform_remote_state" "vpc" {
#   backend = "s3"
#   config = {
#     bucket = "terraform-state-lazzaro"
#     key    = "env:/v2/terraform.tfstate"
#     region = "us-east-1"
#   }
# }
