# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-11 13:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_auto_20170111_1554'),
    ]

    operations = [
        migrations.RenameField(
            model_name='delivery',
            old_name='cash_id_transaction_id',
            new_name='cash_in_transaction_id',
        ),
        migrations.RenameField(
            model_name='delivery',
            old_name='storage_id_transaction_id',
            new_name='storage_in_transaction_id',
        ),
    ]
