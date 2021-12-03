variable "lambdas" {
  type = list
  default = ["post_lambda","get_lambda"]
}

provider "aws" {
}

terraform{
  backend "s3"{
    bucket = "terraform-state-dev-development"
    key = "state/s3-state/terraform.tfstate"
    dynamodb_table = "terraform-state-lock-dynamo-dev-development"
    region = "eu-central-1"
    encrypt = true
  }
}

resource "aws_dynamodb_table" "dynamodb-terraform-state-lock" {
  name = "terraform-state-lock-dynamo-dev-development"
  hash_key = "LockID"
  read_capacity = 20
  write_capacity = 20
 
  attribute {
    name = "LockID"
    type = "S"
  }
}

resource "aws_lambda_function" "manager_lambda" {
  function_name = "MANAGER_LAMBDA"

  s3_bucket = "apitest-bucket-123"
  s3_key    = "v1.0.0/manager.zip"

  handler = "main.lambda_handler"
  runtime = "python3.8"

  role = "${aws_iam_role.lambda_exec.arn}"

   environment {
    variables = {
      ABSENCE_TABLE = "Absence_Data"
      EMPLOYEES_TABLE = "Employees"
      TEAM_TABLE = "OU_Table"
    }
  }
}

resource "aws_lambda_function" "post_lambda" {
  function_name = "API_POST_LAMBDA"

  s3_bucket = "apitest-bucket-123"
  s3_key    = "v1.0.0/post.zip"

  handler = "main.lambda_handler"
  runtime = "python3.8"

  role = "${aws_iam_role.lambda_exec.arn}"

   environment {
    variables = {
      TABLE_NAME = "Absence_Data"
    }
  }
}

resource "aws_lambda_function" "get_lambda" {
  function_name = "API_GET_LAMBDA"

  s3_bucket = "apitest-bucket-123"
  s3_key    = "v1.0.0/get.zip"

  handler = "main.lambda_handler"
  runtime = "python3.8"

  role = "${aws_iam_role.lambda_exec.arn}"

   environment {
    variables = {
      TABLE_NAME = "Absence_Data"
    }
  }
}

resource "aws_lambda_function" "decision_lambda" {
  function_name = "DECISION_LAMBDA"

  s3_bucket = "apitest-bucket-123"
  s3_key    = "v1.0.0/decision.zip"

  handler = "main.lambda_handler"
  runtime = "python3.8"

  role = "${aws_iam_role.lambda_exec.arn}"

   environment {
    variables = {
      ABSENCE_TABLE = "Absence_Data"
      EMPLOYEES_TABLE = "Employees"
      TEAM_TABLE = "OU_Table"
    }
  }
}



resource "aws_iam_role" "lambda_exec" {
  name = "serverless_example_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_api_gateway_resource" "post" {
  rest_api_id = "${aws_api_gateway_rest_api.example.id}"
  parent_id   = "${aws_api_gateway_rest_api.example.root_resource_id}"
  path_part   = "submit"
}

resource "aws_api_gateway_resource" "get" {
  rest_api_id = "${aws_api_gateway_rest_api.example.id}"
  parent_id   = "${aws_api_gateway_rest_api.example.root_resource_id}"
  path_part   = "load"
}

resource "aws_api_gateway_resource" "get_ou" {
  rest_api_id = "${aws_api_gateway_rest_api.example.id}"
  parent_id   = "${aws_api_gateway_rest_api.example.root_resource_id}"
  path_part   = "load_team_absence_data"
}

resource "aws_api_gateway_method" "post" {
  rest_api_id   = "${aws_api_gateway_rest_api.example.id}"
  resource_id   = "${aws_api_gateway_resource.post.id}"
  http_method   = "POST"
  authorization = "NONE"
  api_key_required = "true"
}

resource "aws_api_gateway_method" "get" {
  rest_api_id   = "${aws_api_gateway_rest_api.example.id}"
  resource_id   = "${aws_api_gateway_resource.get.id}"
  http_method   = "GET"
  authorization = "NONE"
  api_key_required = "true"
  request_parameters = { "method.request.header.personID" = true }
}

resource "aws_api_gateway_method" "get_ou" {
  rest_api_id   = "${aws_api_gateway_rest_api.example.id}"
  resource_id   = "${aws_api_gateway_resource.get_ou.id}"
  http_method   = "GET"
  authorization = "NONE"
  api_key_required = "true"
  request_parameters = { "method.request.header.managerID" = true }
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke_POST"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.post_lambda.function_name}"
  principal     = "apigateway.amazonaws.com"

  # The /*/* portion grants access from any method on any resource
  # within the API Gateway "REST API".
  source_arn = "${aws_api_gateway_rest_api.example.execution_arn}/*/*"
}

resource "aws_lambda_permission" "apigw2" {

  statement_id  = "AllowAPIGatewayInvoke_GET"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.get_lambda.function_name}"
  principal     = "apigateway.amazonaws.com"

  # The /*/* portion grants access from any method on any resource
  # within the API Gateway "REST API"..
  source_arn = "${aws_api_gateway_rest_api.example.execution_arn}/*/*"
}