# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-13 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_auto_20170113_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverystatus',
            name='label',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
