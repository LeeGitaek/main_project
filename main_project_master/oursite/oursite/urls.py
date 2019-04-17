"""
메인 urls, 프로젝트 관리를 위한 url 정의이다
앱별로 url 정의를할 수 있음
"""
from django.contrib import admin
from django.conf.urls import include,url
from django.urls import path


urlpatterns = [
    url('admin/', admin.site.urls), #장고 내장 admin으로 매핑되는 url
    url('main/', include('main.urls')), #main 앱 urls로 매핑되는 url

    #url('accounts/', include('accounts.urls')), #accounts 앱 urls로 매핑되는 url
]
