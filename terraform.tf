# Resources
# - https://nquayson.com/aws-lambda-function-url-using-terraform-quick-walkthrough
# - https://itnext.io/creating-an-https-lambda-endpoint-without-api-gateway-eb0db1f6af7a
# - https://www.deadbear.io/simple-serverless-fastapi-with-aws-lambda/

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.39.0"
    }
    # docker = {
    #   source = "kreuzwerker/docker"
    #   version = "~> 2.23.0"
    # }
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

# data "archive_file" "zip" {
#   type        = "zip"
#   source_dir = "${path.module}/app_lambda/"
#   output_path = "${path.module}/app_lambda.zip"
# }
# 
# resource "aws_lambda_function" "energy_forecast_lambda" {
#   filename         = data.archive_file.zip.output_path
#   source_code_hash = data.archive_file.zip.output_base64sha256
#   function_name    = "energy_forecast"
#   role             = aws_iam_role.iam_for_lambda.arn
#   handler          = "app.lambda_handler"
#   runtime          = "python3.9"
# }

resource "aws_lambda_function" "energy_forecast_lambda" {
  package_type     = "Image"
  image_uri        = "081150070467.dkr.ecr.eu-west-2.amazonaws.com/energy_forecast/lambda:latest"
  function_name    = "energy_forecast"
  role             = aws_iam_role.iam_for_lambda.arn
  timeout          = 30
}

resource "aws_lambda_function_url" "lambda_function_url" {
  function_name      = aws_lambda_function.energy_forecast_lambda.arn
  authorization_type = "AWS_IAM"
  cors {
    allow_credentials = true
    allow_origins     = ["*"]
    allow_methods     = ["*"]
    allow_headers     = ["date", "keep-alive"]
    expose_headers    = ["keep-alive", "date"]
    max_age           = 86400
  }
}

output "function_url" {
  description = "Energy forecasting for uk grid consumption"
  value       = aws_lambda_function_url.lambda_function_url.function_url
}


# Configure monitoring/logging
# https://technotrampoline.com/articles/how-to-configure-aws-lambda-cloudwatch-logging-with-terraform/

resource "aws_cloudwatch_log_group" "function_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.energy_forecast_lambda.function_name}"
  retention_in_days = 7
  lifecycle {
    prevent_destroy = false
  }
}

resource "aws_iam_policy" "iam_policy_for_logging" {
  name   = "iam_policy_for_loggingy"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        Action : [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Effect : "Allow",
        Resource : "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "logging_policy_attachment" {
  role = aws_iam_role.iam_for_lambda.id
  policy_arn = aws_iam_policy.iam_policy_for_logging.arn
}


