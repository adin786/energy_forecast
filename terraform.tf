# Resources
# - https://nquayson.com/aws-lambda-function-url-using-terraform-quick-walkthrough
# - https://itnext.io/creating-an-https-lambda-endpoint-without-api-gateway-eb0db1f6af7a
# - https://www.deadbear.io/simple-serverless-fastapi-with-aws-lambda/

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.9.0"
    }
  }
  required_version = "~> 1.0"
}

provider "aws" {
  region = "eu-west-2"
}

terraform {
  backend "s3" {
    bucket = "energy-forecast"
    key    = "terraform/state"
    region = "eu-west-2"
  }
}


resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

data "archive_file" "zip" {
  type        = "zip"
  source_dir = "${path.module}/app_lambda/"
  output_path = "${path.module}/app_lambda.zip"
}

resource "aws_lambda_function" "energy_forecast_lambda" {
  filename         = data.archive_file.zip.output_path
  source_code_hash = data.archive_file.zip.output_base64sha256
  function_name    = "energy_forecast"
  role             = aws_iam_role.iam_for_lambda.arn
  handler          = "app.lambda_handler"
  runtime          = "python3.9"
}

resource "aws_lambda_function_url" "lambda_function_url" {
  function_name      = aws_lambda_function.energy_forecast_lambda.arn
  authorization_type = "NONE"
}

output "function_url" {
  description = "Energy forecasting for uk grid consumption"
  value       = aws_lambda_function_url.lambda_function_url.function_url
}
