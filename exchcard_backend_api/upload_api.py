#coding:utf-8
import datetime

from django.shortcuts import Http404

from exchcard.models_main import AvatarPhoto, CardPhoto, Card, Profile
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

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated, ])
@parser_classes([MultiPartParser, FormParser])
def upload_avatarphoto_by_profile_id(request, pk, format=None):
    """
    主要在settting中设置storage
    :param request:
    :param pk:
    :param format:
    :return:
    """
    if request.method == "POST":
        try:
            profile_from_request = Profile.objects.get(profileuser=request.user)
            if int(pk) == int(profile_from_request.id):
                profile = Profile.objects.get(pk=int(pk))
                photo = AvatarPhoto(owner=profile, avatar=request.data['avatar'])
                photo.save()

                name = photo.avatar.name
                url = photo.avatar.url

                serializer = AvatarPhotoSerializer(photo, context={'request': request})
                data = serializer.data
                data["name"] = name
                data["url"] = url

                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response({"details": "request user != user from url",
                                 "id1": pk,
                                 "id2:": profile_from_request.id },
                                 status=status.HTTP_403_FORBIDDEN)

        except Profile.DoesNotExist:
            return Response({"details": "profile of logged user does not exist"},
                          status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated, ])
@parser_classes([MultiPartParser, FormParser])
def upload_avatarphoto(request):
    if request.method == "POST":
        try:
            profile = Profile.objects.get(profileuser=request.user)

            # DJANGO REST, parse request.body
            # print request.data

            # DJANGO
            # print request.FILES
            # print request.POST

            ## 前端按照有表单Form, 文件在request.FILES里面, 也在request.data里面

            # 上传的文件
            f = request.FILES['avatar']
            # 改变文件名，注意不要改变文件格式后缀
            f.name = utils.hash_file_name(f.name)

            photo = AvatarPhoto(owner=profile, avatar=f)
            photo.save()

            serializer = AvatarPhotoSerializer(photo, context={'request': request})
            data = serializer.data

            data["avatarHasBaseUrl"] = 1

            return Response(data=data, status=status.HTTP_201_CREATED)

        except Profile.DoesNotExist:
            return Response({"details":"Internal server error! Can not find Profile object."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AvatarUploadView(APIView):
    parser_classes = ([MultiPartParser, FormParser]) ## only key is file
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def post(self, request, pk, format=None):

        try:
            profile_from_request = Profile.objects.get(profileuser=request.user)
            if int(pk) == profile_from_request.id:
                profile = Profile.objects.get(pk=int(pk))
                photo = AvatarPhoto(owner=profile, avatar=request.data['avatar'])
                photo.save()

                name = photo.avatar.name
                url = photo.avatar.url

                aserializer = AvatarPhotoSerializer(photo, context={'request': request})
                data = aserializer.data
                data["name"] = name
                data["avatar_url"] = url

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
           serializer.save() # 会保存并返回得到一个object

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

    def put(self, request, pk, format=None):
        photo = self.get_object(pk)
        serializer = AvatarPhotoSerializer(photo, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        photo = self.get_object(pk)
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def pre_save(self, obj):
        obj.owner = Profile.objects.get(profileuser=self.request.user)


