# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2020-04-10 08:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courriers_app', '0015_track_soft_copy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Binome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='the_selecter', to='courriers_app.Staff')),
                ('staff_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='the_selected', to='courriers_app.Staff')),
            ],
        ),
        migrations.CreateModel(
            name='NotAvailable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courriers_app.Staff')),
            ],
        ),
    ]
