# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-13 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_deliverylog_delivery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='delivery_date',
            field=models.DateField(),
        ),
    ]
