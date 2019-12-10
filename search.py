from pymongo import MongoClient
from pymongo import *
import re

conn = MongoClient('localhost', 27017)
db = conn.mydb
my_set = db.shares

for item in my_set.find().sort('分红利率', DESCENDING).limit(20):
    print(item)