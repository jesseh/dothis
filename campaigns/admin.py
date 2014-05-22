from django.contrib import admin
from campaigns.models import Campaign, Duty


class DutyInline(admin.StackedInline):
    model = Duty


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = (DutyInline,)
admin.site.register(Campaign, CampaignAdmin)
