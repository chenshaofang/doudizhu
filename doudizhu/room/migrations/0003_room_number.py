# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-10-06 08:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0002_auto_20180926_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='number',
            field=models.IntegerField(default=0, null=True, verbose_name='人数'),
        ),
    ]