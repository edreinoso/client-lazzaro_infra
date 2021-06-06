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

### SUBNETS ###
variable "region" {
  type    = string
  default = "eu-central-"
}

# SUBNETS: PUBLIC #
variable "public-subnet-cidr-1-a" {
  type = map

  default = {
    v1 = "10.0.0.0/27,10.0.0.96/27"
    # v1 = "10.0.0.0/27"
  }
}

variable "public-subnet-name-1-a" {
  type = map

  default = {
    v1 = "public-subnet-01-a,public-subnet-02-a"
    # v1 = "public-subnet-01-a"
  }
}

variable "public-subnet-cidr-1-b" {
  type = map

  default = {
    v1 = "10.0.0.32/27,10.0.0.160/27"
    # v1 = "10.0.0.32/27"
  }
}

variable "public-subnet-name-1-b" {
  type = map

  default = {
    v1 = "public-subnet-01-b,public-subnet-02-b"
    # v1 = "public-subnet-01-b"
  }
}

# SUBNETS: PRIVATE #
variable "private-type" {
  type    = string
  default = "private"
}

variable "main-subnet" {
  type    = string
  default = "main-subnet"
}

variable "private-subnet-cidr-1-a" {
  type = map

  default = {
    v1 = "10.0.0.64/27"
    # v1 = "10.0.0.64/27,10.0.0.96/27"
  }
}

variable "private-subnet-name-1-a" {
  type = map

  default = {
    v1 = "private-app-subnet-01-a"
    # v1 = "private-app-subnet-01-a,private-db-subnet-01-a"
  }
}

variable "private-subnet-cidr-1-b" {
  type = map

  default = {
    v1 = "10.0.0.128/27"
    # v1 = "10.0.0.128/27,10.0.0.160/27"
  }
}

variable "private-subnet-name-1-b" {
  type = map

  default = {
    v1 = "private-app-subnet-01-b"
    # v1 = "private-app-subnet-01-b,private-db-subnet-01-b"
  }
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
