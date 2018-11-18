#Build Linear Regression Example
#Plot y = mX + b
from statistics import mean
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')
xs = np.array([10000,25000,47000,54000,65000,100000], dtype=np.float64) #Number of rows affected by the same  SQLID
ys = np.array([8.75,22.57,43.68,56.89,63.21,89.93], dtype=np.float64) #Duration in seconds
#Order of Operation PEMDAS
#Paranthesis, Exponents, Multiplication, Division, Addition, Subtraction
def best_fit_slope_and_intercept(xs,ys):
    #calculate slope m
    m = ( ((mean(xs) * mean(ys)) - mean(xs*ys)) / ((mean(xs)*mean(xs)) - mean(xs*xs)))
    #calculate y intercept
    b = mean(ys) - m*mean(xs)
    return m, b

m,b = best_fit_slope_and_intercept(xs,ys)
# print m,b
#Create a line that best fits the data
regression_line = [(m*x)+b for x in xs]
#OR
#for x in xs:
#    regression_line.append((m*x)+b)
#make prediction
predict_x = 80000
predict_y = (m*predict_x)+b
#Dots
# plt.scatter(xs, ys)
# plt.scatter(predict_x, predict_y, color='g')
print 'For {} rows system will take around {} second(s) for this SQLID'.format(predict_x, predict_y)
#Line
#plt.plot(xs, ys)
# plt.plot(xs, regression_line)
#Display the graph
plt.show()
