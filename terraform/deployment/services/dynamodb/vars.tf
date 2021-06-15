variable "primary-key" {
  type    = string
  # default = "instanceId"
  default = "Client"
}

variable "attribute-type" {
  type    = string
  default = "S"
}

variable "read-write-capacity" {
  type    = string
  default = "5"
}

variable "billing" {
  type    = string
  default = "PROVISIONED"
}

variable "streams" {
  type    = string
  default = "true"
}

variable "stream-view" {
  type    = string
  default = "NEW_AND_OLD_IMAGES"
}

variable "ttl-enabled" {
  type    = string
  default = "false"
}
