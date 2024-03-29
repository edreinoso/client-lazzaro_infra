resource "aws_iam_role" "removeservice_permission" {
  name               = "frontend-delete-lambda-service-role-${terraform.workspace}"
  assume_role_policy = data.aws_iam_policy_document.trust_remove_policy.json

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
  # ddb
  inline_policy {
    name = "ddb"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "dynamodb:GetRecords",
            "dynamodb:GetShardIterator",
            "dynamodb:DescribeStream"
          ]
          Effect = "Allow"
          Resource = [
            "arn:aws:dynamodb:eu-central-1:648410456371:table/frontend-ddb-client/stream/2021-05-06T13:13:45.502",
            "arn:aws:dynamodb:eu-central-1:648410456371:table/frontend-ddb-client-pre/stream/2021-06-14T18:56:04.772"
          ]
        },
        {
          Action = [
            "dynamodb:ListStreams"
          ]
          Effect = "Allow"
          Resource = [
            "arn:aws:dynamodb:eu-central-1:648410456371:table/frontend-ddb-client",
            "arn:aws:dynamodb:eu-central-1:648410456371:table/frontend-ddb-client-pre"
          ]
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
          Action = [
            "logs:DeleteLogGroup"
          ]
          Effect = "Allow"
          Resource = [
            "arn:aws:logs:eu-central-1:648410456371:*"
          ]
        },
        {
          Action = [
            "elasticloadbalancing:DeleteTargetGroup",
            "ecs:DeregisterTaskDefinition",
            "ecs:DeleteService"
          ]
          Effect   = "Allow"
          Resource = "*"
        },
        {
          Action = [
            "elasticloadbalancing:DeleteListener",
            "elasticloadbalancing:DeleteRule"
          ]
          Effect   = "Allow"
          Resource = "*"
        },
        {
          Action = [
            "codebuild:BatchDeleteBuilds",
            "ecr:BatchDeleteImage",
            "s3:DeleteObject"
          ]
          Effect = "Allow"
          Resource = [
            "arn:aws:ecr:eu-central-1:648410456371:repository/lazzaro-front-repo",
            "arn:aws:ecr:eu-central-1:648410456371:repository/lazzaro-front-repo-pre",
            "arn:aws:s3:::lazzaro-ongs-template-artifacts-${terraform.workspace}/*",
            "arn:aws:codebuild:eu-central-1:648410456371:project/frontend-code-build-service-${terraform.workspace}"
          ]
        },
        {
          Action = [
            "route53:ChangeResourceRecordSets"
          ]
          Effect   = "Allow"
          Resource = "arn:aws:route53:::hostedzone/Z05961833L2QBW4GTOR3X"
        },
        {
          Action = [
            "sqs:SendMessage"
          ]
          Effect   = "Allow"
          Resource = "arn:aws:sqs:eu-central-1:648410456371:lazzaro-sqs-service-${terraform.workspace}"
        }
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
          Action = [
            "ssm:GetParametersByPath",
            "ssm:GetParameter"
          ]
          Effect   = "Allow"
          Resource = "arn:aws:ssm:eu-central-1:648410456371:parameter/*"
        }
      ]
    })
  }
  # events
  inline_policy {
    name = "events"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "events:PutRule",
            "events:PutTargets"
          ]
          Effect   = "Allow"
          Resource = ["*"]
        },
        {
          Action = [
            "lambda:AddPermission",
          ]
          Effect   = "Allow"
          Resource = ["*"] # elb stabilizer lambda arn
        }
      ]
    })
  }
}

data "aws_iam_policy_document" "trust_remove_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}
