variable "region" {
  description = "region you want to create lambda function"
  type = string
}

variable "sns_topic_endpoint" {
  description = "endpoint for sns e.g email=example@gmail.com"
  type = string
}

variable "iam_role_for_lambda" {
  description = "arm of iam role for lambda"
  type = string
}