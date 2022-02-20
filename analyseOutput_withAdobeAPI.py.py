import json
import zipfile
import os
import pandas as pd

COUNT_COLS = 4

base_path = "/".join(__file__.split('/')[:-1]) + '/'
filename_zip = 'ExtractTextInfoFromPDF.zip'
filename_json = 'structuredData.json'

if not os.path.exists(base_path + filename_json):
    zipfile.ZipFile(base_path + '/output/' + filename_zip, 'r').extractall(base_path)

output_file = open(base_path + filename_json, 'r')
output = json.load(output_file)
elements = output['elements']

table = dict()
for e in elements:
    if 'Text' in e.keys() and 'Table' in e['Path']:
        label = e['Path'].split('/')

        tr = int('0' + label[5].replace('TR', '').replace('[', '').replace(']', ''))
        td = int('0' + label[6].replace('TH', '').replace('TD', '').replace('[', '').replace(']', ''))
        if td > 0: td -= 1

        if tr not in table: table[tr] = [''] * COUNT_COLS

        table[tr][td] = e['Text']

df = pd.DataFrame().from_dict(table).T
df.to_csv('data.csv')