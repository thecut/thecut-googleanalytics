from django import template
from django.contrib.sites.models import Site
from thecut.googleanalytics.models import AnalyticsWebProperty


register = template.Library()

@register.inclusion_tag('googleanalytics/_analytics_tracking_code.html',
    takes_context=True)
def analytics_tracking_code(context):
    """Google Analytics tracking code.
    
    http://code.google.com/apis/analytics/docs/tracking/asyncUsageGuide.html
    
    """
    request = context['request']
    site = Site.objects.get_current()
    try:
        analytics = AnalyticsWebProperty.objects.get(site=site)
    except AnalyticsWebProperty.DoesNotExist:
        analytics_enabled = False
        web_property_id = None
    else:
        analytics_enabled = analytics.is_enabled
        web_property_id = analytics.web_property_id
    return {'analytics_enabled': analytics_enabled,
        'web_property_id': web_property_id, 'request': request}

