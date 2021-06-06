resource "aws_codebuild_project" "ecs_containers_build" {
  name         = "${var.name}-build"
  service_role = aws_iam_role.ecs-build-role.arn

  artifacts {             # required
    type = "NO_ARTIFACTS" # required
  }

  environment {                              # required
    type            = "LINUX_CONTAINER"      # required
    compute_type    = "BUILD_GENERAL1_SMALL" # requried
    image           = var.image              # required
    privileged_mode = true
    environment_variable {
      name  = "aws_account_id"
      value = var.acct
    }
    environment_variable {
      name  = "aws_default_region"
      value = var.region
    }
    environment_variable {
      name  = "username"
      value = var.username
    }
    # environment_variable {
    #   name  = "environment"
    #   value = ""
    # }
  }

  source {              # required
    type     = "GITHUB" # required
    location = var.location
    auth {
      type = "OAUTH" # required
    }
  }

  logs_config {
    cloudwatch_logs {
      status = "ENABLED"
    }

    s3_logs {
      encryption_disabled = false
      status              = "DISABLED"
    }
  }

  tags = {
    Name          = "${var.name}-build"
    Template      = var.template
    Purpose       = var.purpose
    Creation_Date = var.created-on
  }
}

resource "aws_codepipeline" "ecs_container_pipeline" {
  name     = "${var.name}-pipeline"              # required
  role_arn = aws_iam_role.ecs-pipeline-role.arn # required

  artifact_store {                       # required
    location = aws_s3_bucket.ecs-s3-pipeline.bucket # what is this?
    type     = "S3"
  }

  # Source
  stage {
    name = "Source" # required

    action { # required
      name             = "Source"
      category         = "Source"
      owner            = "AWS"
      provider         = "CodeStarSourceConnection"
      version          = "1"
      output_artifacts = ["source_output_ecs_cluster"]

      configuration = {
        ConnectionArn    = "arn:aws:codestar-connections:us-east-1:648410456371:connection/dc980cdf-217c-4b16-9361-21001850438d"
        FullRepositoryId = "IvanSaiz/lazzaro-base-api"
        BranchName       = "master"
      }
    }
  }

  # Build
  stage {
    name = "Build"

    action {
      name             = "Build"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      input_artifacts  = ["source_output_ecs_cluster"]
      output_artifacts = ["build_output_ecs_cluster"]
      version          = "1"

      configuration = {
        ProjectName = "${var.name}-build"
      }
    }
  }

  # Deploy
  stage {
    name = "Deploy"

    action {
      category        = "Deploy"
      name            = "Deploy"
      owner           = "AWS"
      provider        = "ECS"
      version         = "1"
      input_artifacts = ["build_output_ecs_cluster"]
      
      configuration = {
        "ClusterName" = "lazzaro-cluster"
        "ServiceName" = "service-v2-ecs-cluster" # this need to be dynamic
        "FileName"    = "imagedefinitions.json"
      }
    }
  }

  tags = {
    Name          = "${var.name}-pipeline"
    Template      = var.template
    Creation_Date = var.created-on
    Purpose       = var.purpose
  }
}
