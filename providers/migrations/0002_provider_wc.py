# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-22 22:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='wc',
            field=models.TextField(default=datetime.datetime(2016, 3, 22, 22, 19, 16, 235942, tzinfo=utc), verbose_name='w3p config'),
            preserve_default=False,
        ),
    ]