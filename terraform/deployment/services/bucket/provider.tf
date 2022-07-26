provider "aws" {
  region = "eu-central-1"
  default_tags {
    tags = {
      Environment   = terraform.workspace
      Creation_Date = timestamp()
    }
  }
}
