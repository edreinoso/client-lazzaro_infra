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
  default = "https://github.com/IvanSaiz/lazzaro-base-api"
}

variable "username" {
  type    = string
  default = "edreinoso23"
}

variable "branch" {
  type = map
  default = {
    prod = "prod"
    pre = "pre"
    nfts-pre = "nfts-pre"
  }
}

variable "source_namespace" {
  type = string
  default = "SourceVariable"
}