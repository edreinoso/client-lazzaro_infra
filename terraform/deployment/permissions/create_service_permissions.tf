resource "aws_iam_role" "createservice_permission" {
  name               = "frontend-create-lambda-service-role-${terraform.workspace}"
  assume_role_policy = data.aws_iam_policy_document.trust_lambda_create_policy.json

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
  # ddb
  inline_policy {
    name = "ddb"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "dynamodb:Scan",
            "dynamodb:Query",
            "dynamodb:UpdateItem",
          ]
          Effect = "Allow"
          Resource = [
            "arn:aws:dynamodb:eu-central-1:648410456371:table/frontend-ddb-client",
            "arn:aws:dynamodb:eu-central-1:648410456371:table/frontend-ddb-client-pre",
          ]
        },
      ]
    })
  }
  # create
  inline_policy {
    name = "create"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "elasticloadbalancing:CreateTargetGroup",
            "elasticloadbalancing:DescribeListeners",
            "elasticloadbalancing:DescribeRules",
            "elasticloadbalancing:DescribeTargetGroups",
            "elasticloadbalancing:CreateRule",
          ]
          Effect   = "Allow"
          Resource = "*"
        },
        #need to come back and check
        {
          Action = [
            "elasticloadbalancing:CreateListener",
          ]
          Effect = "Allow"
          Resource = [
            "arn:aws:elasticloadbalancing:eu-central-1:648410456371:loadbalancer/app/*/*" # warning, hardcoded value
          ]
        },
        {
          Action = [
            "iam:PassRole",
          ]
          Effect   = "Allow"
          Resource = "*"
        },
        {
          Action = [
            "ecs:RegisterTaskDefinition",
            "ecs:CreateService"
          ]
          Effect   = "Allow"
          Resource = "*"
        },
        {
          Action = [
            "route53:ChangeResourceRecordSets",
          ]
          Effect = "Allow"
          Resource = [
            "arn:aws:route53:::hostedzone/Z05961833L2QBW4GTOR3X"
          ]
        },
        {
          Action = [
            "ec2:CreateTags",
            "ec2:CreateSecurityGroup",
            "ec2:AuthorizeSecurityGroupIngress",
          ]
          Effect = "Allow"
          Resource = [
            "arn:aws:ec2:eu-central-1:648410456371:security-group/*",
            "arn:aws:ec2:eu-central-1:648410456371:vpc/*"
          ]
        },
        {
          Action = [
            "ec2:DescribeSecurityGroups",
          ]
          Effect   = "Allow"
          Resource = "*"
        },
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
            "ssm:GetParametersByPath"
          ]
          Effect   = "Allow"
          Resource = "arn:aws:ssm:eu-central-1:648410456371:parameter/*"
        }
      ]
    })
  }
}

data "aws_iam_policy_document" "trust_lambda_create_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}
