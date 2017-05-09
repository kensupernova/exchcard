# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchcard_backend_api', '0006_auto_20160529_2126'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DianZanManager',
        ),
        migrations.AlterModelOptions(
            name='dianzan',
            options={'ordering': ['-created']},
        ),
        migrations.AlterField(
            model_name='cardphoto',
            name='owner',
            field=models.ForeignKey(related_name='cardphotos_of_profile', to='exchcard_backend_api.Profile'),
        ),
    ]
