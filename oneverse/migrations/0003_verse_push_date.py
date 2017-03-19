# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oneverse', '0002_auto_20160319_2314'),
    ]

    operations = [
        migrations.AddField(
            model_name='verse',
            name='push_date',
            field=models.DateField(default=None),
        ),
    ]
