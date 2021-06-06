variable "name" {
  type    = string
  default = "ecs-cluster"
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
  default = "setting up pipeline for lazzaro ecs cluster backend"
}

variable "created-on" {
  type    = string
  default = "26_February_2021"
}
