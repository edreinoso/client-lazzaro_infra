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
    type = map
    # this is completely static
    default = {
      prod = "arn:aws:ecs:eu-central-1:648410456371:cluster/lazzaro-back-cluster-prod"
      pre = "arn:aws:ecs:eu-central-1:648410456371:cluster/lazzaro-back-cluster-pre"
      nfts-pre = "arn:aws:ecs:eu-central-1:648410456371:cluster/lazzaro-back-cluster-nfts-pre"
    }
  }
  
  variable "repository-name" {
    type = map
    default = {
      v1 = "tst" # this is the todo app
      v2 = "dev"
      prod = "prod"
      pre = "pre"
    }
  }

  variable "app-port" {
    type = map
    default = {
      v1 = 3000
      v2 = 8080
    }
  }

  variable "pub-ip" {
    type = map
    default = {
      prod = true
      pre = false
      pre = false
    }
  }