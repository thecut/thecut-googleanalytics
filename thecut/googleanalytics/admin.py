# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib import admin
from thecut.googleanalytics.models import AnalyticsWebProperty


class AnalyticsWebPropertyAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'web_property_id']

admin.site.register(AnalyticsWebProperty, AnalyticsWebPropertyAdmin)

