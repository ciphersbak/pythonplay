'''
   Call PS Synch Service
'''
# from pprint import pprint
import requests
url="http://192.168.56.101:8000/PSIGW/HttpListeningConnector?&Operation=X_PP_IB_SVOP_X.v1&From=PSFT_EP"
#headers = {'content-type': 'application/soap+xml'}
headers = {'content-type': 'text/xml'}
body = """<?xml version="1.0"?>
          <Request>
           <CI_NAME>PP_CREATE_LEASE</CI_NAME>
           <LEASE_OBLG></LEASE_OBLG>
           <BUSINESS_UNIT>US001</BUSINESS_UNIT>
           <LS_NBR>0000000011</LS_NBR>
          </Request>"""

response = requests.post(url,data=body,headers=headers)
print response.content