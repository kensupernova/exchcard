#coding: utf-8

import datetime
import time

import os
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Manager

import utils.datetime_helper
from exchcard import settings
from exchcard.manage import AddressManager
from exchcard.manage import DetailedAddressManager

#-------------------------------------------------------------------------
"""
Model Manager管理模型的CRUD, 可以实现某些特殊的功能。
"""
class ProfileManager(Manager):
    def create_profile_with_ids(self, userid, addressid):
        user = User.objects.get(pk=userid)
        address = Address.objects.get(pk=addressid)

        profile = self.create(profileuser=user, profileaddress=address)
        return profile

    def update_profile_address_with_ids(self, userid, addressid):
        profile = Profile.objects.get(profileuser_id=userid)
        profile.profileaddress_id = addressid

        return profile


class CardManager(Manager):
    def create_with_profile_ids(self, card_name, torecipient_id, fromsender_id):
        if Profile.objects.filter(id=torecipient_id).exists() and \
                Profile.objects.filter(id=fromsender_id).exists():
            card = self.create(card_name=card_name,
                               torecipient_id=torecipient_id,
                               fromsender_id=fromsender_id,
                               has_arrived=False)

            return card

        return None


class DianZanManager(Manager):
    def create_with_ids(self, card_by_dianzan_id,
                        card_photo_by_dianzan_id, person_who_dianzan_id):
        if Card.objects.filter(id=card_by_dianzan_id).exists():
            dianzan = self.create(card_by_dianzan=Card.objects.get(id=card_by_dianzan_id),
                                  card_photo_by_dianzan=CardPhoto.objects.get(id=card_photo_by_dianzan_id),
                                  person_who_dianzan=Profile.objects.get(id=person_who_dianzan_id));

            dianzan.save()

            return dianzan

        return None


#-----------------------------------------------------------------------
"""
数据模型model
"""

class Address(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length = 255, default="name")
    address = models.CharField(max_length = 255, default="address")
    postcode = models.CharField(max_length = 100,  default="111111")

    class Meta:
        ordering = ['-name']

    # the full mailling address
    def __str__(self):
        return u'%s, address: %s, %s, %s' % (self.id, self.name, self.address, self.postcode)

    def update(self, name, address, postcode, *args, **kwargs):
        self.name = name
        self.address =address
        self.postcode = postcode

        super(Address, self).save(*args, **kwargs)


    objects = AddressManager()

class DetailedAddress(models.Model):
    address_first_line = models.CharField(max_length = 255, default=" ")
    address_second_line = models.CharField(max_length = 255, default=" ")
    address_third_line = models.CharField(max_length = 255, default=" ")
    city = models.CharField(max_length = 255, default=" ")
    state_province = models.CharField(max_length = 255, default=" ")
    country = models.CharField(max_length = 255, default=" ")

    def __str__(self):
        return u'%s, %s, %s, %s, %s' % (self.address_first_line, self.address_second_line,
            self.address_third_line, self.city, self.country)

    objects = DetailedAddressManager()


class Profile(models.Model):
    """
    It combines information for:
    Account information: User account, Weibo UID, Weixin UID, etc,
    Address information

    """

    created = models.DateTimeField(auto_now_add = True)

    profileuser = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="profileuser",
        null=False,
        default=1
    )
    profileaddress = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        verbose_name="profileaddress", null=True)

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return u'%s, user: %s, %s; ' \
               u'address: %s, %s, %s, %s' % (self.id,
                   self.profileuser.id, self.profileuser.email,
                   self.profileaddress.id, self.profileaddress.name,
                   self.profileaddress.address,self.profileaddress.postcode)

    def __str__(self):
        return u'%s, user: %s, %s; ' \
               u'address: %s, %s, %s, %s' % (self.id,
                   self.profileuser.id, self.profileuser.email,
                   self.profileaddress.id, self.profileaddress.name,
                   self.profileaddress.address,
                   self.profileaddress.postcode)

    def save(self, *args, **kwargs):
        """
        save the newly created Object
        """
        super(Profile, self).save(*args, **kwargs)

    objects = ProfileManager()



class Card(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    card_name = models.CharField(max_length=50, default=None)

    #exchcard_backend_api of recipient
    torecipient = models.ForeignKey('Profile', related_name='receive_cards', default=1)

    #exchcard_backend_api of sender
    fromsender = models.ForeignKey('Profile', related_name='sent_cards', default=1)

    sent_time = models.BigIntegerField(default=int(round(time.time()*1000)))
    sent_date = models.DateTimeField(auto_now_add=True)

    arrived_time = models.BigIntegerField(default=None)
    arrived_date = models.DateTimeField(default=None)

    has_arrived = models.BooleanField(default=False)


    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        """
        决定了后台管理呈现的数据
        :return:
        """
        return u'sender: %s, %s -> recipient: %s, %s, address: %s, %s, %s' % (
            self.fromsender.id,
            self.fromsender.profileuser.email,
            self.torecipient.id,
            self.torecipient.profileuser.email,
            self.torecipient.profileaddress.name,
            self.torecipient.profileaddress.address,
            self.torecipient.profileaddress.postcode)

    def __str__(self):
        """
        决定了后台管理呈现的数据
        :return:
        """
        return u'sender: %s, %s -> recipient: %s, %s, address: %s, %s, %s' % (
            self.fromsender.id,
            self.fromsender.profileuser.email,
            self.torecipient.id,
            self.torecipient.profileuser.email,
            self.torecipient.profileaddress.name,
            self.torecipient.profileaddress.address,
            self.torecipient.profileaddress.postcode)

    def save(self, *args, **kwargs):
        """
        save the newly created Object
        """
        super(Card, self).save(*args, **kwargs)

    def update(self, torecipient_id, fromsender_id, card_name, sent_time, *args, **kwargs):
        """
        save the newly created Object
        """
        self.torecipient.id = torecipient_id
        self.fromsender.id = fromsender_id
        self.card_name = card_name
        self.sent_time  =sent_time
        super(Card, self).save(*args, **kwargs)

    def update_with_cardname(self, *args, **kwargs):
        """
        save the newly created Object
        """
        super(Card, self).save(*args, **kwargs)

    def mark_arrived(self, *args, **kwargs):
        self.has_arrived = True
        ## save arrived time as current time in mill seconds
        self.arrived_time = int(round(time.time()*1000))
        self.arrived_date = datetime.datetime.now()

        super(Card, self).save(*args, **kwargs)

    def update_date_with_timestamp(self, *args, **kwargs):
        if (not self.arrived_time) and (self.arrived_time != 0) and (self.arrived_time is not None):
            ## print self.arrived_time
            self.arrived_date = utils.datetime_helper.mills2datetime(self.arrived_time)

        if (not self.sent_time) and (self.sent_time != 0) and (self.sent_time is not None):
            ## print self.sent_time
            self.sent_date = utils.datetime_helper.mills2datetime(self.sent_time)

        super(Card, self).save(*args, **kwargs)

    def get_sent_datetime(self):
        # return exchcard_backend_api.utils.datetime_helper.mills2datetime(self.sent_time)
        return self.sent_date

    def get_arrived_datetime(self):
        # return exchcard_backend_api.utils.datetime_helper.mills2datetime(self.arrived_time)
        return self.arrived_date

    objects = CardManager()



## exchcard_backend_api avatar photo
class AvatarPhoto(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey("Profile", related_name="avatars") ## related name is for Profile to use
    avatar = models.ImageField(upload_to="avatar_photos")

    def get_abs_path(self):
        return os.path.join(settings.MEDIA_ROOT, self.avatar.name)



class CardPhoto(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey("Profile", related_name="cardphotos_of_profile") ## related name is for Profile to use
    card_host = models.ForeignKey('Card', related_name='cardphotos_of_card', default=1)

    card_photo = models.ImageField(upload_to="card_photos")

    def get_abs_path(self):
        return os.path.join(settings.MEDIA_ROOT, self.card_photo.name)


class DianZan(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    # the card who is dianzaned
    card_by_dianzan = models.ForeignKey('Card', related_name='dianzans_of_card', default=1)

    # Photo which is dianzaned
    card_photo_by_dianzan = models.ForeignKey('CardPhoto', related_name='dianzans_of_card_photo', default=1)

    # the person who dianzan
    person_who_dianzan = models.ForeignKey('Profile', related_name='dianzans_by_person', default=1)

    class Meta:
        ordering = ['-created']

    def as_json(self):
        created_in_ms = self.created
        return dict(
            dianzan_id = self.id,
            card_by_dianzan = self.card_by_dianzan.id,
            person_who_dianzan = self.person_who_dianzan.id,
            created = created_in_ms
        )


    objects = DianZanManager()



