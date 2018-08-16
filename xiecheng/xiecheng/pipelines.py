# -*- coding: utf-8 -*-


import pymongo
from scrapy.conf import settings

class XiechengPipeline(object):
    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        sheetname = settings["MONGODB_SHEETNAME"]
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        mydb = client[dbname]
        # 存放数据的数据库表名
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item

import json
import codecs

class XiechengCrawlPipeline(object):
    def __init__(self):
        self.filename=codecs.open('xiecheng.json','w',encoding="utf-8")

    def process_item(self,item,spider):
        text=json.dumps(dict(item),ensure_ascii=False) + ',\n'
        self.filename.write(text)
        return item
    def close_spider(self,spider):
        self.filename.close()