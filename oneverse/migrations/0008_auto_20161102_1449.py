# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oneverse', '0007_serect'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Serect',
            new_name='Secret',
        ),
    ]
