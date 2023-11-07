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
  service_role = "arn:aws:iam::648410456371:role/lazzaro-back-iam-build-${terraform.workspace}"

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
    environment_variable {
      name  = "environment"
      value = "#{SourceVariables.BranchName}"
    }
  }

  source {              # required
    type     = "GITHUB" # required
    location = var.location
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

resource "aws_codestarconnections_connection" "codestar_connection" {
  name          = lookup(var.codestarconnection, terraform.workspace)
  provider_type = "GitHub"
}

resource "aws_codepipeline" "ecs_container_pipeline" {
  name     = "lazzaro-back-pipeline-${terraform.workspace}"
  role_arn = "arn:aws:iam::648410456371:role/lazzaro-back-iam-pipeline-${terraform.workspace}"

  artifact_store {
    location = "lazzaro-back-s3-pipeline-artifacts-${terraform.workspace}"
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
        # this is where the problem lays
        # then the question becomes, what can I do to change this?
        # 1) check codestar on the console
        # 2) use cli to check codestar
        # 3) create a codestar connection with terraform
        # codestar connection needs to be dynamic
        ConnectionArn          = "arn:aws:codestar-connections:eu-central-1:648410456371:connection/664d6f12-ffd6-40aa-ac43-f3f64081be21"
        FullRepositoryId       = "${lookup(var.repository-name, terraform.workspace)}"
        BranchName             = "${lookup(var.branch, terraform.workspace)}"
        "OutputArtifactFormat" = "CODE_ZIP"
        # BranchName       = "master"
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
        ProjectName = "lazzaro-back-build-${terraform.workspace}"
        # this needs to be changed depending on the environment
        # EnvironmentVariables = "[{\"name\":\"environment\",\"value\":\"prod\",\"type\":\"PLAINTEXT\"}]"
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

