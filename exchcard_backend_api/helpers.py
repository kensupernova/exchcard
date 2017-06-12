#coding: utf-8

import json
import datetime

from django.contrib.auth import get_user_model # If used custom user mode
User = get_user_model()

from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse

from exchcard.models_main import Profile, Follow, SentCardAction, ReceiveCardAction, AvatarPhoto, UploadCardPhotoAction
from exchcard_backend_api.serializers import SentCardActionSerializer, ReceiveCardActionSerializer, \
    UploadCardPhotoActionSerializer
from utils.utils import compare_created_early_to_late


def get_all_activities_of_a_user(user):
    """
    取得用户的所有活动，扁平化处理，
    :param user: 活动的subject
    :return: 列表
    """
    try:
        profile = Profile.objects.get(profileuser=user)
    except Profile.DoesNotExists:
        return JsonResponse({"details": "Profile dose not exists"})

    # 得到被关注用户的avatar photo
    if AvatarPhoto.objects.filter(owner=profile).exists():
        avatar_photo = AvatarPhoto.objects.filter(owner=profile). \
            order_by('-created').first()
        avatar_url = avatar_photo.avatar.url
    else:
        # avatar_photo = None
        avatar_url = "/static/images/default-avatar.jpg"



    # 得到被关注用户的所有actions, SP, SPP, RP, RPP, UPP

    sent_actions = SentCardAction.objects.filter \
        (subject=user)  # sorted by created : early -> late
    receive_actions = ReceiveCardAction.objects.filter \
        (subject=user)
    upload_cardphoto_actions = UploadCardPhotoAction.objects.filter \
        (subject=user)

    # s_serializer = SentCardActionSerializer(sent_actions, many=True)
    # r_serializer = ReceiveCardActionSerializer(receive_actions, many=True)
    # u_serializer = UploadCardPhotoActionSerializer(upload_cardphoto_actions, many=True)
    #
    # # print "activities 1 %s" % s_serializer.data
    # # print "activities 2 %s" % r_serializer.data
    # # print "activities 3 %s" % u_serializer.data
    #
    #
    # s_data = s_serializer.data
    # r_data = r_serializer.data
    # u_data = u_serializer.data

    response_data = []
    # 所有数据，扁平化处理
    for obj in sent_actions:
        item = SentCardActionSerializer(obj).data
        # print item
        if item['has_photo']:
            item["activity_type_id"] = 2
            item["activity_type"] = "SPP"
            item["activity_short_name"] = "Sent a postcard with photo"

            card_photo = obj.card_sent_photo

            if card_photo:
                item['has_photo'] = True
                item['card_photo_url'] = card_photo.card_photo.url
                item['card_photo_name'] = card_photo.card_photo.name

        else:
            item['has_photo'] = False
            item["activity_type_id"] = 1
            item["activity_type"] = "SP"
            item["activity_short_name"] = "Sent a postcard no photo"

        item["user_id_who_made_actions"] = user.id
        item["user_email_who_made_actions"] = user.email
        item["username_who_made_actions"] = user.username

        item["avatar_url"] = avatar_url

        response_data.append(item)

    for obj in receive_actions:
        # print item
        item = ReceiveCardActionSerializer(obj).data
        # print item
        if item['has_photo']:
            item["activity_type_id"] = 4
            item["activity_type"] = "RPP"
            item["activity_short_name"] = "Receive a postcard with photo"

            card_photo = obj.card_received_photo
            if card_photo:
                item['has_photo'] = True
                item['card_photo_url'] = card_photo.card_photo.url
                item['card_photo_name'] = card_photo.card_photo.name

        else:
            item['has_photo'] = True
            item["activity_type_id"] = 3
            item["activity_type"] = "RP"
            item["activity_short_name"] = "Receive a postcard no photo"

        item["user_id_who_made_actions"] = user.id
        item["user_email_who_made_actions"] = user.email
        item["username_who_made_actions"] = user.username

        item["avatar_url"] = avatar_url

        response_data.append(item)

    for obj in upload_cardphoto_actions:
        # print item
        item = UploadCardPhotoActionSerializer(obj).data
        # print item

        item["activity_type_id"] = 5
        item["activity_type"] = "UPP"
        item["activity_short_name"] = "upload a postcard with photo"

        item["user_id_who_made_actions"] = user.id
        item["user_email_who_made_actions"] = user.email
        item["username_who_made_actions"] = user.username

        item["avatar_url"] = avatar_url

        card_photo = obj.card_photo_uploaded
        if card_photo:
            item['has_photo'] = True
            item['card_photo_url'] = card_photo.card_photo.url
            item['card_photo_name'] = card_photo.card_photo.name

        response_data.append(item)


    sorted_response = sorted(response_data, cmp=compare_created_early_to_late)

    return sorted_response