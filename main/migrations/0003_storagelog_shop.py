# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-26 15:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_storagelogtype_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='storagelog',
            name='shop',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.Shop'),
            preserve_default=False,
        ),
    ]
