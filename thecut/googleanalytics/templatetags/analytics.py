# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import template
from thecut.googleanalytics.models import Profile


register = template.Library()

@register.inclusion_tag('googleanalytics/_analytics_tracking_code.html',
    takes_context=True)
def analytics_tracking_code(context):
    """Google Analytics tracking code.
    
    http://code.google.com/apis/analytics/docs/tracking/asyncUsageGuide.html
    
    """
    request = context['request']
    try:
        analytics = Profile.objects.get_current()
    except Profile.DoesNotExist:
        analytics_enabled = False
        web_property_id = None
    else:
        analytics_enabled = analytics.is_enabled
        web_property_id = analytics.web_property_id
    return {'analytics_enabled': analytics_enabled,
        'web_property_id': web_property_id, 'request': request}

