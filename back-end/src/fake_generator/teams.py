#%%
import numpy as np
import pandas as pd
import random
import string
#%%
def unique_numbers(num):
    list_a = []
    while(len(list_a) < num):
        x = random.randint(1,100)
        if x not in list_a:
            list_a.append(x)
    list_a.sort()
    return list_a
#%%
def unique_team_name(num):
    list_a = []
    while(len(list_a) < num):
        x = ''.join(random.choice(string.ascii_uppercase) for _ in range(3))
        if x not in list_a:
            list_a.append(x)
    return list_a
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

