# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-09-26 11:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=10, verbose_name='昵称')),
                ('uimg', models.ImageField(upload_to='static/touxiang', verbose_name='头像')),
                ('uphone', models.CharField(max_length=20, verbose_name='手机号')),
                ('upwd', models.CharField(max_length=20, verbose_name='密码')),
                ('ucoin', models.IntegerField(max_length=9, verbose_name='金币')),
                ('isActiv', models.BooleanField(default=True, verbose_name='激活')),
            ],
        ),
    ]