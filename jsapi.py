# This program will prompt for a location, contact a web service and retrieve JSON
# Retrieve first place_id from JSON
import urllib.request, urllib.parse, urllib.error
import json

api_key = False
# If you have a Google Places API key, enter it here
api_key = 'Enter Your API Key If You Have One'
# https://developers.google.com/maps/documentation/geocoding/intro

if api_key is False:
	api_key = 42
	serviceurl = 'http://py4e-data.dr-chuck.net/json?'
else:
	serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

while True:
	address = input('Enter location:')
	if len(address)<1: break
	
	parms = dict()
	parms['key'] = api_key
	parms['address'] = address
	url = serviceurl + urllib.parse.urlencode(parms)
	
	print('Retrieving', url)
	uh = urllib.request.urlopen(url)
	data = uh.read().decode()
	print('Retrieved', len(data), 'characters')
	
	try:
		js = json.loads(data)
	except:
		js = None
		
	if js is None or 'status' not in js or js['status']!='OK':
		print('==== Failure To Retrieve ====')
		print(json.dumps(js, indent=4))
		continue
	print(json.dumps(js, indent=4))
	place_id = js['results'][0]['place_id']
	print(place_id)
