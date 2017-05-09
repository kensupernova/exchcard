# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db.models import Q

from exchcard.models import Address, Card
from exchcard.models import Profile
from exchcard_backend_api.permissions import IsProfileUserOrStaffUser
from exchcard_backend_api.serializers import AddressSerializer
from exchcard_backend_api.serializers import CreateProfileSerializer
from exchcard_backend_api.serializers import GetProfileWithCardSerializer
from exchcard_backend_api.serializers import GetUserAddressProfileSerializer
from exchcard_backend_api.serializers import RegisterUserAddressProfileSerializer
from exchcard_backend_api.serializers import UserSerializer, CardSerializer
from exchcard_backend_api.utils import count_arrive_travel
from multiple_model.views import MultipleModelAPIView
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

## get a profile with cards list
class GetProfileListView(generics.ListAPIView):
    serializer_class = GetProfileWithCardSerializer
    queryset = Profile.objects.all()

    permission_classes = [
        permissions.IsAuthenticated
    ]

class GetProfileDetailView(generics.RetrieveAPIView):
    serializer_class = GetProfileWithCardSerializer
    queryset = Profile.objects.all()

    permission_classes = [
        permissions.IsAuthenticated,
        IsProfileUserOrStaffUser
    ]

## add profile
class RegisterProfileView(generics.CreateAPIView):
    """
    Add Profile View and Update View
    """
    serializer_class = CreateProfileSerializer

    queryset = Profile.objects.all()

    permission_classes = [
        permissions.IsAuthenticated
    ]

# ## multi model views with multi serializers
# ## permission limit access to admin users
class RegisterUserAddressProfileView(MultipleModelAPIView):
    """
    User and Address serializer information
    """
    queryList = [
        (User.objects.all(), UserSerializer),
        (Address.objects.all(), AddressSerializer)
    ]

    permission_classes = [
        permissions.IsAdminUser
    ]


@api_view(["POST","GET"])
@permission_classes([permissions.AllowAny, ])
def api_register_user_address_profile(request, format=None):
    """
    first time register with username, password, address
    :param request: user, password, email, address, postcode, etc.
    :param format:
    :return:
    """
    if request.method == "POST":
        try:
            ## the requst data in json or other format
            dict_data = request.data
            # print dict_data
            if "username" not in dict_data.keys():
                return Response({"detail":"Dict Key Error"},
                        status==status.HTTP_500_INTERNAL_SERVER_ERROR)

            ## check whether the username already existed
            if not User.objects.filter(username=dict_data["username"]).exists():

                user = User.objects.create_user(
                    username=dict_data["username"],
                    password=dict_data["password"],
                    email=dict_data["email"])

                user.save()

                address =Address.objects.create_address(name=dict_data["name"],
                    address=dict_data["address"],
                    postcode=dict_data["postcode"])
                address.save()

                profile = Profile.objects.create(profileuser = user, profileaddress=address)
                profile.save()


            else:
                return Response({"detail":"user alreay exist!"},
                    status=status.HTTP_400_BAD_REQUEST)

        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = RegisterUserAddressProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == "GET":
        return Response({"detail":"Get method is not allowed"}, status= status.HTTP_405_METHOD_NOT_ALLOWED)

## admin user or staff user can create exchcard_backend_api with user_id and profile_id
@api_view(["POST"])
@permission_classes([permissions.IsAdminUser, ])
def api_register_new_profile_with_ids(request, format=None):
    """
    create a new user
    """
    if request.method == "POST":
        print "------------------------------"
        print "adding new profile"
        data = request.data
        print data
        p = Profile.objects.create_profile_with_ids(
                userid=data['userid'],
                addressid=data['addressid']
            )

        print p

        p.save()

        dict_data = {}
        dict_data["profileuser"] = p.profileuser.username
        dict_data["profileaddress"] = p.profileaddress.address

        return Response(dict_data, status=status.HTTP_201_CREATED)

##
@api_view(["GET","PUT"])
@permission_classes([IsProfileUserOrStaffUser, ])
def api_update_profile(request, format=None):
    """
    update profile
    :param: userid, addressid
    """
    if request.method == "GET":
        try:
            profile = Profile.objects.get(profileuser_id=request.data['userid'])
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CreateProfileSerializer(profile)
        return Response(serializer.data)

    if request.method == "PUT":
        ### check whether profileuser is the currentuser
        print "------------------------------"
        print "update exchcard_backend_api"
        # serializer = AddProfileSerializerWithIds(exchcard_backend_api, data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        data = request.data
        print data
        p = Profile.objects.update_profile_address_with_ids(
                userid=data['userid'],
                addressid=data['addressid']
            )

        print p

        p.save()
        return Response(CreateProfileSerializer(p).data, status=status.HTTP_200_OK)



@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def api_get_random_profile(request, format=None):
    """
    get one exchcard_backend_api for sending card, randomly, later, use algorithm to match
    :param Request:
    :return:
    """
    if request.method == "GET":
        try:
            profile = Profile.objects.order_by("?").first()

        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = GetUserAddressProfileSerializer(profile)

        data = serializer.data
        ### search the sender exchcard_backend_api id at the same time
        data["sender_profile_id"] = request.user.profile.id
        return Response(data)

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def api_profile_get_cards_count(request, pk, format=None):
    """
    register with user information and address information
    :param request:
    :param pk:
    :param format:
    :return:
    """

    try:
        profile = Profile.objects.get(pk=pk)
        profile_from_user = Profile.objects.get(profileuser
                                                =request.user)
        if not int(profile.id) == int(profile_from_user.id):
            return Response({"details": "request user != profileuser",
                             "id_url": pk,
                             "id_request:": profile_from_user.id},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = GetProfileWithCardSerializer(profile, context={'request': request})
        # `HyperlinkedIdentityField` requires the request in the serializer context.
        # Add `context={'request': request}` when instantiating the serializer.
    except Profile.DoesNotExist:
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        data = serializer.data
        sent_cards = data["sent_cards"]
        receive_cards = data["receive_cards"]

        sent_cards_count = count_arrive_travel(sent_cards)
        receive_cards_count = count_arrive_travel(receive_cards)

        response_data ={}
        response_data["sent_cards"] = {}
        response_data["sent_cards"]["total"] = sent_cards_count[0]
        response_data["sent_cards"]["arrived"] = sent_cards_count[1]
        response_data["sent_cards"]["travelling"] = sent_cards_count[2]
        response_data["receive_cards"] = {}
        response_data["receive_cards"]["total"] = receive_cards_count[0]
        response_data["receive_cards"]["arrived"] = receive_cards_count[1]
        response_data["receive_cards"]["travelling"] = receive_cards_count[2]

        return Response(response_data, status= status.HTTP_200_OK)



@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def api_profile_get_cards_total(request, pk, format=None):
    try:
        profile = Profile.objects.get(pk=pk)
        profile_from_user = Profile.objects.get(profileuser
                                                =request.user)
        if not int(profile.id) == int(profile_from_user.id):
            return Response({"details": "request user != profileuser",
                             "id_url": profile.id,
                             "id_request:": profile_from_user.id},
                            status=status.HTTP_403_FORBIDDEN)

    except Profile.DoesNotExist:
        return Response({"details": "user does not exit"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        cards_receive_travel = Card.objects.filter(Q(torecipient=profile_from_user) & Q(has_arrived=False))
        cards_receive_arrive = Card.objects.filter(Q(torecipient=profile_from_user) & Q(has_arrived=True))

        cards_sent_travel = Card.objects.filter(Q(fromsender=profile_from_user) & Q(has_arrived=False))
        cards_sent_arrive = Card.objects.filter(Q(fromsender=profile_from_user) & Q(has_arrived=True))


        return Response({"sent_arrived": CardSerializer(cards_sent_arrive,
                                                        many=True, context={'request': request}).data,
                         "sent_travelling": CardSerializer(cards_sent_travel,
                                                        many=True, context={'request': request}).data,
                         "receive_arrived": CardSerializer(cards_receive_arrive,
                                                        many=True, context={'request': request}).data,
                         "receive_travelling": CardSerializer(cards_receive_travel,
                                                        many=True, context={'request': request}).data,

        }, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def api_profile_get_cards_sent_total(request, pk, format=None):
    try:
        profile = Profile.objects.get(pk=pk)
        profile_from_user = Profile.objects.get(profileuser
                                                =request.user)
        if not int(profile.id) == int(profile_from_user.id):
            return Response({"details": "request user != profileuser",
                             "id_url": profile.id,
                             "id_request:": profile_from_user.id},
                            status=status.HTTP_403_FORBIDDEN)

    except Profile.DoesNotExist:
        return Response({"details":"Profile object does not exit"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        cards = Card.objects.filter(fromsender = profile_from_user)
        serializer = CardSerializer(cards, many=True, context={'request': request})

        return Response(serializer.data, status= status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def api_profile_get_cards_receive_total(request, pk, format=None):
    try:
        profile = Profile.objects.get(pk=pk)
        profile_from_user = Profile.objects.get(profileuser
                                                =request.user)
        if not int(profile.id) == int(profile_from_user.id):
            return Response({"details": "request user != profileuser",
                             "id_url": profile.id,
                             "id_request:": profile_from_user.id},
                            status=status.HTTP_403_FORBIDDEN)

    except Profile.DoesNotExist:
        return Response({"details":"Profile object does not exit"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        cards = Card.objects.filter(torecipient=profile_from_user)
        serializer = CardSerializer(cards, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def api_profile_get_cards_sent_travelling(request, pk, format=None):
    try:
        profile = Profile.objects.get(pk=pk)
        profile_from_user = Profile.objects.get(profileuser
                                                =request.user)
        if not int(profile.id) == int(profile_from_user.id):
            return Response({"details": "request user != profileuser",
                             "id_url": profile.id,
                             "id_request:": profile_from_user.id},
                            status=status.HTTP_403_FORBIDDEN)

    except Profile.DoesNotExist:
        return Response({"details":"Profile object does not exit"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        cards = Card.objects.filter(Q(fromsender=profile_from_user ) & Q(has_arrived=False))

        serializer = CardSerializer(cards, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def api_profile_get_cards_receive_travelling(request, pk, format=None):
    try:
        profile = Profile.objects.get(pk=pk)
        profile_from_user = Profile.objects.get(profileuser
                                                =request.user)
        if not int(profile.id) == int(profile_from_user.id):
            return Response({"details": "request user != profileuser",
                             "id_url": profile.id,
                             "id_request:": profile_from_user.id},
                            status=status.HTTP_403_FORBIDDEN)

    except Profile.DoesNotExist:
        return Response({"details":"Profile object does not exit"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        cards = Card.objects.filter(Q(torecipient=profile_from_user ) & Q(has_arrived=False))

        serializer = CardSerializer(cards, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def api_profile_get_cards_sent_arrived(request, pk, format=None):
    try:
        profile = Profile.objects.get(pk=pk)
        profile_from_user = Profile.objects.get(profileuser
                                                =request.user)
        if not int(profile.id) == int(profile_from_user.id):
            return Response({"details": "request user != profileuser",
                             "id_url": profile.id,
                             "id_request:": profile_from_user.id},
                            status=status.HTTP_403_FORBIDDEN)

    except Profile.DoesNotExist:
        return Response({"details":"Profile object does not exit"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        cards = Card.objects.filter(Q(fromsender=profile_from_user ) & Q(has_arrived=True))

        serializer = CardSerializer(cards, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def api_profile_get_cards_receive_arrived(request, pk, format=None):
    try:
        profile = Profile.objects.get(pk=pk)
        profile_from_user = Profile.objects.get(profileuser
                                                =request.user)
        if not int(profile.id) == int(profile_from_user.id):
            return Response({"details": "request user != profileuser",
                             "id_url": profile.id,
                             "id_request:": profile_from_user.id},
                            status=status.HTTP_403_FORBIDDEN)

    except Profile.DoesNotExist:
        return Response({"details":"Profile object does not exit"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        cards = Card.objects.filter(Q(torecipient=profile_from_user ) & Q(has_arrived=True))

        serializer = CardSerializer(cards, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

