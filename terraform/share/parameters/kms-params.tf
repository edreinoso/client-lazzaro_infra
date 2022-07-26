## kms key
resource "aws_ssm_parameter" "kms_id" {
  name  = "/${terraform.workspace}/share/security/kms"
  type  = "String"
  value = "arn:aws:kms:eu-central-1:648410456371:key/5001c33a-d8b6-4c59-81b1-39d0d595e90d"
}
