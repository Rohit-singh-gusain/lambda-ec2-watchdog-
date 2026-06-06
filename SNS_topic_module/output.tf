output "sns_topic_arn" {
  value = aws_sns_topic.lambda_topic.arn
}