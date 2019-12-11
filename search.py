from pymongo import MongoClient
from pymongo import *
import re
from prettytable import PrettyTable


conn = MongoClient('localhost', 27017)
db = conn.mydb
my_set = db.shares

headings = ['股票', '当前股价', '市盈率', '市净率', '分红利率', '振幅', '换手率', '成交量', '成交额']
table = PrettyTable(headings)


item_list = []
for item in my_set.find({'市盈率': {'$gt': 0.0}}).sort('分红利率', DESCENDING).limit(20):
    table.add_row([item['name'], item['最新股价'], item['市盈率'], item['市净率'], item['分红利率'], item['振幅'], item['换手率'], item['成交量'], item['成交额']])

print(table)