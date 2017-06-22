# coding: utf-8

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from exchcard_backend_api import card_api, profile_api, address_api, user_api, upload_api, activity_api

urlpatterns = format_suffix_patterns([

    ## authentication and registeration
    url(r"^auth/", "exchcard_backend_api.user_api.user_auth", name="auth"),
    url(r"^login/", "exchcard_backend_api.user_api.user_login_with_email_pw", name="login-email-pw"),
    url(r"^logout/", "exchcard_backend_api.user_api.user_logout", name="logout"),
## --------------------------------------------------------
    url(r"^user/address/register/$", "exchcard_backend_api.profile_api.register_user_address_profile",
        name="user-address-profile-register"),
    url(r"^user/address/register2/$", profile_api.RegisterUserAddressProfileView.as_view(),
        name="user-address-profile-register2"),

## --------------------------------------------------------
    ## users
    url(r"^users/register/", user_api.RegisterUserView.as_view(),
        name="user-register"),
    url(r"^users/register2/", "exchcard_backend_api.user_api.register_new_user",
        name="user-register2"),
    url(r"^users/$", user_api.UserList.as_view(),
        name="user-list"),
    url(r"^users/(?P<pk>[0-9]+)/$", user_api.UserDetail.as_view(),
        name="user-detail"),
    ## 得到当前登录用户信息
    url(r'^users/get/info/$',
        "exchcard_backend_api.user_api.get_info_of_logged_user",
        name="user-get-info"),
    ## 修改用户名
    url(r'^users/update/username/$',
        'exchcard_backend_api.user_api.update_username',
        name='user-username-update'),
    url(r'^users/check/password/$',
        'exchcard_backend_api.user_api.check_password',
        name='user-check-password'),
    url(r'^users/update/password/$',
        'exchcard_backend_api.user_api.update_password',
        name='user-update-password'),
    # 关注某人
    url(r"^users/follow/him/$", "exchcard_backend_api.user_api.make_a_follow_to_him",
        name="user-follow-him"),

## --------------------------------------------------------
    ## addresss
    url(r'^address/create/$', address_api.CreateAddressView.as_view(),
        name="address-create"),
    url(r'^address/profile/create/$', "exchcard_backend_api.address_api.address_profile_create",
        name="address-profile-create"),

    url(r'^address/getrandom/$', address_api.GetOneRandomAddressView.as_view(),
        name="address-random"),
    url(r'^address/$', address_api.GetAllAddressListView.as_view(),
        name="address-list"),
    url(r'^address/get/id/(?P<pk>[0-9]+)/$', address_api.GetAddressView.as_view(),
        name="address-detail-by-id"),
    url(r'^address/get/name/(?P<name>.+)/$', address_api.GetAddressViewWithNameField.as_view(),
        name="address-detail-by-name"),
    url(r'^address/update/$',
        "exchcard_backend_api.address_api.update_address",
        name="address-update"),
    ## 得到当前登录用户的地址
    url(r'^address/get/info/$',
        "exchcard_backend_api.address_api.get_address_of_logged_user",
        name="address-of-logged-user"),

## --------------------------------------------------------
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
        name="profile-get-random-for-sent-card"),

    url(r'^profiles/avatar/url/$',
        "exchcard_backend_api.profile_api.get_avatar_url",
        name="profile-get-avatar-url"),

    ## 头像图片上传
    url(r'^profiles/avatar/upload/$',
        "exchcard_backend_api.upload_api.upload_avatarphoto",
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
    url(r"^profiles/(?P<pk>[0-9]+)/cards/eachstate/count/$",
        "exchcard_backend_api.profile_api.profile_get_cards_each_state_count",
        name="profile-get-cards-allstate-count"),

    ## 查看各个状态的明信片
    url(r"^profiles/(?P<pk>[0-9]+)/cards/all/$",
        "exchcard_backend_api.profile_api.profile_get_all_cards",
        name="profile-get-all-cards-data"),

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


## --------------------------------------------------------
    ## cards
    url(r"^cards/$", card_api.CardList.as_view(),
        name="card-list"),
    url(r"^cards/(?P<pk>[0-9]+)/$", card_api.CardDetail.as_view(),
        name="card-detail"),
    ## 创建新的明信片，当用户申请邮寄地址时创建，并把明信片收信人地址返回
    url(r"^cards/add/no/photo/$",
        "exchcard_backend_api.card_api.add_new_card_no_photo",
        name="card-add-no-photo"),
    url(r"^cards/get/address/$", "exchcard_backend_api.card_api.get_address_before_confirm_send_card",
        name="get-address-only"),
    url(r"^cards/confirm/send/card/$", "exchcard_backend_api.card_api.confirm_send_card",
        name="confirm_send_card"),
    url(r"^cards/confirm/send/card/no/photo/$", "exchcard_backend_api.card_api.confirm_send_card_no_photo",
        name="confirm_send_card_no_photo"),
    url(r"^cards/confirm/send/card/with/photo/$", "exchcard_backend_api.card_api.confirm_send_card_with_photo",
        name="confirm_send_card_with_photo"),

    ## 接收明信片，没有照片
    url(r"^cards/receive/$",
        "exchcard_backend_api.card_api.receive_a_card_no_photo",
        name="card-receive-no-photo"),
    ## 接收明信片，带照片
    url(r"^cards/receive/photo/$",
        "exchcard_backend_api.card_api.receive_a_card_with_photo",
        name="card-receive-with-photo"),

    ## 单独为某明信片上传图片
    url(r"^cards/upload/photo/$",
        "exchcard_backend_api.card_api.upload_cardphoto",
        name="card-upload-photo-after"
        ),
    # 明信片创建，不管是否达到，为明信片上传图片
    url(r"^cards/(?P<card_name>.+)/upload/photo/$",
        "exchcard_backend_api.card_api.upload_cardphoto_afterwards_by_cardname",
        name="card-upload-photo-afterwards"
        ),
    url(r"^cards/(?P<pk>[0-9]+)/upload/photo2/$",
        'exchcard_backend_api.card_api.upload_cardphoto_afterwards_by_id',
        name="card-photo-upload-afterwards2"),

    url(r"^cards/(?P<pk>[0-9]+)/update/$",
        "exchcard_backend_api.card_api.update_destrory_card",
        name="card-update"),
    url(r"^cards/(?P<pk>[0-9]+)/is-arrived/$",
        "exchcard_backend_api.card_api.card_check_is_arrived",
        name="card-check-arrive"),


    ## 明信片实时信息
    url(r"^cards/feeds/$", "exchcard_backend_api.card_api.cards_feeds",
        name="cards-feed"),

## ------------------------------------------------------------
    ## 发烧友
    url(r"^hobbyist/list/page/(?P<number>[0-9]+)/$",
        "exchcard_backend_api.hobbyist_api.get_basic_info_of_hobbyist_list",
        name="hobbyist-list-by-page"),

    ## 某个用户的基本信息
    url(r"^hobbyist/u/(?P<user_id>[0-9]+)/basic/info/$",
        "exchcard_backend_api.hobbyist_api.get_all_basic_info_of_other_user",
        name="get-basic-info-of-other-user"),
    ## 某个用户所有活动
    url(r"^hobbyist/u/(?P<user_id>[0-9]+)/activities/all/$",
        "exchcard_backend_api.hobbyist_api.get_all_activities_of_other_user",
        name="activities-all"),
    # 某个用户的某条活动细节
    url(r"^hobbyist/u/(?P<user_id>[0-9]+)/activity/(?P<action_id>[0-9]+)/$",
        "exchcard_backend_api.hobbyist_api.get_single_activity_detail_of_other_user",
        name="activity-detail"),

    # 某条发送明信片的细节
    url(r"^hobbyist/sent-card/(?P<pk>[0-9]+)/$", activity_api.SentCardActionDetailView.as_view(),
        name="sent-card-activity-detail"),
    # 所有发送明信片的活动
    url(r"^hobbyist/sent-card/list/$", activity_api.SentCardActionListView.as_view(),
        name="sent-card-activity-list"),
#------------------------------------------------------------
    ## 朋友圈
    url(r"^moments/followings/get-activities/$", "exchcard_backend_api.moments_api.get_all_activities_of_my_followings",
        name="get-all-activities-of-my-followings"),
# ---------------------------------------------------------------
#   某个动态得到点赞
    url(r"^moments/activity/toggle-dianzan/$",
            "exchcard_backend_api.activity_api.toggle_dianzan",
            name="toggle_dianzan"),

## ------------------------------------------------------------
    ## 其他
    url(r"^storage/sae/s3/$", "exchcard_backend_api.upload_api.sae_s3_storage"),

    ])

urlpatterns += [
    ## django rest framework authentication
    url(r"^api-auth/", include('rest_framework.urls', namespace='rest_framework')),
]
