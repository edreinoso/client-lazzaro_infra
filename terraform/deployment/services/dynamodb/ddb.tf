module "dynamodb-table" {
  source         = "github.com/edreinoso/terraform_infrastructure_as_code/modules/storage/dynamodb/"
  name           = "frontend-ddb-client-${terraform.workspace}"
  hash-key       = var.primary-key
  attribute-name = var.primary-key
  billingMode    = var.billing
  read           = var.read-write-capacity
  write          = var.read-write-capacity
  attribute-type = var.attribute-type
  streams        = var.streams
  stream-view    = var.stream-view
  ttl-enabled    = var.ttl-enabled
  tags = {
    Name          = "frontend-ddb-client-${terraform.workspace}"
    Creation_Date = "14 June 2021"
  }
}