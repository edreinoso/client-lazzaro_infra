### VPC ###
variable "vpc-cidr" {
  type = map

  default = {
    v1 = "10.0.0.0/24"
  }
}

variable "vpc-dns-hostname" {
  type    = string
  default = true
}

variable "vpc-dns-support" {
  type    = string
  default = true
}

### Flow logs ###
variable "log-destination" {
  type    = string
  default = "/vpc/ecs/flow-logs" #for now this would be example
}

variable "traffic-type" {
  type    = string
  default = "ALL"
}

variable "max-aggregation-interval" {
  type    = string
  default = "600"
}

# ### ROUTE TABLES ###
variable "public-route-table" {
  type    = string
  default = "public-route-table"
}

variable "private-route-table" {
  type    = string
  default = "private-route-table"
}

variable "destinationRoute" {
  type    = string
  default = "0.0.0.0/0"
}
