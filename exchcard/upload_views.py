#coding:utf-8
import datetime
from django.shortcuts import Http404
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, DataAndFiles


from mysite import settings
from exchcard.models import Profile
from exchcard.permissions import IsProfileUserOrStaffUser
from exchcard import utils

from exchcard.permissions import IsOwnerOrReadOnly
from exchcard.models import AvatarPhoto, CardPhoto, Card
from exchcard.serializers import AvatarPhotoSerializer, CreateAvatarPhotoSerializer, CardPhotoSerializer

#
## post and get files from sae storage
@api_view(['GET',])
@permission_classes([permissions.AllowAny, ])
def s3_storage(request, format=None):
    if request.method == "GET":
        bucket = utils.get_bucket()
        bucket.put_object('1.txt', str(datetime.datetime.now().today()))
        strs1 = str(bucket.generate_url("1.txt"))
        strs2 = str(bucket.get_object_contents('1.txt'))
        data = "%s, %s" %(strs1, strs2)

        return Response({'content':data},
                        status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated, ])
@parser_classes([MultiPartParser, FormParser])
def upload_avatar(request, pk, format=None):
    if request.method == "POST":
        try:
            profile_from_request = Profile.objects.get(profileuser=request.user)
            if int(pk) == profile_from_request.id:
                profile = Profile.objects.get(pk=int(pk))

                ##photo = AvatarPhoto(owner=exchcard, avatar=request.data['avatar'])
                photo = AvatarPhoto(owner=profile, avatar=request.FILES['avatar'])
                photo.save()

                name_on_s3 = photo.avatar.name
                ## sae s3 does not support path
                # path_on_s3 = photo.avatar.path
                url_on_s3 = photo.avatar.url

                ##bucket = utils.get_bucket()
                ##bucket.put_object("%s-avatar.jpg"%pk, request.data['avatar'])

                aserializer = AvatarPhotoSerializer(photo, context={'request': request})
                data = aserializer.data
                data["name"] = name_on_s3
                data["url"] = url_on_s3
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response({"details": "request user != profileuser",
                             "id1":pk,
                            "id2:":profile_from_request.id },
                            status=status.HTTP_403_FORBIDDEN)

            ## method 2: using serializer
            # serializer = CreateAvatarPhotoSerializer(data=request.data, context={'request': request})
            # if serializer.is_valid():
            #     serializer.save(owner=exchcard)
            #     photo = AvatarPhoto(owner=exchcard, avatar=request.data["avatar"])
            #     photo.save()
            #
            #     ## bucket.put_object("%s-avatar"%pk, request.data['avatar'])
            #     aserializer = AvatarPhotoSerializer(photo, context={'request': request})

            #     return Response(aserializer.data, status=status.HTTP_201_CREATED)
            # else:
            #     return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

        except Profile.DoesNotExist:
            return Response({"details":"exchcard id %s does not exist" % pk},
                            status=status.HTTP_404_NOT_FOUND)

class AvatarUploadView(APIView):
    parser_classes = ([MultiPartParser, FormParser]) ## only key is file
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def post(self, request, pk, format=None):

        try:
            profile_from_request = Profile.objects.get(profileuser=request.user)
            if int(pk) == profile_from_request.id:
                profile = Profile.objects.get(pk=int(pk))
                photo = AvatarPhoto(owner=profile, avatar=request.data['avatar'])
                ## photo = AvatarPhoto(owner=exchcard, avatar=request.data["avatar"])
                ## createSerializer = CreateAvatarPhotoSerializer(photo)
                ## createSerializer.save()
                photo.save()

                name_on_s3 = photo.avatar.name
                url_on_s3 = photo.avatar.url

                aserializer = AvatarPhotoSerializer(photo, context={'request': request})
                data = aserializer.data
                data["name"] = name_on_s3
                data["url"] = url_on_s3

                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response({"details": "request user != profileuser",
                             "id1":pk,
                            "id2:":profile_from_request.id },
                            status=status.HTTP_403_FORBIDDEN)
        except Profile.DoesNotExist:
            return Response({"details":"exchcard id %s does not exist" % pk},
                            status=status.HTTP_404_NOT_FOUND)

class AvatarPhotoList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    parser_classes = (MultiPartParser,)

    def get(self, request, format=None):
        photo = AvatarPhoto.objects.all()
        serializer = AvatarPhotoSerializer(photo, many=True , context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        profile = Profile.objects.get(profileuser=request.user)
        serializer = CreateAvatarPhotoSerializer(avatar=request.data['avatar'],
                                                 owner=profile,
                                                 context={'request': request})
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def pre_save(self, obj):
        obj.owner = Profile.objects.get(profileuser=self.request.user)

### get, update, destory
class AvatarPhotoDetail(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_object(self, pk):
        try:
            return AvatarPhoto.objects.get(pk=pk)
        except AvatarPhoto.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        photo = self.get_object(pk)
        serializer = AvatarPhoto(photo)
        return Response(serializer.data)

    # def put(self, request, pk, format=None):
    #     photo = self.get_object(pk)
    #     serializer = AvatarPhotoSerializer(photo, data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, pk, format=None):
    #     photo = self.get_object(pk)
    #     photo.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #
    # def pre_save(self, obj):
    #     obj.owner = Profile.objects.get(profileuser=self.request.user)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated, ])
@parser_classes([MultiPartParser, FormParser])
def api_upload_card_photo(request, pk, format=None):
    if request.method == "POST":
        try:
            profile_from_request = Profile.objects.get(profileuser=request.user)
            card_host = Card.objects.get(pk=int(pk))

            ### get the recipient of the card
            recipient = card_host.torecipient
            sender = card_host.fromsender
            if profile_from_request.id == recipient.id or profile_from_request.id == sender.id:


                photo = CardPhoto(owner=profile_from_request,
                                  card_host=card_host,
                                  card_photo=request.FILES['cardphoto'])
                photo.save()

                name_on_s3 = photo.card_photo.name
                ## sae s3 does not support path
                # path_on_s3 = photo.card_photo.path
                url_on_s3 = photo.card_photo.url

                ##bucket = utils.get_bucket()
                ##bucket.put_object("%s-avatar.jpg"%pk, request.data['avatar'])

                serializer = CardPhotoSerializer(photo, context={'request': request})
                data = serializer.data
                data["name_on_server"] = name_on_s3
                data["url_on_server"] = url_on_s3

                return Response(data, status=status.HTTP_201_CREATED)
            else:
                Response({"details": "card recipient!= profileuser, sender !=profileuser",
                          "id1": recipient.id,
                          "id2": profile_from_request.id},
                         status= status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response({"details":"exchcard id %s does not exist" % pk},
                            status=status.HTTP_404_NOT_FOUND)