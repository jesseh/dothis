from django.contrib import admin

from import_export.admin import ExportMixin
from import_export.resources import ModelResource
from import_export import fields

from models import (Activity, Assignment, Attribute, Campaign, Duty, Event,
                    Family, Location, Message, TriggerByDate, Volunteer,
                    Sendable, TriggerByAssignment, TriggerByEvent)


class DutyInline(admin.TabularInline):
    model = Duty
    readonly_fields = ['unassigned_count']
    extra = 0


class AssignmentInline(admin.TabularInline):
    model = Assignment
    readonly_fields = ['hh_service_location']
    extra = 0


TRIGGER_FIELDSETS = (
    (None,
     {'fields': ('message',)}),
    ('Send on a fixed date',
     {'fields': ('fixed_date', 'assignment_state')}),
    )


class TriggerByDateInline(admin.TabularInline):
    model = TriggerByDate
    extra = 0


class TriggerByAssignmentInline(admin.TabularInline):
    model = TriggerByAssignment
    extra = 0


class TriggerByEventInline(admin.TabularInline):
    model = TriggerByEvent
    extra = 0


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
    list_display = ['external_id', 'hh_location_2014', 'names']
    fields = (('external_id', 'surnames'),)
    search_fields = ['external_id', 'volunteer__surname']
    list_filter = ['hh_location_2014']
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
    inlines = [TriggerByDateInline, TriggerByAssignmentInline,
               TriggerByEventInline]
admin.site.register(Campaign, CampaignAdmin)


class VolunteerAdmin(admin.ModelAdmin):
    fields = (('family', 'external_id', 'last_summary_view',),
              ('title', 'first_name', 'surname', 'dear_name'),
              ('email_address', 'home_phone', 'mobile_phone'),
              'note', 'temporary_change', 'attributes')
    list_display = ['slug', 'external_id', 'title', 'first_name', 'surname',
                    'dear_name', 'family_link', 'email_address', 'home_phone',
                    'mobile_phone', 'attributes_list', 'temporary_change',
                    'last_summary_view']
    readonly_fields = ['attributes_list', 'last_summary_view']
    search_fields = ['slug', 'first_name', 'surname', 'family__external_id',
                     'external_id']
    list_filter = ['attributes', 'temporary_change', 'last_summary_view']
    filter_horizontal = ['attributes']
    inlines = [AssignmentInline]
    date_hierarchy = 'last_summary_view'
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


class AssignmentResource(ModelResource):
    event = fields.Field(column_name='event',
                         attribute='duty__event__name')
    event_date = fields.Field(column_name='event date',
                              attribute='duty__event__date')
    activity = fields.Field(column_name='activity',
                            attribute='duty__activity__name')
    location = fields.Field(column_name='location',
                            attribute='duty__location__name')
    assigned_location = fields.Field(column_name='assigned location',
                                     attribute='assigned_location__name')
    start_time = fields.Field(column_name='start time',
                              attribute='duty__start_time')
    end_time = fields.Field(column_name='end time',
                            attribute='duty__end_time')
    volunteer = fields.Field(column_name='volunteer')
    mobile_phone = fields.Field(column_name='mobile phone',
                                attribute='volunteer__mobile_phone')
    home_phone = fields.Field(column_name='home phone',
                              attribute='volunteer__home_phone')
    email_address = fields.Field(column_name='email address',
                                 attribute='volunteer__email_address')
    hh_service_location = fields.Field(column_name='hh_service_location')

    class Meta:
        model = Assignment
        fields = []

    def dehydrate_volunteer(self, assignment):
        return str(assignment.volunteer)

    def dehydrate_hh_service_location(self, assignment):
        return assignment.volunteer.family.get_hh_location_2014_display()


class AssignmentAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('id', 'volunteer', 'duty_link', 'assigned_location')
    list_filter = ['duty__activity', 'duty__event', 'duty__location',
                   'assigned_location', 'duty__start_time']
    resource_class = AssignmentResource
    list_select_related = True
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


class SendableAdmin(admin.ModelAdmin):
    list_display = ['send_date', 'volunteer', 'assignment',
                    'trigger_detail', 'send_failed']
    list_filter = ['send_failed']
    date_hierarchy = 'send_date'
    actions = ['send_message']

    def send_message(self, request, queryset):
        sent_count = 0
        for sendable in queryset:
            sendable.send_email()
            sent_count += 1
        if sent_count == 1:
            message_bit = "1 message was"
        else:
            message_bit = "%s messages were" % sent_count
        self.message_user(request, "%s sent." % message_bit)
    send_message.short_description = "Send (or resend) the message"


admin.site.register(Sendable, SendableAdmin)
