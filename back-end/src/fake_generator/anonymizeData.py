#%%
import pandas as pd

#%%
def anonymize(df):
    df.drop(['Unnamed: 0','PersonNumber'], axis=1, inplace=True)
    return df


# %%
df = pd.read_csv("database.csv")
df_per_day = pd.read_csv("databasePerDay.csv")
# %%
df = anonymize(df)
df_per_day = anonymize(df_per_day)
# %%
