import json
import datetime
import os
from bs4 import BeautifulSoup
from io import BytesIO
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
from django.http import JsonResponse
from django.core.mail import send_mail
from django.db.models import Count, F
from cnblog import settings
from Blog import models
from Blog.utils.handle_code import *
from Blog import blog_forms
from Blog.utils.filter import *
from Blog.utils.handle_page import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# Create your views here.


@ csrf_exempt
def login(request):
    '''
    通过auth组件进行登录验证
    :param request:
    :return:
    '''

    if request.method == 'GET':
        # 判断尝试登陆的次数，如果大于三次就要输入验证码了
        if request.session.get('loin_time'):
            return render(request, 'login.html')
        request.session['loin_time'] = 0
        return render(request, 'login.html')
    elif request.method == 'POST':
        response = {'state': False, 'user': '', 'msg': '', 'error_count': 0}
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if request.session['loin_time'] > 3:
            response['error_count'] = request.session['loin_time']
            check_code = request.POST.get('check_code')
            valid_code = request.session.get('valid_code')
            if check_code:
                if check_code.upper() != valid_code.upper():
                    response['msg'] = '验证码输入有误'
                    return HttpResponse(json.dumps(response))
            else:
                response['msg'] = '请输入验证码'
                return HttpResponse(json.dumps(response))
        if user:

            auth.login(request, user)
            response['state'] = True
            return JsonResponse(response)
        else:
            request.session['loin_time'] += 1
            response['error_count'] = request.session['loin_time']
            response['msg'] = '用户名或密码错误'

            return HttpResponse(json.dumps(response))


def register(request):
    '''
    通过ajax实现用户注册
    :param request:
    :return:
    '''
    response = {'state': False, 'error_msg':"", 'summary_error': ""}

    if request.is_ajax():
        form_obj = blog_forms.RegisterForm(request.POST)
        if form_obj.is_valid():
            username = form_obj.cleaned_data.get('username')
            password = form_obj.cleaned_data.get('password')
            Email = form_obj.cleaned_data.get('email')
            valid_code = form_obj.cleaned_data.get('check_code')
            avatar_obj = request.FILES.get('avatar')
            check_valid = request.session['valid_code']
            if valid_code == check_valid:
                extra = {}
                if avatar_obj:
                    extra["avatar"] = avatar_obj
                blog_obj = models.Blog.objects.create(
                    title="%s的博客" % username,
                    site_name="%s的个人站点" % username,
                    theme="default.css")

                models.UserInfo.objects.create_user(username=username, password=password, blog=blog_obj, email=Email, **extra)
                response['state'] = True
                return JsonResponse(response)
            else:
                response['summary_error'] = '验证码错误'
                return JsonResponse(response)
        else:

            response['error_msg'] = form_obj.errors
            return JsonResponse(response)
    elif request.method == 'GET':
        form_obj = blog_forms.RegisterForm()
        return render(request, 'register.html', {'form_obj': form_obj})


def get_code_img(request):
    """
    获取登录图片验证码
    :param request:
    :return:
    """
    code_obj = CheckCode()

    img, valid_code = code_obj.generation_img()
    f = BytesIO()
    img.save(f, "png")
    request.session['valid_code'] = valid_code
    code_img = f.getvalue()

    return HttpResponse(code_img)


def email_valid_code(request):
    '''
    获取注册邮箱验证码
    :param request:
    :return:
    '''

    response = {"state": False, "msg": ""}

    if request.method == 'POST':
        try_times = request.session.get('try_times', 0)
        last_send_time = request.session.get('last_send_time')
        if last_send_time:
            current_time = datetime.datetime.now()
            limit_time = datetime.datetime.strptime(request.session.get('limit_time'), '%Y-%m-%d %H:%M:%S')
            # 如果当前发送的时间小于限制的时间并且次数大于10次那么提示用户发送太过频繁
            if current_time < limit_time and request.session['try_times'] > 10:
                response['msg'] = ["发送的太过频繁"]
                return JsonResponse(response)
            # 如果已经超出了限制的时间那么尝试次数清空为0
            elif current_time > limit_time:
                request.session['try_times'] = 0
        email = request.POST.get('email')
        email_form = blog_forms.EmailForm(request.POST)
        if email_form.is_valid():
            code_ojb = CheckCode()
            valid_code = code_ojb.generation_code()
            # 给注册的邮箱发送验证码
            send_mail(
                "欢迎注册,请输入以下验证码",
                valid_code,
                settings.EMAIL_HOST_USER,
                [email]
            )
            current_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
            limit_time = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(minutes=10),'%Y-%m-%d %H:%M:%S')
            request.session['limit_time'] = limit_time
            request.session['last_send_time'] = current_time
            try_times += 1
            request.session['try_times'] = try_times
            request.session['valid_code'] = valid_code
            response['state'] = True
            return JsonResponse(response)
        else:
            response["msg"] = email_form.errors
            return JsonResponse(response)


def index(request):
    '''
    首页
    :param request:
    :return:
    '''
    if request.method == 'GET':
        category = models.Category.objects.all().distinct()
        article_count = models.Article.objects.all().count()
        current_page = int(request.GET.get('page', 1))
        page_obj = PageClass(current_page, article_count, 'index')
        article_list = models.Article.objects.all()[page_obj.db_start:page_obj.db_end]
        page_str = page_obj.str_page()
        return render(request, 'index.html', {
            'category': category,
            'article_list': article_list,
            'page_str': page_str
        }
                    )


def home_site(request, username, **kwargs):
    '''
    个人站点页面
    :param request:
    :param username:
    :param kwargs: 根据条件过滤出相应的文章类型
    :return:
    '''
    if request.method == "GET":
        user_obj = models.UserInfo.objects.filter(username=username).first()
        if not user_obj:
            return HttpResponse('404 not found')
        article_list = models.Article.objects.filter(user=user_obj)
        user_blog = user_obj.blog

        if article_list:
            if kwargs:
                condition = kwargs['condition']
                parm = kwargs['parm']
                if condition == 'category':
                    article_list = article_list.filter(category__title=parm)
                elif condition == 'tag':
                    article_list = article_list.filter(tags__title=parm)
                elif condition == 'archive':
                    year, month, day = parm.split("-")
                    article_list = article_list.filter(create_time__year=year,
                                                       create_time__month=month,
                                                       create_time__day=day)

            return render(request, "user_site.html", {
                "user_obj": user_obj,
                "user_blog": user_blog,
                "article_list": article_list
            })
        return render(request, "user_site.html", {"user_blog": user_blog})


def article_detail(request, username, article_id):
    '''
    文章详情页
    :param request:
    :param username:
    :param article_id:
    :return:
    '''
    if request.method == 'GET':
        user = models.UserInfo.objects.filter(username=username).first()

        article_obj = user.article_set.filter(nid=article_id).first()
        comment_set = models.Comment.objects.filter(article_id=article_id)
        comment_list =[]
        for row in comment_set:
            row_dic ={
                'nid': row.nid,
                'user': row.user.username,
                'create_time': row.create_time,
                'content': row.content,
                'parent_comment_id': row.parent_comment_id
            }
            comment_list.append(row_dic)
        ret = []

        # 获取评论 构建树形数据结构
        comment_dic = {}

        for row in comment_list:
            row.update({'children': []})
            comment_dic[row['nid']] = row

        for item in comment_list:
            current_row = item
            current_row_parent_id = current_row['parent_comment_id']
            if not current_row_parent_id:
                ret.append(item)
            else:
                comment_dic[current_row_parent_id]['children'].append(current_row)

        return render(request, 'article_detail.html', {"article_obj": article_obj,
                                                       'user_obj': user,
                                                       'comment':  ret
                                                       })


def dig(request):
    '''
    点赞与踩灭功能
    :param request:
    :return:
    '''
    if request.method == 'POST':
        is_up = json.loads(request.POST.get("is_up"))
        article_id = request.POST.get('article_id')
        user_id = request.user.pk
        up_down_obj = models.ArticleUpDown.objects.filter(article_id=article_id, user=user_id).first()
        response = {"state": True, "is_up": None}
        if not up_down_obj:
            models.ArticleUpDown.objects.create(article_id=article_id, user_id=user_id, is_up=is_up)
            if is_up:
                models.Article.objects.filter(pk=article_id).update(up_count=F("up_count")+1)
            else:
                models.Article.objects.filter(pk=article_id).update(down_count=F("down_count") + 1)
        else:
            response['state'] = False
            response['is_up'] = up_down_obj.is_up
        return JsonResponse(response)


def comment(request):
    '''
    评论功能 实现对文章进行评论
    :param request:
    :return:
    '''
    response = {'user': "", "content": "", "create_time": ""}
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        content = request.POST.get('content')
        pid = request.POST.get('pid')
        user_id = request.user.pk
        comment_obj = models.Comment.objects.create(article_id=article_id, content=content, parent_comment_id=pid, user_id=user_id)
        if not pid:
            models.Article.objects.filter(nid=article_id).update(comment_count=F("comment_count")+1)
        response['user'] = request.user.username
        response['content'] = comment_obj.content
        response['create_time'] = datetime.datetime.strftime(comment_obj.create_time, '%Y-%m-%d %H:%M:%S')
        response['id'] = comment_obj.nid
    return JsonResponse(response)


@login_required
def background(request):
    '''
    后台管理页面
    :param request:
    :return:
    '''
    if request.method == 'GET':
        user_id = request.user.pk
        article_list = models.Article.objects.filter(user_id=user_id)
        return render(request, 'background.html',{
            "article_list":article_list
        })


@login_required
def add_article(request):
    '''
    添加新的文章
    :param request:
    :return:
    '''
    user_obj = models.UserInfo.objects.filter(username=request.user.username).first()
    blog = user_obj.blog
    category_list = models.Category.objects.filter(blog=blog)
    tag_list = models.Tag.objects.filter(blog=blog)
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category = request.POST.get('category')
        tag = request.POST.get('tag')
        content = filter_js(content)
        summary = content.text[0:150]

        models.Article.objects.create(title=title, summary=summary, content=str(content), user=request.user, category_id=category)
    return render(request, 'add_article.html', {'category_list': category_list, 'tag_list': tag_list})


def edit_article(request, article_id):
    user_obj = models.UserInfo.objects.filter(username=request.user.username).first()
    blog = user_obj.blog
    category_list = models.Category.objects.filter(blog=blog)
    tag_list = models.Tag.objects.filter(blog=blog)
    article = models.Article.objects.filter(nid=article_id)
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category = request.POST.get('category')
        tag = request.POST.get('tag')
        content = filter_js(content)
        summary = content.text[0:150]
        article.update(title=title, summary=summary,content=str(content), user=request.user, category_id=category)
        return redirect('/background/')
    article_obj = article.first()
    return render(request, 'edit_article.html', {
        'category_list': category_list,
        'tag_list': tag_list,
        'article_obj': article_obj})


def upload(request):
    """
    上传文件
    :param request:
    :return:
    """
    if request.method == "POST":
        img = request.FILES.get("upload_img")
        path = os.path.join(settings.MEDIA_ROOT, "add_article_img", img.name)
        with open(path, 'wb') as f:
            for line in img:
                f.write(line)

        response = {
            "error": 0,
            "url": "media/add_article_img/%s" % img.name
        }

        return HttpResponse(json.dumps(response))


def logout(request):
    '''
    账户登出
    :param request:
    :return:
    '''
    auth.logout(request)
    return redirect("/index/")


def delete_article(request, article_id):
    if request.method == 'POST':
        models.Article.objects.filter(nid=article_id)
        return redirect("/background/")