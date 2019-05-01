from django.contrib import admin
from django.conf.urls import include, url
from django.contrib.auth import views as login_views
from django.urls import path

urlpatterns = [
    url('admin/', admin.site.urls), #장고 내장 admin으로 매핑되는 url
    url('main/', include('main.urls')), #main 앱 urls로 매핑되는 url
    url('', login_views.LoginView.as_view(template_name='main/templates/registration/login.html'), name='Login')
]
