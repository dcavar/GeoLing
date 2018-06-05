# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geoevent', '0005_auto_20151209_1057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='addresses',
        ),
        migrations.AddField(
            model_name='address',
            name='profiles',
            field=models.ManyToManyField(to='geoevent.Profile', related_name='addresses'),
        ),
    ]
