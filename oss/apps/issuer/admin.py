from django.contrib import admin
from .models import Color, Issuer, ActiveAddress, HistoryAddress

# Register your models here.
admin.site.register(Color)
admin.site.register(Issuer)
admin.site.register(ActiveAddress)
admin.site.register(HistoryAddress)
