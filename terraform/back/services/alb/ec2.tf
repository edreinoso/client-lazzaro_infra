data "aws_ami" "amazon_linux" {
  most_recent = true

  owners = ["648410456371"]

  filter {
    name = "name"
    values = [
      "nat-ami-5-11"
    ]
  }
}


module "bastion-server" {
  source             = "github.com/edreinoso/terraform_infrastructure_as_code/modules/compute/ec2"
  ami                = data.aws_ami.amazon_linux.id
  instance-type      = "t2.micro"
  key-name           = "hello_world"
  public-ip          = "true"
  user-data          = "${file("user.sh")}"
  sourceCheck        = "" # emtpy values signifiy false
  subnet-ids         = element(
   element(data.terraform_remote_state.network.outputs.pub-subnet-id-b, 0),
   0,
 ) #public subnet a
  security-group-ids = split(",", aws_security_group.bastion-security-group.id)
  tags = {
    Name          = "ec2-${var.name}"
    Template      = var.template
    Purpose       = "EC2 instance that would serve as NAT for the Fargate containers to communicate with the open world"
    Creation_Date = var.created-on
  }
}

# module "test-server" {
#   source             = "github.com/edreinoso/terraform_infrastructure_as_code/modules/compute/ec2"
#   ami                = "ami-0a6dc7529cd559185"
#   instance-type      = "t2.micro"
#   key-name           = "hello_world"
#   public-ip          = ""
#   user-data          = "${file("user.sh")}"
#   sourceCheck        = "true" # emtpy values signifiy false
#   subnet-ids         = element(
#    element(data.terraform_remote_state.network.outputs.pri-subnet-id-b, 1),
#    0,
#  ) #private app b
#   security-group-ids = split(",", aws_security_group.test-security-group.id)
#   tags = {
#     Name          = "test-ec2-${var.name}"
#     Template      = var.template
#     Purpose       = "EC2 instance that would serve as NAT for the Fargate containers to communicate with the open world"
#     Creation_Date = var.created-on
#   }
# }

module "private-routes-bastion" {
  source       = "github.com/edreinoso/terraform_infrastructure_as_code/modules/network/route-tables/route"
  routeTableId = element(data.terraform_remote_state.network.outputs.private-rt-id, 1)
  instanceId   = "${module.bastion-server.ec2-id}"
  destination  = "0.0.0.0/0"
}
