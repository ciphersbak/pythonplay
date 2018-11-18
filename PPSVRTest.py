# Support Vector Regression (SVR) using linear and non-linear kernels
print __doc__
import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm import SVR


# Generate sample data
xs = np.sort(5 * np.random.rand(40, 1), axis=0)
ys = np.sin(xs).ravel()

# Add noice to targets
ys[::5] += 3 * (0.5 - np.random.rand(8))

# Fit regression model
svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
svr_lin = SVR(kernel='linear', C=1e3)
svr_poly = SVR(kernel='poly', C=1e3, degree=2)
y_rbf = svr_rbf.fit(xs, ys).predict(xs)
y_lin = svr_lin.fit(xs, ys).predict(xs)
y_poly = svr_poly.fit(xs, ys).predict(xs)

# look at results
lw = 2
plt.scatter(xs, ys, color='darkorange', label='data')
plt.hold('on')
plt.plot(xs, y_rbf, color='navy', lw=lw, label='RBF Model')
plt.plot(xs, y_lin, color='c', lw=lw, label='Linear Model')
plt.plot(xs, y_poly, color='cornflowerblue', lw=lw, label='Polynomial Model')
plt.xlabel('Data')
plt.ylabel('Target')
plt.title('Support Vector Regression')
plt.legend()
plt.show()
