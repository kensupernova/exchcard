#coding: utf-8
"""
主要负责与地址有关的数据model
"""

import datetime
import time

import os

from django.db import models
from django.db.models import Manager

from exchcard import settings
from exchcard.manage import AddressManager, DetailedAddressManager

from django.contrib.auth import get_user_model # If used custom user mode
User = get_user_model() #  自定义用户模型


from utils import datetime_helper



class ProfileManager(Manager):
    def create_profile_with_ids(self, userid, addressid):
        user = User.objects.get(pk=userid) ## 使用自定义的扩展的数据模型
        address = Address.objects.get(pk=addressid)

        profile = self.create(profileuser=user, profileaddress=address)
        profile.save()
        return profile

    def update_profile_address_with_ids(self, userid, addressid):
        profile = Profile.objects.get(profileuser_id=userid)
        profile.profileaddress_id = addressid
        profile.save()
        return profile




class CardManager(Manager):
    def create_with_profile_ids(self, card_name, torecipient_id, fromsender_id):
        if Profile.objects.filter(id=torecipient_id).exists() and \
                Profile.objects.filter(id=fromsender_id).exists():
            card = self.create(card_name=card_name,
                               torecipient_id=torecipient_id,
                               fromsender_id=fromsender_id,
                               has_arrived=False)
            card.save()
            return card

        return None



"""
数据模型model
"""

class Address(models.Model):
    """
    postal address, 可以邮寄用的，包括名字，地址，邮编等
    """
    created = models.DateTimeField(auto_now_add=True)
    # DateField.auto_now表示是否每次修改时改变时间
    # DateField.auto_now_add 表示是否创建时表示时间
    name = models.CharField(max_length = 255, default="name")
    # 包括邮箱号，门牌号，房间楼层，建筑名，建筑牌号，街道，城市，国家
    address = models.CharField(max_length = 255, default="address")
    postcode = models.CharField(max_length = 100,  default="111111")

    # 单独列出城市，国家
    city = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)

    ## 包括以上所有信息
    full_text_address = models.CharField(max_length=510, null=True)

    objects = AddressManager()

    class Meta:
        ordering = ['-created']

    # the full mailling address
    def __str__(self):
        return u'%s, address: %s, %s, %s' % (self.id, self.name, self.address, self.postcode)

    def save(self, *args, **kwargs):
        """
        save the newly created Object
        """
        super(Address, self).save(*args, **kwargs)

    def update(self, name, address, postcode, *args, **kwargs):
        self.name = name
        self.address = address
        self.postcode = postcode
        super(Address, self).save(*args, **kwargs)



class DetailedAddress(models.Model):
    address_first_line = models.CharField(max_length = 255, default=" ")
    address_second_line = models.CharField(max_length = 255, default=" ")
    address_third_line = models.CharField(max_length = 255, default=" ")
    city = models.CharField(max_length = 255, default=" ")
    state_province = models.CharField(max_length = 255, default=" ")
    country = models.CharField(max_length = 255, default=" ")

    objects = DetailedAddressManager()

    def __str__(self):
        return u'%s, %s, %s, %s, %s' % (self.address_first_line, self.address_second_line,
            self.address_third_line, self.city, self.country)





class Profile(models.Model):
    """
    It combines information for:
    XUser information: email, Weibo UID, Weixin UID, etc,
    Address information: name, address, postcode, city, country

    """

    created = models.DateTimeField(auto_now_add = True)

    profileuser = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="profileuser",
        null=False
    )

    profileaddress = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        verbose_name="profileaddress",
        null=False)

    objects = ProfileManager()

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
        ## *args表示任何多个无名参数，它是一个tuple；**kwargs表示关键字参数，它是一个dict。



## exchcard_backend_api avatar photo
class AvatarPhoto(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey("Profile", related_name="avatars") ## related name is for Profile to use in serializer
    avatar = models.ImageField(upload_to="avatar_photos")

    def get_abs_path(self):
        return os.path.join(settings.MEDIA_ROOT, self.avatar.name)


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

    objects = CardManager()

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
            self.arrived_date = datetime_helper.mills2datetime(self.arrived_time)

        if (not self.sent_time) and (self.sent_time != 0) and (self.sent_time is not None):
            ## print self.sent_time
            self.sent_date = datetime_helper.mills2datetime(self.sent_time)

        super(Card, self).save(*args, **kwargs)

    def get_sent_datetime(self):
        # return exchcard_backend_api.utils.datetime_helper.mills2datetime(self.sent_time)
        return self.sent_date

    def get_arrived_datetime(self):
        # return exchcard_backend_api.utils.datetime_helper.mills2datetime(self.arrived_time)
        return self.arrived_date





class CardPhoto(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey("Profile", related_name="cardphotos_of_profile") ## related name is for Profile to use
    card_host = models.ForeignKey('Card', related_name='cardphotos_of_card', default=1)
    card_photo = models.ImageField(upload_to="card_photos")

    def get_abs_path(self):
        return os.path.join(settings.MEDIA_ROOT, self.card_photo.name)




