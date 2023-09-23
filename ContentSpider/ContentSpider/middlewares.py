# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import random
import time

import requests

from scrapy import signals

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from scrapy.http import HtmlResponse
from logging import getLogger
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SeleniumOption:
    # Middleware中会传递进来一个spider，这就是我们的spider对象，从中可以获取__init__时的chrome相关元素
    def process_request(self, request, spider):
        """
        用chrome抓取页面
        :param request: Request请求对象
        :param spider: Spider对象
        :return: HtmlResponse响应
        """
        # 依靠meta中的标记，来决定是否需要使用selenium来爬取
        spider.logger.debug('ChromeServer is Starting')
        try:
            spider.browser.get(request.url)
            time.sleep(random.randint(2, 4))
            js = "var q=document.documentElement.scrollTop=1000"
            spider.browser.execute_script(js)  # 可执行js，模仿用户操作。此处为将页面拉至最底端。
            time.sleep(random.randint(1, 3))
            spider.logger.debug("访问" + request.url)
            self.use_selenium_func(request, spider)
            return HtmlResponse(url=request.url, body=spider.browser.page_source, request=request, encoding='utf-8',
                                status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)

    def use_selenium_func(self, request, spider):
        used_selenium = request.meta.get('usedSelenium', False)
        if used_selenium:
            if request.meta.get('pageType', '') == 'login':
                # 先存储原始的url链接
                originalUrl = request.url
                try:
                    # 会自动跳转到登录页面
                    spider.browser.get(originalUrl)
                    # 用户名登录框是否出现
                    usernameInput = spider.wait.until(
                        EC.presence_of_element_located((By.XPATH, "//div[@id='messagelogin']//input[@name='username']"))
                    )
                    time.sleep(2)
                    usernameInput.clear()
                    usernameInput.send_keys("ancoxxxxxxx")  # 输入用户名

                    passWordElem = spider.browser.find_element_by_xpath(
                        "//div[@id='messagelogin']//input[@name='password']")
                    time.sleep(2)
                    passWordElem.clear()
                    passWordElem.send_keys("anco00000000")  # 输入密码

                    captchaElem = spider.browser.find_element_by_xpath(
                        "//div[@id='messagelogin']//input[@name='seccodeverify']")
                    time.sleep(2)
                    captchaElem.clear()
                    # 此处采用手动输入
                    # 关于自动打码，可以参考之前写过的文章,链接如下：
                    # https://blog.csdn.net/zwq912318834/article/details/78616462
                    captcha = input("输入验证码\n>").strip()
                    captchaElem.send_keys(captcha)  # 输入验证码

                    # 点击登录按钮
                    loginButtonElem = spider.browser.find_element_by_xpath(
                        "//div[@id='messagelogin']//button[@name='loginsubmit']")
                    time.sleep(2)
                    loginButtonElem.click()
                    time.sleep(1)
                    seleniumCookies = spider.browser.get_cookies()
                    print(f"seleniumCookies = {seleniumCookies}")
                    # # 查看搜索结果是否出现
                    # searchRes = spider.wait.until(
                    #     EC.presence_of_element_located((By.XPATH, "//div[@id='resultsCol']"))
                    # )
                except Exception as e:
                    print(f"chrome user login handle error, Exception = {e}")
                    return HtmlResponse(url=request.url, status=500, request=request)
                else:
                    time.sleep(3)
                    # 登录成功之后，获取到selenium的cookie
                    cookie = [item["name"] + ":" + item["value"] for item in seleniumCookies]
                    cookMap = {}
                    for elem in cookie:
                        str = elem.split(':')
                        cookMap[str[0]] = str[1]
                    print(f"cookMap = {cookMap}")
                    # 中间件，对Request进行加工
                    # 开始用这个转换后的cookie重新构造Request，从源码中来看Request构造的原型
                    # E:\Miniconda\Lib\site-packages\scrapy\http\request\__init__.py
                    request.cookies = cookMap  # 让这个带有登录后cookie的Request继续爬取
                    request.meta['usedSelenium'] = False  # 避免这个url发生重定向302，里面的meta信息会让它回到这个流程


class SeleniumMiddleware:

    def __init__(self, timeout=None, options=None, service_args=None):
        if options is None:
            options = []
        if service_args is None:
            service_args = []
        self.logger = getLogger(__name__)
        self.timeout = timeout
        print(options)
        self.browser = webdriver.Chrome(options=options, service_args=service_args)
        self.browser.set_window_size(1400, 700)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()

    def process_request(self, request, spider):
        """
        用ChromeServer抓取页面
        :param request: Request对象
        :param spider: Spider对象
        :return: HtmlResponse
        """
        self.logger.debug('ChromeServer is Starting')
        try:
            self.browser.get(request.url)
            time.sleep(random.randint(1, 3))
            js = "var q=document.documentElement.scrollTop=1000"
            self.browser.execute_script(js)  # 可执行js，模仿用户操作。此处为将页面拉至最底端。
            time.sleep(random.randint(1, 3))
            print("访问" + request.url)
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        options = webdriver.ChromeOptions()
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # chrome_options.add_experimental_option("prefs", prefs) 禁止图片加载
        options.add_argument('lang=zh_CN.UTF-8')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        return cls(timeout=settings.get('SELENIUM_TIMEOUT'),
                   options=options,
                   service_args=settings.get('SERVICE_ARGS'))


class ContentspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ContentspiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 对接IP代理池
class ProxyMiddleware:
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        if request.meta.get('retry_times'):
            proxy = self.get_random_proxy()
            if proxy:
                uri = 'https://{proxy}'.format(proxy=proxy)
                self.logger.debug('使用代理 ' + proxy)
                request.meta['proxy'] = uri

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )


# 随机切换User-Agent
class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        # print ("**************************" + random.choice(self.agents))
        request.headers.setdefault('User-Agent', random.choice(self.agents))
