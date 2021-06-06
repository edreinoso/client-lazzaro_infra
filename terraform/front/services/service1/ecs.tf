data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "terraform-state-lazzaro"
    key    = "env:/v1/network.tfstate"
    region = "eu-central-1"
  }
}

data "terraform_remote_state" "cluster_id" {
    backend = "s3"
    config = {
        bucket = "terraform-state-lazzaro"
        key    = "infra_front.tfstate"
        region = "eu-central-1"
    }
}

resource "aws_ecs_service" "ecs_service" {
 name            = var.name
 task_definition = aws_ecs_task_definition.ecs_task_definition.arn
 cluster         = data.terraform_remote_state.cluster_id.outputs.cluster-id
 capacity_provider_strategy {
   capacity_provider = "FARGATE_SPOT"
   weight = 100
 }

 desired_count = 1

 load_balancer {
   target_group_arn = element(data.terraform_remote_state.load_balancer.outputs.target_group_arn, 0)
   container_name   = "ecs-cluster"
   container_port   = "3000"
 }

 network_configuration {
   assign_public_ip = false # this needs to change accordingly as well

   security_groups = split(",", aws_security_group.fargate-security-group.id)

   # these are going to have to be static while there is no backend set up
   subnets = [
     element(element(data.terraform_remote_state.network.outputs.pub-subnet-id-a, 0), 0),
     element(element(data.terraform_remote_state.network.outputs.pub-subnet-id-b, 0), 0)
    #  element(element(data.terraform_remote_state.network.outputs.pri-subnet-id-b, 1),0,),
    #  element(element(data.terraform_remote_state.network.outputs.pri-subnet-id-a, 1),0,)
   ]
 }
}

resource "aws_ecs_task_definition" "ecs_task_definition" {
 family = "frontend-task-definition"

 container_definitions = <<EOF
 [
   {
     "name": "ecs-cluster",
     "image": "648410456371.dkr.ecr.eu-central-1.amazonaws.com/lazzaro-front-repo:v4",
     "portMappings": [
       {
         "containerPort": 3000,
         "hostPort": 3000
       }
     ],
     "logConfiguration": {
       "logDriver": "awslogs",
       "options": {
         "awslogs-region": "eu-central-1",
         "awslogs-group": "/ecs/front/",
         "awslogs-stream-prefix": "ecs"
       }
     }
   }
 ]

EOF

 execution_role_arn = aws_iam_role.ecs-api-task-execution-role.arn
 cpu                      = 512
 memory                   = 1024
 requires_compatibilities = ["FARGATE"]
 network_mode = "awsvpc"
}