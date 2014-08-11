from django.contrib import admin
from models import (Activity, Assignment, Attribute, Campaign, Duty, Event,
                    Family, Location, Message, Trigger, Volunteer, Sendable)


class DutyInline(admin.TabularInline):
    model = Duty
    readonly_fields = ['unassigned_count']
    extra = 0


class AssignmentInline(admin.StackedInline):
    model = Assignment
    extra = 0


TRIGGER_FIELDSETS = (
    (None,
     {'fields': ('message',)}),
    ('Send on a fixed date',
     {'fields': ('fixed_date', 'fixed_assignment_state')}),
    ('Send before the event',
     {'fields': ('event_based_days_before',
                 'event_based_assignment_state')}),
    ('Send after the volunteer was assigned the duty',
     {'fields': ('assignment_based_days_after',)}),
    )


class TriggerInline(admin.StackedInline):
    model = Trigger
    extra = 0
    fieldsets = TRIGGER_FIELDSETS


class VolunteerInline(admin.StackedInline):
    model = Volunteer
    fields = (('title', 'first_name', 'surname', 'dear_name'),
              ('email_address', 'home_phone', 'mobile_phone'),
              'attributes', 'note',
              'slug')
    readonly_fields = ['slug']
    filter_horizontal = ['attributes']
    extra = 0


class FamilyAdmin(admin.ModelAdmin):
    inlines = [VolunteerInline]
    list_display = ['external_id', 'names']
    fields = (('external_id', 'surnames'),)
    search_fields = ['external_id', 'volunteer__surname']
    readonly_fields = ['surnames']
admin.site.register(Family, FamilyAdmin)


class AttributeAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Attribute, AttributeAdmin)


class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'recipient_count', 'volunteers_needed',
                    'volunteers_assigned', 'percent_assigned']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name', 'slug']
    filter_horizontal = ['events', 'locations', 'activities']
    fieldsets = ((None,
                  {'fields': ('name', 'slug'), }),
                 ('Recipient selection',
                  {'fields': ('events', 'locations', 'activities'), }),
                 ('Recipient list',
                  {'fields': ('recipient_names', ),
                   'classes': ('collapse', ),
                   })
                 )
    readonly_fields = ['recipient_names']
    inlines = [TriggerInline]
admin.site.register(Campaign, CampaignAdmin)


class VolunteerAdmin(admin.ModelAdmin):
    fields = ('family',
              ('title', 'first_name', 'surname', 'dear_name'),
              ('email_address', 'home_phone', 'mobile_phone'),
              'note', 'attributes')
    list_display = ['slug', 'external_id', 'title', 'first_name', 'surname',
                    'dear_name', 'family_link', 'email_address', 'home_phone',
                    'mobile_phone', 'attributes_list']
    readonly_fields = ['attributes_list']
    search_fields = ['slug', 'first_name', 'surname', 'family__external_id',
                     'external_id']
    list_filter = ['attributes']
    filter_horizontal = ['attributes']
    inlines = [AssignmentInline]
admin.site.register(Volunteer, VolunteerAdmin)


class DutyAdmin(admin.ModelAdmin):
    list_display = ['id', 'activity', 'event', 'location', 'start_time',
                    'end_time', 'multiple', 'unassigned_count',
                    'coordinator_note', 'details']
    list_filter = ['activity', 'event', 'location', 'start_time']
    readonly_fields = ['unassigned_count']
    inlines = [AssignmentInline]
admin.site.register(Duty, DutyAdmin)


class DutyEditable(Duty):
    class Meta:
        proxy = True
        verbose_name_plural = "Duties (editable)"


class DutyEditableAdmin(DutyAdmin):
    list_editable = ['location', 'multiple', 'start_time', 'end_time',
                     'coordinator_note', 'details']
admin.site.register(DutyEditable, DutyEditableAdmin)


class AssignmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Assignment, AssignmentAdmin)


class ActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'attributes_list']
    readonly_fields = ['attributes_list']
    list_filter = ['attributes']
    filter_horizontal = ['attributes']
admin.site.register(Activity, ActivityAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    pass
admin.site.register(Location, LocationAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ('date', 'name', 'description')
    list_display_links = ('name',)
    inlines = [DutyInline]
admin.site.register(Event, EventAdmin)


class MessageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Message, MessageAdmin)


class TriggerAdmin(admin.ModelAdmin):
    fieldsets = TRIGGER_FIELDSETS
    list_display = ['campaign', 'message', 'fixed_date',
                    'fixed_assignment_state', 'event_based_days_before',
                    'event_based_assignment_state',
                    'assignment_based_days_after']
admin.site.register(Trigger, TriggerAdmin)


class SendableAdmin(admin.ModelAdmin):
    list_display = ['send_date', 'trigger', 'volunteer', 'assignment',
                    'sent_date', 'send_failed']
    list_filter = ['send_failed', 'trigger']
    date_hierarchy = 'send_date'
admin.site.register(Sendable, SendableAdmin)
