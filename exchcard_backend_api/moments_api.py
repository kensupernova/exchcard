# coding: utf-8
import json
import datetime

from django.contrib.auth import get_user_model # If used custom user mode
User = get_user_model()

from django.http import HttpResponse
from django.http import JsonResponse

from exchcard.models_main import Profile, Follow, SentCardAction, ReceiveCardAction, AvatarPhoto, UploadCardPhotoAction, \
    DianZan
from exchcard_backend_api.serializers import SentCardActionSerializer, ReceiveCardActionSerializer, \
    UploadCardPhotoActionSerializer, DianZanSerializer
from utils.utils import compare_created_early_to_late

from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes


@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticated, ])
def get_all_activities_of_my_followings(request):
    """
    Get all the activities of my followings.
    :param request: request.data is empty
    :param format: could be json, xml, text
    :return: all activities categorized by activity_type， SP, SPP, RP, RPP, UPP
    """

    # print request.query_params
    # print request.GET
    # DJANGO REST WAY
    # if request.query_params["start"]:
    #     print "start=%s" % request.query_params['start']
    # DJANGO WAY
    # if request.GET["start"]:
    #     print "start=%s" % request.GET['start']

    user = request.user
    # 用户所有的关注用户
    followings = Follow.objects.filter(subject=user)

    if not followings.exists():
        return HttpResponse(json.dumps({
            "details": "You have no followings"
        }), content_type="application/json", status=status.HTTP_204_NO_CONTENT)

    if request.method == "GET":

        response_data = []

        for follow in followings:
            print ("{0} following {1}".format(follow.subject.email, follow.user_being_followed.email))

            user_being_followed = follow.user_being_followed

            try:
                profile_being_followed = Profile.objects.get(profileuser=user_being_followed)
            except Profile.DoesNotExists as e:
                return JsonResponse({"details": "Profile dose not exists"})

            # 得到被关注用户的avatar photo
            if AvatarPhoto.objects.filter(owner=profile_being_followed).exists():
                avatar_photo = AvatarPhoto.objects.filter(owner=profile_being_followed).\
                    order_by('-created').first()
                avatar_url = avatar_photo.avatar.url
            else:
                # avatar_photo = None
                avatar_url = "/static/images/default-avatar.jpg"

            # 得到被关注用户的所有actions, SP, SPP, RP, RPP, UPP

            sent_actions = SentCardAction.objects.filter \
                (subject=user_being_followed)  # sorted by created : early -> late
            receive_actions = ReceiveCardAction.objects.filter\
                (subject=user_being_followed)
            upload_cardphoto_actions = UploadCardPhotoAction.objects.filter\
                (subject=user_being_followed)

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

                item["user_id_who_made_actions"] = user_being_followed.id
                item["user_email_who_made_actions"] = user_being_followed.email
                item["username_who_made_actions"] = user_being_followed.username

                item["avatar_url"] = avatar_url

                # 活动得到的feedback, dianzan
                active_dianzans = DianZan.objects.filter_by_action_id(sent_card_action_zaned_id=obj.id)\
                    .filter(is_active=True)

                if active_dianzans:
                    dianzans_serializer = DianZanSerializer(active_dianzans, many=True)
                    item["feedback"]={}
                    item["feedback"]["dianzans"] = dianzans_serializer.data

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

                item["user_id_who_made_actions"] = user_being_followed.id
                item["user_email_who_made_actions"] = user_being_followed.email
                item["username_who_made_actions"] = user_being_followed.username

                item["avatar_url"] = avatar_url

                active_dianzans = DianZan.objects.filter_by_action_id(receive_card_action_zaned_id=obj.id)\
                    .filter(is_active=True)

                if active_dianzans:
                    dianzans_serializer = DianZanSerializer(active_dianzans, many=True)
                    item["feedback"] = {}
                    item["feedback"]["dianzans"] = dianzans_serializer.data
                response_data.append(item)

            for obj in upload_cardphoto_actions:
                # print item
                item = UploadCardPhotoActionSerializer(obj).data
                # print item

                item["activity_type_id"] = 5
                item["activity_type"] = "UPP"
                item["activity_short_name"] = "upload a postcard with photo"

                item["user_id_who_made_actions"] = user_being_followed.id
                item["user_email_who_made_actions"] = user_being_followed.email
                item["username_who_made_actions"] = user_being_followed.username

                item["avatar_url"] = avatar_url

                # print obj
                card_photo = obj.card_photo_uploaded
                if card_photo:
                    item['has_photo'] = True
                    item['card_photo_url'] = card_photo.card_photo.url
                    item['card_photo_name'] = card_photo.card_photo.name

                #---------------
                active_dianzans = DianZan.objects.filter_by_action_id(upload_cardphoto_action_zaned_id=obj.id)\
                    .filter(is_active=True)

                if active_dianzans:
                    dianzans_serializer = DianZanSerializer(active_dianzans, many=True)
                    # 点赞总数
                    # count = len(dianzans)
                    # 点赞用户字符串

                    item["feedback"] = {}
                    item["feedback"]["dianzans"] = dianzans_serializer.data

                response_data.append(item)

        # start = time.time()
        sorted_response = sorted(response_data, cmp=compare_created_early_to_late)
        # end = time.time()
        # print "time taken to sort: {0} micro seconds".format(int((end - start)*1000))

        # TODO: PAGINATION
        # TODO: GET THE MOST CURRENT

        # 错误的方法，前端得到string, 只能通过JSON.parse(response-in-string), 才能得到JSON OBJECTS
        # return Response(json.dumps(sorted_response), status=status.HTTP_200_OK)

        # 正确地，把list, dict转成JSON
        return HttpResponse(json.dumps(sorted_response), content_type="application/json")
        # return JsonResponse(sorted_response, safe=False) # not-dict data, must safe=False


def f(a, b):
    """
    比较两个时间的早晚
    :param a: a['created'] has datetime string in format '%Y-%m-%dT%H:%M:%S.%fZ'
    :param b:
    :return:
    """
    atime = datetime.datetime.strptime(a['created'], '%Y-%m-%dT%H:%M:%S.%fZ')
    btime = datetime.datetime.strptime(b['created'], '%Y-%m-%dT%H:%M:%S.%fZ')

    # 从大到小 -- 后面参数减前面参数
    # 从早到晚
    dtime = btime - atime  # datetime.timedelta
    return int(dtime.total_seconds())






