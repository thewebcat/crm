# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-29 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20161229_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='is_custom_price',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='delivery',
            name='is_custom_product',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='custom_price',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
