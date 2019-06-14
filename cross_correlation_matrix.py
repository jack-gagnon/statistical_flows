#!/usr/bin/env

# Importing the necessary modules
import pandas as pd
import sklearn as skl
import numpy as np
import pprint as pp
import os, sys, shutil, pathlib
import time
import sqlite3
from datetime import datetime, timedelta
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
import pathlib
from pathlib import Path
import math

# ----------------------------------------------------------------------------
# Sets the working directory -- or, workspace
# ----------------------------------------------------------------------------

def workspace():
    print("The current working directory is: ", os.getcwd())
    # Enter the path without quotations or // separation
    path = input("Please enter the path to the working directory: ")
    os.chdir(path)
    print("The current working directory is: ", os.getcwd())
    return (path)

workspace()

def workspace_tree():
             

            working_direct = Path(os.getcwd())
            all_files = []
            
            for i in working_direct.rglob('*.*'):
                all_files.append((i.name, i.parent, time.ctime(i.stat().st_ctime)))

            columns = ["File_Name", "Parent", "Created"]
            rootDirectory_df = pd.DataFrame.from_records(all_files, columns=columns)

            paths = []
            for paths, directories, files in os.walk(working_direct):
                paths.append(os.path.join(path, directory))
                
            return (rootDirectory_df, paths)

# ----------------------------------------------------------------------------
# Load the necessary data
# ----------------------------------------------------------------------------
 
raw_data = pd.read_csv("C:\\Users\\path\\to\\file.csv", encoding = 'cp1252')
data = pd.read_csv("C:\\Users\\path\\to\\file.csv", encoding = 'cp1252')

con = sqlite3.connect("C:\\Users\\e650609\\Desktop\\useful-py-cmds\\raw_data_workflow\\SHO_KPI_details_archive.sqlite")
sql_data = pd.read_sql_query("SELECT * FROM Data;", con)

con.close()

data_sources = [raw_data, data]


# -------------------------------------------------------------------------------
# Defining a data cleaning function - and iterating through the data_source list
# -------------------------------------------------------------------------------


def df_pipe(df):
    # Exploring the data briefly
    import pprint as pp
    head = df.head()
    shape = df.shape
    nulls = df.isnull().sum()
    varias = df.columns.values
    df_length = len(df)
                      
    nulls = nulls.to_dict()
    to_drop = []
    # If a column is made up of >50% null values - it gets dropped
    for k, v in nulls.items():
        if (v / df_length) > 0.25:
            to_drop.append(k)
    df = df.drop(to_drop, axis=1)
    return (df.head(5))

for df in data_sources:
    df_pipe(df);


# -------------------------------------------------------------------------------
# Reducing teh dimensionality of the working data frames
# -------------------------------------------------------------------------------
raw_data_sub = pd.DataFrame(data=raw_data[['ColNames...']].groupby(by=['ColNames...'], as_index=True).mean())

data_sub = data[data['ColName'].notnull()]

working_data_sources = [raw_data_sub, data_sub]

# -------------------------------------------------------------------------------
# Creating unique identifiers to merge into a working correlation dataframe --
# *Example syntax*
# -------------------------------------------------------------------------------
data_sub['date_client_identifier'] = data_sub['Date'] + data_sub['Client']


# -------------------------------------------------------------------------------
# Merging into a single dataframe
# -------------------------------------------------------------------------------

data_merged = data_sub.merge(raw_data_sub, how='inner', on=['date_client_identifier'])


#data.drop(['ColName'], inplace=True)

# -------------------------------------------------------------------------------
# Correlation matrix
# -------------------------------------------------------------------------------

corr = data.corr()

mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

f, ax = plt.subplots(figsize=(11, 9))

cmap = sns.diverging_palette(220, 10, as_cmap=True)

sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

plt.show()





















