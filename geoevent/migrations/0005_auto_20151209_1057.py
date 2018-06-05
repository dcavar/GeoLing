# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geoevent', '0004_auto_20150805_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('location', models.CharField(null=True, verbose_name='Address', blank=True, max_length=500)),
                ('lat', models.FloatField(null=True, verbose_name='Latitude', blank=True)),
                ('lng', models.FloatField(null=True, verbose_name='Longitude', blank=True)),
                ('url', models.URLField(null=True, verbose_name='URL', blank=True)),
                ('label', models.CharField(null=True, verbose_name='Label', blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('lat', models.FloatField(null=True, verbose_name='Latitude', blank=True)),
                ('lng', models.FloatField(null=True, verbose_name='Longitude', blank=True)),
                ('url', models.URLField(null=True, verbose_name='URL', blank=True)),
                ('label', models.CharField(null=True, verbose_name='Label', blank=True, max_length=255)),
                ('event', models.ForeignKey(to='geoevent.Event', related_name='locations', on_delete=models.DO_NOTHING)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='lon',
        ),
        migrations.AddField(
            model_name='profile',
            name='addresses',
            field=models.ManyToManyField(related_name='profiles', to='geoevent.Address'),
        ),
    ]
