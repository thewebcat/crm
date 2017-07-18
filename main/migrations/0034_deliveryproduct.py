# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-18 22:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_deliverystatus_label'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Delivery')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Storage')),
            ],
        ),
    ]