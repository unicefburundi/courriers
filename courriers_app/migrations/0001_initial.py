# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-30 10:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.ImageField(upload_to=b'')),
                ('received_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MailType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail_type_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Sender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=100)),
                ('phone_number', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('office_phone_number', models.CharField(max_length=20)),
                ('mobile_phone_number', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='StaffPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('purpose', models.CharField(max_length=100)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('mail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courriers_app.Mail')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courriers_app.Staff')),
            ],
        ),
        migrations.AddField(
            model_name='staff',
            name='function',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courriers_app.StaffPosition'),
        ),
        migrations.AddField(
            model_name='staff',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courriers_app.Section'),
        ),
        migrations.AddField(
            model_name='mail',
            name='mail_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courriers_app.MailType'),
        ),
        migrations.AddField(
            model_name='mail',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courriers_app.Sender'),
        ),
    ]