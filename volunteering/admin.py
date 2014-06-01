from django.contrib import admin
from models import Campaign, Duty, Volunteer


class DutyInline(admin.StackedInline):
    model = Duty
    extra = 10


class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [DutyInline]
admin.site.register(Campaign, CampaignAdmin)


class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'external_id']
    readonly_fields = ['assignable_duty_names', 'assigned_duty_names']
    fields = ['name', 'assignable_duty_names', 'assigned_duty_names']
admin.site.register(Volunteer, VolunteerAdmin)


class DutyAdmin(admin.ModelAdmin):
    list_display = ['name', 'campaign', 'assigned_to']
admin.site.register(Duty, DutyAdmin)
