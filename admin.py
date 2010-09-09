from django.contrib import admin
from googleanalytics.models import AnalyticsWebProperty


class AnalyticsWebPropertyAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'web_property_id']

admin.site.register(AnalyticsWebProperty, AnalyticsWebPropertyAdmin)

