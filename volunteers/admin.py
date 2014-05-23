from django.contrib import admin
from volunteers.models import Volunteer


class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Volunteer, VolunteerAdmin)
