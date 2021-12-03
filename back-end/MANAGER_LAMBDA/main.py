import json
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import os


def lambda_handler(event, context):
    # TODO implement
    
    #print(event)
    
   
    
    
    
    managerID = event["queryStringParameters"]['managerID']
    #print(managerID)
    
    #table_name = os.environ['TABLE_NAME']
    #table = dynamodb.Table(table_name)
    #list_to_return = []
    dynamodb = boto3.resource('dynamodb')
    
     ## ---- assigning table paths -----
    path_absence_table = os.environ['ABSENCE_TABLE'] #Absence_Data table DynamoDB
    path_teams_table = os.environ['TEAM_TABLE'] #OU_Table table dynamoDB
    path_employees_table = os.environ['EMPLOYEES_TABLE'] #Employees table dynamoDB
    
    ## ---- loading tables -----
    
    load_absence_table = dynamodb.Table(path_absence_table)
    load_teams_table = dynamodb.Table(path_teams_table)
    load_employees_table = dynamodb.Table(path_employees_table)
    
    
    try:
        absence_table = load_absence_table.scan()
        teams_table = load_teams_table.scan()
        employees_table = load_employees_table.scan()
        #print(x)
        #df = pd.json_normalize(x['Items'])
        teams_return_data = ""
        teams_table_list = teams_table['Items']
        
        for index in range (len(teams_table_list)):
            if str(teams_table_list[index]['ManagerID']) == managerID:
                teams_table_list[index]['ManagerID'] = managerID
                teams_table_list[index]['OUID'] = str(teams_table_list[index]['OUID'])
                teams_return_data = teams_table_list[index]['OUID']
                #print(teams_return_data)
        #print("TEAMS RETURN DATA")
        #print(teams_return_data)
                
        employees_table_list = employees_table['Items']
        employees_return_data = []
        
        for index in range (len(employees_table_list)):
            if str(employees_table_list[index]['OUID']) == str(teams_return_data):
                employees_table_list[index]['EmployeeID'] = str(employees_table_list[index]['EmployeeID'])
                employees_return_data.append(employees_table_list[index]['EmployeeID'])
        #print("EMPLOYEES RETURN DATA BELOW")
        #print(employees_return_data)
        absence_table_list = absence_table['Items']
        return_data = []
        
        for index in range (len(absence_table_list)):
            for y in range (len(employees_return_data)):
                if str(absence_table_list[index]['Employee ID']) == employees_return_data[y]:
                    #print("INSIDE IF")
                    absence_table_list[index]['Employee ID'] = str(absence_table_list[index]['Employee ID'])
                    return_data.append(absence_table_list[index])
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
