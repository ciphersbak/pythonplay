from statistics import mean
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style


style.use('fivethirtyeight')
xs = np.array([73125, 122567, 542131, 999999, 888888, 765432, 654321, 555555, 444444, 987654], dtype=np.float64)  # Number of rows affected by the same  SQLID
ys = np.array([19.55, 34.15, 137.29, 238.8, 213.2, 183.31, 169.18, 133.42, 105.87, 249.37], dtype=np.float64)  # Duration in seconds
# Order of Operation PEMDAS
# Paranthesis, Exponents, Multiplication, Division, Addition, Subtraction


def best_fit_slope_and_intercept(xs, ys):
    # calculate slope m
    m = (((mean(xs) * mean(ys)) - mean(xs*ys)) / ((mean(xs)*mean(xs)) - mean(xs*xs)))
    # calculate y intercept
    b = mean(ys) - m*mean(xs)
    return m, b

# Calculate coefficient of determination
# How good is the fit


def squared_error(ys_orig, ys_line):
    return sum((ys_line-ys_orig)**2)


def coefficient_of_determination(ys_orig, ys_line):
    y_mean_line = [mean(ys_orig) for y in ys_orig]
    squared_error_regr = squared_error(ys_orig, ys_line)
    squared_error_y_mean = squared_error(ys_orig, y_mean_line)
    return 1 - (squared_error_regr / squared_error_y_mean)


m, b = best_fit_slope_and_intercept(xs, ys)
# print m,b
# Create a line that best fits the data
regression_line = [(m*x)+b for x in xs]
# make prediction
predict_x = 876543
predict_y = (m*predict_x)+b

plt.scatter(xs, ys)
plt.scatter(predict_x, predict_y, s=100, color='r')
# print 'For {} rows system will take around {} second(s) for this SQLID'.format(predict_x, predict_y)
print 'Approx {} second(s) for {} rows'.format(predict_y, predict_x)

predict_x = 1000001
predict_y = (m*predict_x)+b
plt.scatter(predict_x, predict_y, s=100, color='r')
# print 'For {} rows system will take around {} second(s) for this SQLID'.format(predict_x, predict_y)
print 'Approx {} second(s) for {} rows'.format(predict_y, predict_x)
# Test r_squared
r_squared = coefficient_of_determination(ys, regression_line)
print r_squared
# Line
plt.plot(xs, regression_line, label='Rows Affected vs Duration')
plt.xlabel('Rows Affected')
plt.ylabel('Duration')
plt.legend()
# Display the graph
plt.show()
