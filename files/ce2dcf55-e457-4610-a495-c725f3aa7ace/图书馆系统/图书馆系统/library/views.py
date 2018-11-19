from django.shortcuts import render, redirect, HttpResponse
from library.models import *
from library.pub_func import *
# Create your views here.


def index(request):
    '''
    首页显示所有数据相关信息
    :param request:
    :return:
    '''
    book_obj = Book.objects.all()

    return render(request,'index.html', {'book_obj':book_obj})


def add_book(req):
    '''
    添加书籍
    :param req:
    :return:
    '''
    publish = Publish.objects.all()
    if req.method == "POST":
        # 将获取信息放到一个公共函数
        info_dic, author, publish_obj = get_book_info(req)
        book_obj = Book.objects.create(title=info_dic['title'], price=info_dic['price'], pub_date=info_dic['pub_date']
                            ,publish=publish_obj)
        book_obj.authors.add(author)
        return redirect('/index/')

    return render(req, "add_book.html", {'publish_obj': publish})


def delete_book(req, nid):
    '''
    删除书籍
    :param req:
    :param nid:
    :return:
    '''
    book_obj = Book.objects.filter(id=nid).first()
    if book_obj:
        book_obj.delete()
        return redirect('/index/')
    else:
        return HttpResponse('该书籍不存在')


def edit_book(req, nid):
    '''
    编辑书籍
    :param req:
    :param nid:
    :return:
    '''

    publish = Publish.objects.all()
    book = Book.objects.filter(id=nid)
    book_obj = book.first()
    authors = Author.objects.all().distinct()
    if req.method == 'POST':
        info_dic, author, publish_obj = get_book_info(req)
        book.update(title=info_dic['title'], price=info_dic['price'], pub_date=info_dic['pub_date']
                            ,publish=publish_obj)

        if info_dic["change_author"] != 'None':
            new_author = Author.objects.filter(name=info_dic['change_author']).first()
            book_obj.authors.clear()
            book_obj.authors.add(new_author)
        else:
            book_obj.authors.add(author)
        return redirect('/index/')

    return render(req, 'edit_book.html', locals())


def show_authors(req):
    '''
    显示所有作者信息
    :param req:
    :return:
    '''
    authors = Author.objects.all()

    return render(req, 'authors.html', {'authors': authors})


def author_detail(req, nid):
    '''
    展示作者详细信息
    :param req:
    :param nid:
    :return:
    '''

    author_obj = Author.objects.filter(id=nid).first()
    return render(req,'author_detail.html', locals())


def add_author(req):
    '''
    添加作者
    :param req:
    :return:
    '''
    if req.method == 'POST':
        info_dic = get_author_info(req)
        author_obj = Author.objects.all()
        detail = AuthorDetail.objects.create(telephone=info_dic['tel'], addr=info_dic['addr'])
        author_obj.create(name=info_dic['name'], age=info_dic['age'], sex=info_dic['sex'],author_detail=detail)
        return redirect('/index/')

    return render(req,'add_author.html', )


def delete_author(req, nid):
    '''
    删除作者
    :param req:
    :param nid:
    :return:
    '''
    author_obj = Author.objects.filter(id=nid)
    author_obj.delete()
    return redirect('/author/')


def edit_author(req, nid):
    '''
    编辑作者信息
    :param req:
    :param nid:
    :return:
    '''
    author = Author.objects.filter(id=nid)
    author_obj = author.first()
    if req.method == 'POST':
        info_dic = get_author_info(req)
        detail = AuthorDetail.objects.filter(id=author_obj.author_detail_id).update(telephone=info_dic['tel'], addr=info_dic['addr'])
        author.update(name=info_dic['name'], age=info_dic['age'], sex=info_dic['sex'])
        return redirect('/author/')
    return render(req, 'edit_author.html', locals())


def show_publish(req):
    publish_list = Publish.objects.all()
    return render(req, 'publish.html', locals())


def publish_detail(req, nid):
    publish_obj = Publish.objects.filter(id=nid).first()
    book_list = publish_obj.book_set.all()

    return render(req, 'publish_detail.html', locals())


def add_publish(req):
    '''
    添加出版社
    :param req:
    :return:
    '''
    if req.method == 'POST':
        info_dic = get_publish_info(req)
        Publish.objects.create(name=info_dic['name'], city=info_dic['city'], email=info_dic['email'])
        return redirect('/publish/')
    return render(req, 'add_publish.html')


def edit_publish(req,nid):
    '''
    编辑出版社
    :param req:
    :return:
    '''
    publish = Publish.objects.filter(id=nid)
    publish_obj = publish.first()
    if req.method == 'POST':
        info_dic = get_publish_info(req)
        publish.update(name=info_dic['name'], city=info_dic['city'], email=info_dic['email'])
        return redirect('/publish/')

    return render(req,'edit_publish.html', locals())


def delete_publish(req, nid):
    '''
    删除出版社
    :param req:
    :param nid:
    :return:
    '''
    publish_obj = Publish.objects.filter(id=nid).first()
    publish_obj.delete()
    return redirect('/publish/')