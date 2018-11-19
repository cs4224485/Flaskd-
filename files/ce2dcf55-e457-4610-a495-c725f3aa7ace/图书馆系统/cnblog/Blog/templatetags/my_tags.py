# Author: harry.cai
# DATE: 2018/7/2

from django import template
from Blog import models
from django.db.models import Count
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag('classfication.html')
def get_classification_style(user_obj):
    user_blog = user_obj.blog
    category_List = models.Category.objects.filter(blog=user_blog).values("pk").annotate(
        c=Count('article')).values('title', 'c')
    tag_list = models.Tag.objects.filter(blog=user_blog).values("pk").annotate(
        c=Count("article")).values("title", 'c')
    data_list = models.Article.objects.filter(user=user_obj).extra(
        select={"y_m_d_date": "strftime('%%Y-%%m-%%d', create_time)"}).values(
        "y_m_d_date").annotate(c=Count("nid")).values("y_m_d_date", 'c')

    return {"category_List": category_List, "tag_list": tag_list, "data_list": data_list, "user_obj": user_obj}


def recursion(children_list):
    html = ''
    for cv in children_list:
        b = '''
             <div class="comment_box" id={id}>
                                    <div class="comment_content">
                                        <a class="pull-right">删除</a>
                                        <a class="pull-right" username="{user}" pid="{id2}" id="replay_btn">回复</a>
                                        {content}
                                    </div>
           
        '''.format(id=cv['nid'],
                   user=cv['user'],
                   id2=cv['nid'],
                   content=cv['content']
                   )

        b += recursion(cv['children'])
        b += "</div>"
        html += b

    return html


@register.simple_tag
def create_tree(comment_list):
    html = '''
           <li  class="comment_item">
             
                
    '''
    for v in comment_list:

        a = '''
                                <div class="comment_info" style="margin-top: 10px">
                                    <a href="">{create_time}</a>
                                    <a href="">{user}</a>
                                    <a class="pull-right">删除</a>
                                    <a class="pull-right" username="{user2}" pid="{id}" id="replay_btn">回复</a>
                                </div>
                                <div class="comment_box" id={id2}>
                                    <div class="comment_content">{content}</div>
        '''.format(
            create_time=v['create_time'],
            user=v['user'],
            user2=v['user'],
            id=v['nid'],
            id2=v['nid'],
            content=v['content']
        )

        a += recursion(v['children'])
        a += "</div></li>"
        html += a

    return mark_safe(html)
