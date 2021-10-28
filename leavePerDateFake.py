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
dfPerDays = pd.DataFrame()  
fake = Faker()
HoursOfLeave = ("4:00", "4:30", "5:00", "5:30", "6:00", "6:30", "7:00", "7:30", "8:00")

ListOfPersonNumber = []
ListOfEmploymentNumber = []
ListOfLeaveYear = []
ListOfLeaveTypeCode = []
ListOfHoursOfLeave = []
ListOfSequenceNumbers = []
ListOfDateOfLeave = []


# %%
for x in range(df.shape[0]):
    start = pd.to_datetime(df['StartDate'][x])
    hourse = random.choice(HoursOfLeave)
    while str(start) != str((pd.to_datetime(df['EndDate'][x]) + timedelta(days=1)).date()):
        ListOfPersonNumber.append(df['PersonNumber'][x])
        ListOfEmploymentNumber.append(df['EmploymentNumber'][x])
        ListOfLeaveYear.append(df['LeaveYear'][x])
        ListOfLeaveTypeCode.append(df['LeaveTypeCode'][x])
        ListOfSequenceNumbers.append(df['SequenceNumber'][x])

        ListOfHoursOfLeave.append(hourse)
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
dfPerDays["DateOfLeave"] = pd.to_datetime(dfPerDays["DateOfLeave"])
dfPerDays['DateOfLeave'] = dfPerDays["DateOfLeave"].dt.strftime("%d/%m/%Y")
#%%
for column in dfPerDays:
    dfPerDays[column] = dfPerDays[column].apply(str) 

# %%
print(dfPerDays)
# %%
dfPerDays.to_csv("databasePerDay.csv")

# %%
