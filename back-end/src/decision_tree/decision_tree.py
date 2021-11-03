#%%
import pandas as pd
from sklearn import tree
import pydotplus
import datetime
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import matplotlib.image as pltimg

df = pd.read_csv("back-end/src/data/database.csv")

print(df)
# %%
#adding status column
d = {'Accepted': 1, 'Rejected': 0}
df['Status'] = df['Status'].map(d)
df['Overlap'] = 0

print(df)

#%%
#converting date to numeric
for x in range(df.shape[0]):
    df['StartDate'][x] = datetime.datetime.strptime(df['StartDate'][x], '%d/%m/%Y')
    df['EndDate'][x] = datetime.datetime.strptime(df['EndDate'][x], '%d/%m/%Y')
    df['StartDate'][x] = int(df['StartDate'][x].strftime('%Y%m%d'))
    df['EndDate'][x] = int(df['EndDate'][x].strftime('%Y%m%d'))



print (df['StartDate'][0])

#%%
print(type(df['StartDate'][0]))

# %%
#finding overlaping dates
for idx_1 in range(df.shape[0]):
  for idx_2 in range(df.shape[0]):
    if idx_1 != idx_2:
        i1 = pd.Interval(df['StartDate'][idx_1], df['EndDate'][idx_1])
        i2 = pd.Interval(df['StartDate'][idx_2], df['EndDate'][idx_2])
        
        overlap = i1.overlaps(i2)

        if overlap == True:
            df["Status"][idx_1] = 0
            df["Overlap"][idx_1] = 1

# %%
print(df)

# %%
#inputs for decision tree
features = ['Overlap']

X = df[features]
y = df['Status']

print(X)
print(y)

# %%
#decision tree clasifier and graphing
import os
os.environ["PATH"] += os.pathsep + 'C:\Program Files\Graphviz/bin/'

dtree = DecisionTreeClassifier()
dtree = dtree.fit(X, y)
data = tree.export_graphviz(dtree, out_file=None, feature_names=features)
graph = pydotplus.graph_from_dot_data(data)
graph.write_png('mydecisiontree.png')

img=pltimg.imread('mydecisiontree.png')
imgplot = plt.imshow(img)
plt.show()

# %%
# prediction 0 = non overlaping, 1 = overlaping
print(dtree.predict([[0]]))


# %%
