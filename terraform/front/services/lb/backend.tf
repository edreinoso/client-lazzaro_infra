terraform {
  backend "s3" {
    bucket         = "terraform-state-lazzaro"
    dynamodb_table = "terraform-state-lock-ddb"
    region         = "eu-central-1"
    key            = "services_lb_front.tfstate" # this would come to be the name of the file
  }
}