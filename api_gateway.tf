resource "aws_api_gateway_rest_api" "example" {
  name        = "Absence_Data_API"
  description = "First stage of API"
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id = "${aws_api_gateway_rest_api.example.id}"
  resource_id = "${aws_api_gateway_method.post.resource_id}"
  http_method = "${aws_api_gateway_method.post.http_method}"

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.post_lambda.invoke_arn}"
}


resource "aws_api_gateway_integration_response" "lambda_mockapi_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.example.id
  resource_id = aws_api_gateway_resource.post.id
  http_method = aws_api_gateway_method.post.http_method
  status_code = aws_api_gateway_method_response.post_api_response.status_code

  /**
   * This is second half of the CORS configuration.
   * Here we give values to each of the header parameters to ALLOW 
   * Cross-Origin requests from ALL hosts.
   **/
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers"     = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
    "method.response.header.Access-Control-Allow-Methods"     = "'GET,OPTIONS,POST,PUT'",
    "method.response.header.Access-Control-Allow-Origin"      = "'*'",
    "method.response.header.Access-Control-Allow-Credentials" = "'true'"
  }

  response_templates = {
    "application/json" = <<EOF
{
  "statusCode": 200,
  "message": "OK! Everything in order"
}
EOF
  }
}



resource "aws_api_gateway_integration" "lambda2" {
  rest_api_id = "${aws_api_gateway_rest_api.example.id}"
  resource_id = "${aws_api_gateway_method.get.resource_id}"
  http_method = "${aws_api_gateway_method.get.http_method}"

  integration_http_method = "GET"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.get_lambda.invoke_arn}"
}

resource "aws_api_gateway_integration_response" "lambda2_mockapi_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.example.id
  resource_id = aws_api_gateway_resource.get.id
  http_method = aws_api_gateway_method.get.http_method
  status_code = aws_api_gateway_method_response.get_api_response.status_code

  /**
   * This is second half of the CORS configuration.
   * Here we give values to each of the header parameters to ALLOW 
   * Cross-Origin requests from ALL hosts.
   **/
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers"     = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
    "method.response.header.Access-Control-Allow-Methods"     = "'GET,OPTIONS,POST,PUT'",
    "method.response.header.Access-Control-Allow-Origin"      = "'*'",
    "method.response.header.Access-Control-Allow-Credentials" = "'true'"
  }

  response_templates = {
    "application/json" = <<EOF
{
  "statusCode": 200,
  "message": "OK! Everything in order"
}
EOF
  }
}


resource "aws_api_gateway_integration" "lambda3" {
  rest_api_id = "${aws_api_gateway_rest_api.example.id}"
  resource_id = "${aws_api_gateway_method.get_ou.resource_id}"
  http_method = "${aws_api_gateway_method.get_ou.http_method}"

  integration_http_method = "GET"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.manager_lambda.invoke_arn}"

}

resource "aws_api_gateway_integration_response" "lambda3_mockapi_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.example.id
  resource_id = aws_api_gateway_resource.get_ou.id
  http_method = aws_api_gateway_method.get_ou.http_method
  status_code = aws_api_gateway_method_response.get_ou_api_response.status_code

  /**
   * This is second half of the CORS configuration.
   * Here we give values to each of the header parameters to ALLOW 
   * Cross-Origin requests from ALL hosts.
   **/
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers"     = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
    "method.response.header.Access-Control-Allow-Methods"     = "'GET,OPTIONS,POST,PUT'",
    "method.response.header.Access-Control-Allow-Origin"      = "'*'",
    "method.response.header.Access-Control-Allow-Credentials" = "'true'"
  }

  response_templates = {
    "application/json" = <<EOF
{
  "statusCode": 200,
  "message": "OK! Everything in order"
}
EOF
  }
}

resource "aws_api_gateway_integration" "lambda4" {
  rest_api_id = "${aws_api_gateway_rest_api.example.id}"
  resource_id = "${aws_api_gateway_method.delete.resource_id}"
  http_method = "${aws_api_gateway_method.delete.http_method}"

  integration_http_method = "DELETE"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.delete_lambda.invoke_arn}"

}

resource "aws_api_gateway_integration_response" "lambda4_mockapi_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.example.id
  resource_id = aws_api_gateway_resource.delete.id
  http_method = aws_api_gateway_method.delete.http_method
  status_code = aws_api_gateway_method_response.delete_api_response.status_code

  /**
   * This is second half of the CORS configuration.
   * Here we give values to each of the header parameters to ALLOW 
   * Cross-Origin requests from ALL hosts.
   **/
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers"     = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
    "method.response.header.Access-Control-Allow-Methods"     = "'GET,OPTIONS,POST,PUT'",
    "method.response.header.Access-Control-Allow-Origin"      = "'*'",
    "method.response.header.Access-Control-Allow-Credentials" = "'true'"
  }

  response_templates = {
    "application/json" = <<EOF
{
  "statusCode": 200,
  "message": "OK! Everything in order"
}
EOF
  }
}


resource "aws_api_gateway_deployment" "example" {
  depends_on = [
    "aws_api_gateway_integration.lambda",
    "aws_api_gateway_method_response.post_api_response",
    "aws_api_gateway_method_response.get_api_response",
    "aws_api_gateway_method_response.get_ou_api_response",
    "aws_api_gateway_method_response.delete_api_response"
  ]

  rest_api_id = "${aws_api_gateway_rest_api.example.id}"
}

resource "aws_api_gateway_stage" "development" {
  deployment_id = aws_api_gateway_deployment.example.id
  rest_api_id   = aws_api_gateway_rest_api.example.id
  stage_name    = "leaveRequestTF"
}

resource "aws_api_gateway_api_key" "API_Key" {
  name = "dev_api_key"
}

resource "aws_api_gateway_usage_plan" "api-plan" {
  name         = "api_usage_plan"
  description  = "usage plan for product"
  product_code = "01"

  api_stages {
    api_id = aws_api_gateway_rest_api.example.id
    stage  = aws_api_gateway_stage.development.stage_name
  }

  quota_settings {
    limit  = 20
    offset = 2
    period = "WEEK"
  }

  throttle_settings {
    burst_limit = 5
    rate_limit  = 10
  }
}

resource "aws_api_gateway_usage_plan_key" "main" {
  key_id        = aws_api_gateway_api_key.API_Key.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.api-plan.id
}

variable "api_resources" {
  default = ["aws_api_gateway_resource.post.id", "aws_api_gateway_resource.get.id","aws_api_gateway_resource.get_ou.id","aws_api_gateway_resource.delete.id"]
  type = list
}

module "cors" {
  source  = "squidfunk/api-gateway-enable-cors/aws"
  version = "0.3.3"

  api_id            = aws_api_gateway_rest_api.example.id
  api_resource_id   = aws_api_gateway_resource.get.id
  allow_credentials = true
}

module "corspost" {
  source  = "squidfunk/api-gateway-enable-cors/aws"
  version = "0.3.3"

  api_id            = aws_api_gateway_rest_api.example.id
  api_resource_id   = aws_api_gateway_resource.post.id
  allow_credentials = true
}

output "base_url" {
  value = "${aws_api_gateway_deployment.example.invoke_url}"
}