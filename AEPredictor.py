"""This is import"""
import csv
import numpy as np
from sklearn.svm import SVR
from sklearn import tree
import matplotlib.pyplot as plt

Input = [[1, 50000], [1, 100000], [1, 150000], [1, 200000], [1, 250000], [1, 300000]]
Duration = [[55], [85], [97], [112], [137], [156]]

clf = tree.DecisionTreeClassifier()
clf = clf.fit(Input, Duration)

print clf.predict([1, 275001])
# def get_data(filename):
#     """This function gets the file"""
#     with open(filename, 'r') as csvfile:
#         csvFileReader = csv.reader(csvfile)
#         next (csvFileReader)
#         for row in csvFileReader:
#             Input.append([row[0], row[1]])
#             Duration.append([row[2]])
#     return
