#%%
import pandas as pd
import random
import names
# %%
def unique_numbers(num):
    listA = []
    while(len(listA) < num):
        x = random.randint(1,100)
        if x not in listA:
            listA.append(x)
    listA.sort()
    return listA

# %%
def unique_names(num):
    listA = []
    while(len(listA) < num):
        x = names.get_full_name()
        if x not in listA:
            listA.append(x)
    return listA
# %%
df_people = pd.DataFrame()
df_teams = pd.read_csv("databaseOfTeams.csv")
teams = df_teams.Team_id.unique()
#%%
num = 50
df_people["PersonNumber"] = unique_numbers(num)
df_people["PersonName"] = unique_names(num)
df_people["EmploymentNumber"] = [random.randint(1,10) for _ in range(len(df_people))]
df_people["Team"] = [random.choice(teams) for _ in range(len(df_people))]
# %%
df_people.to_csv("databaseOfPeople.csv")
# %%

