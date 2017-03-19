# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oneverse', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='verse',
            options={'ordering': ['-created']},
        ),
        migrations.RenameField(
            model_name='verse',
            old_name='push_datetime',
            new_name='created',
        ),
    ]
