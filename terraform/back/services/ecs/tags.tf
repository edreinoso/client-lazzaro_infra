variable "region" {
  type = string
  default = "eu-central-1"
}

variable "name" {
  type    = string
  default = "backend-ecs-stack"
}

variable "template" {
  type    = string
  default = "containarized_backend"
}

variable "application" {
  type    = string
  default = ""
}

variable "purpose" {
  type    = string
  default = "setting up network for lazzaro ecs cluster backend"
}

variable "created-on" {
  type    = string
  default = "5_February_2021"
}
