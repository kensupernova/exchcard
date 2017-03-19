#coding: utf-8

from django.contrib import admin
from models import Address, Card, Profile

# a class to customize admin the models
class AddressAdmin(admin.ModelAdmin):
    #field display on change list in admin mysite
    fields = ('name','address', 'postcode')



class CardAdmin(admin.ModelAdmin):
    #field display on change list in admin mysite
    fields = ('card_name','torecipient', "fromsender")

class ProfileAdmin(admin.ModelAdmin):
    #field display on change list in admin mysite
    model = Profile
    fields = ('profileaddress', 'profileuser')


admin.site.register(Address, AddressAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Profile, ProfileAdmin)
