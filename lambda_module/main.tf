

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.root}/python_lambda_code/lambda_function.py"
  output_path = "${path.root}/python_lambda_code/ec2_monitor.zip"
}


resource "aws_lambda_function" "ec2_monitor" {
  function_name    = "ec2_inspector"
  description      = "Checks for running EC2 instances daily and sends SNS alert"

  
  filename         = data.archive_file.lambda_zip.output_path

  
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.12"
  handler          = "lambda_function.lambda_handler"  
  role             = var.lambda_role_arn
  timeout          = 30  
  memory_size      = 128  

  environment {
    variables = {
      SNS_TOPIC_ARN = var.sns_topic_arn                  
    }
  }

  depends_on = [
    var.lambda_role_arn
  ]
}