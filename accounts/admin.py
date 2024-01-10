from django.contrib import admin

from accounts.models import *

class RiderProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'user')

admin.site.register(RiderProfile, RiderProfileAdmin)


class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'user')

admin.site.register(DriverProfile, DriverProfileAdmin)