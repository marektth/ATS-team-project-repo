#%%
import pandas as pd

#%%
def anonymize(df):
    df.drop(['Unnamed: 0','PersonNumber'], axis=1, inplace=True)
    return df


# %%
df = pd.read_csv("database.csv")
dfPerDay = pd.read_csv("databasePerDay.csv")
# %%
df
#%%
dfPerDay
# %%
df = anonymize(df)
dfPerDay = anonymize(dfPerDay)
# %%
df

#%%
dfPerDay

# %%
