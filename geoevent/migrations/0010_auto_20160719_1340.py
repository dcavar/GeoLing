# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-19 17:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geoevent', '0009_auto_20160714_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='x_linguistlist_progdescr',
            field=models.TextField(),
        ),
    ]