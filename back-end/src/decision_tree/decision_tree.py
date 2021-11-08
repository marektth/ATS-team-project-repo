import datetime
import os
from os.path import exists

import matplotlib.image as pltimg
import matplotlib.pyplot as plt
import pandas as pd
import pydotplus
import pytest
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier


#adding status column
def status_column_add(df):
  d = {'Accepted': 1, 'Rejected': 0}
  df['Status'] = df['Status'].map(d)
  df['Overlap'] = 0
  return df


#converting date to numeric
def converter(df):
  for x in range(df.shape[0]):
      df['StartDate'][x] = datetime.datetime.strptime(df['StartDate'][x], '%d/%m/%Y')
      df['EndDate'][x] = datetime.datetime.strptime(df['EndDate'][x], '%d/%m/%Y')
      df['StartDate'][x] = int(df['StartDate'][x].strftime('%Y%m%d'))
      df['EndDate'][x] = int(df['EndDate'][x].strftime('%Y%m%d'))
  
  df["StartDate"] = df["StartDate"].astype('int64')
  df["EndDate"] = df["EndDate"].astype('int64')

  return df


#finding overlaping dates
def overlap_dates_finder(df):
  for idx_1 in range(df.shape[0]):
    for idx_2 in range(df.shape[0]):
      if idx_1 != idx_2:
          i1 = pd.Interval(df['StartDate'][idx_1], df['EndDate'][idx_1])
          i2 = pd.Interval(df['StartDate'][idx_2], df['EndDate'][idx_2])
          
          overlap = i1.overlaps(i2)

          if overlap == True:
              df["Status"][idx_1] = 0
              df["Overlap"][idx_1] = 1

  #df.to_csv('klpklkl.csv')

  return df


#inputs for decision tree
def decision_tree(df):
  features = ['Overlap']

  X = df[features]
  y = df['Status']
  

  if(X.empty or y.empty):
    return 0
  else:
    os.environ["PATH"] += os.pathsep + 'C:\Program Files\Graphviz/bin/'

    dtree = DecisionTreeClassifier()
    dtree = dtree.fit(X, y)
    data = tree.export_graphviz(dtree, out_file=None, feature_names=features)
    graph = pydotplus.graph_from_dot_data(data)
    graph.write_png('mydecisiontree.png')

    img=pltimg.imread('mydecisiontree.png')
    imgplot = plt.imshow(img)
    plt.show()
    return 1


# prediction 0 = non overlaping, 1 = overlaping

#print(dtree.predict([[0]]))


def main():
  df = pd.read_csv("back-end\src\data\database.csv")
  df = status_column_add(df)
  df = converter(df)
  df = overlap_dates_finder(df)
  decision_tree(df)


if __name__ == "__main__":
  main()
