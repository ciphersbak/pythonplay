print __doc__
import numpy as np
import pandas as pd
# import pandas.io.data as web
from pandas_datareader import data, wb
# import pandas_datareader as web
import timeit

# goog = data.DataReader('GOOG', data_source='google', start='3/14/2009', end='4/14/2014')
# goog.tail()
# goog.head()
loops = 25000000
from math import *
a =  range(1, loops)
def f(x):
    return 3 * log(x) + cos(x) ** 2

c = timeit.timeit = [f(x) for x in a]
# print c
import numexpr as ne
ne.set_num_threads(4)
f = '3 * log(a) + cos(a) ** 2'
r = timeit.timeit = ne.evaluate(f)
# print r