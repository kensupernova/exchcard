#coding:utf-8
from django.conf.urls import include, url
# from django.views.generic.simple import direct_to_template
from django.views.generic.base import TemplateView
from exchcard import settings

# To enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^$', 'exchcard.views.index'),
    url(r'^account/login/$', 'exchcard.views.user_login'),
    url(r'^account/register/$', 'exchcard.views.user_register'),
    url(r'^account/resetpassword/$', 'exchcard.views.profile'),
    url(r'^account/findpassword/$', 'exchcard.views.profile'),

    #设置
    url(r'^setting/$', 'exchcard.views.setting'),

    # view the current logged user's profile
    url(r'^profile/$', 'exchcard.views.profile'),

    # send a card
    url(r'^card/send/$', 'exchcard.views.card_send'),
    url(r'^card/send/confirm/$', 'exchcard.views.card_send_confirm'),
    # 查看还在路途中的某张明信片
    url(r'^card/travelling/(?P<cardname>.+)/$', 'exchcard.views.card_travelling'),
    # register a card
    url(r'^card/receive/$', 'exchcard.views.card_receive'),
    # view a card with cardname
    url(r'^card/(?P<cardname>.+)/$', 'exchcard.views.view_single_card'),

    # view current logged user's cards list
    # url(r'^profile/(?P<id>.+)/cards/$', 'exchcard.views.view_cards_list'),
    url(r'^profile/cards/$', 'exchcard.views.view_cards_list'),

    # view other's public profile page
    url(r'^u/(?P<username>.+)/cards/$', 'exchcard.views.view_others_public_profile'),

    # 发烧友圈子
    url(r'^moments/$', 'exchcard.views.view_shao_you_quan'),


    # 后台管理
    url(r'^admin/', include(admin.site.urls)),

    # 前后端分离设计，这是后端API设计，基于rest framework
    url(r'^exchcard/api/', include('exchcard_backend_api.urls')),
    url(r'^oneverse/api/', include('oneverse_api.urls')),

    # oneverse的url
    url(r'^oneverse/', include('oneverse.urls')),

    # 服务静态HTML文件
    url(r'^html/$', TemplateView.as_view(template_name='index.html')),

    # 服务MEDIA_ROOT里面的文件
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT, }),
    # Method 2 :
    # urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    # 其他
    url(r'^search/$', 'exchcard.views_search.search'),



]
