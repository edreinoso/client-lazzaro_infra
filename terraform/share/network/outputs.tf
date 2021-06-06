### VPC ###
output "vpc-id" {
  value = ["${module.new-vpc.vpc-id}"]
}

# output "vpc-cidr" {
#   value = ["${module.new-vpc.vpc-cidr}"]
# }

# ### SUBNETS ###
output "pub-subnet-id-a" {
  value = ["${module.public_subnet_1_a.subnet-id}"]
}
output "pub-subnet-id-b" {
  value = ["${module.public_subnet_1_b.subnet-id}"]
}
output "pri-subnet-id-a" {
  value = ["${module.private_subnet_1_a.subnet-id}"]
}
output "pri-subnet-id-b" {
  value = ["${module.private_subnet_1_b.subnet-id}"]
}

# ### INTERNET GATEWAY ###
# output "igw-id" {
#   value = ["${module.igw-vpc.igw-id}"]
# }

# ### ROUTE TABLES ###
output "private-rt-id" {
  value = ["${module.private-route-table.rt-id}"]
}
output "public-rt-id" {
  value = ["${module.public-route-table.rt-id}"]
}
