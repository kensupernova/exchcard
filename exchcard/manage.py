# coding: utf-8
from django.db.models import Manager

## manage the model create, delete, etc.
class DetailedAddressManager(Manager):
    def create_detailed_address(self, first, second, third, city, stateorprovince, country):
        detailedAddress = self.create(first, second, third, city, stateorprovince, country)
        return detailedAddress

class AddressManager(Manager):
    def create_address(self, name, address, postcode):
        address_object = self.create(name=name, address=address, postcode=postcode)
        return address_object


