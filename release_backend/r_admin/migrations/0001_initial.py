# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 07:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='env',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('remark', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='env_child',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('envchild_name', models.CharField(max_length=24)),
                ('env_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='r_admin.env')),
            ],
        ),
    ]
