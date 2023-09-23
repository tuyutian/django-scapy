# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import json
import os
import uuid
from urllib.parse import urlparse
from urllib.request import urlretrieve

import requests
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonLinesItemExporter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline

import pymongo
# ============================MySQL===========================
import pymysql

from scrapy.utils.project import get_project_settings


class DuplicatesPipeline(object):
    """
    去重
    """

    def __init__(self):
        self.book_set = set()

    def process_item(self, item, spider):
        name = item['title']
        if name in self.book_set:
            raise DropItem("Duplicate book found:%s" % item)

        self.book_set.add(name)
        return item


# 内容图片下载替换管道 伪（滑稽）
class ContentImagesPipeline:

    @staticmethod
    def send_img(img_path, img_name, url, img_type='image/jpeg'):
        """
        :param img_path:图片的路径
        :param img_name:图片的名称
        :param img_type:图片的类型,这里写的是image/jpeg，也可以是png/jpg
        :param url:自己想要请求的接口地址
        """
        with open(img_path + img_name, "rb")as f_abs:  # 以2进制方式打开图片
            body = {
                # 有些上传图片时可能会有其他字段,比如图片的时间什么的，这个根据自己的需要
                'img': (img_name, f_abs, img_type),
                # 图片的名称、图片的绝对路径、图片的类型（就是后缀）
                "time": (None, "2019-01-01 10:00:00")

            }
            # 上传图片的时候，不使用data和json，用files
            response = requests.post(url=url, files=body)
            result = eval(response.text)
            if result['code'] == 200:
                return result['data']['url']
            else:
                return False

    @staticmethod
    def get_filename(url_str):
        url = urlparse(url_str)
        print(url)
        i = len(url.path) - 1
        while i > 0:
            if url.path[i] == '/':
                break
            i = i - 1
        filename = url.path[i + 1:len(url.path)]
        if not filename.strip():
            return False
        return filename

    def process_item(self, item, spider):
        image_urls = item['image_urls']
        spider.logger.debug('------*******' * 10)
        spider.logger.debug(image_urls)
        mySetting = get_project_settings()
        # 文件夹生成当天的
        today = datetime.datetime.now()
        file_path = '{}{}{}'.format(today.year, today.month, today.day)
        # 服务器文件储存路劲
        storage_path = mySetting['STORAGE_PATH']
        images_path = storage_path + file_path + '/'
        os.makedirs(images_path, exist_ok=True)
        server_image_urls =[]
        if len(image_urls) > 0:
            for image_url in image_urls:
                file_name = self.get_filename(image_url)
                if file_name:
                    # 获取随机字符
                    uuid_str = uuid.uuid4().hex
                    file_type = os.path.splitext(file_name)[1]
                    # 图片物理路径
                    image_path = images_path + uuid_str + file_type
                    # 存储图片
                    urlretrieve(image_url, image_path)
                    url = self.send_img(images_path, uuid_str + file_type, mySetting['STORAGE_SERVER_API'])
                    if url:
                        server_image_urls.append(url)
                        item['content'] = item['content'].replace(image_url, url)
                    else:
                        item['content'] = item['content'].replace(image_url, '')
                else:
                    continue
        if len(server_image_urls)>0:
            item['thumb'] = server_image_urls[0]
            item['image_urls'] = server_image_urls
        return item


class MyFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1] + '.jpg'
        return file_name

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem('File DownloadedFailed')
        return item

    def get_media_requests(self, item, info):
        if item['file_urls'] is not None:
            for file_url in item['file_urls']:
                yield Request(file_url)


class DataPipeline:

    def __init__(self):
        self.fp = open('content.json', 'wb')
        self.export = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')
        pass

    def open_spider(self, spider):
        self.fp.write(b'[')
        pass

    def close_spider(self, spider):
        self.fp.write(b']')
        self.fp.close()
        pass

    def process_item(self, item, spider):
        data = dict(item)
        self.export.export_item(data)
        print('datapipeline-----------------------------')
        self.fp.write(b',')
        requests.post(spider.settings.get('TARGET'), {'data': json.dumps(data)})
        return item


class MongoPipeline(object):
    def __init__(self, mongodb_url, mongodb_DB):
        self.db = self.client[self.mongodb_DB]
        self.client = pymongo.MongoClient(self.mongodb_url)
        self.mongodb_url = mongodb_url
        self.mongodb_DB = mongodb_DB

    @classmethod
    # 获取settings配置文件当中设置的MONGODB_URL和MONGODB_DB
    def from_crawler(cls, crawler):
        return cls(
            mongodb_url=crawler.settings.get("MONGODB_URL"),
            mongodb_DB=crawler.settings.get("MONGODB_DB")
        )

    # 开启爬虫时连接MongoDB数据库
    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        table_name = item.collection
        self.db[table_name].insert(dict(item))
        return item

    # 关闭爬虫时断开MongoDB数据库连接
    def close_spider(self, spider):
        self.client.close()


class MysqlPipeline:
    def __init__(self, host, database, port, user, password):
        self.host = host
        self.database = database
        self.port = port
        self.user = user
        self.password = password

    @classmethod
    # 获取settings配置文件当中设置的MySQL各个参数
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get("MYSQL_HOST"),
            database=crawler.settings.get("MYSQL_DATABASE"),
            port=crawler.settings.get("MYSQL_PORT"),
            user=crawler.settings.get("MYSQL_USER"),
            password=crawler.settings.get("MYSQL_PASSWORD")
        )

    # 开启爬虫时连接MySQL数据库
    def open_spider(self, spider):
        self.db = pymysql.connect(host=self.host, database=self.database, user=self.user, password=self.password,
                                  port=self.port, charset="utf8")
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ",".join(data.keys())  # 字段名
        values = ",".join(["%s"] * len(data))  # 值
        sql = "insert into %s(%s) values(%s)" % (item.table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item

    # 关闭爬虫时断开MySQL数据库连接
    def close_spider(self, spider):
        self.db.close()
