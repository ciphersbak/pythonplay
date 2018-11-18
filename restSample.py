import requests
import json

response = requests.get('http://services.groupkt.com/country/get/all')
if response.status_code != 200:
	# This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))

responseJSON = json.loads(response.text)

for result in responseJSON['RestResponse']['result']:
	print "name: " + result['name'] + ", code1: " + result['alpha2_code'] + ", code2: " + result['alpha3_code']