# Author: harry.cai
# DATE: 2018/6/7
from library.models import *


def get_book_info(req):
    '''
    获取添加或更新书籍的信息
    :param req:
    :return:
    '''
    info_dic = {
        'title': req.POST.get('title'),
        'price': req.POST.get('price'),
        'pub_date': req.POST.get('pub_date'),
        'author': req.POST.get('author'),
        'change_author': req.POST.get('change_author'),
        'publish': req.POST.get('publish')
    }
    author = Author.objects.filter(name=info_dic['author']).first()
    if not author and info_dic['author'] != '':
        author = Author.objects.create(name=info_dic['author'])
    publish_obj = Publish.objects.filter(name=info_dic['publish']).first()

    return info_dic, author, publish_obj


def get_author_info(req):
    '''
    获取添加或更新作者的信息
    :param req:
    :return:
    '''
    info_dic = {
        'name': req.POST.get('name'),
        'age': req.POST.get('age'),
        'sex': req.POST.get('sex'),
        'tel': req.POST.get('tel'),
        'addr': req.POST.get('addr'),
    }

    return info_dic


def get_publish_info(req):
    '''
    获取添加或更新出版社的信息
    :param req:
    :return:
    '''
    info_dic = {
        'name': req.POST.get('name'),
        'city': req.POST.get('city'),
        'email': req.POST.get('email')

    }
    return info_dic
