#coding:utf-8
from django.conf.urls import include, url


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
## admin.mysite.admin_view("Exchange Postcard Administration Site")
admin.autodiscover()

urlpatterns = [
    url(r'^$', 'mysite.views.home'),
    url(r'^account/login/$', 'mysite.views.user_login'),
    url(r'^account/register/$', 'mysite.views.user_register'),
    url(r'^account/resetpassword/$', 'mysite.views.profile'),
    url(r'^profile/$', 'mysite.views.profile'),
    url(r'^card/send/$', 'mysite.views.card_send'),
    url(r'^card/send/confirm/$', 'mysite.views.card_send_confirm'),
    url(r'^card/travelling/(?P<cardname>.+)/$', 'mysite.views.card_travelling'),
    url(r'^card/register/$', 'mysite.views.card_register'),
    url(r'^card/(?P<cardname>.+)/$', 'mysite.views.view_single_card'),
    url(r'^profile/(?P<id>.+)/cards/$', 'mysite.views.view_cards_list'),

    url(r'^moments/$', 'mysite.views.view_shao_you_quan'),

    url(r'^search/$', 'mysite.views_search.search'),
    url(r"^storage/s3/$", "exchcard_backend_api.upload_views.s3_storage"),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^exchcard_backend_api/api/', include('exchcard_backend_api.urls')),
    url(r'^oneverse/api/', include('oneverse.urls')),

]
