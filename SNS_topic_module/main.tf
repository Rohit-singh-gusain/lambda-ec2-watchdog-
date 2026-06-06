resource "aws_sns_topic" "lambda_topic" {
    name = "lambda_topic"
  
}

resource "aws_sns_topic_subscription" "name" {
    topic_arn = aws_sns_topic.lambda_topic.arn
    protocol = "email"
    endpoint = var.sns_topic_endpoint
  
}