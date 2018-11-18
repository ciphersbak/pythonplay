import requests
import json
from pprint import pprint
from requests.auth import HTTPBasicAuth

# response = requests.get('https://slc16lnq.us.oracle.com/assetMonitoring/clientapi/v2/groups', verify=False)
url = 'https://slc16lnq.us.oracle.com/assetMonitoring/clientapi/v2/assets'
new_payload = {
               "name" : "001 Runway Sweeping Machine",
               "type" : "RunwaySweepingAssetType", # Asset Type should be predefined
               "description" : "001 Runway Sweeping Machine",
               "geoLocation" : "13.196859665896742, 77.70419643159327",
               "tags" : [ "TAGMC1" ],
               "assignedPlaceName" : "ACMEInternationalAirport",
            #    "assignedPlace" : {
            #                       "name" : "ACMEInternationalAirport",
            #                       "type" : "place",
            #                       "description" : "ACME International Airport",
            #                       "geoFences" : [ "2E656F09-046E-409D-A561-D80302A05882" ],
            #                       "places" : [  ],
            #                       "tags" : [  ]
            #                      },
               "attributes" : [ { "name" : "RunwaySweepingAssetTypeDM", 
                                  "value" : "11DD08B2-7367-4E22-BE00-05F915660A23" } ], # This is unique, create in DS
               "storagePlaces" : [  ], # Location should be predefined
               "groupNames" : [  ] # Asset Group should be predefined
              }
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data=json.dumps(new_payload), headers=headers, auth=('iot', 'welcome1'), verify=False)
print (response.url)

if response.status_code != 202:	
    # raise ApiError('GET /tasks/ {}'.format(response.status_code))
    print "Status Code: " + str(response.status_code)
    # pass

responseJSON = json.loads(response.text)
pprint(responseJSON)