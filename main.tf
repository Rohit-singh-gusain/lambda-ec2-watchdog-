module "SNS_topic_module" {
  source = "./SNS_topic_module"
  sns_topic_endpoint = var.sns_topic_endpoint

}

module "IAM_ROLE_module" {
  source = "./IAM_ROLE"

}

module "lambda_module" {
  source = "./lambda_module"
  lambda_role_arn = module.IAM_ROLE_module.iam_role_for_lambda
  sns_topic_arn = module.SNS_topic_module.sns_topic_arn

}

module "EventBridge_module" {
  source = "./event_bridge"
  lambda_function_arn = module.lambda_module.lambda_function_arn
  lambda_function_name = module.lambda_module.lambda_function_name

}