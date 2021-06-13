output "code_pipeline_role_arn" {
    value = aws_iam_role.ecs-pipeline-role.arn
}

output "code_build_role_arn" {
    value = aws_iam_role.ecs-build-role.arn
}

output "bucket_location" {
    value = aws_s3_bucket.ecs-s3-pipeline.bucket
}