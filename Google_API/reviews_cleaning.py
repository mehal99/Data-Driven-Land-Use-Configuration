import pandas as pd
from pathlib import Path
import re
import os
from pathlib import Path

pre = os.path.dirname(os.path.realpath(__file__))
fname = 'Data/Reviews.xlsx'
path = os.path.join(pre, fname)
df = pd.read_excel(path, sheet_name='shopping_mall')
print("Before clearning: " + str(len(df)))

# drop null row
df = df.dropna()
print("After 1: " + str(len(df)))

# reset index
df.reset_index(drop=True, inplace = True)
print(df)

# Save Reviews_clean.xlsx under Google_API/Data/
output_file = 'Reviews_clean.xlsx'
output_dir = Path('Data')
output_dir.mkdir(parents=True, exist_ok=True)
df.to_excel(output_dir/output_file, sheet_name='shopping_mall', encoding='utf_8_sig')
