# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 18:58:52 2019

@author: YASH SAINI
"""

import numpy as np
import quandl
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from sklearn.preprocessing import MinMaxScaler
df=pd.read_csv("Credit_Card_Applications.csv")
X=df.iloc[:,:-1].values
Y=df.iloc[:,-1].values
sc=MinMaxScaler(feature_range=(0,1))
X=sc.fit_transform(X)

from minisom import MiniSom
som=MiniSom(x=10,y=10,input_len=15,sigma=1.0,learning_rate=0.5)
som.random_weights_init(X)
som.train_random(data=X,num_iteration=100)

#Visualizing
from pylab import bone,pcolor,colorbar,plot,show
bone()
pcolor(som.distance_map().T)
colorbar()
markers=['o','s']
colors=['r','g']
for i,x in enumerate(X):
    w=som.winner(x)
    plot(w[0]+0.5,w[1]+0.5,markers[Y[i]],markeredgecolor=colors[Y[i]],markerfacecolor=None,markersize=10,markeredgewidth=2)
show()    

#Detecting Frauds
mappings=som.win_map(X)
frauds=np.concatenate((mappings[(8,1)],mappings[(6,4)]),axis=0)
frauds=sc.inverse_transform(frauds)


