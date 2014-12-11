from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import BaseIssuer, Address, Color

admin.site.register(BaseIssuer, SimpleHistoryAdmin)
admin.site.register(Color, SimpleHistoryAdmin)
admin.site.register(Address, SimpleHistoryAdmin)
