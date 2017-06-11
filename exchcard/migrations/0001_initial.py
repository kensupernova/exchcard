# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='XUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name=b'Email', db_index=True)),
                ('username', models.CharField(unique=True, max_length=50, db_index=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('type', models.IntegerField(default=0)),
                ('sex', models.IntegerField(default=1)),
                ('weibo_uid', models.CharField(max_length=50, null=True)),
                ('weibo_access_token', models.CharField(max_length=100, null=True)),
                ('desc', models.CharField(max_length=2000, null=True)),
                ('url', models.URLField(null=True)),
                ('avatar', models.CharField(max_length=500, null=True)),
            ],
            options={
                'db_table': 'exchcard_xuser',
            },
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(max_length=50, choices=[(b'SP', b'Sent Postcard'), (b'SPP', b'Sent Postcard with Photo'), (b'RP', b'Receive Postcard'), (b'RPP', b'Receive postcard with photo'), (b'UPP', b'Upload postcard photo'), (b'MC', b'Make comment'), (b'MDZ', b'Make dian Zan')])),
                ('short_name', models.CharField(max_length=20)),
                ('short_name_zh', models.CharField(max_length=20, null=True)),
                ('description', models.CharField(max_length=100, null=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(default=b'name', max_length=255)),
                ('address', models.CharField(default=b'address', max_length=255)),
                ('postcode', models.CharField(default=b'111111', max_length=100)),
                ('city', models.CharField(max_length=50, null=True)),
                ('country', models.CharField(max_length=50, null=True)),
                ('full_text_address', models.CharField(max_length=510, null=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='AvatarPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('avatar', models.ImageField(upload_to=b'avatar_photos')),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('card_name', models.CharField(default=None, max_length=50)),
                ('sent_time', models.BigIntegerField(default=1497094768994)),
                ('sent_date', models.DateTimeField(auto_now_add=True)),
                ('arrived_time', models.BigIntegerField(default=None)),
                ('arrived_date', models.DateTimeField(default=None)),
                ('has_arrived', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='CardPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('card_photo', models.ImageField(upload_to=b'card_photos')),
                ('card_host', models.ForeignKey(related_name='cardphotos_of_card', default=1, to='exchcard.Card')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(max_length=500)),
            ],
            options={
                'ordering': ['-created'],
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
            name='DianZan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('subject', models.ForeignKey(related_name='follows_user_make', default=1, to=settings.AUTH_USER_MODEL)),
                ('user_being_followed', models.ForeignKey(related_name='followers_of_user', default=1, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('profileaddress', models.OneToOneField(verbose_name=b'profileaddress', to='exchcard.Address')),
                ('profileuser', models.OneToOneField(verbose_name=b'profileuser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ReceiveCardAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('has_photo', models.BooleanField(default=False)),
                ('card_received', models.OneToOneField(to='exchcard.Card')),
                ('card_received_photo', models.OneToOneField(null=True, to='exchcard.CardPhoto')),
                ('subject', models.ForeignKey(related_name='receive_card_actions_by_subject', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='SentCardAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('has_photo', models.BooleanField(default=False)),
                ('card_sent', models.OneToOneField(to='exchcard.Card')),
                ('card_sent_photo', models.OneToOneField(null=True, to='exchcard.CardPhoto')),
                ('subject', models.ForeignKey(related_name='sent_card_actions_by_subject', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='UploadCardPhotoAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('card_actioned', models.ForeignKey(related_name='upload_actions_to_card', to='exchcard.Card')),
                ('card_photo_uploaded', models.OneToOneField(to='exchcard.CardPhoto')),
                ('subject', models.ForeignKey(related_name='upload_actions_by_subject', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.AddField(
            model_name='dianzan',
            name='receive_card_action_zaned',
            field=models.ForeignKey(related_name='dianzans_of_receive_card_action', to='exchcard.ReceiveCardAction', null=True),
        ),
        migrations.AddField(
            model_name='dianzan',
            name='sent_card_action_zaned',
            field=models.ForeignKey(related_name='dianzans_of_send_card_action', to='exchcard.SentCardAction', null=True),
        ),
        migrations.AddField(
            model_name='dianzan',
            name='upload_cardphoto_action_zaned',
            field=models.ForeignKey(related_name='dianzans_of_receive_card_action', to='exchcard.UploadCardPhotoAction', null=True),
        ),
        migrations.AddField(
            model_name='dianzan',
            name='user_who_zan',
            field=models.ForeignKey(related_name='dianzans_by_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='receive_card_action_commented',
            field=models.ForeignKey(related_name='comments_of_receive_card_action', to='exchcard.ReceiveCardAction', null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='sent_card_action_commented',
            field=models.ForeignKey(related_name='comments_of_send_card_action', to='exchcard.SentCardAction', null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='upload_cardphoto_action_commented',
            field=models.ForeignKey(related_name='comments_of_receive_card_action', to='exchcard.UploadCardPhotoAction', null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='user_who_comment',
            field=models.ForeignKey(related_name='comments_by_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cardphoto',
            name='owner',
            field=models.ForeignKey(related_name='cardphotos_of_profile', to='exchcard.Profile'),
        ),
        migrations.AddField(
            model_name='card',
            name='fromsender',
            field=models.ForeignKey(related_name='sent_cards', default=1, to='exchcard.Profile'),
        ),
        migrations.AddField(
            model_name='card',
            name='torecipient',
            field=models.ForeignKey(related_name='receive_cards', default=1, to='exchcard.Profile'),
        ),
        migrations.AddField(
            model_name='avatarphoto',
            name='owner',
            field=models.ForeignKey(related_name='avatars', to='exchcard.Profile'),
        ),
    ]
