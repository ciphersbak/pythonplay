#Build Linear Regression Example
#Plot y = mX + b
from statistics import mean
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')
#xs = [1,2,3,4,5,6]
#ys = [5,4,6,5,6,7]
xs = np.array([1,2,3,4,5,6], dtype=np.float64)
#ys = np.array([5,4,6,5,6,7], dtype=np.float64)
ys = np.array([3,4,5,4,7,8], dtype=np.float64)
#Order of Operation PEMDAS
#Paranthesis, Exponents, Multiplication, Division, Addition, Subtraction
def best_fit_slope_and_intercept(xs,ys):
    #calculate slope m
    m = ( ((mean(xs) * mean(ys)) - mean(xs*ys)) / ((mean(xs)*mean(xs)) - mean(xs*xs)))
    #calculate y intercept
    b = mean(ys) - m*mean(xs)
    return m, b

m,b = best_fit_slope_and_intercept(xs,ys)
print m,b
#Create a line that best fits the data
regression_line = [(m*x)+b for x in xs]
#OR
#for x in xs:
#    regression_line.append((m*x)+b)
#make prediction
predict_x = 8
predict_y = (m*predict_x)+b
#Dots
plt.scatter(xs, ys)
plt.scatter(predict_x, predict_y, color='g')
#Line
#plt.plot(xs, ys)
plt.plot(xs, regression_line)
#Display the graph
plt.show()
