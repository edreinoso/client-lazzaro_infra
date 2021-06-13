data "terraform_remote_state" "ecr_arn" {
  backend = "s3"
  config = {
    bucket = "terraform-state-lazzaro"
    key    = "env:/${terraform.workspace}/back/infra/ecr_cluster_logs.tfstate"
    region = "eu-central-1"
  }
}


resource "aws_s3_bucket" "ecs-s3-pipeline" {
  bucket        = "lazzaro-back-s3-pipeline-artifacts-${terraform.workspace}"
  acl           = "private"
  force_destroy = true
}

resource "aws_iam_role" "ecs-build-role" {
  name = "lazzaro-back-iam-build-${terraform.workspace}"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "codebuild.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "ecs-build-policy" {
  role = aws_iam_role.ecs-build-role.name

  policy = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "secretsmanager:DescribeSecret",
                "secretsmanager:PutSecretValue",
                "secretsmanager:CreateSecret",
                "secretsmanager:DeleteSecret",
                "secretsmanager:CancelRotateSecret",
                "s3:ListBucket",
                "secretsmanager:ListSecretVersionIds",
                "secretsmanager:UpdateSecret",
                "s3:PutObject",
                "s3:GetObject",
                "secretsmanager:GetResourcePolicy",
                "secretsmanager:GetSecretValue",
                "secretsmanager:RestoreSecret",
                "secretsmanager:UpdateSecretVersionStage",
                "secretsmanager:RotateSecret",
                "ecr:*",
                "s3:GetObjectVersion"
            ],
            "Resource": [
                "${data.terraform_remote_state.ecr_arn.outputs.ecr_arn}",
                "arn:aws:secretsmanager:eu-central-1:648410456371:secret:dockerToken-XYhC3a",
                "${aws_s3_bucket.ecs-s3-pipeline.arn}",
                "${aws_s3_bucket.ecs-s3-pipeline.arn}/*"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "ecr:GetRegistryPolicy",
                "secretsmanager:GetRandomPassword",
                "logs:CreateLogStream",
                "ecr:DescribeRegistry",
                "ecr:GetAuthorizationToken",
                "ecr:DeleteRegistryPolicy",
                "logs:CreateLogGroup",
                "logs:PutLogEvents",
                "ecr:PutRegistryPolicy",
                "ecr:PutReplicationConfiguration"
            ],
            "Resource": "*"
        }
    ]
}
POLICY
}

resource "aws_iam_role" "ecs-pipeline-role" {
  name = "lazzaro-back-iam-pipeline-${terraform.workspace}"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "codepipeline.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "ecs-pipeline-policy" {
  role = aws_iam_role.ecs-pipeline-role.name

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
    "Action": [
        "iam:PassRole"
    ],
    "Resource": "*",
    "Effect": "Allow",
    "Condition": {
        "StringEqualsIfExists": {
            "iam:PassedToService": [
                "cloudformation.amazonaws.com",
                "elasticbeanstalk.amazonaws.com",
                "ec2.amazonaws.com",
                "ecs-tasks.amazonaws.com"
            ]
        }
    }
},
{
    "Action": [
        "codecommit:CancelUploadArchive",
        "codecommit:GetBranch",
        "codecommit:GetCommit",
        "codecommit:GetUploadArchiveStatus",
        "codecommit:UploadArchive"
    ],
    "Resource": "*",
    "Effect": "Allow"
},
{
    "Action": [
        "codedeploy:CreateDeployment",
        "codedeploy:GetApplication",
        "codedeploy:GetApplicationRevision",
        "codedeploy:GetDeployment",
        "codedeploy:GetDeploymentConfig",
        "codedeploy:RegisterApplicationRevision"
    ],
    "Resource": "*",
    "Effect": "Allow"
},
{
    "Action": [
        "codestar-connections:UseConnection"
    ],
    "Resource": "*",
    "Effect": "Allow"
},
{
    "Action": [
        "elasticbeanstalk:*",
        "ec2:*",
        "elasticloadbalancing:*",
        "autoscaling:*",
        "cloudwatch:*",
        "s3:*",
        "sns:*",
        "cloudformation:*",
        "rds:*",
        "sqs:*",
        "ecs:*"
    ],
    "Resource": "*",
    "Effect": "Allow"
},
{
    "Action": [
        "lambda:InvokeFunction",
        "lambda:ListFunctions"
    ],
    "Resource": "*",
    "Effect": "Allow"
},
{
    "Action": [
        "cloudformation:CreateStack",
        "cloudformation:DeleteStack",
        "cloudformation:DescribeStacks",
        "cloudformation:UpdateStack",
        "cloudformation:CreateChangeSet",
        "cloudformation:DeleteChangeSet",
        "cloudformation:DescribeChangeSet",
        "cloudformation:ExecuteChangeSet",
        "cloudformation:SetStackPolicy",
        "cloudformation:ValidateTemplate"
    ],
    "Resource": "*",
    "Effect": "Allow"
},
{
    "Action": [
        "codebuild:BatchGetBuilds",
        "codebuild:StartBuild",
        "codebuild:BatchGetBuildBatches",
        "codebuild:StartBuildBatch"
    ],
    "Resource": "*",
    "Effect": "Allow"
},
{
    "Effect": "Allow",
    "Action": [
        "cloudformation:ValidateTemplate"
    ],
    "Resource": "*"
},
{
    "Effect": "Allow",
    "Action": [
        "ecr:DescribeImages"
    ],
    "Resource": "*"
}
  ]
}
POLICY
}