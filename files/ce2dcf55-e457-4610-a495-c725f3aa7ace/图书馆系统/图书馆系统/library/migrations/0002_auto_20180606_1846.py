# Generated by Django 2.0.5 on 2018-06-06 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='publish_date',
            new_name='pub_date',
        ),
    ]
