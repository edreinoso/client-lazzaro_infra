resource "aws_s3_bucket" "ecs-s3-pipeline" {
  bucket = "${var.name}-pipeline-bucket"
  acl    = "private"
}

resource "aws_iam_role" "ecs-build-role" {
  name = "${var.name}-build-role"

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
                "arn:aws:ecr:eu-central-1:648410456371:repository/ecr-dev-ecs-cluster",
                "arn:aws:secretsmanager:eu-central-1:648410456371:secret:dockerToken-XYhC3a",
                "arn:aws:s3:::ecs-cluster-pipeline-bucket",
                "arn:aws:s3:::ecs-cluster-pipeline-bucket/*"
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
  name = "${var.name}-pipeline-role"

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
        "opsworks:CreateDeployment",
        "opsworks:DescribeApps",
        "opsworks:DescribeCommands",
        "opsworks:DescribeDeployments",
        "opsworks:DescribeInstances",
        "opsworks:DescribeStacks",
        "opsworks:UpdateApp",
        "opsworks:UpdateStack"
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
        "devicefarm:ListProjects",
        "devicefarm:ListDevicePools",
        "devicefarm:GetRun",
        "devicefarm:GetUpload",
        "devicefarm:CreateUpload",
        "devicefarm:ScheduleRun"
    ],
    "Resource": "*"
},
{
    "Effect": "Allow",
    "Action": [
        "servicecatalog:ListProvisioningArtifacts",
        "servicecatalog:CreateProvisioningArtifact",
        "servicecatalog:DescribeProvisioningArtifact",
        "servicecatalog:DeleteProvisioningArtifact",
        "servicecatalog:UpdateProduct"
    ],
    "Resource": "*"
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
},
{
    "Effect": "Allow",
    "Action": [
        "states:DescribeExecution",
        "states:DescribeStateMachine",
        "states:StartExecution"
    ],
    "Resource": "*"
},
{
    "Effect": "Allow",
    "Action": [
        "appconfig:StartDeployment",
        "appconfig:StopDeployment",
        "appconfig:GetDeployment"
    ],
    "Resource": "*"
}
  ]
}
POLICY
}