resource "aws_iam_role" "testservice_permission" {
  name               = "frontend-test-service-role-${terraform.workspace}"
  assume_role_policy = data.aws_iam_policy_document.trust_lambda_create_policy.json

  # logs
  inline_policy {
    name = "logs"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = [
            "logs:CreateLogGroup",
            "logs:PutLogEvents",
            "logs:CreateLogStream"
          ]
          Effect   = "Allow"
          Resource = "*"
        },
        # {
        #   Action   = [
        #   ]
        #   Effect   = "Allow"
        #   Resource: [
        #     "arn:aws:logs:eu-central-1:648410456371:log-group:frontend-ecs-services-${terraform.workspace}-createservice:log-stream:*",
        #     "arn:aws:logs:eu-central-1:648410456371:log-group:frontend-ecs-services-${terraform.workspace}-createservice"
        #   ]
        # },
      ]
    })
  }
  # ssm
  inline_policy {
    name = "ssm"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = [
            "ssm:GetParametersByPath"
          ]
          Effect   = "Allow"
          Resource = "arn:aws:ssm:eu-central-1:648410456371:parameter/*"
        }
      ]
    })
  }
}

data "aws_iam_policy_document" "trust_lambda_test_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}