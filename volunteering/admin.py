from django.contrib import admin
from models import Campaign, Duty, Volunteer


class DutyInline(admin.StackedInline):
    model = Duty


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = (DutyInline,)
admin.site.register(Campaign, CampaignAdmin)


class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Volunteer, VolunteerAdmin)
