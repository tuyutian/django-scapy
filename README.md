运行pip install -r requirements.txt


### 运行环境 
* scrapyd
* scrapydweb
* django
* logparser
* selenium 

windows下需要安装pywin32,chromedriver.exe已放于根目录

配置项修改ContentSpider/ContentSpider和ContentSystem/scrapy_site下的settings文件

* 运行命令
  一定要进入进入 ContentSpider目录执行： `scrapyd`
* 在 ContentSystem目录执行 `py manage.py runserver`
* 在 ContentSpider目录执行 `scraydweb`
* 在 ContentSpider目录执行 `logparser  -dir E:/xxx/scrapy_site/ContentSpider/logs`
* 还有两个setting文件分别是爬虫和django的配置文件，其中的绝对路径配置项需要修改 `ContentSpider/ContentSpider/settings.py`和`ContentSystem/scrapy_site/settings.py`
### 备忘
* scrapyd的中间件中有模拟向下滚动操作
* admin_spider文件中有自动翻页操作
* 图片使用管道pipelines处理先存放在本地再发送的云存储，云存储路径在settings中
* 内容也会通过接口发送，路径也在settings中，本地数据库也会存一份，由django部分migrations中数据表可见结构
* 设置文件可以调节管道并发以及代理
### 运行流程：
1. 通过给定网页链接，指定每个部分的xpath匹配规则进行批量爬取数据，以下示例来自新浪新闻
   #x-www-form-urlencoded
   #post
   #url = http://127.0.0.1:8000/spider/scrapy
# postman参数json示例

```json{
  "add_time": "2020-04-22",
  "allowed_domains": " ",
  "cate_id": 4,
  "charset": "uft-8",
  "id": 1,
  "list_xpath": " .//u/li/a/@href",
  "rules": [
    {
      "match": ".//h1[@class=\"main-title\"]/text()",
      "name": "title"
    },
    {
      "key": 1587637191655,
      "match": ".//div[@class=\"date-source\"]/a[@class=\"source ent-source\"]/text()",
      "name": "author",
      "value": ""
    },
    {
      "key": 1587637233828,
      "match": ".//div[@class=\"channel-path\"]/a[2]/text()",
      "name": "tag",
      "value": ""
    },
    {
      "key": 1587637245922,
      "match": ".//div[@id=\"artibody\"]",
      "name": "content",
      "value": ""
    },
    {
      "key": 1587637281180,
      "match": ".//div[@class=\"date-source\"]/span[@class=\"date\"]/text()",
      "name": "create_time",
      "value": ""
    }
  ],
  "spider_name": "新浪体育中超列表爬虫",
  "start_urls": "http://sports.sina.com.cn/csl/",
  "update_time": "2020-04-22",
  "url_contain": " ",
  "url_no_contain": " ",
  "url_type": 1
}
```