terraform {
  backend "s3" {
    bucket         = "terraform-state-lazzaro"
    dynamodb_table = "terraform-state-lock-ddb"
    region         = "eu-central-1"
    key            = "back/cicd/pipeline/pipeline.tfstate"
  }
}