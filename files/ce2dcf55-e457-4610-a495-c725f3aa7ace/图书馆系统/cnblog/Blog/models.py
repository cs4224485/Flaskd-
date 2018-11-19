from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserInfo(AbstractUser):
    '''
    用户信息表
    '''
    nid = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=11, null=True, unique=True)
    avatar = models.FileField(upload_to='avatar/', default='avatar/default.jpg')
    email = models.EmailField(unique=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    blog = models.ForeignKey(to='Blog', to_field='nid', null=True, on_delete=True)

    def __str__(self):
        return self.username


class Blog(models.Model):
    '''
    用户个人站点博客
    '''
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site_name = models.CharField(verbose_name='站点名称', max_length=64)
    theme = models.CharField(verbose_name='博客主体', max_length=32
                             )

    def __str__(self):
       return self.title


class Category(models.Model):
    '''
    文章分类
    '''
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
    blog = models.ForeignKey(to='Blog', to_field='nid', on_delete=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    '''
    文章标签
    '''
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签标题', max_length=32)
    blog = models.ForeignKey(to='Blog', to_field='nid', on_delete=True)

    def __str__(self):
        return self.title


class Article(models.Model):
    '''
    文章信息表
    '''
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题', max_length=32)
    summary = models.CharField(max_length=128)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    content = models.TextField()
    category = models.ForeignKey(to='Category', to_field='nid', on_delete=True)
    tags = models.ManyToManyField(
        to='Tag',
        through='Article2Tag',
        through_fields=(('article', 'tag'))
    )
    user = models.ForeignKey(to='UserInfo', to_field='nid', on_delete=True)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    read_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Article2Tag(models.Model):
    '''
    文章与tag多对多映射
    '''
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章', to='Article', to_field='nid', on_delete=True)
    tag = models.ForeignKey(verbose_name='标签', to='Tag', to_field='nid', on_delete=True)

    class Meta:
            unique_together = [
                ('article', 'tag')
            ]


class ArticleUpDown(models.Model):
    '''
    文章点赞与踩灭表
    '''
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInfo', null=True, on_delete=True)
    article = models.ForeignKey(to='Article', to_field='nid', on_delete=True)
    is_up = models.BooleanField(default=True)


class Comment(models.Model):
    '''
    文章评论表
    '''
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid', on_delete=True)
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid', on_delete=True)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, on_delete=True)


