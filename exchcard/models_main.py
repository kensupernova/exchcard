#coding: utf-8
"""
主要负责与地址有关的数据model
"""

import datetime
import time
from django.utils import timezone
import os

from django.db import models
from django.db.models import Manager

from exchcard import settings

from django.contrib.auth import get_user_model # If used custom user mode


User = get_user_model() #  自定义用户模型


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
        return profile

    def update_profile_address_with_ids(self, userid, addressid):
        profile = Profile.objects.get(profileuser_id=userid)
        profile.profileaddress_id = addressid
        profile.save()
        return profile


class CardManager(Manager):
    def create(self, *args, **kwargs):
        # 重新定义create
        # kwargs['order_no'] = datetime.datetime.now.strftime('%Y%m%d' + seq)
        return super(CardManager, self).create(*args, **kwargs)

    def create_with_profile_ids(self, card_name, torecipient_id, fromsender_id):
        if Profile.objects.filter(id=torecipient_id).exists() and \
                Profile.objects.filter(id=fromsender_id).exists():

            # method 1:
            # card = self.create(card_name=card_name,
            #                    torecipient_id=torecipient_id,
            #                    fromsender_id=fromsender_id,
            #                    has_arrived=False)

            # method 2:
            card = self.model(card_name=card_name,
                               torecipient_id=torecipient_id,
                               fromsender_id=fromsender_id,
                               has_arrived=False)
            card.save(using=self._db)  ## 必须save()

            return card

        return None

    def create_with_card_action_objs_returned(self,
                                              card_name, torecipient_id, fromsender_id,
                                              *args, **kwargs):
        """
        objects card, sent card action, shall be created automatically and sync
        :return: card, sentcardaction,
        """
        if (not Profile.objects.filter(id=torecipient_id).exists()) or \
                (not Profile.objects.filter(id=fromsender_id).exists()):
            return None

        card = self.create(card_name=card_name,
                               torecipient_id=torecipient_id,
                               fromsender_id=fromsender_id,
                               has_arrived=False, *args, **kwargs)

        action = SentCardAction(subject=card.fromsender.profileuser,
                                card_sent=card,
                                has_photo=False)
        action.save()

        return card, action

    def create_with_card_action_photo_objs_returned(self,
                                                    card_name, torecipient_id, fromsender_id, card_photo_file,
                                                    *args, **kwargs):
        """
        objects card, sent card action, card photo;shall be created automatically and sync
        :return: card, sentcardaction,
        """
        if (not Profile.objects.filter(id=torecipient_id).exists()) or \
                (not Profile.objects.filter(id=fromsender_id).exists()):
            return None

        # method 1
        card = self.create(card_name=card_name,
                           torecipient_id=torecipient_id,
                           fromsender_id=fromsender_id,
                           has_arrived=False, *args, **kwargs)

        # method 2
        # card = self.model(card_name=card_name,
        #                    torecipient_id=torecipient_id,
        #                    fromsender_id=fromsender_id,
        #                    has_arrived=False, *args, **kwargs)
        # card.save(using=self._db)

        photo = CardPhoto(owner=card.fromsender,
                          card_host=card,
                          card_photo=card_photo_file)
        photo.save()

        action = SentCardAction(subject=card.fromsender.profileuser,
                                card_sent=card,
                                has_photo=True,
                                card_sent_photo=photo)
        action.save()

        return card, action, photo


class FollowManager(Manager):
    def create_with_ids(self, subject_id, object_being_followed_id):
        if not Follow.objects.filter(object_being_followed_id=object_being_followed_id).exists():
            obj = self.create(subject_id=subject_id,
                            object_being_followed_id=object_being_followed_id)
            return obj
        return None


class SentCardActionManager(Manager):
    """"""

class ReceiveCardActionManager(Manager):
    """"""

class UploadCardPhotoActionManager(Manager):
    """
    Upload postcard photo action manager
    """
    def create_with_ids(self, subject_id, card_host_id, card_photo_uploaded_id):
        obj = self.create(subject_id=subject_id,
                          card_host_id=card_host_id,
                          card_photo_uploaded_id=card_photo_uploaded_id)
        return obj


class DianZanManager(Manager):
    def create_with_ids(self, user_who_zan_id, sent_card_action_zaned_id=None,
                        receive_card_action_zaned_id=None, upload_cardphoto_action_zaned_id=None,
                        *args, **kwargs):
        obj = self.model(user_who_zan_id=user_who_zan_id,
                         sent_card_action_zaned_id=sent_card_action_zaned_id,
                         receive_card_action_zaned_id=receive_card_action_zaned_id,
                         upload_cardphoto_action_zaned_id=upload_cardphoto_action_zaned_id)
        # if kwargs:
        #     if kwargs.get('sent_card_action_zaned_id', None):
        #         obj.sent_card_action_zaned_id = kwargs['sent_card_action_zaned_id']
        #     if kwargs.get('receive_card_action_zaned_id', None):
        #         obj.receive_card_action_zaned_id = kwargs['receive_card_action_zaned_id']
        #     if kwargs.get('upload_cardphoto_action_zaned_id', None):
        #         obj.upload_cardphoto_action_zaned_id = kwargs['upload_cardphoto_action_zaned_id']

        # save !!! important
        obj.save(using=self._db)
        return obj

    @staticmethod
    def filter_by_action_id(sent_card_action_zaned_id=None,
                            receive_card_action_zaned_id=None, upload_cardphoto_action_zaned_id=None):
        """
        通过活动action_id过滤得到DianZan
        :param args:
        :param kwargs:
        :return: list of objects
        """
        dianzans = None
        if not sent_card_action_zaned_id:
            dianzans = DianZan.objects.filter(sent_card_action_zaned_id=sent_card_action_zaned_id)

        if not receive_card_action_zaned_id:
            dianzans = DianZan.objects.filter(receive_card_action_zaned_id=receive_card_action_zaned_id)

        if not upload_cardphoto_action_zaned_id:
            dianzans = DianZan.objects.filter(upload_cardphoto_action_zaned_id=upload_cardphoto_action_zaned_id)

        return dianzans


class CommentManager(Manager):
    def create_with_ids(self, comment, user_who_comment_id, *args, **kwargs):
        obj = self.model(comment=comment, user_who_comment_id=user_who_comment_id)
        if kwargs:
            if kwargs.get('sent_card_action_commented_id', None):
                obj.sent_card_action_commented_id = kwargs['sent_card_action_commented_id']
            if kwargs.get('receive_card_action_commented_id', None):
                obj.sent_card_action_commented_id = kwargs['receive_card_action_commented_id']
            if kwargs.get('upload_cardphoto_action_commented_id', None):
                obj.sent_card_action_commented_id = kwargs['upload_cardphoto_action_commented_id']

        # save !!! important
        obj.save(using=self._db)
        return obj


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



#----------------------------------------------------------------
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
        save the newly created Object when it is like: Profle(...).save(),
        """
        super(Profile, self).save(*args, **kwargs)
        # *args表示任何多个无名参数，它是一个tuple；**kwargs表示关键字参数，它是一个dict。


class AvatarPhoto(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey("Profile", related_name="avatars") ## related name is for Profile to use in serializer
    avatar = models.ImageField(upload_to="avatar_photos")

    def get_abs_path(self):
        return os.path.join(settings.MEDIA_ROOT, self.avatar.name)


class Card(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    # 在前端显示时cardname就是postcard id，而不是card.id
    card_name = models.CharField(max_length=50, default=None)

    #exchcard_backend_api of recipient
    torecipient = models.ForeignKey('Profile', related_name='receive_cards', default=1)

    #exchcard_backend_api of sender
    fromsender = models.ForeignKey('Profile', related_name='sent_cards', default=1)

    sent_time = models.BigIntegerField(default=int(round(time.time()*1000)))
    # int(round(time.time()*1000), microseconds ==> millseconds!!!
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
        # 重新定义save
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

    def mark_arrived(self, has_photo=False, card_photo_file=None, *args, **kwargs):
        self.has_arrived = True
        # save arrived time as current time in mill seconds
        self.arrived_time = int(round(time.time()*1000))

        # self.arrived_date = datetime.datetime.now()
        # RuntimeWarning: DateTimeField Card.arrived_date received a naive datetime
        # (2017-06-06 16:18:43.939844) while time zone support is active.

        self.arrived_date = timezone.now()

        # 接收明信片有图片
        if has_photo and card_photo_file:
            print "Receive postcard with photo , SPP, activity_type_id = 4"
            photo = CardPhoto(owner=self.torecipient,
                              card_host=self,
                              card_photo=card_photo_file)
            photo.save()

        else:
            print "Receive postcard, SP, SP, activity_type_id = 3"
            photo = None


        # objects.create() Receive action automatically card.save()
        receive_card_action = ReceiveCardAction.objects.create(
            subject=self.torecipient.profileuser,
            card_received=self,
            has_photo=has_photo,
            card_received_photo= photo)
        receive_card_action.save()

        # 保存明信片到达等信息
        super(Card, self).save(*args, **kwargs)

        return receive_card_action, photo

    def update_date_with_timestamp(self, *args, **kwargs):
        if (not self.arrived_time) and (self.arrived_time != 0) and (self.arrived_time is not None):
            ## print self.arrived_time
            self.arrived_date = mills2datetime(self.arrived_time)

        if (not self.sent_time) and (self.sent_time != 0) and (self.sent_time is not None):
            ## print self.sent_time
            self.sent_date = mills2datetime(self.sent_time)

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
class Activity(models.Model):
    ACTIVITY_TYPES = (
        #------- user make action initially, each action has a subject, and something being done
        ('SP', 'Sent Postcard'), # activity_type_id = 1
        ('SPP', 'Sent Postcard with Photo'), # activity_type_id = 2
        ('RP', 'Receive Postcard'), # activity_type_id = 3
        ('RPP', 'Receive postcard with photo'), # activity_type_id = 4
        ('UPP', 'Upload postcard photo'), # activity_type_id = 5
        #-------- Feedback on above actions, each has a subject, and an aboved actions being done
        ('MC', 'Make comment'), #
        ('MDZ', 'Make dian Zan'), #
    )

    created = models.DateTimeField(auto_now_add=True)
    ## 活动的种类
    type = models.CharField(max_length=50,null=False, choices=ACTIVITY_TYPES)
    ## 活动的简短名字："send postcard" "register postcard" "comment", "dianzan", "upload postcard photo"
    short_name = models.CharField(max_length=20, null=False)
    short_name_zh = models.CharField(max_length=20, null=True)
    # EX: sent a postcard to others by get a postal mailling address
    description = models.CharField(max_length=100, null=True)

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return u'activty type: %s, short name: %s, description: %s' \
               % (self.type, self.short_name, self.description)

    def __str__(self):
        return u'activty type: %s, short name: %s, description: %s' \
               % (self.type, self.short_name, self.description)

    def save(self, *args, **kwargs):
        # type: (object, object) -> object
        super(Activity, self).save(*args, **kwargs)


class Follow(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    ## the user who make the follow
    subject = models.ForeignKey('XUser', related_name='follows_user_make', default=1, null=False)
    ## the user who is being followed by the subject
    user_being_followed = models.ForeignKey('XUser', related_name='followers_of_user', default=1, null=False)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return u'%s following %s' \
               % (self.subject, self.user_being_followed)

    def __str__(self):
        return u'%s following %s' \
               % (self.subject, self.user_being_followed)

    def save(self, *args, **kwargs):
        # type: (object, object) -> object
        super(Follow, self).save(*args, **kwargs)

    objects = FollowManager


#------------------------------------------------------------------------
# 用户的主要活动

class SentCardAction(models.Model):
    """
    用户发送明信片这样一个action
    Note: Sorry, it is typo to use Sent instead of Send
    """
    created = models.DateTimeField(auto_now_add=True)

    # 用户是行为的subject
    subject = models.ForeignKey('XUser', related_name='sent_card_actions_by_subject', null=False)
    # 是行为的object
    card_sent = models.OneToOneField('Card') #  一张明信片只有一个sent action

    ## 新加的！
    has_photo = models.BooleanField(default=False) # 默认没有photo
    card_sent_photo = models.OneToOneField('CardPhoto', null=True)

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
    用户接收到明信片这样一个action
    """
    created = models.DateTimeField(auto_now_add=True)

    # 用户是行为的subject
    subject = models.ForeignKey('XUser', related_name='receive_card_actions_by_subject', null=False)

    card_received = models.OneToOneField('Card')  # 一张明信片只有一个receive action

    ## 新加的！
    has_photo = models.BooleanField(default=False)  # 默认没有photo
    card_received_photo = models.OneToOneField('CardPhoto', null=True)

    objects = ReceiveCardActionManager

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return u'%s receive a card with postcard id %s; ' % (self.subject, self.card_received.card_name)

    def __str__(self):
        return u'%s receive a card with postcard id %s; ' % (self.subject, self.card_sent.card_name)

    def save(self, *args, **kwargs):
        super(ReceiveCardAction, self).save(*args, **kwargs)


class UploadCardPhotoAction(models.Model):
    """
    用户给某张自己发送或者接收的明信片之后, 补上传一张明信片图片
    """
    created = models.DateTimeField(auto_now_add=True)

    # 用户是行为的subject
    subject = models.ForeignKey('XUser', related_name='upload_actions_by_subject', null=False)
    # 这种图片所属的明信片
    card_actioned = models.ForeignKey('Card', related_name='upload_actions_to_card', null=False)

    card_photo_uploaded = models.OneToOneField('CardPhoto', null=False)

    objects = UploadCardPhotoActionManager

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return u'%s upload a photo for postcard id %s; ' % (self.subject, self.card_actioned.card_name)

    def __str__(self):
        return u'%s upload a photo for postcard id %s; ' % (self.subject, self.card_actioned.card_name)

    def save(self, *args, **kwargs):
        super(UploadCardPhotoAction, self).save(*args, **kwargs)


class DianZan(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user_who_zan = models.ForeignKey('XUser',
                                    related_name='dianzans_by_user',
                                    null=False)
    is_active = models.BooleanField(null=False, default=True)
    # 用户活动点赞的对象, 三种情况
    sent_card_action_zaned = models.ForeignKey('SentCardAction',
                                            related_name='dianzans_of_send_card_action',
                                            null=True)
    receive_card_action_zaned = models.ForeignKey('ReceiveCardAction',
                                                related_name='dianzans_of_receive_card_action',
                                                null=True)
    upload_cardphoto_action_zaned = models.ForeignKey('UploadCardPhotoAction',
                                                    related_name='dianzans_of_receive_card_action',
                                                    null=True)
    objects = DianZanManager()

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        super(DianZan, self).save(*args, **kwargs)

    def toggle_active(self, *args, **kwargs):
        self.is_active = not self.is_active
        super(DianZan, self).save(*args, **kwargs)


class Comment(models.Model):
    """
    用户USER给其他用户或者自己活动Action, ReceiveCardAction, SentCardAction, UploadCardPhotoAction,
    （SP, SPP, RP, RPP, UPP）的评论， 或者对评论的评论
    # Feedback on Actions: ReceiveCardAction, SentCardAction, UploadCardPhotoAction
    """
    created = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=500, null=False)
    user_who_comment = models.ForeignKey('XUser',
                                         related_name='comments_by_user',
                                         null=False)


    # 用户评论的对象, 三种情况
    sent_card_action_commented = models.ForeignKey('SentCardAction',
                                                   related_name='comments_of_send_card_action',
                                                   null=True)

    receive_card_action_commented = models.ForeignKey('ReceiveCardAction',
                                                      related_name='comments_of_receive_card_action',
                                                      null=True)

    upload_cardphoto_action_commented = models.ForeignKey('UploadCardPhotoAction',
                                                          related_name='comments_of_receive_card_action',
                                                          null=True)

    # reply_to =

    objects = CommentManager()

    class Meta:
        ordering = ['-created']

    def as_json(self):
        return dict(
            created=self.created,
            comment_id=self.id,
            comment=self.comment,
            user_who_comment_id=self.user_who_comment.id
        )





#-------------------------
#  helpers
def mills2datetime(ms):
    """
    convert mill seconds to datetime
    :param ms: mill seconds
    :return: datetime
    """
    if ms is None:
        return
    if ms == 0:
        return
    return datetime.datetime.fromtimestamp(int(ms/1000))


def datetime2milss(dt):
    """
    convert datetime to mill seconds
    :param dt: datetime object
    :return: mill seconds
    """
    return int(dt.strftime("%s") * 1000)