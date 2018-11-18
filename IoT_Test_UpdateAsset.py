import requests
import json
from pprint import pprint
from requests.auth import HTTPBasicAuth

# response = requests.get('https://slc16lnq.us.oracle.com/assetMonitoring/clientapi/v2/groups', verify=False)
url = 'https://slc16lnq.us.oracle.com/assetMonitoring/clientapi/v2/assets/US001000000000229'
new_payload = {
               "name" : "US001000000000229",
               "type" : "HARDWARE", # Asset Type should be predefined
               "description" : "PP Asset 1",
               "tags" : [ "TAGMC1" ],
               "storagePlaces" : [ "Hyderabad 1" ], # Location should be predefined
               "groupNames" : [ "DUMMY_GROUP_1" ] # Asset Group should be predefined
              }
headers = {'Content-Type': 'application/json', 'X-HTTP-Method-Override':'PATCH'}
response = requests.post(url, data=json.dumps(new_payload), headers=headers, auth=('iot', 'welcome1'), verify=False)
print (response.url)

if response.status_code != 200:	
    # raise ApiError('GET /tasks/ {}'.format(response.status_code))
    print "Status Code: " + str(response.status_code)
    # pass

responseJSON = json.loads(response.text)
pprint(responseJSON)