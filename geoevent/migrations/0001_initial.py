# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='Title', max_length=500)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('lat', models.FloatField(verbose_name='Latitude', blank=True, null=True)),
                ('lon', models.FloatField(verbose_name='Longitude', blank=True, null=True)),
                ('location', models.CharField(verbose_name='Address', max_length=1024)),
                ('url', models.URLField(verbose_name='URL', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('due', models.DateTimeField(blank=True, null=True)),
                ('dstart', models.DateTimeField(blank=True, null=True)),
                ('dend', models.DateTimeField(blank=True, null=True)),
                ('approved', models.BooleanField(default=False, verbose_name='Approved')),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('event_type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('display_user_name', models.CharField(blank=True, max_length=255)),
                ('avatar_url', models.CharField(default='', blank=True, max_length=200)),
                ('localization', models.CharField(default='en', max_length=10)),
                ('url', models.URLField(verbose_name='URL', blank=True)),
                ('show', models.BooleanField(default=False, verbose_name='Show')),
                ('location', models.CharField(verbose_name='Address', blank=True, max_length=500)),
                ('lat', models.FloatField(verbose_name='Latitude', blank=True, null=True)),
                ('lon', models.FloatField(verbose_name='Longitude', blank=True, null=True)),
                ('banned', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('tos_accepted', models.BooleanField(default=False)),
                ('institution', models.BooleanField(default=False)),
                ('verified', models.BooleanField(default=False)),
                ('bio', models.TextField(verbose_name='BIO', blank=True)),
                ('specialization', models.CharField(verbose_name='Specialization', blank=True, max_length=150)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.DO_NOTHING)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(to='geoevent.EventType', related_name='event', null=True, on_delete=models.DO_NOTHING),
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', help_text='A comma-separated list of tags.', blank=True, verbose_name='Tags', through='taggit.TaggedItem'),
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='events', null=True, on_delete=models.DO_NOTHING),
        ),
    ]
