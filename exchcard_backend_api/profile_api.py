# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login

from multiple_model.views import MultipleModelAPIView

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from exchcard.models import Address, Card
from exchcard.models import Profile

from exchcard_backend_api.permissions import IsProfileUserOrStaffUser
from exchcard_backend_api.serializers import AddressSerializer
from exchcard_backend_api.serializers import CreateProfileSerializer
from exchcard_backend_api.serializers import GetProfileWithCardSerializer
from exchcard_backend_api.serializers import GetUserAddressProfileSerializer
from exchcard_backend_api.serializers import UserAddressProfileSerializer
from exchcard_backend_api.serializers import UserSerializer, CardSerializer
from exchcard_backend_api.utils.utils import generateToken

from exchcard_backend_api.utils.utils import count_arrive_travel


class GetProfileListView(generics.ListAPIView):
    """
    get a profile with cards list
    """
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
    User and Address serializer, Multiple Model API View
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
def register_user_address_profile(request, format=None):
    """
    First time registration
    需要的参数：user, password, email, name, address, postcode
    得到：一个user，一个address，一个profile
    :param request:
    :param format:
    :return:
    created by guanghui
    """
    if request.method == "POST":
        try:
            ## the request data in json or other format from put, post, patch methods
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
            return Response({"detail": "Server internal error!"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        ## 序列化数据
        serializer = UserAddressProfileSerializer(profile)
        ## 打印到服务器
        print "New user address profile created: {0}".format(serializer.data)

        ## 最后返回给客服端，新的
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == "GET":
        return Response({"detail":"Get method is not allowed"},
                        status= status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
@permission_classes([permissions.IsAdminUser, ])
def register_new_profile_with_ids(request, format=None):
    """
    create a new profile with user id and address id
    limited to: admin user or staff user can create exchcard_backend_api with user_id and profile_id
    """
    if request.method == "POST":
        print "------------------------------"
        print "adding a new profile"
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


@api_view(["GET","PUT"])
@permission_classes([IsProfileUserOrStaffUser, ])
def update_profile_with_ids(request, format=None):
    """
    update profile with user id and address id
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
        print "update profile"
        # serializer = AddProfileSerializerWithIds(exchcard_backend_api, data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = request.data

        p = Profile.objects.update_profile_address_with_ids(
                userid=data['userid'],
                addressid=data['addressid']
            )

        print p

        p.save()
        return Response(CreateProfileSerializer(p).data, status=status.HTTP_205_RESET_CONTENT)



@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_random_profile(request, format=None):
    """
    get one profile for sending card, randomly, later, use algorithm to match
    :param Request:
    :return:
    """
    if request.method == "GET":
        try:
            profile = Profile.objects.order_by("?").first()

        except Profile.DoesNotExist:
            return Response({"detail": "404 NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        serializer = GetUserAddressProfileSerializer(profile)

        data = serializer.data
        ### Get the sender profile id at the same time
        data["sender_profile_id"] = request.user.profile.id

        return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def profile_get_cards_all_state_count(request, pk, format=None):
    """
    得到某个Profile的各个状态的明信片总信息汇总
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
        response_data["sent_cards_count"] = {}
        response_data["sent_cards_count"]["total"] = sent_cards_count[0]
        response_data["sent_cards_count"]["arrived"] = sent_cards_count[1]
        response_data["sent_cards_count"]["travelling"] = sent_cards_count[2]

        response_data["receive_cards_count"] = {}
        response_data["receive_cards_count"]["total"] = receive_cards_count[0]
        response_data["receive_cards_count"]["arrived"] = receive_cards_count[1]
        response_data["receive_cards_count"]["travelling"] = receive_cards_count[2]

        return Response(response_data, status= status.HTTP_200_OK)


"""
用户明信片根据各个状态分别处理
"""
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def profile_get_cards_total(request, pk, format=None):
    """
    得到所有的明信片
    :param request:
    :param pk:
    :param format:
    :return:
    """
    try:
        profile = Profile.objects.get(pk=pk)
        profile_of_request_user = Profile.objects.get(profileuser
                                                =request.user)
        if not int(profile.id) == int(profile_of_request_user.id):
            return Response({"details": "profile of request user != profile of id in url",
                             "id_url": profile.id,
                             "id_request:": profile_of_request_user.id},
                            status=status.HTTP_403_FORBIDDEN)

    except Profile.DoesNotExist:
        return Response({"details": "User does not exit"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        try:
            cards_receive_travelling = Card.objects.filter(Q(torecipient=profile_of_request_user) & Q(has_arrived=False))
            cards_receive_arrived = Card.objects.filter(Q(torecipient=profile_of_request_user) & Q(has_arrived=True))

            cards_sent_travelling = Card.objects.filter(Q(fromsender=profile_of_request_user) & Q(has_arrived=False))
            cards_sent_arrived = Card.objects.filter(Q(fromsender=profile_of_request_user) & Q(has_arrived=True))


            return Response({"sent_arrived": CardSerializer(cards_sent_arrived,
                                                            many=True, context={'request': request}).data,
                             "sent_travelling": CardSerializer(cards_sent_travelling,
                                                            many=True, context={'request': request}).data,
                             "receive_arrived": CardSerializer(cards_receive_arrived,
                                                            many=True, context={'request': request}).data,
                             "receive_travelling": CardSerializer(cards_receive_travelling,
                                                            many=True, context={'request': request}).data,

            }, status=status.HTTP_200_OK)

        except Exception:
            return Response({"detail":"Error when get all cards info"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def profile_get_cards_sent_total(request, pk, format=None):
    try:
        profile = Profile.objects.get(pk=pk)
        profile_of_request_user = Profile.objects.get(profileuser
                                                =request.user)
        if not int(profile.id) == int(profile_of_request_user.id):
            return Response({"details": "request user != profileuser",
                             "id_url": profile.id,
                             "id_request:": profile_of_request_user.id},
                            status=status.HTTP_403_FORBIDDEN)

    except Profile.DoesNotExist:
        return Response({"details":"Profile object does not exit"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        cards = Card.objects.filter(fromsender = profile_of_request_user)
        serializer = CardSerializer(cards, many=True, context={'request': request})

        return Response(serializer.data, status= status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def profile_get_cards_receive_total(request, pk, format=None):
    try:
        profile = Profile.objects.get(pk=pk)
        profile_of_request_user = Profile.objects.get(profileuser
                                                =request.user)
        if not int(profile.id) == int(profile_of_request_user.id):
            return Response({"details": "request user != user from profile id in url",
                             "id_url": profile.id,
                             "id_request:": profile_of_request_user.id},
                            status=status.HTTP_403_FORBIDDEN)

    except Profile.DoesNotExist:
        return Response({"details":"Profile object does not exit"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        cards = Card.objects.filter(torecipient=profile_of_request_user)
        serializer = CardSerializer(cards, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def profile_get_cards_sent_travelling(request, pk, format=None):
    try:
        profile = Profile.objects.get(pk=pk)
        profile_of_request_user = Profile.objects.get(profileuser
                                                =request.user)
        if not int(profile.id) == int(profile_of_request_user.id):
            return Response({"details": "request user != profileuser",
                             "id_url": profile.id,
                             "id_request:": profile_of_request_user.id},
                            status=status.HTTP_403_FORBIDDEN)

    except Profile.DoesNotExist:
        return Response({"details":"Profile object does not exit"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        cards = Card.objects.filter(Q(fromsender=profile_of_request_user ) & Q(has_arrived=False))

        serializer = CardSerializer(cards, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def profile_get_cards_receive_travelling(request, pk, format=None):
    try:
        profile = Profile.objects.get(pk=pk)
        profile_of_request_user = Profile.objects.get(profileuser
                                                =request.user)
        if not int(profile.id) == int(profile_of_request_user.id):
            return Response({"details": "request user != profileuser",
                             "id_url": profile.id,
                             "id_request:": profile_of_request_user.id},
                            status=status.HTTP_403_FORBIDDEN)

    except Profile.DoesNotExist:
        return Response({"details":"Profile object does not exit"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        cards = Card.objects.filter(Q(torecipient=profile_of_request_user ) & Q(has_arrived=False))

        serializer = CardSerializer(cards, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def profile_get_cards_sent_arrived(request, pk, format=None):
    try:
        profile = Profile.objects.get(pk=pk)
        profile_of_request_user = Profile.objects.get(profileuser
                                                =request.user)
        if not int(profile.id) == int(profile_of_request_user.id):
            return Response({"details": "request user != profileuser",
                             "id_url": profile.id,
                             "id_request:": profile_of_request_user.id},
                            status=status.HTTP_403_FORBIDDEN)

    except Profile.DoesNotExist:
        return Response({"details":"Profile object does not exit"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        cards = Card.objects.filter(Q(fromsender=profile_of_request_user) & Q(has_arrived=True))

        serializer = CardSerializer(cards, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def profile_get_cards_receive_arrived(request, pk, format=None):
    try:
        profile = Profile.objects.get(pk=pk)
        profile_of_request_user = Profile.objects.get(profileuser
                                                =request.user)
        if not int(profile.id) == int(profile_of_request_user.id):
            return Response({"details": "request user != profileuser",
                             "id_url": profile.id,
                             "id_request:": profile_of_request_user.id},
                            status=status.HTTP_403_FORBIDDEN)

    except Profile.DoesNotExist:
        return Response({"details":"Profile object does not exit"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        cards = Card.objects.filter(Q(torecipient=profile_of_request_user ) & Q(has_arrived=True))

        serializer = CardSerializer(cards, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

