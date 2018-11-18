import pandas as pd
import math, datetime
import time
import numpy as np
from sklearn import preprocessing, svm
from statistics import mean
# preprocessing helps in processing before calculation
# cross_validation helps in shuffling data specially for statics
# svm is support vector machine
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from matplotlib import style
import pickle, random

style.use('fivethirtyeight')


def create_dataset(howmany, variance, stepup=2, correlation=False):
    val = 1
    ys = []
    for i in range(howmany):
        y = val + random.randrange(-variance, variance)
        ys.append(y)
        if correlation and correlation == 'pos':
            val+=stepup
        elif correlation and correlation == 'neg':
            val-=stepup
    xs = [i for i in range(len(ys))]

    return np.array(xs, dtype=np.float64), np.array(ys, dtype=np.float64)

# Order of Operation PEMDAS
# Paranthesis, Exponents, Multiplication, Division, Addition, Subtraction
def best_fit_slope_and_intercept(xs,ys):
    # calculate slope m
    m = (((mean(xs) * mean(ys)) - mean(xs*ys)) / ((mean(xs)*mean(xs)) - mean(xs*xs)))
    # calculate y intercept
    b = mean(ys) - m*mean(xs)
    return m, b


# calculate coefficient of determination
# How good is the fit
def squared_error(ys_orig, ys_line):
    return sum((ys_line-ys_orig)**2)


def coefficient_of_determination(ys_orig, ys_line):
    y_mean_line = [mean(ys_orig) for y in ys_orig]
    squared_error_regr = squared_error(ys_orig, ys_line)
    squared_error_y_mean = squared_error(ys_orig, y_mean_line)
    return 1 - (squared_error_regr / squared_error_y_mean)


# Create random data set
# xs, ys = create_dataset(40, 80, 2, correlation=False)
xs, ys = create_dataset(40, 10, 2, correlation='pos')

m, b = best_fit_slope_and_intercept(xs, ys)
# Create a line that best fits the data
regression_line = [(m*x)+b for x in xs]
# make prediction
predict_x = 8
predict_y = (m*predict_x)+b
# Test r_squared
r_squared = coefficient_of_determination(ys, regression_line)
print r_squared
plt.scatter(xs, ys)
plt.scatter(predict_x, predict_y, s=100, color='r')
# Line
plt.plot(xs, regression_line, label='Linear Regression')
plt.xlabel('Xs')
plt.ylabel('Ys')
plt.legend()
# Display the graph
plt.show()
