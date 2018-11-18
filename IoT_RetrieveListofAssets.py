import requests
import json
from pprint import pprint
from requests.auth import HTTPBasicAuth

url = 'https://slc16lnq.us.oracle.com/assetMonitoring/clientapi/v2/assets/Machine_1'
headers = {'Content-Type': 'application/json'}
response = requests.get(url, headers=headers, auth=('iot', 'welcome1'), verify=False)

if response.status_code != 200:
	# This means something went wrong.
    # raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    print "Status Code: " + str(response.status_code)
    # pass

responseJSON = json.loads(response.text)
pprint("Response: " + str(responseJSON))
# for result in responseJSON['links']:
	# print "ID: " + result['id'] + ", Name: " + result['name'] + ", Type: " + result['type']
