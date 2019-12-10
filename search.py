from pymongo import MongoClient
from pymongo import *
import re

conn = MongoClient('localhost', 27017)
db = conn.mydb
my_set = db.shares

for item in my_set.find().sort('bonusRatio', DESCENDING).limit(10):
    print(item)