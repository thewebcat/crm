# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-11 11:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20170109_2358'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type_code', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='cash',
            name='cash_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.CashType'),
            preserve_default=False,
        ),
    ]