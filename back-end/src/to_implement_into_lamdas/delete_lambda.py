import json
import pandas as pd


def load_table(path, as_df=True):
    if as_df:
        return pd.read_json(path)
    else:
        with open(path) as f:
            json_data = json.load(f)
        return json_data


def get_request_leave_hours(self, request, working_hours=8, date_format='%d/%m/%Y'):
    '''
        returns total leave hours of requested absence
        future feature - check if year has 356 or 366 days
    '''
    absence_from = pd.to_datetime(request["AbsenceFrom"], format=date_format)
    absence_to = pd.to_datetime(request["AbsenceTo"], format=date_format)
    days_delta = absence_to - absence_from
    
    if days_delta.days == 0:
        return working_hours
    else:
        return days_delta.days*working_hours


if __name__ == "__main__":
    # tables init
    absence_table_path = "back-end/src/data/jsons/absence_data.json"
    employees_table_path = "back-end/src/data/jsons/employees_table.json"

    # request to cancel - from DELETE lambda (API)
    request_id_to_cancel = 1
    '''
        "AbsenceFrom": "24/10/2021",
        "AbsenceTo": "28/10/2021"
    '''
    # cancel date the day when DELETE button is pressed on FE
    cancel_date = "27/10/2021"
    date_format = '%d/%m/%Y'


    # load data - employees and absence
    absence_data = load_table(absence_table_path)
    print(absence_data)
    employees_data = load_table(employees_table_path)

    # get absence request
    request_to_cancel = (absence_data.loc[absence_data["id"] == request_id_to_cancel]).iloc[0]

    # check if request to cancel is accepted or pending
    if request_to_cancel['Status'] == "Pending":
        # if pending change status to cancelled 
        # do not change column AbsenceTo
        absence_data.loc[absence_data['id'] == request_id_to_cancel, 'Status'] = "Cancelled"
        absence_data.loc[absence_data['id'] == request_id_to_cancel, 'StatusResolution'] = "Cancelled Pending request"
        response = "set this response to OK and END lambda"

    elif request_to_cancel['Status'] == "Accepted":
        # if accepted change status to cancelled
        # change column AbcenceTo to cancel_date
        # check if not cancel_date is not past AbsenceTo
        if pd.to_datetime(request_to_cancel['AbsenceTo'], format=date_format) > pd.to_datetime(cancel_date, format=date_format):

            #check if request if TIMEOFF
            if request_to_cancel['AbsenceTypeCode'] == "TIM":
                # add remaining absence hours to leave_balance of employee
                absence_from = pd.to_datetime(cancel_date, format=date_format)
                absence_to = pd.to_datetime(request_to_cancel["AbsenceTo"], format=date_format)
                working_hours = 8
                remaining_hours = ((absence_to - absence_from).days)*working_hours
                employee_leave_balance = (employees_data.loc[employees_data['EmployeeID']== request_to_cancel['EmployeeID']]['LeaveBalance']).values[0]
                employees_data.loc[employees_data['EmployeeID'] == request_to_cancel['EmployeeID'], 'LeaveBalance'] = employee_leave_balance + remaining_hours

            # set status to cancelled, change AbsenceTo to cancel_date, set StatusResolution to display user request state
            absence_data.loc[absence_data['id'] == request_id_to_cancel, 'Status'] = "Cancelled"
            absence_data.loc[absence_data['id'] == request_id_to_cancel, 'AbsenceTo'] = cancel_date
            absence_data.loc[absence_data['id'] == request_id_to_cancel, 'StatusResolution'] = "Cancelled Accepted request"

            response = "set this response to OK and END lambda"
        else:
            # if canceling is later or same as the end of absence
            response = "set this response to method not allowed and END lambda"
    else:
        # response - cancelling not allowed on other types of statuses (Rejected, ...)
        response = "set this response to method not allowed and END lambda"
        

    # if response OK, here save tables to S3
    print(absence_data)


    
    
    