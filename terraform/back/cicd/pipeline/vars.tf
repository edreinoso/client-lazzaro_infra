variable "image" {
  type    = string
  default = "aws/codebuild/amazonlinux2-x86_64-standard:2.0"
}

variable "acct" {
  type    = string
  default = "648410456371"
}

variable "region" {
  type    = string
  default = "eu-central-1"
}

variable "location" {
  type    = string
  default = "https://github.com/Lazzaro-Social-Impact/lazzaro-entrepeneurs-api"
}

variable "username" {
  type    = string
  default = "edreinoso23"
}

variable "branch" {
  type = map(any)
  default = {
    prod               = "prod"
    pre                = "pre"
    entrepreneurs-pre  = "main"
    entrepreneurs-prod = "prod"
  }
}

variable "codestarconnection" {
  type = map(any)
  default = {
    prod               = "prod"
    pre                = "pre"
    entrepreneurs-pre  = "entrepreneurs-pre-connection"
    entrepreneurs-prod = "entrepreneurs-prod-connection"
  }
}

variable "source_namespace" {
  type    = string
  default = "SourceVariable"
}

variable "repository-name" {
  type = map(any)
  default = {
    prod               = "IvanSaiz/lazzaro-base-api"
    pre                = "IvanSaiz/lazzaro-base-api"
    entrepreneurs-pre  = "Lazzaro-Social-Impact/lazzaro-entrepreneurs-api"
    entrepreneurs-prod = "Lazzaro-Social-Impact/lazzaro-entrepreneurs-api"
  }
}
