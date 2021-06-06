output "ec2-id" {
  value = "${aws_instance.ec2.id}"
  # outputs for more than one ec2 instance
    # value = "${aws_instance.ec2.*.id}"
}

output "ip" {
  value = "${aws_instance.ec2.public_ip}"
}

output "public-dns" {
  value = "${aws_instance.ec2.public_dns}"
}