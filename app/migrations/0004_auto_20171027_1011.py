# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 02:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20171026_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='city_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='link_man',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='province_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='remark',
            field=models.CharField(default='', max_length=1024),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=1024),
        ),
    ]
