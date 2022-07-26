resource "aws_kms_key" "s3_encryption_key" {
  description             = "This key is used to encrypt bucket objects"
  deletion_window_in_days = 10
}

resource "aws_s3_bucket" "s3_resource" {
  bucket        = "frontend-deployment-resource-management-with-s3"
  force_destroy = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "encrypt_objects" {
  bucket = "frontend-deployment-resource-management-with-s3"

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.s3_encryption_key.arn
      sse_algorithm     = "aws:kms"
    }
  }
}

