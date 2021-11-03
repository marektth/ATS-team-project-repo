#%%
from faker import Faker
import faker
import pandas as pd
import random
import datetime
import numpy as np
# %%
fake = Faker()
teams = ("team1","team2")
def create_rows(num=1):
    output = [{
                "PersonNumber":random.randint(1,10),
                "EmploymentNumber":random.randint(1,10),
                "team":random.choice(teams)
                } for _ in range(num)]
    return output

df = pd.DataFrame(create_rows(10))

# %%
df = df.drop_duplicates(subset=['PersonNumber'], keep='first')
# %%
print(df)
# %%
df.to_csv("databaseOfPeople.csv")
# %%
