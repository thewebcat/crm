# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-09 18:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_delivery_delivery_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Delivery')),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='deliverylist',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.DeliveryStatus'),
        ),
    ]