import csv
import json
import re

import requests
from django.core import serializers
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.conf import settings
from .models import Spider,ApiContent


def index(request):
    latest_article_list = Spider.objects.order_by('spider_name')[:5]
    context = {
        'latest_article_list': latest_article_list,
    }
    return render(request, 'spider/index.html', context)


def detail(request, pk):
    spider = Spider.objects.get(id=pk)
    if spider:
        main_info = model_to_dict(spider)
        main_info['rules'] = json.loads(main_info['rules'])
    else:
        main_info = {}
    return JsonResponse(main_info, json_dumps_params={'ensure_ascii': False}, safe=False)


def spider_store(request):
    if request.method == "POST":
        post_data = request.body
        post_data = eval(post_data)
        post_data['rules'] = json.dumps(post_data['rules'])
        hasSpider = Spider.objects.filter(id=post_data['id']).first()
        if hasSpider:
            Spider.objects.filter(id=post_data['id']).update(**post_data)
        else:
            Spider.objects.create(**post_data)
        return JsonResponse({'code': 200, 'message': '保存成功'})
    else:
        return HttpResponseBadRequest(HttpResponse('请求方式错误！'))


def results(request, pk):
    response = "You're looking at the results of article %s."
    return HttpResponse(response % pk)


def api_launch(request):
    post_data = eval(request.body)
    api_list = {
        1: 'sync/weixin/account/articles_content',
        2: 'sync/weixin/data/combine/search_content',
        3: 'sync/weixin/data/hot/day_content',
        4: 'sync/weixin/data/hot/week_content',
        5: 'sync/weixin/data/hot/month_content',

    }
    api = api_list.get(post_data['spider_type'], 1)

    del post_data['spider_type']
    api = settings.NEWRANK_BASE_URL + api
    Key = settings.NEWRANK_KEY

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Key': Key
    }

    response = requests.post(api, headers=headers, data=post_data)
    body = json.loads(response.text)
    if body['code'] == 0:
        data = body['data']
        csvFile = open("newrank.csv", "w")
        file_header = ['name', 'account', 'type', 'author', 'orderNum', 'imageUrl', 'sourceUrl', 'musicUrl', 'audioUrl',
                       'updateTime', 'title', 'summary', 'publicTime', 'url', 'originalFlag', 'readNum', 'likeNum',
                       'content', 'keywords']
        dict_writer = csv.DictWriter(csvFile, file_header)
        dict_writer.writeheader()

        data_list = []
        # 之后，按照（属性：数据）的形式，将字典写入CSV文档即可
        for row in data:
            dict_writer.writerow(row)
            book = ApiContent(row)
            data_list.append(book)
        # 批量插入数据
        ApiContent.objects.bulk_create(data_list)
        csvFile.close()

    else:
        return JsonResponse(body, safe=False)


def scrapy_daemonstatus(request):
    response = requests.get('http://127.0.0.1:6800/daemonstatus.json')
    return JsonResponse(eval(response.text))
