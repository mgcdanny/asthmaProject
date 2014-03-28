from lxml import html
import requests as rq
import csv

borough = ["queen", "bronx", "new_y", "richm", "kings"]
table = {"t1":"Age 0-4", "t2":"Age 5-11", "t3":"Age 0-17","t4":"Age 18-64","t5":"Age 65+","t6":"Total", "t21":"Age 12-17"}

urls = {}
for b in borough:
    for t in table:
        urls["https://www.health.ny.gov/statistics/ny_asthma/ed/zipcode/{borough}_{table}.htm".format(borough=b , table=t)] = {"borough": b, "bucket":table[t]}

data = []
for u in urls:
    print(u)
    mainPage = rq.get(u)
    print(mainPage)
    tree = html.fromstring(mainPage.text)
    raw = tree.xpath('//*[@id="content"]/table')[0]
    rows = raw.findall('tr')
    for row in rows[2:]:
        temp = [c.text.strip().replace(',','') for c in row.getchildren()]
        if temp[0].isdigit() and temp[1].isdigit():
            temp.extend(urls[u].values())
            data.append(temp)

with open("asthma.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(data)
