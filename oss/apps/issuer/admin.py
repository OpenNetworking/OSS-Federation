from django.contrib import admin
from .models import Issuer, Address, AddressHistory, Color, ColorHistory

# Register your models here.
admin.site.register(Issuer)
admin.site.register(Color)
admin.site.register(ColorHistory)
admin.site.register(Address)
admin.site.register(AddressHistory)
