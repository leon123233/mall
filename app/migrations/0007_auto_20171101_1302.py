# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 05:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20171030_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='display_pic',
            field=models.ImageField(upload_to='img'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='display_pic',
            field=models.ImageField(upload_to='img'),
        ),
    ]
