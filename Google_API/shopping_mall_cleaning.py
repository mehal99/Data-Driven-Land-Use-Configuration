import pandas as pd
from pathlib import Path
import re

df = pd.read_excel("Google_API/Data/Data.xlsx")
print("Before clearning: " + str(len(df)))

# remove duplicate data
df.sort_values("place_ID", inplace=True)
df.drop_duplicates(subset="place_ID", keep="first", inplace=True)
print("After 1: " + str(len(df)))

# remove other countries
df = df[df['plus_code'].str.contains("Singapore")]
print("After 2: " + str(len(df)))

# drop non-english name
for name in df['place_name']:
    if re.search(u'[\u4e00-\u9fff]', name):
        df = df[df['place_name'] != name]
print("After 3: " + str(len(df)))

# reset index
df.drop(df.columns[0], axis = 1, inplace = True)
df.reset_index(drop=True, inplace = True)
print(df)

# Save Data_clean.xlsx under Google_API/Data/
output_file = 'Data_clean.xlsx'
output_dir = Path('Google_API/Data')
output_dir.mkdir(parents=True, exist_ok=True)
df.to_excel(output_dir/output_file, sheet_name='shopping_mall', encoding='utf_8_sig')
