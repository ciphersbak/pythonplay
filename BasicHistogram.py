#Basic Histogram Example
import matplotlib.pyplot as plt
import numpy as np

import plotly.plotly as py
# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api

gaussian_numbers = np.random.randn(1000)
plt.hist(gaussian_numbers)
plt.title("Gaussian Histogram")
plt.xlabel("SQLID")
plt.ylabel("Rows Affcted")

fig = plt.gcf()

plot_url = py.plot_mpl(fig, filename='mpl-basic-histogram')
