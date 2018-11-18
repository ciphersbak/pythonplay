import requests
import json
from pprint import pprint
from requests.auth import HTTPBasicAuth

url = 'https://slc16lnq.us.oracle.com/assetMonitoring/clientapi/v2/assets/' + 'US001000000000253'
headers = {'Content-Type': 'application/json'}
response = requests.delete(url, headers=headers, auth=('iot', 'welcome1'), verify=False)
print (response.url)

if response.status_code != 204:
    # raise ApiError('GET /tasks/ {}'.format(response.status_code))
    print "Status Code: " + str(response.status_code)
    # pass
elif response.status_code == 404:
	print "Not Found: " + str(response.status_code)