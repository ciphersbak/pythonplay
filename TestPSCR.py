import requests
import json
from pprint import pprint
from requests.auth import HTTPBasicAuth

url = 'https://fuscdrmsmc255-fa-ext.us.oracle.com:443/fscmRestApi/resources/11.13.18.05/publicSectorAgencies/1'
new_payload = {           
              }
headers = {'Content-Type': 'application/json'}
# response = requests.get(url, data=json.dumps(new_payload), headers=headers, auth=('SYSTEM_ADMIN', 'Welcome1'), verify=False)
response = requests.get(url, headers=headers, auth=('SYSTEM_ADMIN', 'Welcome1'), verify=False)
print (response.url)

if response.status_code != 202:	
    # raise ApiError('GET /tasks/ {}'.format(response.status_code))
    print "Status Code: " + str(response.status_code)
    # pass

responseJSON = json.loads(response.text)
pprint(responseJSON)