# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

import utils
from exchcard.models import Card, DianZan, CardPhoto
from exchcard.models import Profile
from exchcard_backend_api.permissions import IsSenderStaffOrReadOnly
from exchcard_backend_api.serializers import CreateCardSerializer, CardSerializer
from exchcard_backend_api.serializers import DianZanSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.reverse import reverse

exchcard_api_endpoint = "http://exchcard_backend_api.applinzi.com/exchcard_backend_api/"
@permission_classes([permissions.AllowAny, ])
@api_view(["GET",])
def api_root(request, format=None):
    return Response({
        "auth": reverse("auth", request=request, format=format),
        "login": reverse("login", request=request, format=format),
        "logout": reverse("logout", request=request, format=format),
        "exchcard_backend_api-user-address-register": reverse("exchcard_backend_api-user-address-register", request=request, format=format),
        "exchcard_backend_api-user-address-register2": reverse("exchcard_backend_api-user-address-register2", request=request, format=format),
        "user-list": reverse("user-list", request=request, format=format),
        "user-register": reverse("user-register", request=request, format=format),
        # "user-detail": reverse("user-detail", request=request, format=format),
        "user-detail": exchcard_api_endpoint + "api/users/(?P<pk>[0-9]+)/",

        "address-list": reverse("address-list", request=request, format=format),
        "address-register": reverse("address-register", request=request, format=format),
        "address-random": reverse("address-random", request=request, format=format),

        # "address-get-id": reverse("address-get-id", request=request, format=format),
        # "address-get-name": reverse("address-get-name", request=request, format=format),
        # "address-update-with-profile-id": reverse("address-update-with-profile-id", request=request, format=format),
        "address-get-id": exchcard_api_endpoint + "api/address/get/(?P<pk>[0-9]+)/",
        "address-get-name": exchcard_api_endpoint + "api/address/get/name/(?P<name>.+)/",
        "address-update-with-profile-id": exchcard_api_endpoint+"api/address/update/(?P<id>[0-9]+)/",

        "profile-list": reverse("profile-list", request=request, format=format),
        # "profile-detail": reverse("profile-detail", request=request, format=format),
        "profile-detail": exchcard_api_endpoint+"api/profiles/(?P<pk>[0-9]+)/",

        "profile-register": reverse("profile-register", request=request, format=format),
        "profile-register-with-ids": reverse("profile-register-with-ids", request=request, format=format),
        "profile-update": reverse("profile-update", request=request, format=format),
        "profile-getone-for-card": reverse("profile-getone-for-card", request=request, format=format),
        # "profile-get-cards": reverse("profile-get-cards", request=request, format=format),
        # "profile-avatarphoto-upload": reverse("profile-avatarphoto-upload", request=request, format=format),
        # "profile-avatarphoto-uploadf": reverse("profile-avatarphoto-uploadf", request=request, format=format),
        "profile-get-cards": exchcard_api_endpoint + "api/profiles/(?P<pk>[0-9]+)/getcards/",
        "profile-avatarphoto-upload": exchcard_api_endpoint + "api/profiles/(?P<pk>[0-9]+)/avatar/",
        "profile-avatarphoto-uploadf": exchcard_api_endpoint + "api/profiles/(?P<pk>[0-9]+)/avatarf/",

        "avatarphoto-list": reverse("avatarphoto-list", request=request, format=format),
        # "avatarphoto-detail": reverse("avatarphoto-detail", request=request, format=format),
        "avatarphoto-detail": exchcard_api_endpoint +"api/profiles/photos/(?P<pk>[0-9]+)/",

        "card-list": reverse("card-list", request=request, format=format),
        # "card-detail": reverse("card-detail", request=request, format=format),
        "card-detail": exchcard_api_endpoint + "api/cards/(?P<pk>[0-9]+)/",
        "card-add2": reverse("card-add2", request=request, format=format),
        "card-add": reverse("card-add", request=request, format=format),
        "card-receive": reverse("card-receive", request=request, format=format),
        "card-receive-with-photo": reverse("card-receive-with-photo", request=request, format=format),
        # "card-update": reverse("card-update", request=request, format=format),
        # "card-check-arrive": reverse("card-check-arrive", request=request, format=format),

        "card-update":exchcard_api_endpoint +"api/cards/(?P<pk>[0-9]+)/update/",
        "card-check-arrive": exchcard_api_endpoint +"api/cards/(?P<pk>[0-9]+)/hasarrived/",
        "card-dianzan": exchcard_api_endpoint + "api/cards/(?P<pk>[0-9]+)/cardphotos/(?P<photoid>[0-9]+)/dianzan/",
        "card-dianzans": exchcard_api_endpoint + "api/cards/(?P<pk>[0-9]+)/cardphotos/(?P<photoid>[0-9]+)/dianzans/",
        "card-dianzans-2": exchcard_api_endpoint + "api/cards/(?P<pk>[0-9]+)/dianzans2/",
        "card-cardphoto": exchcard_api_endpoint + "api/cards/(?P<pk>[0-9]+)/cardphoto/",
        # "card-dianzan": reverse("card-dianzan", request=request, format=format),
        # "card-dianzans": reverse("card-dianzans", request=request, format=format),
        # "card-dianzans-2": reverse("card-dianzans-2", request=request, format=format),
        # "card-cardphoto": reverse("card-cardphoto", request=request, format=format),

        "cards-feed": reverse("cards-feed", request=request, format=format),

    })


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


# all the
class DianzanListView(generics.ListAPIView):
    serializer_class = DianZanSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        pk = self.kwargs['pk']
        card = Card.objects.filter(id=int(pk))
        return DianZan.objects.filter(card_by_dianzan=card)

class DianzanRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DianZan.objects.all()
    serializer_class =  DianZanSerializer
    permission_classes = [permissions.IsAuthenticated, ]

################################################ API VIEWS



@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticated, ])
def api_add_new_card(request):
    if request.method == "POST":
        ## the sender_id must be the current log in user exchcard_backend_api
        profile_from_request_user = Profile.objects.get(profileuser = request.user)

        randomProfile = Profile.objects.order_by("?").first()

        data = {}
        data["card_name"] = utils.generatePostCardName()
        data["torecipient_id"] = int(randomProfile.id)
        data["fromsender_id"] = int(profile_from_request_user.id)

        print data
        serializer = CreateCardSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            data['torecipient'] = {}
            data['torecipient']['name'] = randomProfile.profileaddress.name
            data['torecipient']['address'] = randomProfile.profileaddress.address
            data['torecipient']['postcode'] = randomProfile.profileaddress.postcode
            print data

            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST", ])
@permission_classes([permissions.IsAuthenticated, ])
def api_receive_a_card(request):
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
            card.mark_arrived()

            data= {}
            data['card_name'] = card.card_name
            data['arrived_time']=card.arrived_time
            data['has_arrived'] = card.has_arrived

            return Response(data,
                        status=status.HTTP_200_OK)

        else:
            return Response({"details": "exchcard_backend_api id!= card recipient exchcard_backend_api id, card name ",
                         "id1":profile_from_request_user.id ,
                        "id2:":recipient_profile_id },
                        status=status.HTTP_403_FORBIDDEN)

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated, ])
def api_card_check_isarrived(request, pk):
    """
    Check whether a card has registered or not
    :param request:
    :return: true or false
    """
    try:
        card = Card.objects.get(pk=pk)

        return Response({
            "hasArrived": card.has_arrived
        })

    except Card.DoesNotExist:
        return Response({
            "details": "card with %s does not exit" % pk
        })



@api_view(["POST", ])
@permission_classes([permissions.IsAuthenticated, ])
@parser_classes([MultiPartParser, FormParser])
def api_receive_a_card_with_photo(request):
    """
    recevie a card from others
    :param request:
    :return:
    """
    if request.method == "POST":
        #### add photo
        print request.data
        print request.FILES

        card_name = request.data["card_name"]
        profile_from_request_user = Profile.objects.get(profileuser
                                                   =request.user)
        ## check whether the exchcard_backend_api id in the request response_data is the the same
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
            # card.mark_arrived()

            response_data= {}
            response_data['card_name'] = card.card_name
            response_data['arrived_time']=card.arrived_time
            response_data['has_arrived'] = card.has_arrived


            photo = CardPhoto(owner=profile_from_request_user,
                              card_host=card,
                              card_photo=request.data['card_photo'])
            photo.save()

            name_on_s3 = photo.card_photo.name
            ## sae s3 does not support path
            url_on_s3 = photo.card_photo.url

            ##bucket = utils.get_bucket()
            ##bucket.put_object("%s-avatar.jpg"%pk, request.response_data['avatar'])

            ### related to the photo of card
            response_data["name_on_server"] = name_on_s3
            response_data["url_on_server"] = url_on_s3
            response_data["card_host_id"] = card.id
            response_data["owner_id"] = profile_from_request_user.id

            print response_data

            return Response(response_data, status=status.HTTP_201_CREATED)

        else:
            return Response({"details": "exchcard_backend_api id!= card recipient exchcard_backend_api id, card name ",
                         "id1":profile_from_request_user.id ,
                        "id2:":recipient_profile_id },
                        status=status.HTTP_403_FORBIDDEN)


@api_view(["GET","PUT", "DELETE", ])
@permission_classes([permissions.IsAuthenticated, IsSenderStaffOrReadOnly])
def api_update_destrory_card(request, pk, format=None):
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

##################################################
### add dianzan to a card
@api_view(["GET","PUT", "DELETE", "POST", ])
@permission_classes([permissions.IsAuthenticated,])
def api_card_dianzan(request, pk):
    profile_from_user = Profile.objects.get(profileuser=request.user)
    try:
        card = Card.objects.get(id=int(pk))
    except Card.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = request.data
    if request.method == 'POST':
        card_by_dianzan_id = card.id,
        person_who_dianzan_id = profile_from_user.id

        ## check whether had been dianzan already
        if DianZan.objects.filter(person_who_dianzan = profile_from_user, card_by_dianzan = card).exists():
            DianZan.objects.filter(person_who_dianzan = profile_from_user, card_by_dianzan = card).delete()
            return Response({"detail": "already dianzan"})
        else:
            zan = DianZan.objects.create_with_ids(card_by_dianzan_id=card.id,
                                                person_who_dianzan_id=profile_from_user.id)


            serializer = DianZanSerializer(zan)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    if request.method == "DELETE":
        zan = DianZan.objects.filter(card_by_dianzan_id = data['card_by_dianzan_id'])
        zan.delete()

    if request.method == 'GET':
        zan = DianZan.objects.filter(card_by_dianzan_id=data['card_by_dianzan_id'])
        serializer = DianZanSerializer(zan)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET", ])
@permission_classes([permissions.IsAuthenticated,])
def api_card_dianzans(request, pk):
    pk = int(pk)
    try:
        card = Card.objects.get(id=pk)
    except Card.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        zans = DianZan.objects.filter(card_by_dianzan_id =pk)
        results = [obj.as_json() for obj in zans]
        return Response(results, status= status.HTTP_200_OK)

#


@api_view(["GET", ])
@permission_classes([permissions.IsAuthenticated,])
def api_cardsfeed(request):
    ""
    # get news feed when user refresh page
    if request.method == "GET":
        try:
            profile_from_request_user = Profile.objects.get(profileuser=request.user)
        except:
            return Response({
                "detail": "no profiler"
            }, status= status.HTTP_404_NOT_FOUND)




