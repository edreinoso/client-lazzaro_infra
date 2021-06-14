output "cluster_id" {
    value = aws_ecs_cluster.ecs-cluster.id
}

output "repository_url" {
    value = aws_ecr_repository.ecr.repository_url
}