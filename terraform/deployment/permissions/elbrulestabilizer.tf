resource "aws_iam_role" "elbrulestabilizer_permission" {
  name               = "frontend-elbrulestabilizer-lambda-service-role-${terraform.workspace}"
  assume_role_policy = data.aws_iam_policy_document.trust_lambda_fargate_service_policy.json

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
        },
      ]
    })
  }
  # update service
  inline_policy {
    name = "elb"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "elasticloadbalancing:DescribeListener",
          ]
          Effect   = "Allow"
          Resource = "*"
        },
      ]
    })
  }
  # stop rds instance
  inline_policy {
    name = "s3"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "s3:PutObject",
          ]
          Effect = "Allow"
          Resource = [
            "arn:aws:s3:::deployment-resources-pre/*",
          ]
        },
        {
          Action = [
            "kms:Decrypt",
            "kms:GenerateDataKey"
          ]
          Effect = "Allow"
          Resource = [
            "*"
          ]
        }
      ]
    })
  }
}

data "aws_iam_policy_document" "trust_lambda_elbrulestabilizer_service_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}
