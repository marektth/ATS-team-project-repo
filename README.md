# Documentation 


## Architecture of the product

![Architecture Diagram](images/diagram.drawio.png)


## Infrastructure

The infrastructure is deployed using Terraform. The terraform files used are: ```lambda.tf & api_gateway.tf```

## Description of the infrastructure

### Lambdas

<details closed>
<summary>GET Method Lambda</summary>
<br>
This lambda is responsible for the GET method of the api endpoint.
It has a dependency of a query parameter in the URL: personID
By catching the event of the requestor (fe. personID=3), it then returns all the information of the given persons absence data.
The code first checks if the bucket exists and after that check it checks if the function has the necessary permissions to access the bucket and its content.
Once these checks have successfuly passed it proceeds on parsing the event query and gets the necessary information from the S3 .json file.
</details>

<details closed>
<summary>Manager Lambda (Get method)</summary>
<br>
This lambda is responsible for the GET method of the manager api endpoint.
It has a dependency of a query parameter in the URL: managerID
By catching the event of the requestor (fe. managerID=3), it then returns all the information of the given managers team absence data.
The code first checks if the bucket exists and after that check it checks if the function has the necessary permissions to access the bucket and its content.
Once these checks have successfuly passed it proceeds on parsing the event query and gets the necessary information from the S3 .json file depending on the managerID.
</details>

<details closed>
<summary>DELETE Lambda (Delete method)</summary>
<br>
This lambda is responsible for the DELETE method of the api endpoint.
It has a dependency on the "id" parameter in the event body.
By catching the event of the id, it then proceeds to verify if the given requested absence date has been Approved or if it is still in Pending state.
The code first checks if the bucket exists and after that check it checks if the function has the necessary permissions to access the bucket and its content.
Once these checks have successfuly passed it proceeds on parsing the event query and gets the necessary information from the S3 .json file depending on the request ID.
The lambda function then returns the corresponding statusCode: 200 = Success, 405 = Operation not allowed, 404 = other type of error.
If the return value is 200, the deletion went on successfully.
</details>

<details closed>
<summary>POST Lambda (Delete method)</summary>
<br>
This lambda is responsible for the POST method of the api endpoint.
It has a dependency on the event body.
By catching the body, it creates a json dictionary of the requested absence by an employee.
The code first checks if the bucket exists and after that check it checks if the function has the necessary permissions to access the bucket and its content.
Once these checks have successfuly passed it proceeds on parsing the event query and checks if the person has a big enough leave balance, if he does, then it writes the requested absence into the DB.
The lambda function then returns the corresponding statusCode: 200.
</details>


## Terraform code

In this section the resource blocks present in the .tf files will be explained.

```js
resource "aws_lambda_function" "local_name_of_resource" {
  function_name = "name_of_function_on_cloud"  //here the developer defines the name of the function

  s3_bucket = "bucket_name"  //name of the bucket where the source code (in zipped format) is located
  s3_key    = "zip_file_name" //path to the .zip file

  handler = "main.lambda_handler" //file executor (main.py)
  runtime = "python3.8" //runtime (python, node etc..)

  role = "${aws_iam_role.lambda_exec.arn}" //define the role which the lambda function will be using
  layers = ["arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-pandas:43", "arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-numpy:22"] //import necessary layers for code execution
   environment {
    variables = {
      BUCKET_NAME = "s3_bucket_name" //define env. variables
      OBJECT_NAME_TEAMS = "db_file_name"
    }
  }
}



resource "aws_sns_topic" "local_sns_topic_name" { //create sns topic
  name = "name_of_sns_topic" //define name for sns topic on the cloud
}

resource "aws_sns_topic_subscription" "local_name_for_subscription" { //create subscription to sns topic
  topic_arn = aws_sns_topic.manager_updates.arn // depends on the topic above
  protocol  = "email" //message protocol (email, email-json, push notif, sms etc..)
  endpoint  = "value_here" // endpoint address (phone number, webhook url, email address etc.)
}



resource "aws_cloudwatch_event_rule" "local_name_for_cw_event_rule" {
    name = "value_here" //define name for cw event rule
    description = "Launches every day at 18:01" // description of the event rule
    schedule_expression = "cron(01 18 * * ? *)" //cron job expression in cw format
}

resource "aws_cloudwatch_event_target" "local_name_for_cw_event_target" {
    rule = "${aws_cloudwatch_event_rule.every_day_mail.name}"//depends on the event rule specified above
    target_id = "MAILING_LAMBDA" // target id 
    arn = "${aws_lambda_function.mailing_lambda.arn}" //arn of the targeted lambda
}

resource "aws_lambda_permission" "local_name_for_lambda_permission" {
    statement_id = "AllowExecutionFromCloudWatch" //statement from where it will execute
    action = "lambda:InvokeFunction" // what we want it to do(action)
    function_name = "${aws_lambda_function.mailing_lambda.function_name}" //link to dependent arn of lambda
    principal = "events.amazonaws.com" // what service launches the process 
    source_arn = "${aws_cloudwatch_event_rule.every_day_mail.arn}" //source arn for the cw event rule
}



resource "aws_api_gateway_resource" "local_name_for_api_resource" {
  rest_api_id = "${aws_api_gateway_rest_api.example.id}" //dependend on the api id
  parent_id   = "${aws_api_gateway_rest_api.example.root_resource_id}" //dependent on the root resource of the api 
  path_part   = "submit" // URL path
}


resource "aws_api_gateway_method_response" "local_method_response_name" {
  rest_api_id = aws_api_gateway_rest_api.example.id //dependend on the api id
  resource_id = aws_api_gateway_resource.post.id //dependent on the resource of the api (in this case post, which is above)
  http_method = aws_api_gateway_method.post.http_method // dependent on the method of the api (in this case post)
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

resource "aws_lambda_permission" "local_name_for_lambda_perms" {
  statement_id  = "AllowAPIGatewayInvoke_POST" //what we want it to invoke
  action        = "lambda:InvokeFunction" //what action
  function_name = "${aws_lambda_function.post_lambda.function_name}" //what function it is for
  principal     = "apigateway.amazonaws.com" // service responsible for the action

  
  source_arn = "${aws_api_gateway_rest_api.example.execution_arn}/*/*"
}


resource "aws_api_gateway_rest_api" "local_name_for_api_gw_api" {
  name        = "Absence_Data_API" // name of the api in the cloud interface
  description = "First stage of API" // description of the api
}

resource "aws_api_gateway_integration" "local_name_for_apigw_integration" {
  rest_api_id = "${aws_api_gateway_rest_api.example.id}" //depends on rest api id above
  resource_id = "${aws_api_gateway_method.post.resource_id}" // depends  on api resource id of post
  http_method = "${aws_api_gateway_method.post.http_method}"// depends  on api method id of post

  integration_http_method = "POST" //integration method
  type                    = "AWS_PROXY" // type of api integration
  uri                     = "${aws_lambda_function.post_lambda.invoke_arn}" //invoke uri of lambda function
}

resource "aws_api_gateway_integration_response" "lambda_lambda_api_gw_integration_response_name" {
  rest_api_id = aws_api_gateway_rest_api.example.id //depends on rest api id above
  resource_id = aws_api_gateway_resource.post.id // depends  on api resource id of post
  http_method = aws_api_gateway_method.post.http_method // depends  on api method id of post
  status_code = aws_api_gateway_method_response.post_api_response.status_code // depends on api method response code

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


resource "aws_api_gateway_deployment" "local_deployment_of_api_name" {
  //the deployment of the api depends on the resources in this list (this block makes sure they are created before this resource block gets executed)  
  depends_on = [
    "aws_api_gateway_integration.lambda", 
    "aws_api_gateway_method_response.post_api_response",
    "aws_api_gateway_method_response.get_api_response",
    "aws_api_gateway_method_response.get_ou_api_response",
    "aws_api_gateway_method_response.delete_api_response"
  ]

  rest_api_id = "${aws_api_gateway_rest_api.example.id}" //which api to deploy
}

resource "aws_api_gateway_stage" "local_name_for_stage_resource" {
  deployment_id = aws_api_gateway_deployment.example.id //references deployment id above
  rest_api_id   = aws_api_gateway_rest_api.example.id // references api id above
  stage_name    = "value_here" // definition of stage name
}

//creation of api key
resource "aws_api_gateway_api_key" "local_api_key_resource_name" {
  name = "value_here" //name of the api key 
}

resource "aws_api_gateway_usage_plan" "local_api_plan_resource_name" {
  name         = "value_here" // name of api plan to be deployed
  description  = "usage plan for product" // description of api plan
  product_code = "01" // code of api plan

  //which stages will use this api plan  
  api_stages {
    api_id = aws_api_gateway_rest_api.example.id
    stage  = aws_api_gateway_stage.development.stage_name
  }
  //quota settings for the number of calls for the api endpoints
  quota_settings {
    limit  = 20
    offset = 2
    period = "WEEK"
  }
  //throttle settings
  throttle_settings {
    burst_limit = 5
    rate_limit  = 10
  }
}

//assigning the above created api_key to the usage_plan
resource "aws_api_gateway_usage_plan_key" "main" {
  key_id        = aws_api_gateway_api_key.API_Key.id //depends on the api key id
  key_type      = "API_KEY" // key type (in our case API KEY)
  usage_plan_id = aws_api_gateway_usage_plan.api-plan.id // depends on the usage_plan id
}

//calling cors module to enable cors for the given api methods (has to be called multiple times, does not support entry of resource id from list)
module "cors" {
  source  = "squidfunk/api-gateway-enable-cors/aws"
  version = "0.3.3"

  api_id            = aws_api_gateway_rest_api.example.id
  api_resource_id   = aws_api_gateway_resource.get.id
  allow_credentials = true
}

```

## Tests

The tool for testing is called **Coverage**. Main testing functions are **Assert Equal, Assert Array Equal, Assert Frame Equal and Assert Series Equal.**

### ARS test

In ARS test the main goal is to test the overall functionality of the code. It's using test cases as a main approach to test every possible scenario, which may occur. Every test case is testing if the dataframe returned by main ARS file is same as expected dataframe.

1. Test case is testing 2 employees with requested timeoff at the different days. 
2. Test case is testing 2 employees with requested timeoff at the same days. 
3. Test case is testing 2 employees with one requesting timeoff and second requesting parental holiday at the same day. 
4. Test case is testing 2 employees with both of them requesting parental holiday at the different days. 
5. Test case is testing 2 employees with one of them requesting parental holiday and second one requesting special holiday at the different days. 
6. Test case is testing 2 employees with requested timeoff at the same 5 days. 
7. Test case is testing 2 employees with requested timeoff with overlapping days, one employee is requesting 3 days and the other 5 days.


### Data Handler test

Data Handler test is testing every function in original file Data Handler. Every function is testing if output from the function in Data handler is same as expected output. Both expected output and output from the function must be equal, otherwise test returns error.
