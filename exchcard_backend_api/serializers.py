#coding: utf-8
from django.contrib.auth import get_user_model # If used custom user mode
User = get_user_model()
# from django.contrib.auth.models import User

from rest_framework import serializers

from exchcard.models_profile import Card, Profile, Address, AvatarPhoto, CardPhoto
from exchcard.models_activity import DianZan



class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    用户序列化类
    """
    class Meta:
        model = User
        fields =('url', 'username', "email")


class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=("username", "email") ### password can not be read


class RegisterUserSerializer1(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) ## 密码write only, can not be read

    class Meta:
        model = get_user_model()

    def create(self, validated_data):

        user = get_user_model().objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password']) ## 密码只能这样创建
        user.save()

        return user


class RegisterUserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        read_only_fields = ('id',)  ## read only, can not be written
        write_only_fields = ('password',) ## write only, can not be read


    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user



class UserAddressProfileSerializer(serializers.ModelSerializer):
    """
    注册新的Profile, 会创建一个User, 一个Address, 一个Profile
    """
    username = serializers.CharField(source="profileuser.username")
    password = serializers.CharField(source="profileuser.password")
    email = serializers.CharField(source="profileuser.email")

    name = serializers.CharField(source="profileaddress.name")
    address = serializers.CharField(source="profileaddress.address")
    postcode = serializers.CharField(source="profileaddress.postcode")

    class Meta:
        model = Profile
        fields = ("id", "username", "password", "email",
                  "name", "address", "postcode")



###################################################################################
"""
明信片序列化类
"""
class CardSerializer(serializers.ModelSerializer):
    # fromsender_username = serializers.CharField(source='fromsender.profileuser.username')

    fromsender_email = serializers.CharField(source='fromsender.profileuser.email')
    fromsender_id = serializers.IntegerField(source='fromsender.id')

    from_name = serializers.CharField(source='fromsender.profileaddress.name')
    from_address = serializers.CharField(source='fromsender.profileaddress.address')
    from_postcode = serializers.CharField(source='fromsender.profileaddress.postcode')

    torecipient_email = serializers.CharField(source='torecipient.profileuser.email')
    torecipient_id = serializers.IntegerField(source='torecipient.id')

    to_name = serializers.CharField(source='torecipient.profileaddress.name')
    to_address = serializers.CharField(source='torecipient.profileaddress.address')
    to_postcode = serializers.CharField(source="torecipient.profileaddress.postcode")


    class Meta:
        model = Card
        fields = ("url", "card_name",
                  "fromsender_id", "fromsender_email", "from_name","from_address", "from_postcode",
                  "torecipient_id", "torecipient_email", "to_name", "to_address", "to_postcode",
                  "sent_time", "arrived_time",
                  "sent_date", "arrived_date", "has_arrived")


class CreateCardSerializer(serializers.ModelSerializer):
    fromsender_id = serializers.IntegerField(source='fromsender.id')
    torecipient_id = serializers.IntegerField(source='torecipient.id')

    class Meta:
        model = Card
        fields = ("card_name",
                  "fromsender_id",
                  "torecipient_id"
                  )

    def create(self, validated_data):
        # print validated_data
        ## card name should be generated from sever to avoid duplicates?
        ## print validated_data
        card = Card.objects.create_with_profile_ids(
            card_name=validated_data["card_name"],
            torecipient_id=validated_data["torecipient"]["id"],
            fromsender_id=validated_data["fromsender"]["id"]
        )

        if card != None:
            card.save()
        else:
            return None

        return card


"""
地址序列化类
"""
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("id", "name", "address", "postcode")

class SimpleAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("id", "name", "address", "postcode")

class AddressSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("id", "name", "city", "country")

class FullTextAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("id", "full_text_address")

###################################################################################
"""
创建Profile序列化类
"""
class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields=("profileuser", "profileaddress")

    def create(self, validated_data):
        # print "----------------------------"
        # print validated_data
        profile = Profile.objects.create(
            profileuser=validated_data['profileuser'],
            profileaddress=validated_data['profileaddress'],
        )

        profile.save()

        return profile



class CreateProfileSerializerWithIds(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields=("profileuser_id", "profileaddress_id")

    def create(self, validated_data):
        # print "----------------------------"
        # print validated_data
        profile = Profile.objects.create_profile_with_ids(
            addressid=validated_data['addressid'],
            userid=validated_data['userid'],
        )

        profile.save()

        return profile



class GetProfileSerializer(serializers.HyperlinkedModelSerializer):
    """
    Get Profile序列化
    """
    profileuser_id = serializers.CharField(source="profileuser.id")
    profileuser_username = serializers.CharField(source="profileuser.username")
    profileuser_email = serializers.CharField(source="profileuser.email")

    profileaddress_id = serializers.CharField(source="profileaddress.id")
    profileaddress_name = serializers.CharField(source="profileaddress.name")
    profileaddress_address = serializers.CharField(source="profileaddress.address")
    profileaddress_postcode = serializers.CharField(source="profileaddress.postcode")

    class Meta:
        model = Profile
        fields=("id", "url", "profileuser_id", "profileuser_username", 'profileuser_email',
                "profileaddress_id",
                "profileaddress_name",
                "profileaddress_address",
                "profileaddress_postcode"
                )
        related_fields = ["user", "address"]



class GetProfileWithCardSerializer(serializers.HyperlinkedModelSerializer):
    profileuser_username = serializers.CharField(source="profileuser.username")

    profileaddress_name = serializers.CharField(source="profileaddress.name")
    profileaddress_address = serializers.CharField(source="profileaddress.address")
    profileaddress_postcode= serializers.CharField(source="profileaddress.postcode")

    # sent_cards = serializers.HyperlinkedIdentityField(many=True,
    #     view_name="card-detail", read_only=True)
    #
    # receive_cards = serializers.HyperlinkedIdentityField(many=True,
    #     view_name="card-detail", read_only=True)

    sent_cards = serializers.HyperlinkedRelatedField(many=True,
                                                     view_name="card-detail",
                                                     read_only=True)

    receive_cards = serializers.HyperlinkedRelatedField(many=True,
                                                        view_name="card-detail",
                                                        read_only=True)

    class Meta:
        model = Profile
        fields=("id",
                "url",
                "profileuser_username",
                "profileaddress_name",
                "profileaddress_address",
                "profileaddress_postcode",
                "sent_cards", "receive_cards")
        related_fields = ["user", "address"]



class GetUserAddressProfileSerializer(serializers.ModelSerializer):
    """
    address, exchcard_backend_api id,address Id, user id, user name serializer
    """
    profile_id = serializers.CharField(source="id")
    profile_user_id  = serializers.CharField(source="profileuser.id")
    profile_address_id = serializers.CharField(source="profileaddress.id")

    username = serializers.CharField(source="profileuser.username")

    name = serializers.CharField(source="profileaddress.name")
    address = serializers.CharField(source="profileaddress.address")
    postcode = serializers.CharField(source="profileaddress.postcode")

    class Meta:
        model = Profile
        fields =("url", "profile_id",
                 "profile_user_id",
                 "profile_address_id",
                 "username",
                 "name","address", "postcode")


###################################################################################
class AvatarPhotoSerializer(serializers.ModelSerializer):
    """
    只有avatar 包含全地址
    avatar_url 仅仅包含path
    """
    # owner_username = serializers.CharField(source='owner.profileuser.username')
    owner_email = serializers.CharField(source='owner.profileuser.email')
    owner_id = serializers.IntegerField(source="owner.id")
    avatar_url = serializers.CharField(source='avatar.url')


    class Meta:
        model = AvatarPhoto
        fields = ('id', 'avatar', 'avatar_url',"owner_id", "owner_email")

class ProfileWithAvatarPhotoSerializer(serializers.HyperlinkedModelSerializer):
    profileuser_username = serializers.CharField(source="profileuser.username")
    profileuser_email = serializers.CharField(source="profileuser.email")

    avatars = serializers.HyperlinkedIdentityField(many=True,
        view_name="avatarphoto-detail", read_only=True) #用户所有的头像图片

    class Meta:
        model = Profile
        fields=("id", "profileuser_username", "profileuser_email", "avatars")

class CreateAvatarPhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AvatarPhoto
        fields = ('avatar', "id")

    def create(self, validated_data):
        return AvatarPhoto(**validated_data)

###################################################################################
class CardPhotoSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.CharField(source='owner.profileuser.username')
    owner_id = serializers.IntegerField(source="owner.id")
    card_host = serializers.CharField(source="card_host.card_name")
    card_host_id = serializers.IntegerField(source="card_host.id")

    class Meta:
        model = CardPhoto
        fields = ('id', 'owner', "owner_id", "card_host", "card_host_id")


#----------------------------------------------------------------------
class DianZanSerializer(serializers.ModelSerializer):
    person_who_dianzan_id = serializers.IntegerField(source='person_who_dianzan.id')
    class Meta:
        model = DianZan
        fields = ('card_by_dianzan', 'person_who_dianzan_id', 'created')