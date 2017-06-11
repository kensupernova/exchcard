# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchcard', '0002_auto_20170611_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='sent_time',
            field=models.BigIntegerField(default=1497151861574),
        ),
        migrations.AlterField(
            model_name='dianzan',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
