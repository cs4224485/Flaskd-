# Generated by Django 2.0.5 on 2018-06-20 09:39

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='文章标题')),
                ('summary', models.CharField(max_length=128)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Article2Tag',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('article', models.ForeignKey(on_delete=True, to='Blog.Article', verbose_name='文章')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleUpDown',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('is_up', models.BooleanField(default=True)),
                ('article', models.ForeignKey(on_delete=True, to='Blog.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64, verbose_name='个人博客标题')),
                ('site_name', models.CharField(max_length=64, verbose_name='站点名称')),
                ('theme', models.CharField(max_length=32, verbose_name='博客主体')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='分类标题')),
                ('blog', models.ForeignKey(on_delete=True, to='Blog.Blog')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=255, verbose_name='评论内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('article', models.ForeignKey(on_delete=True, to='Blog.Article', verbose_name='评论文章')),
                ('parent_comment', models.ForeignKey(null=True, on_delete=True, to='Blog.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='标签标题')),
                ('blog', models.ForeignKey(on_delete=True, to='Blog.Blog')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('telephone', models.CharField(max_length=11, null=True, unique=True)),
                ('avatar', models.FileField(default='avatar/default.jpg', upload_to='avatar/')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('blog', models.ForeignKey(null=True, on_delete=True, to='Blog.Blog')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=True, to=settings.AUTH_USER_MODEL, verbose_name='评论者'),
        ),
        migrations.AddField(
            model_name='articleupdown',
            name='user',
            field=models.ForeignKey(null=True, on_delete=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article2tag',
            name='tag',
            field=models.ForeignKey(on_delete=True, to='Blog.Tag', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=True, to='Blog.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(through='Blog.Article2Tag', to='Blog.Tag'),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(on_delete=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='article2tag',
            unique_together={('article', 'tag')},
        ),
    ]
