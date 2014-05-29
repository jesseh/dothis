from django.contrib import admin
from models import Campaign, Duty, Volunteer


class DutyInline(admin.StackedInline):
    model = Duty


class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [DutyInline]
admin.site.register(Campaign, CampaignAdmin)


class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['name']
    readonly_fields = ['assignable_duties']
    fields = ['name', 'assignable_duties']
admin.site.register(Volunteer, VolunteerAdmin)


class DutyAdmin(admin.ModelAdmin):
    list_display = ('name', 'campaign', 'assigned_to')
admin.site.register(Duty, DutyAdmin)
