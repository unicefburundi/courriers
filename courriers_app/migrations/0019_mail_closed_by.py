# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2021-09-07 18:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courriers_app', '0018_auto_20210905_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='closed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courriers_app.Staff'),
        ),
    ]
