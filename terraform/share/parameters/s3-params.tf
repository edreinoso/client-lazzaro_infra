## s3 bucket
resource "aws_ssm_parameter" "s3_bucket" {
  name  = "/${terraform.workspace}/share/storage/s3"
  type  = "String"
  value = "frontend-deployment-resource-management-with-s3"
}
