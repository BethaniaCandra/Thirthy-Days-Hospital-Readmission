import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision_score
from sklearn.model_selection import train_test_split, cross_val_score, RepeatedStratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import GaussianNB

#EDA diagnosis
def diabetic_diagnosis(data, cols):
    for col in cols:
        data.loc[(data[col].str.contains("V"))|(data[col].str.contains("E")),col]=-1
        data[col]=data[col].astype(np.float16)
    for col in cols:
        data["temp_diag"]=np.nan
        data.loc[(data[col]>=390)&(data[col]<=459)|(data[col]==785),"temp_diag"]= "Circulatory"
        data.loc[(data[col]>=460)&(data[col]<=519)|(data[col]==786),"temp_diag"]= "Respiratory"
        data.loc[(data[col]>=520)&(data[col]<=579)|(data[col]==787),"temp_diag"]= "Disgestive"
        data.loc[(data[col]>=250)&(data[col]<251),"temp_diag"]= "Diabetes"
        data.loc[(data[col]>=800)&(data[col]<=999),"temp_diag"]= "Injury"
        data.loc[(data[col]>=710)&(data[col]<=739),"temp_diag"]= "Musculoskeletal"
        data.loc[(data[col]>=580)&(data[col]<=629)|(data[col]==788),"temp_diag"]= "Genitourinary"
        data.loc[(data[col]>=140)&(data[col]<=239),"temp_diag"]= "Neoplasms"
        data["temp_diag"]=data["temp_diag"].fillna("Other")
        data[col]=data["temp_diag"]
        data=data.drop("temp_diag",axis=1)
    return data

#feature selection using Mutual Infromation
def select_features_mi(X_train,y_train,X_test,k):
    #configure to select all features
    fs_mi = SelectKBest(score_func=mutual_info_classif,k=k)
    #learn relationship from training data
    fs_mi.fit(X_train,y_train)
    #transform train input data
    X_train_mi = fs_mi.transform(X_train)
    #transform test input data
    X_test_mi =fs_mi.transform(X_test)
    return X_train_mi,X_test_mi, fs_mi
