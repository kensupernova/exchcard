# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oneverse', '0004_auto_20160319_2318'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='verse',
            options={'ordering': ['-push_date']},
        ),
        migrations.AddField(
            model_name='verse',
            name='detail',
            field=models.TextField(default=None, null=True),
        ),
    ]
