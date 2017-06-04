#coding: utf-8
import json

from django.contrib.auth import get_user_model # If used custom user mode
from django.db.models import Q

from exchcard.models_profile import Profile, Follow, SentCardAction, ReceiveCardAction, AvatarPhoto
from exchcard_backend_api.serializers import SentCardActionSerializer, ReceiveActionSerializer

User = get_user_model()

from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView


@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticated, ])
def get_all_activities_of_my_followings(request, format=None):
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

        # try:
        followings = Follow.objects.filter(subject=user)

        if not followings.exists():
            return Response(json.dumps({
                "details": "You have no following"
            }))

        response_data = []
        for follow in followings:
            print "{0} following {1}".format(follow.subject.username, follow.user_being_followed.username)

            # 得到某个用户的所有活动
            user_being_followed = follow.user_being_followed
            profile_being_followed = Profile.objects.get(profileuser=user_being_followed)

            if AvatarPhoto.objects.filter(owner=profile_being_followed).exists():
                avatar_photo = AvatarPhoto.objects.filter(owner=profile_being_followed).\
                    order_by('-created')[0]
                avatar_url = avatar_photo.avatar.url
            else:
                avatar_photo = None
                avatar_url = "/static/images/default-avatar.jpg"

            sent_actions = SentCardAction.objects.filter(subject=user_being_followed)
            receive_actions = ReceiveCardAction.objects.filter(subject=user_being_followed)

            s_serializer = SentCardActionSerializer(sent_actions, many=True)
            r_serializer = ReceiveActionSerializer(receive_actions, many=True)

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


                # TODO: card_photo_url

                response_data.append(item)

        # TODO: sort by created


        return Response(json.dumps(response_data), status=status.HTTP_200_OK)

        # except:
        #     return Response({
        #         "details": "server error"
        #     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






