# interesting question would be to separate teh logging of
# different services inside the cluster
resource "aws_cloudwatch_log_group" "ecs-cloudwatch-logs" {
 name = "/ecs/front/"
}