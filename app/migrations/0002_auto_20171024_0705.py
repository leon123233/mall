# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-24 07:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_domain', models.CharField(max_length=255)),
                ('key', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('c_type', models.CharField(max_length=255)),
                ('icon', models.CharField(max_length=255)),
            ],
        ),
        migrations.RenameField(
            model_name='picture',
            old_name='display_pic',
            new_name='name',
        ),
        migrations.AddField(
            model_name='goods',
            name='number_order',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='goods',
            name='stores',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='picture',
            name='pic',
            field=models.ImageField(default='', upload_to='img'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='goods',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Category'),
        ),
    ]