## kms key
resource "aws_ssm_parameter" "kms_id" {
  name  = "/${terraform.workspace}/share/security/kms"
  type  = "String"
  value = "arn:aws:kms:eu-central-1:648410456371:key/35f4521a-c954-44ab-94fb-4ce6c7b21146"
}
