resource "aws_ecr_repository" "ecr" {
  name = "lazzaro-back-repo-${terraform.workspace}"
}