# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-28 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('percent', models.IntegerField()),
                ('enabled', models.BooleanField()),
            ],
        ),
    ]
