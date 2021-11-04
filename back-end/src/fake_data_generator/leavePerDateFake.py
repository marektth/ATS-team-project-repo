#%%
from faker import Faker
import faker
import pandas as pd
import random
import datetime
import numpy as np
#%%
def generate_leave_per_date(df_per_days):
    hours_of_leave = ("4:00", "4:30", "5:00", "5:30", "6:00", "6:30", "7:00", "7:30", "8:00")

    list_of_person_number = []
    list_of_employment_number = []
    list_of_leave_per_year = []
    list_leave_type_code = []
    list_of_hours_leave = []
    list_of_sequence_number = []
    list_of_date_of_leaves = []

    for x in range(df.shape[0]):
        start = datetime.datetime.strptime(df['StartDate'][x], '%d/%m/%Y')
        hourse = random.choice(hours_of_leave)
        number = datetime.datetime.strptime(df['EndDate'][x], '%d/%m/%Y').date()- datetime.datetime.strptime(df['StartDate'][x], '%d/%m/%Y').date()
        for _ in range(number.days +1):
            list_of_person_number.append(df['PersonNumber'][x])
            list_of_employment_number.append(df['EmploymentNumber'][x])
            list_of_leave_per_year.append(df['LeaveYear'][x])
            list_leave_type_code.append(df['LeaveTypeCode'][x])
            list_of_sequence_number.append(df['SequenceNumber'][x])

            list_of_hours_leave.append(hourse)
            list_of_date_of_leaves.append(start)
            start = (start  + datetime.timedelta(days=1))

    df_per_days["PersonNumber"] = list_of_person_number
    df_per_days["EmploymentNumber"] = list_of_employment_number
    df_per_days["LeaveYear"] = list_of_leave_per_year
    df_per_days["LeaveTypeCode"] = list_leave_type_code
    df_per_days["SequenceNumber"] = list_of_sequence_number
    df_per_days["hoursOfLeave"] = list_of_hours_leave
    df_per_days["DateOfLeave"] = list_of_date_of_leaves

    return df_per_days

# %%
df = pd.read_csv("database.csv")

# %%
df_per_days = pd.DataFrame()  
df_per_days = generate_leave_per_date(df_per_days)
#%%
df_per_days['DateOfLeave'] = df_per_days["DateOfLeave"].dt.strftime("%d/%m/%Y")
#%%
for column in df_per_days:
    df_per_days[column] = df_per_days[column].apply(str) 

# %%
print(df_per_days)
# %%
df_per_days.to_csv("databasePerDay.csv")

# %%
