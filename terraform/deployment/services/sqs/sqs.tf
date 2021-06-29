resource "aws_sqs_queue" "sg_delete_queue" {
  name                      = "${var.name}-${terraform.workspace}"
  delay_seconds             = 300
  
  tags = {
    Purpose = "Queue to delete security group from clients"
    Environment = terraform.workspace
    Name = var.name
    Creation_Date = "28 June 2021"
  }
}

resource "aws_lambda_event_source_mapping" "lambda_mapping" {
  event_source_arn = aws_sqs_queue.sg_delete_queue.arn
  function_name    = "arn:aws:lambda:eu-central-1:648410456371:function:frontend-ecs-services-${terraform.workspace}-deletesecuritygroup"
}

variable "name" {
    type = string
    default = "lazzaro-sqs-service"
}