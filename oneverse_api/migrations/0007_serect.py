# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oneverse_api', '0006_gcmregister'),
    ]

    operations = [
        migrations.CreateModel(
            name='Serect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('api_key', models.CharField(default=None, max_length=100)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
