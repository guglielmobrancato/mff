import pandas as pd
import json
import os

df = pd.read_excel('assets/film selezionati.xlsx')
df = df.fillna('')
records = df.to_dict('records')

with open('temp_excel.json', 'w', encoding='utf-8') as f:
    json.dump(records, f, indent=2, ensure_ascii=False)
