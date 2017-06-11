# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchcard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dianzan',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='card',
            name='sent_time',
            field=models.BigIntegerField(default=1497149118738),
        ),
    ]
