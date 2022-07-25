resource "aws_sns_topic" "billing_alert" {
  name = "billing-alert-${terraform.workspace}"
}
