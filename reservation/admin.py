from django.contrib import admin

from .models import *

admin.site.register(Reservation)

admin.site.register(Zone)

admin.site.register(User)

admin.site.register(Team)

admin.site.register(TeamMember)