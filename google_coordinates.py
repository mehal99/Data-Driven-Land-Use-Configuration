# This program read from a list of locations
# Access Geocoding API to obtain plus_code, longitude, and latitude
# Append new data to excel worksheet
import urllib.request, urllib.parse, urllib.error
import json
import pandas as pd
from openpyxl import load_workbook

api_key = False
# If you have a Google Places API key, enter it here and uncomment
# api_key = 'AIzaSyDARYIx4bmWx5FXrOOeDtYJp68KmUEVzPg'
# https://developers.google.com/maps/documentation/geocoding/intro

if api_key is False:
    api_key = 42
    serviceurl = 'http://py4e-data.dr-chuck.net/json?'
else:
    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

# The sheet we want to update
sheet = 'Shopping Malls'
# Read Location Name from Worksheet.xlsx, sheet 1
work = pd.read_excel('Worksheet.xlsx', sheet_name = sheet)
print('Total number of locations:', len(work))
locations = work['Name']

lats = list()
lngs = list()
plus_codes = list()
for location in locations:

    parms = dict()
    parms['key'] = api_key
    parms['address'] = location + ' ,Singapore'
    url = serviceurl + urllib.parse.urlencode(parms)

    print('Retrieving', url)
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')

    try:
        js = json.loads(data)
    except:
        js = None

    if js is None or 'status' not in js or js['status'] != 'OK':
        print('==== Failure To Retrieve ====')
        print(json.dumps(js, indent=4))
        continue
    #print(json.dumps(js, indent=4))
    lat = js['results'][0]['geometry']['location']['lat']
    lng = js['results'][0]['geometry']['location']['lng']
    # Some locations do not have plus_code
    try:
        plus_code = js['results'][0]['plus_code']['compound_code']
    except:
        plus_code = None
    lats.append(lat)
    lngs.append(lng)
    plus_codes.append(plus_code)
    print('Location {}: latitude = {}, longitude = {}, plus_code = {}'.format(location, lat, lng, plus_code))

# Write to the excel sheet
# Remember not to open excel file when appending new data to it!!!
writer = pd.ExcelWriter('Worksheet.xlsx', mode = 'a', engine = 'openpyxl')
writer.book = load_workbook('Worksheet.xlsx')
writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets) #copy existing sheets
d = {'Plus Code': plus_codes, 'Latitude': lats, 'Longitude': lngs}
df = pd.DataFrame(data = d)
df.to_excel(writer, sheet_name = sheet, startcol = 2, index = False, header = False, startrow = 1)
writer.close()



