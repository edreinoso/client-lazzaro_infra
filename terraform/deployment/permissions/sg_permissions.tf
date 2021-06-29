resource "aws_iam_role" "sg_function_permission" {
  name               = "frontend-delete-sg-service-role-${terraform.workspace}"
  assume_role_policy = data.aws_iam_policy_document.trust_sg_policy.json

  # logs
  inline_policy {
    name = "logs"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "logs:CreateLogGroup",
            "logs:PutLogEvents",
            "logs:CreateLogStream"
          ]
          Effect   = "Allow"
          Resource = "*"
        }
      ]
    })
  }
  # sqs
  inline_policy {
    name = "sqs"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "sqs:DeleteMessage",
            "sqs:GetQueueAttributes",
            "sqs:ReceiveMessage"
          ]
          Effect   = "Allow"
          Resource = "arn:aws:sqs:eu-central-1:648410456371:lazzaro-sqs-service-${terraform.workspace}"
        },
      ]
    })
  }
  # remove
  inline_policy {
    name = "remove"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = [
            "ec2:DeleteSecurityGroup"
          ]
          Effect   = "Allow"
          Resource = [
            "arn:aws:ec2:eu-central-1:648410456371:security-group/*",
            "arn:aws:ec2:eu-central-1:648410456371:vpc/*"
          ]
        },
      ]
    })
  }
}

data "aws_iam_policy_document" "trust_sg_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}
