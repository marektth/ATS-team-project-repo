#%%
import numpy as np
import pandas as pd
import random
import string
#%%
def unique_numbers(num):
    listA = []
    while(len(listA) < num):
        x = random.randint(1,100)
        if x not in listA:
            listA.append(x)
    listA.sort()
    return listA
#%%
def unique_team_name(num):
    listA = []
    while(len(listA) < num):
        x = ''.join(random.choice(string.ascii_uppercase) for _ in range(3))
        if x not in listA:
            listA.append(x)
    return listA
# %%
df_teams = pd.DataFrame()
# %%
num = 10
df_teams["Team_id"] = unique_numbers(num)
df_teams["Manager_id"] = unique_numbers(num)
df_teams['MinimalCapaCity'] = np.random.randint(5,num, len(df_teams))
df_teams['TeamName'] = unique_team_name(num)
# %%
df_teams.to_csv("databaseOfTeams.csv")
# %%
