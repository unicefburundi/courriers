# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2020-04-10 10:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('binome', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notavailable',
            name='staff',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='courriers_app.Staff'),
        ),
    ]