# Regression Example
# Supervised Machine Learning - Features and Labels
#Features are your attributes or in this case continous data
#Labels are prediction into the future
#How to train a classifier to predict
#Classifier - Train and Test
import pandas as pd
import quandl, math, datetime
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')
df = quandl.get('WIKI/GOOGL')
#print df.head()
#Create Data Frame
df = df[['Adj. Open','Adj. High','Adj. Low','Adj. Close','Adj. Volume']]
#Percent Volatility
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100.0
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0
#Define a new Data Frame
#Features
df = df[['Adj. Close','HL_PCT','PCT_change','Adj. Volume']]
#print df.head()
#Define your forecast column
forecast_col = 'Adj. Close'
#check for NaN
df.fillna(-99999, inplace=True)
#This is a Regression Algorithm
forecast_out = int(math.ceil(0.01*len(df)))
#Number of days in advance
print forecast_out
#Define Labels
df['label'] = df[forecast_col].shift(-forecast_out)
#print df.head()
df.dropna(inplace=True)
#Comparing Forecast Price to the Adjusted Close Price
#print df.tail()

#Features - X
#Labels - y
X = np.array(df.drop(['label'], 1))
X = preprocessing.scale(X)
X = X[:-forecast_out]
X_lately = X[-forecast_out:]
#X = X[:-forecast_out+1]
df.dropna(inplace=True)
y = np.array(df['label'])
y = np.array(df['label'])
#print len(X), len(y)

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,y,test_size=0.2)
#Now define a Classifier
#Run in parallel n_jobs, set to -1 to run as many jobs as possible by your processor
clf = LinearRegression(n_jobs=-1)
#Fit Features and Labels
clf.fit(X_train, y_train)
#Compute accuracy and confidence as 2 different values
accuracy = clf.score(X_test, y_test)
print accuracy
#Switch to Support Vector Machines
clf = svm.SVR(kernel='poly')
#Fit Features and Labels
clf.fit(X_train, y_train)
#Compute accuracy and confidence as 2 different values
#accuracy = clf.score(X_test, y_test)
#print accuracy

forecast_set = clf.predict(X_lately)
print forecast_set, accuracy, forecast_out
df['Forecast'] = np.NaN

last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
one_day = 86400
next_unix = last_unix + one_day

for i in forecast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix += one_day
    df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]

df['Adj. Close'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
