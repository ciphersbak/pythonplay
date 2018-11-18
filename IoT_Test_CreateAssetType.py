import requests
import json
from pprint import pprint
from requests.auth import HTTPBasicAuth

# response = requests.get('https://slc16lnq.us.oracle.com/assetMonitoring/clientapi/v2/groups', verify=False)
url = 'https://slc16lnq.us.oracle.com/assetMonitoring/clientapi/v2/assetTypes'
new_payload = {"attributes" : [ { "name" : "Dimension_1", "type" : "NUMBER", "defaultValue" : 120, 
                                  "required" : True, "sensorAttributes" : [], "static" : False, 
                                  "unique" : False } ],
               "name" : "PP_AssetType_1",
               "description" : "PP AssetType 1",
               "maintenanceActivities" : []
              }
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data=json.dumps(new_payload), headers=headers, auth=('iot', 'welcome1'), verify=False)
print (response.url)

if response.status_code != 201:	
    # raise ApiError('GET /tasks/ {}'.format(response.status_code))
    print "Status Code: " + str(response.status_code)
    # pass

responseJSON = json.loads(response.text)
pprint(responseJSON)