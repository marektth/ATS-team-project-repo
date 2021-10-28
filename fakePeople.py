#%%
from faker import Faker
import pandas as pd
import random
from datetime import date

#%%
LeaveTypeCode = ("WET", "BOV")
CodeLeaveReason = ("HOL", "Health","")
#%%
fake = Faker()

def create_rows(num=1):
    output = [{
                "PersonNumber":random.randint(1,2),
                "StartDate":fake.date_between(start_date='-20d', end_date='-1d'),
                "EndDate":fake.date_between(start_date='today', end_date='+10d'),
                "CodeLeaveReason":random.choice(CodeLeaveReason),
                } for _ in range(num)]
    return output

df = pd.DataFrame(create_rows(5))
new_row = {'PersonNumber':1, 'StartDate':fake.date_between(start_date='-500d', end_date='-230d'), 'EndDate':fake.date_between(start_date='-100d', end_date='-50d'), 'CodeLeaveReason':""}
df = df.append(new_row, ignore_index=True)
df = df.append(new_row, ignore_index=True)
#%%
listOfLeaveTypeCode = []
listOfPersons = []
listOfSequenceNumbers = []
listOfJobsIndexes = []
leaveYear = []
listOfStartDates = []
listOfEndDates = []

for x in range (df.shape[0]):
    leaveYear.append(df['StartDate'][x].year)
    listOfPersons.append(df['PersonNumber'][x])
    sequnceNumber =listOfPersons.count(df['PersonNumber'][x])
    listOfSequenceNumbers.append(sequnceNumber)

    if sequnceNumber == 1:
        listOfJobsIndexes.append(random.randint(1,10))
        listOfLeaveTypeCode.append(random.choice(LeaveTypeCode))
    else:
        idx = listOfPersons.index(df['PersonNumber'][x])
        listOfJobsIndexes.append(listOfJobsIndexes[idx])
        listOfLeaveTypeCode.append(listOfLeaveTypeCode[idx])
#%%
df['SequenceNumber'] = listOfSequenceNumbers
df['EmploymentNumber'] = listOfJobsIndexes
df['LeaveYear'] = leaveYear
df['LeaveTypeCode'] = listOfLeaveTypeCode

#%%
df = df.sort_values("PersonNumber")
df = df.reset_index(drop=True)

df['StartDate'] = pd.to_datetime(df['StartDate'])
df['EndDate'] = pd.to_datetime(df['EndDate'])

#%%
print(df)
#%%
uniPerson = df['PersonNumber'].unique()
skip = 0
for person in uniPerson:
    numberOfLeaves = df["PersonNumber"].where(df["PersonNumber"]==person).count()
    iteration = 0
    for x in range(numberOfLeaves-1):
        y = 0
        while numberOfLeaves-1 - iteration > y:
            i1 = pd.Interval(df['StartDate'][x+skip], df['EndDate'][x+skip])
            i2 = pd.Interval(df['StartDate'][x +y +1+skip], df['EndDate'][x +y+1+skip])
            overlap = i1.overlaps(i2)
            if overlap == True:
                df.drop(index= x + y+1+skip,axis=0, inplace=True)
                df = df.reset_index(drop=True)
                numberOfLeaves = df["PersonNumber"].where(df["PersonNumber"]==person).count()
                y = y -1
            y = y +1
        iteration = iteration +1
    skip = skip + df["PersonNumber"].where(df["PersonNumber"]==person).count()

#%%
#reset sequence numbers
listOfPersons = []
listOfSequenceNumbers = []

df.drop(['SequenceNumber'], axis=1, inplace=True)
for x in range (df.shape[0]):
    listOfPersons.append(df['PersonNumber'][x])
    sequnceNumber =listOfPersons.count(df['PersonNumber'][x])
    listOfSequenceNumbers.append(sequnceNumber)

df['SequenceNumber'] = listOfSequenceNumbers
#%%
df = df[['PersonNumber', 'EmploymentNumber', 'SequenceNumber', 'LeaveYear', 'LeaveTypeCode', 'StartDate', 'EndDate', 'CodeLeaveReason']]
#%%
df['StartDate'] = df["StartDate"].dt.strftime("%d/%m/%Y")
df['EndDate'] = df["EndDate"].dt.strftime("%d/%m/%Y")
#%%
for column in df:
    df[column] = df[column].apply(str)

#%%
print(df)
#%%
df.to_csv("database.csv")
# %%
