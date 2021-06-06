# # # Log groups hold logs from our app.
resource "aws_cloudwatch_log_group" "ecs-cloudwatch-logs" {
 name = "/ecs/back/${terraform.workspace}/"
#  name = "/ecs/${terraform.workspace}/" # going to be deprecated
}