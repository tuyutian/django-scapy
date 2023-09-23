from django.urls import path

from . import views

app_name = 'spider'
urlpatterns = [
    # ex: /spiders/
    path('', views.index, name='index'),
    # ex: /spiders/article/1
    path('spiderInfo/<int:pk>/', views.detail, name='detail'),
    # ex: /spiders/article/1/results/
    path('article/<int:pk>/results/', views.results, name='results'),
    # ex: /spiders/launch
    path('launch', views.api_launch, name='launch'),
    path('daemonstatus', views.scrapy_daemonstatus, name='daemonstatus'),
    path('store',views.spider_store,name='store')
]