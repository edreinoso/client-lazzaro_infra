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
  default = "setting up network for lazzaro ecs cluster backend"
}

variable "created-on" {
  type    = string
  default = "4_February_2021"
}
