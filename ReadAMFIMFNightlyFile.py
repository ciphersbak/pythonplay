import requests
import pandas as pd
from pandas import parser

try:
	# data = pd.read_csv('https://www.amfiindia.com/spages/NAVAll.txt?t=09012018100518', encoding='cp1251', sep=';', skiprows=None, nrows=5)
	data = pd.read_csv('https://www.amfiindia.com/spages/NAVAll.txt?t=09012018100518', sep=";", nrows=5)
	data.head()
	data.tail()
	# headers = ["Scheme Code", "ISIN Div Payout/ISIN Growth", "ISIN Div Reinvestment", "Scheme Name", "Net Asset Value", "Repurchase Price", "Sale Price", "Date"]
	# data_no_headers = pd.read_csv('https://www.amfiindia.com/spages/NAVAll.txt?t=09012018100518', names = headers)
	# data_no_headers.head()

except (parser.CParserError) as detail:
	print detail

# response = requests.get('https://www.amfiindia.com/spages/NAVAll.txt?t=09012018100518')
# print "file contents " + response.text