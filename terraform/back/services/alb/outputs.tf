# target group arn
    output "target_group_arn" {
      value = ["${module.target-group.target-arn}"]
    }

# bastion security group id
    output "bastion-security-group" {
      value = aws_security_group.bastion-security-group.id
    }
    
    output "elb-security-group" {
      value = aws_security_group.elb-security-group.id
    }