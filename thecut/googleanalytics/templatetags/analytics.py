# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import template
from django.contrib.sites.models import Site
from thecut.googleanalytics.models import Profile


register = template.Library()


@register.inclusion_tag('googleanalytics/_analytics_tracking_code.html',
                        takes_context=True)
def analytics_tracking_code(context):
    """Google Analytics tracking code.

    http://code.google.com/apis/analytics/docs/tracking/asyncUsageGuide.html

    """

    try:
        analytics = Profile.objects.get_current()
    except Profile.DoesNotExist:
        analytics_enabled = False
        web_property_id = None
        display_features = False
    else:
        analytics_enabled = analytics.is_enabled
        web_property_id = analytics.web_property_id
        display_features = analytics.display_features

    try:
        current_site = Site.objects.get_current()
    except Site.DoesNotExist:
        current_site = None

    return {'analytics_enabled': analytics_enabled,
            'web_property_id': web_property_id,
            'display_features': display_features,
            'current_site': current_site,
            'request': context.get('request')}
