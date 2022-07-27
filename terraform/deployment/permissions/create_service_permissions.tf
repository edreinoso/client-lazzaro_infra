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
            "ec2:CreateTags",
            "ec2:DescribeSecurityGroups",
          ]
          Effect   = "Allow"
          Resource = "*"
        }
      ]
    })
  }
  # s3
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
            "arn:aws:s3:::frontend-deployment-resource-management-with-s3/*",
            # it would be nice if this was dynamic
            # "arn:aws:s3:::${data.terraform_remote_state.s3_deployment_bucket.outputs.s3_name}/*",
          ]
        },
        {
          Action = [
            "s3:GetObject",
            "s3:ListBucket"
          ]
          Effect = "Allow"
          Resource = [
            "*"
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

  # dashboard
  inline_policy {
    name = "cwd"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "cloudwatch:GetDashboard",
            "cloudwatch:PutDashboard"
          ]
          Effect   = "Allow"
          Resource = "arn:aws:cloudwatch::648410456371:dashboard/frontend-clients-dashboards-${terraform.workspace}"
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
