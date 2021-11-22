from numpy import empty
import db_get_data as csv 
import pandas as pd
import datetime



def get_employees(csv_file):
    df = pd.read_csv(csv_file)
    df = pd.DataFrame(df)
    df = df.where(df["OUID"] == 32).dropna()
    df = df.head(5)

    return df

def get_absence_data():
    absence_data = [
        {
            "id" : 0,
            "EmployeeID" : 14,
            "DateOfAbsence" : "22/10/2021",
            "Status" : "Accepted"
        },
        {
            "id" : 1,
            "EmployeeID" : 18,
            "DateOfAbsence" : "22/10/2021",
            "Status" : "Accepted"
        },
        {
            "id" : 2,
            "EmployeeID" : 98,
            "DateOfAbsence" : "22/10/2021",
            "Status" : "Accepted"
        },
        {
            "id" : 3,
            "EmployeeID" : 100,
            "DateOfAbsence" : "28/10/2021",
            "Status" : "Accepted"
        },
    ]

    df = pd.DataFrame(absence_data)
    return df



def capacity_rule(min_capacity, absence_data_accepted, absence_request):

    # if(status != "Pending" or status.empty):
    #     return absence_request

    if(not absence_data_accepted.empty):
        absence_data_accepted['DateOfAbsence'] =  (pd.to_datetime(absence_data_accepted['DateOfAbsence'], format='%d/%m/%Y')).dt.dayofyear
        absence_request["DayOfYear"] = (pd.to_datetime(absence_request['DateOfAbsence'], format='%d/%m/%Y')).dt.dayofyear

        employee_absence_overlap = 0
        for idx in range(absence_data_accepted.shape[0]):
            if absence_request["DayOfYear"][0] - absence_data_accepted['DateOfAbsence'][idx] == 0:
                employee_absence_overlap += 1
           

        if employee_absence_overlap > min_capacity:
            #change in db
            absence_request["Status"] = "Rejected"
            return absence_request
        else:
            return absence_request
    else:
        absence_request["Status"] = "Accepted"
        return absence_request


def main():
    absence_data = get_absence_data()

    absence_requests_db = [
        {
            "id" : 3,
            "EmployeeID" : 100,
            "DateOfAbsence" : "22/10/2021",
            "Status" : "Pending"
        }
    ]
    absence_requests_db = pd.DataFrame(absence_requests_db)

    print(capacity_rule(min_capacity = 2, absence_data_accepted = absence_data, absence_request = absence_requests_db))


if __name__ == "__main__":
    main()