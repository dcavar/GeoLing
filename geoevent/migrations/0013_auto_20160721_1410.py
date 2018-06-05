# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-21 18:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geoevent', '0012_auto_20160720_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adr',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adrs', to='geoevent.Contact'),
        ),
    ]