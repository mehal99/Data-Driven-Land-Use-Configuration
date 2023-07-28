import pandas as pd
from pathlib import Path
import requests
import json
import time
import os

final_data = []
api_key = ''

#read excel file
pre = os.path.dirname(os.path.realpath(__file__))
fname = 'Data/Data_clearning.xlsx'
path = os.path.join(pre, fname)
df = pd.read_excel(path, sheet_name='shopping_mall')
place_ids = df['place_ID']

#get reviews
for place_id in place_ids:
    url = 'https://maps.googleapis.com/maps/api/place/details/json?place_id='+ place_id +'&key='+str(api_key)
    print(url)
    print(place_id)
    respon = requests.get(url)
    json_result = json.loads(respon.text)

    if('result' in json_result):
        results = json_result['result']
        if('reviews' in results):
            reviews = results['reviews']
            for review in reviews:
                review_text = review['text']
                language = (review['language'] if "language" in review else '')
                rating = (review['rating'] if "rating" in review else '')

                print(review_text)
                data = [place_id, language, rating, review_text]
                final_data.append(data)
                time.sleep(5)

#export
labels = ['place_ID', 'language', 'rating', 'review']
export_data = pd.DataFrame.from_records(final_data, columns=labels)
# print(export_data)

output_file = 'Reviews.xlsx'
output_dir = Path('Google_API/Data')
output_dir.mkdir(parents=True, exist_ok=True)
export_data.to_excel(output_dir/output_file, sheet_name='shopping_mall', encoding='utf_8_sig')

