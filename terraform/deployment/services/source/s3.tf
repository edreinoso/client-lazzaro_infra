resource "aws_s3_bucket" "repository" {
  bucket        = "lazzaro-ongs-template-bucket"
  acl           = "private"
  force_destroy =  true
}
