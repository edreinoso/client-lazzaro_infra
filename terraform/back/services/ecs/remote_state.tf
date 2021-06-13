data "terraform_remote_state" "load_balancer" {
  backend = "s3"
  config = {
    bucket = "terraform-state-lazzaro"
    key    = "env:/${terraform.workspace}/back/services/alb/alb.tfstate"
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
