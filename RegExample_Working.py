import pandas as pd
import quandl, math, datetime
import time
import numpy as np
from sklearn import preprocessing, svm
# preprocessing helps in processing before calculation
# cross_validation help in suffling data specially for statics
#svm is support vector machine
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from matplotlib import style
import pickle

style.use('ggplot')

df = quandl.get('WIKI/GOOGL')
df = df[['Adj. Open','Adj. High','Adj. Low','Adj. Close','Adj. Volume',]]
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100
#           price        x          x            x
df = df[['Adj. Close','HL_PCT','PCT_change','Adj. Volume']]

forecast_col = 'Adj. Close'
df.fillna(-99999, inplace=True) #we do this so we should not lose any data
forecast_out = int(math.ceil(0.1*len(df)))  #ceil used for making whole number rather then decimal
print(forecast_out)
df['label'] = df[forecast_col].shift(-forecast_out) # -ve this shift up like spreadsheet from down to upper part

#Features = X
#Labels = y
X = np.array(df.drop(['label'],1))
# X = np.array(df.drop(['label', 'Adj. Close'],1)) #this is our feature & drop drops label
X = preprocessing.scale(X)
X_lately = X[-forecast_out:]
X = X[:-forecast_out]

df.dropna(inplace=True)
Y = np.array(df['label'])

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
clf = LinearRegression(n_jobs=-1) #n_jobs=-1 allows to run in parallel subject to your processors capacity
#y = mX +  b
#m = slope, b = y intercept
#clf = svm.SVR(kernel='poly') #How to use Support Vector Machines
clf.fit(X_train,Y_train) #retrain your algo once a month when you are using pickle
with open('linearregression.pickle', 'wb') as f:
    pickle.dump(clf, f)

pickle_in = open('linearregression.pickle', 'rb')
clf = pickle.load(pickle_in)

accuracy = clf.score(X_test,Y_test)
#print(accuracy)
forecast_set = clf.predict(X_lately)
print(forecast_set, accuracy, forecast_out)
df['Forecast'] = np.nan #this specifies that the entire column contains full of non endent number of data

last_date = df.iloc[-1].name
last_unix = time.mktime(last_date.timetuple())
#last_unix = last_date.timestamp()
one_day = 86400 #seconds in one day
next_unix = last_unix + one_day

for i in forecast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix += one_day
    df.loc[next_date]= [np.nan for _ in range(len(df.columns)-1)] + [i] #This line basically converts all the NaN in the future to values in the Forecast_set

df['Adj. Close'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

#What is Pickling
