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

''' Supervised'''
# features
customers=df.iloc[:,1:].values

#dependent variable
is_fraud=np.zeros(len(df))
for i in range(len(df)):
    if (df.iloc[i,0] in frauds):
        is_fraud[i]=1

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
customers = sc.fit_transform(customers)



import keras
from keras.models import Sequential
from keras.layers import Dense 
clf=Sequential()
''' units for no of nodes in hidden layer , avg(input nodes +output), 
     input_dim= no of input nodes
     activation= rectifier for hidden layer and sigmoid for output layer
'''
''' First input layer and hidden layer '''
clf.add(Dense(units=2,kernel_initializer='uniform',activation='relu',input_dim=15))
#output layer
clf.add(Dense(units=1,kernel_initializer='uniform',activation='sigmoid'))

#compiling ANN
clf.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])#adam for stochastic gradient descent

#Fit data
clf.fit(customers,is_fraud, batch_size=1,epochs=2)
#Predict data
y_pred = clf.predict(customers)
y_pred=np.concatenate((df.iloc[:,0:1],y_pred),axis=1)
y_pred=y_pred[y_pred[:,1].argsort()]
