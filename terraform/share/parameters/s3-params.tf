## dashboard name
resource "aws_ssm_parameter" "s3_bucket" {
  name  = "/${terraform.workspace}/share/storage/s3"
  type  = "String"
  value = "deployment-resources-${terraform.workspace}"
}
