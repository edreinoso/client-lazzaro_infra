## dashboard name
resource "aws_ssm_parameter" "cloudwatch_dasboard" {
  name  = "/${terraform.workspace}/share/monitor/dashboard"
  type  = "String"
  value = "frontend-clients-dashboards-${terraform.workspace}"
}
