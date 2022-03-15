from django.contrib import admin

from .models import Reservation, Zone

admin.site.register(Reservation)

admin.site.register(Zone)