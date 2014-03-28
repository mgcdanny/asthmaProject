from pprint import pprint
import json
import csv
import re

header = ['zipcode','discharge','rate','county','bucket']
reader = csv.DictReader(open("asthma.csv","rb"), header)

asthma = {}

for row in reader:
    if row['zipcode'] in asthma:
        asthma[row['zipcode']][row['bucket']] = {'discharge':row['discharge'],'rate':row['rate']}
    else:
        asthma[row['zipcode']] = {}
        asthma[row['zipcode']][row['bucket']] = {'discharge':row['discharge'],'rate':row['rate']}
        

raw = json.loads(open("nyc_zip.json", "rb").read())

for row in raw['features']:
    zipcode = row['properties']['postalCode']
    if zipcode in asthma:
        row['properties']['asthma'] = asthma[zipcode]
    else:
        row['properties']['asthma'] = {}
        row['properties']['asthma'] = {'discharge':0,'rate':0}
        print("missing data for this zip code: ")
        print(zipcode)


with open("nyc_zip_astham.json", "wb") as f:
    f.write(json.dumps(raw))

with open("../map/nyc_zip_asthma.js", "wb") as f:
    f.write("var nycdata = " + json.dumps(raw))
