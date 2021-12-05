import json
from pprint import pprint
import boto3
import botocore
from botocore.exceptions import ClientError
import os

s3 = boto3.client('s3')



s3_bucket_name = os.environ.get('BUCKET_NAME')
s3_key_website_absence = os.environ.get('OBJECT_NAME_ABSENCE')
s3_key_website_teams = os.environ.get('OBJECT_NAME_TEAMS')
s3_key_website_employees = os.environ.get('OBJECT_NAME_EMPLOYEES')


def lambda_handler(event, context):
    # TODO implement
    
    #print(event)
    
    s3 = boto3.resource('s3')
    managerID = event["queryStringParameters"]['managerID']
    
    try:
        s3.Object(s3_bucket_name, s3_key_website_absence).load()
        s3.Object(s3_bucket_name, s3_key_website_teams).load()
        s3.Object(s3_bucket_name, s3_key_website_employees).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f"File ({s3_key_website_absence})) required by this function does not exist!")
            return f"File ({s3_key_website_absence})) required by this function does not exist!"
        else:
            raise f"File ({s3_key_website_absence}) required by this function is not accessible!"
            print(f"File ({s3_key_website_absence}) required by this function is not accessible!")
            return f"File ({s3_key_website_absence}) required by this function is not accessible!"
        if e.response['Error']['Code'] == "404":
            print(f"File ({s3_key_website_teams})) required by this function does not exist!")
            return f"File ({s3_key_website_teams})) required by this function does not exist!"
        else:
            raise f"File ({s3_key_website_teams}) required by this function is not accessible!"
            print(f"File ({s3_key_website_teams}) required by this function is not accessible!")
            return f"File ({s3_key_website_teams}) required by this function is not accessible!"
        if e.response['Error']['Code'] == "404":
            print(f"File ({s3_key_website_employees})) required by this function does not exist!")
            return f"File ({s3_key_website_employees})) required by this function does not exist!"
        else:
            raise f"File ({s3_key_website_employees}) required by this function is not accessible!"
            print(f"File ({s3_key_website_employees}) required by this function is not accessible!")
            return f"File ({s3_key_website_employees}) required by this function is not accessible!"

    
    
    
    #print(managerID)
    
    #table_name = os.environ['TABLE_NAME']
    #table = dynamodb.Table(table_name)
    #list_to_return = []
    #dynamodb = boto3.resource('dynamodb')
    
     ## ---- assigning table paths -----
    #path_absence_table = os.environ['ABSENCE_TABLE'] #Absence_Data table DynamoDB
    #path_teams_table = os.environ['TEAM_TABLE'] #OU_Table table dynamoDB
    #path_employees_table = os.environ['EMPLOYEES_TABLE'] #Employees table dynamoDB
    
    obj_absence_table = s3.Object(s3_bucket_name, s3_key_website_absence)
    data_absence_table = obj_absence_table.get()['Body'].read().decode('utf-8')
    json_data_absence = json.loads("" + 
        data_absence_table.replace("}\n{", "},\n{") + 
    "")

    obj_teams_table = s3.Object(s3_bucket_name, s3_key_website_teams)
    data_teams_table = obj_teams_table.get()['Body'].read().decode('utf-8')
    json_data_teams = json.loads("" + 
        data_teams_table.replace("}\n{", "},\n{") + 
    "")
    
    obj_employees_table = s3.Object(s3_bucket_name, s3_key_website_employees)
    data_employees_table = obj_employees_table.get()['Body'].read().decode('utf-8')
    json_data_employees = json.loads("" + 
        data_employees_table.replace("}\n{", "},\n{") + 
    "")
    
    
    ## ---- loading tables -----
    
    #load_absence_table = dynamodb.Table(path_absence_table)
    #load_teams_table = dynamodb.Table(path_teams_table)
    #load_employees_table = dynamodb.Table(path_employees_table)
    
    
    try:
        #absence_table = load_absence_table.scan()
        #teams_table = load_teams_table.scan()
        #employees_table = load_employees_table.scan()
        #print(x)
        #df = pd.json_normalize(x['Items'])
        teams_return_data = ""
        #teams_table_list = teams_table['Items']
        
        for index in range (len(json_data_teams)):
            if str(json_data_teams[index]['ManagerID']) == managerID:
                json_data_teams[index]['ManagerID'] = managerID
                json_data_teams[index]['OUID'] = str(json_data_teams[index]['OUID'])
                teams_return_data = json_data_teams[index]['OUID']
                #print(teams_return_data)
        #print("TEAMS RETURN DATA")
        #print(teams_return_data)
                
        #employees_table_list = employees_table['Items']
        employees_return_data = []
        
        for index in range (len(json_data_employees)):
            if str(json_data_employees[index]['OUID']) == str(teams_return_data):
                json_data_employees[index]['EmployeeID'] = str(json_data_employees[index]['EmployeeID'])
                employees_return_data.append(json_data_employees[index]['EmployeeID'])
        #print("EMPLOYEES RETURN DATA BELOW")
        #print(employees_return_data)
        #absence_table_list = absence_table['Items']
        return_data = []
        
        #change EmployeeID to Employee ID in this for
        for index in range (len(json_data_absence)):
            for y in range (len(employees_return_data)):
                if str(json_data_absence[index]['EmployeeID']) == employees_return_data[y]:
                    #print("INSIDE IF")
                    json_data_absence[index]['EmployeeID'] = str(json_data_absence[index]['EmployeeID'])
                    return_data.append(json_data_absence[index])
        #print(return_data)   
                
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
