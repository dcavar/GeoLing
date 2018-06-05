# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geoevent', '0003_event_last_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='related_to',
            field=models.CharField(max_length=255, blank=True, null=True, verbose_name='RELATED-TO'),
        ),
        migrations.AddField(
            model_name='event',
            name='uid',
            field=models.CharField(max_length=255, blank=True, null=True, verbose_name='UID'),
        ),
    ]
