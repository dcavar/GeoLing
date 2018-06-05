# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geoevent', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(null=True, verbose_name='Description', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='url',
            field=models.URLField(null=True, verbose_name='URL', blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='display_user_name',
            field=models.CharField(null=True, max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(null=True, max_length=500, verbose_name='Address', blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='url',
            field=models.URLField(null=True, verbose_name='URL', blank=True),
        ),
    ]
