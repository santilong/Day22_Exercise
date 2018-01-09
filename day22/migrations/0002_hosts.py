# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-06 13:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('day22', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='hosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=32)),
                ('ip', models.GenericIPAddressField(unique=True)),
                ('port', models.IntegerField(max_length=5)),
            ],
        ),
    ]