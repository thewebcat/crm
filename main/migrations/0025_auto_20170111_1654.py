# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-11 13:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_auto_20170111_1601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storage',
            name='count',
        ),
        migrations.AddField(
            model_name='storagelog',
            name='storage',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='main.Storage'),
            preserve_default=False,
        ),
    ]
