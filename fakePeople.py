#%%
from faker import Faker
import pandas as pd
import random
from datetime import date

#%%
programing_skill = ("C#", "C", "python","c++")
LeaveTypeCode = ("WET", "BOV")
CodeLeaveReason = ("HOL", "Health","")
#%%
fake = Faker()

def create_rows(num=1):
    output = [{
                "PersonNumber":random.randint(1,2),
                "LeaveTypeCode":random.choice(LeaveTypeCode),
                "StartDate":fake.date_between(start_date='-3d', end_date='-1d'),
                "EndDate":fake.date_between(start_date='today', end_date='+3d'),
                "CodeLeaveReason":random.choice(CodeLeaveReason),
                } for x in range(num)]
    return output

# %%
df = pd.DataFrame(create_rows(5))
#%%
listOfPersons = []
listOfSequenceNumbers = []
listOfJobsIndexes = []
leaveYear = []

for x in range (df.shape[0]):
    leaveYear.append(df['StartDate'][x].year)
    listOfPersons.append(df['PersonNumber'][x])
    sequnceNumber =listOfPersons.count(df['PersonNumber'][x])
    listOfSequenceNumbers.append(sequnceNumber)

    if sequnceNumber == 1:
        listOfJobsIndexes.append(random.randint(1,10))
    else:
        idx = listOfPersons.index(df['PersonNumber'][x])
        listOfJobsIndexes.append(listOfJobsIndexes[idx])
#%%
df['SequenceNumber'] = listOfSequenceNumbers
df['EmploymentNumber'] = listOfJobsIndexes
df['LeaveYear'] = leaveYear

#%%
df = df.sort_values("PersonNumber")
#%%
df = df.reset_index(drop=True)
#%%
df = df[['PersonNumber', 'EmploymentNumber', 'SequenceNumber', 'LeaveYear', 'LeaveTypeCode', 'StartDate', 'EndDate', 'CodeLeaveReason']]
#%%
df
#%%
df.to_csv("database.csv")
# %%
