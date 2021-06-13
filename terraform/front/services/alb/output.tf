output "alb_arn" {
    value = module.elb.elb-arn
}

output "alb_dns" {
    value = module.elb.elb-dns-name
}

output "alb_zone" {
    value = module.elb.elb-zone-id
}