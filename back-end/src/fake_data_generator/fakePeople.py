#%%
from faker import Faker
import pandas as pd
import random
import datetime

#%%
def create_rows(list_of_peoples,code_leave_reason,num=1):
    output = [{
                "PersonNumber":random.choice(list_of_peoples),
                "CodeLeaveReason":random.choice(code_leave_reason),
                } for _ in range(num)]
    return output
#%%
def drop_overlaping_dates_of_the_same_person(df):
    uni_person = df['PersonNumber'].unique()
    skip = 0
    for person in uni_person:
        number_of_leaves = df["PersonNumber"].where(df["PersonNumber"]==person).count()
        iteration = 0
        for x in range(number_of_leaves-1):
            y = 0
            while number_of_leaves-1 - iteration > y:
                i1 = pd.Interval(df['StartDate'][x+skip], df['EndDate'][x+skip])
                i2 = pd.Interval(df['StartDate'][x +y +1+skip], df['EndDate'][x +y+1+skip])
                overlap = i1.overlaps(i2)
                if overlap == True:
                    df.drop(index= x + y+1+skip,axis=0, inplace=True)
                    df = df.reset_index(drop=True)
                    number_of_leaves = df["PersonNumber"].where(df["PersonNumber"]==person).count()
                    y = y -1
                y = y +1
            iteration = iteration +1
        skip = skip + df["PersonNumber"].where(df["PersonNumber"]==person).count()
    
    return df

#%%
def generate_data_of_people(df,df_of_peoples,leave_type_code):
    fake = Faker()

    list_Of_leave_type_code = []
    list_of_persons = []
    list_of_sequence_numbers = []
    list_of_jobs = []
    list_of_years = []
    list_of_start_dates = []
    list_of_end_dates = []

    for x in range (df.shape[0]):
        list_of_persons.append(df['PersonNumber'][x])
        sequence_number = list_of_persons.count(df['PersonNumber'][x])
        list_of_sequence_numbers.append(sequence_number)
        idx_of_job = df_of_peoples.index[df_of_peoples['PersonNumber'] == df['PersonNumber'][x]].tolist()
        list_of_jobs.append(df_of_peoples['EmploymentNumber'][idx_of_job[0]])

        if sequence_number == 1:
            list_Of_leave_type_code.append(random.choice(leave_type_code))
            new_interval_start_date = fake.date_between(start_date='-600d', end_date='today')
            new_interval_enddate = (pd.to_datetime(new_interval_start_date) + datetime.timedelta(days=10)).date()

            list_of_start_dates.append(new_interval_start_date)
            list_of_end_dates.append(fake.date_between(start_date=new_interval_start_date, end_date=new_interval_enddate))
            list_of_years.append(new_interval_start_date.year)

        else:
            idx = list_of_persons.index(df['PersonNumber'][x])
            new_interval_start_date = fake.date_between(start_date='-100d', end_date='today')
            new_interval_enddate = (pd.to_datetime(new_interval_start_date) + datetime.timedelta(days=10)).date()

            list_of_start_dates.append(new_interval_start_date)
            list_of_end_dates.append(fake.date_between(start_date=new_interval_start_date, end_date=new_interval_enddate))
            list_Of_leave_type_code.append(list_Of_leave_type_code[idx])
            list_of_years.append(new_interval_start_date.year)

    df['SequenceNumber'] = list_of_sequence_numbers
    df['EmploymentNumber'] = list_of_jobs
    df['LeaveYear'] = list_of_years
    df['LeaveTypeCode'] = list_Of_leave_type_code
    df['StartDate'] = list_of_start_dates
    df['EndDate'] = list_of_end_dates
    return df
#%%
def reset_sequence_number(df):
    list_of_persons = []
    list_of_sequence_numbers = []

    df.drop(['SequenceNumber'], axis=1, inplace=True)
    for x in range (df.shape[0]):
        list_of_persons.append(df['PersonNumber'][x])
        sequence_number =list_of_persons.count(df['PersonNumber'][x])
        list_of_sequence_numbers.append(sequence_number)

    df['SequenceNumber'] = list_of_sequence_numbers
    return df

#%%
leave_type_code = ("WET", "BOV")
code_leave_reason = ("HOL", "Health","")
#%%
df_of_peoples = pd.read_csv("databaseOfPeople.csv")
df_of_peoples = df_of_peoples.sort_values("PersonNumber")
df_of_peoples = df_of_peoples.reset_index(drop=True)
list_of_peoples = df_of_peoples["PersonNumber"].tolist()
#%%
df = pd.DataFrame(create_rows(list_of_peoples,code_leave_reason,5))

df = df.sort_values("PersonNumber")
df = df.reset_index(drop=True)
#%%
df = generate_data_of_people(df,df_of_peoples,leave_type_code)

#%%
df['StartDate'] = pd.to_datetime(df['StartDate'])
df['EndDate'] = pd.to_datetime(df['EndDate'])

df = drop_overlaping_dates_of_the_same_person(df)
#%%
df = df.sort_values(['PersonNumber', 'StartDate'])
df = df.reset_index(drop=True)
#%%
df = reset_sequence_number(df)
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
