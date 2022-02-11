variable "lambdas" {
  type = list
  default = ["post_lambda","get_lambda"]
}

provider "aws" {
}

terraform{
  backend "s3"{
    bucket = "terraform-state-stage-development"
    key = "state/s3-state/terraform.tfstate"
    dynamodb_table = "terraform-state-lock-dynamo-stage"
    region = "eu-central-1"
    encrypt = true
  }
}

resource "aws_sns_topic" "manager_updates" {
  name = "DECISION_MANAGER_NOTIFICATION"
}

resource "aws_sns_topic_subscription" "user_updates_sqs_target" {
  topic_arn = aws_sns_topic.manager_updates.arn
  protocol  = "email"
  endpoint  = "marektoth199@gmail.com"
}

resource "aws_lambda_function" "mailing_lambda" {
  function_name = "MAILING_LAMBDA"

  s3_bucket = "api-stage-be-bucket"
  s3_key    = "v1.0.0/mail.zip"

  handler = "main.lambda_handler"
  runtime = "python3.8"

  role = "${aws_iam_role.lambda_exec.arn}"
  layers = ["arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-pandas:43", "arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-numpy:22"]
   environment {
    variables = {
      BUCKET_NAME = "database-bucket-absence"
      OBJECT_NAME_TEAMS = "teams_table.json"
    }
  }
}

resource "aws_cloudwatch_event_rule" "every_day_mail" {
    name = "every_day_mail"
    description = "Launches every day at 18:01"
    schedule_expression = "cron(01 18 * * ? *)"
}

resource "aws_cloudwatch_event_target" "check_mail_every_day" {
    rule = "${aws_cloudwatch_event_rule.every_day_mail.name}"
    target_id = "MAILING_LAMBDA"
    arn = "${aws_lambda_function.mailing_lambda.arn}"
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_check_every_day_mailing" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = "${aws_lambda_function.mailing_lambda.function_name}"
    principal = "events.amazonaws.com"
    source_arn = "${aws_cloudwatch_event_rule.every_day_mail.arn}"
}


resource "aws_lambda_function" "manager_lambda" {
  function_name = "MANAGER_LAMBDA"

  s3_bucket = "api-stage-be-bucket"
  s3_key    = "v1.0.0/manager.zip"

  handler = "main.lambda_handler"
  runtime = "python3.8"

  role = "${aws_iam_role.lambda_exec.arn}"
  layers = ["arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-pandas:43", "arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-numpy:22"]
   environment {
    variables = {
      BUCKET_NAME = "database-bucket-absence-stage"
      OBJECT_NAME_ABSENCE = "absence_data.json"
      OBJECT_NAME_EMPLOYEES = "employees_table.json"
      OBJECT_NAME_TEAMS = "teams_table.json"
      OBJECT_NAME_JOBS = "jobs_table.json"
    }
  }
}

resource "aws_lambda_function" "post_lambda" {
  function_name = "API_POST_LAMBDA"

  s3_bucket = "api-stage-be-bucket"
  s3_key    = "v1.0.0/post.zip"

  handler = "main.lambda_handler"
  runtime = "python3.8"
  layers = ["arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-pandas:43", "arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-numpy:22"]
  role = "${aws_iam_role.lambda_exec.arn}"

   environment {
    variables = {
      BUCKET_NAME = "database-bucket-absence-stage"
      OBJECT_NAME = "absence_data.json"
      OBJECT_NAME_EMPLOYEE = "employees_table.json"
    }
  }
}

resource "aws_lambda_function" "get_lambda" {
  function_name = "API_GET_LAMBDA"

  s3_bucket = "api-stage-be-bucket"
  s3_key    = "v1.0.0/get.zip"

  handler = "main.lambda_handler"
  runtime = "python3.8"

  role = "${aws_iam_role.lambda_exec.arn}"
  layers = ["arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-pandas:43", "arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-numpy:22"]
   environment {
    variables = {
      BUCKET_NAME = "database-bucket-absence"
      OBJECT_NAME_ABSENCE = "absence_data.json"
      OBJECT_NAME_EMPLOYEE = "employees_table.json"
    }
  }
}

resource "aws_lambda_function" "decision_lambda" {
  function_name = "DECISION_LAMBDA"

  s3_bucket = "api-stage-be-bucket"
  s3_key    = "v1.0.0/decision.zip"

  handler = "main.lambda_handler"
  runtime = "python3.8"
  timeout = 10

  role = "${aws_iam_role.lambda_exec.arn}"
  layers = ["arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-pandas:43", "arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-numpy:22"]
   environment {
    variables = {
      BUCKET_NAME = "database-bucket-absence-stage"
      OBJECT_NAME_ABSENCE = "absence_data.json"
      OBJECT_NAME_ABSENCE_TYPE = "absence_type.json"
      OBJECT_NAME_EMPLOYEES = "employees_table.json"
      OBJECT_NAME_JOBS = "jobs_table.json"
      OBJECT_NAME_TEAMS = "teams_table.json"
      OBJECT_NAME_RULES = "rules_table.json"
    }
  }
}


resource "aws_cloudwatch_event_rule" "every_day" {
    name = "every_day"
    description = "Launches every day at 18:00"
    schedule_expression = "cron(0 18 * * ? *)"
}

resource "aws_cloudwatch_event_target" "check_decision_every_day" {
    rule = "${aws_cloudwatch_event_rule.every_day.name}"
    target_id = "DECISION_LAMBDA"
    arn = "${aws_lambda_function.decision_lambda.arn}"
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_check_every_day" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = "${aws_lambda_function.decision_lambda.function_name}"
    principal = "events.amazonaws.com"
    source_arn = "${aws_cloudwatch_event_rule.every_day.arn}"
}



resource "aws_lambda_function" "delete_lambda" {
  function_name = "DELETE_LAMBDA"

  s3_bucket = "api-stage-be-bucket"
  s3_key    = "v1.0.0/delete.zip"

  handler = "main.lambda_handler"
  runtime = "python3.8"

  role = "${aws_iam_role.lambda_exec.arn}"
  layers = ["arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-pandas:43", "arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-numpy:22"]
   environment {
    variables = {
      BUCKET_NAME = "database-bucket-absence-stage"
      OBJECT_NAME = "absence_data.json"
      OBJECT_NAME_EMPLOYEES = "employees_table.json"
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
          "sns:*",
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

resource "aws_api_gateway_method_response" "post_api_response" {
  rest_api_id = aws_api_gateway_rest_api.example.id
  resource_id = aws_api_gateway_resource.post.id
  http_method = aws_api_gateway_method.post.http_method
  status_code = 200

  /**
   * This is where the configuration for CORS enabling starts.
   * We need to enable those response parameters and in the 
   * integration response we will map those to actual values
   */
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers"     = true,
    "method.response.header.Access-Control-Allow-Methods"     = true,
    "method.response.header.Access-Control-Allow-Origin"      = true,
    "method.response.header.Access-Control-Allow-Credentials" = true
  }
}


resource "aws_api_gateway_method" "get" {
  rest_api_id   = "${aws_api_gateway_rest_api.example.id}"
  resource_id   = "${aws_api_gateway_resource.get.id}"
  http_method   = "GET"
  authorization = "NONE"
  api_key_required = "true"
  request_parameters = { "method.request.querystring.personID" = true }
}

resource "aws_api_gateway_method_response" "get_api_response" {
  rest_api_id = aws_api_gateway_rest_api.example.id
  resource_id = aws_api_gateway_resource.get.id
  http_method = aws_api_gateway_method.get.http_method
  status_code = 200

  /**
   * This is where the configuration for CORS enabling starts.
   * We need to enable those response parameters and in the 
   * integration response we will map those to actual values
   */
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers"     = true,
    "method.response.header.Access-Control-Allow-Methods"     = true,
    "method.response.header.Access-Control-Allow-Origin"      = true,
    "method.response.header.Access-Control-Allow-Credentials" = true
  }
}


resource "aws_api_gateway_method" "get_ou" {
  rest_api_id   = "${aws_api_gateway_rest_api.example.id}"
  resource_id   = "${aws_api_gateway_resource.get_ou.id}"
  http_method   = "GET"
  authorization = "NONE"
  api_key_required = "true"
  request_parameters = { "method.request.querystring.managerID" = true }
}

resource "aws_api_gateway_method_response" "get_ou_api_response" {
  rest_api_id = aws_api_gateway_rest_api.example.id
  resource_id = aws_api_gateway_resource.get_ou.id
  http_method = aws_api_gateway_method.get_ou.http_method
  status_code = 200

  /**
   * This is where the configuration for CORS enabling starts.
   * We need to enable those response parameters and in the 
   * integration response we will map those to actual values
   */
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers"     = true,
    "method.response.header.Access-Control-Allow-Methods"     = true,
    "method.response.header.Access-Control-Allow-Origin"      = true,
    "method.response.header.Access-Control-Allow-Credentials" = true
  }
}

resource "aws_api_gateway_method" "delete" {
  rest_api_id   = "${aws_api_gateway_rest_api.example.id}"
  resource_id   = "${aws_api_gateway_resource.delete.id}"
  http_method   = "DELETE"
  authorization = "NONE"
  api_key_required = "true"
}

resource "aws_api_gateway_method_response" "delete_api_response" {
  rest_api_id = aws_api_gateway_rest_api.example.id
  resource_id = aws_api_gateway_resource.delete.id
  http_method = aws_api_gateway_method.delete.http_method
  status_code = 200

  /**
   * This is where the configuration for CORS enabling starts.
   * We need to enable those response parameters and in the 
   * integration response we will map those to actual values
   */
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers"     = true,
    "method.response.header.Access-Control-Allow-Methods"     = true,
    "method.response.header.Access-Control-Allow-Origin"      = true,
    "method.response.header.Access-Control-Allow-Credentials" = true
  }
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
  # within the API Gateway "REST API"...
  source_arn = "${aws_api_gateway_rest_api.example.execution_arn}/*/*"
}

resource "aws_lambda_permission" "apigw3" {

  statement_id  = "AllowAPIGatewayInvoke_DELETE"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.delete_lambda.function_name}"
  principal     = "apigateway.amazonaws.com"

  # The /*/* portion grants access from any method on any resource.....
  # within the API Gateway "REST API"..........
  source_arn = "${aws_api_gateway_rest_api.example.execution_arn}/*/*"
}

