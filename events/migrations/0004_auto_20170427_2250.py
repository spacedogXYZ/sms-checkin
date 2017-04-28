# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 22:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_participant_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='host_name',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.CharField(max_length=150, null=True),
        ),
    ]