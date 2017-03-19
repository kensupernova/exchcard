# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchcard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='arrived_date',
        ),
        migrations.RemoveField(
            model_name='card',
            name='fromaddress',
        ),
        migrations.RemoveField(
            model_name='card',
            name='sent_date',
        ),
        migrations.RemoveField(
            model_name='card',
            name='toaddress',
        ),
    ]
