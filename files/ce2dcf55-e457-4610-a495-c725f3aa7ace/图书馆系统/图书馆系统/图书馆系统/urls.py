"""图书馆系统 URL Configuration

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
from django.urls import path,re_path
from library import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    re_path('^$', views.index),
    path('add_book/', views.add_book),
    re_path('([0-9]+)/delete/', views.delete_book),
    re_path('([0-9]+)/edit/', views.edit_book),
    re_path('([0-9]+)/author/', views.author_detail),
    path('author/', views.show_authors),
    path('add_author/', views.add_author),
    re_path('([0-9]+)/delete_author', views.delete_author),
    re_path('([0-9]+)/edit_author', views.edit_author),
    path('publish/', views.show_publish),
    re_path('([0-9]+)/publish/', views.publish_detail),
    path('add_publish/', views.add_publish),
    re_path('([0-9]+)/edit_publish/', views.edit_publish),
    re_path('([0-9]+)/delete_publish/', views.delete_publish)
]
