# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 03:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20171101_1302'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appconfig',
            old_name='webchat_pay_id',
            new_name='wechat_pay_id',
        ),
        migrations.AlterField(
            model_name='category',
            name='key',
            field=models.CharField(help_text='key', max_length=255),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='\u5546\u54c1\u7c7b\u522b', max_length=255),
        ),
    ]
