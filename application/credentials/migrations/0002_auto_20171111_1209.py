# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-11-11 04:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credentials', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='oauthuser',
            name='address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='oauthuser',
            name='idCard',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='oauthuser',
            name='phone',
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='oauthuser',
            name='sex',
            field=models.IntegerField(choices=[(0, '\u7537'), (1, '\u5973'), (2, '\u5176\u4ed6')], default=0),
        ),
    ]
