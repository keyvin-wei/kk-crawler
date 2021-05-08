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

config={
    "host":"127.0.0.1",
    "user":"root",
    "password":"123456",
    "database":"knowledge_db"
}
db = pymysql.connect(**config)
cursor = db.cursor()
sql = "INSERT INTO `tb_data_house` (`name`, `layout`, `area`, `address`, `price`, `unit`, `create_time`, `district`, `type`, `url`) " \
      "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

error = 0
succeed = 0
for a in range(38):
    url = 'http://nn.loupan.com/xinfang/p{}'.format(a+1)
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
            else:
                price = '0'
            district = address.split('-')[0]
            type = 'loupan.com'
            url = house.xpath("./a/@href")[0].strip()
            row = (name, layout, area, address, price, unit, datetime.today().strftime('%Y-%m-%d %H:%M:%S'), district, type, url)
            lists.append(row)
            print(row)
            succeed = succeed + 1
        except:
            error = error + 1
    cursor.executemany(sql, lists)
    db.commit()
    print("DB插入完成：" + str(len(lists)))

cursor.close()
db.close()
print("爬取完成，成功：" + str(succeed) + "条，失败：" + str(error) + "条")