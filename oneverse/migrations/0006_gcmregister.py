# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oneverse', '0005_auto_20160324_0932'),
    ]

    operations = [
        migrations.CreateModel(
            name='GcmRegister',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('gcmToken', models.CharField(default=None, max_length=255)),
                ('deviceId', models.CharField(default=None, max_length=100)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
