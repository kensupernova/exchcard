#coding:utf-8
import datetime

from django.shortcuts import Http404

from exchcard.models_profile import AvatarPhoto, CardPhoto, Card, Profile
from exchcard_backend_api.permissions import IsOwnerOrReadOnly
from exchcard_backend_api.serializers import AvatarPhotoSerializer, CreateAvatarPhotoSerializer, CardPhotoSerializer
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from utils import utils


#
## post and get files from sae storage
@api_view(['GET',])
@permission_classes([permissions.AllowAny, ])
def sae_s3_storage(request, format=None):
    if request.method == "GET":
        bucket = utils.get_sae_bucket()
        bucket.put_object('1.txt', str(datetime.datetime.now().today()))
        strs1 = str(bucket.generate_url("1.txt"))
        strs2 = str(bucket.get_object_contents('1.txt'))
        data = "%s, %s" %(strs1, strs2)

        return Response({'content':data},
                        status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated, ])
def get_avatar_url(request, format=None):
    """
    得到avatar photo的url
    :param request:
    :param pk:
    :param format:
    :return:
    """
    if request.method == "GET":
        try:
            profile = Profile.objects.get(profileuser=request.user)

            photos = AvatarPhoto.objects.filter(owner=profile).order_by('-created')

            print "头像图片总数为{0}".format(len(photos))

            if len(photos)>1:

                photo = photos[0]
            elif len(photos)==1:
                photo = photos
            elif len(photos) < 1:
                print "no avatar photo, use default"
                return Response({
                    "url": "/static/images/default-avatar.jpg"
                })

            url = photo.avatar.url

            serializer = AvatarPhotoSerializer(photo, context={'request': request})
            data = serializer.data
            data["url"] = url

            return Response(data, status=status.HTTP_200_OK)


        except Profile.DoesNotExist:
            return Response({"details":"profile of logged user does not exist"},
                            status=status.HTTP_404_NOT_FOUND)
        except AvatarPhoto.DoesNotExist:
            return Response({"details": "avatar photo of logger user does not exist"},
                            status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated, ])
@parser_classes([MultiPartParser, FormParser])
def upload_avatar_to_s3(request, pk, format=None):
    if request.method == "POST":
        try:
            profile_from_request = Profile.objects.get(profileuser=request.user)
            if int(pk) == profile_from_request.id:
                profile = Profile.objects.get(pk=int(pk))

                ##photo = AvatarPhoto(owner=profile, avatar=request.data['avatar'])
                photo = AvatarPhoto(owner=profile, avatar=request.FILES['avatar'])
                photo.save()

                name_on_s3 = photo.avatar.name
                ## sae s3 does not support path
                # path_on_s3 = photo.avatar.path
                url_on_s3 = photo.avatar.url

                serializer = AvatarPhotoSerializer(photo, context={'request': request})
                data = serializer.data
                data["name"] = name_on_s3
                data["url"] = url_on_s3

                return Response(data, status=status.HTTP_201_CREATED)

            else:
                return Response({"details": "request user != user from url",
                                 "id1":pk,
                                 "id2:":profile_from_request.id },
                                 status=status.HTTP_403_FORBIDDEN)


        except Profile.DoesNotExist:

            return Response({"details": "profile of logged user does not exist"},

                            status=status.HTTP_404_NOT_FOUND)

        except AvatarPhoto.DoesNotExist:

            return Response({"details": "avatar photo of logger user does not exist"},

                            status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated, ])
@parser_classes([MultiPartParser, FormParser])
def upload_avatar(request):
    if request.method == "POST":
        try:
            profile = Profile.objects.get(profileuser=request.user)

            # 上传的文件
            f = request.FILES['avatar']
            # 改变文件名，注意不要改变文件格式后缀
            f.name = utils.hash_file_name(f.name)

            photo = AvatarPhoto(owner=profile, avatar=f)
            photo.save()

            name = photo.avatar.name
            url = photo.avatar.url

            serializer = AvatarPhotoSerializer(photo, context={'request': request})
            data = serializer.data
            data["name"] = name
            data["url"] = url

            return Response(data, status=status.HTTP_201_CREATED)


        except Profile.DoesNotExist:
            return Response({"details":"Internal server error! Can not find Profile object."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated, ])
@parser_classes([MultiPartParser, FormParser])
def upload_card_photo(request, pk, format=None):
    if request.method == "POST":
        try:
            profile_from_request = Profile.objects.get(profileuser=request.user)

            # pk为明信片的Id
            card_host = Card.objects.get(pk=int(pk))

            ### get the recipient and sender of the card
            recipient = card_host.torecipient
            sender = card_host.fromsender

            # 确保目前登录用户就是明信片的接受者
            if profile_from_request.id == recipient.id or profile_from_request.id == sender.id:
                f = request.FILES['cardphoto']
                f.name = utils.hash_file_name(f.name)

                photo = CardPhoto(owner=profile_from_request,
                                  card_host=card_host,
                                  card_photo=f)
                photo.save()

                name = photo.card_photo.name
                url = photo.card_photo.url

                serializer = CardPhotoSerializer(photo, context={'request': request})
                data = serializer.data
                data["name_on_server"] = name
                data["url_on_server"] = url

                return Response(data, status=status.HTTP_201_CREATED)
            else:
                Response({"details": "card recipient!= profileuser, sender !=profileuser",
                          "id1": recipient.id,
                          "id2": profile_from_request.id},
                         status= status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response({"details":"Current logged user's profile does not exist"},
                            status=status.HTTP_404_NOT_FOUND)

        except Card.DoesNotExist:
            return Response({"details": "Postcard with id %s does not exist" % pk},
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
                ## photo = AvatarPhoto(owner=exchcard_backend_api, avatar=request.data["avatar"])
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
            return Response({"details":"exchcard_backend_api id %s does not exist" % pk},
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

