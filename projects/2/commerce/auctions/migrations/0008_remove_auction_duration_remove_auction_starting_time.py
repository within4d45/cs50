# Generated by Django 4.1.4 on 2022-12-19 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_comment_delete_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='auction',
            name='starting_time',
        ),
    ]
