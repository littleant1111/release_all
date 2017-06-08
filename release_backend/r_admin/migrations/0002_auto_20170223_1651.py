# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 08:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('r_admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('remark', models.CharField(blank=True, max_length=50)),
                ('env_child', models.ManyToManyField(to='r_admin.env_child')),
            ],
        ),
        migrations.AlterField(
            model_name='env',
            name='remark',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
