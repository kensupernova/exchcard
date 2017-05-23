#coding: utf-8

"""
主要是用户活动的数据模型, 与地址无关，不用Profile关联，而用正常的User
"""

from django.db import models
from django.db.models import Manager

# from django.contrib.auth import get_user_model # If used custom user mode
# User = get_user_model() #  自定义用户模型

from exchcard.models_profile import Card, CardPhoto, Profile


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
