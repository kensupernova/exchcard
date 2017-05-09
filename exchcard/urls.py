#coding:utf-8
from django.conf.urls import include, url


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
## admin.exchard.admin_view("Exchange Postcard Administration Site")
admin.autodiscover()

urlpatterns = [
    url(r'^$', 'exchcard.views.index'),
    url(r'^account/login/$', 'exchcard.views.user_login'),
    url(r'^account/register/$', 'exchcard.views.user_register'),
    url(r'^account/resetpassword/$', 'exchcard.views.profile'),
    url(r'^account/findpassword/$', 'exchcard.views.profile'),

    url(r'^profile/$', 'exchcard.views.profile'),
    url(r'^card/send/$', 'exchcard.views.card_send'),
    url(r'^card/send/confirm/$', 'exchcard.views.card_send_confirm'),
    url(r'^card/travelling/(?P<cardname>.+)/$', 'exchcard.views.card_travelling'),
    url(r'^card/register/$', 'exchcard.views.card_register'),
    url(r'^card/(?P<cardname>.+)/$', 'exchcard.views.view_single_card'),
    url(r'^profile/(?P<id>.+)/cards/$', 'exchcard.views.view_cards_list'),

    url(r'^moments/$', 'exchcard.views.view_shao_you_quan'),

    url(r'^search/$', 'exchcard.views_search.search'),
    url(r"^storage/s3/$", "exchcard_backend_api.upload_views.s3_storage"),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^exchcard/api/', include('exchcard_backend_api.urls')),
    url(r'^oneverse/api/', include('oneverse_api.urls')),

]
