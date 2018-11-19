from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=24)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    pub_date = models.DateField()

    # 与出版社表建立多对关系
    publish = models.ForeignKey(to='Publish',to_field='id',on_delete=True)
    authors = models.ManyToManyField(to='Author')

    def __str__(self):
        return self.title


class Publish(models.Model):
    name = models.CharField(max_length=24)
    city = models.CharField(max_length=24)
    email = models.EmailField()


class Author(models.Model):
    name = models.CharField(max_length=24)
    sex = models.CharField(max_length=10,default='man')
    age = models.IntegerField(null=True)
    author_detail = models.OneToOneField(to="AuthorDetail",on_delete=True, null=True)


class AuthorDetail(models.Model):
    birthday = models.DateField(null=True)
    telephone = models.BigIntegerField()
    addr = models.CharField(max_length=64)


