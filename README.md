pip install -r requirements.txt
# x-www-form-urlencoded
# post
# url = http://127.0.0.1:8000/spider/scrapy
# 运行环境 scrapyd,scrapydweb,django,logparser,selenium windows下需要安装pywin32,chromedriver.exe已放于根目录
1. 修改ContentSpider/ContentSpider和ContentSystem/scrapy_site下的settings文件
2. 运行命令
  一定要进入进入 ContentSpider  : scrapyd
3. ContentSystem py manage.py runserver
4. 进入ContentSpider: scraydweb
5. 进入 ContentSpider  : logparser  -dir E:/xxx/scrapy_site/ContentSpider/logs
6. 还有两个setting文件的绝对路径



# postman参数json示例
`{
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
}`