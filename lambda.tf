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


resource "aws_lambda_function" "example" {
  function_name = "SIMPLE_API_TEST"

  s3_bucket = "apitest-bucket-123"
  s3_key    = "v1.0.0/example.zip"

  # "basic_API_handler.py" is the filename within the zip file and "handler"
  # is the name of the property under which the handler function was
  # exported in that file.
  handler = "main.lambda_handler"
  runtime = "python3.8"

  role = "${aws_iam_role.lambda_exec.arn}"
}

# IAM role which dictates what other AWS services the Lambda function
# may access.
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

resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = "${aws_api_gateway_rest_api.example.id}"
  parent_id   = "${aws_api_gateway_rest_api.example.root_resource_id}"
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy" {
  rest_api_id   = "${aws_api_gateway_rest_api.example.id}"
  resource_id   = "${aws_api_gateway_resource.proxy.id}"
  http_method   = "ANY"
  authorization = "NONE"
} 