# -*- coding: utf-8 -*-
"""
Activity就是就是各种Action
"""
from django.http import JsonResponse

from exchcard.models_main import Card,CardPhoto, Profile, SentCardAction
from exchcard.models_main import DianZan
from exchcard_backend_api.serializers import DianZanSerializer, SentCardActionSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


class SentCardActionListView(generics.ListAPIView):
    serializer_class = SentCardActionSerializer
    permission_classes = [permissions.IsAuthenticated,  ]
    queryset = SentCardAction.objects.all()


class SentCardActionDetailView(generics.RetrieveAPIView):
    queryset = SentCardAction.objects.all()
    serializer_class = SentCardActionSerializer

    lookup_field = ["pk"]

    permission_classes = [
        permissions.IsAuthenticated
    ]


#-----------------------------------------------------------


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated,])
def toggle_dianzan(request):
    """
    make dianzan
    :param request:
    :return:
    """
    user = request.user

    if request.method == "POST":
        request_data = request.data
        """
        得到数据格式
        {
            user_who_action_id: '',
            activity_type_id: '',
            activity_short_name: '',
            action_id:""
        }
        activity_type_id 可以确定是那种活动，SentCardAction, ReceiveCardAction, UploadCardPhotoAction,
        action_id + activity_type_id, 可以查询到被点赞的对象
        """
        user_who_zan_id = user.id
        if request_data.get('user_who_action_id', None) == user.id:
           print "You are dianzan your own action!"

        activity_type_id = request_data.get('activity_type_id', None)
        action_id = request_data.get('action_id', None)
        activity_short_name= request_data.get('activity_short_name', None)

        print 'action id: %s ' % action_id
        print 'activity_type_id: %s ' % activity_type_id
        print 'user_who_zan_id: %s ' % user_who_zan_id
        print 'activity_short_name: %s ' % activity_short_name

        #---------------------------
        # check whether the dianzan already exist,
        # the same user make dianzan to the same action.
        # if exist, toggle is_active
        # otherwise, create new dianzan

        if activity_type_id == 1 or activity_type_id == '1'\
                or activity_type_id == 2 or activity_type_id == "2":
            # SentCardAction, No photo
            # action = SentCardAction.objects.get(id=action_id)

            existing_dianzan = DianZan.objects.filter_by_action_id \
                (sent_card_action_zaned_id=action_id).filter(user_who_zan_id=user.id)

            if existing_dianzan.exists():
                dianzan = existing_dianzan.first()
                # dianzan.is_active = False
                # dianzan.save();
                dianzan.toggle_active()

            else:
                dianzan = DianZan.objects.create_with_ids(
                    user_who_zan_id=user_who_zan_id,
                    sent_card_action_zaned_id=action_id
                 )

        elif activity_type_id == 3 or activity_type_id == '3'\
                or activity_type_id == 4 or activity_type_id == "4":
            # ReceiveCardAction, No photo
            # action = ReceiveCardAction.objects.get(id=action_id)

            existing_dianzan = DianZan.objects.filter_by_action_id \
                (receive_card_action_zaned_id=action_id).filter(user_who_zan_id=user.id)
            if existing_dianzan.exists():
                dianzan = existing_dianzan.first()
                # dianzan.is_active = False
                # dianzan.save();
                dianzan.toggle_active()

            else:
                dianzan = DianZan.objects.create_with_ids(
                user_who_zan_id=user_who_zan_id,
                receive_card_action_zaned_id=action_id
            )

        elif activity_type_id == 5 or activity_type_id == '5'\
                or activity_type_id == 5 or activity_type_id == "5":
            # UploadCardPhotoAction, photo
            # action = UploadCardPhotoAction.objects.get(id=action_id)
            existing_dianzan = DianZan.objects.filter_by_action_id \
                (upload_cardphoto_action_zaned_id=action_id).filter(user_who_zan_id=user.id)
            if existing_dianzan.exists():
                dianzan = existing_dianzan.first()
                # dianzan.is_active = False
                # dianzan.save();
                dianzan.toggle_active()

            else:
                dianzan = DianZan.objects.create_with_ids(
                    user_who_zan_id=user_who_zan_id,
                    upload_cardphoto_action_zaned_id=action_id
                )

        else:
            dianzan = None

        if dianzan:
            serializer = DianZanSerializer(dianzan)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({
                "details": "Fail to dianzan"
            }, safe=True)








