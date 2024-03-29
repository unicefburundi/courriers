# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2020-01-13 09:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courriers_app', '0011_remove_staff_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='function',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courriers_app.StaffPosition'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='mobile_phone_number',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='office_phone_number',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courriers_app.Section'),
        ),
    ]
