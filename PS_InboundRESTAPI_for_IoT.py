import requests
import json
from pprint import pprint
from requests.auth import HTTPBasicAuth

url = 'http://slc10ubp.us.oracle.com:8000/PSIGW/RESTListeningConnector/PSFT_EP/PPIOT_RUNWAYSWEEPMC.v1/update/'
new_payload = [{
	"id": "2a98b873-1f67-44fa-82f6-48ef53921a03",
	"clientId": "2e7ea8d8-5ad5-4c61-99f3-18b49040e54e",
	"source": "4B91B70C-B03A-471D-B3D7-C7F0E70AF713",
	"destination": "",
	"priority": "MEDIUM",
	"reliability": "BEST_EFFORT",
	"eventTime": 1533016759396,
	"sender": "",
	"type": "DATA",
	"properties": {},
	"direction": "FROM_DEVICE",
	"receivedTime": 1533016759451,
	"sentTime": 1533016759549,
	"payload": {
		"format": "urn:oracle:runway:sweeper:machine:data:attributes",
		"data": {
			"$(souce)_description": "Created by Simulator",
			"$(source)_id": "4B91B70C-B03A-471D-B3D7-C7F0E70AF713",
			"engineVibration": 3.335778530713718,
			"engineTemp": 7.361155052963864,
			"fuelLevel": 42.70555840989347,
			"messageCount": 100.0,
			"hydraulicPressure": 195.34225122706474,
			"anomalousMessages": 0.0,
			"ora_longitude": 77.7091400493462,
			"engineOilPressure": 3572.4681506168617,
			"goodMessages": 0.0,
			"ora_latitude": 13.204383727651413,
			"speed": 17.711691110249983
		}
	}
}]
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data=json.dumps(new_payload), headers=headers)
print (response.url)
print "Status Code: " + str(response.status_code)

if response.status_code != 200:
    # raise ApiError('GET /tasks/ {}'.format(response.status_code))
    print "Status Code: " + str(response.status_code)
    # pass

# responseJSON = json.loads(response.text)
# pprint(responseJSON)