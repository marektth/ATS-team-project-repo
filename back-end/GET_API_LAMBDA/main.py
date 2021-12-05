import json
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import os

s3 = boto3.client('s3')

s3_bucket_name = os.environ.get('BUCKET_NAME')
s3_key_website = os.environ.get('OBJECT_NAME')


def lambda_handler(event, context):
    # TODO implement
    
    #print(event)
    employeeID = event["queryStringParameters"]['personID']
    listOfEntries = []
    s3 = boto3.resource('s3')
    
    try:
        s3.Object(s3_bucket_name, s3_key_website).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f"File ({s3_key_website})) required by this function does not exist!")
            return f"File ({s3_key_website})) required by this function does not exist!"
        else:
            raise f"File ({s3_key_website}) required by this function is not accessible!"
            print(f"File ({s3_key_website}) required by this function is not accessible!")
            return f"File ({s3_key_website}) required by this function is not accessible!"

    
    
    
    
    '''
    json_data = json.loads("" + 
        data.replace("}\n{", "},\n{") + 
    "")
    
    json_data = json.dumps(json_data)
    '''
    

    
    #print(employeeID)
    
    #dynamodb = boto3.resource('dynamodb')
    #table_name = os.environ['TABLE_NAME']
   
    #table = dynamodb.Table(table_name)
    #list_to_return = []
    try:
        #x = table.scan()
        #print(x)
        #df = pd.json_normalize(x['Items'])
        obj = s3.Object(s3_bucket_name, s3_key_website)
        data = obj.get()['Body'].read().decode('utf-8')
        return_data = []
        #table_list = x['Items']
        if employeeID == "all":
            json_data = json.loads("" + 
            data.replace("}\n{", "},\n{") + 
            "")
            return_data.append(json_data)
            
        
        
        
        json_data = json.loads("" + 
            data.replace("}\n{", "},\n{") + 
            "")
    
        #print(data)
        for index in range (len(json_data)):
            if str(json_data[index]['EmployeeID']) == employeeID:
                json_data[index]['EmployeeID'] = employeeID
                return_data.append(json_data[index])
                
        #print(df['EmployeeID'])
        #return_data = df.index[df['Employee ID'] == employeeID].tolist()       ## OG CODE..
        #print(return_data)
        #list_to_return.append(df['EmployeeID'][return_data][0])
        #list_to_return = df.iloc[return_data]   ## OG CODE
        #print(list_to_return)
        #list_to_return = df.to_json(orient="split") ## OG CODE
        parsed = json.dumps(return_data)
        #print(parsed)
        
    except ClientError as e:
        print()
        response = {
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": e.response['Error']['Message']
        }
        
        return response
    else:
        response = {
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": parsed
        }
        
        return response
    
    
    
    return response
