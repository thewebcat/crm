# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-03 12:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20161229_2133'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum', models.IntegerField()),
                ('last_coming', models.DateTimeField()),
                ('own_shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Shop')),
            ],
        ),
        migrations.AlterField(
            model_name='delivery',
            name='time',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
