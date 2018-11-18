'''
	Program to show how python calls a REST url	
'''

import requests
import json
import os

def clearScreen():
	if os.name != "windows":
		os.system('clear')
	else:
		os.system('cls')

def getURLResponse(str_URL, isAll):
	response = requests.get(str_URL)
	if response.status_code != 200:
		# This means something went wrong.
	    raise ApiError('GET /tasks/ {}'.format(resp.status_code))

	responseJSON = json.loads(response.text)
	#print "Json response: " + response.text
	printResponse(responseJSON, isAll)

def printResponse(strJSONReponse, isAll):
	if isAll:
		for result in strJSONReponse['RestResponse']['result']:
			print "name: " + result['name'] + ", code1: " + result['alpha2_code'] + ", code2: " + result['alpha3_code']
	else:
		print "name: %s, code1: %s, code2: %s" % (strJSONReponse['RestResponse']['result'].get("name"),
												strJSONReponse['RestResponse']['result'].get("alpha2_code"), 
												strJSONReponse['RestResponse']['result'].get("alpha3_code"))

str_base_URL = "http://services.groupkt.com/country/"

str_show_all_options = '''1. REST web-service to get a list of all Countries
2. REST web-service to search country by 2 character alphanumeric ISO code
3. REST web-service to search country by 3 character alphanumeric ISO code
4. REST web-service to search country by 3 character ISO code or 2 character ISO code or country name

5. Exit'''

clearScreen()

var_input_user_option = raw_input(str_show_all_options + "\n Please enter your option: ")
str_URL = ""

while True:
	if var_input_user_option == "1":
		str_URL = str_base_URL + "get/all"
		getURLResponse(str_URL, True)
		var_input_user_option = raw_input("Press any key to continue...")
		#break
	elif var_input_user_option == "2":
		var_input_user_option = raw_input("Enter 2 character country code: ")
		str_URL = str_base_URL + "get/iso2code/" + var_input_user_option
		getURLResponse(str_URL, False)
		var_input_user_option = raw_input("Press any key to continue...")
		#break
	elif var_input_user_option == "3":
		str_URL = str_base_URL + "all"
		var_input_user_option = raw_input("Enter 3 character country code: ")
		str_URL = str_base_URL + "get/iso3code/" + var_input_user_option
		getURLResponse(str_URL, False)
		var_input_user_option = raw_input("Press any key to continue...")
		#break
	elif var_input_user_option == "4":
		str_URL = str_base_URL + "all"
		var_input_user_option = raw_input("Enter 2 or 3 character country code: ")
		str_URL = str_base_URL + "search/?text=" + var_input_user_option
		getURLResponse(str_URL, True)
		var_input_user_option = raw_input("Press any key to continue...")
		#break
	elif var_input_user_option == "5":
		break;
	else:
		#clearScreen()
		var_input_user_option = raw_input(str_show_all_options + "\n Invalid option, please re-enter: ")


exit(0)