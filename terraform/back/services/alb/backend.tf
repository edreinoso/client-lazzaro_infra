terraform {
  backend "s3" {
    bucket         = "terraform-state-lazzaro"
    dynamodb_table = "terraform-state-lock-ddb"
    region         = "eu-central-1"
    # key            = "lb-ec2.tfstate" # this would come to be the name of the file
    key            = "back/services/alb/alb.tfstate" # this would come to be the name of the file
  }
}