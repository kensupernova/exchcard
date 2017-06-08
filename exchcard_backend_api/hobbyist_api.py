# -*- coding: utf-8 -*-
"""
提供发烧友需要的各种REST API
"""

import json

from django.contrib.auth import get_user_model # If used custom user mode
from django.http import HttpResponse
from django.http import JsonResponse

User = get_user_model()

from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from exchcard.models_main import Address, Profile, AvatarPhoto, SentCardAction, ReceiveCardAction, Follow
from exchcard.models import XUser

from exchcard_backend_api.helpers import get_all_activities_of_user

def getAvatarInfoByProfile(profile):
    """
    得到最新的用户的avatar信息
    """
    photos = AvatarPhoto.objects.filter(owner=profile).order_by('-created')  ## 得到最新添加图片

    if len(photos) > 1:
        photo = photos[0]
    elif len(photos) == 1:
        photo = photos.first()
    elif len(photos) < 1:
        # print "no avatar photo, use default"
        return {
            "avatar_url": "/static/images/default-avatar.jpg",
            "avatar": "/static/images/default-avatar.jpg",
            "avatarHasBaseUrl": 0
        }

    # serializer = AvatarPhotoSerializer(photo)
    # serializer.is_valid()
    # data = serializer.validated_data

    data = {}
    data["avatar"] = photo.avatar.url
    data["avatar_url"] = photo.avatar.url
    data["avatarHasBaseUrl"] = 0

    return data




def getBasicTextInfoByProfile(profile):
    address = Address.objects.get(id=profile.profileaddress.id)

    text_info = {}
    text_info['name'] = address.name
    text_info['city'] = address.city
    text_info['country'] = address.country
    text_info['postcards_index'] = u'10'
    text_info['ranking'] = u"1"
    return text_info


def getAvatarBasicTextByProfile(profile):
    avatar_info = getAvatarInfoByProfile(profile)
    text_info = getBasicTextInfoByProfile(profile)

    return {
        "avatar_info": avatar_info,
        "text_info": text_info,
        "profile_id": profile.id,
        "user_id": profile.profileuser.id,
        "user_email": profile.profileuser.email,
        "username": profile.profileuser.username
    }





@api_view(["GET", ])
@permission_classes([permissions.IsAuthenticated, ])
def get_basic_info_of_hobbyist_list(request, number, format=None):
    """
    得到注册用户的基本信息，管理员除外。
    TODO: 因为可能用户很多，所以要进行设计，一部分一部分传输。分页处理。
    :param request:
    :param number: 第几页
    :param format:
    :return: 包括邮寄地址的名字，城市，国家名，明信片指数，用户等级, 已经头像
    """

    logged_user = request.user

    profiles = Profile.objects.all().order_by('created')

    count = len(profiles)
    number = int(number)
    items_per_page = 20 # row4 * col5
    start = (number-1)*items_per_page
    end = number*items_per_page
    end = count if end > count else end ##

    profiles_paged = profiles[start: end]

    response_data = []
    for f in profiles_paged:
        item = getAvatarBasicTextByProfile(f)
        response_data.append(item)
    # print response_data

    return Response(json.dumps(response_data), status=status.HTTP_200_OK)


@api_view(["GET", ])
@permission_classes([permissions.IsAuthenticated, ])
def get_all_basic_info_of_other_user(request, user_id):
    """
    得到访问用户页面的所有基本信息，包括头像信息，文字信息
    :param request: data is null
    :param user_id: user id of the other user who logged user visit.
    :return:
    """
    if request.user.id == user_id:
        print "你在访问自己的页面"

    try:
        other_user = XUser.objects.get(id=user_id)
        profile_of_other_user = Profile.objects.get(profileuser=other_user)
        data = getAvatarBasicTextByProfile(profile_of_other_user)

        logged_user = request.user ## 登录用户就是自己
        # 登录用户关注了此另外用户
        # 另外用户就是自己现在访问的用户hobbyist
        # VERY IMPORTANT
        # 不要用count来确认是否存在
        if Follow.objects.filter(subject=logged_user, user_being_followed=other_user).exists():
            data["isFollowingHim"] = True
            data["isFollowingHimInt"] = 1
            data["isFollowingHimBool"] = True
        else:
            data["isFollowingHim"] = False
            data["isFollowingHimInt"] = 0
            data["isFollowingHimBool"] = False

        return Response(data, status=status.HTTP_200_OK)

    except XUser.DoesNotExist:
        return Response({"details": "can not find user with user ID = %s" % user_id},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Profile.DoesNotExist:
        return Response({"details": "can not find profile with user ID = %s" % user_id},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET", ])
@permission_classes([permissions.IsAuthenticated, ])
def get_all_activities_of_other_user(request, user_id):
    """
    访问其他用户个人主页时，得到该用户所有活动
    :param request:
    :param user_id:
    :return:
    """
    if request.user.id == user_id:
        print "你在访问自己的页面"

    try:
        user = XUser.objects.get(id=user_id)

        # sent_actions = SentCardAction.objects.filter(subject=user)
        # receive_actions = ReceiveCardAction.objects.filter(subject=user)
        #
        # s_serializer = SentCardActionSerializer(sent_actions, many=True)
        # r_serializer = ReceiveCardActionSerializer(receive_actions, many=True)
        #
        # # print "activities 1 %s" % s_serializer.data
        # # print "activities 2 %s" % r_serializer.data
        #
        # s_data = s_serializer.data
        # r_data = r_serializer.data
        #
        # response_data = []
        # for item in s_data:
        #     item["activity_id"] = 1
        #     item["activity_type_id"] = 1
        #     item["activity_type"] = "SP"
        #     item["activity_short_name"] = "Sent a postcard"
        #
        #     response_data.append(item)
        #
        # for item in r_data:
        #     item["activity_id"] = 3
        #     item["activity_type_id"] = 3
        #     item["activity_type"] = "RP"
        #     item["activity_short_name"] = "Receive a postcard"
        #
        #     response_data.append(item)
        #
        # sorted_response = sorted(response_data, cmp=compare_created_early_to_late)

        sorted_response = get_all_activities_of_user(user)

        return HttpResponse(json.dumps(sorted_response), content_type="application/json")
        # return JsonResponse(sorted_response)

    except XUser.DoesNotExist:
        return Response({"details": "can not find user with user ID = %s" % user_id},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except SentCardAction.DoesNotExist:
        return Response({"details": "can not find actions of user with user ID = %s" % user_id},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET", ])
@permission_classes([permissions.IsAuthenticated, ])
def get_single_activity_detail_of_other_user(request, user_id, action_id):
    """
    get the activity detail of other user
    :param request:
    :param user_id:
    :param action_id:
    :return:
    """




#-----------------------------------------------------------------------------------------------
