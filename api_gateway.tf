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

resource "aws_api_gateway_integration" "lambda2" {
  rest_api_id = "${aws_api_gateway_rest_api.example.id}"
  resource_id = "${aws_api_gateway_method.get.resource_id}"
  http_method = "${aws_api_gateway_method.get.http_method}"

  integration_http_method = "GET"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.get_lambda.invoke_arn}"
}

resource "aws_api_gateway_integration" "lambda3" {
  rest_api_id = "${aws_api_gateway_rest_api.example.id}"
  resource_id = "${aws_api_gateway_method.get.resource_id}"
  http_method = "${aws_api_gateway_method.get.http_method}"

  integration_http_method = "GET"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.manager_lambda.invoke_arn}"

}

resource "aws_api_gateway_deployment" "example" {
  depends_on = [
    "aws_api_gateway_integration.lambda"
  ]

  rest_api_id = "${aws_api_gateway_rest_api.example.id}"
  stage_name  = "leaveRequest"
}

output "base_url" {
  value = "${aws_api_gateway_deployment.example.invoke_url}"
}