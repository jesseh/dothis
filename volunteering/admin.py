from django.contrib import admin
from models import (Assignment, Attribute, Campaign, CampaignDuty, Duty,
                    Volunteer)


class DutyInline(admin.StackedInline):
    model = Duty
    extra = 10
    prepopulated_fields = {"slug": ("name",)}


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
    list_display = ['name']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name', 'slug']
admin.site.register(Duty, DutyAdmin)


class CampaignDutyAdmin(admin.ModelAdmin):
    pass
admin.site.register(CampaignDuty, CampaignDutyAdmin)


class AssignmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Assignment, AssignmentAdmin)
