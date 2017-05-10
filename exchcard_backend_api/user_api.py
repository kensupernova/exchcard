# -*- coding: utf-8 -*-

import django.contrib.auth as auth
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model # If used custom user mode
from django.contrib.auth.models import User

from exchcard_backend_api.serializers import UserSerializer, RegisterUserSerializer2
from exchcard_backend_api.util.utils import generateToken

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response


### list all users
class UserList(generics.ListAPIView):
    queryset = User.objects.all().order_by('-date_joined')
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
    model = get_user_model()
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




@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def user_login(request):
    """
    User log in with username and password, the name is email is the username
    :param request:
    :return:
    """
    if request.method == "POST":
        username = request.data['username']
        password = request.data['password']
        print "login with {0}: {1}".format(username, password)

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({"username": username,
                         "isauth": True,
                         "accessToken": generateToken(username)},
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
                     "isauth": True,
                     },
                    status= status.HTTP_200_OK
                )

        else:
            return Response(
                    {
                     "isauth": False,
                     "next": "/login"
                    },
                    status= status.HTTP_200_OK
                )

    except:
        return Response(
                    {
                     "isauth": False,
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
    if auth.logout(request):
        return Response(
                        { "isauth": False,
                          "next": "/"
                        },
                        status= status.HTTP_200_OK
                    )
    else:
        return Response(
            {"isauth": False,
             "next": "/profile"
             },
            status=status.HTTP_200_OK
        )
