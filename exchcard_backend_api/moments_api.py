#coding: utf-8
import json
import datetime

from django.contrib.auth import get_user_model # If used custom user mode
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse

from exchcard.models_profile import Profile, Follow, SentCardAction, ReceiveCardAction, AvatarPhoto
from exchcard_backend_api.serializers import SentCardActionSerializer, ReceiveCardActionSerializer

User = get_user_model()

from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView


@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticated, ])
def get_all_activities_of_my_followings(request):
    """
    Get all the activities of my followings.
    :param request: request.data is empty
    :param format: could be json, xml, text
    :return: all activities categorized by activity_type
    """

    if request.method == "GET":

        # print request.query_params
        # print request.GET
        # DJANGO REST WAY
        # if request.query_params["start"]:
        #     print "start=%s" % request.query_params['start']
        # DJANGO WAY
        # if request.GET["start"]:
        #     print "start=%s" % request.GET['start']

        user = request.user

        followings = Follow.objects.filter(subject=user)

        if not followings.exists():
            return Response(json.dumps({
                "details": "You have no following"
            }))

        response_data = []
        for follow in followings:
            # print "{0} following {1}".format(follow.subject.email, follow.user_being_followed.email)

            # 得到某个用户的所有活动
            user_being_followed = follow.user_being_followed

            try:
                profile_being_followed = Profile.objects.get(profileuser=user_being_followed)
            except Profile.DoesNotExists:
                return JsonResponse({"details": "Profile dose not exists"})

            if AvatarPhoto.objects.filter(owner=profile_being_followed).exists():
                avatar_photo = AvatarPhoto.objects.filter(owner=profile_being_followed).\
                    order_by('-created')[0]
                avatar_url = avatar_photo.avatar.url
            else:
                # avatar_photo = None
                avatar_url = "/static/images/default-avatar.jpg"

            sent_actions = SentCardAction.objects.filter\
                (subject=user_being_followed) # sorted by created : early -> late
            receive_actions = ReceiveCardAction.objects.filter(subject=user_being_followed) # sorted by created : early -> late

            s_serializer = SentCardActionSerializer(sent_actions, many=True)
            r_serializer = ReceiveCardActionSerializer(receive_actions, many=True)

            # print "activities 1 %s" % s_serializer.data
            # print "activities 2 %s" % r_serializer.data

            s_data = s_serializer.data
            r_data = r_serializer.data

            for item in s_data:
                # print item
                item["activity_id"] = 1
                item["activity_type_id"] = 1
                item["activity_type"] = "SP"
                item["activity_short_name"] = "Sent a postcard"

                item["user_id_who_made_actions"] = user_being_followed.id
                item["user_email_who_made_actions"] = user_being_followed.email
                item["username_who_made_actions"] = user_being_followed.username

                item["avatar_url"] = avatar_url


                # TODO: card_photo_url

                response_data.append(item)

            for item in r_data:
                # print item
                item["activity_id"] = 2
                item["activity_type_id"] = 2
                item["activity_type"] = "RP"
                item["activity_short_name"] = "Receive a postcard"

                item["user_id_who_made_actions"] = user_being_followed.id
                item["user_email_who_made_actions"] = user_being_followed.email
                item["username_who_made_actions"] = user_being_followed.username

                item["avatar_url"] = avatar_url

                # print item['created']
                # 2017-05-29T12:50:33.495153Z
                # 2017-05-31T07:55:23.112844Z
                # time in local timezone
                # >> > datetime.datetime.now()
                # datetime.datetime(2017, 6, 5, 13, 13, 23, 103926)
                # time in UTC
                # >> > datetime.datetime.utcnow()
                # datetime.datetime(2017, 6, 5, 5, 13, 30, 287766)
                # >> > time.time()
                # 1496639972.792231

                # TODO: card_photo_url

                response_data.append(item)

        # datetime.datetime.strptime('2017-05-29T12:50:33.495153Z', '%Y-%m-%dT%H:%M:%S.%fZ')
        def f(a, b):
            atime = datetime.datetime.strptime(a['created'], '%Y-%m-%dT%H:%M:%S.%fZ')
            btime = datetime.datetime.strptime(b['created'], '%Y-%m-%dT%H:%M:%S.%fZ')

            # 从大到小
            dtime = btime - atime # datetime.timedelta
            return int(dtime.total_seconds())

        # import time
        # s = time.time()
        sorted_response = sorted(response_data, cmp=f)
        # print sorted_response
        # e = time.time()
        # print e - s

        # TODO: PAGINATION
        # TODO: GET THE MOST CURRENT

        # 错误的方法，前端只能通过JSON.parse(response), 才能得到JSON OBJECTS
        # return Response(json.dumps(sorted_response), status=status.HTTP_200_OK)

        # 正确地，把list, dict转成JSON
        return HttpResponse(json.dumps(sorted_response), content_type="application/json")
        # return JsonResponse(sorted_response, safe=False)









