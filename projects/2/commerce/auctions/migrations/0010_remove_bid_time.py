# Generated by Django 4.1.4 on 2022-12-19 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auction_open'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='time',
        ),
    ]
