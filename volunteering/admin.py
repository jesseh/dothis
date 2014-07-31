from django.contrib import admin
from models import (Activity, Assignment, Attribute, Campaign, CampaignEvent,
                    Duty, Event, Location, Volunteer)


class DutyInline(admin.StackedInline):
    model = Duty
    extra = 10


class AttributeAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Attribute, AttributeAdmin)


class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name', 'slug']
admin.site.register(Campaign, CampaignAdmin)


class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'external_id', 'slug']
    readonly_fields = ['slug']
    fields = ['name', 'phone_number', 'external_id', 'slug', 'attributes']
    search_fields = ['name', 'external_id', 'slug']
admin.site.register(Volunteer, VolunteerAdmin)


class DutyAdmin(admin.ModelAdmin):
    list_display = ['id', 'activity', 'event', 'location',
                    'start_time', 'end_time', 'multiple']
admin.site.register(Duty, DutyAdmin)


class CampaignEventAdmin(admin.ModelAdmin):
    pass
admin.site.register(CampaignEvent, CampaignEventAdmin)


class AssignmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Assignment, AssignmentAdmin)


class ActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_description']
    pass
admin.site.register(Activity, ActivityAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_description']
    pass
admin.site.register(Location, LocationAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ('date', 'name', 'short_description')
    list_display_links = ('name',)
    pass
admin.site.register(Event, EventAdmin)
