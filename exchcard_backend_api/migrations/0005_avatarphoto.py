# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchcard_backend_api', '0004_auto_20160318_2315'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvatarPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar', models.ImageField(max_length=254, upload_to=b'card_photos')),
                ('owner', models.ForeignKey(related_name='avatar', to='exchcard_backend_api.Profile')),
            ],
        ),
    ]
