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

## ECR ##
  variable "cluster_id" {
    type = string
    # this is completely static
    default = "arn:aws:ecs:eu-central-1:648410456371:cluster/lazzaro-cluster"
  }
  
  variable "repository-name" {
    type = map
    default = {
      v1 = "tst" # this is the todo app
      v2 = "dev"
    }
  }

  variable "app-port" {
    type = map
    default = {
      v1 = 3000
      v2 = 8080
    }
  }