# -*- coding: utf-8 -*-
import datetime
import json
import os
import re
import uuid
from abc import ABC
from copy import copy
from urllib.request import urlretrieve

import scrapy
from pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from ..items import ContentItem


class AdminSpider(scrapy.Spider, ABC):
    """
       作用：根据关键字爬取csdn对应的博客

       """
    # 爬虫名字
    name = 'admin_spider'

    # 本脚本的配置
    custom_settings = {
        # 是否遵守反爬协议
        'ROBOTSTXT_OBEY': False,
        'COOKIES_ENABLED': False,
        # 每次并发请求的数量，如果数量太大，爬虫可能会被封。
        'CONCURRENT_REQUESTS': 5,
        # 每次请求之后延迟0.3秒再请求
        'DOWNLOAD_DELAY': .3,
        # 请求允许的响应码
        'HTTPERROR_ALLOWED_CODES': [403, 404],
    }
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'COOKIES_ENABLED': False,  # enabled by default
        'DOWNLOADER_MIDDLEWARES': {
            'ContentSpider.middlewares.SeleniumOption': 500,
            'ContentSpider.middlewares.RandomUserAgent': 543,
            'ContentSpider.middlewares.ProxyMiddleware': 544,
        },
        'ITEM_PIPELINES': {
            # 'myproject.pipelines.MyImagesPipeline': 300  #自己的管道
            'ContentSpider.pipelines.ContentImagesPipeline': 546,
            # 'ContentSpider.pipelines.FilesPipeline': 100,
            'ContentSpider.pipelines.DataPipeline': 551,
            # 'ContentSpider.pipelines.DuplicatesPipeline': 1,
        }
    }

    def __init__(self, *args, **kwargs):

        # 从settings.py中获取设置参数
        self.mySetting = get_project_settings()
        self.timeout = self.mySetting['SELENIUM_TIMEOUT']
        self.isLoadImage = self.mySetting['LOAD_IMAGE']
        self.windowHeight = self.mySetting['WINDOW_HEIGHT']
        self.windowWidth = self.mySetting['WINDOW_WIDTH']
        options = webdriver.ChromeOptions()
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # chrome_options.add_experimental_option("prefs", prefs) 禁止图片加载
        options.add_argument('lang=zh_CN.UTF-8')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        # 初始化chrome对象
        self.browser = webdriver.Chrome(options=options, service_args=self.mySetting.get('SERVICE_ARGS'))
        if self.windowHeight and self.windowWidth:
            self.browser.set_window_size(900, 900)
        self.browser.set_page_load_timeout(self.timeout)  # 页面加载超时时间
        self.wait = WebDriverWait(self.browser, 25)  # 指定元素加载超时时间
        super(AdminSpider, self).__init__(*args, **kwargs)
        params = json.loads(kwargs['params'])
        self.deal_params(params)
        # 设置信号量，当收到spider_closed信号时，spider_close_handle，关闭chrome
        dispatcher.connect(receiver=self.spider_close_handle,
                           signal=signals.spider_closed)

    # 信号量处理函数：关闭chrome浏览器
    def spider_close_handle(self, spider):
        self.logger.info(f"spider_close_handle: enter ")
        self.browser.quit()

    def start_requests(self):
        self.logger.debug('start_requests---------------------------------')
        if isinstance(self.start_urls, list):
            for url in self.start_urls:
                if self.url_type == 1:
                    yield scrapy.Request(url=url, callback=self.list_parse, meta={'usedSelenium': False})
                elif self.url_type == 2:
                    yield scrapy.Request(url=url, callback=self.detail_parse, meta={'usedSelenium': False})
        else:
            self.logger.debug(self.url_type)
            if self.url_type == 1:
                yield scrapy.Request(url=self.start_urls, callback=self.list_parse, meta={'usedSelenium': False})
            elif self.url_type == 2:
                yield scrapy.Request(url=self.start_urls, callback=self.detail_parse, meta={'usedSelenium': False})

    def single_parse(self, response):
        pass

    def list_parse(self, response):
        # filename = 'articletest.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)

        art_list = response.xpath(self.list_xpath).getall()
        self.logger.info('---' * 10 + 'art_list')
        self.logger.debug(art_list)
        i = 0
        if art_list:
            for url in art_list:
                i += 1
                # if i > 2:  # 限制请求测试用
                #     break
                if url.startswith('http'):
                    self.logger.debug(response.urljoin(url))
                    yield scrapy.Request(response.urljoin(url), callback=self.detail_parse, dont_filter=True,
                                         meta={'usedSelenium': False})
                else:
                    continue

    def detail_parse(self, response):
        self.logger.info('detail_response_start' + '___' * 20)
        item = ContentItem()
        i = len(self.rules)
        item_list = ['title', 'author', 'create_time', 'tag', 'content', 'thumb', 'image_urls']
        item_list_copy = copy(item_list)
        if i > 0:
            for rule in self.rules:
                for field in item_list:
                    if rule['name'] == field:
                        self.logger.info('match' + '__-_' * 10)
                        self.logger.debug(rule['match'])
                        if field == 'content':
                            content = response.xpath(rule['match']).get()
                            if content is not None:
                                images = response.xpath(rule['match']).xpath('.//img/@src').getall()
                                image_urls = []
                                # 将链接替换为完整链接
                                for image in images:
                                    url = response.urljoin(image)
                                    if url.startswith('http'):
                                        content = content.replace(image, response.urljoin(image))
                                        image_urls.append(response.urljoin(image))
                                if len(image_urls) > 0:
                                    item_list_copy.remove('image_urls')
                                item['image_urls'] = image_urls
                                content = content.replace(self.url_no_contain, self.url_contain)
                                item['content'] = content
                                self.logger.debug('------*******' * 10)
                                self.logger.debug(image_urls)
                                self.logger.debug(content)
                                item['thumb'] = ''
                                item_list_copy.remove('thumb')
                            else:
                                continue

                        else:
                            item['%s' % field] = response.xpath(rule['match']).get()
                        item_list_copy.remove('%s' % field)
        self.logger.info('item_list_copy' + '___' * 10)
        self.logger.debug(item_list_copy)
        if len(item_list_copy) > 0:
            for field in item_list_copy:
                if field == 'thumb':
                    item['%s' % field] = None
                elif field == 'image_urls':
                    item['%s' % field] = []
                else:
                    item['%s' % field] = ''
        item['origin_url'] = response.url
        item['cate_id'] = self.cate_id
        yield item

    def close(self, reason):
        self.logger.info(reason)
        pass

    def clear_br(self, value):
        """
        文本中包含有<br>标签的话，传值到itme中就不会是整个文本，而是一条一条的数据
            保存到数据库的时候会报错：Operand should contain 1 column(s)
            那就要将文本里面的<br>换成其他，由于传递过来的value是一个列表list，所以用for循环把元素replace也可以
            这里用.join()方法把列表里的所有元素用逗号拼接成字符串
        """
        value = ','.join(value)
        return value

    def deal_params(self, params):

        self.params_copy = copy(params)
        for key in params:
            # 字符集
            if key == 'charset':
                self.charset = params[key]
                self.log('charset' + '___' * 10)
                self.logger.debug(self.charset)
                self.params_copy.pop(key)
            # 允许域名
            if key == 'allowed_domains':
                self.allowed_domains = list(filter(None, params[key].split('#')))
                self.log('allowed_domains' + '___' * 10)
                self.logger.debug(self.allowed_domains)
                self.params_copy.pop(key)
            # 开始网址
            if key == 'start_urls':
                self.start_urls = list(filter(None, params[key].split('#')))
                self.log('start_urls' + '___' * 10)
                self.logger.debug(self.start_urls)
                self.params_copy.pop(key)
            # 爬虫类型
            if key == 'url_type':
                self.url_type = int(params[key])
                self.log('url_type' + '___' * 10)
                self.logger.debug(self.url_type)
                self.params_copy.pop(key)
            # 列表规则
            if key == 'list_xpath':
                self.list_xpath = params[key]
                self.log('list_xpath' + '___' * 10)
                self.logger.debug(self.list_xpath)
                self.params_copy.pop(key)
            # 内容链接不应该包函
            if key == 'url_no_contain':
                if params[key] is None:
                    self.url_no_contain = ' '
                else:
                    self.url_no_contain = params[key]
                self.log('url_no_contain' + '___' * 10)
                self.logger.debug(self.url_no_contain)
                self.params_copy.pop(key)
            # 内容链接应该包函
            if key == 'url_contain':
                if params[key] is None:
                    self.url_contain = ' '
                else:
                    self.url_contain = params[key]
                self.log('url_contain' + '___' * 10)
                self.logger.debug(self.url_contain)
                self.params_copy.pop(key)
            # 内容所属分类
            if key == 'cate_id':
                self.cate_id = params[key]
                self.log('cate_id' + '___' * 10)
                self.logger.debug(self.cate_id)
                self.params_copy.pop(key)
            if key == 'rules':
                self.rules = json.loads(params[key])
                self.log('rules' + '___' * 10)
                self.logger.debug(self.rules)
                self.params_copy.pop(key)
        self.log('last_params' + '___' * 10)
        self.logger.debug(self.params_copy)

    # 列表规则
    list_xpath = ''
    # 爬虫类型
    url_type = 1
    # 爬虫被允许访问的域名
    allowed_domains = ''
    url_no_contain = ''
    url_contain = ''
    charset = 'utf-8'
    params_copy = {}
    cate_id = 0
    rules = {}
