#coding: utf-8
from rest_framework.decorators import permission_classes, api_view
from rest_framework import permissions
from rest_framework.reverse import reverse
from rest_framework.response import Response

exchcard_api_endpoint = "http://exchcard_backend_api.applinzi.com/exchcard_backend_api/api/"
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
        "user-detail": exchcard_api_endpoint + "users/(?P<pk>[0-9]+)/",

        "address-list": reverse("address-list", request=request, format=format),
        "address-register": reverse("address-register", request=request, format=format),
        "address-random": reverse("address-random", request=request, format=format),

        # "address-get-id": reverse("address-get-id", request=request, format=format),
        # "address-get-name": reverse("address-get-name", request=request, format=format),
        # "address-update-with-profile-id": reverse("address-update-with-profile-id", request=request, format=format),
        "address-get-id": exchcard_api_endpoint + "address/get/(?P<pk>[0-9]+)/",
        "address-get-name": exchcard_api_endpoint + "address/get/name/(?P<name>.+)/",
        "address-update-with-profile-id": exchcard_api_endpoint+"address/update/(?P<id>[0-9]+)/",

        "profile-list": reverse("profile-list", request=request, format=format),

        # "profile-detail": reverse("profile-detail", request=request, format=format),
        "profile-detail": exchcard_api_endpoint+"profiles/(?P<pk>[0-9]+)/",

        "profile-register": reverse("profile-register", request=request, format=format),
        "profile-register-with-ids": reverse("profile-register-with-ids", request=request, format=format),
        "profile-update": reverse("profile-update", request=request, format=format),
        "profile-getone-for-card": reverse("profile-getone-for-card", request=request, format=format),

        # "profile-get-cards": reverse("profile-get-cards", request=request, format=format),
        # "profile-avatarphoto-upload": reverse("profile-avatarphoto-upload", request=request, format=format),
        # "profile-avatarphoto-uploadf": reverse("profile-avatarphoto-uploadf", request=request, format=format),
        "profile-get-cards": exchcard_api_endpoint + "profiles/(?P<pk>[0-9]+)/getcards/",
        "profile-avatarphoto-upload": exchcard_api_endpoint + "profiles/(?P<pk>[0-9]+)/avatar/",
        "profile-avatarphoto-uploadf": exchcard_api_endpoint + "profiles/(?P<pk>[0-9]+)/avatarf/",

        "avatarphoto-list": reverse("avatarphoto-list", request=request, format=format),

        # "avatarphoto-detail": reverse("avatarphoto-detail", request=request, format=format),
        "avatarphoto-detail": exchcard_api_endpoint +"profiles/photos/(?P<pk>[0-9]+)/",

        "card-list": reverse("card-list", request=request, format=format),

        # "card-detail": reverse("card-detail", request=request, format=format),
        "card-detail": exchcard_api_endpoint + "cards/(?P<pk>[0-9]+)/",

        "card-add2": reverse("card-add2", request=request, format=format),
        "card-add": reverse("card-add", request=request, format=format),
        "card-receive": reverse("card-receive", request=request, format=format),
        "card-receive-with-photo": reverse("card-receive-with-photo", request=request, format=format),
        # "card-update": reverse("card-update", request=request, format=format),
        # "card-check-arrive": reverse("card-check-arrive", request=request, format=format),

        "card-update":exchcard_api_endpoint +"cards/(?P<pk>[0-9]+)/update/",
        "card-check-arrive": exchcard_api_endpoint +"cards/(?P<pk>[0-9]+)/hasarrived/",
        "card-dianzan": exchcard_api_endpoint + "cards/(?P<pk>[0-9]+)/cardphotos/(?P<photoid>[0-9]+)/dianzan/",
        "card-dianzans": exchcard_api_endpoint + "cards/(?P<pk>[0-9]+)/cardphotos/(?P<photoid>[0-9]+)/dianzans/",
        "card-dianzans-2": exchcard_api_endpoint + "cards/(?P<pk>[0-9]+)/dianzans2/",
        "card-cardphoto": exchcard_api_endpoint + "cards/(?P<pk>[0-9]+)/cardphoto/",
        # "card-dianzan": reverse("card-dianzan", request=request, format=format),
        # "card-dianzans": reverse("card-dianzans", request=request, format=format),
        # "card-dianzans-2": reverse("card-dianzans-2", request=request, format=format),
        # "card-cardphoto": reverse("card-cardphoto", request=request, format=format),

        "cards-feed": reverse("cards-feed", request=request, format=format),

    })