# -*- coding: utf-8 -*-
"""
提供发烧友需要的各种REST API
"""

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json

from django.contrib.auth import get_user_model # If used custom user mode
from django.http import HttpResponse

from exchcard_backend_api.serializers import AddressSerializer2, AvatarPhotoSerializer
from rest_framework import permissions
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes

from exchcard.models_profile import Address, Profile, AvatarPhoto
from rest_framework.response import Response

User = get_user_model()

@api_view(["GET", ])
@permission_classes([permissions.IsAuthenticated, ])
def get_hobbyist_list_basic_info(request, number, format=None):
    """
    得到注册用户的基本信息，管理员除外。
    TODO: 因为可能用户很多，所以要进行设计，一部分一部分传输。分页处理。
    :param request:
    :param number: 第几页
    :param format:
    :return: 包括邮寄地址的名字，城市，国家名，明信片指数，用户等级, 已经头像
    """

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


def getCurrentAvatarInfoByProfile(profile):
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
    avatar_info = getCurrentAvatarInfoByProfile(profile)
    text_info = getBasicTextInfoByProfile(profile)

    return {
        "avatar_info": avatar_info,
        "text_info": text_info,
        "profile_id": profile.id,
        "user_id": profile.profileuser.id,
        "user_email": profile.profileuser.email
    }


class JSONResponse(HttpResponse):
    """docstring for JSONRenderer"""
    '''
    将HttpResponse对象相应的内容转化为json
    '''

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)