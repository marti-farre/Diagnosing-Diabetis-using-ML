# -*- coding: utf-8 -*-
"""preprocessing_diabetes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19wGP5QK3tntnPvjXXPPeUfT2gBjcrxRB

Martí, Miquel and Pere, June 2022

This are the instructions we have used to preprocess our data.
"""

import sys
!{sys.executable} -m pip install pandas
!{sys.executable} -m pip install numpy
!{sys.executable} -m pip install matplotlip
!{sys.executable} -m pip install math
!{sys.executable} -m pip install scipy
!{sys.executable} -m pip install scikit-learn
!{sys.executable} -m pip install easyinput
!{sys.executable} -m pip install seaborn

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.io import arff
from scipy import stats
from sklearn.impute import KNNImputer
from easyinput import read
import seaborn as sns


import seaborn as sns


from scipy.io import arff
from numpy import isnan
from pandas import read_csv

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.impute import KNNImputer
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import GridSearchCV

"""Data preprocessing.

The program will ask for Y/N no execute certain chunks of code.
"""

def ask(title):
    print(title + "? [y/n]", end = " ")
    #qt = read(str)
    qt="y"
    if (qt == "y"):
        print("\n")
        return True
    else:
        return False

#### INTRODUCTION TO THE DATA SET ####


db_data = pd.read_csv('diabetes.csv', sep=',')
if (ask("FIVE FIRST INSTANCES OF OUR DATA SET")):
    print(db_data.head())
    print("\n")
if (ask("TYPE OF DATA")):
    print(db_data.info())
    print("\n")

## MODIFICATIONS ##

db_mod = db_data

# CHANGE FACTORS FOR NUMBERS

for i in range(0, 768):
    if (db_mod.loc[i, 'class'] == 'tested_positive'):
        db_mod.loc[i, 'class'] = 1
    elif (db_mod.loc[i, 'class'] == 'tested_negative'):
        db_mod.loc[i, 'class'] = 0

db_mod = db_mod.drop('id', axis=1)

# INSPECTION OF THE DATA SET #

if (ask("INSPECTION OF THE DATA SET")):
    print(db_mod.describe())
    print("\n")

# MISSING VALUES #

# COUNTING AND INTERPRETING ZEROS #

db_mod[['plas', 'pres', 'skin', 'insu', 'mass']] = db_mod[[
    'plas', 'pres', 'skin', 'insu', 'mass']].replace(0, np.NaN)

if (ask("NUMBER OF NAN VALUES FOR EACH VARIABLE")):
    print(db_mod.isnull().sum())
    print("\n")

# REPLACING BY NEAREST NEIGHBOURS #

imputer = KNNImputer()
imputed = imputer.fit_transform(db_mod)
db_mod = pd.DataFrame(imputed, columns=db_mod.columns)
if (ask("NUMBER OF NAN VALUES FOR EACH VARIABLE AFTER KNN")):
    print(db_mod.isnull().sum())
    print("\n")

# INSPECTION OF THE  NEW DATA SET

if (ask("INSPECTION OF THE MODIFIED DATA SET")):
    print(db_mod.describe())
    print("\n")

# CHECK THAT THE DATA SET IS BALANCED

number, freq = np.unique(db_mod.values[:, 8], return_counts=True)
if (ask("CHECK IF THE DATA SET IS BALANCED")):
    print(number[0], ":", freq[0]/np.sum(freq), "%")
    print(number[1], ":", freq[1]/np.sum(freq), "%")
    print("\n")

# DERIVATION OF NEW VARIABLES #


# GAUSSANITY AND TRANSFORMATIONS #

if (ask("HISTOGRAM OF EACH VARIABLE")):
    db_mod.hist(bins=60, figsize=(20, 20))
    plt.show()

# TRASNFORMATIONS

db_mod['log_insu'] = db_mod['insu']
db_mod['log_insu'] = np.log(db_mod['insu'])

mod_names = ['log_insu']

if (ask("HISTOGRAM OF MODIFIED VARIABLES")):
    db_mod[mod_names].hist(bins=60, figsize=(20, 20))
    plt.show()

# PAIR-WISE COMPARISIONS OF VARIABLES #

if (ask("PAIR-WISE COMPARISIONS OF VARIABLES")):
    pd.plotting.scatter_matrix(db_mod)
    plt.show()

if (ask("CORRELATION BETWEEN VARIABLES")):
    corr = db_mod.corr()
    print(corr)
    sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns)
    plt.show()

# NORMALIZING THE DATA FRAME #
if (ask("NORMALIZATION OF VARIABLES")):
    db_mod = db_mod.apply(lambda iterator: ((iterator.max()-iterator) /
                                            (iterator.max()-iterator.min())).round(2))
    print(db_mod.describe())


db_mod.to_csv(r'diabetes_mod.csv', index = False, header=True)