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
        ## obj = Address.objects.get(pk=somenumber)
        print AddressSerializer(obj).data

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
        ## query params are obtained in this way
        # sortby = self.request.query_params.get('sortby', None) ## ?sortby=
        return Address.objects.filter(name=name)

class GetAddressViewWithNameQuery(generics.ListAPIView):
    serializer_class = AddressSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        ## query paramater ?name=zhang
        name = self.request.query_params.get('name', None)
        return Address.objects.filter(name=name)

class RegisterAddressView(generics.CreateAPIView):
    serializer_class = AddressSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

@api_view(["PUT",])
@permission_classes([permissions.IsAuthenticated, ])
def api_update_address_with_profile_id(request, pk, format=None):
    ""
    if request.method == "PUT":
        profile_from_user = Profile.objects.get(profileuser
                                                   =request.user)
        if not int(pk) == int(profile_from_user.id):
            return Response({"details": "request user != profileuser",
                             "id_url": pk,
                             "id_request:": profile_from_user.id},
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

