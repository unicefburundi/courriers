# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-12-30 16:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courriers_app', '0010_auto_20191230_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='email',
        ),
    ]