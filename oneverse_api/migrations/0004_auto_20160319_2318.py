# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oneverse_api', '0003_verse_push_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verse',
            name='push_date',
            field=models.DateField(default=None, null=True),
        ),
    ]
