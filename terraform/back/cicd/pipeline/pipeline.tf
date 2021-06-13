data "terraform_remote_state" "cicd_permissions" {
  backend = "s3"
  config = {
    bucket = "terraform-state-lazzaro"
    key    = "env:/${terraform.workspace}/back/cicd/permissions/permissions.tfstate"
    region = "eu-central-1"
  }
}

resource "aws_codebuild_project" "ecs_containers_build" {
  name         = "lazzaro-back-build-${terraform.workspace}"
  service_role = data.terraform_remote_state.cicd_permissions.outputs.code_build_role_arn

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
    #   value = "#{SourceVariables.BranchName}"
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
    Name          = "lazzaro-back-build-${terraform.workspace}"
    Template      = var.template
    Purpose       = var.purpose
    Creation_Date = var.created-on
  }
}

resource "aws_codepipeline" "ecs_container_pipeline" {
  name     = "lazzaro-back-pipeline-${terraform.workspace}"
  role_arn = data.terraform_remote_state.cicd_permissions.outputs.code_pipeline_role_arn

  artifact_store {
    location = data.terraform_remote_state.cicd_permissions.outputs.bucket_location
    type     = "S3"
  }

  # Source
  stage {
    name = "Source" # required

    action { # required
      category         = "Source"
      name             = "GithubCode"
      namespace        = var.source_namespace
      owner            = "AWS"
      provider         = "CodeStarSourceConnection"
      version          = "1"
      output_artifacts = ["backend_${terraform.workspace}_source_output"]
      configuration = {
        ConnectionArn    = "arn:aws:codestar-connections:us-east-1:648410456371:connection/dc980cdf-217c-4b16-9361-21001850438d"
        FullRepositoryId = "IvanSaiz/lazzaro-base-api"
        BranchName       = "${lookup(var.branch, terraform.workspace)}"
        # BranchName       = "master"
        # "OutputArtifactFormat" = "CODE_ZIP"
      }
    }
  }

  # Build
  stage {
    name = "Build"

    action {
      category         = "Build"
      name             = "DockerBuild"
      owner            = "AWS"
      provider         = "CodeBuild"
      input_artifacts  = ["backend_${terraform.workspace}_source_output"]
      output_artifacts = ["backend_${terraform.workspace}_build_output"]
      version          = "1"

      ## some variables here for the environment

      configuration = {
        ProjectName         = "lazzaro-back-build-${terraform.workspace}"
        EnvironmentVariables = "[{\"name\":\"environment\",\"value\":\"#{${var.source_namespace}.BranchName}\",\"type\":\"PLAINTEXT\"}]"
      }
    }
  }

  # Deploy
  stage {
    name = "Deploy"

    action {
      category        = "Deploy"
      name            = "ECSDeploy"
      owner           = "AWS"
      provider        = "ECS"
      version         = "1"
      input_artifacts = ["backend_${terraform.workspace}_build_output"]

      configuration = {
        "ClusterName" = "lazzaro-back-cluster-${terraform.workspace}"
        "ServiceName" = "lazzaro-back-service-${terraform.workspace}"
        "FileName"    = "imagedefinitions.json" # why do I need this?
      }
    }
  }

  tags = {
    Name          = "lazzaro-back-pipeline-${terraform.workspace}"
    Template      = var.template
    Creation_Date = var.created-on
    Purpose       = var.purpose
  }
}

