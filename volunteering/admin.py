from django.contrib import admin
from models import (Activity, Assignment, Attribute, Campaign, Duty, Event,
                    Family, Location, Message, Trigger, Volunteer)


class DutyInline(admin.StackedInline):
    model = Duty
    extra = 10


class AssignmentInline(admin.StackedInline):
    model = Assignment
    extra = 0


class VolunteerInline(admin.StackedInline):
    model = Volunteer
    fields = (('title', 'first_name', 'surname', 'dear_name'),
              ('email_address', 'home_phone', 'mobile_phone'),
              'attributes',
              'slug')
    readonly_fields = ['slug']


class FamilyAdmin(admin.ModelAdmin):
    inlines = [VolunteerInline]
admin.site.register(Family, FamilyAdmin)


class AttributeAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Attribute, AttributeAdmin)


class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name', 'slug']
    filter_horizontal = ['events', 'locations', 'activities']
admin.site.register(Campaign, CampaignAdmin)


class VolunteerAdmin(admin.ModelAdmin):
    fields = ('family',
              ('title', 'first_name', 'surname', 'dear_name'),
              ('email_address', 'home_phone', 'mobile_phone'),
              'attributes')
    list_display = ['slug', 'external_id', 'title', 'first_name', 'surname',
                    'dear_name', 'email_address', 'home_phone', 'mobile_phone',
                    'attributes_list']
    readonly_fields = ['attributes_list']
    search_fields = ['slug', 'first_name', 'surname', 'family__external_id',
                     'external_id']
    list_filter = ['attributes']
admin.site.register(Volunteer, VolunteerAdmin)


class DutyAdmin(admin.ModelAdmin):
    list_display = ['id', 'activity', 'event', 'location',
                    'start_time', 'end_time', 'multiple', 'unassigned_count']
    list_filter = ['activity', 'event', 'location', 'start_time']
    readonly_fields = ['unassigned_count']
    inlines = [AssignmentInline]
admin.site.register(Duty, DutyAdmin)


class AssignmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Assignment, AssignmentAdmin)


class ActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'attributes_list']
    readonly_fields = ['attributes_list']
    list_filter = ['attributes']
admin.site.register(Activity, ActivityAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    pass
admin.site.register(Location, LocationAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ('date', 'name', 'description')
    list_display_links = ('name',)
admin.site.register(Event, EventAdmin)


class MessageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Message, MessageAdmin)


class TriggerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('campaign', 'message')
        }),
        ('When to send', {
            'fields': ('fixed_date', 'days_before_event',
                       'days_after_assignment')
        }),
    )
    list_display = ['campaign', 'message', 'fixed_date', 'days_before_event',
                    'days_after_assignment']
admin.site.register(Trigger, TriggerAdmin)
