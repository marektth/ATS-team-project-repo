#%%
from faker import Faker
import pandas as pd
import random
import datetime

#%%
def create_rows(listOfPeoples,CodeLeaveReason,num=1):
    output = [{
                "PersonNumber":random.choice(listOfPeoples),
                "CodeLeaveReason":random.choice(CodeLeaveReason),
                } for _ in range(num)]
    return output
#%%
def DropOverLapingDatesOftheSamePerson(df):
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
    
    return df

#%%
def generateDataOfPeople(df,dfOfPeoples,LeaveTypeCode):
    fake = Faker()

    listOfLeaveTypeCode = []
    listOfPersons = []
    listOfSequenceNumbers = []
    listOfJobsIndexes = []
    listOfleaveYear = []
    listOfStartDates = []
    listOfEndDates = []

    for x in range (df.shape[0]):
        listOfPersons.append(df['PersonNumber'][x])
        sequnceNumber = listOfPersons.count(df['PersonNumber'][x])
        listOfSequenceNumbers.append(sequnceNumber)
        idxOfJob = dfOfPeoples.index[dfOfPeoples['PersonNumber'] == df['PersonNumber'][x]].tolist()
        listOfJobsIndexes.append(dfOfPeoples['EmploymentNumber'][idxOfJob[0]])

        if sequnceNumber == 1:
            listOfLeaveTypeCode.append(random.choice(LeaveTypeCode))
            newIntervalStartDate = fake.date_between(start_date='-600d', end_date='today')
            newIntervaEndDate = (pd.to_datetime(newIntervalStartDate) + datetime.timedelta(days=10)).date()

            listOfStartDates.append(newIntervalStartDate)
            listOfEndDates.append(fake.date_between(start_date=newIntervalStartDate, end_date=newIntervaEndDate))
            listOfleaveYear.append(newIntervalStartDate.year)

        else:
            idx = listOfPersons.index(df['PersonNumber'][x])
            newIntervalStartDate = fake.date_between(start_date='-100d', end_date='today')
            newIntervaEndDate = (pd.to_datetime(newIntervalStartDate) + datetime.timedelta(days=10)).date()

            listOfStartDates.append(newIntervalStartDate)
            listOfEndDates.append(fake.date_between(start_date=newIntervalStartDate, end_date=newIntervaEndDate))
            listOfLeaveTypeCode.append(listOfLeaveTypeCode[idx])
            listOfleaveYear.append(newIntervalStartDate.year)

    df['SequenceNumber'] = listOfSequenceNumbers
    df['EmploymentNumber'] = listOfJobsIndexes
    df['LeaveYear'] = listOfleaveYear
    df['LeaveTypeCode'] = listOfLeaveTypeCode
    df['StartDate'] = listOfStartDates
    df['EndDate'] = listOfEndDates
    return df
#%%
def resetSequenceNumber(df):
    listOfPersons = []
    listOfSequenceNumbers = []

    df.drop(['SequenceNumber'], axis=1, inplace=True)
    for x in range (df.shape[0]):
        listOfPersons.append(df['PersonNumber'][x])
        sequnceNumber =listOfPersons.count(df['PersonNumber'][x])
        listOfSequenceNumbers.append(sequnceNumber)

    df['SequenceNumber'] = listOfSequenceNumbers
    return df

#%%
LeaveTypeCode = ("WET", "BOV")
CodeLeaveReason = ("HOL", "Health","")
#%%
dfOfPeoples = pd.read_csv("databaseOfPeople.csv")
dfOfPeoples = dfOfPeoples.sort_values("PersonNumber")
dfOfPeoples = dfOfPeoples.reset_index(drop=True)
listOfPeoples = dfOfPeoples["PersonNumber"].tolist()
#%%
df = pd.DataFrame(create_rows(listOfPeoples,CodeLeaveReason,5))

df = df.sort_values("PersonNumber")
df = df.reset_index(drop=True)
#%%
df = generateDataOfPeople(df,dfOfPeoples,LeaveTypeCode)

#%%
df['StartDate'] = pd.to_datetime(df['StartDate'])
df['EndDate'] = pd.to_datetime(df['EndDate'])

df = DropOverLapingDatesOftheSamePerson(df)
#%%
df = df.sort_values(['PersonNumber', 'StartDate'])
df = df.reset_index(drop=True)
#%%
df = resetSequenceNumber(df)
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
