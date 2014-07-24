from django.contrib import admin
from models import Attribute, Campaign, Duty, Volunteer


class DutyInline(admin.StackedInline):
    model = Duty
    extra = 10


class AttributeAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Attribute, AttributeAdmin)


class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [DutyInline]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name', 'slug']
admin.site.register(Campaign, CampaignAdmin)


class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'external_id', 'slug']
    readonly_fields = ['assignable_duty_names', 'assigned_duty_names',
                       'slug']
    fields = ['name', 'phone_number', 'external_id', 'slug',
              'assignable_duty_names', 'assigned_duty_names', 'attributes']
    search_fields = ['name', 'external_id', 'slug']
admin.site.register(Volunteer, VolunteerAdmin)


class DutyAdmin(admin.ModelAdmin):
    list_display = ['name', 'campaign', 'assigned_to']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name', 'slug']
admin.site.register(Duty, DutyAdmin)
