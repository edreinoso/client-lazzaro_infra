## V1 = 3000
## V2 = 8080

resource "aws_ecs_service" "ecs_service" {
 name            = "lazzaro-back-service-${terraform.workspace}"
 task_definition = aws_ecs_task_definition.ecs_task_definition.arn
 cluster         = lookup(var.cluster_id, terraform.workspace)
 # launch_type     = "FARGATE" # I have to change things here if I want to do fargate spot
 capacity_provider_strategy {
  #  capacity_provider = "FARGATE"
   capacity_provider = "FARGATE_SPOT"
   weight = 100
 }

 desired_count = 1

 load_balancer {
   target_group_arn = element(data.terraform_remote_state.load_balancer.outputs.target_group_arn, 0)
   container_name   = "lazzaro-back-container-${terraform.workspace}"
   container_port   = "8080"
 }

 network_configuration {
   # need to test with Ivan in order to change
   assign_public_ip = lookup(var.pub-ip, terraform.workspace)

   security_groups = split(",", aws_security_group.fargate-security-group.id)

   # you are going to have to change to public subnets if deploying in production
   subnets = [
    #  element(element(data.terraform_remote_state.network.outputs.pub-subnet-id-a, 0), 0),
    #  element(element(data.terraform_remote_state.network.outputs.pub-subnet-id-b, 0), 0)
     element(element(data.terraform_remote_state.network.outputs.pri-subnet-id-b, 1),0,),
     element(element(data.terraform_remote_state.network.outputs.pri-subnet-id-a, 1),0,)
   ]
 }
}

resource "aws_ecs_task_definition" "ecs_task_definition" {
 family = "lazzaro-back-tsk-${terraform.workspace}"

 container_definitions = <<EOF
 [
   {
     "name": "lazzaro-back-container-${terraform.workspace}",
     "image": "${var.account-id}.dkr.ecr.${var.region}.amazonaws.com/lazzaro-back-repo-${terraform.workspace}:v1",
     "portMappings": [
       {
         "containerPort": 8080
       }
     ],
     "logConfiguration": {
       "logDriver": "awslogs",
       "options": {
         "awslogs-region": "eu-central-1",
         "awslogs-group": "/ecs/back/${terraform.workspace}/",
         "awslogs-stream-prefix": "ecs"
       }
     }
   }
 ]

EOF

 execution_role_arn = "arn:aws:iam::648410456371:role/task-execution-role-backend-ecs-stack"

 # Might have to have more computing power for the containers.
 cpu                      = 512
 memory                   = 1024
 requires_compatibilities = ["FARGATE"]

 # This is required for Fargate containers (more on this later).
 network_mode = "awsvpc"
}
