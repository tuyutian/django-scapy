import json
import requests
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse


def index(request):
    if request.method == "POST":
        post_data = request.body
        post_data = eval(post_data)
        fire_spider(params=post_data)
        return JsonResponse({'code': 200, 'message': '爬虫启动中>>>>>>'})
    else:
        return HttpResponseBadRequest(HttpResponse('请求方式错误！'))


# 发动爬虫的方法
def fire_spider(params):
    # 通过请求调用scrapyd服务器上的爬虫运行。
    print(params)
    url = 'http://127.0.0.1:6800/schedule.json'
    data = {
        'project': 'ContentSpider',
        'spider': 'admin_spider',
        'params': json.dumps(params),
    }
    # 发送请求调度爬虫运行。
    response = requests.post(url, data)
    if response.status_code == 200:
        print(json.dumps(response.text))
