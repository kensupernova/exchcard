#coding: utf-8
from django.db import models
from django.db.models import Manager

from exchcard.models_main import Card, CardPhoto, Profile


class DianZanManager(Manager):
    ""


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

        # save !! important
        obj.save(using=self._db)
        return obj



#--------------------------------------------

class DianZan(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user_who_zan = models.ForeignKey('XUser',
                                         related_name='dianzans_by_user',
                                         null=False)

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