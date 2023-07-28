import pandas as pd
import requests
import json
import time
from pathlib import Path

final_data = []
api_key = ''

region_list =['Marina Bay','Marina Centre','Raffles Place','Tanjong Pagar','Outram','Sentosa','Rochor','Orchard','Newton','River Valley','Bukit Timah',
'Holland Road','Tanglin','Novena','Thomson','Bishan','Bukit Merah','Geylang','Kallang','Marine Parade','Queenstown','Toa Payoh'
'Lim Chu Kang','Mandai','Sembawang','Simpang','Sungei Kadut','Woodlands''Yishun''Ang Mo Kio','Hougang','North-Eastern Islands','Punggol','Seletar',
'Sengkang','Serangoon','Bedok','Changi','Changi Bay','Paya Lebar','Pasir Ris',
'Tampines','Bukit Batok','Bukit Panjang','Boon Lay','Pioneer','Choa Chu Kang','Clementi','Jurong East','Jurong West','Tengah',
'Tuas','Western Islands','Western Water Catchment','Benoi','Ghim Moh','Gul','Pandan Gardens',
'Jurong Island','Kent Ridge','Nanyang','Pioneer','Pasir Laba','Teban Gardens','Toh Tuck','Tuas South','West Coast']

for regions in region_list:
    regions =regions.replace (" ", "+")
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=shopping+mall+around+'+ str(regions) +'&key='+str(api_key)

    while True:
        print(url)
        respon = requests.get(url)
        json_result = json.loads(respon.text)
        results = json_result['results']

        for result in results:
            name = result['name']
            print(name)
            place_id = result ['place_id']
            lat = result['geometry']['location']['lat']
            lng = result['geometry']['location']['lng']

            if 'plus_code' in result:
                print(result['plus_code'])
                plus_code = result['plus_code']['compound_code']
            else:
                plus_code = 0

            rating = (result['rating'] if "rating" in result else '')
            user_ratings_total = (result['user_ratings_total'] if "user_ratings_total" in result else 0)
            business_status = (result['business_status'] if "business_status" in result else '')
            types = (result['types'][0] if "types" in result else '')
            formatted_address = (result['formatted_address'] if "formatted_address" in result else '')

            if ((int(result['user_ratings_total']) > 5) and (business_status == 'OPERATIONAL') and (types == 'shopping_mall')):
                data = [name, place_id, lat, lng, plus_code, rating, user_ratings_total, business_status, types, formatted_address]

            final_data.append(data)
            time.sleep(5)

        if 'next_page_token' not in json_result:
            break
        else:
            next_page_token = json_result['next_page_token']
            url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?key='+str(api_key)+'&pagetoken='+str(next_page_token)
            continue


labels = ['place_name', 'place_ID', 'latitude', 'Longitude', 'plus_code', 'rating', 'user_ratings_total', 'business_status', 'types', 'address']
export_data = pd.DataFrame.from_records(final_data, columns=labels)

output_file = 'Data.xlsx'
output_dir = Path('Google_API/Data')
output_dir.mkdir(parents=True, exist_ok=True)
export_data.to_excel(output_dir/output_file, sheet_name='shopping_mall', encoding='utf_8_sig')
