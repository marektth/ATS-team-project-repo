import json
import boto3
import os
import pandas as pd
import datetime as dt

s3_c = boto3.client('s3')

s3_bucket_name = os.environ.get('BUCKET_NAME')
s3_key_website_teams = os.environ.get('OBJECT_NAME_TEAMS')


def load_table(s3_bucket_name, s3_key_website):
    resp=s3_c.get_object(Bucket=s3_bucket_name, Key=s3_key_website)
    data=resp.get('Body')
    return json.load(data)
    
def permission_testing(s3_bucket_name, s3_key_website):
    s3 = boto3.resource('s3')
    
    try:
        s3.Object(s3_bucket_name, s3_key_website).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f"File ({s3_key_website})) required by this function does not exist!")
            return f"File ({s3_key_website})) required by this function does not exist!"
        else:
            print(f"File ({s3_key_website}) required by this function is not accessible!")
            raise e




def lambda_handler(event, context):
    
    teams_data = load_table(s3_bucket_name, s3_key_website_teams)
    teams_changed = []
    # load data
    todays_date = dt.datetime.today().strftime("%d/%m/%Y")
    teams_data = pd.DataFrame(teams_data)
    teams_data['LastChangeMS'] = pd.to_datetime(teams_data['LastChangeMS'], unit='s', origin='unix').dt.strftime("%d/%m/%Y")
    teams_data_only_changes = teams_data.loc[(teams_data['LastChangeMS'] == todays_date)]
    teams_changed = teams_data_only_changes["TeamName"].tolist()
    
    if not teams_changed:
        return 0
    else:
        notification = "List of teams where absence was changed: " + ' '.join(str(team) for team in teams_changed)
        
        client = boto3.client('sns')
        response = client.publish (
          TargetArn = "arn:aws:sns:eu-central-1:094291892872:ManagerNotification",
          Message = json.dumps({'default': notification}),
          MessageStructure = 'json'
        )
        
        return {
          'statusCode': 200,
          'body': json.dumps(response)
        }