## ELB ##

  variable "elb-type" {
    type    = string
    default = "application"
  }

  variable "internal-elb" {
    type    = string
    default = "false"
  }

  variable "elb-tg-name" {
    type = string
    default = "ecs-cluster-tg"
    # default = "lazzaro-back-tg-"
  }

  variable "tg-port" {
    type    = string
    default = "8080"
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
    default =  "/api/private/ongs"
  }

## S3 ##
  variable "bucket-name" {
    type    = string
    default = "tf-ecs-load-balancer-lazzaro"
    # default = "lazzaro-back-s3-"
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

## Security Group ##
  variable "ips" {
    type    = string
    default = "80.112.143.163/32"
  }

  variable "db-port" {
    type = string
    default = "5432"
  }

## Route53 ##
  variable "r53-record-name" {
    type = map
    default = {
      prod = ""
      pre = "pre"
    }
  }