data "terraform_remote_state" "build_permissions" {
  backend = "s3"
  config = {
    bucket = "terraform-state-lazzaro"
    key    = "env:/${terraform.workspace}/deployment/permissions/roles.tfstate"
    region = "eu-central-1"
  }
}

resource "aws_s3_bucket" "repository" {
  bucket        = "lazzaro-ongs-template-bucket-${terraform.workspace}"
  acl           = "private"
  force_destroy =  true
}

resource "aws_codebuild_project" "ecs_containers_build" {
  name         = "frontend-code-build-service-${terraform.workspace}"
  service_role = data.terraform_remote_state.build_permissions.outputs.codebuild_permission_arn

  artifacts {            
    type = "S3"
    location = "lazzaro-ongs-template-artifacts-${terraform.workspace}"
  }

  environment {                              
    type            = "LINUX_CONTAINER"      
    compute_type    = "BUILD_GENERAL1_SMALL" 
    image           = "aws/codebuild/amazonlinux2-x86_64-standard:2.0"
    privileged_mode = true
  }

  source {
    type     = "S3"
    location = "${aws_s3_bucket.repository.bucket}/"
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
    Name          = "frontend-code-build-service-${terraform.workspace}"
    Creation_Date = "14 June 2021"
  }
}