# -*- coding: utf-8 -*-
from django.http import Http404

from exchcard.models_main import Address, Profile
from exchcard_backend_api.serializers import AddressSerializer, GetProfileSerializer

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView


class AddressDetailAPIView(APIView):
    """
    Create, Retrieve, update or delete
    """

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_object(self, pk):
        try:
            return Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = AddressSerializer(obj)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AddressSerializer(data=request.data) # create a object when save
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = AddressSerializer(obj, data=request.data) ## update object when save
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetAllAddressListView(generics.ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class GetOneRandomAddressView(generics.RetrieveAPIView):
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


class GetAddressViewWithNameField(generics.ListAPIView):
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


class CreateAddressView(generics.CreateAPIView):
    serializer_class = AddressSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]





# -----------------------------------------------------------------------

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated, ])
def address_profile_create(request):
    """
    address and profile created
    :param request:
    :return:
    """
    # METHOD 1
    obj = Address.objects.create_address(name=request.data["name"],
                           address=request.data["address"],
                           postcode=request.data["postcode"])

    # METHOD 2
    # serializer = AddressSerializer(data=request.data)
    # if serializer.is_valid():
    #     obj = serializer.save()

    user = request.user

    profile = Profile.objects.create_profile_with_ids(userid=user.id, addressid=obj.id)

    return Response(GetProfileSerializer(profile, context={'request': request}).data,
                    status=status.HTTP_201_CREATED)



@api_view(["PUT", "POST"])
@permission_classes([permissions.IsAuthenticated, ])
def update_address(request, format=None):
    """
    更新某个Profile的地址
    :param request:
    :param format:
    :return: 更新后的地址
    """
    if request.method == "PUT" or request.method == "POST":
        try:
            profile = Profile.objects.get(profileuser=request.user)

            address = profile.profileaddress

            address.update(name=request.data["name"],
                           address=request.data["address"],
                           postcode=request.data["postcode"])

            return Response(AddressSerializer(address).data, status=status.HTTP_200_OK)
        except:
            return Response({"details":"Internal server error in address_api.py"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response({"details": "method is not allowed"},
                        status= status.HTTP_403_FORBIDDEN)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated, ])
def get_address_of_logged_user(request, format=None):
    """
    得到目前登录用户的地址
    :param request:
    :param format:
    :return:
    """
    if request.method == "GET":
        try:
            profile = Profile.objects.get(profileuser = request.user)

            address = profile.profileaddress

            return Response(AddressSerializer(address).data, status=status.HTTP_200_OK)
        except:
            return Response({"details":"Internal server error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)