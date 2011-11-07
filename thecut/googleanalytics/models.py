# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.db import models
from thecut.googleanalytics.managers import AnalyticsWebPropertyManager


class AnalyticsWebProperty(models.Model):
    """Google Analytics web property settings for a site.
    
    Google Analytics profiles can be created at:
    http://www.google.com/analytics/
    
    """
    site = models.OneToOneField('sites.Site', unique=True)
    web_property_id = models.CharField(max_length=25,
        help_text='Web Property ID is obtained when \
        <a href="http://www.google.com/analytics/" target="_new">\
        configuring the site profile in Google Analytics</a>.')
    is_enabled = models.BooleanField(default=False,
        help_text='Is Google Analytics tracking enabled on the website?')
    objects = AnalyticsWebPropertyManager()
    
    class Meta(object):
        ordering = ['site']
        verbose_name = 'web property'
        verbose_name_plural = 'web properties'
    
    def __unicode__(self):
        return self.site.name

