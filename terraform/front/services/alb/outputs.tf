# target group arn
    # output "target_group_arn" {
    #   value = ["${module.target-group.target-arn}"]
    # }

output "elb-security-group" {
    value = aws_security_group.elb-security-group.id
}