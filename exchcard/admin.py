#coding: utf-8

from django.contrib.admin import AdminSite
from django.contrib import admin
from django.utils.translation import ugettext_lazy

from exchcard.models import Address, Card, Profile


class MyAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('Exchange Postcard Administration Site')

    ## Text to put in each page's <h1>.
    site_header = ugettext_lazy('Exchange Postcard  Administration')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('Exchange Postcard  Administration')



admin_site = MyAdminSite()


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



# 注册对于模型的后台管理
admin.site.register(Address, AddressAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Profile, ProfileAdmin)

