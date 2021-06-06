# terraform {
#   backend "s3" {
#     bucket         = "terraform-state-lazzaro"
#     dynamodb_table = "terraform-state-lock-ddb"
#     region         = "eu-central-1"
#     key            = "infra_back.tfstate" # this would come to be the name of the file
#     # key            = "infra_front.tfstate" # this would come to be the name of the file
#   }
# }