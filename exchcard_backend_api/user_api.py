# -*- coding: utf-8 -*-

import django.contrib.auth as auth
from django.contrib.auth import authenticate, login, logout

# from django.contrib.auth.models import User
# from exchcard.models import XUser as User
from django.contrib.auth import get_user_model # If used custom user mode
from rest_framework.serializers import Serializer

from exchcard.models_profile import Follow

User = get_user_model()

from exchcard_backend_api.serializers import UserSerializer, UserSerializer2, RegisterUserSerializer2
from exchcard_backend_api.serializers import FollowSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from utils.utils import generateToken


### list all users
class UserList(generics.ListAPIView):
    queryset = User.objects.all().order_by('-created')
    serializer_class = UserSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

## list all user detail
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

### method 2: to create a new user, without auth
class RegisterUserView(CreateAPIView):
    # model = get_user_model()
    model = User

    serializer_class = RegisterUserSerializer2

    permission_classes = [
        permissions.AllowAny # Or un-authed users can't register
    ]


## method 1: create new user, need superuser or staffuser auth
## super user permission
@api_view(["POST"])
def register_new_user(request):
    """
    create a new user with email, username, passwd
    """
    if request.method == "POST":
        data = request.data
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            ## method 1
            # serializer.save()
            ## method 2
            # User.objects.create_user(
            #     serialized.init_data['email'],
            #     serialized.init_data['username'],
            #     serialized.init_data['password']
            # )
            ## method 3
            User.objects.create_user(
                email=data['email'],
                username=data['username'],
                password=data['password']
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET", ])
@permission_classes([permissions.IsAuthenticated, ])
def get_info_of_logged_user(request):
    """
    得到目前登录用户的账户信息
    :param request:
    :return:
    """
    if request.method == "GET":
        try:
            # print "getting info of user ... "
            user = request.user
            return Response(UserSerializer2(user).data, status=status.HTTP_200_OK)
        except:
            return Response({"details":"Internal server error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def user_login_with_email_pw(request):
    """
    User log in with username and password, the name is email is the username
    :param request:
    :return:
    """
    if request.method == "POST":
        email = request.data['email']
        password = request.data['password']

        # print "login with {0}:{1}".format(email, password)

        # user = authenticate(username=email, password=password)
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({"username": email,
                                 "isAuth": True,
                                 "accessToken": generateToken(email)},
                                 status= status.HTTP_200_OK
                    )
                # Redirect to a success page.
            else:
                # Return a 'disabled account' error message
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            # Return an 'invalid login' error message.
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST", "GET"])
@permission_classes([permissions.AllowAny])
def user_auth(request):
    """
    auth user with inputed username and password
    :param request:
    :return:
    """
    try:
        if request.user.is_authenticated():

                return Response(
                    {
                     "isAuth": True,
                     },
                    status= status.HTTP_200_OK
                )

        else:
            return Response(
                    {
                     "isAuth": False,
                     "next": "/login"
                    },
                    status= status.HTTP_200_OK
                )

    except:
        return Response(
                    {
                     "isAuth": False,
                     "next": "/login"
                    },
                    status= status.HTTP_404_NOT_FOUND
                )



@api_view(["POST", "GET"])
@permission_classes([permissions.IsAuthenticated])
def user_logout(request):
    """
    User log out
    :param request:
    :return:
    """
    if logout(request):
        return Response(
                        { "isAuth": False,
                          "next": "/"
                        },
                        status= status.HTTP_200_OK
                    )
    else:
        return Response(
            {"isAuth": False,
             "next": "/profile"
             },
            status=status.HTTP_200_OK
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_username(request):
    """
    update username
    :param request:
    :return:
    """
    # check whether already exist
    newusername = request.data['username']
    dusers = User.objects.filter(username=newusername)
    if dusers.count() > 1:
        return Response({
            "details": "username already exists! choose a new one.",
            "error_msg": "username already exists! choose a new one."
        })

    user = request.user
    user.username = newusername
    user.save()
    return Response(UserSerializer(user).data,
                    status=status.HTTP_202_ACCEPTED)


@api_view(['POST', 'GET'])
@permission_classes([permissions.IsAuthenticated])
def check_password(request):
    """
    check the password of user correct or not
    :param request:
    :return:
    """
    try:
        pwd = request.data['password']
    except:
        return Response({
            "description": "no pwd in the request!",
            "details": "no pwd in the request!"
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        user = authenticate(email=request.user.email, password=pwd)
        if user is not None:
            return Response({
                "is_correct": 1,
                "is_correct_int": 1,
                "description": "password is correct!"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "is_correct": 0,
                "is_correct_int": 0,
                "description": "password is wrong!"
            }, status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
@permission_classes([permissions.IsAuthenticated, ])
def update_password(request):
    """
    check the password of user correct or not
    :param request:
    :return:
    """
    try:
        new_pwd = request.data['new_password']
        user = request.user
    except:
        return Response({
            "description": "no pwd in the request!",
            "details": "no pwd in the request!"
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        try:
            user.set_password(new_pwd)
            user.save()

            logout(request)

            return Response({
                "update_pwd_is_succuss": 1,
                "update_pwd_is_succuss_int": 1,
                "description": "password is updated successfully!"
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                "details": "no errors found"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST', ])
@permission_classes([permissions.IsAuthenticated, ])
def make_a_follow_to_him(request):
    """
    用户关注其他人
    :param request: request.data is not empty, {'user_being_followed_id': int }
    :return: {'isFollowSuccess': True}
    """
    if request.method == "POST":
        user = request.user
        user_being_followed_id = request.data["user_being_followed_id"]

        # VERY IMPORTANT !!!
        # CHECK WHETHER ALREADY FOLLOWING HIM!!!
        if Follow.objects.filter(subject_id=user.id).\
                filter(user_being_followed_id=user_being_followed_id).\
                exists():
            return Response({"details":"You had already followed him",
                             "error_msg": "You had already followed him",
                             "isFollowSuccessBool": False,
                             "isFollowSuccessInt": 0,
                             "isAlreadyFollowingHimBool": True,
                             "isAlreadyFollowingHimInt": 1,
                             })

        follow = Follow(subject_id=user.id, user_being_followed_id=user_being_followed_id)
        follow.save()

        serializer = FollowSerializer(follow)
        data = serializer.data
        data['isFollowSuccessBool'] = True
        data['isFollowSuccessInt'] = 1

        return Response(data, status=status.HTTP_201_CREATED)
