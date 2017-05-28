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

from django.contrib.auth import get_user_model # If used custom user mode
User = get_user_model() #  自定义用户模型

from utils import datetime_helper

class DetailedAddressManager(Manager):
    def create_detailed_address(self, first, second, third, city, stateorprovince, country):
        detailedAddress = self.create(first, second, third, city, stateorprovince, country) ## 可以省去save
        detailedAddress.save()
        return detailedAddress

class AddressManager(Manager):
    def create_address(self, name, address, postcode):
        address_object = self.create(name=name, address=address, postcode=postcode)
        ## obj = self.model(name=name, address=address, postcode=postcode)
        address_object.save()
        return address_object

    def create_address_with_full_text(self, name, address, postcode, full_text_address):
        obj = self.create(name=name, address=address, postcode=postcode, full_text_address=full_text_address)
        obj.save()
        return obj
    def create_address_all_information(self, name, address, postcode, city, country, full_text_address):
        obj = self.create(name=name, address=address, postcode=postcode,
                          city = city,
                          country = country,
                          full_text_address=full_text_address)
        obj.save()
        return obj

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

            card = Card.objects.create(card_name=card_name,
                               torecipient_id=torecipient_id,
                               fromsender_id=fromsender_id,
                               has_arrived=False)

            action = SentCardAction(subject=card.fromsender.profileuser, card_sent=card)
            action.save()

            return card

        return None

    def create_with_card_action_returns(self, *args, **kwargs):
        """
        sent card action shall be created automatically
        :return:
        """
        card = Card.objects.create(self, *args, **kwargs)
        action = SentCardAction(subject=card.fromsender, card_sent=card, *args, **kwargs).save()
        return (card, action)

    def create(self, *args, **kwargs):
        ## 重新定义create
        # kwargs['order_no'] = datetime.datetime.now.strftime('%Y%m%d' + seq)
        return super(CardManager, self).create(*args, **kwargs)


class DianZanManager(Manager):
    def create_with_ids(self, card_by_dianzan_id,
                        card_photo_by_dianzan_id, person_who_dianzan_id):
        if Card.objects.filter(id=card_by_dianzan_id).exists():
            dianzan = self.create(card_by_dianzan=Card.objects.get(id=card_by_dianzan_id),
                                  card_photo_by_dianzan=CardPhoto.objects.get(id=card_photo_by_dianzan_id),
                                  person_who_dianzan=Profile.objects.get(id=person_who_dianzan_id))

            dianzan.save()

            return dianzan

        return None

class SentCardActionManager(Manager):
    """"""

class ReceiveCardActionManager(Manager):
    """"""



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
        # self.order_no = datetime.datetime.now.strftime('%Y%m%d' + seq)
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

        ## create Receive action automaticallycard.save()
        ## TODO: check
        ReceiveCardAction.objects.create(subject=self.torecipient.profileuser, card_received = self)

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




"""
主要是用户活动的数据模型, 与地址无关，不用Profile关联，而用正常的User
"""

#-----------------------------------------------------------------------


class DianZan(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    # the card who is dianzaned
    card_by_dianzan = models.ForeignKey('Card', related_name='dianzans_of_card', default=1)

    # Photo which is dianzaned
    card_photo_by_dianzan = models.ForeignKey('CardPhoto', related_name='dianzans_of_card_photo', default=1)

    ## the user who dianzan, not profile
    person_who_dianzan = models.ForeignKey('XUser', related_name='dianzans_by_person', default=1)


    objects = DianZanManager()

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


class SentCardAction(models.Model):
    """
    用户发送明信片这样一个action
    """
    created = models.DateTimeField(auto_now_add=True)

    # 用户是行为的subject
    subject = models.ForeignKey('XUser', related_name='sent_card_actions_by_subject', null=False)

    card_sent = models.OneToOneField('Card') #  一张明信片只有一个action

    objects = SentCardActionManager

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return u'%s send a card with postcard id %s; ' % (self.subject, self.card_sent.card_name)

    def __str__(self):
        return u'%s send a card with postcard id %s; ' % (self.subject, self.card_sent.card_name)

    def save(self, *args, **kwargs):
        # type: (object, object) -> object
        super(SentCardAction, self).save(*args, **kwargs)


class ReceiveCardAction(models.Model):
    """
    用户发送明信片这样一个action
    """
    created = models.DateTimeField(auto_now_add=True)

    # 用户是行为的subject
    subject = models.ForeignKey('XUser', related_name='receive_card_actions_by_subject', null=False)

    card_received = models.OneToOneField('Card')  # 一张明信片只有一个action

    objects = ReceiveCardActionManager

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return u'%s receive a card with postcard id %s; ' % (self.subject, self.card_received.card_name)

    def __str__(self):
        return u'%s receive a card with postcard id %s; ' % (self.subject, self.card_sent.card_name)

    def save(self, *args, **kwargs):
        super(ReceiveCardAction, self).save(*args, **kwargs)
