# target group arn
    # output "target_group_arn" {
    #   value = ["${module.target-group.target-arn}"]
    # }

output "alb_sg" {
    value = aws_security_group.elb-security-group.id
}

output "alb_arn" {
    value = module.elb.elb-arn
}

output "alb_dns" {
    value = module.elb.elb-dns-name
}

output "alb_zone" {
    value = module.elb.elb-zone-id
}