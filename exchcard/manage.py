# coding: utf-8
from django.db.models import Manager

## manage the model, create, delete, etc.
class DetailedAddressManager(Manager):
    def create_detailed_address(self, first, second, third, city, stateorprovince, country):
        detailedAddress = self.create(first, second, third, city, stateorprovince, country) ## 可以省去save
        detailedAddress.save()
        return detailedAddress

class AddressManager(Manager):
    def create_address(self, name, address, postcode):
        address_object = self.create(name=name, address=address, postcode=postcode)
        address_object.save()
        return address_object

    def create_address_with_full_text(self, name, address, postcode, full_text_address):
        obj = self.create(name=name, address=address, postcode=postcode, full_text_address=full_text_address)
        obj.save()
        return obj
    def create_address_all_information(self, name, address, postcode, city, country, full_text_address):
        obj = self.create(name=name, address=address, postcode=postcode,
                          city = city,
                          country = country,
                          full_text_address=full_text_address)
        obj.save()
        return obj

