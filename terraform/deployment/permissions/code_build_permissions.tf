resource "aws_iam_role" "codebuild_permissions" {
  name               = "frontend-code-build-service-role-${terraform.workspace}"
  assume_role_policy = data.aws_iam_policy_document.trust_codebuild_policy.json

  # logs
  inline_policy {
    name = "logs"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ]
          Effect   = "Allow"
          Resource = "*"
        },
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
          Action   = [
            "s3:PutObject",
            "s3:GetObject",
            "s3:GetObjectVersion",
            "s3:ListBucket"
          ]
          Effect   = "Allow"
          Resource = "*"
        },
      ]
    })
  }
  # ecr 1
  inline_policy {
    name = "ecr_1"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = [
            "ecr:BatchGetImage",
            "ecr:BatchCheckLayerAvailability",
            "ecr:CompleteLayerUpload",
            "ecr:DescribeImages",
            "ecr:DescribeRepositories",
            "ecr:GetDownloadUrlForLayer",
            "ecr:InitiateLayerUpload",
            "ecr:ListImages",
            "ecr:PutImage",
            "ecr:UploadLayerPart"
          ]
          Effect   = "Allow"
          Resource = [
              "arn:aws:ecr:eu-central-1:648410456371:repository/lazzaro-front-repo",
              "arn:aws:ecr:eu-central-1:648410456371:repository/lazzaro-front-repo-pre",
          ]
        },
      ]
    })
  }
  # ecr 2
  inline_policy {
    name = "ecr_2"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = [
            "ecr:GetAuthorizationToken"
          ]
          Effect   = "Allow"
          Resource = "*"
        },
      ]
    })
  }
  # secrets manager
  inline_policy {
    name = "secrets_manager"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = [
            "secretsmanager:DescribeSecret",
            "secretsmanager:PutSecretValue",
            "secretsmanager:CreateSecret",
            "secretsmanager:DeleteSecret",
            "secretsmanager:CancelRotateSecret",
            "secretsmanager:ListSecretVersionIds",
            "secretsmanager:UpdateSecret",
            "secretsmanager:GetResourcePolicy",
            "secretsmanager:GetSecretValue",
            "secretsmanager:RestoreSecret",
            "secretsmanager:UpdateSecretVersionStage",
            "secretsmanager:RotateSecret"
          ]
          Effect   = "Allow"
          Resource = [
              "arn:aws:secretsmanager:eu-central-1:648410456371:secret:dockerToken-XYhC3a"
          ]
        },
      ]
    })
  }
}

data "aws_iam_policy_document" "trust_codebuild_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["codebuild.amazonaws.com"]
    }
  }
}