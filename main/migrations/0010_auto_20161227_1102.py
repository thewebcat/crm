# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-27 08:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20161227_1051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('comment', models.CharField(max_length=255)),
            ],
        ),
        migrations.RenameField(
            model_name='delivery',
            old_name='custom_deliveryprice',
            new_name='delivery_fromclient',
        ),
        migrations.AddField(
            model_name='delivery',
            name='delivery_price',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='delivery',
            name='courier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Courier'),
        ),
    ]
