# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchcard', '0005_avatarphoto'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('card_photo', models.ImageField(upload_to=b'card_photos')),
                ('card_host', models.ForeignKey(related_name='photos_of_card', default=1, to='exchcard.Card')),
                ('owner', models.ForeignKey(related_name='cardphotos', to='exchcard.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='DianZan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('card_by_dianzan', models.ForeignKey(related_name='dianzans_of_card', default=1, to='exchcard.Card')),
                ('person_who_dianzan', models.ForeignKey(related_name='dianzans_by_person', default=1, to='exchcard.Profile')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='DianZanManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AlterField(
            model_name='avatarphoto',
            name='avatar',
            field=models.ImageField(upload_to=b'card_photos'),
        ),
        migrations.AlterField(
            model_name='avatarphoto',
            name='owner',
            field=models.ForeignKey(related_name='avatars', to='exchcard.Profile'),
        ),
    ]
