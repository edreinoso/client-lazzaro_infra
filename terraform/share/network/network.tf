### VPC ###
module "new-vpc" {
  source              = "github.com/edreinoso/terraform_infrastructure_as_code/modules/network/vpc"
  vpc-cidr            = lookup(var.vpc-cidr, terraform.workspace)
  enable-dns-support  = var.vpc-dns-support
  enable-dns-hostname = var.vpc-dns-hostname
  tags = {
    Name          = "vpc-${var.name}"
    Template      = var.template
    Purpose       = "VPC created for ecs cluster and fargate containers"
    Creation_Date = var.created-on
  }
}

### Flow Logs ###
module "vpc-flow-logs" {
  source                   = "github.com/edreinoso/terraform_infrastructure_as_code/modules/network/flow-log"
  vpc-id                   = module.new-vpc.vpc-id
  traffic-type             = var.traffic-type
  log-destination          = var.log-destination
  max-aggregation-interval = var.max-aggregation-interval
  #roles
  role-policy-name = "flow-logs-policy-${var.name}"
  role-name        = "flow-logs-role-${var.name}"
  #Tags
  tags = {
    Name          = "flow-logs-${var.name}"
    Template      = var.template
    Purpose       = "Flow logs to monitor the in and out traffic in the VPC"
    Creation_Date = var.created-on
  }
}

# ### INTERNET GATEWAY ###
module "igw-vpc" {
  source = "github.com/edreinoso/terraform_infrastructure_as_code/modules/network/igw"
  vpc-id = module.new-vpc.vpc-id
  tags = {
    Name          = "igw-${var.name}"
    Template      = var.template
    Purpose       = "Internet gateway for the ${var.name} vpc"
    Creation_Date = var.created-on
  }
}

# ### SUBNETS ###
# # PUB SUBNET 1
module "public_subnet_1_a" {
  source            = "github.com/edreinoso/terraform_infrastructure_as_code/modules/network/subnet"
  vpc-id            = module.new-vpc.vpc-id
  subnet-cidr       = split(",", lookup(var.public-subnet-cidr-1-a, terraform.workspace))
  availability_zone = "${var.region}1a"
  visibility        = "public"
  # Tags
  subnet-name         = split(",", lookup(var.public-subnet-name-1-a, terraform.workspace))
  template            = var.template
  subnet-availability = "main"
  purpose             = "Public subnet for resources with internet communication"
  type                = "public"
  created-on          = var.created-on
}
# # PUB SUBNET 2
module "public_subnet_1_b" {
  source            = "github.com/edreinoso/terraform_infrastructure_as_code/modules/network/subnet"
  vpc-id            = module.new-vpc.vpc-id
  subnet-cidr       = split(",", lookup(var.public-subnet-cidr-1-b, terraform.workspace))
  availability_zone = "${var.region}1b"
  visibility        = "public"
  # Tags
  subnet-name         = split(",", lookup(var.public-subnet-name-1-b, terraform.workspace))
  template            = var.template
  subnet-availability = "ha"
  purpose             = "Public subnet for resources with internet communication"
  type                = "public"
  created-on          = var.created-on
}

# # PRI SUBNET 1
module "private_subnet_1_a" {
  source            = "github.com/edreinoso/terraform_infrastructure_as_code/modules/network/subnet"
  vpc-id            = module.new-vpc.vpc-id
  subnet-cidr       = split(",", lookup(var.private-subnet-cidr-1-a, terraform.workspace))
  availability_zone = "${var.region}1a"
  visibility        = "private"
  # Tags
  subnet-name = split(",", lookup(var.private-subnet-name-1-a, terraform.workspace))
  template    = var.template
  purpose     = "Private subnet for internal communication"
  type        = "private"
  created-on  = var.created-on
}
# PRI SUBNET 2
module "private_subnet_1_b" {
  source            = "github.com/edreinoso/terraform_infrastructure_as_code/modules/network/subnet"
  vpc-id            = module.new-vpc.vpc-id
  subnet-cidr       = split(",", lookup(var.private-subnet-cidr-1-b, terraform.workspace))
  availability_zone = "${var.region}1b"
  visibility        = "private"
  # Tags
  subnet-name = split(",", lookup(var.private-subnet-name-1-b, terraform.workspace))
  template    = var.template
  purpose     = "Private subnet for internal communication"
  type        = "private"
  created-on  = var.created-on
}

### ROUTE TABLES ###
# ROUTE TABLE: PRIVATE #
module "private-route-table" {
  source = "github.com/edreinoso/terraform_infrastructure_as_code/modules/network/route-tables/rt"
  vpc-id = module.new-vpc.vpc-id
  tags = {
    Name          = "private-rt-${var.name}"
    Template      = var.template
    Purpose       = "Route table set up for ${var.name} VPC in the private subnets"
    Creation_Date = var.created-on
  }
}

# application subnet associations
module "rt-pri-subnet-1" {
  source       = "github.com/edreinoso/terraform_infrastructure_as_code/modules/network/route-tables/rtAssociation"
  subnet-ids   = module.private_subnet_1_a.subnet-id
  rt-id        = module.private-route-table.rt-id
  subnet-cidrs = split(",", lookup(var.private-subnet-cidr-1-a, terraform.workspace))
}

# database subnet associations
module "rt-pri-subnet-2" {
  source       = "github.com/edreinoso/terraform_infrastructure_as_code/modules/network/route-tables/rtAssociation"
  subnet-ids   = module.private_subnet_1_b.subnet-id
  rt-id        = module.private-route-table.rt-id
  subnet-cidrs = split(",", lookup(var.private-subnet-cidr-1-b, terraform.workspace))
}

# # ROUTE TABLE: PUBLIC #
module "public-route-table" {
  source = "github.com/edreinoso/terraform_infrastructure_as_code/modules/network/route-tables/rt"
  vpc-id = module.new-vpc.vpc-id
  tags = {
    Name          = "public-rt-${var.name}"
    Template      = var.template
    Purpose       = "Route table set up for ${var.name} VPC in the public subnets"
    Creation_Date = var.created-on
  }
}

module "rt-public-subnet-1" {
  source       = "github.com/edreinoso/terraform_infrastructure_as_code/modules/network/route-tables/rtAssociation"
  subnet-ids   = module.public_subnet_1_a.subnet-id
  rt-id        = module.public-route-table.rt-id
  subnet-cidrs = split(",", lookup(var.public-subnet-cidr-1-a, terraform.workspace))
}

module "rt-public-subnet-2" {
  source       = "github.com/edreinoso/terraform_infrastructure_as_code/modules/network/route-tables/rtAssociation"
  subnet-ids   = module.public_subnet_1_b.subnet-id
  rt-id        = module.public-route-table.rt-id
  subnet-cidrs = split(",", lookup(var.public-subnet-cidr-1-b, terraform.workspace))
}

# route destination from the subnets to the internet gateway
# module "public-routes" {
#   source       = "github.com/edreinoso/terraform_infrastructure_as_code/modules/network/route-tables/route"
#   routeTableId = module.public-route-table.rt-id
#   destination  = var.destinationRoute
#   igw          = module.igw-vpc.igw-id
# }

resource "aws_route" "public-routes" {
  route_table_id         = module.public-route-table.rt-id
  destination_cidr_block = var.destinationRoute
  gateway_id             = module.igw-vpc.igw-id
}
