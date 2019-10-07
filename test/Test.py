import requests
from datetime import datetime

import pymysql
from lxml import etree
import requests
import time


def getArea(vals):
    tex = ""
    for val in vals:
        tex = tex + ',' + val.text
    return tex

url = 'http://nn.loupan.com/xinfang/p1'
print(url)
data = requests.get(url)
data.encoding = 'utf-8'
tx = data.text
s=etree.HTML(tx)
houses = s.xpath('/html/body/div[7]/div[3]/div[3]/div[1]/ul/li')
time.sleep(2)

lists = []
for house in houses:
    try:
        name = house.xpath("./div[1]/h2/a/text()")[0].strip()
        layout = getArea(house.xpath("./div[1]/div[2]/span[1]/a"))
        address = house.xpath("./div[1]/div[1]/span/text()")[0].strip()
        price = house.xpath("./div[2]/div[1]/span/text()")[0].strip()
        unit = ''
        area = '0'
        if(price != '价格待定'):
            area = house.xpath("./div[1]/div[2]/span[2]/a/text()")[0].strip()
            unit = house.xpath("./div[2]/div[1]/text()[2]")[0].strip()
        district = address.split('-')[0]
        type = 'loupan.com'
        url = house.xpath("./a/@href")[0].strip()
        row = (name, layout, area, address, price, unit, datetime.today().strftime('%Y-%m-%d %H:%M:%S'), district, type, url)
        lists.append(row)
        print(row)
    except Exception as e:
        print("err:" + str(e))
