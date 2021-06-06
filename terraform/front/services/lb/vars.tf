### Generic Variables
    variable "region" {
      type = string
      default = "eu-central-1"
    }

    variable "name" {
        type = map
        default = {
          default = "default-frontend"
          prod = "frontend"
        }
    }

    variable "template" {
      type    = string
      default = "containarized_frontend"
    }

    variable "application" {
      type    = string
      default = ""
    }

    variable "purpose" {
      type    = string
      default = "setting up frontend services"
    }

    variable "created-on" {
      type    = string
      default = "25_April_2021"
    }

## ELB ##
  variable "elb-type" {
    type    = string
    default = "application"
  }

  variable "internal-elb" {
    type    = string
    default = "false"
  }

  variable "tg-port" {
      type = string
      default = "3000"
  }

    variable "tg-target-type" {
    type    = string
    default = "ip"
  }

  variable "tg-deregister" {
    type = string

    # monitor for change
    default = "400"
  }

  variable "path" {
    type = string
    default =  "/healthcheck" # need to configure this to go
  }

## S3 ##
  variable "bucket-name" {
    type    = string
    default = "load-balancer-lazzaro"
  }

  variable "acl" {
    type    = string
    default = "private"
  }

  variable "destroy" {
    type    = string
    default = "true"
  }

  variable "account-id" {
    type    = string
    default = "648410456371" # your account ID
  }

