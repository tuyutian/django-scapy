# -*- coding: utf-8 -*-

# Scrapy settings for ContentSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import datetime
import os

BOT_NAME = 'ContentSpider'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPIDER_MODULES = ['ContentSpider.spiders']
NEWSPIDER_MODULE = 'ContentSpider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'ContentSpider (+http://www.yourdomain.com)'
URLLENGTH_LIMIT = 5000
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# 是否启用日志
LOG_ENABLED = True
# 日志时间格式
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'
# 日志使用的编码
LOG_ENCODING = 'utf-8'
# 日志级别 CRITICAL, ERROR, WARNING, INFO, DEBUG
LOG_LEVEL = 'DEBUG'
# 如果等于True，所有的标准输出（包括错误）都会重定向到日志，例如：print('hello')
LOG_STDOUT = False
# 如果等于True，日志仅仅包含根路径，False显示日志输出组件
LOG_SHORT_NAMES = False
today = datetime.datetime.now()

LOG_FILE = 'logs/scrapy_{}_{}_{}.log'.format(today.year, today.month, today.day)
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'ContentSpider.middlewares.ContentSpiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html


# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'myproject.pipelines.MyImagesPipeline': 300  #自己的管道
    # 'ContentSpider.pipelines.MyImagesPipeline': 80,
    # 'ContentSpider.pipelines.FilesPipeline': 100,
    'ContentSpider.pipelines.DataPipeline': 10,
    # 'ContentSpider.pipelines.DuplicatesPipeline': 1,
}
FILES_STORE = os.path.join(BASE_DIR, 'static/files')
IMAGES_STORE = os.path.join(BASE_DIR, 'static/images')
# IMAGES_THUMBS = {
#     'small': (50, 50),
#     'big': (270, 270),
# }
# IMAGES_MIN_HEIGHT = 80  # 图像最小高度
# MEDIA_ALLOW_REDIRECTS = True  # 允许媒体链接重定向
# 图像管道避免下载最近已经下载的图片。使用 FILES_EXPIRES (或 IMAGES_EXPIRES) 设置可以调整失效期限，
# 可以用天数来指定
IMAGES_EXPIRES = 30

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 抛出可用IP地址
PROXY_URL = 'http://www.goubanjia.com/'
proxy_list = [
    '183.95.80.102:8080',
    '123.160.31.71:8080',
    '115.231.128.79:8080',
    '166.111.77.32:80',
    '43.240.138.31:8080',
    '218.201.98.196:3128'
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36 Edg/81.0.416.53",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0",
]

DOWNLOADER_MIDDLEWARES = {
    'ContentSpider.middlewares.SeleniumMiddleware': 500,
    'ContentSpider.middlewares.RandomUserAgent': 543,
    'ContentSpider.middlewares.ProxyMiddleware': 550,
}
KEYWORDS = ['iPad']

MAX_PAGE = 100

SELENIUM_TIMEOUT = 10
CHROME_OPTIONS = ['lang=zh_CN.UTF-8', "--headless", "--disable-gpu"]
SERVICE_ARGS = ['--disk-cache=true']
LOAD_IMAGE = True
WINDOW_HEIGHT = 900
WINDOW_WIDTH = 900
# 内容池接口用于接收扒取的内容
TARGET = 'http://tiyupc.com/api.php/web/index/scrapyd_content_store'
# 本地储存路劲
STORAGE_PATH = 'E:/Company/WorkPlace/system/images/'
# 图片发送路径
STORAGE_SERVER_API = 'http://tiyu88.junjs.cn/api.php/web/index/scrayd_image_store'
