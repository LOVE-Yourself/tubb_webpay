# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-27 21:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to='teacher/%Y/%m', verbose_name='教练头像'),
        ),
    ]