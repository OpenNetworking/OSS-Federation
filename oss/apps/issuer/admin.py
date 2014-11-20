from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Issuer, Address, Color

admin.site.register(Issuer, SimpleHistoryAdmin)
admin.site.register(Color, SimpleHistoryAdmin)
admin.site.register(Address, SimpleHistoryAdmin)
