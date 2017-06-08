# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from exchcard.models_main import Card,CardPhoto, Profile, ReceiveCardAction, UploadCardPhotoAction
from exchcard.models_main import DianZan
from exchcard_backend_api.permissions import IsSenderStaffOrReadOnly
from exchcard_backend_api.serializers import CreateCardSerializer, CardSerializer, CardPhotoSerializer, \
    SentCardActionSerializer, ReceiveCardActionSerializer, UploadCardPhotoActionSerializer
from exchcard_backend_api.serializers import DianZanSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from utils import utils
from utils.utils import hash_file_name


## create and list cards
class CardList(generics.ListAPIView):
    queryset = Card.objects.all()
    lookup_field = ["pk"]
    serializer_class = CardSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                      IsSenderStaffOrReadOnly,)

##  get, put, patch and delete card detail
class CardDetail(generics.RetrieveAPIView):
    queryset = Card.objects.all()

    lookup_field = ["pk"]

    serializer_class = CardSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                      IsSenderStaffOrReadOnly,)

    def get_object(self):
        queryset = Card.objects.all()
        filter = {}
        filter["pk"] = self.kwargs["pk"]
        # query parameters
        # for field in self.multiple_lookup_fields:
        #     filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    # def perform_create(self, serializer):
    #     serializer.save(fromsender = self.request.user.exchcard_backend_api)
    #
    # def perform_update(self, serializer):
    #     serializer.save()
    #
    # def perform_destroy(self, instance):
    #     instance.delete()




################################################------------------------------------
# API VIEWS
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated, ])
def get_address_before_confirm_send_card(request):
    """
    仅仅得到一个地址，在用户发送请求寄送明信片时，不创建明信片
    :param request:
    :return:
    """
    if request.method == "GET":
        # the sender_id must be the current log in user exchcard_backend_api
        try:
            # TODO: smartly get recipient!!!
            randomProfile = Profile.objects.order_by("?").first()
            # profile_of_request_user = Profile.objects.get(profileuser=request.user)
            # randomProfile = profile_of_request_user

            response_data= {}
            response_data["card_name"] = utils.generateUniquePostcardName()
            response_data["torecipient_id"] = randomProfile.id
            response_data['name'] = randomProfile.profileaddress.name
            response_data['address'] = randomProfile.profileaddress.address
            response_data['postcode'] = randomProfile.profileaddress.postcode
            response_data['country'] = randomProfile.profileaddress.country

            # print "pre postal address information is {0}".format(response_data)

            return HttpResponse(json.dumps(response_data), content_type="application/json")

        except Profile.DoesNotExist:
            return Response({"details": "Profile of the request.user does not exit!"})


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated, ])
def confirm_send_card_no_photo(request):
    """
    用户确定发送，创建明信片, 可以有图片， 或者没有
    :param request:
    :return:
    """

    try:
        profile_of_logged_user = Profile.objects.get(profileuser=request.user)
    except Profile.DoesNotExist:
        return HttpResponse(json.dumps({
            "details": "Can not find profile of the logger user, possibly not address"
        }), status=status.HTTP_400_BAD_REQUEST)

    if request.method == "POST":
        # print request.data ## <QueryDict
        # print request.FILES # <MultiValueDict: {}>
        # if not key, raise MultiValueDictKeyError

        # has_photo_int = request.data["has_photo_int"]
        #
        # if has_photo_int == 1 or has_photo_int == "1":
        #     print "has photo"
        # else:
        #     print "not photo"

        card_name = request.data["card_name"]
        torecipient_id = request.data["torecipient_id"]

        # create a card, sent postcard action, no photo
        # activity_type_id = 1, SP

        # card = Card.objects.create_with_profile_ids(card_name=card_name,
        #                                             torecipient_id=torecipient_id,
        #                                             fromsender_id=profile_of_logged_user.id)
        #

        card, sent_card_no_photo_action = Card.objects.create_with_card_action_objs_returned(
            card_name=card_name,
            torecipient_id=torecipient_id,
            fromsender_id=profile_of_logged_user.id
        )


        card_s = CardSerializer(card, context={'request': request})
        action_s = SentCardActionSerializer(sent_card_no_photo_action, context={'request': request})

        return Response(
            {"card": card_s.data,
            "sent_card_action": action_s.data},
            status=status.HTTP_201_CREATED
        )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated, ])
def confirm_send_card_with_photo(request):
    """
    用户确定发送，创建明信片, 可以有图片， 或者没有
    :param request:
    :return:
    """
    try:
        profile_of_logged_user = Profile.objects.get(profileuser=request.user)
    except Profile.DoesNotExist:
        return HttpResponse(json.dumps({
            "details": "Can not find profile of the logger user, possibly not address"
        }), status=status.HTTP_400_BAD_REQUEST)

    if request.method == "POST":
        # print request.data ## <QueryDict
        # print request.FILES # <MultiValueDict: {}>

        # has_photo_int = request.data["has_photo_int"]
        #
        # if has_photo_int == 1 or has_photo_int == "1":
        #     print "has photo"
        # else:
        #     print "not photo"

        card_name = request.data["card_name"]
        torecipient_id = request.data["torecipient_id"]

        # create a card, cardphoto; sent postcard action with photo
        # activity_type_id = 2, SPP
        card_photo_file = request.FILES['card_photo']
        card_photo_file.name = hash_file_name(card_photo_file.name)

        # photo = CardPhoto(owner=profile_of_logged_user,
        #                   card_host=card,
        #                   card_photo=card_photo_file)
        # photo.save()

        card, sent_card_has_photo_action, card_photo = \
            Card.objects.create_with_card_action_photo_objs_returned(
            card_name=card_name, torecipient_id=torecipient_id, fromsender_id=profile_of_logged_user.id,
            card_photo_file=card_photo_file
        )

        card_s = CardSerializer(card, context={'request': request})
        action_s = SentCardActionSerializer(sent_card_has_photo_action)
        card_photo_s = CardPhotoSerializer(card_photo)

        return Response(
            {
                "card": card_s.data,
                 "sent_card_photo_action": action_s.data,
                 "card_photo": card_photo_s.data
             },
            status=status.HTTP_201_CREATED
        )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated, ])
def confirm_send_card(request):
    """
    用户确定发送，创建明信片, 可以有图片， 或者没有
    :param request:
    :return:
    """
    try:
        profile_of_logged_user = Profile.objects.get(profileuser=request.user)
    except Profile.DoesNotExist:
        return HttpResponse(json.dumps({
            "details": "Can not find profile of the logger user, possibly not address"
        }), status=status.HTTP_400_BAD_REQUEST)

    if request.method == "POST":
        print request.data ## <QueryDict
        print request.FILES # <MultiValueDict: {}>

        card_name = request.data["card_name"]
        torecipient_id = request.data["torecipient_id"]

        has_photo_int = request.data["has_photo_int"]

        if has_photo_int == 1 or has_photo_int == "1":
            print "sent a postcard has photo, SPP"
            # create a card, action, card photo;
            # sent postcard action with photo
            # activity_type_id = 2, SPP

            card_photo_file = request.FILES['card_photo']
            card_photo_file.name = hash_file_name(card_photo_file.name)

            # photo = CardPhoto(owner=profile_of_logged_user,
            #                   card_host=card,
            #                   card_photo=card_photo_file)
            # photo.save()

            card, sent_card_has_photo_action, card_photo = \
                Card.objects.create_with_card_action_photo_objs_returned(
                    card_name=card_name, torecipient_id=torecipient_id, fromsender_id=profile_of_logged_user.id,
                    card_photo_file=card_photo_file
                )

            card_s = CardSerializer(card, context={'request': request})
            action_s = SentCardActionSerializer(sent_card_has_photo_action)
            card_photo_s = CardPhotoSerializer(card_photo)

            return Response(
                {
                    "card": card_s.data,
                    "sent_card_photo_action": action_s.data,
                    "card_photo": card_photo_s.data
                },
                status=status.HTTP_201_CREATED
            )

        else:
            print "sent a postcard with not photo"
            # create a card, action;
            # activity_type_id = 1, SP

            card, sent_card_no_photo_action = Card.objects.create_with_card_action_objs_returned(
                card_name=card_name,
                torecipient_id=torecipient_id,
                fromsender_id=profile_of_logged_user.id
            )

            card_s = CardSerializer(card, context={'request': request})
            action_s = SentCardActionSerializer(sent_card_no_photo_action, context={'request': request})

            return Response(
                {"card": card_s.data,
                 "sent_card_action": action_s.data},
                status=status.HTTP_201_CREATED
            )






@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticated, ])
def add_new_card_no_photo(request):
    """
    Create a new card, initiated when user request a mailing address. not card photo!!!
    :param request:
    :return:
    """
    if request.method == "POST":
        ## the sender_id must be the current log in user exchcard_backend_api
        try:
            profile_of_request_user = Profile.objects.get(profileuser = request.user)

            # TODO: UNCOMMENT OUT!!
            # randomProfile = Profile.objects.order_by("?").first()
            randomProfile = profile_of_request_user # FOR DEBUG

            data = {}
            data["card_name"] = utils.generateUniquePostcardName()
            data["torecipient_id"] = randomProfile.id
            data["fromsender_id"] = profile_of_request_user.id

            card = Card.objects.create_with_profile_ids(card_name=data["card_name"],
                                                        torecipient_id=data["torecipient_id"],
                                                        fromsender_id=data["fromsender_id"])

            # print data

            data['torecipient'] = {}
            data['torecipient']['name'] = randomProfile.profileaddress.name
            data['torecipient']['address'] = randomProfile.profileaddress.address
            data['torecipient']['postcode'] = randomProfile.profileaddress.postcode
            data['id'] = card.id

            print "new card information is {0}".format(data)

            return Response(data, status=status.HTTP_201_CREATED)

        except Profile.DoesNotExist:
            Response({"details": "Profile of the request.user does not exit!"},
                     status=status.HTTP_404_FORBIDDEN)

        # serializer = CreateCardSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save() ## 创建了新明信片
        #
        #     data['torecipient'] = {}
        #     data['torecipient']['name'] = randomProfile.profileaddress.name
        #     data['torecipient']['address'] = randomProfile.profileaddress.address
        #     data['torecipient']['postcode'] = randomProfile.profileaddress.postcode
        #
        #     print "new card information is {0}".format(data)
        #
        #     return HttpResponse(json.dumps(data), content_type="application/json")
        #
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
@api_view(["POST", ])
@permission_classes([permissions.IsAuthenticated, ])
def receive_a_card_no_photo(request):
    """
    recevie a card from others
    :param request:
    :return: 
    """
    if request.method == "POST":
        data = request.data

        card_name = data["card_name"]
        profile_from_request_user = Profile.objects.get(profileuser
                                                   =request.user)
        ## check whether the exchcard_backend_api id in the request data is the the same
        ## with the one of the request

        try:
            card = Card.objects.get(card_name=card_name)
        except Card.DoesNotExist:
            return Response({"details":"card name is invalid"},
                        status=status.HTTP_404_NOT_FOUND)

        ## has_arrived is true, respond with ok
        if card.has_arrived:
            return Response({"details": "%s already registered" % card_name},
                            status= status.HTTP_400_BAD_REQUEST)

        recipient_profile_id = card.torecipient.id

        ## check wether the recipient id is the one of the request
        if profile_from_request_user.id == recipient_profile_id:
            receive_card_action, card_photo = card.mark_arrived(has_photo=False, card_photo_file=None)

            response_data = {}
            response_data['card_name'] = card.card_name
            response_data['arrived_time'] = card.arrived_time
            response_data['has_arrived'] = card.has_arrived
            response_data["card_host_id"] = card.id
            response_data["owner_id"] = profile_from_request_user.id

            action_s = ReceiveCardActionSerializer(receive_card_action)
            response_data["action"] = action_s.data

            # print response_data

            return Response(response_data, status=status.HTTP_201_CREATED)


        else:
            return Response({"details": "You are not the recipient of the card %s " % card_name},
                            status=status.HTTP_403_FORBIDDEN)



@api_view(["POST", ])
@permission_classes([permissions.IsAuthenticated, ])
@parser_classes([MultiPartParser, FormParser])
def receive_a_card_with_photo(request):
    """
    recevie a card from others, register a card
    :param request:
    :return:
    """
    # print request.data
    ## In REST, request.data = request.POST + request.FILES in django
    ## In REST, request.query_params = request.GET


    try:
        profile_from_request_user = Profile.objects.get(profileuser
                                                        =request.user)
    except Profile.DoesNotExist:
        return Response({"details": "profile is invalid! not registered user or not address"},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == "POST":
        #### add photo
        card_name = request.data["card_name"]
        # f = request.data['card_photo']
        card_photo_file = request.FILES['card_photo']
        card_photo_file.name = hash_file_name(card_photo_file.name)

        try:
            card = Card.objects.filter(card_name=card_name).first()
            if not card:
                return Response({"details": "card with post id is invalid"},
                                status=status.HTTP_404_NOT_FOUND)
        except Card.DoesNotExist:
            return Response({"details":"card with post id is invalid"},
                        status=status.HTTP_404_NOT_FOUND)

        ## has_arrived is true, respond with ok
        if card.has_arrived:
            return Response({"details": "%s already registered" % card_name},
                            status= status.HTTP_400_BAD_REQUEST)

        ## check wether the recipient id is the one of the request
        if profile_from_request_user.id == card.torecipient.id:
            receive_card_action, card_photo = card.mark_arrived(has_photo=True, card_photo_file=card_photo_file) # VERY IMPORTANT

            response_data= {}
            response_data['card_name'] = card.card_name
            response_data['arrived_time']=card.arrived_time
            response_data['has_arrived'] = card.has_arrived
            response_data["card_host_id"] = card.id
            response_data["owner_id"] = profile_from_request_user.id

            action_s = ReceiveCardActionSerializer(receive_card_action)
            response_data["action"] = action_s.data

            # photo = CardPhoto(owner=profile_from_request_user,
            #                   card_host=card,
            #                   card_photo=card_photo_file)
            # photo.save()

            response_data["card_photo_name"] = card_photo.card_photo.name
            response_data["card_photo_url"] = card_photo.card_photo.url

            return Response(response_data, status=status.HTTP_201_CREATED)

        else:
            return Response({"details": "You are not the recipient of the card %s " % card_name },
                        status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated, ])
@parser_classes([MultiPartParser, FormParser])
def upload_cardphoto(request):
    """
    Upload a photo for an card
    :param request:
    :return:
    """
    try:
        profile_from_request_user = Profile.objects.get(profileuser
                                                        =request.user)
    except Profile.DoesNotExist:
        return Response({"details": "Can not find profile"},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == "POST":

        card_name = request.data["card_name"]
        # f = request.data['card_photo']
        card_photo_file = request.FILES['card_photo']
        card_photo_file.name = hash_file_name(card_photo_file.name)

        # print card_name

        try:
            card = Card.objects.get(card_name=card_name)
        except Card.DoesNotExist:
            return Response({"details":"Card with post id %s is invalid" % card_name},
                        status=status.HTTP_404_NOT_FOUND)


        if profile_from_request_user.id == card.torecipient.id or \
            profile_from_request_user.id == card.fromsender.id:

            photo = CardPhoto(owner=profile_from_request_user,
                              card_host=card,
                              card_photo=card_photo_file)
            photo.save()

            name = photo.card_photo.name
            url = photo.card_photo.url
            card_photo = photo.card_photo

            response_data = {}
            response_data['card_name'] = card.card_name
            response_data["name_on_server"] = name
            response_data["url_on_server"] = url
            response_data["card_photo"] = card_photo
            response_data["card_host_id"] = card.id
            response_data["owner_id"] = profile_from_request_user.id

            print response_data

            return Response(response_data, status=status.HTTP_201_CREATED)

        else:
            return Response({"details": "You are neither sender nor recipient of the card!"},
                        status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated, ])
@parser_classes([MultiPartParser, FormParser])
def upload_cardphoto_afterwards_by_cardname(request, card_name):
    """
    Upload a photo for an card
    :param request:
    :param card_name:
    :return:
    """
    try:
        profile_from_request_user = Profile.objects.get(profileuser
                                                        =request.user)
    except Profile.DoesNotExist:
        return Response({"details": "Can not find profile"},
                            status=status.HTTP_404_NOT_FOUND)


    if card_name != request.data["card_name"]:
        return Response({"details": "card name in url %s != card name in request %s"
                                    % (card_name, request.data["card_name"])},
                        status=status.HTTP_400_BAD_REQUEST)

    if request.method == "POST":
        card_name = request.data["card_name"]
        # f = request.data['card_photo']
        card_photo_file = request.FILES['card_photo']
        card_photo_file.name = hash_file_name(card_photo_file.name)

        try:
            card = Card.objects.get(card_name=card_name)
        except Card.DoesNotExist:
            return Response({"details":"card with card name %s is invalid" % card_name},
                        status=status.HTTP_404_NOT_FOUND)

        if profile_from_request_user.id == card.torecipient.id or \
            profile_from_request_user.id == card.fromsender.id:

            photo = CardPhoto(owner=profile_from_request_user,
                              card_host=card,
                              card_photo=card_photo_file)
            photo.save()

            card_photo_serializer = CardPhotoSerializer(photo, context={'request': request})

            action = UploadCardPhotoAction(subject=request.user, card_actioned=card,
                                           card_photo_uploaded=photo)
            action.save()

            action_s = UploadCardPhotoActionSerializer(action)

            return Response(
                {
                    "card_photo":card_photo_serializer.data,
                    "action": action_s.data
                },
                status=status.HTTP_201_CREATED)

        else:
            return Response({"details": "You are neither sender nor recipient of the card!"},
                        status=status.HTTP_403_FORBIDDEN)



@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated, ])
@parser_classes([MultiPartParser, FormParser])
def upload_cardphoto_afterwards_by_id(request, pk):
    if request.method == "POST":
        try:
            profile_from_request = Profile.objects.get(profileuser=request.user)

            # pk为明信片的Id
            card_host = Card.objects.get(pk=int(pk))

            ### get the recipient and sender of the card
            recipient = card_host.torecipient
            sender = card_host.fromsender

            # 确保目前登录用户就是明信片的接受者
            if profile_from_request.id == recipient.id or profile_from_request.id == sender.id:
                f = request.FILES['cardphoto']
                f.name = utils.hash_file_name(f.name)

                photo = CardPhoto(owner=profile_from_request,
                                  card_host=card_host,
                                  card_photo=f)
                photo.save()

                name = photo.card_photo.name
                url = photo.card_photo.url

                serializer = CardPhotoSerializer(photo, context={'request': request})
                data = serializer.data
                data["name_on_server"] = name
                data["url_on_server"] = url

                return Response(data, status=status.HTTP_201_CREATED)
            else:
                Response({"details": "card recipient!= profileuser, sender !=profileuser",
                          "id1": recipient.id,
                          "id2": profile_from_request.id},
                         status= status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response({"details":"Current logged user's profile does not exist"},
                            status=status.HTTP_404_NOT_FOUND)

        except Card.DoesNotExist:
            return Response({"details": "Postcard with id %s does not exist" % pk},
                            status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated, ])
def card_check_is_arrived(request, pk):
    """
    Check whether a card has registered or not
    :param request:
    :return: true or false
    """
    try:
        card = Card.objects.get(pk=pk)

        return Response({
            "hasArrived": card.has_arrived,
            "isArrived": card.has_arrived
        })

    except Card.DoesNotExist:
        return Response({
            "details": "card with %s does not exit" % pk
        })


@api_view(["GET", "PUT", "DELETE", ])
@permission_classes([permissions.IsAuthenticated, IsSenderStaffOrReadOnly])
def update_destrory_card(request, pk, format=None):
    try:
        card = Card.objects.get(pk)
        origin = CreateCardSerializer(card)
    except Card.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":

        serializer = CardSerializer(card)
        return Response(serializer.data)

    if request.method == "PUT":
        # print "------------------------------"
        # print "update card"
        # print "pk = %s" % pk

        try:
            data = request.data
            # print "updated"
            # print data
            card.update(card_name=data['card_name'],
                        torecipient_id=data['torecipient_id'],
                        fromsender_id=data['fromsender_id'],
                        sent_time=data['sent_time'])

            ## hyperidentity field need context
            serializer = CardSerializer(card, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(origin.data, status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        return Response({"detail":"Delete is not supported"},
                        status = status.HTTP_403_FORBIDDEN)


@api_view(["GET", ])
@permission_classes([permissions.IsAuthenticated,])
def cards_feeds(request):
    ""
    # get news feed when user refresh page
    if request.method == "GET":
        try:
            profile_from_request_user = Profile.objects.get(profileuser=request.user)
        except:
            return Response({
                "detail": "no profiler"
            }, status= status.HTTP_404_NOT_FOUND)




