#coding: utf-8

from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy

class MyAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('Exchange Postcard Administration Site')

    # # Text to put in each page's <h1>.
    site_header = ugettext_lazy('Exchange Postcard  Administration')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('Exchange Postcard  Administration')

admin_site = MyAdminSite()