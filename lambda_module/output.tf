output "lambda_function_arn" {
  value = aws_lambda_function.ec2_monitor.arn
}

output "lambda_function_name" {
  value = aws_lambda_function.ec2_monitor.function_name
}