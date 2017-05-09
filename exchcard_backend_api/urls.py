#coding: utf-8

from django.conf.urls import url, include

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from exchcard_backend_api import card_views, profile_views, address_views, account_views, upload_views

urlpatterns = format_suffix_patterns([
    url(r"^$", card_views.api_root),
    ## authentication
    url(r"^auth/", "exchcard_backend_api.account_views.user_auth", name="auth"),
    url(r"^login/", "exchcard_backend_api.account_views.user_login", name="login"),
    url(r"^logout/", "exchcard_backend_api.account_views.user_logout", name="logout"),
    url(r"^register/$", "exchcard_backend_api.profile_views.api_register_user_address_profile",
        name="exchcard_backend_api-user-address-register"),
    url(r"^account/register2/$", profile_views.RegisterUserAddressProfileView.as_view(),
        name="exchcard_backend_api-user-address-register2"),

    ## users
    url(r"^users/$", account_views.UserList.as_view(),
        name="user-list"),
    url(r"^users/register/", account_views.RegisterUserView.as_view(),
        name="user-register"),
    url(r"^users/(?P<pk>[0-9]+)/$", account_views.UserDetail.as_view(),
        name="user-detail"),

    ## addresss
    url(r'^address/$', address_views.GetAllAddressListView.as_view(),
        name="address-list"),
    url(r'^address/register/$', address_views.RegisterAddressView.as_view(),
        name="address-register"),
    url(r'^address/getrandom/$', address_views.GetOneAddressView.as_view(),
        name="address-random"),
    url(r'^address/get/id/(?P<pk>[0-9]+)/$', address_views.GetAddressView.as_view(),
        name="address-get-id"),
    url(r'^address/get/name/(?P<name>.+)/$', address_views.GetAddressViewWithName.as_view(),
        name="address-get-name"),
     url(r'^address/update/(?P<pk>[0-9]+)/$', "exchcard_backend_api.address_views.api_update_address_with_profile_id",
        name="address-update-with-profile-id"),

    ## profiles
    url(r"^profiles/$", profile_views.GetProfileListView.as_view(),
        name="profile-list"),
    url(r"^profiles/(?P<pk>[0-9]+)/$",  profile_views.GetProfileDetailView.as_view(),
        name="profile-detail"),
    url(r"^profiles/register/$", profile_views.RegisterProfileView.as_view(),
        name="profile-register"),
    url(r"^profiles/register/ids/$", "exchcard_backend_api.profile_views.api_register_new_profile_with_ids",
        name="profile-register-with-ids"),
    url(r"^profiles/update/$", "exchcard_backend_api.profile_views.api_update_profile",
        name="profile-update"),
    url(r"^profiles/getrandom/$", "exchcard_backend_api.profile_views.api_get_random_profile",
        name="profile-getrandom-for-card"),

    url(r'^profiles/(?P<pk>[0-9]+)/avatar/$', "exchcard_backend_api.upload_views.upload_avatar",
        name="profile-avatarphoto-upload"),
    url(r'^profiles/(?P<pk>[0-9]+)/avatarf/$', upload_views.AvatarUploadView.as_view(),
        name="profile-avatarphoto-uploadf"),

    url(r"^profiles/photos/$",
        upload_views.AvatarPhotoList.as_view(),
        name="avatarphoto-list"),
    url(r"^profiles/photos/(?P<pk>[0-9]+)/$",
        upload_views.AvatarPhotoDetail.as_view(),
        name="avatarphoto-detail"),

    url(r"^profiles/(?P<pk>[0-9]+)/cards/count/$", "exchcard_backend_api.profile_views.api_profile_get_cards_count",
        name="profile-get-cards-count"),
    url(r"^profiles/(?P<pk>[0-9]+)/cards/total/$", "exchcard_backend_api.profile_views.api_profile_get_cards_total",
        name="profile-get-cards-total"),
    url(r"^profiles/(?P<pk>[0-9]+)/cards/sent/total/$", "exchcard_backend_api.profile_views.api_profile_get_cards_sent_total",
        name="profile-get-cards-sent"),
    url(r"^profiles/(?P<pk>[0-9]+)/cards/receive/total/$", "exchcard_backend_api.profile_views.api_profile_get_cards_receive_total",
        name="profile-get-cards-receive"),
    url(r"^profiles/(?P<pk>[0-9]+)/cards/sent/travelling/$", "exchcard_backend_api.profile_views.api_profile_get_cards_sent_travelling",
        name="profile-get-cards-sent-travelling"),
    url(r"^profiles/(?P<pk>[0-9]+)/cards/receive/travelling/$", "exchcard_backend_api.profile_views.api_profile_get_cards_receive_travelling",
        name="profile-get-cards-receive-travelling"),
    url(r"^profiles/(?P<pk>[0-9]+)/cards/sent/arrived/$", "exchcard_backend_api.profile_views.api_profile_get_cards_sent_arrived",
        name="profile-get-cards-sent-arrived"),
    url(r"^profiles/(?P<pk>[0-9]+)/cards/receive/arrived/$", "exchcard_backend_api.profile_views.api_profile_get_cards_receive_arrived",
        name="profile-get-cards-receive-arrived"),


    ##
## cards
    url(r"^cards/$", card_views.CardList.as_view(),
        name="card-list"),
    url(r"^cards/(?P<pk>[0-9]+)/$", card_views.CardDetail.as_view(),
        name="card-detail"),
    url(r"^cards/add/$", "exchcard_backend_api.card_views.api_add_new_card",
        name="card-add"),
    url(r"^cards/receive/$", "exchcard_backend_api.card_views.api_receive_a_card",
        name="card-receive"),
    url(r"^cards/receive/photo/$", "exchcard_backend_api.card_views.api_receive_a_card_with_photo",
        name="card-receive-with-photo"),
    url(r"^cards/(?P<pk>[0-9]+)/update/$", "exchcard_backend_api.card_views.api_update_destrory_card",
        name="card-update"),
    url(r"^cards/(?P<pk>[0-9]+)/hasarrived/$", "exchcard_backend_api.card_views.api_card_check_isarrived",
        name="card-check-arrive"),
    url(r"^cards/(?P<pk>[0-9]+)/cardphotos/(?P<photoid>[0-9]+)/dianzan/$", "exchcard_backend_api.card_views.api_card_dianzan",
        name="card-dianzan"),
    url(r"^cards/(?P<pk>[0-9]+)/cardphotos/(?P<photoid>[0-9]+)/dianzans/$", "exchcard_backend_api.card_views.api_card_dianzans",
        name="card-dianzans"),
    url(r"^cards/(?P<pk>[0-9]+)/dianzans2/$", card_views.DianzanListView.as_view(),
        name="card-dianzans-2"),
    url(r"^cards/(?P<pk>[0-9]+)/cardphoto/$", 'exchcard_backend_api.upload_views.api_upload_card_photo',
        name="card-cardphoto"),
    url(r"cardsfeed/", "exchcard_backend_api.card_views.api_cardsfeed", name="cards-feed")

    ])

urlpatterns += [
    ## django rest framework authentication
    url(r"^api-auth/", include('rest_framework.urls', namespace='rest_framework')),
]
