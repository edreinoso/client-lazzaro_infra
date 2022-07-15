resource "aws_sns_topic_subscription" "edgardo_subscriber" {
  topic_arn = aws_sns_topic.billing_alert.arn
  protocol  = "email"
  endpoint  = "edgardojesus16@gmail.com"
}

resource "aws_sns_topic_subscription" "ivan_subscriber" {
  topic_arn = aws_sns_topic.billing_alert.arn
  protocol  = "email"
  endpoint  = "ivan@lazzaro.io"
}
