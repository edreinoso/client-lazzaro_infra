resource "aws_ecr_repository" "ecr" {
  name = "lazzaro-back-repo-${terraform.workspace}" # this is the todo app
  # name = "ecr-${lookup(var.hello, terraform.workspace)}-ecs-cluster" # v2 - needs to be deprecated
}

# this variable is going to be deprecated as well
variable "hello" {
  type = map
  default = {
    # v1 and v2 two will eventually be deprecated
    v1 = "tst"
    v2 = "dev"
    prod = "prod"
    pre = "pre"
  }
}