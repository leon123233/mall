# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 07:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20171027_1049'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='user_id',
            new_name='remark',
        ),
        migrations.AddField(
            model_name='appconfig',
            name='wechat_pay_secret',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='price',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.WechatUser'),
            preserve_default=False,
        ),
    ]
