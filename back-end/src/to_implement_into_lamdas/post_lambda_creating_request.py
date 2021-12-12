import json
import pandas as pd
import numpy as np
from time import time

def load_table(path, as_df=True):
    if as_df:
        return pd.read_json(path)
    else:
        with open(path) as f:
            json_data = json.load(f)
        return json_data


if __name__ == "__main__":

    '''
        !! NEEDS TO BE OPTIMIZED !!
    '''

    # table init
    absence_table_path = "back-end/src/data/jsons/absence_data.json"

    # load data - absence
    absence_data = load_table(absence_table_path, as_df=False)
    date_format = '%d/%m/%Y'
    todays_date = pd.to_datetime(time(), unit='s')

    new_request_id = absence_data[-1]["id"] + 1
    # create request from API call
    new_request = {
        "id": new_request_id,
        "EmployeeID": 69,
        "AbsenceRequestedAt": time(),
        "AbsenceFrom": "14/12/2021",
        "AbsenceTo": "15/12/2021",
        "AbsenceTypeCode": "TIM",
        "Status": "Pending",
        "StatusResolution" : "",
        "LeaveReason": "Need to go to medical exam",
        "Rating": {}
    }

    # append to absence data table
    absence_data.append(new_request)

    # create dataframe from absence table
    absence_data = pd.DataFrame(absence_data)

    print(absence_data[absence_data['id'] == new_request_id])

    # check if request Absence timespan if its correct
    if pd.to_datetime(new_request['AbsenceTo'], format=date_format) < todays_date:
        absence_data.loc[absence_data['id'] == new_request_id, 'Status'] = "Rejected"
        absence_data.loc[absence_data['id'] == new_request_id, 'StatusResolution'] = "End date is earlier than request date"
        response = "set this response to OK - and END lambda"

    elif pd.to_datetime(new_request['AbsenceFrom'], format=date_format) < todays_date:
        absence_data.loc[absence_data['id'] == new_request_id, 'Status'] = "Rejected"
        absence_data.loc[absence_data['id'] == new_request_id, 'StatusResolution'] = "Start date is later than request date"
        response = "set this response to OK and END lambda"

    else:
        response = "set this response to sth went wrong and END lambda"

    # in case checks before were OK, continue:
        ## check if there are any requests with time-intervals intersecting request time-interval

    # get employee absence data
    employee_absence_data = absence_data.loc[absence_data['EmployeeID'] == new_request["EmployeeID"]]
    employee_absence_data = employee_absence_data[employee_absence_data['Status'].isin(["Accepted", "Pending"])]

    # check if dataframe not empty
    if not employee_absence_data.empty:

        # drop all columns except 'AbsenceFrom', 'AbsenceTo'
        employee_absence_data = employee_absence_data.loc[:, employee_absence_data.columns.isin(['id', 'AbsenceFrom', 'AbsenceTo'])]

        # format AbsenceFrom and AbsenceTo to pandas datetime + format to specified date format
        employee_absence_data['AbsenceFrom'] = pd.to_datetime(employee_absence_data['AbsenceFrom'], format=date_format)
        employee_absence_data['AbsenceTo'] = pd.to_datetime(employee_absence_data['AbsenceTo'], format=date_format)

        # drop all columns except 'AbsenceFrom', 'AbsenceTo'
        employee_absence_data = employee_absence_data.loc[:, employee_absence_data.columns.isin(['id', 'AbsenceFrom', 'AbsenceTo'])]

        # format AbsenceFrom and AbsenceTo to pandas datetime + format to specified date format
        employee_absence_data['AbsenceFrom'] = pd.to_datetime(employee_absence_data['AbsenceFrom'], format=date_format)
        employee_absence_data['AbsenceTo'] = pd.to_datetime(employee_absence_data['AbsenceTo'], format=date_format)

        # drop new request
        request = employee_absence_data[employee_absence_data['id'] == new_request_id]
        employee_absence_data = employee_absence_data.drop(request.index)

        # get nearest date to request, to filter out old data
        nearest_date = (employee_absence_data.loc[(employee_absence_data['AbsenceTo'] - \
                                    pd.to_datetime(new_request['AbsenceFrom'], format=date_format)).abs().idxmin(), 'AbsenceFrom'])
        

        # drop all absence data earlier than nearest date to request date
        employee_absence_data = employee_absence_data[employee_absence_data['AbsenceFrom'] >= nearest_date]
        employee_absence_data = employee_absence_data.append(request)

        a = np.triu(employee_absence_data['AbsenceTo'].values>employee_absence_data['AbsenceFrom'].values[:,None])
        b = np.triu(employee_absence_data['AbsenceFrom'].values<employee_absence_data['AbsenceTo'].values[:,None])

        # new request overlaps others Accepter or Pending
        if (employee_absence_data.shape[0] != (employee_absence_data[(a&b).sum(0)==1]).shape[0]):
            absence_data.loc[absence_data['id'] == new_request_id, 'Status'] = "Rejected"
            absence_data.loc[absence_data['id'] == new_request_id, 'StatusResolution'] = "Request timespan overlaps"
            response = "OK return lambda"

    #empty dataframe, no employee absences
    else:
        response = "OK return lambda"


    # if response OK, here save table to S3
    print(absence_data[absence_data['id'] == new_request_id])