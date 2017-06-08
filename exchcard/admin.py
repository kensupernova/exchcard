#coding: utf-8
from django.contrib.admin import AdminSite
from django.contrib import admin
from django.utils.translation import ugettext_lazy

from exchcard.models_main import Address, Card, Profile
from exchcard.models import XUser


"""
后台管理的个性化定制
"""
class MyAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('Exchange Postcard Administration Site')

    ## Text to put in each page's <h1>.
    site_header = ugettext_lazy('Exchange Postcard  Administration')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('Exchange Postcard  Administration')



admin_site = MyAdminSite()


"""
exchcard的后台管理
"""
# a class to customize admin the models
class AddressAdmin(admin.ModelAdmin):
    # field display on change list in admin exchcard
    fields = ('name','address', 'postcode')



class CardAdmin(admin.ModelAdmin):
    # field display on change list in admin exchcard
    fields = ('card_name','torecipient', "fromsender")



class ProfileAdmin(admin.ModelAdmin):
    # field display on change list in admin exchcard
    model = Profile
    fields = ('profileaddress', 'profileuser')

class XUserAdmin(admin.ModelAdmin):
    """
    Extended django.contrib.auth.models.AbstractBaseUser
    """
    model = XUser
    name = 'XUser'
    fields = ('email', 'is_admin', 'is_active', 'type', 'desc')

# 注册对于模型的后台管理
admin.site.register(Address, AddressAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(XUser, XUserAdmin)


