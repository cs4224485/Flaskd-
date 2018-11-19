"""cnblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from cnblog import settings
from Blog import views

urlpatterns = [
    re_path(r"media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    path('admin/', admin.site.urls),
    # 登录注册
    path('login/', views.login),
    path('register/', views.register),
    # 登出
    path('logout/', views.logout),
    # 获取验证码
    path('get_code_img/', views.get_code_img),
    # 点赞
    path("dig/", views.dig),
    # 首页
    path("index/", views.index),
    re_path(r"^$", views.index),
    # 获取邮箱注册验证码
    path('email_valid_code/', views.email_valid_code),
    # 评论
    path('comment/', views.comment),
    # 上传
    path('upload/', views.upload),
    # 后台管理
    path('background/', views.background),
    path('add_article/', views.add_article),
    re_path("edit_article/(\w+)", views.edit_article),
    re_path("delete_article/(\w+)",views.delete_article),
    # 个人博客页面
    re_path("(?P<username>\w+)/articles/(?P<article_id>\d+)", views.article_detail),
    re_path("(?P<username>\w+)/(?P<condition>tag|category|archive)/(?P<parm>.*)$", views.home_site),
    re_path("(?P<username>\w+)/", views.home_site),


]
