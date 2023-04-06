# This is the role under which ECS will execute our task. This role becomes more important
# as we add integrations with other AWS services later on.

# The assume_role_policy field works with the following aws_iam_policy_document to allow
# ECS tasks to assume this role we're creating.
resource "aws_iam_role" "ecs-api-task-execution-role" {
 name               = "task-execution-role-${var.name}"
 assume_role_policy = data.aws_iam_policy_document.ecs-task-assume-role.json
}

data "aws_iam_policy_document" "ecs-task-assume-role" {
 statement {
   actions = ["sts:AssumeRole"]

   principals {
     type        = "Service"
     identifiers = ["ecs-tasks.amazonaws.com"]
   }
 }
}

# # Normally we'd prefer not to hardcode an ARN in our Terraform, but since this is an AWS-managed
# # policy, it's okay.
data "aws_iam_policy" "ecs-task-execution-role" {
 arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# # Attach the above policy to the execution role.
resource "aws_iam_role_policy_attachment" "ecs-task-execution-role" {
 role       = aws_iam_role.ecs-api-task-execution-role.name
 policy_arn = data.aws_iam_policy.ecs-task-execution-role.arn
}