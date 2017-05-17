# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

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
from utils import utils


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


# All the dianzan of a postcard
class DianzanListView(generics.ListAPIView):
    serializer_class = DianZanSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        cardid = self.kwargs['cardid']
        card = Card.objects.filter(id=int(cardid))
        return DianZan.objects.filter(card_by_dianzan=card)


class DianzanRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DianZan.objects.all()
    serializer_class =  DianZanSerializer
    permission_classes = [permissions.IsAuthenticated, ]

################################################------------------------------------
# API VIEWS

@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticated, ])
def add_new_card(request):
    """
    Create a new card, initiated when user request a mailing address.
    :param request:
    :return:
    """
    if request.method == "POST":
        ## the sender_id must be the current log in user exchcard_backend_api
        profile_of_request_user = Profile.objects.get(profileuser = request.user)

        randomProfile = Profile.objects.order_by("?").first()

        data = {}
        data["card_name"] = utils.generatePostCardName()
        data["torecipient_id"] = int(randomProfile.id)
        data["fromsender_id"] = int(profile_of_request_user.id)



        serializer = CreateCardSerializer(data = data)
        if serializer.is_valid():
            serializer.save() ## 创建了新明信片

            data['torecipient'] = {}
            data['torecipient']['name'] = randomProfile.profileaddress.name
            data['torecipient']['address'] = randomProfile.profileaddress.address
            data['torecipient']['postcode'] = randomProfile.profileaddress.postcode

            print "new card information is {0}".format(data)

            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST", ])
@permission_classes([permissions.IsAuthenticated, ])
def receive_a_card(request):
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
def card_check_isarrived(request, pk):
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
def receive_a_card_with_photo(request):
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

##################################################
### add dianzan to a card
@api_view(["GET", "POST", "PUT", "DELETE",  ])
@permission_classes([permissions.IsAuthenticated,])
def card_dianzan(request, cardid, photoid):
    profile_from_user = Profile.objects.get(profileuser=request.user)

    try:
        card = Card.objects.get(id=int(cardid))
    except Card.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        cardphoto = CardPhoto.objects.get(id=int(photoid))
    except CardPhoto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = request.data

    if request.method == 'POST':
        card_by_dianzan_id = card.id,
        person_who_dianzan_id = profile_from_user.id

        ## check whether had been dianzan already
        if DianZan.objects.filter(person_who_dianzan = profile_from_user,
                                  card_by_dianzan = card,
                                  card_photo_by_dianzan = cardphoto).exists():
            # DianZan.objects.filter(person_who_dianzan = profile_from_user, card_by_dianzan = card).delete()
            return Response({"detail": "already dianzan"})

        else:
            zan = DianZan.objects.create_with_ids(card_by_dianzan_id=card.id,
                                                  card_photo_by_dianzan_id=cardphoto.id,
                                                person_who_dianzan_id=profile_from_user.id)
            serializer = DianZanSerializer(zan)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == "PUT":
        ## check whether had been dianzan already
        if DianZan.objects.filter(person_who_dianzan=profile_from_user, card_by_dianzan=card).exists():
            # DianZan.objects.filter(person_who_dianzan=profile_from_user, card_by_dianzan=card).delete()
            return Response({"detail": "Already dianzan"})

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
def card_dianzans(request, cardid):
    cardid = int(cardid)
    try:
        card = Card.objects.get(id=cardid)
    except Card.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        zans = DianZan.objects.filter(card_by_dianzan_id =cardid)
        results = [obj.as_json() for obj in zans]
        return Response(results, status= status.HTTP_200_OK)

#


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




