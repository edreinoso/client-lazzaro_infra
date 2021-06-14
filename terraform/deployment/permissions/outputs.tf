output "codebuild_permission_arn" {
    value = aws_iam_role.codebuild_permissions.arn
}
output "client_permission_arn" {
    value = aws_iam_role.client_permission.arn
}
output "create_permission_arn" {
    value = aws_iam_role.createservice_permission.arn
}
output "remove_permission_arn" {
    value = aws_iam_role.removeservice_permission.arn
}