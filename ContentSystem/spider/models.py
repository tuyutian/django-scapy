from django.db import models

# Create your models here.
from django.db import models


class Spider(models.Model):
    charset = models.CharField(max_length=25, null=True)
    cate_id = models.PositiveIntegerField()
    url_type = models.PositiveSmallIntegerField()
    start_urls = models.TextField()
    allowed_domains = models.CharField(max_length=255, null=True, default='')
    list_xpath = models.CharField(max_length=255, null=True, default='')
    url_contain = models.CharField(max_length=100, null=True, default='')
    url_no_contain = models.CharField(max_length=100, null=True, default='')
    rules = models.TextField()
    spider_name = models.CharField(max_length=100)
    add_time = models.DateField(auto_now_add=True)
    update_time = models.DateField(auto_now=True)

    def __str__(self):
        return self.spider_name


class ApiContent(models.Model):
    name = models.CharField(max_length=255, null=True)
    account = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=50, null=True)
    author = models.CharField(max_length=100, null=True)
    orderNum = models.CharField(max_length=255, null=True)
    imageUrl = models.TextField(null=True)
    sourceUrl = models.TextField(null=True)
    musicUrl = models.TextField(null=True)
    audioUrl = models.TextField(null=True)
    updateTime = models.DateTimeField(null=True)
    title = models.CharField(max_length=255, null=True)
    summary = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255, null=True)
    originalFlag = models.CharField(max_length=255, null=True)
    readNum = models.CharField(max_length=255, null=True)
    likeNum = models.CharField(max_length=255, null=True)
    content = models.TextField(null=True)
    keywords = models.TextField(null=True)

    def __str__(self):
        return self.title
