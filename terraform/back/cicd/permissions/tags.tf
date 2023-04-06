variable "name" {
  type    = string
  default = "backend-cicd-stack"
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
  default = "Setting up pipeline for lazzaro backend cluster"
}

variable "created-on" {
  type    = string
  default = "04_April_2023"
}
