
resource "aws_cloudwatch_event_rule" "ec2_monitor_schedule" {
  name                = "ec2-cost-guardian-schedule"
  description         = "Triggers EC2 Cost Guardian Lambda daily at 09:00 AM UTC"
  schedule_expression = "cron(35 6 * * ? *)"
  state = "ENABLED"

  tags = {
    Project     = "EC2-Cost-Guardian"
    ManagedBy   = "Terraform"
  }
}



resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.ec2_monitor_schedule.name
  target_id = "EC2MonitorLambdaTarget"
  arn       = var.lambda_function_arn  
}



resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.ec2_monitor_schedule.arn
}