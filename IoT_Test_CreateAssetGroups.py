import requests
import json
from pprint import pprint
from requests.auth import HTTPBasicAuth

# response = requests.get('https://slc16lnq.us.oracle.com/assetMonitoring/clientapi/v2/groups', verify=False)
url = 'https://slc16lnq.us.oracle.com/assetMonitoring/clientapi/v2/groups'
new_payload = {"assetNames" : ["Machine_1"],                
               "name" : "PP_Group_5", 
               "description" : "PP Asset Group 5",
               "type" : "STATIC" }
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data=json.dumps(new_payload), headers=headers, auth=('iot', 'welcome1'), verify=False)
print (response.url)

if response.status_code != 201:	
    # raise ApiError('GET /tasks/ {}'.format(response.status_code))
    print "Status Code: " + str(response.status_code)
    # pass

responseJSON = json.loads(response.text)
pprint(responseJSON)
# print "Response: " + str(responseJSON)

# for result in responseJSON['assets']:
    # print "ID: " + result['id']
