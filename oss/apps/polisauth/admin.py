from django.contrib import admin
from .models import Color, Polis, PolisOwner

# Register your models here.

admin.site.register(Color)
admin.site.register(Polis)
admin.site.register(PolisOwner)

