# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geoevent', '0002_auto_20150729_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='last_modified',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
    ]
