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
    readonly_fields = ['duty', 'assigned_location', 'hh_service_location']
    extra = 0

    def has_add_permission(self, request):
        return False


class AssignmentChangeableInline(admin.TabularInline):
    model = Assignment
    readonly_fields = ['hh_service_location']
    extra = 0

    def has_add_permission(self, request):
        return False

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
    list_display = ['external_id', 'hh_location', 'names']
    fields = (('external_id', 'surnames'),)
    search_fields = ['external_id', 'volunteer__surname']
    list_filter = ['hh_location']
    change_list_template = "admin/change_list_filter_sidebar.html"
    readonly_fields = ['surnames']
admin.site.register(Family, FamilyAdmin)


class AttributeAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Attribute, AttributeAdmin)


class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'assignable_recipient_count',
                    'unassigned_recipient_count', 'volunteers_needed',
                    'volunteers_assigned', 'percent_assigned']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name', 'slug']
    filter_horizontal = ['events', 'locations', 'activities']
    fieldsets = ((None, {'fields': ('name', 'slug', 'from_address',
                                    'bcc_address'), }),
                 ('Recipient selection',
                  {'fields': ('events', 'locations', 'activities'), }),
                 ('Trigger By Date Inlines',
                  {'fields': (),
                   'classes': ('placeholder triggerbydate_set-group',)}),
                 ('Trigger By Assignment Inlines',
                  {'fields': (),
                   'classes': ('placeholder triggerbyassignment_set-group',)}),
                 ('Trigger By Event Inlines',
                  {'fields': (),
                   'classes': ('placeholder triggerbyevent_set-group',)}),
                 ('Recipient list',
                  {'fields': ('recipient_names', ),
                   'classes': ('grp-collapse grp-closed',),
                   })
                 )
    readonly_fields = ['recipient_names']
    inlines = [TriggerByDateInline, TriggerByAssignmentInline,
               TriggerByEventInline]
admin.site.register(Campaign, CampaignAdmin)


class VolunteerAdmin(admin.ModelAdmin):
    fields = ('title', 'first_name', 'surname', 'family', 'dear_name',
              'email_address', 'home_phone', 'mobile_phone', 'external_id',
              'last_summary_view', 'temporary_change', 'note', 'attributes')
    list_display = ['first_name', 'surname', 'title', 'family_link',
                    'email_address', 'home_phone', 'mobile_phone',
                    'attributes_list', 'temporary_change', 'last_summary_view']
    readonly_fields = ['attributes_list', 'last_summary_view']
    raw_id_fields = ['family']
    related_lookup_fields = {
        'fk': ['family'],
    }
    search_fields = ['slug', 'first_name', 'surname', 'family__external_id',
                     'external_id']
    list_filter = ['attributes', 'temporary_change', 'last_summary_view',
                   'attributes__activity', 'assignment__duty']
    filter_horizontal = ['attributes']
    inlines = [AssignmentInline]
    date_hierarchy = 'last_summary_view'
admin.site.register(Volunteer, VolunteerAdmin)


class VolunteerAdded(Volunteer):
    class Meta:
        proxy = True
        verbose_name_plural = "Recently added volunteers"


def _set_attribute(attribute_name, volunteer_queryset):
    attribute = Attribute.objects.get(name=attribute_name)
    for volunteer in volunteer_queryset:
        volunteer.attributes.add(attribute)


def add_attribute_adult(modeladmin, request, queryset):
    _set_attribute('adult', queryset)
add_attribute_adult.short_description = "Add 'adult' attribute"


def add_attribute_stewardable(modeladmin, request, queryset):
    _set_attribute('steward able', queryset)
add_attribute_stewardable.short_description = "Add 'steward able' attribute"


def add_attribute_securityable(modeladmin, request, queryset):
    _set_attribute('security able', queryset)
add_attribute_securityable.short_description = "Add 'security able' attribute"


class VolunteerAddedAdmin(VolunteerAdmin):
    list_display = ['created', 'first_name', 'surname', 'title', 'family_link',
                    'email_address', 'home_phone', 'mobile_phone',
                    'attributes_list', 'temporary_change']
    ordering = ('-created',)
    date_hierarchy = 'created'
    actions = [add_attribute_adult, add_attribute_securityable,
               add_attribute_stewardable]
    list_filter = []
admin.site.register(VolunteerAdded, VolunteerAddedAdmin)


class VolunteerNotModified(Volunteer):
    class Meta:
        proxy = True
        verbose_name_plural = "Recently (not) modified volunteers"


class VolunteerNotModifiedAdmin(VolunteerAdmin):
    list_display = ['modified', 'first_name', 'surname', 'title',
                    'family_link', 'email_address', 'home_phone',
                    'mobile_phone', 'attributes_list', 'temporary_change']
    ordering = ('modified',)
    date_hierarchy = 'modified'
    list_filter = []
admin.site.register(VolunteerNotModified, VolunteerNotModifiedAdmin)


class DutyAdmin(admin.ModelAdmin):
    list_display = ['id', 'event_is_visible_to_volunteers', 'activity', 'event',
                    'location', 'start_time', 'end_time', 'multiple',
                    'unassigned_count', 'coordinator_note', 'details']
    list_filter = ['event__is_visible_to_volunteers', 'activity', 'event',
                   'location', 'start_time', 'event__campaign']
    readonly_fields = ['unassigned_count']
    inlines = [AssignmentChangeableInline]
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
        return assignment.volunteer.family.get_hh_location_display()


class AssignmentAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('id', 'modified', 'volunteer', 'duty_link', 'assigned_location')
    list_filter = ['duty__activity', 'duty__event', 'duty__location',
                   'assigned_location', 'duty__start_time']
    date_hierarchy = 'modified'
    search_fields = ['volunteer__first_name', 'volunteer__surname']
    resource_class = AssignmentResource
    list_select_related = True
admin.site.register(Assignment, AssignmentAdmin)


class ActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'attributes_list', 'web_summary_description',
                    'assignment_message_description']
    readonly_fields = ['attributes_list']
    list_filter = ['attributes']
    change_list_template = "admin/change_list_filter_sidebar.html"
    filter_horizontal = ['attributes']
admin.site.register(Activity, ActivityAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'web_summary_description',
                    'assignment_message_description']
    pass
admin.site.register(Location, LocationAdmin)


def visible_to_volunteers_events(modeladmin, request, queryset):
    queryset.update(is_visible_to_volunteers=True)
visible_to_volunteers_events.short_description = "Make events visible to volunteers"


def not_visible_to_volunteers_events(modeladmin, request, queryset):
    queryset.update(is_visible_to_volunteers=False)
not_visible_to_volunteers_events.short_description = "Make events not visible to volunteers"


def archive_events(modeladmin, request, queryset):
    queryset.update(is_archived=True)
archive_events.short_description = "Archive events"


def unarchive_events(modeladmin, request, queryset):
    queryset.update(is_archived=False)
unarchive_events.short_description = "Unarchive events"


def copy_events(modeladmin, request, queryset):
    for event in queryset:
        event.create_deep_copy()
copy_events.short_description = "Copy events"


class EventAdmin(admin.ModelAdmin):
    list_display = ('date', 'name', 'is_visible_to_volunteers',
                    'web_summary_description',
                    'assignment_message_description')
    list_display_links = ('name',)
    list_filter = ['is_archived', 'is_visible_to_volunteers']
    date_hierarchy = 'date'
    change_list_template = "admin/change_list_filter_sidebar.html"
    inlines = [DutyInline]
    actions = [copy_events, visible_to_volunteers_events,
               not_visible_to_volunteers_events, archive_events,
               unarchive_events]
admin.site.register(Event, EventAdmin)


class MessageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Message, MessageAdmin)


class SendableAdmin(admin.ModelAdmin):
    list_display = ['send_date', 'sent_date', 'volunteer', 'assignment',
                    'trigger_detail', 'send_failed']
    list_filter = ['send_failed']
    change_list_template = "admin/change_list_filter_sidebar.html"
    date_hierarchy = 'send_date'
    search_fields = ['volunteer__first_name', 'volunteer__surname',
                     'volunteer__family__external_id',
                     'volunteer__external_id']
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
