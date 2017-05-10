# -*- coding: utf-8 -*-

from exchcard.models import Address
from exchcard.models import Profile
from exchcard_backend_api.serializers import AddressSerializer

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


class GetAllAddressListView(generics.ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class GetOneAddressView(generics.RetrieveAPIView):
    ## queryset = Address.objects.all()
    serializer_class = AddressSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_object(self):
        ## get one randomly
        obj = Address.objects.order_by("?").first()

        ## print AddressSerializer(obj).data

        return obj


class GetAddressView(generics.RetrieveAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    lookup_field = ["pk"]

    permission_classes = [
        permissions.IsAuthenticated
    ]


class GetAddressViewWithName(generics.ListAPIView):
    serializer_class = AddressSerializer

    lookup_field = ["name"]

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        name= self.kwargs['name'] # parameters in url path

        # query params are like ?sortby=some_parameter
        # sortby = self.request.query_params.get('sortby', None) ## query是?sortby=

        return Address.objects.filter(name=name)

class GetAddressViewWithNameQuery(generics.ListAPIView):
    serializer_class = AddressSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        ## query paramater like  ?name=zhang
        name = self.request.query_params.get('name', None)
        return Address.objects.filter(name=name)


class RegisterAddressView(generics.CreateAPIView):
    serializer_class = AddressSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]


@api_view(["PUT",])
@permission_classes([permissions.IsAuthenticated, ])
def update_address_with_profile_id(request, pk, format=None):
    """
    更新某个Profile的地址
    :param request:
    :param pk: profile id
    :param format:
    :return: 更新后的地址
    """
    if request.method == "PUT":
        profile_from_request = Profile.objects.get(profileuser
                                                   =request.user)
        if not int(pk) == int(profile_from_request.id):
            return Response({"details": "request user != user with profile id in url",
                             "id_url": pk,
                             "id_request:": profile_from_request.id},
                            status=status.HTTP_403_FORBIDDEN)


        profile = Profile.objects.get(pk=pk)
        address = profile.profileaddress
        address.update(name=request.data["name"],
                       address=request.data["address"],
                       postcode=request.data["postcode"])

        return Response(AddressSerializer(address).data, status=status.HTTP_200_OK)

    else:
        return Response({"details: method is not allowed"},
                        status= status.HTTP_403_FORBIDDEN)

