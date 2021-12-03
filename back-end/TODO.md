# Backend


1. Add bucket versioning to the lambda zip bucket, add terraform upload file from repository to S3 functionality.
2. Add the whole project to IaaC.
3. Implement new decision rules into the lambda function.
4. Clean up the code (fix code smell issues), clean up AWS environment.


## DONE

1. Create new GET API method for manager  -> Manager is able to get information about his Team (OU).    * DONE *
2. Edit Get method lambda to send only the person data from whom the request came from (query parameters string in the url)   * DONE *
3. Implement api key verification for the API so only people with the api key can invoke the endpoints. * DONE - STILL NEED TO ADD IT TO IaaC * 

## Maybe

If there is enough time deploy the working POC to the staging environment.