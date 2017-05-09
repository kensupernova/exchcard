# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchcard_backend_api', '0002_auto_20160313_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='has_arrived',
            field=models.BooleanField(default=False),
        ),
    ]
