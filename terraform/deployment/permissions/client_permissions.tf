resource "aws_iam_role" "client_permission" {
  name               = "frontend-client-gateway-role-${terraform.workspace}"
  assume_role_policy = data.aws_iam_policy_document.trust_lambda_policy.json

  # logs
  inline_policy {
    name = "logs"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = [
            "logs:CreateLogGroup"
          ]
          Effect   = "Allow"
          Resource = "arn:aws:logs:eu-central-1:648410456371:*"
        },
        {
          Action   = [
            "logs:PutLogEvents",
            "logs:CreateLogStream"
          ]
          Effect   = "Allow"
          Resource = "arn:aws:logs:eu-central-1:648410456371:log-group:/aws/lambda/frontend-ecs-services-${terraform.workspace}-client:*"
        },
      ]
    })
  }
  # codebuild
  inline_policy {
    name = "codebuild"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = [
            "codebuild:StartBuild"
          ]
          Effect   = "Allow"
          Resource = [
            "arn:aws:codebuild:eu-central-1:648410456371:project/frontend-code-build-service-${terraform.workspace}"
          ]
        },
      ]
    })
  }
  # ddb
  inline_policy {
    name = "ddb"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = [
            "dynamodb:PutItem",
            "dynamodb:DeleteItem",
            "dynamodb:UpdateItem",
            "dynamodb:Query"
          ]
          Effect   = "Allow"
          Resource = [
              "arn:aws:dynamodb:eu-central-1:648410456371:table/frontend-ddb-client",
              "arn:aws:dynamodb:eu-central-1:648410456371:table/frontend-ddb-client-pre",
          ]
        },
      ]
    })
  }
}

data "aws_iam_policy_document" "trust_lambda_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}