from django.conf.urls import include, url
from oneverse import views

urlpatterns = [
    url(r'^$', 'oneverse.views.oneverse_get_one_today'),
    url(r'^gcm/register/$', 'oneverse.gcm_views.save_user_gcm_registration_id'),
    url(r'^add/$', views.CreateVerseView.as_view()),
    url(r'^list/$', views.ListVerseView.as_view()),
    url(r'^update/(?P<id>[0-9]+)/$', views.UpdateVerseView.as_view(),
        name="verse-detail"),
]
