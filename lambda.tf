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
  layers = ["arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-pandas:43", "arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-numpy:22"]
   environment {
    variables = {
      BUCKET_NAME = "database-bucket-absence"
      OBJECT_NAME_ABSENCE = "absence_data.json"
      OBJECT_NAME_EMPLOYEES = "employees_table.json"
      OBJECT_NAME_TEAMS = "teams_table.json"
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
      BUCKET_NAME = "database-bucket-absence"
      OBJECT_NAME = "absence_data.json"
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
  layers = ["arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-pandas:43", "arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-numpy:22"]
   environment {
    variables = {
      BUCKET_NAME = "database-bucket-absence"
      OBJECT_NAME = "absence_data.json"
    }
  }
}

resource "aws_lambda_function" "decision_lambda" {
  function_name = "DECISION_LAMBDA"

  s3_bucket = "apitest-bucket-123"
  s3_key    = "v1.0.0/decision.zip"

  handler = "main.lambda_handler"
  runtime = "python3.8"
  timeout = 10

  role = "${aws_iam_role.lambda_exec.arn}"
  layers = ["arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-pandas:43", "arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-numpy:22"]
   environment {
    variables = {
      BUCKET_NAME = "database-bucket-absence"
      OBJECT_NAME_ABSENCE = "absence_data.json"
      OBJECT_NAME_ABSENCE_TYPE = "absence_type.json"
      OBJECT_NAME_EMPLOYEES = "employees_table.json"
      OBJECT_NAME_JOBS = "jobs_table.json"
      OBJECT_NAME_TEAMS = "teams_table.json"
    }
  }
}

resource "aws_lambda_function" "delete_lambda" {
  function_name = "DELETE_LAMBDA"

  s3_bucket = "apitest-bucket-123"
  s3_key    = "v1.0.0/delete.zip"

  handler = "main.lambda_handler"
  runtime = "python3.8"

  role = "${aws_iam_role.lambda_exec.arn}"
  layers = ["arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-pandas:43", "arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-numpy:22"]
   environment {
    variables = {
      BUCKET_NAME = "database-bucket-absence"
      OBJECT_NAME = "absence_data.json"
    }
  }
}

resource "aws_iam_role_policy" "test_policy" {
  name = "test_policy"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:*",
          "s3-object-lambda:*",
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
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
  path_part   = "load_team_absence"
}

resource "aws_api_gateway_resource" "delete" {
  rest_api_id = "${aws_api_gateway_rest_api.example.id}"
  parent_id   = "${aws_api_gateway_rest_api.example.root_resource_id}"
  path_part   = "delete"
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
  request_parameters = { "method.request.querystring.personID" = true }
}

resource "aws_api_gateway_method" "get_ou" {
  rest_api_id   = "${aws_api_gateway_rest_api.example.id}"
  resource_id   = "${aws_api_gateway_resource.get_ou.id}"
  http_method   = "GET"
  authorization = "NONE"
  api_key_required = "true"
  request_parameters = { "method.request.querystring.managerID" = true }
}

resource "aws_api_gateway_method" "delete" {
  rest_api_id   = "${aws_api_gateway_rest_api.example.id}"
  resource_id   = "${aws_api_gateway_resource.delete.id}"
  http_method   = "DELETE"
  authorization = "NONE"
  api_key_required = "true"
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

  # The /*/* portion grants access from any method on any resource..
  # within the API Gateway "REST API"..
  source_arn = "${aws_api_gateway_rest_api.example.execution_arn}/*/*"
}

resource "aws_lambda_permission" "apigw3" {

  statement_id  = "AllowAPIGatewayInvoke_DELETE"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.delete_lambda.function_name}"
  principal     = "apigateway.amazonaws.com"

  # The /*/* portion grants access from any method on any resource..
  # within the API Gateway "REST API".....
  source_arn = "${aws_api_gateway_rest_api.example.execution_arn}/*/*"
}