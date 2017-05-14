#coding: utf-8

from django.conf.urls import url, include

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from exchcard_backend_api import card_api, profile_api, address_api, user_api, upload_api, apis

urlpatterns = format_suffix_patterns([
    url(r"^$", apis.root),

    ## authentication and registeration
    url(r"^auth/", "exchcard_backend_api.user_api.user_auth", name="auth"),
    url(r"^login/", "exchcard_backend_api.user_api.user_login", name="login"),
    url(r"^logout/", "exchcard_backend_api.user_api.user_logout", name="logout"),
    url(r"^register/$", "exchcard_backend_api.profile_api.register_user_address_profile",
        name="exchcard_backend_api-user-address-register"),
    url(r"^register2/$", profile_api.RegisterUserAddressProfileView.as_view(),
        name="exchcard_backend_api-user-address-register2"),

    ## users
    url(r"^users/$", user_api.UserList.as_view(),
        name="user-list"),
    url(r"^users/register/", user_api.RegisterUserView.as_view(),
        name="user-register"),
    url(r"^users/(?P<pk>[0-9]+)/$", user_api.UserDetail.as_view(),
        name="user-detail"),
    ## 得到当前登录用户信息
    url(r'^users/get/info/$',
        "exchcard_backend_api.user_api.get_info_of_logged_user",
        name="user-get-info"),

    ## addresss
    url(r'^address/$', address_api.GetAllAddressListView.as_view(),
        name="address-list"),
    url(r'^address/register/$', address_api.RegisterAddressView.as_view(),
        name="address-register"),
    url(r'^address/getrandom/$', address_api.GetOneAddressView.as_view(),
        name="address-random"),
    url(r'^address/get/id/(?P<pk>[0-9]+)/$', address_api.GetAddressView.as_view(),
        name="address-get-id"),
    url(r'^address/get/name/(?P<name>.+)/$', address_api.GetAddressViewWithName.as_view(),
        name="address-get-name"),
    url(r'^address/update/(?P<pk>[0-9]+)/$',
        "exchcard_backend_api.address_api.update_address_with_profile_id",
        name="address-update-with-profile-id"),
    ## 得到当前登录用户的地址
    url(r'^address/get/info/$',
        "exchcard_backend_api.address_api.get_address_of_logged_user",
        name="address-of-logged-user"),

    ## profiles
    url(r"^profiles/$", profile_api.GetProfileListView.as_view(),
        name="profile-list"),
    url(r"^profiles/(?P<pk>[0-9]+)/$", profile_api.GetProfileDetailView.as_view(),
        name="profile-detail"),
    url(r"^profiles/register/$", profile_api.RegisterProfileView.as_view(),
        name="profile-register"),
    url(r"^profiles/register/ids/$",
        "exchcard_backend_api.profile_api.register_new_profile_with_ids",
        name="profile-register-with-ids"),
    url(r"^profiles/update/$",
        "exchcard_backend_api.profile_api.update_profile_with_ids",
        name="profile-update-with-ids"),
    url(r"^profiles/getrandom/$",
        "exchcard_backend_api.profile_api.get_random_profile",
        name="profile-getrandom-for-card"),

    ## 头像图片
    url(r'^profiles/avatar/url/$',
        "exchcard_backend_api.upload_api.get_avatar_url"),
    url(r'^profiles/avatar/upload/$',
        "exchcard_backend_api.upload_api.upload_avatar",
        name="profile-avatarphoto-upload"),
    url(r'^profiles/(?P<pk>[0-9]+)/avatar/upload2/$', upload_api.AvatarUploadView.as_view(),
        name="profile-avatarphoto-upload2"),

    url(r"^profiles/photos/$",
        upload_api.AvatarPhotoList.as_view(),
        name="avatarphoto-list"),
    url(r"^profiles/photos/(?P<pk>[0-9]+)/$",
        upload_api.AvatarPhotoDetail.as_view(),
        name="avatarphoto-detail"),

    ## 查看总的各状态的明信片
    url(r"^profiles/(?P<pk>[0-9]+)/cards/allstate/count/$",
        "exchcard_backend_api.profile_api.profile_get_cards_all_state_count",
        name="profile-get-cards-allstate-count"),

    ## 查看各个状态的明信片
    url(r"^profiles/(?P<pk>[0-9]+)/cards/total/$",
        "exchcard_backend_api.profile_api.profile_get_cards_total",
        name="profile-get-cards-total"),

    #### 接受之所以用receive, 是因为包括发出去未到的，和已经到达的两种
    url(r"^profiles/(?P<pk>[0-9]+)/cards/sent/total/$",
        "exchcard_backend_api.profile_api.profile_get_cards_sent_total",
        name="profile-get-cards-sent"),
    url(r"^profiles/(?P<pk>[0-9]+)/cards/receive/total/$",
        "exchcard_backend_api.profile_api.profile_get_cards_receive_total",
        name="profile-get-cards-receive"),

    url(r"^profiles/(?P<pk>[0-9]+)/cards/sent/travelling/$",
        "exchcard_backend_api.profile_api.profile_get_cards_sent_travelling",
        name="profile-get-cards-sent-travelling"),
    url(r"^profiles/(?P<pk>[0-9]+)/cards/receive/travelling/$",
        "exchcard_backend_api.profile_api.profile_get_cards_receive_travelling",
        name="profile-get-cards-receive-travelling"),

    url(r"^profiles/(?P<pk>[0-9]+)/cards/sent/arrived/$",
        "exchcard_backend_api.profile_api.profile_get_cards_sent_arrived",
        name="profile-get-cards-sent-arrived"),
    url(r"^profiles/(?P<pk>[0-9]+)/cards/receive/arrived/$",
        "exchcard_backend_api.profile_api.profile_get_cards_receive_arrived",
        name="profile-get-cards-receive-arrived"),


    ## cards
    url(r"^cards/$", card_api.CardList.as_view(),
        name="card-list"),
    url(r"^cards/(?P<pk>[0-9]+)/$", card_api.CardDetail.as_view(),
        name="card-detail"),
    ## 创建新的明信片，当用户申请邮寄地址时创建，并把明信片收信人地址返回
    url(r"^cards/add/$",
        "exchcard_backend_api.card_api.add_new_card",
        name="card-add"),

    ## 当明信片到达，接收方注册
    url(r"^cards/receive/$",
        "exchcard_backend_api.card_api.receive_a_card",
        name="card-receive"),
    ## 注册明信片，带照片
    url(r"^cards/receive/photo/$",
        "exchcard_backend_api.card_api.receive_a_card_with_photo",
        name="card-receive-with-photo"),

    url(r"^cards/(?P<pk>[0-9]+)/update/$",
        "exchcard_backend_api.card_api.update_destrory_card",
        name="card-update"),
    url(r"^cards/(?P<pk>[0-9]+)/hasarrived/$",
        "exchcard_backend_api.card_api.card_check_isarrived",
        name="card-check-arrive"),
    url(r"^cards/(?P<pk>[0-9]+)/cardphotos/(?P<photoid>[0-9]+)/dianzan/$",
        "exchcard_backend_api.card_api.card_dianzan",
        name="card-dianzan"),
    url(r"^cards/(?P<pk>[0-9]+)/cardphotos/(?P<photoid>[0-9]+)/dianzans/$",
        "exchcard_backend_api.card_api.card_dianzans",
        name="card-dianzans"),
    url(r"^cards/(?P<pk>[0-9]+)/dianzans2/$", card_api.DianzanListView.as_view(),
        name="card-dianzans-2"),
    url(r"^cards/(?P<pk>[0-9]+)/cardphoto/$", 'exchcard_backend_api.upload_api.upload_card_photo',
        name="card-cardphoto"),
    ## 明信片实时信息
    url(r"cards/feed/", "exchcard_backend_api.card_api.cards_feed", name="cards-feed"),

    ## 其他
    url(r"^storage/s3/$", "exchcard_backend_api.upload_api.s3_storage"),


    ])

urlpatterns += [
    ## django rest framework authentication
    url(r"^api-auth/", include('rest_framework.urls', namespace='rest_framework')),
]
