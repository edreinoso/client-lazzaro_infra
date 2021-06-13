### SUBNETS ###
  variable "region" {
    type    = string
    default = "eu-central-"
  }

# SUBNETS: PUBLIC #
  variable "public-subnet-cidr-1-a" {
    type = map

    default = {
      v1 = "10.0.0.0/27,10.0.0.96/27,10.0.0.192/27"
      # v1 = "10.0.0.0/27"
    }
  }

  variable "public-subnet-name-1-a" {
    type = map

    default = {
      v1 = "public-subnet-01-a,client-public-subnet-02-a,client-public-subnet-03-a"
      # v1 = "public-subnet-01-a"
    }
  }

  variable "public-subnet-cidr-1-b" {
    type = map

    default = {
      v1 = "10.0.0.32/27,10.0.0.160/27,10.0.0.224/27"
      # v1 = "10.0.0.32/27"
    }
  }

  variable "public-subnet-name-1-b" {
    type = map

    default = {
      v1 = "public-subnet-01-b,client-public-subnet-02-b,client-public-subnet-03-b"
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