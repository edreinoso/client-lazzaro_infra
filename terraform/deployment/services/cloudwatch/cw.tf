resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "frontend-clients-dashboards-${terraform.workspace}"
  dashboard_body = <<EOF
{
    "widgets": []
}
EOF
}
