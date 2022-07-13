resource "aws_kms_key" "s3_encryption_key" {
  description             = "This key is used to encrypt bucket objects"
  deletion_window_in_days = 10
}

resource "aws_s3_bucket" "s3_resource" {
  bucket = "deployment-resources-${terraform.workspace}"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "encrypt_objects" {
  bucket = aws_s3_bucket.s3_resource.bucket

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.s3_encryption_key.arn
      sse_algorithm     = "aws:kms"
    }
  }
}
