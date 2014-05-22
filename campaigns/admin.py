from django.contrib import admin
from campaigns.models import Campaign

class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Campaign, CampaignAdmin)
