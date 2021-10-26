#%%
from faker import Faker
import faker
import pandas as pd
import random
from datetime import date
from datetime import datetime, timedelta
import numpy as np
# %%
df = pd.read_csv("database.csv")
# %%
print(df)
# %%
dfPerDays = pd.DataFrame()  
HoursOfLeave = ("4", "8")
# %%
print(dfPerDays)

# %%
fake = Faker()

ListOfPersonNumber = []
ListOfEmploymentNumber = []
ListOfLeaveYear = []
ListOfLeaveTypeCode = []
ListOfHoursOfLeave = []

ListOfSequenceNumbers = []
ListOfDateOfLeave = []

for x in range(df.shape[0]):
    start = pd.to_datetime(df['StartDate'][x])
    while str(start) != str((pd.to_datetime(df['EndDate'][x])  + timedelta(days=1)).date()):
        ListOfPersonNumber.append(df['PersonNumber'][x])
        ListOfEmploymentNumber.append(df['EmploymentNumber'][x])
        ListOfLeaveYear.append(df['LeaveYear'][x].item())
        ListOfLeaveTypeCode.append(df['LeaveTypeCode'][x])

        ListOfSequenceNumbers.append(df['SequenceNumber'][x])
        ListOfHoursOfLeave.append(random.choice(HoursOfLeave))

        ListOfDateOfLeave.append(start)
        start = (pd.to_datetime(start)  + timedelta(days=1)).date()

#%%
dfPerDays["PersonNumber"] = ListOfPersonNumber
dfPerDays["EmploymentNumber"] = ListOfEmploymentNumber
dfPerDays["LeaveYear"] = ListOfLeaveYear
dfPerDays["LeaveTypeCode"] = ListOfLeaveTypeCode

dfPerDays["SequenceNumber"] = ListOfSequenceNumbers
dfPerDays["HoursOfLeave"] = ListOfHoursOfLeave

dfPerDays["DateOfLeave"] = ListOfDateOfLeave

# %%
print(dfPerDays)
# %%
dfPerDays['DateOfLeave'] = dfPerDays['DateOfLeave'].dt.strftime('%Y-%m-%d')
for x in range(dfPerDays.shape[0]):   
    print(type(dfPerDays["DateOfLeave"][x]))    

#%%
for x in range(dfPerDays.shape[0]):   
    print(type(dfPerDays["LeaveYear"][x]))  
# %%
dfPerDays.to_csv("databasePerDay.csv")

# %%
