# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b' ', max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('postcode', models.CharField(default=b'111111', max_length=100)),
            ],
            options={
               'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('card_name', models.CharField(default=None, max_length=50)),
                ('sent_time', models.BigIntegerField(default=0)),
                ('sent_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('arrived_time', models.BigIntegerField(default=0)),
                ('arrived_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('fromaddress', models.ForeignKey(related_name='from_addresses', default=None, to='exchcard_backend_api.Address')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='DetailedAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address_first_line', models.CharField(default=b' ', max_length=255)),
                ('address_second_line', models.CharField(default=b' ', max_length=255)),
                ('address_third_line', models.CharField(default=b' ', max_length=255)),
                ('city', models.CharField(default=b' ', max_length=255)),
                ('state_province', models.CharField(default=b' ', max_length=255)),
                ('country', models.CharField(default=b' ', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('profileaddress', models.OneToOneField(null=True, verbose_name=b'profileaddress', to='exchcard_backend_api.Address')),
                ('profileuser', models.OneToOneField(default=1, verbose_name=b'profileuser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.AddField(
            model_name='card',
            name='fromsender',
            field=models.ForeignKey(related_name='sent_cards', default=1, to='exchcard_backend_api.Profile'),
        ),
        migrations.AddField(
            model_name='card',
            name='toaddress',
            field=models.ForeignKey(related_name='to_addresses', default=None, to='exchcard_backend_api.Address'),
        ),
        migrations.AddField(
            model_name='card',
            name='torecipient',
            field=models.ForeignKey(related_name='received_cards', default=1, to='exchcard_backend_api.Profile'),
        ),
    ]
