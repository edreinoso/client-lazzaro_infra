resource "aws_ecr_repository" "ecr" {
  # name = "lazzaro-front-repo" # this is the todo app
  name = "lazzaro-front-repo-${terraform.workspace}" # this is the todo app
}